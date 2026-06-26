from __future__ import annotations

from pathlib import Path
import random
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberspace_game.battle import BattleState, Owner
from cyberspace_game.cards import build_default_card_pool
from cyberspace_game.random_ai import RandomAgent, run_random_battle, run_random_simulation


class RandomAgentTests(unittest.TestCase):
    def test_random_agent_chooses_legal_move_for_own_turn(self) -> None:
        pool = build_default_card_pool()
        rng = random.Random(123)
        state = BattleState.start(
            blue_hand=pool.draw_player_hand(2, rng),
            red_hand=pool.draw_cpu_hand(rng),
            first_player=Owner.BLUE,
        )
        agent = RandomAgent(Owner.BLUE)

        move = agent.choose_move(state, rng)

        self.assertIn(move, state.legal_moves())

    def test_random_agent_rejects_wrong_turn(self) -> None:
        pool = build_default_card_pool()
        rng = random.Random(123)
        state = BattleState.start(
            blue_hand=pool.draw_player_hand(2, rng),
            red_hand=pool.draw_cpu_hand(rng),
            first_player=Owner.BLUE,
        )
        agent = RandomAgent(Owner.RED)

        with self.assertRaises(ValueError):
            agent.choose_move(state, rng)


class RandomSimulationTests(unittest.TestCase):
    def test_random_battle_finishes_with_valid_result(self) -> None:
        pool = build_default_card_pool()
        result = run_random_battle(battle_index=1, pool=pool, rng=random.Random(1))

        self.assertEqual(result.battle_index, 1)
        self.assertEqual(result.moves_played, 9)
        self.assertIn(result.player_grade, range(5))
        self.assertEqual(result.blue_score + result.red_score, 10)

    def test_random_simulation_counts_match_game_total(self) -> None:
        summary, results = run_random_simulation(games=50, seed=2026)

        self.assertEqual(summary.games, 50)
        self.assertEqual(len(results), 50)
        self.assertEqual(summary.blue_wins + summary.red_wins + summary.draws, 50)
        self.assertEqual(sum(summary.grade_counts.values()), 50)
        self.assertEqual(sum(summary.first_player_counts.values()), 50)

    def test_random_simulation_is_reproducible_with_seed(self) -> None:
        first_summary, first_results = run_random_simulation(games=10, seed=7)
        second_summary, second_results = run_random_simulation(games=10, seed=7)

        self.assertEqual(first_summary, second_summary)
        self.assertEqual(first_results, second_results)

    def test_random_simulation_rejects_zero_games(self) -> None:
        with self.assertRaises(ValueError):
            run_random_simulation(games=0)


if __name__ == "__main__":
    unittest.main()
