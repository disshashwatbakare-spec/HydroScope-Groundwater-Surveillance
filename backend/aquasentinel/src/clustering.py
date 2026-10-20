"""
clustering.py — AquaSentinel Spatial Clustering Module
========================================================
Groups wells by hydro-geological and spatial similarity using:

  1. DBSCAN (primary) — density-based, no need to pre-specify k,
     naturally handles noise/outlier wells as their own "cluster"
  2. Agglomerative Hierarchical Clustering (secondary) — for comparison
     and dendrogram visualisation

Features used for clustering (geospatial + hydrological, no leakage):
  - latitude, longitude         — spatial position
  - groundwater_level_m         — depth to water table
  - state_encoded, district_encoded — regional context

Cluster quality is assessed via Silhouette Score.
Cluster labels are written back to the DataFrame and saved for use
by the anomaly detection module downstream.

All plots are saved to the /figures directory.
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.cluster.hierarchy import dendrogram, linkage

matplotlib.use("Agg")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    "random_seed": 42,
    "figures_dir": "figures",
    # DBSCAN — tune eps (neighbourhood radius in scaled units) and min_samples
    # eps ~0.3 works well for scaled geo+hydro features; increase if too many noise points
    "dbscan_eps": 0.35,
    "dbscan_min_samples": 10,
    # Agglomerative — number of clusters for comparison
    "agg_n_clusters": 8,
    # Features to cluster on
    "cluster_features": [
        "latitude",
        "longitude",
        "groundwater_level_m",
        "state_encoded",
        "district_encoded",
    ],
}
# ──────────────────────────────────────────────────────────────────────────────


def load_prepared(processed_dir: str) -> pd.DataFrame:
    """
    Loads the prepared_wells.csv output of data_prep.py.

    Args:
        processed_dir: Path to the `data/processed/` directory.

    Returns:
        DataFrame ready for clustering.
    """
    path = os.path.join(processed_dir, "prepared_wells.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"prepared_wells.csv not found at {path}. Run data_prep.py first."
        )
    df = pd.read_csv(path, low_memory=False)
    logging.info(f"Loaded prepared_wells.csv: {df.shape[0]} rows.")
    return df


def scale_features(df: pd.DataFrame, feature_cols: list) -> tuple[np.ndarray, StandardScaler, pd.Index]:
    """
    Drops rows with missing cluster features, then standardises the feature
    matrix (zero mean, unit variance). Returns the valid row index so results
    can be merged back into the full DataFrame.

    Args:
        df:           DataFrame containing feature columns.
        feature_cols: List of column names to use.

    Returns:
        Tuple of (scaled numpy array, fitted StandardScaler, valid row Index).
    """
    df_clean = df[feature_cols].dropna()
    dropped = len(df) - len(df_clean)
    if dropped:
        logging.warning(f"Dropped {dropped} rows with NaN in clustering features.")
    X = df_clean.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    logging.info(f"Scaled {len(feature_cols)} features for {len(X)} wells.")
    return X_scaled, scaler, df_clean.index


def run_dbscan(X_scaled: np.ndarray) -> np.ndarray:
    """
    Runs DBSCAN on the scaled feature matrix.
    Label -1 means the point is a noise/outlier well (not assigned to any cluster).

    Args:
        X_scaled: Scaled feature matrix.

    Returns:
        Array of cluster labels (int), -1 for noise points.
    """
    db = DBSCAN(
        eps=CONFIG["dbscan_eps"],
        min_samples=CONFIG["dbscan_min_samples"],
        n_jobs=-1,
    )
    labels = db.fit_predict(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    logging.info(
        f"DBSCAN: {n_clusters} clusters found | {n_noise} noise points "
        f"({n_noise / len(labels):.1%} of wells)"
    )
    return labels


def run_agglomerative(X_scaled: np.ndarray, n_clusters: int) -> np.ndarray:
    """
    Runs Agglomerative (Ward linkage) Hierarchical Clustering.

    Args:
        X_scaled:   Scaled feature matrix.
        n_clusters: Target number of clusters.

    Returns:
        Array of cluster labels.
    """
    agg = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    labels = agg.fit_predict(X_scaled)
    logging.info(f"Agglomerative: {n_clusters} clusters assigned.")
    return labels


def compute_silhouette(X_scaled: np.ndarray, labels: np.ndarray, method: str) -> float:
    """
    Computes the overall Silhouette Score, excluding noise points (label == -1).

    Args:
        X_scaled: Scaled feature matrix.
        labels:   Cluster label array.
        method:   Name of the clustering method (for logging).

    Returns:
        Silhouette score (−1 to +1; higher is better, >0.5 is strong).
    """
    mask = labels != -1
    if mask.sum() < 2 or len(set(labels[mask])) < 2:
        logging.warning(f"{method}: Not enough clusters to compute silhouette score.")
        return float("nan")
    score = silhouette_score(X_scaled[mask], labels[mask], sample_size=5000,
                             random_state=CONFIG["random_seed"])
    logging.info(f"{method} Silhouette Score: {score:.4f}")
    return score


def plot_clusters_map(
    df: pd.DataFrame,
    labels: np.ndarray,
    method: str,
    figures_dir: str,
) -> None:
    """
    Plots wells on a lat/lon scatter coloured by cluster assignment.
    Noise points (DBSCAN label -1) are plotted in grey.

    Args:
        df:          DataFrame with `latitude` and `longitude`.
        labels:      Cluster label array.
        method:      Clustering method name (for title and filename).
        figures_dir: Output directory.
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    unique_labels = sorted(set(labels))
    palette = plt.cm.tab20.colors

    for i, label in enumerate(unique_labels):
        mask = labels == label
        color = "lightgrey" if label == -1 else palette[i % len(palette)]
        marker = "x" if label == -1 else "o"
        size = 10 if label == -1 else 20
        cluster_name = "Noise" if label == -1 else f"Cluster {label}"
        ax.scatter(
            df.loc[mask, "longitude"],
            df.loc[mask, "latitude"],
            c=[color], s=size, marker=marker,
            label=cluster_name, alpha=0.6, linewidths=0.3,
        )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"Well Clusters — {method}\n(coloured by cluster; grey = noise/unassigned)")
    if len(unique_labels) <= 15:
        ax.legend(loc="upper right", fontsize=7, markerscale=1.5)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    fname = f"clusters_map_{method.lower().replace(' ', '_')}.png"
    path = os.path.join(figures_dir, fname)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved cluster map to {path}")


def plot_silhouette_samples_chart(
    X_scaled: np.ndarray,
    labels: np.ndarray,
    overall_score: float,
    method: str,
    figures_dir: str,
) -> None:
    """
    Plots per-sample silhouette coefficients grouped by cluster — a much richer
    diagnostic than the single aggregate score.

    Args:
        X_scaled:      Scaled feature matrix.
        labels:        Cluster label array.
        overall_score: Pre-computed overall silhouette score.
        method:        Method name for title/filename.
        figures_dir:   Output directory.
    """
    mask = labels != -1
    X_clean = X_scaled[mask]
    labels_clean = labels[mask]

    if len(set(labels_clean)) < 2:
        return

    sample_silhouette = silhouette_samples(X_clean, labels_clean)
    unique_labels = sorted(set(labels_clean))
    n_clusters = len(unique_labels)

    fig, ax = plt.subplots(figsize=(10, max(5, n_clusters * 0.8)))
    y_lower = 10
    palette = plt.cm.tab20.colors

    for i, label in enumerate(unique_labels):
        cluster_vals = sample_silhouette[labels_clean == label]
        cluster_vals.sort()
        size = len(cluster_vals)
        y_upper = y_lower + size
        color = palette[i % len(palette)]
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_vals,
                         facecolor=color, edgecolor=color, alpha=0.7)
        ax.text(-0.05, y_lower + 0.5 * size, str(label), fontsize=7)
        y_lower = y_upper + 10

    ax.axvline(x=overall_score, color="red", linestyle="--",
               label=f"Mean = {overall_score:.3f}")
    ax.set_xlabel("Silhouette Coefficient")
    ax.set_ylabel("Cluster")
    ax.set_title(f"Silhouette Plot — {method}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    fname = f"silhouette_{method.lower().replace(' ', '_')}.png"
    path = os.path.join(figures_dir, fname)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved silhouette plot to {path}")


def plot_dendrogram(X_scaled: np.ndarray, figures_dir: str, max_samples: int = 500) -> None:
    """
    Plots a truncated dendrogram for the hierarchical clustering.
    Sub-sampled to max_samples for performance.

    Args:
        X_scaled:    Scaled feature matrix.
        figures_dir: Output directory.
        max_samples: Maximum number of points to include (sub-sampled randomly).
    """
    rng = np.random.default_rng(CONFIG["random_seed"])
    if len(X_scaled) > max_samples:
        idx = rng.choice(len(X_scaled), max_samples, replace=False)
        X_sub = X_scaled[idx]
    else:
        X_sub = X_scaled

    Z = linkage(X_sub, method="ward")

    fig, ax = plt.subplots(figsize=(14, 5))
    dendrogram(Z, ax=ax, truncate_mode="lastp", p=30,
               leaf_rotation=45, leaf_font_size=8, show_contracted=True)
    ax.set_title(f"Hierarchical Clustering Dendrogram (sub-sample of {len(X_sub)} wells)")
    ax.set_xlabel("Cluster / Well")
    ax.set_ylabel("Ward Linkage Distance")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()

    path = os.path.join(figures_dir, "dendrogram_hierarchical.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved dendrogram to {path}")


def cluster_summary(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """
    Generates a per-cluster summary table: size, contamination rate,
    mean coordinates and groundwater level.

    Args:
        df:         DataFrame with cluster label column and `is_contaminated`.
        label_col:  Name of the cluster label column.

    Returns:
        Summary DataFrame.
    """
    agg = (
        df[df[label_col] != -1]
        .groupby(label_col)
        .agg(
            count=(label_col, "count"),
            contamination_rate=("is_contaminated", "mean"),
            mean_lat=("latitude", "mean"),
            mean_lon=("longitude", "mean"),
            mean_gwl=("groundwater_level_m", "mean"),
        )
        .reset_index()
        .sort_values("contamination_rate", ascending=False)
    )
    agg["contamination_rate"] = agg["contamination_rate"].map("{:.2%}".format)
    logging.info(f"\n{agg.to_string(index=False)}")
    return agg


def run_clustering_pipeline(
    processed_dir: str,
    figures_dir: str = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Full clustering pipeline. Runs DBSCAN and Agglomerative, evaluates
    both with Silhouette Score, saves all figures, and returns the
    annotated DataFrame plus quality metrics.

    Args:
        processed_dir: Path to `data/processed/`.
        figures_dir:   Output directory for figures.

    Returns:
        Tuple of (annotated DataFrame, metrics dict).
    """
    figures_dir = figures_dir or CONFIG["figures_dir"]
    os.makedirs(figures_dir, exist_ok=True)

    df = load_prepared(processed_dir)
    feature_cols = CONFIG["cluster_features"]
    X_scaled, scaler, valid_idx = scale_features(df, feature_cols)

    # Initialise cluster columns with -2 (= not evaluated / missing features)
    df["cluster_dbscan"] = -2
    df["cluster_agg"] = -2

    # ── DBSCAN ────────────────────────────────────────────────────────────────
    dbscan_labels = run_dbscan(X_scaled)
    df.loc[valid_idx, "cluster_dbscan"] = dbscan_labels
    dbscan_score = compute_silhouette(X_scaled, dbscan_labels, "DBSCAN")
    plot_clusters_map(df.loc[valid_idx], dbscan_labels, "DBSCAN", figures_dir)
    plot_silhouette_samples_chart(X_scaled, dbscan_labels, dbscan_score, "DBSCAN", figures_dir)

    # ── Agglomerative ─────────────────────────────────────────────────────────
    agg_labels = run_agglomerative(X_scaled, CONFIG["agg_n_clusters"])
    df.loc[valid_idx, "cluster_agg"] = agg_labels
    agg_score = compute_silhouette(X_scaled, agg_labels, "Agglomerative")
    plot_clusters_map(df.loc[valid_idx], agg_labels, "Agglomerative", figures_dir)
    plot_silhouette_samples_chart(X_scaled, agg_labels, agg_score, "Agglomerative", figures_dir)
    plot_dendrogram(X_scaled, figures_dir)

    # ── Cluster summaries ─────────────────────────────────────────────────────
    logging.info("\n=== DBSCAN Cluster Summary ===")
    dbscan_summary = cluster_summary(df, "cluster_dbscan")
    logging.info("\n=== Agglomerative Cluster Summary ===")
    agg_summary = cluster_summary(df, "cluster_agg")

    # Save annotated dataset for anomaly detection
    out_path = os.path.join(processed_dir, "clustered_wells.csv")
    df.to_csv(out_path, index=False)
    logging.info(f"Saved clustered dataset to {out_path}")

    metrics = {
        "dbscan_n_clusters": int((np.unique(dbscan_labels) != -1).sum()),
        "dbscan_noise_pct": float((dbscan_labels == -1).mean()),
        "dbscan_silhouette": dbscan_score,
        "agg_n_clusters": CONFIG["agg_n_clusters"],
        "agg_silhouette": agg_score,
    }

    return df, metrics
