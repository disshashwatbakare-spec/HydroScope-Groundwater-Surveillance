import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AQUASENTINEL_DIR = os.path.join(SCRIPT_DIR, 'aquasentinel')
sys.path.insert(0, AQUASENTINEL_DIR)

from src.ingest import ingest_all_states
from src.merge import run_merge_pipeline, generate_report

DATA_DIR = os.path.join(AQUASENTINEL_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(AQUASENTINEL_DIR, 'data', 'processed')
STATES = ['mh', 'rj', 'ap', 'wb', 'gj']

print("Starting Ingestion...")
chemical_df = ingest_all_states(DATA_DIR, 'chemical', STATES)
physical_df = ingest_all_states(DATA_DIR, 'physical', STATES)
levels_df = ingest_all_states(DATA_DIR, 'levels', STATES)

print(f"Chemical shape: {chemical_df.shape}")
print(f"Physical shape: {physical_df.shape}")
print(f"Levels shape: {levels_df.shape}")

print("Starting Merge Pipeline...")
unified_df, metrics = run_merge_pipeline(PROCESSED_DIR, chemical_df, physical_df, levels_df)

generate_report(metrics)
