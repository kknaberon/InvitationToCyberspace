"""Phase5: 学習済みAIとランダムAIを対戦させ、勝率を測る処理。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random

from .battle import BattleState, Move, Owner
from .cards import CardPool, build_default_card_pool
from .number_guess import resolve_number_guess
from .phase4_ml import HeuristicTeacher, LinearMoveModel
from .random_ai import RandomAgent


@dataclass(frozen=True, slots=True)
class ModelAgent:
    """Phase4で学習したモデルを使って手を選ぶAI。

    モデルの点数だけだと、明らかな取り返されや終盤の勝敗を見落とすことがあります。
    そこでPhase5では、モデル点に戦術評価を少し混ぜて「現在のAI」を底上げします。
    """

    # owner: このAIが担当する色です。
    owner: Owner

    # model: Phase4で学習済みの線形モデルです。
    model: LinearMoveModel

    # tactical_weight: 戦術評価をどれくらい混ぜるかです。
    # 0.0にするとPhase4モデルそのもの、値を上げると盤面評価をより重視します。
    tactical_weight: float = 0.8

    # reply_penalty_weight: 相手の次の返し手をどれくらい警戒するかです。
    reply_penalty_weight: float = 0.25

    def choose_move(self, state: BattleState, rng: random.Random) -> Move:
        """現在状態から、モデルが最も良いと判断した手を返します。"""

        # rng: ランダムAIと同じ形のインターフェースにするため受け取っています。
        # モデルAIは決定的に手を選ぶので、この値は使いません。
        _ = rng

        if state.turn is not self.owner:
            raise ValueError(f"It is {state.turn.value}'s turn, not {self.owner.value}'s")

        # evaluator: 捕獲枚数、スコア差、置き場所、相手の返し手を評価する戦術AIです。
        evaluator = HeuristicTeacher(reply_penalty_weight=self.reply_penalty_weight)

        # legal_moves: 現在の全候補手です。
        legal_moves = state.legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves are available")

        # モデル点 + 戦術点の合計が一番高い手を選びます。
        return max(
            legal_moves,
            key=lambda move: self._combined_score(state, move, evaluator),
        )

    def _combined_score(
        self,
        state: BattleState,
        move: Move,
        evaluator: HeuristicTeacher,
    ) -> float:
        """モデル点と戦術評価を合算した手の点数を返します。"""

        model_score = self.model.score_move(state, move)
        tactical_score = evaluator.score_move(state, move)
        return model_score + (tactical_score * self.tactical_weight)


@dataclass(frozen=True, slots=True)
class Phase5BattleResult:
    """学習済みAI vs ランダムAIの1戦分の結果。"""

    # battle_index: 何戦目かです。
    battle_index: int

    # learned_owner: 学習済みAIが担当した色です。
    learned_owner: Owner

    # first_player: その対戦で先攻だった色です。
    first_player: Owner

    # player_grade: 青側の数当て結果から決まったカードグレードです。
    player_grade: int

    # winner: 勝者です。同点ならNoneです。
    winner: Owner | None

    # blue_score/red_score: 後攻の未使用手札を含めた最終スコアです。
    blue_score: int
    red_score: int

    # moves_played: 盤面に置かれた枚数です。通常は9になります。
    moves_played: int

    @property
    def learned_won(self) -> bool:
        """学習済みAIが勝ったかどうかを返します。"""

        return self.winner is self.learned_owner

    @property
    def random_won(self) -> bool:
        """ランダムAIが勝ったかどうかを返します。"""

        return self.winner is self.learned_owner.opponent


@dataclass(frozen=True, slots=True)
class Phase5EvaluationSummary:
    """学習済みAI vs ランダムAIの複数戦集計。"""

    # games: 対戦数です。
    games: int

    # learned_owner: 学習済みAIが担当した色です。
    learned_owner: Owner

    # learned_wins/random_wins/draws: 学習済みAI勝ち、ランダムAI勝ち、引き分けの回数です。
    learned_wins: int
    random_wins: int
    draws: int

    # learned_first_games/learned_first_wins: 学習済みAIが先攻だった試合数と勝利数です。
    learned_first_games: int
    learned_first_wins: int

    # learned_second_games/learned_second_wins: 学習済みAIが後攻だった試合数と勝利数です。
    learned_second_games: int
    learned_second_wins: int

    # grade_counts: 青側の数当てグレードが何回出たかです。
    grade_counts: dict[int, int]

    @property
    def learned_win_rate(self) -> float:
        """学習済みAIの勝率を0.0から1.0で返します。"""

        return self.learned_wins / self.games if self.games else 0.0

    @property
    def random_win_rate(self) -> float:
        """ランダムAIの勝率を0.0から1.0で返します。"""

        return self.random_wins / self.games if self.games else 0.0

    @property
    def draw_rate(self) -> float:
        """引き分け率を0.0から1.0で返します。"""

        return self.draws / self.games if self.games else 0.0

    @property
    def learned_first_win_rate(self) -> float:
        """学習済みAIが先攻だった試合だけの勝率です。"""

        if not self.learned_first_games:
            return 0.0
        return self.learned_first_wins / self.learned_first_games

    @property
    def learned_second_win_rate(self) -> float:
        """学習済みAIが後攻だった試合だけの勝率です。"""

        if not self.learned_second_games:
            return 0.0
        return self.learned_second_wins / self.learned_second_games


def evaluate_model_against_random(
    model_path: str | Path,
    games: int = 1_000,
    seed: int | None = None,
    learned_owner: Owner = Owner.BLUE,
    pool: CardPool | None = None,
    tactical_weight: float = 0.8,
    reply_penalty_weight: float = 0.25,
) -> tuple[Phase5EvaluationSummary, list[Phase5BattleResult]]:
    """保存済みモデルを読み込み、ランダムAIと指定回数対戦させます。"""

    if games < 1:
        raise ValueError("games must be at least 1")

    # model: Phase4で保存した学習済みモデルです。
    model = LinearMoveModel.load(model_path)

    # rng: seed指定で、評価対戦を再現できます。
    rng = random.Random(seed)

    # pool: 100枚のカードプールです。
    pool = pool or build_default_card_pool()

    # results: 各対戦の詳細結果です。
    results: list[Phase5BattleResult] = []

    for battle_index in range(1, games + 1):
        result = run_model_vs_random_battle(
            battle_index=battle_index,
            model=model,
            rng=rng,
            learned_owner=learned_owner,
            pool=pool,
            tactical_weight=tactical_weight,
            reply_penalty_weight=reply_penalty_weight,
        )
        results.append(result)

    return summarize_phase5_results(results, learned_owner), results


def run_model_vs_random_battle(
    battle_index: int,
    model: LinearMoveModel,
    rng: random.Random,
    learned_owner: Owner = Owner.BLUE,
    pool: CardPool | None = None,
    tactical_weight: float = 0.8,
    reply_penalty_weight: float = 0.25,
) -> Phase5BattleResult:
    """学習済みAIとランダムAIの1戦を実行します。"""

    # pool: 100枚のカードプールです。
    pool = pool or build_default_card_pool()

    # guess: 青側の数当て入力です。Phase5では評価用にランダム入力にします。
    guess = f"{rng.randrange(10_000):04d}"

    # guess_result: 青側のカードグレードを決める数当て結果です。
    guess_result = resolve_number_guess(guess=guess, rng=rng)

    # blue_hand: 青側は企画書どおり、数当てグレードのカードから引きます。
    blue_hand = pool.draw_player_hand(guess_result.grade, rng)

    # red_hand: 赤側は企画書どおり、全100枚から引きます。
    red_hand = pool.draw_cpu_hand(rng)

    # first_player: 先攻をランダムに決めます。
    first_player = rng.choice([Owner.BLUE, Owner.RED])

    # state: バトル状態です。
    state = BattleState.start(
        blue_hand=blue_hand,
        red_hand=red_hand,
        first_player=first_player,
        rng=rng,
    )

    # agents: 学習済みAIとランダムAIを色ごとに割り当てます。
    agents = {
        learned_owner: ModelAgent(
            owner=learned_owner,
            model=model,
            tactical_weight=tactical_weight,
            reply_penalty_weight=reply_penalty_weight,
        ),
        learned_owner.opponent: RandomAgent(owner=learned_owner.opponent),
    }

    # 盤面が埋まるまで、それぞれのAIが手を選びます。
    while not state.is_over:
        move = agents[state.turn].choose_move(state, rng)
        state = state.apply_move(move)

    # scores: 後攻の未使用手札を含めた最終スコアです。
    scores = state.score()

    return Phase5BattleResult(
        battle_index=battle_index,
        learned_owner=learned_owner,
        first_player=first_player,
        player_grade=guess_result.grade,
        winner=state.winner(),
        blue_score=scores[Owner.BLUE],
        red_score=scores[Owner.RED],
        moves_played=state.move_count,
    )


def summarize_phase5_results(
    results: list[Phase5BattleResult],
    learned_owner: Owner,
) -> Phase5EvaluationSummary:
    """Phase5の対戦結果一覧から勝率などを集計します。"""

    if not results:
        raise ValueError("results must not be empty")

    learned_wins = 0
    random_wins = 0
    draws = 0
    learned_first_games = 0
    learned_first_wins = 0
    learned_second_games = 0
    learned_second_wins = 0
    grade_counts = {grade: 0 for grade in range(5)}

    for result in results:
        grade_counts[result.player_grade] += 1

        if result.first_player is learned_owner:
            learned_first_games += 1
        else:
            learned_second_games += 1

        if result.learned_won:
            learned_wins += 1
            if result.first_player is learned_owner:
                learned_first_wins += 1
            else:
                learned_second_wins += 1
        elif result.random_won:
            random_wins += 1
        else:
            draws += 1

    return Phase5EvaluationSummary(
        games=len(results),
        learned_owner=learned_owner,
        learned_wins=learned_wins,
        random_wins=random_wins,
        draws=draws,
        learned_first_games=learned_first_games,
        learned_first_wins=learned_first_wins,
        learned_second_games=learned_second_games,
        learned_second_wins=learned_second_wins,
        grade_counts=grade_counts,
    )
