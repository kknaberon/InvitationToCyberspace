"""Phase4の教師あり学習を実行するCLI。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .phase4_ml import train_and_save_supervised_model


def main(argv: Sequence[str] | None = None) -> int:
    """コマンドラインから教師あり学習を実行します。"""

    # parser: 学習件数や保存先などのコマンド引数を読み取ります。
    parser = argparse.ArgumentParser(description="Train Phase 4 supervised move model.")

    # --games: 教師AI同士で何戦ぶんの教師データを作るかです。
    parser.add_argument("--games", type=int, default=1_000, help="Teacher battles used for training.")

    # --seed: 教師データ生成と学習結果を再現したいときに指定します。
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible training.")

    # --epochs: 同じ教師データを何周学習するかです。
    parser.add_argument("--epochs", type=int, default=6, help="Training epochs.")

    # --learning-rate: 予測を間違えたときに重みをどれだけ動かすかです。
    parser.add_argument("--learning-rate", type=float, default=0.2, help="Perceptron learning rate.")

    # --model: 学習済みモデルの保存先です。
    parser.add_argument(
        "--model",
        default="models/phase4_linear_model.json",
        help="Output model JSON path.",
    )
    args = parser.parse_args(argv)

    # model_path: 文字列で受け取った保存先をPathに変換します。
    model_path = Path(args.model)

    report = train_and_save_supervised_model(
        model_path=model_path,
        games=args.games,
        seed=args.seed,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
    )

    print(f"Teacher battles: {args.games}")
    print(f"Training examples: {report.examples}")
    print(f"Epochs: {report.epochs}")
    print(f"Training accuracy: {report.final_accuracy:.2%}")
    print(f"Weights: {report.weight_count}")
    print(f"Model: {model_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
