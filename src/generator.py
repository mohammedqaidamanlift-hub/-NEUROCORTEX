# src/generator.py
"""
NeuroCortex SRDF Generator.

Structural candidate generation module.

The implementation follows the NeuroCortex SRDF Toy Prototype v2.0
reference implementation.
"""

from typing import Dict, List


class Generator:
    """Structural candidate generator."""

    def __init__(self):
        self.generated_solutions = []

    def propose_solutions(
        self,
        analysis_results: Dict,
    ) -> List[Dict]:
        """
        Generate structural candidates from Trawler findings.

        Candidates are generated only when a class imbalance
        condition has been detected.

        Args:
            analysis_results: Findings returned by Trawler.

        Returns:
            List of structural candidate dictionaries.
        """

        candidates = self.generate_candidates(
            analysis_results
        )

        self.generated_solutions.extend(
            candidates
        )

        return candidates

    def generate_candidates(
        self,
        findings: Dict,
    ) -> List[Dict]:
        """
        Generate structural candidates defined by SRDF.

        Two candidate structures are currently supported:

        1. GradientBoosting
        2. SMOTE_RandomForest
        """

        if not findings.get(
            "class_imbalance",
            False,
        ):
            return []

        candidates = [
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
            },

            {
                "name": "SMOTE_RandomForest",

                "graph": [
                    "Input",
                    "SMOTE",
                    "RandomForest",
                    "Output",
                ],

                "resource_cost": 2.0,

                "description":
                    "Insert SMOTE before RandomForest.",
            },
        ]

        return candidates

    def get_solution_history(self):
        """Return history of all generated structural candidates."""

        return self.generated_solutions
