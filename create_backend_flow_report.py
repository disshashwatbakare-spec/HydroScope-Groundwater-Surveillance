# -*- coding: utf-8 -*-
"""
create_backend_flow_report.py
==============================
Generates a comprehensive, highly structured docx document:
'Backend_Architecture_and_Flow.docx'.

Covers exclusively the backend system:
  - High-level Architectural Overview & End-to-End Execution Diagram
  - Complete File-to-File Dependency Matrix & Dataflow Pipeline
  - Deep-dive into each individual script and module:
      * Master Orchestrator: run_all.py
      * Individual Phase Runners: run_phase2.py, run_phase3.py, run_phase4.py, run_pipeline.py
      * Source Modules (src/):
          - ingest.py (Data Ingestion & Column Normalization)
          - merge.py (Multi-Dataset Outer Join & Temporal Matching)
          - data_prep.py (Leak-Free Feature Engineering & Imputation)
          - classifier.py (SMOTE, Random Forest, AdaBoost, Cost-Benefit)
          - clustering.py (DBSCAN & Agglomerative Hierarchical)
          - anomaly.py (Within-Cluster Isolation Forest)
          - bayesian_network.py (pgmpy Causal DAG, MLE & Inference)
          - active_learning.py (Entropy, Hybrid Acquisition & Simulation)
  - Data Artifacts Flow (Raw -> Unified -> Prepared -> Clustered -> Anomaly -> Bayesian -> Queue)
  - Figures & Visualization Artifacts Catalog
  - Step-by-Step Execution Guide (Environment Setup, Execution, CLI Outputs)
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = "Backend_Architecture_and_Flow.docx"

# Professional Theme: Tech Navy, Deep Slate, Soft Blue Accent
NAVY = "1B365D"
BLUE = "DCEAF7"
PALE = "F4F7FB"
BORDER_COLOR = "CBD5E1"
DARK_TEXT = RGBColor(30, 41, 59)
NAVY_TEXT = RGBColor(27, 54, 93)
GRAY_TEXT = RGBColor(100, 116, 139)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_border(cell, color=BORDER_COLOR):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), color)


def set_cell_margin(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    mar = tc_pr.first_child_found_in("w:tcMar")
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tc_pr.append(mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = mar.find(qn("w:" + side))
        if node is None:
            node = OxmlElement("w:" + side)
            mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        shade(cell, NAVY)
        set_cell_border(cell)
        set_cell_margin(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9.5)
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cell = cells[i]
            cell.text = str(value)
            if ri % 2 == 1:
                shade(cell, PALE)
            set_cell_border(cell)
            set_cell_margin(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
                    r.font.color.rgb = DARK_TEXT
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)
    return table


def bullet(doc, title, desc, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(title)
    r_title.bold = True
    r_title.font.color.rgb = NAVY_TEXT
    r_desc = p.add_run(desc)
    r_desc.font.color.rgb = DARK_TEXT
    return p


def code_block(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.width = Inches(7.0)
    shade(cell, "0F172A")  # Deep Slate/Code Background
    set_cell_border(cell, "334155")
    set_cell_margin(cell, top=100, start=140, bottom=100, end=140)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(226, 232, 240)  # Light gray-white
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)


doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.7)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.75)
sec.right_margin = Inches(0.75)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Calibri"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
normal.font.size = Pt(10)
normal.font.color.rgb = DARK_TEXT
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.line_spacing = 1.15

for name, size, space_b, space_a in (
    ("Title", 22, Pt(0), Pt(4)),
    ("Heading 1", 13.5, Pt(14), Pt(5)),
    ("Heading 2", 11, Pt(9), Pt(3)),
    ("Heading 3", 10, Pt(6), Pt(2)),
):
    s = styles[name]
    s.font.name = "Calibri"
    s._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    s.font.size = Pt(size)
    s.font.color.rgb = NAVY_TEXT
    s.font.bold = True
    s.paragraph_format.space_before = space_b
    s.paragraph_format.space_after = space_a

# Title & Subtitle
p_title = doc.add_paragraph(style="Title")
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.add_run("AquaSentinel / HydroScope")

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(12)
r_sub = p_sub.add_run("Backend Architecture, File Dependency Graph & Execution Workflow")
r_sub.bold = True
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = GRAY_TEXT

# ==============================================================================
# SECTION 1: SYSTEM OVERVIEW & PIPELINE FLOW
# ==============================================================================
doc.add_heading("1. Backend System Overview & Pipeline Flow", level=1)
doc.add_paragraph(
    "The AquaSentinel backend is engineered as a modular, six-stage machine learning pipeline designed to solve the rural groundwater "
    "monitoring resource-allocation problem. The backend ingests multi-decade government water quality records, handles extreme class imbalance, "
    "delineates spatial hydro-geological cohorts, isolates localized anomalies, performs explainable Bayesian causal inference, and optimizes "
    "monthly physical testing schedules via pool-based active learning."
)
doc.add_paragraph(
    "The end-to-end backend workflow is structured into six sequential phases managed by a centralized master orchestrator:"
)

# Textual Architecture Diagram
code_block(doc, """+-----------------------------------------------------------------------------------------------------------------+
|                                        AQUASENTINEL BACKEND EXECUTION FLOW                                      |
+-----------------------------------------------------------------------------------------------------------------+
                                                          |
                                                          v
  [ PHASE 1: INGESTION & MERGING ]                  src/ingest.py + src/merge.py
  * Reads 15 Raw CSVs (Chemical, Physical, Levels) across 5 states (MH, AP, WB, RJ, GJ).
  * Column normalization, regex standard tokenization, and compound temporal-spatial joining.
  * OUTPUT: data/processed/unified_wells.csv (102,109 rows, 86 columns)
                                                          |
                                                          v
  [ PHASE 2: DATA PREP & CLASSIFICATION ]           src/data_prep.py + src/classifier.py
  * Resolves coordinates, imputes missing GWL with district medians, creates binary EC>3000 target.
  * Trains SMOTE + Random Forest (200 trees) and SMOTE + AdaBoost under asymmetric cost matrix.
  * OUTPUT: data/processed/prepared_wells.csv (36,922 rows) + Model Evaluation Curves
                                                          |
                                                          v
  [ PHASE 3: SPATIAL CLUSTERING ]                   src/clustering.py
  * Standardizes 5 leak-free features (lat, lon, gwl, state, district).
  * Unsupervised spatial density clustering via DBSCAN (eps=0.35, min_samples=10) & Agglomerative.
  * OUTPUT: data/processed/clustered_wells.csv (36,922 rows, 39 DBSCAN clusters)
                                                          |
                                                          v
  [ PHASE 4: WITHIN-CLUSTER ANOMALY SCORING ]       src/anomaly.py
  * Executes Isolation Forest independently inside each DBSCAN cluster (peers comparison).
  * Path length scoring isolates wells that deviate from local hydro-geological norms.
  * OUTPUT: data/processed/anomaly_wells.csv (36,922 rows, 1,749 anomalies flagged)
                                                          |
                                                          v
  [ PHASE 5: BAYESIAN CAUSAL INFERENCE ]            src/bayesian_network.py
  * Discretizes depth, district urban risk, cluster risk, and anomaly status into pgmpy DAG.
  * Maximum Likelihood Estimation (MLE) fits CPTs; Variable Elimination computes exact posteriors.
  * OUTPUT: data/processed/bayesian_wells.csv (36,922 rows with bbn_prob_contaminated)
                                                          |
                                                          v
  [ PHASE 6: ACTIVE LEARNING SURVEILLANCE QUEUE ]   src/active_learning.py
  * Computes Shannon Entropy, Least Confidence, and multi-objective Hybrid Priority Scores.
  * Runs 8-round sequential field testing simulation (budget=50/round) vs Random Baseline.
  * OUTPUT: data/processed/testing_priority_queue.csv + active_learning_simulation.csv
+-----------------------------------------------------------------------------------------------------------------+""")

# ==============================================================================
# SECTION 2: FILE DIRECTORY HIERARCHY
# ==============================================================================
doc.add_heading("2. File Directory Hierarchy & Physical Layout", level=1)
doc.add_paragraph(
    "The physical organization of the backend code and data directories is structured to separate raw government data, "
    "reusable source algorithms, processed intermediate datasets, and generated figure artifacts:"
)

code_block(doc, """Mini Project/
  |-- backendrun.txt                       <-- Quick activation & run commands
  |-- backend/
        |-- run_all.py                     <-- MASTER ORCHESTRATOR: Executes Phases 1 through 6
        |-- run_pipeline.py                <-- Dedicated runner for Phase 1 (Ingest & Merge)
        |-- run_phase2.py                  <-- Dedicated runner for Phase 2 (Prep & Classifier)
        |-- run_phase3.py                  <-- Dedicated runner for Phase 3 (Clustering)
        |-- run_phase4.py                  <-- Dedicated runner for Phase 4 (Anomaly Detection)
        |-- export_to_frontend.py          <-- Bridge exporter: Transforms CSVs into live JSON
        |-- aquasentinel/
              |-- requirements.txt         <-- Python package dependencies
              |-- README.md                <-- Technical backend specification
              |-- data/
              |     |-- raw/               <-- 15 Government CGWB source CSV files
              |     |     |-- chemical_mh.csv, physical_mh.csv, levels_mh.csv
              |     |     |-- chemical_ap.csv, physical_ap.csv, levels_ap.csv
              |     |     |-- chemical_wb.csv, physical_wb.csv, levels_wb.csv
              |     |     |-- chemical_rj.csv, physical_rj.csv, levels_rj.csv
              |     |     |-- chemical_gj.csv, physical_gj.csv, levels_gj.csv
              |     |-- processed/         <-- Generated pipeline datasets (CSVs)
              |           |-- unified_wells.csv
              |           |-- prepared_wells.csv
              |           |-- clustered_wells.csv
              |           |-- anomaly_wells.csv
              |           |-- bayesian_wells.csv
              |           |-- testing_priority_queue.csv
              |           |-- active_learning_simulation.csv
              |-- figures/                 <-- Publication-grade visualizations
              |     |-- roc_curve.png, pr_curve.png, cost_benefit_curve.png
              |     |-- clusters_map_dbscan.png, silhouette_dbscan.png
              |     |-- anomaly_distribution.png, cluster_*_anomalies.png
              |     |-- bbn_marginal_contamination.png, bbn_structure.txt
              |     |-- active_learning_curves.png
              |-- src/                     <-- Core algorithmic Python modules
                    |-- __init__.py
                    |-- ingest.py          <-- Phase 1: File ingestion & defensive parsing
                    |-- merge.py           <-- Phase 1: Compound join & temporal alignment
                    |-- data_prep.py       <-- Phase 2: Feature engineering & missing imputation
                    |-- classifier.py      <-- Phase 2: SMOTE Random Forest & AdaBoost
                    |-- clustering.py      <-- Phase 3: Spatial DBSCAN & Agglomerative
                    |-- anomaly.py         <-- Phase 4: Within-cluster Isolation Forest
                    |-- bayesian_network.py<-- Phase 5: pgmpy Causal DAG & Variable Elimination
                    |-- active_learning.py <-- Phase 6: Uncertainty sampling & budget simulation
                    |-- utils.py           <-- Shared mathematical & logging helpers""")

# ==============================================================================
# SECTION 3: FILE-TO-FILE DEPENDENCY & DATAFLOW MATRIX
# ==============================================================================
doc.add_heading("3. File-to-File Dependency & Dataflow Matrix", level=1)
doc.add_paragraph(
    "The table below maps how every Python script links to other files, what functions it imports, "
    "what datasets it consumes, and what artifacts it emits:"
)

add_table(doc, ["Source File", "Imported By / Calls", "Inputs (Files / Dependencies)", "Outputs (Datasets & Figures)"], [
    ["src/ingest.py", "Called by src/merge.py & run_all.py", "Raw CSV files in data/raw/ (chemical, physical, levels for 5 states)", "Standardized in-memory DataFrames with canonical column headers."],
    ["src/merge.py", "Called by run_all.py & run_pipeline.py", "In-memory DataFrames from ingest_all_states()", "data/processed/unified_wells.csv (102,109 rows, 86 cols) + Merge Quality Report."],
    ["src/data_prep.py", "Called by src/classifier.py & run_all.py", "data/processed/unified_wells.csv", "data/processed/prepared_wells.csv (36,922 rows) + X_train, X_test, y_train, y_test."],
    ["src/classifier.py", "Called by run_all.py & run_phase2.py", "X_train, X_test from data_prep.py; imbalanced-learn, scikit-learn", "roc_curve.png, pr_curve.png, cost_benefit_curve.png, confusion_matrix_*.png."],
    ["src/clustering.py", "Called by run_all.py & run_phase3.py", "data/processed/prepared_wells.csv", "data/processed/clustered_wells.csv (36,922 rows) + clusters_map_dbscan.png, silhouette_dbscan.png."],
    ["src/anomaly.py", "Called by run_all.py & run_phase4.py", "data/processed/clustered_wells.csv", "data/processed/anomaly_wells.csv (36,922 rows) + anomaly_distribution.png, cluster_*_anomalies.png."],
    ["src/bayesian_network.py", "Called by run_all.py (Phase 5)", "data/processed/anomaly_wells.csv; pgmpy (DiscreteBayesianNetwork)", "data/processed/bayesian_wells.csv + bbn_marginal_contamination.png, bbn_structure.txt."],
    ["src/active_learning.py", "Called by run_all.py (Phase 6)", "data/processed/bayesian_wells.csv", "data/processed/testing_priority_queue.csv, active_learning_simulation.csv, active_learning_curves.png."],
    ["run_all.py", "Executed directly from terminal", "All 8 modules in src/", "Orchestrates all 6 phases sequentially; refreshes all processed datasets and figure artifacts."],
    ["export_to_frontend.py", "Called at conclusion of run_all.py", "testing_priority_queue.csv, bayesian_wells.csv", "frontend/src/data/live_pipeline_data.json (Clean, sanitized JSON bridge)."],
], [1.3, 1.4, 1.8, 2.5])

# ==============================================================================
# SECTION 4: IN-DEPTH BREAKDOWN OF BACKEND MODULES
# ==============================================================================
doc.add_heading("4. In-Depth Technical Breakdown of Backend Modules", level=1)

# 4.1 Ingestion & Merge
doc.add_heading("4.1 Phase 1: Ingestion & Merge Engine (ingest.py & merge.py)", level=2)
doc.add_paragraph(
    "Responsible for loading, cleaning, and synthesizing disparate government records across 64 years of manual surveillance:"
)
bullet(doc, "ingest.py Functions: ", "ingest_cgwb_file(filepath, file_type, state_code) defensively loads each CSV, catches encoding anomalies, "
       "and calls normalize_columns() to standardize headers into clean lowercase snake_case. standardize_core_columns() maps 46 diverse aliases "
       "into canonical keys: ['station', 'district', 'state', 'date', 'lat', 'lon', 'ph', 'ec', 'tds', 'fluoride', 'nitrate']. "
       "ingest_all_states() aggregates across all 5 states.")
bullet(doc, "merge.py Functions: ", "perform_merge(chem_df, phys_df, levels_df) executes an outer join using a composite temporal-spatial key: "
       "['station', 'district', 'state', 'date_month']. Dates are parsed and floored to monthly intervals ('YYYY-MM') to resolve minor day-level "
       "discrepancies between physical site surveys and chemical laboratory assays. run_merge_pipeline() saves the 102,109-row unified dataset "
       "and logs column-by-column missingness percentages via generate_report().")

# 4.2 Data Prep & Classifier
doc.add_heading("4.2 Phase 2: Data Prep & Supervised Classifier (data_prep.py & classifier.py)", level=2)
doc.add_paragraph(
    "Transforms raw multi-table observations into leak-free, model-ready feature sets and trains cost-sensitive ensemble models:"
)
bullet(doc, "data_prep.py Functions: ", "consolidate_coordinates() resolves triplicate coordinate columns ('lat_chem', 'lat_phys', 'lat') "
       "by prioritizing geodetic water level benchmarks, physical registries, and chemical records. build_contamination_target() sets "
       "is_contaminated = 1 for EC > 3,000 µS/cm. impute_missing_groundwater_levels() applies district-level medians. encode_categoricals() "
       "fits LabelEncoders. run_data_prep() produces a stratified 80/20 train/test split and saves prepared_wells.csv (36,922 rows).")
bullet(doc, "classifier.py Functions: ", "build_rf_pipeline() encapsulates SMOTE(k_neighbors=5) and RandomForestClassifier(n_estimators=200, "
       "max_depth=12, class_weight='balanced') inside an imbalanced-learn Pipeline to guarantee no synthetic data leaks into testing folds. "
       "build_adaboost_pipeline() builds an AdaBoost ensemble (150 decision stumps, learning_rate=0.5). plot_cost_benefit_curve() searches "
       "the decision threshold space under the loss function: Cost = 100*FN + 10*FP. run_classifier_pipeline() trains all models and saves "
       "ROC curves, PR curves, and confusion matrix heatmaps.")

# 4.3 Spatial Clustering
doc.add_heading("4.3 Phase 3: Spatial Clustering (clustering.py)", level=2)
doc.add_paragraph(
    "Delineates natural hydro-geological micro-regions without using the target label (EC), completely eliminating target leakage:"
)
bullet(doc, "clustering.py Functions: ", "scale_features() scales the 5 context features using StandardScaler. run_dbscan() applies "
       "DBSCAN(eps=0.35, min_samples=10), identifying 39 dense spatial clusters while isolating sparse outliers as noise (cluster -1). "
       "run_agglomerative() builds an 8-cluster hierarchical baseline using Ward's minimum-variance linkage. "
       "compute_clustering_metrics() calculates Silhouette Scores (DBSCAN=0.4262, Agglomerative=0.4523). run_clustering_pipeline() "
       "saves clustered_wells.csv and generates geographic cluster scatter plots.")

# 4.4 Within-Cluster Anomaly Detection
doc.add_heading("4.4 Phase 4: Within-Cluster Anomaly Detection (anomaly.py)", level=2)
doc.add_paragraph(
    "Solves the geological confounding problem by scoring anomalies strictly relative to local cluster peers:"
)
bullet(doc, "anomaly.py Functions: ", "score_cluster_anomalies() iterates through each DBSCAN cluster with >=20 wells and fits an independent "
       "IsolationForest(n_estimators=200, contamination=0.05). Points requiring fewer tree partitions have shorter path lengths and negative "
       "decision scores. flag_anomalies() marks the top 5% most unusual wells per cluster (is_anomaly = 1). run_anomaly_pipeline() "
       "evaluates 36,314 wells, flags 1,749 localized anomalies (4.74%), and saves anomaly_wells.csv.")

# 4.5 Bayesian Belief Network
doc.add_heading("4.5 Phase 5: Bayesian Belief Network (bayesian_network.py)", level=2)
doc.add_paragraph(
    "Provides causal probabilistic reasoning and explainable audit trails using pgmpy:"
)
bullet(doc, "bayesian_network.py Functions: ", "discretise_features() buckets features into causal states: bbn_gwl_depth (Shallow <5m, Med 5-15m, "
       "Deep >15m), bbn_district_urban (Rural vs Urban mean EC), bbn_cluster_risk (High >=10% cluster contamination vs Low), and bbn_anomaly (0 vs 1). "
       "build_and_fit_bbn() constructs a 6-node DiscreteBayesianNetwork DAG and fits Conditional Probability Tables (CPTs) via Maximum Likelihood Estimation (MLE). "
       "infer_well_risk() uses VariableElimination to compute P(HighEC | Evidence). explain_well() translates probabilities into plain-language "
       "text explanations. run_bbn_pipeline() computes posteriors for all 36,922 wells, exports bayesian_wells.csv, and writes bbn_structure.txt.")

# 4.6 Active Learning
doc.add_heading("4.6 Phase 6: Active Learning Surveillance Queue (active_learning.py)", level=2)
doc.add_paragraph(
    "Transforms model predictions into a prioritized monthly laboratory testing queue under budget constraints:"
)
bullet(doc, "active_learning.py Functions: ", "calculate_entropy() computes normalized Shannon Entropy H(p) = - [p*log2(p) + (1-p)*log2(1-p)]. "
       "compute_acquisition_scores() formulates the multi-objective priority score: Priority = 0.50*Entropy + 0.30*BBN_Risk + 0.20*Anomaly_Urgency. "
       "simulate_active_learning() runs an 8-round simulation (budget B=50 tests/round) comparing Active Learning vs Uniform Random Sampling. "
       "plot_active_learning_curves() plots cumulative contaminants found and model ROC-AUC progression. run_active_learning_pipeline() "
       "ranks all 36,922 wells, exports testing_priority_queue.csv, and records active_learning_simulation.csv.")

# ==============================================================================
# SECTION 5: DATA ARTIFACTS EVOLUTION
# ==============================================================================
doc.add_heading("5. Data Artifacts Evolution & Schema Transformation", level=1)
doc.add_paragraph(
    "As raw data moves through the backend pipeline, each script consumes the output of the preceding stage and augments it with new "
    "analytical attributes. The table below traces the lifecycle of the surveillance dataset:"
)

add_table(doc, ["File Name", "Generated By", "Key Schema & Added Columns", "Role in Pipeline"], [
    ["unified_wells.csv", "src/merge.py", "station, district, state, date, ec, ph, tds, groundwater_level_quarterly_manual_meter, lat, lon (86 cols)", "Master raw union of all chemical, physical, and level logs."],
    ["prepared_wells.csv", "src/data_prep.py", "latitude, longitude, groundwater_level_m, state_encoded, district_encoded, is_contaminated, ec_numeric", "Clean, imputed, leak-free supervised baseline dataset."],
    ["clustered_wells.csv", "src/clustering.py", "prepared columns + cluster_dbscan, cluster_agg", "Partitions monitoring wells into hydro-geological cohorts."],
    ["anomaly_wells.csv", "src/anomaly.py", "clustered columns + anomaly_score, is_anomaly", "Augments wells with local Isolation Forest outlier scores."],
    ["bayesian_wells.csv", "src/bayesian_network.py", "anomaly columns + bbn_gwl_depth, bbn_district_urban, bbn_cluster_risk, bbn_prob_contaminated", "Augments wells with discrete causal nodes and BBN posterior risk."],
    ["testing_priority_queue.csv", "src/active_learning.py", "bayesian columns + uncertainty_entropy, testing_priority_score, priority_tier, priority_rank, testing_reason", "Final production surveillance queue ranking all 36,922 wells for field testing triage."],
    ["active_learning_simulation.csv", "src/active_learning.py", "round, tests_conducted, al_cum_contam, rnd_cum_contam, al_auc, rnd_auc, contam_discovery_delta", "Empirical proof logging Active Learning sample efficiency vs Random baseline."],
], [1.6, 1.2, 2.5, 1.7])

# ==============================================================================
# SECTION 6: HOW TO EXECUTE THE BACKEND
# ==============================================================================
doc.add_heading("6. Step-by-Step Backend Execution Guide", level=1)
doc.add_paragraph(
    "The backend can be executed in its entirety with a single terminal command, or inspected modularly phase by phase:"
)

doc.add_heading("Option A: Running the Full 6-Phase Pipeline (Recommended)", level=2)
doc.add_paragraph(
    "To run the complete data ingestion, classification, clustering, anomaly detection, Bayesian inference, and active learning pipeline "
    "end-to-end, open PowerShell or Command Prompt and execute:"
)

code_block(doc, """# 1. Activate the Python virtual environment
& "c:\\Data Backup\\MIT-WPU\\Semester V\\ML-Lab\\.venv\\Scripts\\Activate.ps1"

# 2. Navigate to the project root directory
cd "c:\\Data Backup\\MIT-WPU\\Semester V\\ML-Lab\\Mini Project"

# 3. Execute the Master Pipeline Runner
python backend/run_all.py""")

doc.add_paragraph(
    "Execution Runtime: Approximately 45 to 60 seconds total. Terminal output logs phase-by-phase progress, sample well risk explanations, "
    "and top priority queue recommendations."
)

doc.add_heading("Option B: Running Individual Phases Independently", level=2)
doc.add_paragraph(
    "Individual stages can be re-run in isolation when fine-tuning hyperparameters or analyzing intermediate results:"
)

code_block(doc, """# Run Phase 1 only: Ingest and merge raw government CSVs
python backend/run_pipeline.py

# Run Phase 2 only: Feature prep, SMOTE, and Random Forest / AdaBoost
python backend/run_phase2.py

# Run Phase 3 only: DBSCAN and Agglomerative Spatial Clustering
python backend/run_phase3.py

# Run Phase 4 only: Within-Cluster Isolation Forest Anomaly Detection
python backend/run_phase4.py

# Run Phase 5 only: Bayesian Belief Network Causal Inference
python -c "import sys; sys.path.insert(0, 'backend/aquasentinel'); from src.bayesian_network import run_bbn_pipeline; run_bbn_pipeline('backend/aquasentinel/data/processed', 'backend/aquasentinel/figures')"

# Run Phase 6 only: Active Learning Simulation and Priority Queue Ranking
python backend/aquasentinel/src/active_learning.py""")

# Footer
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer.add_run("AquaSentinel / HydroScope — Backend Architecture & Workflow Specification")
fr.font.size = Pt(8.5)
fr.font.color.rgb = GRAY_TEXT

doc.save(OUT)
print(f"Successfully generated: {OUT}")
