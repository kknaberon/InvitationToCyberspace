"""プロジェクト直下からPhase3 CSV出力を起動するファイル。"""

from __future__ import annotations

from pathlib import Path
import sys


# ROOT: このrun_phase3.pyが置かれているプロジェクト直下のフォルダです。
ROOT = Path(__file__).resolve().parent

# SRC: 実際のゲームコードが入っているsrcフォルダです。
SRC = ROOT / "src"

# Pythonがsrc内のcyberspace_gameパッケージを見つけられるよう、検索パスに追加します。
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# main: Phase3 CLI本体です。
from cyberspace_game.phase3_cli import main


if __name__ == "__main__":
    # python run_phase3.py と実行されたときだけCSV出力を開始します。
    raise SystemExit(main())
