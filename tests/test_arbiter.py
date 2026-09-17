import unittest

from src.arbiter import Arbiter


class TestArbiter(unittest.TestCase):

    def setUp(self):
        self.arbiter = Arbiter()

    def test_initialization(self):

        self.assertEqual(
            self.arbiter.validation_threshold,
            0.85,
        )

        self.assertEqual(
            self.arbiter.resource_budget,
            3.0,
        )

    def test_validate_authorizes_valid_candidate(self):

        solutions = [
            {
                "name": "GradientBoosting",

                "graph": [
                    "Input",
                    "GradientBoosting",
                    "Output",
                ],

                "resource_cost": 1.5,

                "description":
                    "Replace the baseline classifier.",

                "metrics": {
                    "accuracy": 0.963333,
                    "precision": 0.946429,
                    "recall": 0.868852,
                    "f1": 0.905983,
                },

                "safety_pass": True,

                "utility": 0.981667,
            }
        ]

        current_graph = [
            "Input",
            "RandomForest",
            "Output",
        ]

        result = (
            self.arbiter.validate_solutions(
                solutions,
                current_graph,
            )
        )

        self.assertIn(
            "selected_solution",
            result,
        )

        self.assertIsNotNone(
            result["selected_solution"]
        )

        self.assertEqual(
            result["selected_solution"]["name"],
            "GradientBoosting",
        )

        authorization = (
            result["selected_solution"]
            ["authorization"]
        )

        self.assertTrue(
            authorization["accepted"]
        )

    def test_rejects_unsafe_candidate(self):

        solutions = [
            {
                "name": "UnsafeCandidate",

                "graph": [
                    "Input",
                    "GradientBoosting",
                    "Output",
                ],

                "resource_cost": 1.5,

                "safety_pass": False,

                "utility": 0.99,
            }
        ]

        current_graph = [
            "Input",
            "RandomForest",
            "Output",
        ]

        result = (
            self.arbiter.validate_solutions(
                solutions,
                current_graph,
            )
        )

        self.assertIsNone(
            result["selected_solution"]
        )

        validated = (
            result["validated_solutions"][0]
        )

        self.assertFalse(
            validated["is_valid"]
        )

    def test_rejects_over_budget_candidate(self):

        solutions = [
            {
                "name": "ExpensiveCandidate",

                "graph": [
                    "Input",
                    "GradientBoosting",
                    "Output",
                ],

                "resource_cost": 4.0,

                "safety_pass": True,

                "utility": 0.99,
            }
        ]

        current_graph = [
            "Input",
            "RandomForest",
            "Output",
        ]

        result = (
            self.arbiter.validate_solutions(
                solutions,
                current_graph,
            )
        )

        self.assertIsNone(
            result["selected_solution"]
        )


if __name__ == "__main__":
    unittest.main()
