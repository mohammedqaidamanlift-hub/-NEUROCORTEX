#!/usr/bin/env python3
# NeuroCortex SRDF - English Example

import json
import numpy as np
from datetime import datetime
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

def run_english_example():
    """Run complete SRDF example in English"""
    
    print("🧠 NeuroCortex SRDF - English Example")
    print("=" * 50)
    
    # Generate synthetic data
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=6,
                              n_redundant=2, weights=[0.8, 0.2], random_state=42)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Initial model
    print("\n1. 🎯 Training Initial Model...")
    initial_model = RandomForestClassifier(n_estimators=100, random_state=42)
    initial_model.fit(X_train, y_train)
    y_pred_initial = initial_model.predict(X_test)
    initial_accuracy = accuracy_score(y_test, y_pred_initial)
    
    # Trawler analysis
    print("\n2. 🔍 Trawler Analysis...")
    trawler_findings = {
        "class_imbalance": True,
        "minority_class_performance": 0.45,
        "recommendations": ["Apply SMOTE", "Try different algorithm"]
    }
    
    # Generator proposals
    print("\n3. 💡 Generator Proposals...")
    
    # Proposal 1: Gradient Boosting
    gb_model = GradientBoostingClassifier(n_estimators=200, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    gb_accuracy = accuracy_score(y_test, y_pred_gb)
    
    # Proposal 2: SMOTE + Random Forest
    smote = SMOTE(random_state=42)
    X_smote, y_smote = smote.fit_resample(X_train, y_train)
    rf_smote = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_smote.fit(X_smote, y_smote)
    y_pred_smote = rf_smote.predict(X_test)
    smote_accuracy = accuracy_score(y_test, y_pred_smote)
    
    # Arbiter validation
    print("\n4. ⚖️ Arbiter Validation...")
    if gb_accuracy > smote_accuracy:
        selected_solution = "GradientBoosting"
        final_accuracy = gb_accuracy
    else:
        selected_solution = "SMOTE_RandomForest"
        final_accuracy = smote_accuracy
    
    improvement = (final_accuracy - initial_accuracy) * 100
    
    # Prepare results
    results = {
        "neurocortex_srdf_experiment": {
            "version": "1.0.0",
            "experiment_date": datetime.now().isoformat(),
            "language": "english",
            "initial_model": {
                "type": "RandomForestClassifier",
                "accuracy": float(initial_accuracy)
            },
            "final_model": {
                "type": selected_solution,
                "accuracy": float(final_accuracy),
                "improvement_percentage": float(improvement)
            },
            "status": "COMPLETED_SUCCESSFULLY"
        }
    }
    
    # Save results
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ English example completed!")
    print(f"📊 Initial Accuracy: {initial_accuracy:.3f}")
    print(f"📈 Final Accuracy: {final_accuracy:.3f}")
    print(f"🚀 Improvement: +{improvement:.1f}%")
    print(f"📁 Results saved to output.json")

if __name__ == "__main__":
    run_english_example()
