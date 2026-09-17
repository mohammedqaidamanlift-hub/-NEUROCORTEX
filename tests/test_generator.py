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
                self.generator.generated_solutions
            ),
            0,
        )

    def test_generate_candidates_when_imbalance_detected(self):

        findings = {
            "class_imbalance": True,
            "imbalance_ratio": 3.895104895104895,
            "threshold": 3.0,
            "trigger": "class_imbalance",
        }

        solutions = (
            self.generator.generate_candidates(
                findings
            )
        )

        self.assertEqual(
            len(solutions),
            2,
        )

        names = [
            solution["name"]
            for solution in solutions
        ]

        self.assertIn(
            "GradientBoosting",
            names,
        )

        self.assertIn(
            "SMOTE_RandomForest",
            names,
        )

    def test_gradient_boosting_candidate(self):

        findings = {
            "class_imbalance": True,
        }

        solutions = (
            self.generator.generate_candidates(
                findings
            )
        )

        candidate = next(
            solution
            for solution in solutions
            if solution["name"]
            == "GradientBoosting"
        )

        self.assertEqual(
            candidate["graph"],
            [
                "Input",
                "GradientBoosting",
                "Output",
            ],
        )

        self.assertEqual(
            candidate["resource_cost"],
            1.5,
        )

        self.assertIn(
            "description",
            candidate,
        )

    def test_smote_random_forest_candidate(self):

        findings = {
            "class_imbalance": True,
        }

        solutions = (
            self.generator.generate_candidates(
                findings
            )
        )

        candidate = next(
            solution
            for solution in solutions
            if solution["name"]
            == "SMOTE_RandomForest"
        )

        self.assertEqual(
            candidate["graph"],
            [
                "Input",
                "SMOTE",
                "RandomForest",
                "Output",
            ],
        )

        self.assertEqual(
            candidate["resource_cost"],
            2.0,
        )

        self.assertIn(
            "description",
            candidate,
        )

    def test_no_candidates_without_trigger(self):

        findings = {
            "class_imbalance": False,
            "imbalance_ratio": 1.5,
            "threshold": 3.0,
            "trigger": "no_trigger",
        }

        solutions = (
            self.generator.generate_candidates(
                findings
            )
        )

        self.assertEqual(
            solutions,
            [],
        )

    def test_propose_solutions_records_history(self):

        findings = {
            "class_imbalance": True,
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

        history = (
            self.generator
            .get_solution_history()
        )

        self.assertEqual(
            len(history),
            2,
        )

        self.assertEqual(
            history,
            solutions,
        )


if __name__ == "__main__":
    unittest.main()
