# AquaSentinel

AquaSentinel is a Bayesian and Active-Learning Framework for Rural Groundwater Contamination Early-Warning.

## Project Overview

Rural groundwater sources are rarely lab-tested for contamination (fluoride, nitrate, salinity, bacterial) because testing is expensive and slow. This project is framed as a **resource-allocation** system: given a fixed, small testing budget, which wells should be tested next, and how confident can we be about the rest? 

AquaSentinel integrates multiple techniques into a cohesive pipeline:
- **Data Preparation & Ingestion:** Loading real-world groundwater quality, physical, and level data from the CGWB (Central Ground Water Board).
- **Classification & Imbalance Handling:** Using ensemble methods (Random Forest / AdaBoost) and SMOTE to handle the rarity of contamination.
- **Clustering & Anomaly Detection:** Grouping wells by hydro-geological similarity (DBSCAN/Hierarchical) and flagging anomalies (Isolation Forest).
- **Bayesian Belief Networks:** Encoding plausible causal structures (e.g., `aquifer_material -> fluoride_risk`) using `pgmpy` to produce human-readable probability explanations.
- **Active Learning (The Core):** Using uncertainty sampling to simulate a monthly testing budget and select the most informative wells to test next, comparing the results against a random sampling baseline.

## Data Sourcing

The primary data comes from the **National Water Data Portal** (CGWB manual readings from 1961-2025) across 5 diverse states: Maharashtra, Rajasthan, Andhra Pradesh, West Bengal, and Gujarat. 

Required files in `data/raw/` (3 per state, 15 total):
- `chemical_<state>.csv`
- `physical_<state>.csv`
- `levels_<state>.csv`

## Setup Instructions

1. Ensure Python 3.11+ is installed.
2. Clone this repository.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place the required 15 CGWB CSV files into `data/raw/` following the naming convention mentioned above.
5. Run the notebooks in the `notebooks/` directory sequentially, starting with `00_ingest_and_merge.ipynb`.
