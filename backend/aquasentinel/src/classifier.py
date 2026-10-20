"""
classifier.py — AquaSentinel Baseline Classifier Module
=========================================================
Implements the classification pipeline for the groundwater contamination
resource-allocation problem:

  - Random Forest + SMOTE  (primary ensemble model)
  - AdaBoost + SMOTE       (secondary ensemble model)
  - K-Nearest Neighbours   (no-SMOTE baseline for comparison)

Evaluation includes:
  - Standard precision / recall / F1 / ROC-AUC
  - Cost-benefit ROC: finds the threshold that minimises
    (FN * cost_false_negative + FP * cost_false_positive)
    — the core business metric for the resource-allocation framing

All plots are saved to the /figures directory.
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix,
)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

matplotlib.use("Agg")  # non-interactive backend for saving figures
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ─── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    "random_seed": 42,
    "figures_dir": "figures",
    # SMOTE
    "smote_k_neighbors": 5,
    # Random Forest
    "rf_n_estimators": 200,
    "rf_max_depth": 12,
    # AdaBoost
    "adaboost_n_estimators": 150,
    "adaboost_learning_rate": 0.5,
    # KNN baseline
    "knn_n_neighbors": 7,
    # Cost-benefit analysis
    "cost_false_negative": 100,   # penalty for missing a contaminated well (health risk)
    "cost_false_positive": 10,    # penalty for testing a clean well unnecessarily
}
# ──────────────────────────────────────────────────────────────────────────────


def _ensure_figures_dir(figures_dir: str) -> None:
    os.makedirs(figures_dir, exist_ok=True)


def build_rf_pipeline() -> ImbPipeline:
    """
    Builds a Random Forest pipeline with SMOTE over-sampling.

    Returns:
        An imbalanced-learn Pipeline with SMOTE → RandomForestClassifier.
    """
    smote = SMOTE(k_neighbors=CONFIG["smote_k_neighbors"], random_state=CONFIG["random_seed"])
    rf = RandomForestClassifier(
        n_estimators=CONFIG["rf_n_estimators"],
        max_depth=CONFIG["rf_max_depth"],
        class_weight="balanced",
        random_state=CONFIG["random_seed"],
        n_jobs=-1,
    )
    return ImbPipeline(steps=[("smote", smote), ("classifier", rf)])


def build_adaboost_pipeline() -> ImbPipeline:
    """
    Builds an AdaBoost pipeline with SMOTE over-sampling.

    Returns:
        An imbalanced-learn Pipeline with SMOTE → AdaBoostClassifier.
    """
    smote = SMOTE(k_neighbors=CONFIG["smote_k_neighbors"], random_state=CONFIG["random_seed"])
    ada = AdaBoostClassifier(
        n_estimators=CONFIG["adaboost_n_estimators"],
        learning_rate=CONFIG["adaboost_learning_rate"],
        random_state=CONFIG["random_seed"],
    )
    return ImbPipeline(steps=[("smote", smote), ("classifier", ada)])


def build_knn_pipeline() -> KNeighborsClassifier:
    """
    Builds a plain KNN classifier (no SMOTE) as a naive baseline.

    Returns:
        A KNeighborsClassifier instance.
    """
    return KNeighborsClassifier(
        n_neighbors=CONFIG["knn_n_neighbors"],
        n_jobs=-1,
    )


def train_and_evaluate(
    name: str,
    model,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict:
    """
    Trains a model and returns a dict of evaluation metrics.

    Args:
        name:    Human-readable model name for logging and plot labels.
        model:   sklearn / imblearn estimator with fit/predict_proba.
        X_train, X_test, y_train, y_test: Data splits.

    Returns:
        Dict containing roc_auc, avg_precision, fpr, tpr, precision_curve,
        recall_curve, y_prob, report_str.
    """
    logging.info(f"Training {name}...")
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    roc_auc = roc_auc_score(y_test, y_prob)
    avg_precision = average_precision_score(y_test, y_prob)
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_test, y_prob)
    report = classification_report(y_test, y_pred, digits=4)

    logging.info(f"{name} — ROC-AUC: {roc_auc:.4f}  |  Avg Precision: {avg_precision:.4f}")
    logging.info(f"\n{report}")

    return {
        "name": name,
        "model": model,
        "roc_auc": roc_auc,
        "avg_precision": avg_precision,
        "fpr": fpr,
        "tpr": tpr,
        "precision_curve": precision_curve,
        "recall_curve": recall_curve,
        "pr_thresholds": pr_thresholds,
        "y_prob": y_prob,
        "report": report,
    }


def plot_roc_curves(results: list[dict], figures_dir: str) -> None:
    """
    Plots and saves ROC curves for all models on a single axes.

    Args:
        results:     List of result dicts from train_and_evaluate.
        figures_dir: Directory to save the figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#2196F3", "#FF5722", "#4CAF50"]
    for res, color in zip(results, colors):
        ax.plot(
            res["fpr"], res["tpr"],
            label=f"{res['name']} (AUC = {res['roc_auc']:.3f})",
            color=color, lw=2,
        )
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random Classifier")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Groundwater Contamination Detection")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(figures_dir, "roc_curve.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved ROC curve to {path}")


def plot_pr_curves(results: list[dict], figures_dir: str) -> None:
    """
    Plots and saves Precision-Recall curves for all models.

    Args:
        results:     List of result dicts from train_and_evaluate.
        figures_dir: Directory to save the figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#2196F3", "#FF5722", "#4CAF50"]
    for res, color in zip(results, colors):
        ax.plot(
            res["recall_curve"], res["precision_curve"],
            label=f"{res['name']} (AP = {res['avg_precision']:.3f})",
            color=color, lw=2,
        )
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curves — Groundwater Contamination Detection")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(figures_dir, "pr_curve.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved PR curve to {path}")


def cost_benefit_analysis(
    y_test: pd.Series,
    y_prob: np.ndarray,
    model_name: str,
    figures_dir: str,
    cost_fn: float = None,
    cost_fp: float = None,
) -> float:
    """
    Computes the total operational cost across all decision thresholds and
    identifies the optimal threshold that minimises cost.

    Cost model:
        total_cost = FN * cost_fn + FP * cost_fp
      where cost_fn >> cost_fp because missing a contaminated well is far
      more damaging than one unnecessary test.

    Args:
        y_test:      True labels.
        y_prob:      Predicted probabilities.
        model_name:  Used for plot title.
        figures_dir: Directory to save the figure.
        cost_fn:     Cost per false negative (default: CONFIG value).
        cost_fp:     Cost per false positive (default: CONFIG value).

    Returns:
        Optimal threshold value.
    """
    cost_fn = cost_fn or CONFIG["cost_false_negative"]
    cost_fp = cost_fp or CONFIG["cost_false_positive"]

    thresholds = np.linspace(0, 1, 200)
    costs = []
    for t in thresholds:
        y_pred = (y_prob >= t).astype(int)
        fn = ((y_pred == 0) & (y_test == 1)).sum()
        fp = ((y_pred == 1) & (y_test == 0)).sum()
        costs.append(fn * cost_fn + fp * cost_fp)

    costs = np.array(costs)
    opt_idx = np.argmin(costs)
    opt_threshold = thresholds[opt_idx]
    opt_cost = costs[opt_idx]

    logging.info(
        f"{model_name} — Optimal threshold: {opt_threshold:.3f} | "
        f"Min cost: {opt_cost:.0f} "
        f"(FN×{cost_fn} + FP×{cost_fp})"
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(thresholds, costs, color="#2196F3", lw=2, label="Total Cost")
    ax.axvline(opt_threshold, color="#FF5722", ls="--", lw=1.5,
               label=f"Optimal threshold = {opt_threshold:.3f}")
    ax.scatter([opt_threshold], [opt_cost], color="#FF5722", zorder=5, s=80)
    ax.set_xlabel("Decision Threshold (P(contaminated) ≥ threshold → flag for testing)")
    ax.set_ylabel(f"Total Cost  (FN×{cost_fn} + FP×{cost_fp})")
    ax.set_title(f"Cost-Benefit Analysis — {model_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(figures_dir, "cost_benefit_curve.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved cost-benefit curve to {path}")

    return opt_threshold


def plot_confusion_matrix(
    y_test: pd.Series,
    y_prob: np.ndarray,
    threshold: float,
    model_name: str,
    figures_dir: str,
) -> None:
    """
    Plots a confusion matrix at the given decision threshold.

    Args:
        y_test:      True labels.
        y_prob:      Predicted probabilities.
        threshold:   Decision threshold.
        model_name:  Used for title.
        figures_dir: Directory to save the figure.
    """
    y_pred = (y_prob >= threshold).astype(int)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", ax=ax,
        xticklabels=["Clean", "Contaminated"],
        yticklabels=["Clean", "Contaminated"],
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix — {model_name}\n(threshold = {threshold:.3f})")
    fig.tight_layout()
    path = os.path.join(figures_dir, f"confusion_matrix_{model_name.replace(' ', '_').lower()}.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logging.info(f"Saved confusion matrix to {path}")


def run_classifier_pipeline(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    figures_dir: str = None,
) -> dict:
    """
    Full classifier training and evaluation pipeline.
    Trains RF+SMOTE, AdaBoost+SMOTE, and KNN; evaluates and plots all results.

    Args:
        X_train, X_test, y_train, y_test: Data splits from data_prep.py.
        figures_dir: Directory to save output figures (default: CONFIG value).

    Returns:
        Dict mapping model names to their result dicts.
    """
    figures_dir = figures_dir or CONFIG["figures_dir"]
    _ensure_figures_dir(figures_dir)

    models = {
        "Random Forest + SMOTE": build_rf_pipeline(),
        "AdaBoost + SMOTE": build_adaboost_pipeline(),
        "KNN (Baseline)": build_knn_pipeline(),
    }

    results = []
    for name, model in models.items():
        res = train_and_evaluate(name, model, X_train, X_test, y_train, y_test)
        results.append(res)

    # Combined ROC and PR curves
    plot_roc_curves(results, figures_dir)
    plot_pr_curves(results, figures_dir)

    # Cost-benefit analysis on the best model (RF)
    rf_result = results[0]
    opt_threshold = cost_benefit_analysis(
        y_test, rf_result["y_prob"], rf_result["name"], figures_dir
    )

    # Confusion matrix at optimal threshold for RF
    plot_confusion_matrix(
        y_test, rf_result["y_prob"], opt_threshold, rf_result["name"], figures_dir
    )

    return {res["name"]: res for res in results}
