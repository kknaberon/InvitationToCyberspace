"""プロジェクト直下からPhase5評価を起動するファイル。"""

from __future__ import annotations

from pathlib import Path
import sys


# ROOT: このrun_phase5.pyが置かれているプロジェクト直下のフォルダです。
ROOT = Path(__file__).resolve().parent

# SRC: 実際のゲームコードが入っているsrcフォルダです。
SRC = ROOT / "src"

# Pythonがsrc内のcyberspace_gameパッケージを見つけられるよう、検索パスに追加します。
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# main: Phase5 CLI本体です。
from cyberspace_game.phase5_cli import main


if __name__ == "__main__":
    # python run_phase5.py と実行されたときだけ評価を開始します。
    raise SystemExit(main())
