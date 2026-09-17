import unittest

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

    def test_analyze_detects_imbalance(self):

        y_train = (
            [0] * 557
            +
            [1] * 143
        )

        state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],
            "version": 0,
        }

        result = self.trawler.analyze(
            y_train,
            state,
        )

        self.assertTrue(
            result["class_imbalance"]
        )

        self.assertGreaterEqual(
            result["imbalance_ratio"],
            3.0,
        )

        self.assertEqual(
            result["trigger"],
            "class_imbalance",
        )

    def test_analyze_no_trigger(self):

        y_train = (
            [0] * 100
            +
            [1] * 100
        )

        state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],
            "version": 0,
        }

        result = self.trawler.analyze(
            y_train,
            state,
        )

        self.assertFalse(
            result["class_imbalance"]
        )

        self.assertEqual(
            result["trigger"],
            "no_trigger",
        )

    def test_analysis_history(self):

        self.assertEqual(
            len(
                self.trawler.get_analysis_history()
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
