# src/generator.py
"""
Generator module for proposing novel architectural modifications and solutions.
"""

import random
from typing import List, Dict

class Generator:
    """Solution proposal unit for generating innovative improvements."""
    
    def __init__(self):
        self.solution_templates = self._initialize_templates()
        self.generated_solutions = []
    
    def propose_solutions(self, analysis_results: Dict) -> List[Dict]:
        """
        Generate proposed solutions based on analysis results.
        
        Args:
            analysis_results: Output from Trawler analysis
            
        Returns:
            List of proposed solutions with metadata
        """
        issues = analysis_results.get("identified_issues", [])
        recommendations = analysis_results.get("recommendations", [])
        
        solutions = []
        
        for issue, recommendation in zip(issues, recommendations):
            solution = self._generate_solution(issue, recommendation)
            solutions.append(solution)
            self.generated_solutions.append(solution)
        
        return solutions
    
    def _initialize_templates(self):
        """Initialize solution templates for different problem types."""
        return {
            "accuracy": [
                "GradientBoosting with hyperparameter optimization",
                "Neural Architecture Search for optimal structure",
                "Ensemble of diverse model types"
            ],
            "recall": [
                "SMOTE for class balancing",
                "Focal loss for imbalanced data",
                "Cost-sensitive learning approach"
            ],
            "speed": [
                "Model quantization for faster inference",
                "Architecture pruning for efficiency",
                "Knowledge distillation to smaller model"
            ]
        }
    
    def _generate_solution(self, issue: str, recommendation: str) -> Dict:
        """Generate a specific solution based on issue type."""
        solution_type = self._identify_solution_type(issue)
        
        template = random.choice(self.solution_templates.get(solution_type, ["Default optimization"]))
        
        return {
            "issue": issue,
            "recommendation": recommendation,
            "proposed_solution": template,
            "confidence_score": random.uniform(0.7, 0.95),
            "estimated_improvement": f"{random.randint(5, 20)}%",
            "complexity": random.choice(["low", "medium", "high"])
        }
    
    def _identify_solution_type(self, issue: str) -> str:
        """Identify the type of solution needed based on issue."""
        issue_lower = issue.lower()
        
        if any(word in issue_lower for word in ["accuracy", "precision", "f1"]):
            return "accuracy"
        elif any(word in issue_lower for word in ["recall", "minority", "class"]):
            return "recall"
        elif any(word in issue_lower for word in ["speed", "time", "slow"]):
            return "speed"
        else:
            return "general"
    
    def get_solution_history(self):
        """Return history of all generated solutions."""
        return self.generated_solutions
