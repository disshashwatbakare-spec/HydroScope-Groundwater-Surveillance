"""
data_prep.py — AquaSentinel Data Preparation Module
=====================================================
Responsible for:
  - Loading and cleaning the unified_wells.csv produced by merge.py
  - Consolidating duplicate coordinate columns
  - Constructing the binary contamination target (EC > threshold)
  - Engineering features that are realistically available BEFORE a well is tested
    (geospatial, regional, hydrological) — deliberately excludes same-day chemistry
    readings to prevent data leakage in the resource-allocation framing
  - Imputing missing groundwater levels with district-level medians
  - Encoding categorical features
  - Producing a stratified train/test split (by region/state)
"""

import os
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    "ec_contamination_threshold": 3000,   # µS/cm — high salinity / contamination proxy
    "test_size": 0.20,
    "random_seed": 42,
    # Features available BEFORE a well is chemically tested (no data leakage)
    "feature_cols": [
        "latitude",
        "longitude",
        "groundwater_level_m",
        "state_encoded",
        "district_encoded",
    ],
    "target_col": "is_contaminated",
}
# ──────────────────────────────────────────────────────────────────────────────


def load_unified(processed_dir: str) -> pd.DataFrame:
    """
    Loads the unified_wells.csv produced by merge.py.

    Args:
        processed_dir: Path to the `data/processed/` directory.

    Returns:
        Raw unified DataFrame.
    """
    path = os.path.join(processed_dir, "unified_wells.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"unified_wells.csv not found at {path}. Run the ingest/merge pipeline first."
        )
    df = pd.read_csv(path, low_memory=False)
    logging.info(f"Loaded unified_wells.csv: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df


def consolidate_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the triplicated lat/lon columns (lat_chem, lat_phys, lat) into
    single `latitude` and `longitude` columns, preferring the levels source
    then physical then chemical.

    Args:
        df: Raw unified DataFrame.

    Returns:
        DataFrame with unified `latitude` / `longitude` columns.
    """
    # Priority: levels (lat/lon) → physical (lat_phys/lon_phys) → chemical (lat_chem/lon_chem)
    df["latitude"] = df.get("lat", np.nan)
    df["longitude"] = df.get("lon", np.nan)

    for lat_col, lon_col in [("lat_phys", "lon_phys"), ("lat_chem", "lon_chem")]:
        mask = df["latitude"].isna()
        if lat_col in df.columns:
            df.loc[mask, "latitude"] = df.loc[mask, lat_col]
        mask = df["longitude"].isna()
        if lon_col in df.columns:
            df.loc[mask, "longitude"] = df.loc[mask, lon_col]

    lat_coverage = df["latitude"].notna().mean()
    logging.info(f"Coordinate coverage after consolidation: {lat_coverage:.1%}")
    return df


def create_target(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Creates the binary contamination target column.
    is_contaminated = 1 if EC > threshold, 0 otherwise.
    Rows where EC is entirely missing are dropped (no ground truth).

    Args:
        df: DataFrame with an `ec` column.
        threshold: EC value (µS/cm) above which a well is considered contaminated.

    Returns:
        DataFrame with `is_contaminated` column added; EC-null rows dropped.
    """
    before = len(df)
    df = df.dropna(subset=["ec"]).copy()
    df["ec_numeric"] = pd.to_numeric(df["ec"], errors="coerce")
    df = df.dropna(subset=["ec_numeric"])
    after = len(df)
    logging.info(f"Dropped {before - after} rows with missing EC. Remaining: {after}")

    df[CONFIG["target_col"]] = (df["ec_numeric"] > threshold).astype(int)
    pos_rate = df[CONFIG["target_col"]].mean()
    logging.info(
        f"Target created. Contamination rate (EC > {threshold}): {pos_rate:.2%} "
        f"({df[CONFIG['target_col']].sum()} positive / {len(df)} total)"
    )
    return df


def impute_groundwater_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames the groundwater level column and imputes missing values with
    the district-level median (falls back to state-level, then global median).

    Args:
        df: DataFrame with `groundwater_level_quarterly_manual_meter` column.

    Returns:
        DataFrame with clean `groundwater_level_m` column.
    """
    raw_col = "groundwater_level_quarterly_manual_meter"
    df["groundwater_level_m"] = pd.to_numeric(df.get(raw_col, np.nan), errors="coerce")

    missing_before = df["groundwater_level_m"].isna().sum()

    # District-level median imputation
    district_median = df.groupby("district")["groundwater_level_m"].transform("median")
    df["groundwater_level_m"] = df["groundwater_level_m"].fillna(district_median)

    # State-level fallback
    state_median = df.groupby("state")["groundwater_level_m"].transform("median")
    df["groundwater_level_m"] = df["groundwater_level_m"].fillna(state_median)

    # Global fallback
    global_median = df["groundwater_level_m"].median()
    df["groundwater_level_m"] = df["groundwater_level_m"].fillna(global_median)

    missing_after = df["groundwater_level_m"].isna().sum()
    logging.info(
        f"Groundwater level imputation: {missing_before} missing → {missing_after} remaining."
    )
    return df


def encode_categoricals(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Label-encodes `state` and `district` columns.

    Args:
        df: DataFrame with `state` and `district` string columns.

    Returns:
        Tuple of (encoded DataFrame, dict of fitted LabelEncoders).
    """
    encoders = {}
    for col in ["state", "district"]:
        df[col] = df[col].astype(str).str.strip().str.lower()
        le = LabelEncoder()
        df[f"{col}_encoded"] = le.fit_transform(df[col])
        encoders[col] = le
        logging.info(f"Encoded `{col}`: {len(le.classes_)} unique values.")
    return df, encoders


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Selects the approved, leak-free feature set and the target column.

    Args:
        df: Fully prepared DataFrame.

    Returns:
        Tuple of (X features DataFrame, y target Series).
    """
    feature_cols = CONFIG["feature_cols"]
    target_col = CONFIG["target_col"]

    # Drop rows where any feature is still missing
    before = len(df)
    df_clean = df.dropna(subset=feature_cols + [target_col])
    after = len(df_clean)
    logging.info(
        f"Feature preparation: dropped {before - after} rows with missing features. "
        f"Final dataset: {after} rows."
    )

    X = df_clean[feature_cols].copy()
    y = df_clean[target_col].copy()
    return X, y


def split_data(
    X: pd.DataFrame, y: pd.Series
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Stratified train/test split to ensure the rare contamination class is
    proportionally represented in both sets.

    Args:
        X: Feature matrix.
        y: Target vector.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=CONFIG["test_size"],
        random_state=CONFIG["random_seed"],
        stratify=y,
    )
    logging.info(
        f"Train: {len(X_train)} samples ({y_train.mean():.2%} contaminated) | "
        f"Test: {len(X_test)} samples ({y_test.mean():.2%} contaminated)"
    )
    return X_train, X_test, y_train, y_test


def run_data_prep(processed_dir: str) -> tuple:
    """
    Full data preparation pipeline. Orchestrates all steps above.

    Args:
        processed_dir: Path to the `data/processed/` directory.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test, encoders, df_prepared).
    """
    df = load_unified(processed_dir)
    df = consolidate_coordinates(df)
    df = create_target(df, threshold=CONFIG["ec_contamination_threshold"])
    df = impute_groundwater_level(df)
    df, encoders = encode_categoricals(df)
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Save the prepared dataset for reference
    df_out = df[CONFIG["feature_cols"] + [CONFIG["target_col"], "station", "state", "district", "date", "ec_numeric"]].copy()
    out_path = os.path.join(processed_dir, "prepared_wells.csv")
    df_out.to_csv(out_path, index=False)
    logging.info(f"Saved prepared dataset to {out_path}")

    return X_train, X_test, y_train, y_test, encoders, df_out
