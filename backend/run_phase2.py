"""Quick validation script to run Phase 2 pipeline from command line."""
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AQUASENTINEL_DIR = os.path.join(SCRIPT_DIR, 'aquasentinel')
sys.path.insert(0, AQUASENTINEL_DIR)

from src.data_prep import run_data_prep
from src.classifier import run_classifier_pipeline

PROCESSED_DIR = os.path.join(AQUASENTINEL_DIR, 'data', 'processed')
FIGURES_DIR   = os.path.join(AQUASENTINEL_DIR, 'figures')

print("\n=== PHASE 2: Data Preparation ===")
X_train, X_test, y_train, y_test, encoders, df_prepared = run_data_prep(PROCESSED_DIR)

print(f"\nTraining set : {len(X_train):,} samples  |  Contamination: {y_train.mean():.2%}")
print(f"Test set     : {len(X_test):,} samples  |  Contamination: {y_test.mean():.2%}")

print("\n=== PHASE 2: Classifier Training & Evaluation ===")
results = run_classifier_pipeline(X_train, X_test, y_train, y_test, figures_dir=FIGURES_DIR)

print("\n=== FINAL SUMMARY ===")
for name, res in results.items():
    print(f"  {name:<30s}  ROC-AUC={res['roc_auc']:.4f}  AvgPrec={res['avg_precision']:.4f}")

print(f"\nFigures saved to: {FIGURES_DIR}/")
