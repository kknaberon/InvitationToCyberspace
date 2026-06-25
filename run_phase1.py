"""プロジェクト直下からPhase1 CLIを起動するための便利ファイル。"""

from __future__ import annotations

from pathlib import Path
import sys


# ROOT: このrun_phase1.pyが置かれているプロジェクト直下のフォルダです。
ROOT = Path(__file__).resolve().parent

# SRC: 実際のゲームコードが入っているsrcフォルダです。
SRC = ROOT / "src"

# Pythonがsrc内のcyberspace_gameパッケージを見つけられるよう、検索パスに追加します。
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# main: Phase1 CLI本体です。ここでは入口だけ借りています。
from cyberspace_game.cli import main


if __name__ == "__main__":
    # python run_phase1.py と実行されたときだけCLIを開始します。
    raise SystemExit(main())
