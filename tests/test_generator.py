import unittest

from src.generator import Generator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()

    def test_initialization(self):

        self.assertIsInstance(
            self.generator,
            Generator,
        )

        self.assertEqual(
            len(
                self.generator.get_solution_history()
            ),
            0,
        )

    def test_generate_candidates_on_imbalance(self):

        findings = {
            "class_imbalance": True,
            "imbalance_ratio": 3.895104895104895,
            "threshold": 3.0,
            "trigger": "class_imbalance",
        }

        solutions = (
            self.generator.propose_solutions(
                findings
            )
        )

        self.assertEqual(
            len(solutions),
            2,
        )

        names = {
            solution["name"]
            for solution in solutions
        }

        self.assertEqual(
            names,
            {
                "GradientBoosting",
                "SMOTE_RandomForest",
            },
        )

    def test_no_candidates_without_trigger(self):

        findings = {
            "class_imbalance": False,
            "imbalance_ratio": 1.0,
            "threshold": 3.0,
            "trigger": "no_trigger",
        }

        solutions = (
            self.generator.propose_solutions(
                findings
            )
        )

        self.assertEqual(
            solutions,
            [],
        )


if __name__ == "__main__":
    unittest.main()
