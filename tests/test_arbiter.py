# tests/test_arbiter.py
import unittest
from src.arbiter import Arbiter

class TestArbiter(unittest.TestCase):
    def setUp(self):
        self.arbiter = Arbiter()
    
    def test_initialization(self):
        self.assertEqual(self.arbiter.validation_threshold, 0.8)
    
    def test_validate_solutions(self):
        solutions = [{
            "issue": "Low accuracy",
            "proposed_solution": "Use GradientBoosting",
            "confidence_score": 0.9,
            "complexity": "medium"
        }]
        
        current_performance = {"accuracy": 0.75}
        
        result = self.arbiter.validate_solutions(solutions, current_performance)
        
        self.assertIn("selected_solution", result)
        self.assertIn("validated_solutions", result)

if __name__ == "__main__":
    unittest.main()
