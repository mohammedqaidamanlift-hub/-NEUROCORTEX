"""
NeuroCortex SRDF Arbiter.

Authorization and candidate-selection module.

The Arbiter validates proposed structural candidates using:
- structural invariants
- resource constraints
- safety status
- utility threshold

A candidate is authorized only when all required conditions pass.
The highest-utility authorized candidate is selected.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List


class Arbiter:
    """Authorization unit for controlled structural adaptation."""

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
    def _check_invariants(
        candidate_graph: List[str],
    ) -> Dict[str, bool]:
        """
        Validate structural graph invariants.
        """

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
        current_performance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate one candidate against SRDF authorization rules.
        """

        graph = solution.get(
            "graph",
            [],
        )

        resource_cost = float(
            solution.get(
                "resource_cost",
                float("inf"),
            )
        )

        utility = float(
            solution.get(
                "utility",
                0.0,
            )
        )

        safety_pass = bool(
            solution.get(
                "safety_pass",
                False,
            )
        )

        invariant = self._check_invariants(
            graph
        )

        invariant_pass = bool(
            invariant["all_pass"]
        )

        resource_pass = bool(
            resource_cost
            <= self.resource_budget
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

        validation_result = dict(
            solution
        )

        validation_result.update(
            {
                "authorization": {
                    "accepted": accepted,

                    "invariant": invariant,

                    "invariant_pass":
                        invariant_pass,

                    "resource_pass":
                        resource_pass,

                    "safety_pass":
                        safety_pass,

                    "utility_pass":
                        utility_pass,

                    "resource_budget":
                        self.resource_budget,

                    "validation_threshold":
                        self.validation_threshold,

                    "current_performance":
                        current_performance,
                }
            }
        )

        return validation_result

    def validate_solutions(
        self,
        solutions: List[Dict[str, Any]],
        current_performance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate all proposed solutions and select the
        highest-utility authorized candidate.

        If no candidate satisfies all authorization
        conditions, selected_solution is None.
        """

        validated_solutions = []

        for solution in solutions:
            validated_solutions.append(
                self._validate_solution(
                    solution,
                    current_performance,
                )
            )

        authorized_solutions = [
            solution
            for solution in validated_solutions
            if solution[
                "authorization"
            ]["accepted"]
        ]

        if authorized_solutions:

            best_solution = max(
                authorized_solutions,
                key=lambda item: float(
                    item.get(
                        "utility",
                        0.0,
                    )
                ),
            )

        else:

            best_solution = None

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        result = {
            "timestamp": timestamp,

            "validated_solutions":
                validated_solutions,

            "authorized_solutions":
                [
                    solution["name"]
                    for solution
                    in authorized_solutions
                ],

            "selected_solution":
                best_solution,

            "validation_threshold":
                self.validation_threshold,

            "resource_budget":
                self.resource_budget,

            "authorization_count":
                len(
                    authorized_solutions
                ),
        }

        self.validation_history.append(
            result
        )

        self.selected_solutions.append(
            (
                best_solution["name"]
                if best_solution is not None
                else None
            )
        )

        return result

    def get_validation_history(self):
        """Return complete authorization history."""

        return self.validation_history

    def get_selected_solutions(self):
        """Return history of selected solution names."""

        return self.selected_solutions
