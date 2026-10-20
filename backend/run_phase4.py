"""CLI runner for Phase 4: Anomaly Detection."""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AQUASENTINEL_DIR = os.path.join(SCRIPT_DIR, 'aquasentinel')
sys.path.insert(0, AQUASENTINEL_DIR)

from src.anomaly import run_anomaly_pipeline

PROCESSED_DIR = os.path.join(AQUASENTINEL_DIR, 'data', 'processed')
FIGURES_DIR   = os.path.join(AQUASENTINEL_DIR, 'figures')

print("\n=== PHASE 4: Within-Cluster Anomaly Detection ===")
df, top_anomalies = run_anomaly_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print(f"\nTotal wells scored : {df['anomaly_score'].notna().sum():,}")
print(f"Anomalies flagged  : {df['is_anomaly'].sum():,}")
print(f"Anomaly rate       : {df['is_anomaly'].mean():.2%}")

print("\n--- Top 10 Most Anomalous Wells ---")
cols = ['station','state','district','cluster_dbscan','anomaly_score','is_contaminated']
cols = [c for c in cols if c in top_anomalies.columns]
print(top_anomalies[cols].head(10).to_string(index=False))

print(f"\nFigures saved to: {FIGURES_DIR}/")
