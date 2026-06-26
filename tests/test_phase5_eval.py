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

from cyberspace_game.battle import Owner
from cyberspace_game.phase4_ml import LinearMoveModel, generate_teacher_examples, train_supervised_model
from cyberspace_game.phase5_eval import (
    ModelAgent,
    evaluate_model_against_random,
    run_model_vs_random_battle,
)


class Phase5EvaluationTests(unittest.TestCase):
    def _create_tiny_model(self) -> LinearMoveModel:
        examples = generate_teacher_examples(games=4, seed=123)
        model, _report = train_supervised_model(examples, epochs=2, learning_rate=0.2)
        return model

    def test_model_agent_returns_legal_move(self) -> None:
        examples = generate_teacher_examples(games=1, seed=1)
        model, _report = train_supervised_model(examples, epochs=1, learning_rate=0.2)
        state = examples[0].state
        agent = ModelAgent(owner=state.turn, model=model)

        move = agent.choose_move(state, random.Random(1))

        self.assertIn(move, state.legal_moves())

    def test_model_vs_random_battle_finishes(self) -> None:
        model = self._create_tiny_model()

        result = run_model_vs_random_battle(
            battle_index=1,
            model=model,
            rng=random.Random(2),
            learned_owner=Owner.BLUE,
        )

        self.assertEqual(result.battle_index, 1)
        self.assertEqual(result.moves_played, 9)
        self.assertEqual(result.blue_score + result.red_score, 10)

    def test_evaluation_summary_counts_match_game_total(self) -> None:
        model = self._create_tiny_model()

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_path = Path(tmp_dir) / "model.json"
            model.save(model_path)

            summary, results = evaluate_model_against_random(
                model_path=model_path,
                games=20,
                seed=2026,
                learned_owner=Owner.BLUE,
            )

        self.assertEqual(len(results), 20)
        self.assertEqual(summary.games, 20)
        self.assertEqual(summary.learned_wins + summary.random_wins + summary.draws, 20)
        self.assertEqual(summary.learned_first_games + summary.learned_second_games, 20)
        self.assertEqual(sum(summary.grade_counts.values()), 20)

    def test_evaluation_can_run_model_as_red(self) -> None:
        model = self._create_tiny_model()

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_path = Path(tmp_dir) / "model.json"
            model.save(model_path)

            summary, _results = evaluate_model_against_random(
                model_path=model_path,
                games=10,
                seed=7,
                learned_owner=Owner.RED,
            )

        self.assertEqual(summary.learned_owner, Owner.RED)
        self.assertEqual(summary.games, 10)


if __name__ == "__main__":
    unittest.main()
