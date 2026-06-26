"""Phase3のCSV特徴量出力を実行するCLI。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .phase3_csv import export_random_ai_features_to_csv


def main(argv: Sequence[str] | None = None) -> int:
    """コマンドラインからランダムAI対戦の特徴量CSVを出力します。"""

    # parser: --games、--seed、--output などのコマンド引数を読み取ります。
    parser = argparse.ArgumentParser(description="Export Phase 3 random AI feature CSV.")

    # --games: 対戦数です。1戦につき9行出力されます。
    parser.add_argument("--games", type=int, default=10_000, help="Number of battles to export.")

    # --seed: CSV内容を再現したいときに指定します。
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible CSV.")

    # --output: CSVの保存先です。デフォルトはdata/random_ai_features.csvです。
    parser.add_argument(
        "--output",
        default="data/random_ai_features.csv",
        help="Output CSV path.",
    )
    args = parser.parse_args(argv)

    # output_path: 文字列で受け取った保存先をPathに変換します。
    output_path = Path(args.output)

    # rows: 実際に書き出した特徴量行です。
    rows = export_random_ai_features_to_csv(
        output_path=output_path,
        games=args.games,
        seed=args.seed,
    )

    print(f"Exported rows: {len(rows)}")
    print(f"Battles: {args.games}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
