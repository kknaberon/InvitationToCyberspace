from __future__ import annotations

from pathlib import Path
import random
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberspace_game.battle import BattleState, Move, Owner
from cyberspace_game.cards import Card, TARGET_GRADE_AVERAGES, build_default_card_pool
from cyberspace_game.number_guess import resolve_number_guess, score_guess


class NumberGuessTests(unittest.TestCase):
    def test_scores_position_matches_only(self) -> None:
        self.assertEqual(score_guess("1234", "4321"), 0)
        self.assertEqual(score_guess("1111", "1100"), 2)
        self.assertEqual(score_guess("0099", "0000"), 2)

    def test_resolve_guess_returns_grade(self) -> None:
        result = resolve_number_guess("1200", secret="1234")
        self.assertEqual(result.matched_digits, 2)
        self.assertEqual(result.grade, 2)
        self.assertFalse(result.is_exact)

    def test_invalid_guess_raises(self) -> None:
        with self.assertRaises(ValueError):
            resolve_number_guess("123", secret="1234")


class CardPoolTests(unittest.TestCase):
    def test_default_pool_shape_and_grade_averages(self) -> None:
        pool = build_default_card_pool()
        self.assertEqual(len(pool.cards), 100)
        for grade, expected_average in TARGET_GRADE_AVERAGES.items():
            self.assertEqual(len(pool.cards_for_grade(grade)), 20)
            self.assertEqual(pool.average_for_grade(grade), expected_average)

    def test_player_draw_allows_duplicates_and_cpu_draw_is_unique(self) -> None:
        pool = build_default_card_pool()
        rng = random.Random(1)
        player_hand = pool.draw_player_hand(0, rng)
        cpu_hand = pool.draw_cpu_hand(rng)
        self.assertEqual(len(player_hand), 5)
        self.assertEqual(len(cpu_hand), 5)
        self.assertEqual(len({card.card_id for card in cpu_hand}), 5)

    def test_card_names_are_short_multiline_labels(self) -> None:
        pool = build_default_card_pool()
        for card in pool.cards:
            lines = card.name.split("/")
            self.assertLessEqual(len(lines), 3)
            for line in lines:
                self.assertGreater(len(line), 0)
                self.assertLessEqual(len(line), 4)


class BattleTests(unittest.TestCase):
    def test_capture_adjacent_opponent_card(self) -> None:
        red_card = Card("R", "Red", 2, top=1, right=1, bottom=3, left=1)
        blue_card = Card("B", "Blue", 4, top=9, right=1, bottom=1, left=1)
        filler = Card("F", "Filler", 2, top=5, right=5, bottom=5, left=5)

        state = BattleState.start(
            blue_hand=[blue_card, filler, filler, filler, filler],
            red_hand=[red_card, filler, filler, filler, filler],
            first_player=Owner.RED,
        )
        state = state.apply_move(Move(Owner.RED, 0, 1))
        state = state.apply_move(Move(Owner.BLUE, 0, 4))

        self.assertIsNotNone(state.board[1])
        self.assertEqual(state.board[1].owner, Owner.BLUE)

    def test_second_players_remaining_hand_counts_in_final_score(self) -> None:
        card = Card("N", "Neutral", 2, top=5, right=5, bottom=5, left=5)
        state = BattleState.start(
            blue_hand=[card, card, card, card, card],
            red_hand=[card, card, card, card, card],
            first_player=Owner.BLUE,
        )
        for move in [
            Move(Owner.BLUE, 0, 0),
            Move(Owner.RED, 0, 1),
            Move(Owner.BLUE, 0, 2),
            Move(Owner.RED, 0, 3),
            Move(Owner.BLUE, 0, 4),
            Move(Owner.RED, 0, 5),
            Move(Owner.BLUE, 0, 6),
            Move(Owner.RED, 0, 7),
            Move(Owner.BLUE, 0, 8),
        ]:
            state = state.apply_move(move)

        scores = state.score()
        self.assertTrue(state.is_over)
        self.assertEqual(scores[Owner.BLUE], 5)
        self.assertEqual(scores[Owner.RED], 5)
        self.assertIsNone(state.winner())


if __name__ == "__main__":
    unittest.main()
