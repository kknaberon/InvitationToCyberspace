"""Phase4: 教師あり学習で「次に置くカードと場所」を予測する処理。"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import random
from typing import Iterable

from .battle import BattleState, Move, Owner
from .cards import Card, CardPool, build_default_card_pool
from .number_guess import resolve_number_guess


@dataclass(frozen=True, slots=True)
class TrainingExample:
    """教師あり学習で使う、1手ぶんの教師データ。"""

    # state: 手を選ぶ直前のバトル状態です。
    state: BattleState

    # expert_move: ヒューリスティック教師AIが選んだ正解手です。
    expert_move: Move


@dataclass(frozen=True, slots=True)
class TrainingReport:
    """学習結果の簡単な集計。"""

    # examples: 学習に使った手番数です。1戦につき最大9件です。
    examples: int

    # epochs: 同じ教師データを何周学習したかです。
    epochs: int

    # final_accuracy: 学習データに対して教師手を再現できた割合です。
    final_accuracy: float

    # weight_count: 学習済み重みの個数です。
    weight_count: int


@dataclass(frozen=True, slots=True)
class HeuristicTeacher:
    """人間の代わりに教師データを作る、簡易攻略AI。

    この教師は完璧な攻略AIではありません。
    ただし「置いた直後に何枚取れるか」「最終スコアが良くなるか」
    「中央や角を取れているか」を見て選ぶため、完全ランダムよりは筋のある手を作れます。
    """

    # reply_penalty_weight: 相手の次の最善手をどれくらい警戒するかです。
    # 0.0なら従来どおり1手先だけ見ます。値を上げると、取られ返しを避けやすくなります。
    reply_penalty_weight: float = 0.0

    def choose_move(self, state: BattleState, rng: random.Random) -> Move:
        """現在の合法手を評価し、最も良い手を1つ返します。"""

        # legal_moves: 今の手番プレイヤーが選べる全候補です。
        legal_moves = state.legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves are available")

        # best_score: 現時点で最も高い評価値です。
        best_score: float | None = None

        # best_moves: 同点1位の手をすべて入れます。最後にランダムで1つ選びます。
        best_moves: list[Move] = []

        for move in legal_moves:
            score = self.score_move(state, move)
            if best_score is None or score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return rng.choice(best_moves)

    def score_move(self, state: BattleState, move: Move) -> float:
        """1手を仮に打ったあとの状態を評価します。"""

        # owner: この手を打つプレイヤーです。
        owner = move.owner

        # before_owned: 手を打つ前にownerが盤面上で持っているカード枚数です。
        before_owned = _owned_board_count(state, owner)

        # next_state: 仮にmoveを打ったあとの状態です。
        next_state = state.apply_move(move)

        # after_owned: 手を打ったあとにownerが盤面上で持っているカード枚数です。
        after_owned = _owned_board_count(next_state, owner)

        # captured_or_placed_gain: 置いたカード1枚ぶんも含めて、盤面所有枚数が何枚増えたかです。
        captured_or_placed_gain = after_owned - before_owned

        # scores: 後攻未使用手札も含めた、その時点のスコアです。
        scores = next_state.score()

        # score_diff: 自分から見たスコア差です。プラスなら有利です。
        score_diff = scores[owner] - scores[owner.opponent]

        # card: 今置こうとしているカードです。
        card = state.hand_for_owner(owner)[move.hand_index]

        # position_bonus: 中央や角など、置き場所のざっくりした価値です。
        position_bonus = _position_bonus(move.position)

        # card_strength: カード自体の平均値です。強いカードほど少しだけ高く評価します。
        card_strength = _card_average(card) / 10.0

        # 基本評価です。捕獲できる手を強めに、スコア差と置き場所を次に重視します。
        score = (captured_or_placed_gain * 4.0) + (score_diff * 1.5) + position_bonus + card_strength

        # 相手の返し手がある場合、その中で一番痛い手を少し差し引きます。
        # これにより「今は1枚取れるが、直後に2枚取り返される」ような手を避けやすくします。
        if self.reply_penalty_weight and not next_state.is_over:
            opponent_best_reply = max(
                self._score_without_reply(next_state, reply)
                for reply in next_state.legal_moves()
            )
            score -= opponent_best_reply * self.reply_penalty_weight

        # ゲームが終わる手なら、実際の勝敗を非常に強く評価します。
        if next_state.is_over:
            winner = next_state.winner()
            if winner is owner:
                score += 100.0
            elif winner is owner.opponent:
                score -= 100.0

        return score

    def _score_without_reply(self, state: BattleState, move: Move) -> float:
        """相手の返し手までは見ず、1手だけの評価値を返します。"""

        owner = move.owner
        before_owned = _owned_board_count(state, owner)
        next_state = state.apply_move(move)
        after_owned = _owned_board_count(next_state, owner)
        captured_or_placed_gain = after_owned - before_owned
        scores = next_state.score()
        score_diff = scores[owner] - scores[owner.opponent]
        card = state.hand_for_owner(owner)[move.hand_index]

        score = (
            (captured_or_placed_gain * 4.0)
            + (score_diff * 1.5)
            + _position_bonus(move.position)
            + (_card_average(card) / 10.0)
        )
        if next_state.is_over:
            winner = next_state.winner()
            if winner is owner:
                score += 100.0
            elif winner is owner.opponent:
                score -= 100.0
        return score


@dataclass(slots=True)
class LinearMoveModel:
    """候補手ごとに点数を付け、一番高い手を選ぶ線形モデル。"""

    # weights: 特徴量名ごとの重みです。学習によって増減します。
    weights: dict[str, float]

    def score_move(self, state: BattleState, move: Move) -> float:
        """状態と候補手から特徴量を作り、モデルの点数を計算します。"""

        # features: この候補手を説明する数値特徴量です。
        features = extract_move_features(state, move)
        return sum(self.weights.get(name, 0.0) * value for name, value in features.items())

    def predict_move(self, state: BattleState) -> Move:
        """現在状態で、モデルが最も良いと思う合法手を返します。"""

        # legal_moves: モデルが選べる候補手です。
        legal_moves = state.legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves are available")

        return max(legal_moves, key=lambda move: self.score_move(state, move))

    def save(self, path: str | Path) -> None:
        """学習済みモデルをJSONファイルへ保存します。"""

        # path: 保存先です。親フォルダがなければ作ります。
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"weights": self.weights}, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "LinearMoveModel":
        """JSONファイルから学習済みモデルを読み込みます。"""

        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(weights={name: float(value) for name, value in data["weights"].items()})


def train_supervised_model(
    examples: Iterable[TrainingExample],
    epochs: int = 6,
    learning_rate: float = 0.2,
) -> tuple[LinearMoveModel, TrainingReport]:
    """ヒューリスティック教師の手を真似する線形モデルを学習します。"""

    if epochs < 1:
        raise ValueError("epochs must be at least 1")

    # example_list: 同じ教師データを複数epochで使うため、リスト化します。
    example_list = list(examples)
    if not example_list:
        raise ValueError("examples must not be empty")

    # model: 最初は重みゼロのモデルです。
    model = LinearMoveModel(weights={})

    for _ in range(epochs):
        for example in example_list:
            predicted_move = model.predict_move(example.state)

            # 予測が教師手と違うときだけ、教師手の特徴を上げ、誤予測手の特徴を下げます。
            if predicted_move != example.expert_move:
                _add_scaled_features(
                    model.weights,
                    extract_move_features(example.state, example.expert_move),
                    learning_rate,
                )
                _add_scaled_features(
                    model.weights,
                    extract_move_features(example.state, predicted_move),
                    -learning_rate,
                )

    accuracy = evaluate_model_accuracy(model, example_list)
    report = TrainingReport(
        examples=len(example_list),
        epochs=epochs,
        final_accuracy=accuracy,
        weight_count=len(model.weights),
    )
    return model, report


def evaluate_model_accuracy(model: LinearMoveModel, examples: Iterable[TrainingExample]) -> float:
    """教師データに対して、モデルが教師手を選べる割合を計算します。"""

    # total: 評価した手番数です。
    total = 0

    # correct: 教師手とモデル予測が一致した数です。
    correct = 0

    for example in examples:
        total += 1
        if model.predict_move(example.state) == example.expert_move:
            correct += 1

    return correct / total if total else 0.0


def generate_teacher_examples(
    games: int = 1_000,
    seed: int | None = None,
    pool: CardPool | None = None,
) -> list[TrainingExample]:
    """ヒューリスティック教師AI同士の対戦から教師データを作ります。"""

    if games < 1:
        raise ValueError("games must be at least 1")

    # rng: seed指定で、同じ教師データを再現できます。
    rng = random.Random(seed)

    # pool: 100枚カード定義です。
    pool = pool or build_default_card_pool()

    # teacher: 人間の代わりに正解手を出すヒューリスティックAIです。
    teacher = HeuristicTeacher()

    # examples: 全対戦から集めた教師データです。
    examples: list[TrainingExample] = []

    for _ in range(games):
        state = _start_random_training_battle(pool=pool, rng=rng)

        # 1戦9手ぶん、教師AIの選んだ手を記録します。
        while not state.is_over:
            expert_move = teacher.choose_move(state, rng)
            examples.append(TrainingExample(state=state, expert_move=expert_move))
            state = state.apply_move(expert_move)

    return examples


def train_and_save_supervised_model(
    model_path: str | Path,
    games: int = 1_000,
    seed: int | None = None,
    epochs: int = 6,
    learning_rate: float = 0.2,
) -> TrainingReport:
    """教師データ生成、学習、モデル保存をまとめて実行します。"""

    examples = generate_teacher_examples(games=games, seed=seed)
    model, report = train_supervised_model(
        examples=examples,
        epochs=epochs,
        learning_rate=learning_rate,
    )
    model.save(model_path)
    return report


def extract_move_features(state: BattleState, move: Move) -> dict[str, float]:
    """状態と候補手を、学習モデルが扱える数値特徴量へ変換します。"""

    # owner: 候補手を打つ側です。
    owner = move.owner

    # card: 候補手で出すカードです。
    card = state.hand_for_owner(owner)[move.hand_index]

    # next_state: 候補手を1手だけ仮適用した状態です。
    next_state = state.apply_move(move)

    # scores: 仮適用後のスコアです。
    scores = next_state.score()

    # before_owned/after_owned: 盤面上の所有カード枚数の変化を見ます。
    before_owned = _owned_board_count(state, owner)
    after_owned = _owned_board_count(next_state, owner)

    # row/col: 0から8のpositionを3x3の行・列へ変換します。
    row, col = divmod(move.position, 3)

    # adjacent_counts: 置き先の上下左右に、自分・相手・空きがいくつあるかです。
    adjacent_counts = _adjacent_owner_counts(state, move.position, owner)

    features = {
        "bias": 1.0,
        "turn_index": state.move_count / 8.0,
        "is_blue": 1.0 if owner is Owner.BLUE else 0.0,
        "is_red": 1.0 if owner is Owner.RED else 0.0,
        "is_first_player": 1.0 if owner is state.first_player else 0.0,
        "is_second_player": 1.0 if owner is state.second_player else 0.0,
        "self_hand_count": len(state.hand_for_owner(owner)) / 5.0,
        "opponent_hand_count": len(state.hand_for_owner(owner.opponent)) / 5.0,
        "self_board_count": _owned_board_count(state, owner) / 9.0,
        "opponent_board_count": _owned_board_count(state, owner.opponent) / 9.0,
        "card_grade": card.grade / 4.0,
        "card_top": card.top / 10.0,
        "card_right": card.right / 10.0,
        "card_bottom": card.bottom / 10.0,
        "card_left": card.left / 10.0,
        "card_average": _card_average(card) / 10.0,
        "position": move.position / 8.0,
        "row": row / 2.0,
        "col": col / 2.0,
        "is_center": 1.0 if move.position == 4 else 0.0,
        "is_corner": 1.0 if move.position in {0, 2, 6, 8} else 0.0,
        "is_edge": 1.0 if move.position in {1, 3, 5, 7} else 0.0,
        "adjacent_self": adjacent_counts["self"] / 4.0,
        "adjacent_opponent": adjacent_counts["opponent"] / 4.0,
        "adjacent_empty": adjacent_counts["empty"] / 4.0,
        "ownership_gain": (after_owned - before_owned) / 5.0,
        "score_diff_after": (scores[owner] - scores[owner.opponent]) / 10.0,
        "wins_immediately": 1.0 if next_state.is_over and next_state.winner() is owner else 0.0,
        "loses_immediately": 1.0 if next_state.is_over and next_state.winner() is owner.opponent else 0.0,
    }
    return features


def _start_random_training_battle(pool: CardPool, rng: random.Random) -> BattleState:
    """教師データ用に、数当て・手札配布・先攻決定をランダムに行います。"""

    # guess: 青側の数当て入力です。
    guess = f"{rng.randrange(10_000):04d}"

    # guess_result: 数当て結果です。青側カードグレードに使います。
    guess_result = resolve_number_guess(guess=guess, rng=rng)

    # blue_hand/red_hand: 対戦開始時の手札です。
    blue_hand = pool.draw_player_hand(guess_result.grade, rng)
    red_hand = pool.draw_cpu_hand(rng)

    # first_player: 先攻をランダムに決めます。
    first_player = rng.choice([Owner.BLUE, Owner.RED])

    return BattleState.start(
        blue_hand=blue_hand,
        red_hand=red_hand,
        first_player=first_player,
        rng=rng,
    )


def _add_scaled_features(
    weights: dict[str, float],
    features: dict[str, float],
    scale: float,
) -> None:
    """重み辞書へ、特徴量ベクトルを指定倍率で足し込みます。"""

    for name, value in features.items():
        weights[name] = weights.get(name, 0.0) + (value * scale)


def _owned_board_count(state: BattleState, owner: Owner) -> int:
    """盤面上で、指定プレイヤーが所有しているカード枚数を数えます。"""

    return sum(1 for cell in state.board if cell is not None and cell.owner is owner)


def _card_average(card: Card) -> float:
    """カードの上下左右の平均値を返します。"""

    return (card.top + card.right + card.bottom + card.left) / 4.0


def _position_bonus(position: int) -> float:
    """ざっくりした置き場所の価値を返します。"""

    if position == 4:
        return 0.6
    if position in {0, 2, 6, 8}:
        return 0.35
    return 0.15


def _adjacent_owner_counts(state: BattleState, position: int, owner: Owner) -> dict[str, int]:
    """指定マスの上下左右にある、自分・相手・空きの数を数えます。"""

    counts = {"self": 0, "opponent": 0, "empty": 0}

    for neighbor_position in _neighbor_positions(position):
        cell = state.board[neighbor_position]
        if cell is None:
            counts["empty"] += 1
        elif cell.owner is owner:
            counts["self"] += 1
        else:
            counts["opponent"] += 1

    return counts


def _neighbor_positions(position: int) -> list[int]:
    """0から8の盤面位置について、上下左右の隣接位置を返します。"""

    row, col = divmod(position, 3)
    positions: list[int] = []
    if row > 0:
        positions.append(position - 3)
    if col < 2:
        positions.append(position + 1)
    if row < 2:
        positions.append(position + 3)
    if col > 0:
        positions.append(position - 1)
    return positions
