"""Phase1のルールを手動で遊んで確認するためのCLI。"""

from __future__ import annotations

import argparse
import random
from typing import Sequence

from .battle import BattleState, Move, Owner
from .cards import Card, build_default_card_pool
from .number_guess import resolve_number_guess


def main(argv: Sequence[str] | None = None) -> int:
    """CLIの入口です。数当てからカードバトル終了までを1回実行します。"""

    # parser: コマンドライン引数を読み取るための標準ライブラリ機能です。
    parser = argparse.ArgumentParser(description="Run the Phase 1 rule engine.")

    # --seed: 乱数結果を固定したいときに使います。同じseedなら同じ展開になります。
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible play.")

    # --guess: 数当ての入力をコマンドから渡したいときに使います。省略時は入力待ちになります。
    parser.add_argument("--guess", default=None, help="Four digit number guess. Prompts if omitted.")

    # args: 実際に指定されたコマンドライン引数をまとめたものです。
    args = parser.parse_args(argv)

    # rng: ゲーム全体で使う乱数生成器です。seed指定があれば再現可能になります。
    rng = random.Random(args.seed)

    # pool: 企画書どおりの100枚カードプールです。
    pool = build_default_card_pool()

    # guess: プレイヤーが入力した4桁数字です。--guessがなければその場で入力します。
    guess = args.guess if args.guess is not None else input("Enter a four digit number (0000-9999): ")

    # guess_result: 正解、入力、一致桁数、カードグレードをまとめた結果です。
    guess_result = resolve_number_guess(guess=guess, rng=rng)

    print(f"Secret: {guess_result.secret}")
    print(f"Matched digits: {guess_result.matched_digits}")
    print(f"Player card grade: {guess_result.grade}")

    # blue_hand: プレイヤー手札です。数当て結果のグレードから5枚引きます。
    blue_hand = pool.draw_player_hand(guess_result.grade, rng)

    # red_hand: CPU手札です。全100枚から5枚引きます。
    red_hand = pool.draw_cpu_hand(rng)

    # first_player: 先攻をランダムに決めます。
    first_player = rng.choice([Owner.BLUE, Owner.RED])

    # state: カードバトルの現在状態です。手を打つたびに新しいstateへ更新します。
    state = BattleState.start(blue_hand, red_hand, first_player=first_player, rng=rng)

    print(f"First player: {state.first_player.value}")

    # 盤面が埋まるまで、青は手入力、赤はランダムで進めます。
    while not state.is_over:
        _print_state(state)
        if state.turn is Owner.BLUE:
            state = state.apply_move(_prompt_player_move(state))
        else:
            # move: CPUがランダムに選んだ合法手です。
            move = state.random_legal_move(rng)
            print(f"CPU plays hand {move.hand_index} at position {move.position}.")
            state = state.apply_move(move)

    # 終了後、最終盤面と勝敗を表示します。
    _print_state(state)

    # scores: 後攻の未使用手札を含めた最終スコアです。
    scores = state.score()

    # winner: 勝者です。同点ならNoneになります。
    winner = state.winner()
    print(f"Final score: blue={scores[Owner.BLUE]} red={scores[Owner.RED]}")
    print(f"Winner: {winner.value if winner is not None else 'draw'}")
    return 0


def _prompt_player_move(state: BattleState) -> Move:
    """プレイヤーから「手札番号 盤面位置」の形式で入力を受け取ります。"""

    # 入力形式が間違っている場合は、正しい入力が来るまで繰り返します。
    while True:
        # raw: 空白区切りで分割した入力値です。例: "0 4" -> ["0", "4"]
        raw = input("Your move as 'hand_index position': ").strip().split()
        if len(raw) != 2:
            print("Please enter two numbers, for example: 0 4")
            continue
        try:
            # hand_index: 出したい手札の番号です。
            # position: 置きたい盤面位置です。
            hand_index, position = int(raw[0]), int(raw[1])
            return Move(Owner.BLUE, hand_index, position)
        except ValueError:
            print("Both values must be numbers.")


def _print_state(state: BattleState) -> None:
    """現在の盤面、手札、手番をCLIに表示します。"""

    print("")
    print("Board:")

    # row/col: 3x3盤面を行と列で順番に表示するためのループ変数です。
    for row in range(3):
        # cells: 1行分の表示文字列を集めるリストです。
        cells = []
        for col in range(3):
            # position: 0から8の盤面番号です。
            position = row * 3 + col

            # placed: そのマスに置かれているカードです。Noneなら空きマスです。
            placed = state.board[position]
            if placed is None:
                cells.append(str(position))
            else:
                cells.append("B" if placed.owner is Owner.BLUE else "R")
        print(" ".join(cells))

    print("")
    print("Blue hand:")
    _print_hand(state.blue_hand)
    print("Red hand:")
    _print_hand(state.red_hand)
    print(f"Turn: {state.turn.value}")


def _print_hand(hand: Sequence[Card]) -> None:
    """手札一覧を、番号とカード数値つきで表示します。"""

    # index: プレイヤーが入力する手札番号です。
    # card: その番号に対応するカードです。
    for index, card in enumerate(hand):
        print(
            f"  {index}: {card.name} "
            f"(T{card.top} R{card.right} B{card.bottom} L{card.left})"
        )

    # 手札が空のときは、見た目が分かるようにハイフンを表示します。
    if not hand:
        print("  -")


if __name__ == "__main__":
    # python -m cyberspace_game.cli で直接実行されたときだけmainを呼びます。
    raise SystemExit(main())
