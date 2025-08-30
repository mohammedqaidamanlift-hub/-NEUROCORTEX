# tests/test_generator.py
import unittest
from src.generator import Generator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = Generator()
    
    def test_initialization(self):
        self.assertIsInstance(self.generator, Generator)
    
    def test_propose_solutions(self):
        analysis_results = {
            "identified_issues": ["Low accuracy", "Poor recall"],
            "recommendations": ["Improve accuracy", "Enhance recall"]
        }
        
        solutions = self.generator.propose_solutions(analysis_results)
        
        self.assertEqual(len(solutions), 2)
        self.assertIn("proposed_solution", solutions[0])

if __name__ == "__main__":
    unittest.main()
