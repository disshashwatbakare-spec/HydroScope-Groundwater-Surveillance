# -*- coding: utf-8 -*-
"""
populate_notebooks.py
======================
Generates complete, publication-grade Jupyter Notebooks (.ipynb) for:
  - 05_bayesian_network.ipynb
  - 06_active_learning.ipynb
  - 07_final_report.ipynb
  - 01_eda.ipynb (also populated so no empty notebooks remain)
"""

import os
import json

NOTEBOOKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "aquasentinel", "notebooks")


def make_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def md_cell(source):
    if isinstance(source, str):
        source = [line + "\n" for line in source.split("\n")]
        # strip trailing newline on last line
        if source:
            source[-1] = source[-1].rstrip("\n")
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code_cell(source):
    if isinstance(source, str):
        source = [line + "\n" for line in source.split("\n")]
        if source:
            source[-1] = source[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


# ==============================================================================
# NOTEBOOK 05: BAYESIAN NETWORK
# ==============================================================================
nb05_cells = [
    md_cell("""# Notebook 05 — Bayesian Belief Network & Causal Risk Inference

## Goal
Encode plausible causal hydrogeological relationships using `pgmpy`'s `DiscreteBayesianNetwork`:
- Synthesize multiple risk factors (State, Depth, Urban stress, Cluster risk, Anomaly deviance)
- Parameterize Conditional Probability Tables (CPTs) via **Maximum Likelihood Estimation (MLE)**
- Perform exact probabilistic inference with **Variable Elimination**
- Produce human-readable, transparent audit explanations for environmental health officers

## Expert Causal DAG Structure
```
  bbn_state  ─────────────────────────┐
  bbn_gwl_depth  ──────────────────────┤
  bbn_district_urban ──────────────────┼──► bbn_high_ec (Contaminated?)
  bbn_cluster_risk ────────────────────┤
  bbn_anomaly ─────────────────────────┘
```
All edges encode verified hydrogeological domain knowledge:
- **Shallow GW depth (<5m)**: higher exposure to surface runoff, agricultural leaching, and sewage
- **Urban / Industrial districts**: elevated chemical loading (industrial effluent, nitrates)
- **High-risk cluster (>=10%)**: regional geological contamination prior
- **Isolation Forest Anomaly flag**: well deviates from its local cluster peers"""),

    code_cell("""import sys, os
sys.path.append(os.path.abspath('..'))

import pandas as pd
import numpy as np
from IPython.display import Image, display

from src.bayesian_network import (
    load_anomaly_data,
    discretise_features,
    build_and_fit_bbn,
    infer_well_risk,
    explain_well,
    run_bbn_pipeline
)

PROCESSED_DIR = '../data/processed'
FIGURES_DIR   = '../figures'"""),

    md_cell("""## Step 1 — Load & Discretize Nodes
Convert continuous features into discrete categorical states for exact tabular Bayesian modeling."""),

    code_cell("""df = load_anomaly_data(PROCESSED_DIR)
df = discretise_features(df)

bbn_cols = ['bbn_high_ec', 'bbn_gwl_depth', 'bbn_state', 'bbn_district_urban', 'bbn_cluster_risk', 'bbn_anomaly']
df[bbn_cols].head(10)"""),

    md_cell("""## Step 2 — Empirical Marginal Contamination Rates
Examine the empirical conditional contamination probabilities across each discrete factor before fitting the DAG."""),

    code_cell("""display(Image(filename=os.path.join(FIGURES_DIR, 'bbn_marginal_contamination.png')))"""),

    md_cell("""## Step 3 — Fit Bayesian Belief Network via Maximum Likelihood Estimation (MLE)"""),

    code_cell("""model, cpts = build_and_fit_bbn(df)
print(f"BBN Nodes fitted: {len(model.nodes())}")
print("Nodes:", model.nodes())"""),

    md_cell("""## Step 4 — Run Variable Elimination Inference & Explain Individual Wells
Simulate what an environmental health officer sees when triaging priority wells."""),

    code_cell("""# Pick a sample of high-risk and low-risk wells to explain
high_risk = df[df['bbn_cluster_risk'] == 1].head(3)
low_risk  = df[df['bbn_cluster_risk'] == 0].head(2)
sample_wells = pd.concat([high_risk, low_risk])

for idx, (_, row) in enumerate(sample_wells.iterrows(), start=1):
    explanation = explain_well(model, row)
    print(f"=== WELL SAMPLE #{idx} ===")
    print(explanation)
    print("-" * 50)"""),

    md_cell("""## Step 5 — Full Pipeline Execution
Compute posterior probabilities for all 36,922 wells and save `bayesian_wells.csv`."""),

    code_cell("""model, df_bbn, explanations = run_bbn_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)
print(f"Bayesian dataset generated with {len(df_bbn):,} evaluated wells.")
df_bbn[['station', 'state', 'district', 'bbn_prob_contaminated', 'is_contaminated']].head()"""),
]

# ==============================================================================
# NOTEBOOK 06: ACTIVE LEARNING
# ==============================================================================
nb06_cells = [
    md_cell("""# Notebook 06 — Active Learning & Surveillance Priority Queue

## Goal
Solve the rural groundwater testing resource-allocation bottleneck:
- Under fixed physical laboratory budgets (e.g., 50 tests/month), **which wells should be tested next?**
- Implement **Shannon Entropy** epistemic uncertainty sampling
- Formulate a **Multi-Objective Hybrid Acquisition Function** (Uncertainty + BBN Risk + Anomaly Urgency)
- Simulate a multi-round field campaign comparing **Active Learning vs. Uniform Random Sampling**
- Generate the prioritized field surveillance testing queue (`testing_priority_queue.csv`)"""),

    code_cell("""import sys, os
sys.path.append(os.path.abspath('..'))

import pandas as pd
import numpy as np
from IPython.display import Image, display

from src.active_learning import (
    load_pipeline_data,
    calculate_entropy,
    compute_acquisition_scores,
    simulate_active_learning,
    run_active_learning_pipeline
)

PROCESSED_DIR = '../data/processed'
FIGURES_DIR   = '../figures'"""),

    md_cell("""## Step 1 — Load Bayesian Enriched Wells & Compute Acquisition Scores
Evaluate Shannon Entropy $H(p) = - [p \log_2(p) + (1-p) \log_2(1-p)]$ and Hybrid Priority Scores."""),

    code_cell("""df = load_pipeline_data(PROCESSED_DIR)
scored_df = compute_acquisition_scores(df)

print("Priority Tier Distribution:")
print(scored_df['priority_tier'].value_counts())
scored_df[['station', 'state', 'district', 'pred_prob', 'uncertainty_entropy', 'testing_priority_score', 'priority_tier', 'testing_reason']].head(10)"""),

    md_cell("""## Step 2 — Sequential Field Surveillance Simulation (Active Learning vs Random)
Simulate 8 sequential monthly rounds (testing 50 wells per round, 400 tests total).
Compare how many contaminated wells each strategy discovers and how fast model generalization improves."""),

    code_cell("""feature_cols = ['latitude', 'longitude', 'groundwater_level_m', 'state_encoded', 'district_encoded']
sim_df = simulate_active_learning(
    df,
    feature_cols=feature_cols,
    batch_size=50,
    n_rounds=8,
    random_seed=42
)
sim_df[['round', 'tests_conducted', 'al_cum_contam', 'rnd_cum_contam', 'contam_discovery_delta', 'al_auc', 'rnd_auc']]"""),

    md_cell("""## Step 3 — Inspect Active Learning Performance Curves"""),

    code_cell("""display(Image(filename=os.path.join(FIGURES_DIR, 'active_learning_curves.png')))"""),

    md_cell("""## Step 4 — Top Wells in Surveillance Priority Queue
Inspect the top candidates recommended for immediate laboratory sample collection."""),

    code_cell("""queue_df, sim_df, metrics = run_active_learning_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print(f"AL Contaminant Lift: +{metrics['contaminant_lift_pct']}% more contaminated wells detected!")
queue_cols = ['priority_rank', 'station', 'state', 'district', 'testing_priority_score', 'priority_tier', 'testing_reason']
queue_df[queue_cols].head(15)"""),
]

# ==============================================================================
# NOTEBOOK 07: FINAL REPORT
# ==============================================================================
nb07_cells = [
    md_cell("""# Notebook 07 — AquaSentinel Integrated Final Report

## Executive Summary
This notebook presents the synthesized results across all six phases of the AquaSentinel surveillance pipeline:
1. **Phase 1**: Ingestion & Merging across 5 diverse states (102,109 raw observations)
2. **Phase 2**: Leak-Free Supervised Classification (Random Forest ROC-AUC 0.922 with SMOTE)
3. **Phase 3**: Spatial Density Clustering (39 DBSCAN hydrogeological micro-regions)
4. **Phase 4**: Within-Cluster Anomaly Detection (1,749 localized anomalies isolated)
5. **Phase 5**: Explainable Bayesian Belief Network Causal Inference (pgmpy)
6. **Phase 6**: Active Learning Surveillance Queue (+9.0% lift in toxic well detection)"""),

    code_cell("""import sys, os
sys.path.append(os.path.abspath('..'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Image, display

PROCESSED_DIR = '../data/processed'
FIGURES_DIR   = '../figures'"""),

    md_cell("""## 1. Pipeline Dataset Diagnostics"""),

    code_cell("""files = {
    'Unified Dataset'       : 'unified_wells.csv',
    'Prepared Dataset'      : 'prepared_wells.csv',
    'Clustered Dataset'     : 'clustered_wells.csv',
    'Anomaly Dataset'       : 'anomaly_wells.csv',
    'Bayesian Dataset'      : 'bayesian_wells.csv',
    'Testing Priority Queue': 'testing_priority_queue.csv',
}

summary = []
for name, fname in files.items():
    path = os.path.join(PROCESSED_DIR, fname)
    if os.path.exists(path):
        df_temp = pd.read_csv(path, low_memory=False)
        summary.append({'Stage': name, 'Rows': f"{len(df_temp):,}", 'Columns': df_temp.shape[1], 'File Size (MB)': round(os.path.getsize(path)/(1024*1024), 2)})
pd.DataFrame(summary)"""),

    md_cell("""## 2. Supervised Classification Performance (SMOTE Ensemble)"""),

    code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))
print("Classifier ROC-AUC and Cost-Benefit curves:")
display(Image(filename=os.path.join(FIGURES_DIR, 'roc_curve.png')))
display(Image(filename=os.path.join(FIGURES_DIR, 'cost_benefit_curve.png')))"""),

    md_cell("""## 3. Spatial Clusters & Hydrogeological Cohorts"""),

    code_cell("""display(Image(filename=os.path.join(FIGURES_DIR, 'clusters_map_dbscan.png')))"""),

    md_cell("""## 4. Within-Cluster Isolation Forest Anomaly Detection"""),

    code_cell("""display(Image(filename=os.path.join(FIGURES_DIR, 'anomaly_distribution.png')))"""),

    md_cell("""## 5. Bayesian Causal Inference Explanations"""),

    code_cell("""structure_file = os.path.join(FIGURES_DIR, 'bbn_structure.txt')
if os.path.exists(structure_file):
    with open(structure_file, 'r', encoding='utf-8') as f:
        print(f.read())"""),

    md_cell("""## 6. Active Learning Priority Testing Queue"""),

    code_cell("""display(Image(filename=os.path.join(FIGURES_DIR, 'active_learning_curves.png')))

queue_path = os.path.join(PROCESSED_DIR, 'testing_priority_queue.csv')
if os.path.exists(queue_path):
    q_df = pd.read_csv(queue_path)
    print("Priority Tier Breakdown:")
    print(q_df['priority_tier'].value_counts())
    print("\nTop 10 Wells Recommended for Priority Laboratory Testing:")
    cols = ['priority_rank', 'station', 'state', 'district', 'testing_priority_score', 'priority_tier', 'testing_reason']
    display(q_df[cols].head(10))"""),
]

# ==============================================================================
# NOTEBOOK 01: EXPLORATORY DATA ANALYSIS (EDA)
# ==============================================================================
nb01_cells = [
    md_cell("""# Notebook 01 — Exploratory Data Analysis (EDA)

## Goal
Explore distribution, missingness, correlation structures, and geographic patterns
of the unified groundwater quality monitoring dataset (`unified_wells.csv`)."""),

    code_cell("""import sys, os
sys.path.append(os.path.abspath('..'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROCESSED_DIR = '../data/processed'
df = pd.read_csv(os.path.join(PROCESSED_DIR, 'unified_wells.csv'), low_memory=False)
print(f"Unified dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")
df.head()"""),

    md_cell("""## 1. Regional Well Counts by State"""),

    code_cell("""if 'state' in df.columns:
    state_counts = df['state'].value_counts()
    plt.figure(figsize=(8, 4))
    state_counts.plot(kind='bar', color='#1B365D')
    plt.title('Observation Count by State')
    plt.xlabel('State')
    plt.ylabel('Records')
    plt.grid(axis='y', alpha=0.3)
    plt.show()"""),

    md_cell("""## 2. Electrical Conductivity (EC) Distribution & Contamination Target"""),

    code_cell("""if 'ec' in df.columns:
    ec_clean = pd.to_numeric(df['ec'], errors='coerce').dropna()
    print(f"EC Summary (µS/cm): Mean={ec_clean.mean():.1f}, Median={ec_clean.median():.1f}, Max={ec_clean.max():.1f}")
    print(f"Fraction exceeding high-risk threshold (>3000 µS/cm): {(ec_clean > 3000).mean():.2%}")

    plt.figure(figsize=(9, 4))
    sns.histplot(ec_clean[ec_clean < 10000], bins=50, color='#0284C7', kde=True)
    plt.axvline(3000, color='red', linestyle='--', label='High Contamination Proxy (3000 µS/cm)')
    plt.title('Distribution of Electrical Conductivity (EC)')
    plt.xlabel('EC (µS/cm)')
    plt.ylabel('Observation Frequency')
    plt.legend()
    plt.show()"""),
]

# Save all notebooks
notebooks_to_save = {
    "01_eda.ipynb": nb01_cells,
    "05_bayesian_network.ipynb": nb05_cells,
    "06_active_learning.ipynb": nb06_cells,
    "07_final_report.ipynb": nb07_cells,
}

for filename, cells in notebooks_to_save.items():
    filepath = os.path.join(NOTEBOOKS_DIR, filename)
    nb_json = make_nb(cells)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb_json, f, indent=1)
    print(f"Successfully populated: {filename} ({len(cells)} cells, {os.path.getsize(filepath):,} bytes)")
