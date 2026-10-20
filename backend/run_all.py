# -*- coding: utf-8 -*-
"""
AquaSentinel - Full Pipeline Runner
====================================
Runs all six phases sequentially:
  Phase 1 : Data Ingestion & Merging
  Phase 2 : Data Prep, Classification & Imbalance Handling
  Phase 3 : Spatial Clustering
  Phase 4 : Within-Cluster Anomaly Scoring
  Phase 5 : Bayesian Belief Network Causal Inference
  Phase 6 : Active Learning Surveillance Priority Queue

Usage (from any directory):
    python run_all.py
    python "c:\path\to\Mini Project\run_all.py"
"""

import sys
import os
import time

# Resolve paths relative to THIS file so it works from any working directory
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR      = os.path.join(SCRIPT_DIR, 'aquasentinel', 'data', 'raw')
PROCESSED_DIR = os.path.join(SCRIPT_DIR, 'aquasentinel', 'data', 'processed')
FIGURES_DIR   = os.path.join(SCRIPT_DIR, 'aquasentinel', 'figures')
STATES        = ['mh', 'rj', 'ap', 'wb', 'gj']

# Add aquasentinel to path so `from src.xxx` imports work
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'aquasentinel'))

# -- Helpers --------------------------------------------------------------------
def section(title):
    bar = "=" * 60
    print(f"\n{bar}")
    print(f"  {title}")
    print(f"{bar}")

def elapsed(start):
    s = time.time() - start
    return f"{s:.1f}s" if s < 60 else f"{s/60:.1f}m"

# ------------------------------------------------------------------------------
# PHASE 1 - Ingestion & Merge
# ------------------------------------------------------------------------------
from src.ingest import ingest_all_states
from src.merge  import run_merge_pipeline, generate_report

section("PHASE 1 : Data Ingestion & Merging")
t = time.time()

chemical_df = ingest_all_states(DATA_DIR, 'chemical', STATES)
physical_df = ingest_all_states(DATA_DIR, 'physical', STATES)
levels_df   = ingest_all_states(DATA_DIR, 'levels',   STATES)

print(f"  Chemical : {chemical_df.shape[0]:,} rows")
print(f"  Physical : {physical_df.shape[0]:,} rows")
print(f"  Levels   : {levels_df.shape[0]:,} rows")

unified_df, metrics = run_merge_pipeline(PROCESSED_DIR, chemical_df, physical_df, levels_df)
generate_report(metrics)
print(f"\n  Phase 1 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# PHASE 2 - Data Prep + Classification
# ------------------------------------------------------------------------------
from src.data_prep  import run_data_prep
from src.classifier import run_classifier_pipeline

section("PHASE 2 : Classification & Imbalance Handling")
t = time.time()

X_train, X_test, y_train, y_test, encoders, df_prepared = run_data_prep(PROCESSED_DIR)
print(f"  Train : {len(X_train):,} samples  |  Contamination: {y_train.mean():.2%}")
print(f"  Test  : {len(X_test):,} samples  |  Contamination: {y_test.mean():.2%}")

results = run_classifier_pipeline(X_train, X_test, y_train, y_test, figures_dir=FIGURES_DIR)

print("\n  --- Classifier Results ---")
for name, res in results.items():
    print(f"  {name:<32s}  ROC-AUC={res['roc_auc']:.4f}  AvgPrec={res['avg_precision']:.4f}")

print(f"\n  Phase 2 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# PHASE 3 - Spatial Clustering
# ------------------------------------------------------------------------------
from src.clustering import run_clustering_pipeline

section("PHASE 3 : Spatial Clustering")
t = time.time()

df_clustered, cluster_metrics = run_clustering_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print("\n  --- Clustering Metrics ---")
for k, v in cluster_metrics.items():
    val = f"{v:.4f}" if isinstance(v, float) else str(v)
    print(f"  {k:<30s}: {val}")

print(f"\n  Phase 3 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# PHASE 4 - Anomaly Detection
# ------------------------------------------------------------------------------
from src.anomaly import run_anomaly_pipeline

section("PHASE 4 : Within-Cluster Anomaly Detection")
t = time.time()

df_anomaly, top_anomalies = run_anomaly_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print(f"  Wells scored    : {df_anomaly['anomaly_score'].notna().sum():,}")
print(f"  Anomalies found : {df_anomaly['is_anomaly'].sum():,}")
print(f"  Anomaly rate    : {df_anomaly['is_anomaly'].mean():.2%}")

print("\n  --- Top 10 Most Anomalous Wells ---")
cols = ['station', 'state', 'district', 'cluster_dbscan', 'anomaly_score', 'is_contaminated']
cols = [c for c in cols if c in top_anomalies.columns]
print(top_anomalies[cols].head(10).to_string(index=False))

print(f"\n  Phase 4 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# PHASE 5 - Bayesian Belief Network (Causal Inference)
# ------------------------------------------------------------------------------
from src.bayesian_network import run_bbn_pipeline

section("PHASE 5 : Bayesian Belief Network Causal Inference")
t = time.time()

bbn_model, df_bbn, bbn_explanations = run_bbn_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print(f"  BBN Nodes fitted : {len(bbn_model.nodes())}")
print(f"  Wells evaluated  : {len(df_bbn):,}")
print("\n  --- Sample Well Causal Risk Explanation ---")
if bbn_explanations:
    print(bbn_explanations[0])

print(f"\n  Phase 5 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# PHASE 6 - Active Learning & Surveillance Priority Queue
# ------------------------------------------------------------------------------
from src.active_learning import run_active_learning_pipeline

section("PHASE 6 : Active Learning & Priority Queue Generation")
t = time.time()

queue_df, sim_df, al_metrics = run_active_learning_pipeline(
    PROCESSED_DIR,
    figures_dir=FIGURES_DIR,
    batch_size=50,
    n_rounds=8,
)

print(f"  Wells Ranked for Testing  : {al_metrics['total_wells_ranked']:,}")
print(f"  High Priority Wells       : {al_metrics['high_priority_wells']:,}")
print(f"  Medium Priority Wells     : {al_metrics['medium_priority_wells']:,}")
print(f"  AL vs Random Contam Lift  : +{al_metrics['contaminant_lift_pct']}% more contaminants found")
print(f"  AL Final Evaluation AUC   : {al_metrics['al_final_auc']:.4f}")

print("\n  --- Top 5 Wells in Surveillance Priority Queue ---")
q_cols = ['priority_rank', 'station', 'state', 'district', 'testing_priority_score', 'priority_tier', 'testing_reason']
q_cols = [c for c in q_cols if c in queue_df.columns]
print(queue_df[q_cols].head(5).to_string(index=False))

print(f"\n  Phase 6 complete  [{elapsed(t)}]")

# ------------------------------------------------------------------------------
# FRONTEND EXPORT - Bridge to Next.js Dashboard
# ------------------------------------------------------------------------------
section("EXPORTING LIVE DATA TO FRONTEND")
try:
    from export_to_frontend import export_pipeline_to_frontend
    out_json = export_pipeline_to_frontend()
    print(f"  Live payload generated   : {out_json}")
except Exception as e:
    print(f"  Frontend export notice   : {e}")

# ------------------------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------------------------
section("FULL PIPELINE COMPLETE")
print(f"  Unified dataset          : {PROCESSED_DIR}\\unified_wells.csv")
print(f"  Prepared dataset         : {PROCESSED_DIR}\\prepared_wells.csv")
print(f"  Clustered dataset        : {PROCESSED_DIR}\\clustered_wells.csv")
print(f"  Anomaly dataset          : {PROCESSED_DIR}\\anomaly_wells.csv")
print(f"  Bayesian dataset         : {PROCESSED_DIR}\\bayesian_wells.csv")
print(f"  Testing Priority Queue   : {PROCESSED_DIR}\\testing_priority_queue.csv")
print(f"  Active Learning Sim CSV  : {PROCESSED_DIR}\\active_learning_simulation.csv")
print(f"  Figures Directory        : {FIGURES_DIR}\\")
print()