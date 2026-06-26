from __future__ import annotations

import csv
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberspace_game.phase3_csv import (
    MoveFeatureRow,
    export_random_ai_features_to_csv,
    generate_random_ai_feature_rows,
)


class Phase3CsvTests(unittest.TestCase):
    def test_generates_nine_feature_rows_per_battle(self) -> None:
        rows = generate_random_ai_feature_rows(games=2, seed=2026)

        self.assertEqual(len(rows), 18)
        self.assertEqual([row.turn_index for row in rows[:9]], list(range(9)))
        self.assertEqual([row.turn_index for row in rows[9:]], list(range(9)))
        self.assertTrue(all(row.chosen_position in range(9) for row in rows))

    def test_feature_rows_are_reproducible_with_seed(self) -> None:
        first_rows = generate_random_ai_feature_rows(games=3, seed=7)
        second_rows = generate_random_ai_feature_rows(games=3, seed=7)

        self.assertEqual(first_rows, second_rows)

    def test_csv_export_writes_header_and_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "features.csv"

            rows = export_random_ai_features_to_csv(output_path, games=2, seed=1)

            with output_path.open("r", encoding="utf-8", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                csv_rows = list(reader)

            self.assertEqual(len(rows), 18)
            self.assertEqual(len(csv_rows), 18)
            self.assertEqual(reader.fieldnames, list(MoveFeatureRow.__dataclass_fields__))
            self.assertEqual(csv_rows[0]["battle_index"], "1")
            self.assertIn(csv_rows[0]["winner"], {"blue", "red", "draw"})

    def test_rejects_zero_games(self) -> None:
        with self.assertRaises(ValueError):
            generate_random_ai_feature_rows(games=0)


if __name__ == "__main__":
    unittest.main()
