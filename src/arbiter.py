# src/arbiter.py
"""
NeuroCortex SRDF Arbiter.

Authorization unit for validating structural candidates.

The Arbiter applies explicit authorization conditions:

1. Structural invariants
2. Resource budget
3. Safety validation
4. Utility threshold

A candidate is selected only if it passes all authorization
conditions. If no candidate passes, the result is None and
the caller must preserve the current state.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class Arbiter:
    """Authorization unit for SRDF structural adaptation."""

    ALLOWED_NODES = {
        "Input",
        "Output",
        "RandomForest",
        "GradientBoosting",
        "SMOTE",
    }

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

    def validate_solutions(
        self,
        solutions: List[Dict[str, Any]],
        current_graph: List[str],
    ) -> Dict[str, Any]:
        """
        Validate and authorize structural candidates.

        A candidate is accepted only when all authorization
        conditions pass.

        No invalid candidate is selected as a fallback.
        """

        validated_solutions = []

        for solution in solutions:

            validation_result = (
                self._validate_solution(
                    solution,
                    current_graph,
                )
            )

            validated_solutions.append(
                validation_result
            )

        selected_solution = (
            self._select_best_solution(
                validated_solutions
            )
        )

        result = {
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),

            "validated_solutions":
                validated_solutions,

            "selected_solution":
                selected_solution,

            "validation_threshold":
                self.validation_threshold,

            "resource_budget":
                self.resource_budget,

            "current_graph":
                list(current_graph),
        }

        self.validation_history.append(
            result
        )

        if selected_solution is not None:
            self.selected_solutions.append(
                selected_solution
            )

        return result

    def _validate_solution(
        self,
        solution: Dict[str, Any],
        current_graph: List[str],
    ) -> Dict[str, Any]:
        """Apply all explicit authorization conditions."""

        invariant = self._check_invariants(
            solution.get("graph", [])
        )

        invariant_pass = bool(
            invariant["all_pass"]
        )

        resource_pass = bool(
            solution.get(
                "resource_cost",
                float("inf"),
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
            >=
            self.validation_threshold
        )

        accepted = bool(
            invariant_pass
            and resource_pass
            and safety_pass
            and utility_pass
        )

        result = dict(solution)

        result["authorization"] = {
            "accepted":
                accepted,

            "invariant":
                invariant,

            "invariant_pass":
                invariant_pass,

            "resource_pass":
                resource_pass,

            "safety_pass":
                safety_pass,

            "utility_pass":
                utility_pass,

            "current_graph":
                list(current_graph),

            "candidate_graph":
                list(
                    solution.get(
                        "graph",
                        [],
                    )
                ),
        }

        result["validation_score"] = utility
        result["is_valid"] = accepted

        return result

    def _check_invariants(
        self,
        candidate_graph: List[str],
    ) -> Dict[str, bool]:
        """Validate structural graph invariants."""

        graph = list(
            candidate_graph
        )

        checks = {
            "starts_with_input":
                (
                    len(graph) >= 2
                    and graph[0] == "Input"
                ),

            "ends_with_output":
                (
                    len(graph) >= 2
                    and graph[-1] == "Output"
                ),

            "unique_nodes":
                (
                    len(graph)
                    ==
                    len(set(graph))
                ),

            "allowed_nodes":
                (
                    set(graph).issubset(
                        self.ALLOWED_NODES
                    )
                ),
        }

        checks["all_pass"] = bool(
            all(
                checks.values()
            )
        )

        return checks

    def _select_best_solution(
        self,
        validated_solutions: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Select the highest-utility authorized candidate.

        No fallback to rejected candidates is permitted.
        """

        authorized = [
            solution
            for solution
            in validated_solutions
            if solution.get(
                "authorization",
                {}
            ).get(
                "accepted",
                False,
            )
        ]

        if not authorized:
            return None

        return max(
            authorized,
            key=lambda solution:
                float(
                    solution.get(
                        "utility",
                        0.0,
                    )
                ),
        )

    def get_validation_history(self):
        """Return complete authorization history."""

        return self.validation_history

    def get_selected_solutions(self):
        """Return successfully authorized solutions."""

        return self.selected_solutions
