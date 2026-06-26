"""Phase2のランダムAI大量対戦を実行するCLI。"""

from __future__ import annotations

import argparse
from typing import Sequence

from .battle import Owner
from .random_ai import run_random_simulation


def main(argv: Sequence[str] | None = None) -> int:
    """コマンドラインからランダムAI同士の対戦を実行します。"""

    # parser: --games や --seed などのコマンド引数を読み取ります。
    parser = argparse.ArgumentParser(description="Run Phase 2 random AI simulations.")

    # --games: 対戦数です。企画書どおり、デフォルトは10,000戦にしています。
    parser.add_argument("--games", type=int, default=10_000, help="Number of battles to run.")

    # --seed: 結果を再現したいときに指定します。
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible runs.")

    # --show-samples: 最初の数戦だけ詳細を表示したいときに使います。
    parser.add_argument(
        "--show-samples",
        type=int,
        default=0,
        help="Print the first N battle results.",
    )
    args = parser.parse_args(argv)

    summary, results = run_random_simulation(games=args.games, seed=args.seed)

    print(f"Games: {summary.games}")
    print(f"Blue wins: {summary.blue_wins} ({summary.blue_win_rate:.2%})")
    print(f"Red wins: {summary.red_wins} ({summary.red_win_rate:.2%})")
    print(f"Draws: {summary.draws} ({summary.draw_rate:.2%})")
    print("")
    print("Player grade counts:")
    for grade, count in summary.grade_counts.items():
        print(f"  Grade {grade}: {count}")
    print("")
    print("First player counts:")
    print(f"  Blue: {summary.first_player_counts[Owner.BLUE]}")
    print(f"  Red: {summary.first_player_counts[Owner.RED]}")

    if args.show_samples:
        print("")
        print("Sample battles:")
        for result in results[: args.show_samples]:
            winner = result.winner.value if result.winner is not None else "draw"
            print(
                f"  #{result.battle_index}: "
                f"grade={result.player_grade}, first={result.first_player.value}, "
                f"score={result.blue_score}-{result.red_score}, winner={winner}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
