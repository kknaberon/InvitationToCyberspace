"""Phase1ルールエンジンの外部公開APIをまとめるファイル。"""

# battle.pyから、カードバトルでよく使うクラスを読み込みます。
from .battle import BattleState, Move, Owner

# cards.pyから、カードとカードプール生成処理を読み込みます。
from .cards import Card, CardPool, build_default_card_pool

# number_guess.pyから、数当て結果と判定処理を読み込みます。
from .number_guess import NumberGuessResult, resolve_number_guess, score_guess

# random_ai.pyから、Phase2のランダムAIとシミュレーターを読み込みます。
from .random_ai import (
    RandomAgent,
    RandomBattleResult,
    RandomSimulationSummary,
    run_random_battle,
    run_random_simulation,
)

# __all__に書いた名前だけを、このパッケージの代表的な公開機能として扱います。
# 例: from cyberspace_game import Card, BattleState のように使いやすくなります。
__all__ = [
    "BattleState",
    "Card",
    "CardPool",
    "Move",
    "NumberGuessResult",
    "Owner",
    "RandomAgent",
    "RandomBattleResult",
    "RandomSimulationSummary",
    "build_default_card_pool",
    "resolve_number_guess",
    "run_random_battle",
    "run_random_simulation",
    "score_guess",
]
