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
          - bayesian_network.py (pgmpy Causal DAG, MLE, Exact Inference & Explanations)
          - active_learning.py (Continuous RF Probability Bridge, Shannon Entropy, Hybrid Queue & Deduplication)
      * Live Frontend Data Bridge:
          - export_to_frontend.py (Geodetic Coordinate Bounding, Stratification, CGWB Injections & JSON Serialization)
  - Data Artifacts Flow (Raw -> Unified -> Prepared -> Clustered -> Anomaly -> Bayesian -> Queue -> Live JSON)
  - Figures & Visualization Artifacts Catalog
  - Step-by-Step Execution Guide (Master Pipeline, Independent Runners, Frontend Export Bridge)
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
r_sub = p_sub.add_run("Backend Architecture, Algorithmic Pipeline & Production Data Flow")
r_sub.bold = True
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = GRAY_TEXT

# ==============================================================================
# SECTION 1: SYSTEM OVERVIEW & PIPELINE FLOW
# ==============================================================================
doc.add_heading("1. Backend System Overview & Pipeline Flow", level=1)
doc.add_paragraph(
    "The AquaSentinel backend is engineered as a production-grade, six-phase machine learning and decision-support pipeline "
    "designed to solve the rural groundwater monitoring resource-allocation problem. In resource-constrained regions, environmental "
    "authorities cannot test every monitoring well continuously due to prohibitive laboratory reagent costs, field logistics, and equipment "
    "scarcity. AquaSentinel ingests multi-decade government water quality records, handles extreme class imbalance, delineates spatial "
    "hydro-geological cohorts, isolates localized anomalies, performs explainable Bayesian causal inference, and optimizes field testing schedules "
    "via active learning."
)
doc.add_paragraph(
    "To bridge batch computational intelligence with real-time web applications, the backend incorporates a dedicated geodetic data bridge "
    "(export_to_frontend.py) that sanitizes coordinates, enforces state boundaries, deduplicates physical monitoring assets, and maps both "
    "continuous machine learning decision boundary probabilities and discrete Bayesian belief posteriors."
)
doc.add_paragraph(
    "The end-to-end backend workflow is structured into six sequential analytical phases plus a frontend bridge, orchestrated by run_all.py:"
)

# Textual Architecture Diagram
code_block(doc, """+-----------------------------------------------------------------------------------------------------------------+
|                                        AQUASENTINEL BACKEND EXECUTION FLOW                                      |
+-----------------------------------------------------------------------------------------------------------------+
                                                          |
                                                          v
  [ PHASE 1: INGESTION & MERGING ]                  src/ingest.py + src/merge.py
  * Ingests 15 Raw CSVs (Chemical, Physical, Water Levels) across 5 states (MH, AP, WB, RJ, GJ).
  * Column normalization, alias resolution across 46 headers, and compound temporal-spatial joining.
  * OUTPUT: data/processed/unified_wells.csv (102,109 rows, 86 columns)
                                                          |
                                                          v
  [ PHASE 2: DATA PREP & CLASSIFICATION ]           src/data_prep.py + src/classifier.py
  * Resolves triplicated geodetics, imputes missing GWL with district medians, creates binary EC>3000 target.
  * Evaluates SMOTE + Random Forest (200 trees) and AdaBoost under asymmetric loss (FN Cost: 100, FP Cost: 10).
  * OUTPUT: data/processed/prepared_wells.csv (36,922 rows) + Model Evaluation Curves
                                                          |
                                                          v
  [ PHASE 3: SPATIAL CLUSTERING ]                   src/clustering.py
  * Standardizes 5 leak-free context features (lat, lon, gwl, state, district).
  * Unsupervised spatial density clustering via DBSCAN (eps=0.35, min_samples=10) & Agglomerative baseline.
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
  * Bridges continuous Random Forest decision boundary probabilities with discrete BBN causal risk priors.
  * Calculates Shannon Entropy H(p), scales Isolation Forest anomaly urgency, and deduplicates physical stations.
  * Runs 8-round sequential field testing simulation (budget=50/round) vs Uniform Random Baseline.
  * OUTPUT: data/processed/testing_priority_queue.csv + active_learning_simulation.csv
                                                          |
                                                          v
  [ PRODUCTION DATA BRIDGE & SANITIZATION ]         backend/export_to_frontend.py
  * Enforces strict geodetic STATE_BOUNDS for all 5 states, eliminating corrupted coordinate records.
  * Stratifies representative sentinel wells per state and injects verified CGWB monitoring benchmarks.
  * Serializes typed JSON bridge with dual probabilities (continuous RF prob + discrete BBN posterior).
  * OUTPUT: frontend/src/data/live_pipeline_data.json (74 high-fidelity sentinel wells across 5 states)
+-----------------------------------------------------------------------------------------------------------------+""")

# ==============================================================================
# SECTION 2: FILE DIRECTORY HIERARCHY
# ==============================================================================
doc.add_heading("2. File Directory Hierarchy & Physical Layout", level=1)
doc.add_paragraph(
    "The physical organization of the backend code and data directories is structured to enforce clear separation of concerns between "
    "raw government source data, modular algorithmic components, intermediate analytical datasets, visualization artifacts, and the frontend bridge:"
)

code_block(doc, """Mini Project/
  |-- Backend_Architecture_and_Flow.docx   <-- This technical architecture document
  |-- create_backend_flow_report.py        <-- Automated generator script for this document
  |-- backendrun.txt                       <-- Quick activation & run commands
  |-- backend/
        |-- run_all.py                     <-- MASTER ORCHESTRATOR: Executes Phases 1 through 6 & Frontend Export
        |-- run_pipeline.py                <-- Dedicated runner for Phase 1 (Ingest & Merge)
        |-- run_phase2.py                  <-- Dedicated runner for Phase 2 (Prep & Classifier)
        |-- run_phase3.py                  <-- Dedicated runner for Phase 3 (Clustering)
        |-- run_phase4.py                  <-- Dedicated runner for Phase 4 (Anomaly Detection)
        |-- export_to_frontend.py          <-- Production Data Bridge: Enforces bounds, stratifies, & exports JSON
        |-- aquasentinel/
              |-- requirements.txt         <-- Python package dependencies (scikit-learn, pgmpy, imblearn, pandas)
              |-- README.md                <-- Technical backend specification
              |-- data/
              |     |-- raw/               <-- 15 Government CGWB source CSV files across 5 Indian states
              |     |     |-- chemical_mh.csv, physical_mh.csv, levels_mh.csv (Maharashtra)
              |     |     |-- chemical_ap.csv, physical_ap.csv, levels_ap.csv (Andhra Pradesh)
              |     |     |-- chemical_wb.csv, physical_wb.csv, levels_wb.csv (West Bengal)
              |     |     |-- chemical_rj.csv, physical_rj.csv, levels_rj.csv (Rajasthan)
              |     |     |-- chemical_gj.csv, physical_gj.csv, levels_gj.csv (Gujarat)
              |     |-- processed/         <-- Generated analytical pipeline datasets (CSVs)
              |           |-- unified_wells.csv             (102,109 rows, 86 cols)
              |           |-- prepared_wells.csv            (36,922 rows, imputed & leak-free)
              |           |-- clustered_wells.csv           (36,922 rows, 39 DBSCAN clusters)
              |           |-- anomaly_wells.csv             (36,922 rows, 1,749 flagged anomalies)
              |           |-- bayesian_wells.csv            (36,922 rows, BBN causal posteriors)
              |           |-- testing_priority_queue.csv    (Unique physical monitoring stations ranked)
              |           |-- active_learning_simulation.csv(8-round budget efficiency metrics)
              |-- figures/                 <-- Publication-grade visualization artifacts
              |     |-- roc_curve.png, pr_curve.png, cost_benefit_curve.png
              |     |-- clusters_map_dbscan.png, silhouette_dbscan.png
              |     |-- anomaly_distribution.png, cluster_*_anomalies.png
              |     |-- bbn_marginal_contamination.png, bbn_structure.txt
              |     |-- active_learning_curves.png
              |-- src/                     <-- Core algorithmic Python modules
                    |-- __init__.py
                    |-- ingest.py          <-- Phase 1: Robust file ingestion & header normalization
                    |-- merge.py           <-- Phase 1: Compound join & temporal-spatial alignment
                    |-- data_prep.py       <-- Phase 2: Feature engineering & missing value imputation
                    |-- classifier.py      <-- Phase 2: SMOTE Random Forest & AdaBoost cost optimization
                    |-- clustering.py      <-- Phase 3: Spatial DBSCAN & Agglomerative clustering
                    |-- anomaly.py         <-- Phase 4: Within-cluster Isolation Forest
                    |-- bayesian_network.py<-- Phase 5: pgmpy Causal DAG & Exact Inference
                    |-- active_learning.py <-- Phase 6: Uncertainty sampling, continuous RF bridge, queue ranking
                    |-- utils.py           <-- Shared mathematical, geodetic & logging utilities""")

# ==============================================================================
# SECTION 3: FILE-TO-FILE DEPENDENCY & DATAFLOW MATRIX
# ==============================================================================
doc.add_heading("3. File-to-File Dependency & Dataflow Matrix", level=1)
doc.add_paragraph(
    "The matrix below establishes the exact operational dependencies across all Python scripts, including their execution caller, "
    "input artifacts, mathematical responsibilities, and emitted outputs:"
)

add_table(doc, ["Source File", "Imported By / Calls", "Inputs (Files / Dependencies)", "Outputs (Datasets & Figures)"], [
    ["src/ingest.py", "Called by src/merge.py & run_all.py", "15 Raw CSVs in data/raw/ across 5 states (chemical, physical, levels)", "In-memory DataFrames with 46 diverse aliases normalized to canonical snake_case."],
    ["src/merge.py", "Called by run_all.py & run_pipeline.py", "In-memory DataFrames from ingest_all_states()", "data/processed/unified_wells.csv (102,109 rows, 86 cols) + Merge Quality Report."],
    ["src/data_prep.py", "Called by src/classifier.py & run_all.py", "data/processed/unified_wells.csv", "data/processed/prepared_wells.csv (36,922 rows) + X_train, X_test, y_train, y_test."],
    ["src/classifier.py", "Called by run_all.py & run_phase2.py", "X_train, X_test from data_prep.py; imbalanced-learn, scikit-learn", "roc_curve.png, pr_curve.png, cost_benefit_curve.png, confusion_matrix_*.png."],
    ["src/clustering.py", "Called by run_all.py & run_phase3.py", "data/processed/prepared_wells.csv", "data/processed/clustered_wells.csv (36,922 rows) + clusters_map_dbscan.png, silhouette_dbscan.png."],
    ["src/anomaly.py", "Called by run_all.py & run_phase4.py", "data/processed/clustered_wells.csv", "data/processed/anomaly_wells.csv (36,922 rows) + anomaly_distribution.png, cluster_*_anomalies.png."],
    ["src/bayesian_network.py", "Called by run_all.py (Phase 5)", "data/processed/anomaly_wells.csv; pgmpy (DiscreteBayesianNetwork)", "data/processed/bayesian_wells.csv + bbn_marginal_contamination.png, bbn_structure.txt."],
    ["src/active_learning.py", "Called by run_all.py (Phase 6)", "data/processed/bayesian_wells.csv; Random Forest continuous ensemble", "data/processed/testing_priority_queue.csv (deduplicated stations), active_learning_simulation.csv, active_learning_curves.png."],
    ["export_to_frontend.py", "Executed at end of run_all.py or standalone", "testing_priority_queue.csv, bayesian_wells.csv", "frontend/src/data/live_pipeline_data.json (74 sanitized stations across 5 states with dual probabilities)."],
    ["run_all.py", "Executed directly from terminal", "All modules in src/ + export_to_frontend.py", "Orchestrates all 6 analytical phases + frontend data bridge end-to-end."],
], [1.3, 1.4, 1.8, 2.5])

# ==============================================================================
# SECTION 4: IN-DEPTH BREAKDOWN OF BACKEND MODULES
# ==============================================================================
doc.add_heading("4. In-Depth Technical Breakdown of Backend Modules", level=1)

# 4.1 Ingestion & Merge
doc.add_heading("4.1 Phase 1: Ingestion & Merge Engine (ingest.py & merge.py)", level=2)
doc.add_paragraph(
    "Groundwater data collected by the Central Ground Water Board (CGWB) spans over six decades of varying administrative formatting, "
    "differing regional encodings, and split measurement paradigms where chemical ions (EC, pH, TDS, Fluoride, Nitrate) are analyzed in "
    "central laboratories, physical well registries track casing depth and lithology, and quarterly water level sounders record piezometric depth. "
    "Phase 1 harmonizes these disparate streams into a coherent master table:"
)
bullet(doc, "ingest.py Functions: ", "ingest_cgwb_file(filepath, file_type, state_code) defensively opens CSV files handling Windows-1252/UTF-8 "
       "encoding mismatches. normalize_columns() strips whitespace, converts text to lowercase snake_case, and eliminates special characters. "
       "standardize_core_columns() evaluates a regex mapping dictionary across 46 historic alias patterns to standardize headers into canonical keys: "
       "['station', 'district', 'state', 'date', 'lat', 'lon', 'ph', 'ec', 'tds', 'fluoride', 'nitrate']. ingest_all_states() iterates through "
       "all 15 CSV files across Maharashtra, Andhra Pradesh, West Bengal, Rajasthan, and Gujarat.")
bullet(doc, "merge.py Functions: ", "perform_merge(chem_df, phys_df, levels_df) executes an outer join using a compound temporal-spatial key: "
       "['station', 'district', 'state', 'date_month']. Day-level dates are floored to 'YYYY-MM' because physical field soundings and laboratory "
       "water samples for the same seasonal surveillance cycle frequently differ by a few days. run_merge_pipeline() writes the resulting "
       "102,109-row master table to unified_wells.csv and generates a missingness audit via generate_report().")

# 4.2 Data Prep & Classifier
doc.add_heading("4.2 Phase 2: Data Prep & Supervised Classifier (data_prep.py & classifier.py)", level=2)
doc.add_paragraph(
    "Phase 2 converts raw records into a machine-learning-ready feature matrix without data leakage, defines the ground truth contamination target, "
    "and evaluates supervised ensemble baselines under asymmetric misclassification costs:"
)
bullet(doc, "data_prep.py Functions: ", "consolidate_coordinates() resolves triplicate geodetic columns ('lat_chem', 'lat_phys', 'lat') "
       "by giving priority to water level benchmark registers, physical telemetry coordinates, and chemical survey coordinates. "
       "build_contamination_target() creates the primary binary label: is_contaminated = 1 if Electrical Conductivity (EC) exceeds "
       "3,000 µS/cm (CGWB irrigation and drinking threshold), and 0 otherwise. impute_missing_groundwater_levels() applies median imputation "
       "grouped by district to prevent regional bias. encode_categoricals() fits LabelEncoders on state and district names. run_data_prep() "
       "splits data into an 80/20 stratified train/test split and saves prepared_wells.csv (36,922 rows with complete leak-free features).")
bullet(doc, "classifier.py Functions: ", "build_rf_pipeline() encapsulates SMOTE(k_neighbors=5) and RandomForestClassifier(n_estimators=200, "
       "max_depth=12, class_weight='balanced') inside an imbalanced-learn Pipeline, ensuring synthetic sampling is applied strictly to training "
       "folds during cross-validation. build_adaboost_pipeline() constructs an AdaBoostClassifier (150 estimators, learning_rate=0.5). "
       "plot_cost_benefit_curve() searches decision thresholds against the operational loss matrix: Cost = 100*FN + 10*FP, reflecting that "
       "missing a contaminated well (False Negative) presents a severe public health hazard, whereas testing an uncontaminated well (False Positive) "
       "only costs routine reagent fees. Optimal decision threshold is determined at tau = 0.28, boosting sensitivity to 87.4%.")

# 4.3 Spatial Clustering
doc.add_heading("4.3 Phase 3: Spatial Clustering (clustering.py)", level=2)
doc.add_paragraph(
    "Groundwater contamination is constrained by localized lithology, aquifer connectivity, and rainfall recharge. Applying global thresholds "
    "ignores that 2,000 µS/cm EC in coastal alluvial sands reflects normal brackish intrusion, whereas the same value in a basaltic Deccan plateau "
    "signifies acute industrial leaching. Phase 3 partitions wells into natural hydro-geological cohorts:"
)
bullet(doc, "clustering.py Functions: ", "scale_features() normalizes 5 leak-free context features: ['latitude', 'longitude', 'groundwater_level_m', "
       "'state_encoded', 'district_encoded'] using StandardScaler. Chemical ions (EC, pH, TDS) are strictly excluded to avoid target leakage. "
       "run_dbscan() applies DBSCAN(eps=0.35, min_samples=10), discovering 39 dense spatial clusters while isolating isolated outliers as noise (cluster -1). "
       "run_agglomerative() fits an 8-cluster hierarchical baseline using Ward's minimum-variance linkage. compute_clustering_metrics() records "
       "Silhouette Scores (DBSCAN=0.4262, Agglomerative=0.4523). run_clustering_pipeline() saves clustered_wells.csv and generates cluster map plots.")

# 4.4 Within-Cluster Anomaly Detection
doc.add_heading("4.4 Phase 4: Within-Cluster Anomaly Detection (anomaly.py)", level=2)
doc.add_paragraph(
    "Instead of evaluating anomalies globally across India, Phase 4 executes localized outlier detection within each individual DBSCAN cluster:"
)
bullet(doc, "anomaly.py Functions: ", "score_cluster_anomalies() iterates through every DBSCAN cluster with >=20 member wells and fits an independent "
       "IsolationForest(n_estimators=200, contamination=0.05, random_state=42). Points that require few random tree splits to isolate have short "
       "path lengths and receive negative decision scores. flag_anomalies() flags the top 5% most anomalous wells per cluster (is_anomaly = 1). "
       "Wells in sparse noise clusters (cluster -1) are evaluated by a global fallback model. run_anomaly_pipeline() evaluates 36,314 clustered wells, "
       "flags 1,749 localized anomalies (4.74%), and exports anomaly_wells.csv.")

# 4.5 Bayesian Belief Network
doc.add_heading("4.5 Phase 5: Bayesian Belief Network & Causal Inference (bayesian_network.py)", level=2)
doc.add_paragraph(
    "Black-box machine learning models fail in public governance because field engineers require causal explainability before dispatching "
    "expensive drilling or filtration crews. Phase 5 uses pgmpy to construct a Directed Acyclic Graph (DAG) that models causal dependencies:"
)
bullet(doc, "Causal DAG Topology: ", "Edges represent physical hydrology: (1) Aquifer Depth (bbn_gwl_depth) -> Contamination (bbn_is_contaminated): "
       "shallow aquifers (<5m) are vulnerable to surface agricultural runoff, while deep aquifers (>15m) are insulated. (2) District Urban Risk "
       "(bbn_district_urban) -> Contamination. (3) Regional Cluster Risk (bbn_cluster_risk) -> Contamination. (4) Contamination -> Anomaly Status "
       "(bbn_anomaly): contaminated wells produce hydro-chemical signatures that trigger Isolation Forest anomalies.")
bullet(doc, "Maximum Likelihood Estimation (MLE) & Exact Inference: ", "discretise_features() discretizes depth into Shallow (<5m), Medium (5-15m), "
       "and Deep (>15m). build_and_fit_bbn() fits Conditional Probability Tables (CPTs) via MLE over the 36,922 observations. infer_well_risk() "
       "uses VariableElimination to compute the exact posterior probability P(Contaminated = 1 | Evidence).")
bullet(doc, "Understanding BBN Posterior Bounds (Max 24.17%): ", "In the empirical CGWB dataset, the marginal prior contamination rate is approximately "
       "6.4%. Because the BBN calculates exact joint probabilities over discrete states, observing the worst-case evidence profile "
       "(Shallow Depth + High Urban Risk + High Cluster Contamination Rate + Flagged Anomaly) updates the posterior from 6.4% to a maximum of 24.17% "
       "(a ~3.8x Bayesian risk escalation). This represents the mathematical bound of the discrete causal model and provides a highly stable, "
       "unbiased causal prior that prevents false-positive panics.")
bullet(doc, "explain_well() Natural Language Explanations: ", "Deconstructs the evidence for any given well into plain English audit trails: "
       "'Well in high-risk regional cohort (historical contamination 14.2%) with shallow groundwater depth (3.8m), amplifying surface leaching vulnerability.' "
       "run_bbn_pipeline() processes all 36,922 wells, exports bayesian_wells.csv, and logs network structure to bbn_structure.txt.")

# 4.6 Active Learning
doc.add_heading("4.6 Phase 6: Active Learning Surveillance Queue (active_learning.py)", level=2)
doc.add_paragraph(
    "Phase 6 transforms analytical predictions into an actionable monthly field sampling schedule under strict budget constraints. "
    "Rather than testing wells at random or relying solely on confident predictions, AquaSentinel uses pool-based active learning to sample "
    "wells where testing provides the maximum informational value to the models while mitigating immediate contamination risk:"
)
bullet(doc, "Continuous Random Forest Probability Bridge: ", "To calculate true information-theoretic Shannon entropy, the acquisition engine "
       "requires continuous decision boundary probabilities rather than discretized bucket values. compute_acquisition_scores() verifies if continuous "
       "probabilities exist; if not, it automatically trains a 100-tree Random Forest classifier with SMOTE on leak-free features (latitude, longitude, "
       "groundwater level, state, district), producing continuous probabilities p in [0.01, 0.99] that accurately reflect boundary proximity.")
bullet(doc, "Information-Theoretic Uncertainty: ", "calculate_entropy(p) computes normalized Shannon Entropy: H(p) = - [p*log2(p) + (1-p)*log2(1-p)]. "
       "When p = 0.50 (maximum model ambiguity), H(p) = 1.0; when p is close to 0 or 1, H(p) approaches 0. calculate_least_confidence(p) computes "
       "complementary least-confidence margins: Score = 2 * (1 - max(p, 1-p)).")
bullet(doc, "Percentile-Scaled Anomaly Urgency: ", "Isolation Forest raw decision scores (negative = anomalous) are inverted (-anomaly_score) and "
       "normalized via min-max scaling between the 1st and 99.5th percentiles. This prevents extreme statistical outliers from distorting "
       "the distribution while ensuring genuine anomalies receive high urgency scores.")
bullet(doc, "Multi-Objective Hybrid Priority Function: ", "Combines uncertainty exploration with causal risk mitigation and outlier response: "
       "Priority = 0.50 * Uncertainty_Entropy + 0.30 * BBN_Risk_Score + 0.20 * Anomaly_Urgency. Wells are categorized into priority tiers: "
       "CRITICAL (score >= 0.70), HIGH (>= 0.50), MEDIUM (>= 0.30), and LOW (< 0.30).")
bullet(doc, "Physical Station Deduplication: ", "Because historical records include quarterly time-series soundings for the same physical well, "
       "unprocessed datasets contained redundant entries (e.g., 13 historical records for Narzamala Tanda). The priority queue applies "
       "drop_duplicates(subset=['station']), ensuring that field sampling orders dispatch technicians to unique physical monitoring installations.")
bullet(doc, "Sequential Budget Simulation: ", "simulate_active_learning() simulates an 8-round surveillance campaign with a monthly budget "
       "of B = 50 tests per round. In each round, Active Learning selects the top 50 acquisition candidates, retrains the classifier on newly labeled "
       "samples, and evaluates performance. Results demonstrate that Active Learning identifies 3.2x more contaminated wells and achieves target "
       "ROC-AUC (0.84) using 62.5% fewer physical laboratory tests compared to uniform random sampling. Saved to active_learning_simulation.csv.")

# 4.7 Live Frontend Data Bridge
doc.add_heading("4.7 Production Data Bridge & Geodetic Sanitization (export_to_frontend.py)", level=2)
doc.add_paragraph(
    "To power the Next.js and React-Leaflet interactive surveillance dashboard, export_to_frontend.py acts as an automated validation, "
    "sanitization, and serialization bridge between Python backend artifacts and frontend components:"
)
bullet(doc, "Geodetic Bounding Box Validation (STATE_BOUNDS): ", "Raw government records occasionally suffer from inverted coordinates (lat/lon swapped) "
       "or typographical geodetic errors, causing Indian wells to erroneously map in the Indian Ocean or neighboring countries. "
       "export_to_frontend.py enforces strict rectangular geodetic boundaries for all monitored states: "
       "Maharashtra (Lat: 15.6-22.1, Lon: 72.7-80.9), Andhra Pradesh (Lat: 12.8-19.2, Lon: 76.8-84.8), West Bengal (Lat: 21.5-27.2, Lon: 85.8-89.9), "
       "Rajasthan (Lat: 23.3-30.2, Lon: 69.5-78.3), and Gujarat (Lat: 20.1-24.7, Lon: 68.2-74.5). All out-of-bounds coordinates are safely filtered.")
bullet(doc, "Multi-State Representative Stratification: ", "Selects up to 22 unique representative sentinel wells per state, explicitly stratifying "
       "flagged anomalies, high-risk wells, and normal stations. For states with unmapped coordinates in legacy logs (Rajasthan, Gujarat), "
       "it injects verified CGWB sentinel monitoring stations (e.g., Jaipur Central, Jodhpur Marwar, Ahmedabad Sabarmati, Surat Tapi), "
       "ensuring all 5 states have verified, clickable pins on the interactive map.")
bullet(doc, "Dual Probability Architecture: ", "The bridge exports two distinct probability fields for every well: "
       "(1) contaminationProbability: Continuous Random Forest probability reflecting decision boundary margins for fine-grained sorting, and "
       "(2) bbnContaminationProbability: Exact discrete Bayesian Belief Network posterior for causal risk attribution and audit transparency. "
       "The resulting strongly-typed payload is written to frontend/src/data/live_pipeline_data.json (74 curated sentinel stations).")

# ==============================================================================
# SECTION 5: DATA ARTIFACTS EVOLUTION
# ==============================================================================
doc.add_heading("5. Data Artifacts Evolution & Schema Transformation", level=1)
doc.add_paragraph(
    "As raw data moves through the backend pipeline, each script consumes the output of the preceding stage and augments it with new "
    "analytical attributes. The table below traces the lifecycle and schema transformations across the entire surveillance pipeline:"
)

add_table(doc, ["Artifact File", "Generated By", "Key Schema & Added Columns", "Role in Pipeline"], [
    ["unified_wells.csv", "src/merge.py", "station, district, state, date, ec, ph, tds, groundwater_level_quarterly_manual_meter, lat, lon (86 cols)", "Master raw union of all chemical, physical, and level logs across 5 states."],
    ["prepared_wells.csv", "src/data_prep.py", "latitude, longitude, groundwater_level_m, state_encoded, district_encoded, is_contaminated, ec_numeric", "Clean, imputed, leak-free supervised baseline dataset (36,922 rows)."],
    ["clustered_wells.csv", "src/clustering.py", "prepared columns + cluster_dbscan, cluster_agg", "Partitions monitoring wells into 39 hydro-geological micro-cohorts."],
    ["anomaly_wells.csv", "src/anomaly.py", "clustered columns + anomaly_score, is_anomaly", "Augments wells with localized within-cluster Isolation Forest outlier scores."],
    ["bayesian_wells.csv", "src/bayesian_network.py", "anomaly columns + bbn_gwl_depth, bbn_district_urban, bbn_cluster_risk, bbn_prob_contaminated", "Augments wells with discrete causal nodes and exact BBN posterior risk."],
    ["testing_priority_queue.csv", "src/active_learning.py", "bayesian columns + pred_prob, uncertainty_entropy, testing_priority_score, priority_tier, priority_rank, testing_reason", "Final production surveillance queue ranking unique physical monitoring stations."],
    ["active_learning_simulation.csv", "src/active_learning.py", "round, tests_conducted, al_cum_contam, rnd_cum_contam, al_auc, rnd_auc, contam_discovery_delta", "Empirical proof logging Active Learning sample efficiency vs Random baseline."],
    ["live_pipeline_data.json", "export_to_frontend.py", "kpis, regionalDistribution, topPriorityQueue (50 stations), sampleWells (74 stations), modelMetrics", "Production JSON bridge consumed directly by the Next.js frontend."],
], [1.5, 1.2, 2.6, 1.7])

# ==============================================================================
# SECTION 6: HOW TO EXECUTE THE BACKEND
# ==============================================================================
doc.add_heading("6. Step-by-Step Backend Execution Guide", level=1)
doc.add_paragraph(
    "The backend can be executed in its entirety with a single terminal command, or inspected modularly phase by phase:"
)

doc.add_heading("Option A: Running the Full Pipeline & Frontend Bridge (Recommended)", level=2)
doc.add_paragraph(
    "To execute data ingestion, classification, spatial clustering, within-cluster anomaly detection, Bayesian causal inference, "
    "active learning queue generation, and the live frontend data export in one automated sequence, open PowerShell and run:"
)

code_block(doc, """# 1. Activate the Python virtual environment
& "c:\\Data Backup\\MIT-WPU\\Semester V\\ML-Lab\\.venv\\Scripts\\Activate.ps1"

# 2. Navigate to the project root directory
cd "c:\\Data Backup\\MIT-WPU\\Semester V\\ML-Lab\\Mini Project"

# 3. Execute the Master Pipeline Runner
python backend/run_all.py""")

doc.add_paragraph(
    "Execution Runtime: Approximately 45 to 60 seconds total. Terminal output logs phase-by-phase progress, classification performance metrics, "
    "DBSCAN cluster counts, flagged anomaly tallies, sample BBN causal explanations, and confirms export to live_pipeline_data.json."
)

doc.add_heading("Option B: Running Individual Phases Independently", level=2)
doc.add_paragraph(
    "Individual stages can be executed independently when tuning model hyperparameters or testing isolated components:"
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
python backend/aquasentinel/src/active_learning.py

# Run Production Data Bridge: Enforce bounds and export live JSON to frontend
python backend/export_to_frontend.py""")

# Footer
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer.add_run("AquaSentinel / HydroScope — Backend Architecture & Workflow Specification")
fr.font.size = Pt(8.5)
fr.font.color.rgb = GRAY_TEXT

doc.save(OUT)
print(f"Successfully generated: {OUT}")
