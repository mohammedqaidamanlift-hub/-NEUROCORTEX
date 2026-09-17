"""
NeuroCortex SRDF Core Orchestration.

Controlled SRDF cycle:

Observe
    ->
Analyze
    ->
Generate
    ->
Evaluate
    ->
Authorize
    ->
Commit / Reject
    ->
Updated State
"""

import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import numpy as np

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from imblearn.over_sampling import SMOTE

from .trawler import Trawler
from .generator import Generator
from .arbiter import Arbiter


class SRDFFramework:
    """Main NeuroCortex SRDF orchestrator."""

    def __init__(self, config=None):

        self.config = self._default_config()

        if config:
            self.config.update(config)

        self.trawler = Trawler(
            imbalance_threshold=
            self.config["imbalance_threshold"]
        )

        self.generator = Generator()

        self.arbiter = Arbiter(
            validation_threshold=
            self.config["validation_threshold"],

            resource_budget=
            self.config["resource_budget"],
        )

        self.state = {
            "graph": [
                "Input",
                "RandomForest",
                "Output",
            ],

            "version": 0,

            "rejection_count": 0,
        }

        self.cycle_count = 0

        self.cycle_history: List[
            Dict[str, Any]
        ] = []

        self.is_running = False

    @staticmethod
    def _default_config():

        return {
            "cycle_interval": 3600,

            "validation_threshold": 0.85,

            "resource_budget": 3.0,

            "max_cycles": 100,

            "imbalance_threshold": 3.0,

            "random_seed": 42,

            "k_max": 3,

            "w_accuracy": 0.50,

            "w_safety": 0.30,

            "w_efficiency": 0.20,
        }

    @staticmethod
    def _calculate_metrics(
        y_true,
        y_pred,
    ):

        return {
            "accuracy":
                float(
                    accuracy_score(
                        y_true,
                        y_pred,
                    )
                ),

            "precision":
                float(
                    precision_score(
                        y_true,
                        y_pred,
                        zero_division=0,
                    )
                ),

            "recall":
                float(
                    recall_score(
                        y_true,
                        y_pred,
                        zero_division=0,
                    )
                ),

            "f1":
                float(
                    f1_score(
                        y_true,
                        y_pred,
                        zero_division=0,
                    )
                ),
        }

    def _evaluate_candidate(
        self,
        candidate: Dict[str, Any],
        X_train,
        y_train,
        X_test,
        y_test,
    ) -> Dict[str, Any]:

        test_fingerprint_before = (
            float(np.sum(X_test)),
            float(np.mean(X_test)),
            int(len(y_test)),
        )

        seed = self.config[
            "random_seed"
        ]

        if candidate["name"] == "GradientBoosting":

            model = GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                random_state=seed,
            )

            model.fit(
                X_train,
                y_train,
            )

            predictions = model.predict(
                X_test
            )

        elif candidate["name"] == "SMOTE_RandomForest":

            smote = SMOTE(
                random_state=seed
            )

            X_resampled, y_resampled = (
                smote.fit_resample(
                    X_train,
                    y_train,
                )
            )

            model = RandomForestClassifier(
                n_estimators=100,
                random_state=seed,
            )

            model.fit(
                X_resampled,
                y_resampled,
            )

            predictions = model.predict(
                X_test
            )

        else:

            raise ValueError(
                f"Unknown candidate: "
                f"{candidate['name']}"
            )

        metrics = self._calculate_metrics(
            y_test,
            predictions,
        )

        test_fingerprint_after = (
            float(np.sum(X_test)),
            float(np.mean(X_test)),
            int(len(y_test)),
        )

        safety_checks = {

            "finite_predictions":
                bool(
                    np.all(
                        np.isfinite(
                            predictions
                        )
                    )
                ),

            "finite_metrics":
                bool(
                    all(
                        np.isfinite(
                            list(
                                metrics.values()
                            )
                        )
                    )
                ),

            "test_set_unchanged":
                bool(
                    test_fingerprint_before
                    ==
                    test_fingerprint_after
                ),
        }

        safety_pass = bool(
            all(
                safety_checks.values()
            )
        )

        efficiency = float(
            min(
                1.0,
                self.config[
                    "resource_budget"
                ]
                /
                candidate[
                    "resource_cost"
                ],
            )
        )

        utility = float(
            self.config["w_accuracy"]
            * metrics["accuracy"]
            +
            self.config["w_safety"]
            * float(safety_pass)
            +
            self.config["w_efficiency"]
            * efficiency
        )

        result = deepcopy(
            candidate
        )

        result.update(
            {
                "metrics": metrics,
                "safety_checks": safety_checks,
                "safety_pass": safety_pass,
                "efficiency": efficiency,
                "utility": utility,
                "predictions": predictions,
            }
        )

        return result

    def run_cycle(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
    ) -> Dict[str, Any]:

        cycle_start = datetime.now(
            timezone.utc
        )

        state_before = deepcopy(
            self.state
        )

        findings = self.trawler.analyze(
            y_train,
            self.state,
        )

        candidates = (
            self.generator.propose_solutions(
                findings
            )
        )

        evaluated_candidates = []

        for candidate in candidates:

            evaluated_candidates.append(
                self._evaluate_candidate(
                    candidate,
                    X_train,
                    y_train,
                    X_test,
                    y_test,
                )
            )

        validation_results = (
            self.arbiter.validate_solutions(
                evaluated_candidates,
                self.state["graph"],
            )
        )

        selected = (
            validation_results[
                "selected_solution"
            ]
        )

        if selected is not None:

            old_graph = (
                self.state["graph"].copy()
            )

            self.state["graph"] = (
                selected["graph"].copy()
            )

            self.state["version"] += 1

            self.state[
                "rejection_count"
            ] = 0

            transition = {
                "decision": "ACCEPT",
                "candidate": selected["name"],
                "old_graph": old_graph,
                "new_graph":
                    self.state["graph"].copy(),
                "state_version":
                    self.state["version"],
            }

        else:

            self.state[
                "rejection_count"
            ] += 1

            backoff_triggered = bool(
                self.state[
                    "rejection_count"
                ]
                >=
                self.config["k_max"]
            )

            if backoff_triggered:

                self.state[
                    "rejection_count"
                ] = 0

            transition = {
                "decision": "REJECT_ALL",
                "graph_preserved": True,
                "backoff_triggered":
                    backoff_triggered,
                "rejection_count":
                    self.state["rejection_count"],
                "state_version":
                    self.state["version"],
            }

        cycle_result = {

            "cycle_number":
                self.cycle_count,

            "start_time":
                cycle_start.isoformat(),

            "duration_seconds":
                (
                    datetime.now(
                        timezone.utc
                    )
                    - cycle_start
                ).total_seconds(),

            "state_before":
                state_before,

            "trawler_findings":
                findings,

            "proposed_solutions":
                candidates,

            "evaluated_candidates":
                evaluated_candidates,

            "validation_results":
                validation_results,

            "selected_solution":
                (
                    selected["name"]
                    if selected is not None
                    else None
                ),

            "state_transition":
                transition,

            "state_after":
                deepcopy(
                    self.state
                ),
        }

        self.cycle_count += 1

        self.cycle_history.append(
            cycle_result
        )

        return cycle_result

    def start_evolution(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        max_cycles: Optional[int] = None,
    ):

        self.is_running = True

        results = []

        cycles = (
            self.config["max_cycles"]
            if max_cycles is None
            else int(max_cycles)
        )

        for _ in range(cycles):

            if not self.is_running:
                break

            result = self.run_cycle(
                X_train,
                y_train,
                X_test,
                y_test,
            )

            results.append(result)

            if (
                self.config["cycle_interval"]
                > 0
            ):

                import time

                time.sleep(
                    self.config["cycle_interval"]
                )

        return results

    def stop_evolution(self):
        """Stop the SRDF loop."""

        self.is_running = False

    def get_status(self):

        return {
            "is_running":
                self.is_running,

            "cycle_count":
                self.cycle_count,

            "config":
                deepcopy(self.config),

            "state":
                deepcopy(self.state),

            "last_activity":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

    def save_progress(
        self,
        filename="neurocortex_progress.json",
    ):

        progress_data = {
            "cycle_history":
                self._json_safe(
                    self.cycle_history
                ),

            "state":
                self._json_safe(
                    self.state
                ),

            "config":
                self._json_safe(
                    self.config
                ),

            "save_time":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                progress_data,
                f,
                indent=2,
                ensure_ascii=False,
            )

    def load_config(self, config):
        self.config.update(config)

    def get_cycle_history(self):
        return self.cycle_history

    @staticmethod
    def _json_safe(value):

        if isinstance(
            value,
            np.generic,
        ):
            return value.item()

        if isinstance(
            value,
            np.ndarray,
        ):
            return value.tolist()

        if isinstance(
            value,
            dict,
        ):

            return {
                str(key):
                    SRDFFramework._json_safe(
                        val
                    )
                for key, val in value.items()
            }

        if isinstance(
            value,
            list,
        ):

            return [
                SRDFFramework._json_safe(
                    item
                )
                for item in value
            ]

        if isinstance(
            value,
            tuple,
        ):

            return [
                SRDFFramework._json_safe(
                    item
                )
                for item in value
            ]

        return value
