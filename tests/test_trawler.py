import unittest

import numpy as np

from src.trawler import Trawler


class TestTrawler(unittest.TestCase):

    def setUp(self):
        self.trawler = Trawler()

    def test_initialization(self):
        self.assertIsInstance(
            self.trawler,
            Trawler,
        )

        self.assertEqual(
            len(
                self.trawler.analysis_history
            ),
            0,
        )

        self.assertEqual(
            self.trawler.imbalance_threshold,
            3.0,
        )

    def test_analyze_detects_class_imbalance(self):

        y_train = np.array(
            [0] * 557
            + [1] * 143
        )

        current_state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],
            "version": 0,
            "rejection_count": 0,
        }

        result = self.trawler.analyze(
            y_train,
            current_state,
        )

        self.assertIsInstance(
            result,
            dict,
        )

        self.assertIn(
            "class_imbalance",
            result,
        )

        self.assertIn(
            "imbalance_ratio",
            result,
        )

        self.assertIn(
            "threshold",
            result,
        )

        self.assertIn(
            "trigger",
            result,
        )

        self.assertTrue(
            result["class_imbalance"]
        )

        self.assertEqual(
            result["trigger"],
            "class_imbalance",
        )

        self.assertAlmostEqual(
            result["imbalance_ratio"],
            557 / 143,
            places=10,
        )

    def test_analyze_no_imbalance(self):

        y_train = np.array(
            [0] * 500
            + [1] * 500
        )

        current_state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],
            "version": 0,
        }

        result = self.trawler.analyze(
            y_train,
            current_state,
        )

        self.assertFalse(
            result["class_imbalance"]
        )

        self.assertEqual(
            result["trigger"],
            "no_trigger",
        )

    def test_analysis_history(self):

        y_train = np.array(
            [0] * 4
            + [1] * 2
        )

        current_state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],
            "version": 0,
        }

        self.trawler.analyze(
            y_train,
            current_state,
        )

        history = (
            self.trawler
            .get_analysis_history()
        )

        self.assertEqual(
            len(history),
            1,
        )

        self.assertIn(
            "timestamp",
            history[0],
        )

        self.assertIn(
            "findings",
            history[0],
        )

        self.assertIn(
            "class_counts",
            history[0],
        )

        self.assertIn(
            "graph",
            history[0],
        )

        self.assertIn(
            "state_version",
            history[0],
        )


if __name__ == "__main__":
    unittest.main()
