"""プロジェクト直下からPhase2ランダムAIシミュレーターを起動するファイル。"""

from __future__ import annotations

from pathlib import Path
import sys


# ROOT: このrun_phase2.pyが置かれているプロジェクト直下のフォルダです。
ROOT = Path(__file__).resolve().parent

# SRC: 実際のゲームコードが入っているsrcフォルダです。
SRC = ROOT / "src"

# Pythonがsrc内のcyberspace_gameパッケージを見つけられるよう、検索パスに追加します。
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# main: Phase2 CLI本体です。
from cyberspace_game.phase2_cli import main


if __name__ == "__main__":
    # python run_phase2.py と実行されたときだけランダムAIシミュレーターを開始します。
    raise SystemExit(main())
