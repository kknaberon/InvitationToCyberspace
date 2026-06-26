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

# phase3_csv.pyから、CSV出力用の特徴量行とエクスポート処理を読み込みます。
from .phase3_csv import (
    MoveFeatureRow,
    export_random_ai_features_to_csv,
    generate_random_ai_feature_rows,
)

# phase4_ml.pyから、教師AIと教師あり学習モデルを読み込みます。
from .phase4_ml import (
    HeuristicTeacher,
    LinearMoveModel,
    TrainingExample,
    TrainingReport,
    generate_teacher_examples,
    train_and_save_supervised_model,
    train_supervised_model,
)

# __all__に書いた名前だけを、このパッケージの代表的な公開機能として扱います。
# 例: from cyberspace_game import Card, BattleState のように使いやすくなります。
__all__ = [
    "BattleState",
    "Card",
    "CardPool",
    "HeuristicTeacher",
    "LinearMoveModel",
    "Move",
    "MoveFeatureRow",
    "NumberGuessResult",
    "Owner",
    "RandomAgent",
    "RandomBattleResult",
    "RandomSimulationSummary",
    "TrainingExample",
    "TrainingReport",
    "build_default_card_pool",
    "export_random_ai_features_to_csv",
    "generate_random_ai_feature_rows",
    "generate_teacher_examples",
    "resolve_number_guess",
    "run_random_battle",
    "run_random_simulation",
    "score_guess",
    "train_and_save_supervised_model",
    "train_supervised_model",
]
