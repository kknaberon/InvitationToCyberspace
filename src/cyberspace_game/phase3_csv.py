"""Phase3: ランダムAIの対戦特徴量をCSVへ出力する処理。"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
import random
from typing import Iterable

from .battle import BattleState, Move, Owner, PlacedCard
from .cards import Card, CardPool, build_default_card_pool
from .number_guess import resolve_number_guess
from .random_ai import RandomAgent


@dataclass(frozen=True, slots=True)
class MoveFeatureRow:
    """CSVの1行分に対応する、1手番前の特徴量データ。"""

    # battle_index: 何戦目かです。
    battle_index: int

    # turn_index: その対戦の何手目かです。0から8までになります。
    turn_index: int

    # acting_owner: この行で手を選ぶプレイヤーです。
    acting_owner: str

    # first_player: その対戦で先攻だったプレイヤーです。
    first_player: str

    # second_player: その対戦で後攻だったプレイヤーです。
    second_player: str

    # guess/secret/matched_digits/player_grade: 数当てゲーム由来の情報です。
    guess: str
    secret: str
    matched_digits: int
    player_grade: int

    # board_0からboard_8: 手を打つ直前の盤面状態です。
    # 空きマスは "empty"、カードがあるマスは "blue:G0-01" のように保存します。
    board_0: str
    board_1: str
    board_2: str
    board_3: str
    board_4: str
    board_5: str
    board_6: str
    board_7: str
    board_8: str

    # blue_remaining_hand/red_remaining_hand: 手を打つ直前の残り手札ID一覧です。
    blue_remaining_hand: str
    red_remaining_hand: str

    # blue_remaining_count/red_remaining_count: 残り手札枚数です。
    blue_remaining_count: int
    red_remaining_count: int

    # chosen_hand_index/chosen_card_id/chosen_position: ランダムAIが実際に選んだ行動です。
    chosen_hand_index: int
    chosen_card_id: str
    chosen_position: int

    # winner: 最終勝者です。引き分けの場合は "draw" です。
    winner: str

    # blue_score/red_score: 後攻の未使用手札を含めた最終スコアです。
    blue_score: int
    red_score: int


def export_random_ai_features_to_csv(
    output_path: str | Path,
    games: int = 10_000,
    seed: int | None = None,
    pool: CardPool | None = None,
) -> list[MoveFeatureRow]:
    """ランダムAI同士の対戦特徴量をCSVへ保存します。"""

    if games < 1:
        raise ValueError("games must be at least 1")

    # output_path: CSVを書き出す先です。親フォルダがなければ作ります。
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # rows: CSVに書き出す全行です。1戦につき9手なので、games * 9行になります。
    rows = generate_random_ai_feature_rows(games=games, seed=seed, pool=pool)

    # newline="" はWindowsで空行が挟まるのを防ぐためのcsvモジュール推奨指定です。
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(MoveFeatureRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    return rows


def generate_random_ai_feature_rows(
    games: int = 10_000,
    seed: int | None = None,
    pool: CardPool | None = None,
) -> list[MoveFeatureRow]:
    """ランダムAI同士の対戦から、CSV用の特徴量行を作ります。"""

    if games < 1:
        raise ValueError("games must be at least 1")

    # rng: seedを指定すると、同じCSV内容を再現できます。
    rng = random.Random(seed)

    # pool: 100枚のカードプールです。毎戦作り直さないよう1回だけ用意します。
    pool = pool or build_default_card_pool()

    # rows: 全対戦ぶんの特徴量行を追加していくリストです。
    rows: list[MoveFeatureRow] = []

    for battle_index in range(1, games + 1):
        rows.extend(_generate_rows_for_one_battle(battle_index=battle_index, pool=pool, rng=rng))

    return rows


def _generate_rows_for_one_battle(
    battle_index: int,
    pool: CardPool,
    rng: random.Random,
) -> list[MoveFeatureRow]:
    """ランダムAI同士の1戦から、9手分の特徴量行を作ります。"""

    # guess: 青側の数当て入力です。Phase3でもPhase2と同じくランダム入力にします。
    guess = f"{rng.randrange(10_000):04d}"

    # guess_result: 数当ての正解、一致桁数、カードグレードです。
    guess_result = resolve_number_guess(guess=guess, rng=rng)

    # blue_hand/red_hand: バトル開始時点の両者の手札です。
    blue_hand = pool.draw_player_hand(guess_result.grade, rng)
    red_hand = pool.draw_cpu_hand(rng)

    # first_player: 先攻をランダムに決めます。
    first_player = rng.choice([Owner.BLUE, Owner.RED])

    # state: バトル状態です。手を打つたびに新しい状態へ更新します。
    state = BattleState.start(
        blue_hand=blue_hand,
        red_hand=red_hand,
        first_player=first_player,
        rng=rng,
    )

    # agents: 青と赤、それぞれのランダムAIです。
    agents = {
        Owner.BLUE: RandomAgent(Owner.BLUE),
        Owner.RED: RandomAgent(Owner.RED),
    }

    # snapshots: 最終勝敗が決まる前に、一手ごとの状態と選択手を仮保存します。
    snapshots: list[tuple[int, BattleState, Move]] = []

    # 盤面が埋まるまで、手を選ぶ直前の状態と、そのとき選んだ手を記録します。
    while not state.is_over:
        turn_index = state.move_count
        move = agents[state.turn].choose_move(state, rng)
        snapshots.append((turn_index, state, move))
        state = state.apply_move(move)

    # ゲーム終了後に、全行へ共通で入れる勝敗情報を計算します。
    scores = state.score()
    winner = state.winner()
    winner_text = winner.value if winner is not None else "draw"

    # snapshotsをCSV行へ変換します。
    return [
        _build_feature_row(
            battle_index=battle_index,
            turn_index=turn_index,
            state=before_move_state,
            move=move,
            guess=guess,
            secret=guess_result.secret,
            matched_digits=guess_result.matched_digits,
            player_grade=guess_result.grade,
            winner=winner_text,
            blue_score=scores[Owner.BLUE],
            red_score=scores[Owner.RED],
        )
        for turn_index, before_move_state, move in snapshots
    ]


def _build_feature_row(
    battle_index: int,
    turn_index: int,
    state: BattleState,
    move: Move,
    guess: str,
    secret: str,
    matched_digits: int,
    player_grade: int,
    winner: str,
    blue_score: int,
    red_score: int,
) -> MoveFeatureRow:
    """手を打つ直前のBattleStateと選択手から、CSVの1行を作ります。"""

    # board_cells: 9マスぶんの盤面状態を、CSVに入れやすい文字列へ変換したリストです。
    board_cells = [_format_board_cell(cell) for cell in state.board]

    # chosen_card: ランダムAIが選んだ手札内のカードです。
    chosen_card = state.hand_for_owner(move.owner)[move.hand_index]

    return MoveFeatureRow(
        battle_index=battle_index,
        turn_index=turn_index,
        acting_owner=move.owner.value,
        first_player=state.first_player.value,
        second_player=state.second_player.value,
        guess=guess,
        secret=secret,
        matched_digits=matched_digits,
        player_grade=player_grade,
        board_0=board_cells[0],
        board_1=board_cells[1],
        board_2=board_cells[2],
        board_3=board_cells[3],
        board_4=board_cells[4],
        board_5=board_cells[5],
        board_6=board_cells[6],
        board_7=board_cells[7],
        board_8=board_cells[8],
        blue_remaining_hand=_format_hand(state.blue_hand),
        red_remaining_hand=_format_hand(state.red_hand),
        blue_remaining_count=len(state.blue_hand),
        red_remaining_count=len(state.red_hand),
        chosen_hand_index=move.hand_index,
        chosen_card_id=chosen_card.card_id,
        chosen_position=move.position,
        winner=winner,
        blue_score=blue_score,
        red_score=red_score,
    )


def _format_board_cell(cell: PlacedCard | None) -> str:
    """盤面1マスをCSV用文字列に変換します。"""

    if cell is None:
        return "empty"
    return f"{cell.owner.value}:{cell.card.card_id}"


def _format_hand(hand: Iterable[Card]) -> str:
    """残り手札を、カードIDの区切り文字列に変換します。"""

    # 例: G0-01|G0-12|G0-03 のような形で保存します。
    return "|".join(card.card_id for card in hand)
