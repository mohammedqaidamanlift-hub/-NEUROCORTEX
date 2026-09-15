# src/trawler.py
"""
Trawler module for runtime context analysis and class-imbalance detection.

The implementation follows the NeuroCortex SRDF Toy Prototype v2.0
reference implementation.
"""

import json
from datetime import datetime, timezone

import numpy as np


class Trawler:
    """Runtime analysis unit for detecting adaptation-triggering conditions."""

    def __init__(self, imbalance_threshold=3.0):
        self.imbalance_threshold = float(imbalance_threshold)
        self.analysis_history = []
        self.last_analysis_time = None

    def analyze(self, y_train, current_state):
        """
        Analyze the current runtime context.

        The analysis follows the reference prototype:
        class imbalance is detected from the training-label distribution.

        Args:
            y_train: Training target labels.
            current_state: Current NeuroCortex runtime state.

        Returns:
            dict: Trawler findings.
        """
        counts = np.bincount(np.asarray(y_train, dtype=int))

        if len(counts) < 2:
            imbalance_ratio = float("inf")
        elif counts.min() == 0:
            imbalance_ratio = float("inf")
        else:
            imbalance_ratio = float(
                counts.max() / counts.min()
            )

        findings = {
            "class_imbalance": bool(
                np.isfinite(imbalance_ratio)
                and imbalance_ratio >= self.imbalance_threshold
            ),
            "imbalance_ratio": float(imbalance_ratio),
            "threshold": self.imbalance_threshold,
            "trigger": (
                "class_imbalance"
                if (
                    np.isfinite(imbalance_ratio)
                    and imbalance_ratio >= self.imbalance_threshold
                )
                else "no_trigger"
            ),
        }

        analysis_time = datetime.now(timezone.utc)

        analysis_record = {
            "timestamp": analysis_time.isoformat(),
            "findings": findings,
            "class_counts": counts.tolist(),
            "graph": list(current_state.get("graph", [])),
            "state_version": int(current_state.get("version", 0)),
        }

        self.analysis_history.append(analysis_record)
        self.last_analysis_time = analysis_time

        return findings

    def get_analysis_history(self):
        """Return the complete Trawler analysis history."""
        return self.analysis_history

    def save_analysis_report(self, filename="trawler_analysis.json"):
        """Save Trawler analysis history to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                self.analysis_history,
                f,
                indent=2,
                ensure_ascii=False,
        )
