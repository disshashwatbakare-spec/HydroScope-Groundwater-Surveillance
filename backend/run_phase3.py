"""CLI runner for Phase 3: Spatial Clustering."""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AQUASENTINEL_DIR = os.path.join(SCRIPT_DIR, 'aquasentinel')
sys.path.insert(0, AQUASENTINEL_DIR)

from src.clustering import run_clustering_pipeline

PROCESSED_DIR = os.path.join(AQUASENTINEL_DIR, 'data', 'processed')
FIGURES_DIR   = os.path.join(AQUASENTINEL_DIR, 'figures')

print("\n=== PHASE 3: Spatial Clustering ===")
df_clustered, metrics = run_clustering_pipeline(PROCESSED_DIR, figures_dir=FIGURES_DIR)

print("\n=== Clustering Quality Metrics ===")
for k, v in metrics.items():
    if isinstance(v, float):
        print(f"  {k:<30s}: {v:.4f}")
    else:
        print(f"  {k:<30s}: {v}")

print(f"\nFigures saved to: {FIGURES_DIR}/")
