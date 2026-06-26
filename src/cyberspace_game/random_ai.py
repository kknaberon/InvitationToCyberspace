"""Phase2: ランダムAIと大量対戦シミュレーター。"""

from __future__ import annotations

from dataclasses import dataclass
import random

from .battle import BattleState, Move, Owner
from .cards import CardPool, build_default_card_pool
from .number_guess import resolve_number_guess


@dataclass(frozen=True, slots=True)
class RandomAgent:
    """合法手の中からランダムに1手を選ぶだけのAI。"""

    # owner: このAIが担当する色です。青ならプレイヤー側、赤ならCPU側です。
    owner: Owner

    def choose_move(self, state: BattleState, rng: random.Random) -> Move:
        """現在状態からランダムな合法手を1つ選びます。"""

        # state.turnとAIのownerが違う場合、このAIが動く番ではありません。
        if state.turn is not self.owner:
            raise ValueError(f"It is {state.turn.value}'s turn, not {self.owner.value}'s")

        # BattleState側が、現在の手番で選べる全合法手を作ってくれます。
        legal_moves = state.legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves are available")

        # 学習や評価は一切せず、完全にランダムで1手を選びます。
        return rng.choice(legal_moves)


@dataclass(frozen=True, slots=True)
class RandomBattleResult:
    """ランダムAI同士の1戦分の結果。"""

    # battle_index: 何戦目かを表す番号です。CSV出力時にも使いやすいよう残します。
    battle_index: int

    # guess: 青側が数当てで入力した4桁数字です。Phase2ではランダム入力です。
    guess: str

    # secret: 数当ての正解です。Phase2ではランダム生成です。
    secret: str

    # matched_digits: 同じ位置で一致した桁数です。カードグレードと同じ値です。
    matched_digits: int

    # player_grade: 青側が受け取るカードグレードです。
    player_grade: int

    # first_player: 先攻だった色です。
    first_player: Owner

    # winner: 勝者です。同点ならNoneです。
    winner: Owner | None

    # blue_score/red_score: 後攻の未使用手札を含めた最終スコアです。
    blue_score: int
    red_score: int

    # moves_played: 盤面に置かれた枚数です。通常は9になります。
    moves_played: int


@dataclass(frozen=True, slots=True)
class RandomSimulationSummary:
    """ランダムAI同士の複数戦を集計した結果。"""

    # games: 実行した対戦数です。
    games: int

    # blue_wins/red_wins/draws: 青勝ち、赤勝ち、引き分けの回数です。
    blue_wins: int
    red_wins: int
    draws: int

    # grade_counts: 数当て結果として各グレードが何回出たかです。
    grade_counts: dict[int, int]

    # first_player_counts: 青先攻、赤先攻がそれぞれ何回あったかです。
    first_player_counts: dict[Owner, int]

    @property
    def blue_win_rate(self) -> float:
        """青側の勝率を0.0から1.0で返します。"""

        return self.blue_wins / self.games if self.games else 0.0

    @property
    def red_win_rate(self) -> float:
        """赤側の勝率を0.0から1.0で返します。"""

        return self.red_wins / self.games if self.games else 0.0

    @property
    def draw_rate(self) -> float:
        """引き分け率を0.0から1.0で返します。"""

        return self.draws / self.games if self.games else 0.0


def run_random_battle(
    battle_index: int,
    pool: CardPool | None = None,
    rng: random.Random | None = None,
) -> RandomBattleResult:
    """数当てからカードバトルまで、ランダムAI同士の1戦を実行します。"""

    # pool: 100枚のカードプールです。指定がなければ定数カードから作ります。
    pool = pool or build_default_card_pool()

    # rng: すべてのランダム要素に使う乱数生成器です。
    rng = rng or random.Random()

    # guess: 青側の数当て入力です。Phase2ではAIなので完全ランダムです。
    guess = f"{rng.randrange(10_000):04d}"

    # guess_result: 数当て結果です。正解もランダム生成されます。
    guess_result = resolve_number_guess(guess=guess, rng=rng)

    # blue_hand: 青側の手札です。数当て結果グレードの20枚から重複ありで5枚引きます。
    blue_hand = pool.draw_player_hand(guess_result.grade, rng)

    # red_hand: 赤側の手札です。全100枚から重複なしで5枚引きます。
    red_hand = pool.draw_cpu_hand(rng)

    # first_player: 先攻をランダムに決めます。
    first_player = rng.choice([Owner.BLUE, Owner.RED])

    # state: バトルの現在状態です。ランダムAIが1手ずつ進めていきます。
    state = BattleState.start(
        blue_hand=blue_hand,
        red_hand=red_hand,
        first_player=first_player,
        rng=rng,
    )

    # agents: 色ごとのランダムAIです。
    agents = {
        Owner.BLUE: RandomAgent(Owner.BLUE),
        Owner.RED: RandomAgent(Owner.RED),
    }

    # 盤面が埋まるまで、現在の手番AIがランダムな合法手を選びます。
    while not state.is_over:
        move = agents[state.turn].choose_move(state, rng)
        state = state.apply_move(move)

    # scores: 後攻の未使用手札を含む最終スコアです。
    scores = state.score()

    return RandomBattleResult(
        battle_index=battle_index,
        guess=guess,
        secret=guess_result.secret,
        matched_digits=guess_result.matched_digits,
        player_grade=guess_result.grade,
        first_player=first_player,
        winner=state.winner(),
        blue_score=scores[Owner.BLUE],
        red_score=scores[Owner.RED],
        moves_played=state.move_count,
    )


def run_random_simulation(
    games: int = 10_000,
    seed: int | None = None,
    pool: CardPool | None = None,
) -> tuple[RandomSimulationSummary, list[RandomBattleResult]]:
    """ランダムAI同士の対戦を指定回数だけ実行します。"""

    if games < 1:
        raise ValueError("games must be at least 1")

    # rng: seed指定により、10,000戦の結果を再現可能にします。
    rng = random.Random(seed)

    # pool: 毎回カード定義を作り直さないよう、最初に1回だけ用意します。
    pool = pool or build_default_card_pool()

    # results: 各対戦の詳細結果です。Phase3のCSV出力でも土台になります。
    results: list[RandomBattleResult] = []

    # 集計用のカウンタです。
    blue_wins = 0
    red_wins = 0
    draws = 0
    grade_counts = {grade: 0 for grade in range(5)}
    first_player_counts = {Owner.BLUE: 0, Owner.RED: 0}

    for battle_index in range(1, games + 1):
        result = run_random_battle(battle_index=battle_index, pool=pool, rng=rng)
        results.append(result)

        grade_counts[result.player_grade] += 1
        first_player_counts[result.first_player] += 1

        if result.winner is Owner.BLUE:
            blue_wins += 1
        elif result.winner is Owner.RED:
            red_wins += 1
        else:
            draws += 1

    summary = RandomSimulationSummary(
        games=games,
        blue_wins=blue_wins,
        red_wins=red_wins,
        draws=draws,
        grade_counts=grade_counts,
        first_player_counts=first_player_counts,
    )
    return summary, results
