"""Phase5の学習済みAI vs ランダムAI評価を実行するCLI。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .battle import Owner
from .phase5_eval import evaluate_model_against_random


def main(argv: Sequence[str] | None = None) -> int:
    """コマンドラインからPhase5の対戦評価を実行します。"""

    # parser: 対戦数、seed、モデルパスなどのコマンド引数を読み取ります。
    parser = argparse.ArgumentParser(description="Evaluate Phase 4 model against random AI.")

    # --model: Phase4で保存したモデルJSONです。
    parser.add_argument(
        "--model",
        default="models/phase4_linear_model.json",
        help="Path to trained Phase 4 model JSON.",
    )

    # --games: 評価対戦数です。標準では1,000戦にしています。
    parser.add_argument("--games", type=int, default=1_000, help="Number of evaluation battles.")

    # --seed: 評価結果を再現したいときに指定します。
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible evaluation.")

    # --learned-owner: 学習済みAIを青/赤どちらで戦わせるかです。
    parser.add_argument(
        "--learned-owner",
        choices=["blue", "red"],
        default="blue",
        help="Side controlled by the trained model.",
    )

    # --tactical-weight: モデル点に混ぜる盤面評価の強さです。
    parser.add_argument(
        "--tactical-weight",
        type=float,
        default=0.8,
        help="How strongly tactical board evaluation is blended into model score.",
    )

    # --reply-penalty-weight: 相手の次の返し手をどれくらい警戒するかです。
    parser.add_argument(
        "--reply-penalty-weight",
        type=float,
        default=0.25,
        help="How strongly the model avoids the opponent's best immediate reply.",
    )
    args = parser.parse_args(argv)

    learned_owner = Owner(args.learned_owner)
    summary, _results = evaluate_model_against_random(
        model_path=Path(args.model),
        games=args.games,
        seed=args.seed,
        learned_owner=learned_owner,
        tactical_weight=args.tactical_weight,
        reply_penalty_weight=args.reply_penalty_weight,
    )

    print(f"Games: {summary.games}")
    print(f"Learned AI side: {summary.learned_owner.value}")
    print(f"Tactical weight: {args.tactical_weight}")
    print(f"Reply penalty weight: {args.reply_penalty_weight}")
    print(f"Learned wins: {summary.learned_wins} ({summary.learned_win_rate:.2%})")
    print(f"Random wins: {summary.random_wins} ({summary.random_win_rate:.2%})")
    print(f"Draws: {summary.draws} ({summary.draw_rate:.2%})")
    print("")
    print("Learned first/second:")
    print(
        f"  First: {summary.learned_first_wins}/{summary.learned_first_games} "
        f"({summary.learned_first_win_rate:.2%})"
    )
    print(
        f"  Second: {summary.learned_second_wins}/{summary.learned_second_games} "
        f"({summary.learned_second_win_rate:.2%})"
    )
    print("")
    print("Blue player grade counts:")
    for grade, count in summary.grade_counts.items():
        print(f"  Grade {grade}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
