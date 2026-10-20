"""
anomaly.py — AquaSentinel Within-Cluster Anomaly Detection Module
==================================================================
Flags wells that deviate significantly from their cluster's norm using
Isolation Forest — an ensemble of random trees that isolates anomalies
(rare, extreme observations) faster than normal points.

Key design choice: anomaly detection runs **within each cluster separately**,
not on the global dataset. This means a well is flagged as anomalous relative
to its regional hydro-geological peers, not against the entire country.
A well in Rajasthan with a high groundwater level is only unusual compared
to other Rajasthan cluster members, not Maharashtra coastal wells.

Features used:
  - latitude, longitude          — spatial position within cluster
  - groundwater_level_m          — depth to water table
  - state_encoded, district_encoded — regional context

Outputs:
  - anomaly_score column: raw Isolation Forest decision score
    (more negative = more anomalous)
  - is_anomaly column: 1 if flagged, 0 if normal
  - anomalied_wells.csv saved to data/processed/
  - Figures: per-cluster anomaly maps + global anomaly score distribution
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

matplotlib.use("Agg")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    "random_seed": 42,
    "figures_dir": "figures",
    # Isolation Forest
    "if_contamination": 0.05,   # expected fraction of anomalies per cluster (~5%)
    "if_n_estimators": 200,
    # Use DBSCAN cluster labels by default (more granular than agglomerative)
    "cluster_col": "cluster_dbscan",
    # Minimum cluster size to run anomaly detection (skip tiny clusters)
    "min_cluster_size": 20,
    # Features for anomaly scoring (must match clustering features)
    "anomaly_features": [
        "latitude",
        "longitude",
        "groundwater_level_m",
        "state_encoded",
        "district_encoded",
    ],
}
# ──────────────────────────────────────────────────────────────────────────────


def load_clustered(processed_dir: str) -> pd.DataFrame:
    """
    Loads the clustered_wells.csv produced by clustering.py.

    Args:
        processed_dir: Path to `data/processed/`.

    Returns:
        DataFrame with cluster labels.
    """
    path = os.path.join(processed_dir, "clustered_wells.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"clustered_wells.csv not found at {path}. Run clustering.py first."
        )
    df = pd.read_csv(path, low_memory=False)
    logging.info(f"Loaded clustered_wells.csv: {df.shape[0]} rows.")
    return df


def run_isolation_forest_per_cluster(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs Isolation Forest independently within each DBSCAN cluster.
    Wells in noise clusters (-1) or too-small clusters get anomaly_score=NaN.

    Args:
        df: DataFrame with cluster labels and feature columns.

    Returns:
        DataFrame with `anomaly_score` and `is_anomaly` columns added.
    """
    feature_cols = CONFIG["anomaly_features"]
    cluster_col = CONFIG["cluster_col"]
    min_size = CONFIG["min_cluster_size"]

    df["anomaly_score"] = np.nan
    df["is_anomaly"] = 0

    cluster_ids = sorted(df[cluster_col].unique())
    valid_clusters = [c for c in cluster_ids if c >= 0]  # exclude noise (-1) and uneval (-2)

    processed_count = 0
    skipped_count = 0

    for cluster_id in valid_clusters:
        mask = df[cluster_col] == cluster_id
        cluster_df = df.loc[mask, feature_cols].dropna()

        if len(cluster_df) < min_size:
            skipped_count += 1
            continue

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(cluster_df.values)

        iso = IsolationForest(
            n_estimators=CONFIG["if_n_estimators"],
            contamination=CONFIG["if_contamination"],
            random_state=CONFIG["random_seed"],
            n_jobs=-1,
        )
        iso.fit(X_scaled)

        scores = iso.decision_function(X_scaled)    # lower = more anomalous
        predictions = iso.predict(X_scaled)          # -1 = anomaly, 1 = normal

        df.loc[cluster_df.index, "anomaly_score"] = scores
        df.loc[cluster_df.index, "is_anomaly"] = (predictions == -1).astype(int)
        processed_count += 1

    n_anomalies = df["is_anomaly"].sum()
    n_scored = df["anomaly_score"].notna().sum()
    logging.info(
        f"Isolation Forest: {processed_count} clusters processed, "
        f"{skipped_count} skipped (< {min_size} wells). "
        f"{n_anomalies} anomalies flagged out of {n_scored} scored wells "
        f"({n_anomalies/n_scored:.1%})."
    )
    return df


def plot_anomaly_score_distribution(df: pd.DataFrame, figures_dir: str) -> None:
    """
    Plots the distribution of Isolation Forest anomaly scores, with
    anomalous wells highlighted in red.

    Args:
        df:          DataFrame with `anomaly_score` and `is_anomaly`.
        figures_dir: Output directory.
    """
    scored = df.dropna(subset=["anomaly_score"])
    normal = scored[scored["is_anomaly"] == 0]["anomaly_score"]
    anomaly = scored[scored["is_anomaly"] == 1]["anomaly_score"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(normal, bins=60, color="#2196F3", alpha=0.7, label=f"Normal ({len(normal):,})")
    ax.hist(anomaly, bins=60, color="#FF5722", alpha=0.8, label=f"Anomaly ({len(anomaly):,})")
    ax.axvline(0, color="black", ls="--", lw=1.2, label="Decision boundary")
    ax.set_xlabel("Isolation Forest Decision Score  (lower = more anomalous)")
    ax.set_ylabel("Number of Wells")
    ax.set_title("Anomaly Score Distribution — Within-Cluster Isolation Forest")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(figures_dir, "anomaly_score_distribution.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved anomaly score distribution to {path}")


def plot_anomaly_map(df: pd.DataFrame, figures_dir: str) -> None:
    """
    Plots all scored wells on a lat/lon scatter; anomalous wells shown
    larger and in red to make them visually salient.

    Args:
        df:          DataFrame with latitude, longitude, is_anomaly.
        figures_dir: Output directory.
    """
    scored = df.dropna(subset=["anomaly_score"])
    normal = scored[scored["is_anomaly"] == 0]
    anomalous = scored[scored["is_anomaly"] == 1]

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.scatter(normal["longitude"], normal["latitude"],
               s=8, c="#90CAF9", alpha=0.4, label=f"Normal ({len(normal):,})")
    ax.scatter(anomalous["longitude"], anomalous["latitude"],
               s=40, c="#FF5722", alpha=0.85, marker="^",
               label=f"Anomalous ({len(anomalous):,})", zorder=5)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Anomalous Wells Map\n(red triangles = flagged by Isolation Forest within their cluster)")
    ax.legend(markerscale=1.5)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(figures_dir, "anomaly_map.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved anomaly map to {path}")


def plot_anomaly_vs_contamination(df: pd.DataFrame, figures_dir: str) -> None:
    """
    Cross-tabulation heatmap: anomaly flag vs. contamination label.
    Ideally anomalous wells should have higher contamination rates.

    Args:
        df:          DataFrame with `is_anomaly` and `is_contaminated`.
        figures_dir: Output directory.
    """
    scored = df.dropna(subset=["anomaly_score"])
    ct = pd.crosstab(
        scored["is_anomaly"].map({0: "Normal", 1: "Anomalous"}),
        scored["is_contaminated"].map({0: "Clean", 1: "Contaminated"}),
        normalize="index",
    ) * 100

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(ct, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax,
                cbar_kws={"label": "% within row"})
    ax.set_title("Anomaly vs. Contamination\n(% within Anomaly/Normal group)")
    ax.set_ylabel("Anomaly Flag")
    ax.set_xlabel("Contamination Label")
    fig.tight_layout()

    path = os.path.join(figures_dir, "anomaly_vs_contamination.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved anomaly vs contamination heatmap to {path}")


def anomaly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prints a top-20 most anomalous wells table for viva presentation.

    Args:
        df: DataFrame with anomaly scores.

    Returns:
        Top-20 anomalous wells DataFrame.
    """
    cols = ["station", "state", "district", "latitude", "longitude",
            "groundwater_level_m", "cluster_dbscan", "anomaly_score",
            "is_anomaly", "is_contaminated"]
    available = [c for c in cols if c in df.columns]
    top = (
        df[df["is_anomaly"] == 1]
        .sort_values("anomaly_score")   # most anomalous first
        [available]
        .head(20)
    )
    logging.info(f"\n=== Top 20 Most Anomalous Wells ===\n{top.to_string(index=False)}")
    return top


def run_anomaly_pipeline(
    processed_dir: str,
    figures_dir: str = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Full anomaly detection pipeline.

    Args:
        processed_dir: Path to `data/processed/`.
        figures_dir:   Output directory for figures.

    Returns:
        Tuple of (full annotated DataFrame, top-20 anomalous wells DataFrame).
    """
    figures_dir = figures_dir or CONFIG["figures_dir"]
    os.makedirs(figures_dir, exist_ok=True)

    df = load_clustered(processed_dir)
    df = run_isolation_forest_per_cluster(df)

    plot_anomaly_score_distribution(df, figures_dir)
    plot_anomaly_map(df, figures_dir)
    plot_anomaly_vs_contamination(df, figures_dir)
    top_anomalies = anomaly_summary(df)

    # Save annotated dataset for downstream modules (BBN, active learning)
    out_path = os.path.join(processed_dir, "anomaly_wells.csv")
    df.to_csv(out_path, index=False)
    logging.info(f"Saved anomaly-annotated dataset to {out_path}")

    return df, top_anomalies
