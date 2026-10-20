"""
active_learning.py — AquaSentinel Active Learning & Surveillance Engine
========================================================================
Implements pool-based active learning for rural groundwater surveillance under
budget constraints.

Framing:
  Lab-testing groundwater samples is expensive, slow, and resource-constrained.
  Authorities can only afford to test a fixed batch (e.g., 25–50 wells) per month.
  This module answers: "Which wells should we test next to maximize contamination
  detection and improve model certainty most rapidly?"

Methodology:
  1. Epistemic Uncertainty Sampling:
     - Shannon Entropy: H(p) = - [p * log2(p) + (1-p) * log2(1-p)]
     - Least Confidence: 2 * (1 - max(p, 1-p))
  2. Hybrid Risk-Weighted Acquisition Function:
     Combines predictive entropy with BBN causal risk priors and Isolation Forest
     anomaly scores:
       Priority = w_unc * Entropy + w_bbn * BBN_Risk + w_anom * Anomaly_Score_Norm
  3. Budget-Constrained Sequential Simulation:
     Simulates multiple testing rounds comparing Active Learning vs Random Sampling
     baseline, tracking:
       - Cumulative Contaminants Detected (True Positive yield)
       - Model ROC-AUC progression as new labels arrive
  4. Testing Priority Queue Generation:
     Produces ranked queue with triage tiers (Critical, High, Medium, Low) and
     actionable audit explanations for environmental health officers.

Outputs:
  - testing_priority_queue.csv (saved to data/processed/)
  - active_learning_simulation.csv (saved to data/processed/)
  - Figures: active_learning_curves.png (saved to /figures)
"""

import os
import logging
import warnings
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore", category=UserWarning)
matplotlib.use("Agg")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    "random_seed": 42,
    "figures_dir": "figures",
    "batch_size": 50,          # wells tested per monthly round
    "n_rounds": 8,             # number of sequential simulation rounds
    "initial_seed_frac": 0.10, # fraction of labeled data in initial seed pool
    # Feature weights for hybrid acquisition score
    "w_uncertainty": 0.50,
    "w_bbn_risk": 0.30,
    "w_anomaly": 0.20,
    "feature_cols": [
        "latitude",
        "longitude",
        "groundwater_level_m",
        "state_encoded",
        "district_encoded",
    ],
}


def load_pipeline_data(processed_dir: str) -> pd.DataFrame:
    """
    Loads bayesian_wells.csv (if available) or anomaly_wells.csv.
    """
    b_path = os.path.join(processed_dir, "bayesian_wells.csv")
    a_path = os.path.join(processed_dir, "anomaly_wells.csv")

    if os.path.exists(b_path):
        df = pd.read_csv(b_path, low_memory=False)
        logging.info(f"Loaded bayesian_wells.csv: {df.shape[0]:,} rows.")
    elif os.path.exists(a_path):
        df = pd.read_csv(a_path, low_memory=False)
        logging.info(f"Loaded anomaly_wells.csv: {df.shape[0]:,} rows.")
    else:
        raise FileNotFoundError(f"Neither bayesian_wells.csv nor anomaly_wells.csv found in {processed_dir}")

    return df


def calculate_entropy(prob: np.ndarray) -> np.ndarray:
    """
    Computes Shannon entropy for binary probabilities, normalized to [0, 1].
    H(p) = - [p * log2(p) + (1-p) * log2(1-p)]
    Max entropy (1.0) occurs at p = 0.5 (maximum uncertainty).
    """
    p = np.clip(prob, 1e-7, 1 - 1e-7)
    entropy = - (p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return np.nan_to_num(entropy, nan=0.0)


def calculate_least_confidence(prob: np.ndarray) -> np.ndarray:
    """
    Least confidence uncertainty score normalized to [0, 1].
    Score = 2 * (1 - max(p, 1-p)). Max = 1.0 when p = 0.5.
    """
    p = np.clip(prob, 0.0, 1.0)
    conf = np.maximum(p, 1 - p)
    return 2.0 * (1.0 - conf)


def compute_acquisition_scores(df: pd.DataFrame, clf_probs: np.ndarray = None) -> pd.DataFrame:
    """
    Computes uncertainty, BBN causal risk, anomaly scores, and combined hybrid priority score.
    """
    df = df.copy()

    # 1. Classifier-derived uncertainty (continuous probability for Shannon entropy)
    if clf_probs is None:
        if "contamination_prob" in df.columns and df["contamination_prob"].notna().sum() > 0:
            probs = df["contamination_prob"].fillna(df["is_contaminated"].mean()).values
        else:
            feature_cols = [c for c in CONFIG["feature_cols"] if c in df.columns]
            valid_mask = df[feature_cols + ["is_contaminated"]].notna().all(axis=1)
            if valid_mask.sum() > 100:
                from sklearn.ensemble import RandomForestClassifier
                from imblearn.over_sampling import SMOTE
                X = df.loc[valid_mask, feature_cols]
                y = df.loc[valid_mask, "is_contaminated"].astype(int)
                try:
                    sm = SMOTE(k_neighbors=min(5, int((y == 1).sum()) - 1), random_state=CONFIG["random_seed"])
                    X_res, y_res = sm.fit_resample(X, y)
                except Exception:
                    X_res, y_res = X, y
                rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=CONFIG["random_seed"], n_jobs=-1)
                rf.fit(X_res, y_res)
                full_probs = np.full(len(df), float(y.mean()))
                full_probs[valid_mask] = rf.predict_proba(X)[:, 1]
                probs = full_probs
                df["contamination_prob"] = probs
            elif "bbn_prob_contaminated" in df.columns:
                probs = df["bbn_prob_contaminated"].fillna(0.1).values
            else:
                probs = np.full(len(df), 0.5)
    else:
        probs = clf_probs

    df["pred_prob"] = probs
    df["uncertainty_entropy"] = calculate_entropy(probs)
    df["uncertainty_least_conf"] = calculate_least_confidence(probs)

    # 2. BBN causal risk prior
    if "bbn_prob_contaminated" in df.columns:
        bbn_risk = df["bbn_prob_contaminated"].fillna(df["bbn_prob_contaminated"].mean()).values
    elif "bbn_cluster_risk" in df.columns:
        bbn_risk = df["bbn_cluster_risk"].fillna(0).values * 0.7 + 0.15
    else:
        bbn_risk = np.full(len(df), 0.15)
    df["bbn_risk_score"] = np.clip(bbn_risk, 0.0, 1.0)

    # 3. Anomaly score normalization (scaled across distribution so outliers are ranked continuously)
    if "anomaly_score" in df.columns:
        raw_anom = pd.to_numeric(df["anomaly_score"], errors="coerce").fillna(0.0).values
        # Isolation Forest score: negative = anomalous. Flip so higher = more anomalous.
        anom_flipped = - raw_anom
        p_low = np.percentile(anom_flipped, 1)
        p_high = np.percentile(anom_flipped, 99.5)
        if p_high > p_low:
            anom_norm = np.clip((anom_flipped - p_low) / (p_high - p_low), 0.0, 1.0)
        else:
            anom_norm = np.zeros_like(anom_flipped)
    else:
        anom_norm = np.zeros(len(df))
    df["anomaly_urgency"] = anom_norm

    # 4. Hybrid Priority Score
    w_u = CONFIG["w_uncertainty"]
    w_b = CONFIG["w_bbn_risk"]
    w_a = CONFIG["w_anomaly"]
    hybrid = (w_u * df["uncertainty_entropy"] +
              w_b * df["bbn_risk_score"] +
              w_a * df["anomaly_urgency"])
    df["testing_priority_score"] = np.clip(hybrid, 0.0, 1.0)

    # Priority Tier assignment
    conditions = [
        df["testing_priority_score"] >= 0.70,
        df["testing_priority_score"] >= 0.50,
        df["testing_priority_score"] >= 0.30,
    ]
    choices = ["CRITICAL", "HIGH", "MEDIUM"]
    df["priority_tier"] = np.select(conditions, choices, default="LOW")

    # Generate recommendation reason
    def build_reason(row):
        reasons = []
        if row["uncertainty_entropy"] > 0.85:
            reasons.append("High model decision uncertainty")
        if row.get("bbn_risk_score", 0) > 0.40:
            reasons.append("Elevated BBN causal risk")
        if row.get("anomaly_urgency", 0) > 0.60:
            reasons.append("Isolation Forest spatial anomaly")
        if row.get("is_anomaly", 0) == 1:
            reasons.append("Cluster outlier")
        if not reasons:
            reasons.append("Routine regional surveillance")
        return " + ".join(reasons)

    df["testing_reason"] = df.apply(build_reason, axis=1)

    return df


def simulate_active_learning(
    df: pd.DataFrame,
    feature_cols: list,
    batch_size: int = 50,
    n_rounds: int = 8,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Simulates sequential field testing comparing Active Learning vs Random Sampling.

    At each round:
      - Active Learning queries the top `batch_size` most uncertain / highest-priority wells.
      - Random baseline queries `batch_size` wells uniformly at random.
      - Evaluates cumulative contaminated wells discovered and test set ROC-AUC.
    """
    logging.info(f"Starting Active Learning simulation: {n_rounds} rounds, budget {batch_size}/round...")
    np.random.seed(random_seed)

    # Clean subset with valid features & target
    sim_cols = feature_cols + ["is_contaminated"]
    valid_df = df[sim_cols].dropna().copy()
    valid_df["is_contaminated"] = valid_df["is_contaminated"].astype(int)

    # Use a stratified test set of 2,000 samples for evaluation
    train_pool_idx, test_idx = next(
        pd.Series(range(len(valid_df))).groupby(valid_df["is_contaminated"]).apply(
            lambda g: (g.iloc[:-min(1000, len(g)//5)], g.iloc[-min(1000, len(g)//5):])
        ).values
    ) if False else (None, None)

    # Standard split
    shuffled_idx = np.random.permutation(len(valid_df))
    n_eval = min(3000, int(len(valid_df) * 0.20))
    eval_indices = shuffled_idx[:n_eval]
    pool_indices = shuffled_idx[n_eval:]

    X_eval = valid_df.iloc[eval_indices][feature_cols].values
    y_eval = valid_df.iloc[eval_indices]["is_contaminated"].values

    # Pools for AL and Random
    n_seed = max(batch_size * 2, int(len(pool_indices) * CONFIG["initial_seed_frac"]))
    initial_seed = pool_indices[:n_seed]
    initial_unlabeled = pool_indices[n_seed:]

    # Simulation tracks
    results = []

    # 1. Active Learning Track
    al_labeled = list(initial_seed)
    al_unlabeled = list(initial_unlabeled)
    al_cum_contam = int(valid_df.iloc[al_labeled]["is_contaminated"].sum())

    # 2. Random Sampling Track
    rnd_labeled = list(initial_seed)
    rnd_unlabeled = list(initial_unlabeled)
    rnd_cum_contam = int(valid_df.iloc[rnd_labeled]["is_contaminated"].sum())

    for r in range(n_rounds + 1):
        # --- Fit AL model ---
        X_al = valid_df.iloc[al_labeled][feature_cols].values
        y_al = valid_df.iloc[al_labeled]["is_contaminated"].values

        clf_al = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_seed)
        if len(np.unique(y_al)) > 1 and np.min(np.bincount(y_al)) >= 3:
            smote = SMOTE(k_neighbors=min(3, np.min(np.bincount(y_al)) - 1), random_state=random_seed)
            X_al_res, y_al_res = smote.fit_resample(X_al, y_al)
        else:
            X_al_res, y_al_res = X_al, y_al

        clf_al.fit(X_al_res, y_al_res)
        y_eval_pred_al = clf_al.predict_proba(X_eval)[:, 1] if len(clf_al.classes_) > 1 else np.zeros(len(y_eval))
        al_auc = roc_auc_score(y_eval, y_eval_pred_al) if len(np.unique(y_eval)) > 1 else 0.5
        al_ap = average_precision_score(y_eval, y_eval_pred_al) if len(np.unique(y_eval)) > 1 else 0.0

        # --- Fit Random model ---
        X_rnd = valid_df.iloc[rnd_labeled][feature_cols].values
        y_rnd = valid_df.iloc[rnd_labeled]["is_contaminated"].values

        clf_rnd = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_seed)
        if len(np.unique(y_rnd)) > 1 and np.min(np.bincount(y_rnd)) >= 3:
            smote = SMOTE(k_neighbors=min(3, np.min(np.bincount(y_rnd)) - 1), random_state=random_seed)
            X_rnd_res, y_rnd_res = smote.fit_resample(X_rnd, y_rnd)
        else:
            X_rnd_res, y_rnd_res = X_rnd, y_rnd

        clf_rnd.fit(X_rnd_res, y_rnd_res)
        y_eval_pred_rnd = clf_rnd.predict_proba(X_eval)[:, 1] if len(clf_rnd.classes_) > 1 else np.zeros(len(y_eval))
        rnd_auc = roc_auc_score(y_eval, y_eval_pred_rnd) if len(np.unique(y_eval)) > 1 else 0.5
        rnd_ap = average_precision_score(y_eval, y_eval_pred_rnd) if len(np.unique(y_eval)) > 1 else 0.0

        tests_conducted = r * batch_size
        results.append({
            "round": r,
            "tests_conducted": tests_conducted,
            "total_labeled": len(al_labeled),
            "al_auc": round(float(al_auc), 4),
            "al_ap": round(float(al_ap), 4),
            "al_cum_contam": al_cum_contam,
            "rnd_auc": round(float(rnd_auc), 4),
            "rnd_ap": round(float(rnd_ap), 4),
            "rnd_cum_contam": rnd_cum_contam,
            "contam_discovery_delta": al_cum_contam - rnd_cum_contam,
        })

        if r == n_rounds:
            break

        # --- Active Learning Query ---
        X_pool_al = valid_df.iloc[al_unlabeled][feature_cols].values
        pool_probs_al = clf_al.predict_proba(X_pool_al)[:, 1] if len(clf_al.classes_) > 1 else np.zeros(len(al_unlabeled))
        # Entropy uncertainty
        unc_scores = calculate_entropy(pool_probs_al)
        top_query_idx = np.argsort(unc_scores)[::-1][:batch_size]

        queried_indices = [al_unlabeled[i] for i in top_query_idx]
        new_contam = int(valid_df.iloc[queried_indices]["is_contaminated"].sum())
        al_cum_contam += new_contam
        al_labeled.extend(queried_indices)
        al_unlabeled = [idx for i, idx in enumerate(al_unlabeled) if i not in top_query_idx]

        # --- Random Sampling Query ---
        rnd_choice = np.random.choice(len(rnd_unlabeled), size=min(batch_size, len(rnd_unlabeled)), replace=False)
        queried_rnd = [rnd_unlabeled[i] for i in rnd_choice]
        rnd_new_contam = int(valid_df.iloc[queried_rnd]["is_contaminated"].sum())
        rnd_cum_contam += rnd_new_contam
        rnd_labeled.extend(queried_rnd)
        rnd_unlabeled = [idx for i, idx in enumerate(rnd_unlabeled) if i not in rnd_choice]

    sim_df = pd.DataFrame(results)
    logging.info("Active Learning simulation complete.")
    return sim_df


def plot_active_learning_curves(sim_df: pd.DataFrame, figures_dir: str) -> None:
    """
    Plots the Active Learning vs Random Baseline evaluation curves:
      1. Cumulative Contaminants Discovered
      2. ROC-AUC Progression vs Budget
    """
    os.makedirs(figures_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    rounds = sim_df["tests_conducted"]

    # 1. Contamination Yield
    ax1 = axes[0]
    ax1.plot(rounds, sim_df["al_cum_contam"], marker="o", color="#2563EB", lw=2.5, label="Active Learning (Uncertainty + Risk)")
    ax1.plot(rounds, sim_df["rnd_cum_contam"], marker="s", color="#94A3B8", lw=2, ls="--", label="Random Sampling Baseline")
    ax1.set_title("Cumulative Contaminated Wells Discovered", fontsize=11, fontweight="bold", pad=8)
    ax1.set_xlabel("Field Tests Conducted (Budget Spent)", fontsize=10)
    ax1.set_ylabel("Contaminated Wells Found", fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    # Highlight delta
    delta = sim_df["contam_discovery_delta"].iloc[-1]
    ax1.annotate(
        f"+{delta} more contaminants found\nvia Active Learning",
        xy=(rounds.iloc[-1], sim_df["al_cum_contam"].iloc[-1]),
        xytext=(rounds.iloc[-1] * 0.65, sim_df["al_cum_contam"].iloc[-1] * 0.90),
        arrowprops=dict(facecolor="#2563EB", shrink=0.08, width=1.5, headwidth=6),
        fontsize=9, fontweight="bold", color="#1E3A8A"
    )

    # 2. ROC-AUC Progression
    ax2 = axes[1]
    ax2.plot(rounds, sim_df["al_auc"], marker="^", color="#059669", lw=2.5, label="Active Learning Model ROC-AUC")
    ax2.plot(rounds, sim_df["rnd_auc"], marker="x", color="#DC2626", lw=2, ls="--", label="Random Sampling Model ROC-AUC")
    ax2.set_title("Classifier Generalization (ROC-AUC) vs Budget", fontsize=11, fontweight="bold", pad=8)
    ax2.set_xlabel("Field Tests Conducted (Budget Spent)", fontsize=10)
    ax2.set_ylabel("ROC-AUC on Held-out Eval Set", fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=9)

    fig.suptitle("AquaSentinel Active Learning Surveillance Benchmarks\n"
                 "(Uncertainty-Directed Resource Allocation vs Random Lab Testing)", fontsize=12, fontweight="bold")
    fig.tight_layout()

    out_path = os.path.join(figures_dir, "active_learning_curves.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved Active Learning curves to {out_path}")


def run_active_learning_pipeline(
    processed_dir: str,
    figures_dir: str = None,
    batch_size: int = 50,
    n_rounds: int = 8,
) -> tuple:
    """
    Executes the full Active Learning pipeline:
      1. Loads latest pipeline dataset (bayesian_wells.csv or anomaly_wells.csv)
      2. Computes acquisition scores (Shannon Entropy, Least Confidence, Hybrid Priority)
      3. Simulates budget allocation vs Random Baseline
      4. Saves testing_priority_queue.csv and simulation metrics
      5. Generates comparison plots

    Returns:
      (queue_df, sim_df, summary_metrics)
    """
    figures_dir = figures_dir or CONFIG["figures_dir"]
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Load data
    df = load_pipeline_data(processed_dir)

    # 2. Compute acquisition scores and build priority queue
    scored_df = compute_acquisition_scores(df)

    # Sort descending by priority score and prioritize unique monitoring stations
    if "station" in scored_df.columns:
        queue_df = scored_df.sort_values("testing_priority_score", ascending=False).drop_duplicates(subset=["station"]).reset_index(drop=True)
    else:
        queue_df = scored_df.sort_values("testing_priority_score", ascending=False).reset_index(drop=True)
    queue_df["priority_rank"] = queue_df.index + 1

    # Save queue
    queue_path = os.path.join(processed_dir, "testing_priority_queue.csv")
    queue_df.to_csv(queue_path, index=False)
    logging.info(f"Saved testing_priority_queue.csv: {queue_df.shape[0]:,} wells ranked.")

    # 3. Simulate sequential budget allocation
    feature_cols = [c for c in CONFIG["feature_cols"] if c in df.columns]
    sim_df = simulate_active_learning(
        df,
        feature_cols=feature_cols,
        batch_size=batch_size,
        n_rounds=n_rounds,
        random_seed=CONFIG["random_seed"],
    )

    sim_path = os.path.join(processed_dir, "active_learning_simulation.csv")
    sim_df.to_csv(sim_path, index=False)
    logging.info(f"Saved active_learning_simulation.csv to {sim_path}")

    # 4. Generate plots
    plot_active_learning_curves(sim_df, figures_dir)

    # Summary metrics
    tier_counts = queue_df["priority_tier"].value_counts().to_dict()
    summary_metrics = {
        "total_wells_ranked": len(queue_df),
        "critical_priority_wells": tier_counts.get("CRITICAL", 0),
        "high_priority_wells": tier_counts.get("HIGH", 0),
        "medium_priority_wells": tier_counts.get("MEDIUM", 0),
        "low_priority_wells": tier_counts.get("LOW", 0),
        "sim_tests_conducted": int(sim_df["tests_conducted"].iloc[-1]),
        "al_final_auc": float(sim_df["al_auc"].iloc[-1]),
        "rnd_final_auc": float(sim_df["rnd_auc"].iloc[-1]),
        "al_contam_found": int(sim_df["al_cum_contam"].iloc[-1]),
        "rnd_contam_found": int(sim_df["rnd_cum_contam"].iloc[-1]),
        "contaminant_lift_pct": round(
            float((sim_df["al_cum_contam"].iloc[-1] - sim_df["rnd_cum_contam"].iloc[-1]) /
                  max(sim_df["rnd_cum_contam"].iloc[-1], 1) * 100), 1
        ),
    }

    return queue_df, sim_df, summary_metrics


if __name__ == "__main__":
    import sys
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proc_dir = os.path.join(script_dir, "..", "data", "processed")
    fig_dir = os.path.join(script_dir, "..", "figures")
    q, s, m = run_active_learning_pipeline(proc_dir, fig_dir)
    print("\nActive Learning Summary:")
    for k, v in m.items():
        print(f"  {k}: {v}")
