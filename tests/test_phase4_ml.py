from __future__ import annotations

from pathlib import Path
import random
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberspace_game.battle import BattleState, Owner
from cyberspace_game.cards import build_default_card_pool
from cyberspace_game.phase4_ml import (
    HeuristicTeacher,
    LinearMoveModel,
    extract_move_features,
    generate_teacher_examples,
    train_and_save_supervised_model,
    train_supervised_model,
)


class Phase4MachineLearningTests(unittest.TestCase):
    def test_heuristic_teacher_returns_legal_move(self) -> None:
        pool = build_default_card_pool()
        rng = random.Random(1)
        state = BattleState.start(
            blue_hand=pool.draw_player_hand(2, rng),
            red_hand=pool.draw_cpu_hand(rng),
            first_player=Owner.BLUE,
        )
        teacher = HeuristicTeacher()

        move = teacher.choose_move(state, rng)

        self.assertIn(move, state.legal_moves())

    def test_extract_move_features_contains_expected_values(self) -> None:
        pool = build_default_card_pool()
        rng = random.Random(2)
        state = BattleState.start(
            blue_hand=pool.draw_player_hand(2, rng),
            red_hand=pool.draw_cpu_hand(rng),
            first_player=Owner.BLUE,
        )
        move = state.legal_moves()[0]

        features = extract_move_features(state, move)

        self.assertIn("bias", features)
        self.assertIn("card_top", features)
        self.assertIn("score_diff_after", features)
        self.assertEqual(features["bias"], 1.0)

    def test_generate_teacher_examples_creates_nine_examples_per_battle(self) -> None:
        examples = generate_teacher_examples(games=3, seed=2026)

        self.assertEqual(len(examples), 27)
        self.assertTrue(all(example.expert_move in example.state.legal_moves() for example in examples))

    def test_train_supervised_model_learns_and_predicts_legal_move(self) -> None:
        examples = generate_teacher_examples(games=8, seed=3)

        model, report = train_supervised_model(examples, epochs=3, learning_rate=0.2)
        predicted_move = model.predict_move(examples[0].state)

        self.assertIn(predicted_move, examples[0].state.legal_moves())
        self.assertEqual(report.examples, len(examples))
        self.assertGreater(report.weight_count, 0)
        self.assertGreaterEqual(report.final_accuracy, 0.0)
        self.assertLessEqual(report.final_accuracy, 1.0)

    def test_train_and_save_model_round_trips_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            model_path = Path(tmp_dir) / "model.json"

            report = train_and_save_supervised_model(
                model_path=model_path,
                games=5,
                seed=4,
                epochs=2,
            )
            loaded_model = LinearMoveModel.load(model_path)

            self.assertTrue(model_path.exists())
            self.assertEqual(report.examples, 45)
            self.assertGreater(len(loaded_model.weights), 0)


if __name__ == "__main__":
    unittest.main()
