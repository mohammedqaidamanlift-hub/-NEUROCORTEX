import unittest

import numpy as np

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from src.core import SRDFFramework


class TestSRDFFramework(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        X, y = make_classification(
            n_samples=300,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            n_clusters_per_class=1,
            weights=[0.80, 0.20],
            random_state=42,
        )

        (
            cls.X_train,
            cls.X_test,
            cls.y_train,
            cls.y_test,
        ) = train_test_split(
            X,
            y,
            test_size=0.30,
            random_state=42,
            stratify=y,
        )

    def setUp(self):

        self.framework = SRDFFramework(
            {
                "cycle_interval": 0,
                "max_cycles": 1,
            }
        )

    def test_initial_state(self):

        self.assertEqual(
            self.framework.state["version"],
            0,
        )

        self.assertEqual(
            self.framework.state["graph"],
            [
                "Input",
                "RandomForest",
                "Output",
            ],
        )

    def test_run_cycle(self):

        result = self.framework.run_cycle(
            self.X_train,
            self.y_train,
            self.X_test,
            self.y_test,
        )

        self.assertIn(
            "trawler_findings",
            result,
        )

        self.assertIn(
            "evaluated_candidates",
            result,
        )

        self.assertIn(
            "validation_results",
            result,
        )

        self.assertIn(
            "state_transition",
            result,
        )

        selected_name = (
            result["selected_solution"]
        )

        self.assertIsNotNone(
            selected_name
        )

        candidate_names = [
            candidate["name"]
            for candidate
            in result[
                "evaluated_candidates"
            ]
        ]

        self.assertIn(
            selected_name,
            candidate_names,
        )

        selected_candidate = next(
            candidate
            for candidate
            in result[
                "evaluated_candidates"
            ]
            if candidate["name"]
            == selected_name
        )

        self.assertTrue(
            selected_candidate[
                "authorization"
            ]["accepted"]
        )

        self.assertEqual(
            result["state_after"]["graph"],
            selected_candidate["graph"],
        )

        self.assertEqual(
            result["state_after"]["version"],
            1,
        )

    def test_json_safe_numpy_values(self):

        value = {
            "array": np.array(
                [1, 2, 3]
            ),
            "scalar": np.float64(
                0.5
            ),
        }

        converted = (
            self.framework._json_safe(
                value
            )
        )

        self.assertEqual(
            converted["array"],
            [1, 2, 3],
        )

        self.assertEqual(
            converted["scalar"],
            0.5,
        )


if __name__ == "__main__":
    unittest.main()
