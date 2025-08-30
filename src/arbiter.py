# src/arbiter.py
"""
Arbiter module for validating and selecting the most effective solutions.
"""

import numpy as np
from typing import List, Dict

class Arbiter:
    """Validation unit for selecting optimal solutions."""
    
    def __init__(self, validation_threshold: float = 0.8):
        self.validation_threshold = validation_threshold
        self.validation_history = []
        self.selected_solutions = []
    
    def validate_solutions(self, solutions: List[Dict], 
                          current_performance: Dict) -> Dict:
        """
        Validate proposed solutions and select the best one.
        
        Args:
            solutions: List of proposed solutions from Generator
            current_performance: Current model performance metrics
            
        Returns:
            Selected solution with validation results
        """
        validated_solutions = []
        
        for solution in solutions:
            validation_result = self._validate_solution(solution, current_performance)
            validated_solutions.append(validation_result)
        
        # Select best solution
        best_solution = self._select_best_solution(validated_solutions)
        
        result = {
            "timestamp": self._get_current_timestamp(),
            "validated_solutions": validated_solutions,
            "selected_solution": best_solution,
            "validation_threshold": self.validation_threshold
        }
        
        self.validation_history.append(result)
        self.selected_solutions.append(best_solution)
        
        return result
    
    def _validate_solution(self, solution: Dict, current_performance: Dict) -> Dict:
        """Validate a single solution proposal."""
        # Simulate validation process
        validation_score = self._calculate_validation_score(solution, current_performance)
        is_valid = validation_score >= self.validation_threshold
        
        return {
            **solution,
            "validation_score": validation_score,
            "is_valid": is_valid,
            "expected_impact": self._estimate_impact(solution, current_performance)
        }
    
    def _calculate_validation_score(self, solution: Dict, current_performance: Dict) -> float:
        """Calculate validation score for a solution."""
        base_score = solution.get("confidence_score", 0.5)
        
        # Adjust based on complexity (lower complexity = higher score)
        complexity = solution.get("complexity", "medium")
        complexity_factor = {
            "low": 1.2,
            "medium": 1.0,
            "high": 0.8
        }.get(complexity, 1.0)
        
        # Adjust based on current performance
        performance_factor = 1.0
        if current_performance.get("accuracy", 0) < 0.7:
            performance_factor = 1.1  # More willing to try solutions if performance is poor
        
        return min(1.0, base_score * complexity_factor * performance_factor)
    
    def _estimate_impact(self, solution: Dict, current_performance: Dict) -> Dict:
        """Estimate the potential impact of the solution."""
        return {
            "accuracy_improvement": random.uniform(0.02, 0.15),
            "speed_improvement": random.uniform(0.01, 0.10),
            "stability_impact": random.choice(["improved", "neutral", "reduced"])
        }
    
    def _select_best_solution(self, validated_solutions: List[Dict]) -> Dict:
        """Select the best solution from validated options."""
        valid_solutions = [s for s in validated_solutions if s["is_valid"]]
        
        if not valid_solutions:
            # Fallback to least bad invalid solution if no valid ones
            valid_solutions = sorted(validated_solutions, 
                                   key=lambda x: x["validation_score"], 
                                   reverse=True)[:1]
        
        # Select solution with highest validation score
        best_solution = max(valid_solutions, key=lambda x: x["validation_score"])
        
        return best_solution
    
    def _get_current_timestamp(self):
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_validation_history(self):
        """Return complete validation history."""
        return self.validation_history
    
    def get_selected_solutions(self):
        """Return history of all selected solutions."""
        return self.selected_solutions
