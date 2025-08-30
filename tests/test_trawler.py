# tests/test_trawler.py
import unittest
from src.trawler import Trawler

class TestTrawler(unittest.TestCase):
    def setUp(self):
        self.trawler = Trawler()
    
    def test_initialization(self):
        self.assertIsInstance(self.trawler, Trawler)
        self.assertEqual(len(self.trawler.analysis_history), 0)
    
    def test_analyze_performance(self):
        # Mock model and data
        class MockModel:
            def predict(self, data):
                return [0] * len(data)
        
        model = MockModel()
        data = [[1, 2], [3, 4]]
        labels = [0, 1]
        
        result = self.trawler.analyze_performance(model, data, labels)
        
        self.assertIn("performance_metrics", result)
        self.assertIn("identified_issues", result)
        self.assertIn("recommendations", result)
    
    def test_analysis_history(self):
        self.assertEqual(len(self.trawler.get_analysis_history()), 0)

if __name__ == "__main__":
    unittest.main()
