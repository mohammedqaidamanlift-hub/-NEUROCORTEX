"""
NeuroCortex SRDF Arbiter.

Bounded authorization unit for structural candidate selection.

The arbiter does not generate experimental results. It evaluates
already-observed candidate results against explicit authorization
conditions and selects the highest-utility authorized candidate.
"""

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List


class Arbiter:
    """Authorization and candidate-selection unit."""

    def __init__(
        self,
        validation_threshold: float = 0.85,
        resource_budget: float = 3.0,
    ):
        self.validation_threshold = float(
            validation_threshold
        )

        self.resource_budget = float(
            resource_budget
        )

        self.validation_history = []
        self.selected_solutions = []

    @staticmethod
    def _invariant_check(
        candidate_graph: List[str],
    ) -> Dict[str, bool]:
        """Validate structural graph invariants."""

        allowed_nodes = {
            "Input",
            "Output",
            "RandomForest",
            "GradientBoosting",
            "SMOTE",
        }

        graph = list(candidate_graph)

        checks = {
            "starts_with_input": (
                len(graph) >= 2
                and graph[0] == "Input"
            ),

            "ends_with_output": (
                len(graph) >= 2
                and graph[-1] == "Output"
            ),

            "unique_nodes": (
                len(graph)
                == len(set(graph))
            ),

            "allowed_nodes": (
                set(graph).issubset(
                    allowed_nodes
                )
            ),
        }

        checks["all_pass"] = bool(
            all(checks.values())
        )

        return checks

    def _validate_solution(
        self,
        solution: Dict[str, Any],
        current_graph: List[str],
    ) -> Dict[str, Any]:
        """Authorize one already-evaluated candidate."""

        invariant = self._invariant_check(
            solution.get("graph", [])
        )

        invariant_pass = bool(
            invariant["all_pass"]
        )

        resource_pass = bool(
            float(
                solution.get(
                    "resource_cost",
                    float("inf"),
                )
            )
            <= self.resource_budget
        )

        safety_pass = bool(
            solution.get(
                "safety_pass",
                False,
            )
        )

        utility = float(
            solution.get(
                "utility",
                0.0,
            )
        )

        utility_pass = bool(
            utility
            >= self.validation_threshold
        )

        accepted = bool(
            invariant_pass
            and resource_pass
            and safety_pass
            and utility_pass
        )

        result = deepcopy(solution)

        result.update(
            {
                "validation_score": utility,
                "is_valid": accepted,
                "authorization": {
                    "accepted": accepted,
                    "invariant": invariant,
                    "invariant_pass": invariant_pass,
                    "resource_pass": resource_pass,
                    "safety_pass": safety_pass,
                    "utility_pass": utility_pass,
                    "current_graph": list(
                        current_graph
                    ),
                    "candidate_graph": list(
                        solution.get(
                            "graph",
                            [],
                        )
                    ),
                },
            }
        )

        return result

    def validate_solutions(
        self,
        solutions: List[Dict[str, Any]],
        current_graph: List[str],
    ) -> Dict[str, Any]:
        """
        Validate all evaluated candidates and select one.

        Selection is performed only among candidates satisfying
        all authorization conditions.
        """

        validated_solutions = [
            self._validate_solution(
                solution,
                current_graph,
            )
            for solution in solutions
        ]

        valid_solutions = [
            solution
            for solution in validated_solutions
            if solution["is_valid"]
        ]

        if valid_solutions:
            best_solution = max(
                valid_solutions,
                key=lambda item: item[
                    "validation_score"
                ],
            )
        else:
            best_solution = None

        result = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "validated_solutions":
                validated_solutions,

            "selected_solution":
                best_solution,

            "validation_threshold":
                self.validation_threshold,

            "resource_budget":
                self.resource_budget,
        }

        self.validation_history.append(
            deepcopy(result)
        )

        if best_solution is not None:
            self.selected_solutions.append(
                deepcopy(best_solution)
            )

        return result

    def get_validation_history(self):
        """Return complete authorization history."""

        return self.validation_history

    def get_selected_solutions(self):
        """Return selected authorized solutions."""

        return self.selected_solutions
