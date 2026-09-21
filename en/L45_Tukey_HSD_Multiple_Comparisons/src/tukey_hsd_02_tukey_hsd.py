"""
Lesson 45 - Step 2: Tukey HSD Simultaneous Comparisons
======================================================

THE RECIPE
----------
Start from tukey_hsd_01_pairwise_unadjusted.py, then introduce:
    1. tukey_comparisons()  statsmodels pairwise_tukeyhsd at FWER=0.05
    2. decision_table()     mean diffs, adjusted p, simultaneous CIs
    3. save_figure()        Tukey intervals that control familywise error

Context:
--------
Tukey's Honestly Significant Difference (HSD) test solves the multiple
comparisons problem by adjusting the confidence intervals and p-values based
on the Studentized Range distribution. Instead of letting the error rate
compound with every test, it guarantees a Familywise Error Rate (FWER) of
alpha (e.g., 0.05) across *all* pairwise comparisons simultaneously.
The same 36 cycle times are rebuilt from seed 42. No earlier lesson script is
imported. Tukey answers the pairwise question that a significant ANOVA F left
open, while keeping the familywise error at 0.05.

How to read this file:
----------------------
1. `tukey_comparisons()` runs the Tukey HSD test using statsmodels.
2. `decision_table()` extracts the results of the Tukey test into a clean
   pandas DataFrame.
3. `save_figure()` visualizes the simultaneous confidence intervals. If an
   interval crosses 0, the difference is not significant.

Run it:
-------
    uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_02_tukey_hsd.py
"""

# itertools provides combinations to generate all unique pairs of groups
from itertools import combinations
# pathlib handles cross-platform file paths
from pathlib import Path

# matplotlib for plotting
import matplotlib
# numpy for array operations and random generation
import numpy as np
# pandas for dataframes
import pandas as pd
# statsmodels provides the pairwise_tukeyhsd function
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Use 'Agg' to avoid popping up a display window when saving plots
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CONSTANTS ---
# SEED ensures the identical dataset as step 1
SEED = 42
# N_PER_GROUP is 12 cycle times per group
N_PER_GROUP = 12
# TREATMENTS are the categorical method labels
TREATMENTS = ("Standard", "Guided", "Automated")
# TRUE_MEANS are the population means from which we draw samples
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
# SIGMA is the population standard deviation
SIGMA = 3.2
# ALPHA is our targeted familywise error rate (FWER)
ALPHA = 0.05
# DIR_FIGURES dictates where plots go
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild the three synthetic cycle-time samples from seed 42.

    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'method' and 'cycle_time_seconds' columns.

    Notes
    -----
    Provides exactly the same data as step 1 because we use the same
    seed and sampling order.
    """
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)


# --- NEW (1) tukey_comparisons() ---------------------------------------------
def tukey_comparisons(sample: pd.DataFrame) -> object:
    """
    Fit Tukey HSD with familywise error rate 0.05.

    Parameters
    ----------
    sample : pd.DataFrame
        Dataset containing response and group columns.

    Returns
    -------
    object
        A statsmodels MultiComparison results object containing the
        Tukey HSD output (adjusted p-values, confidence bounds).

    Notes
    -----
    Tukey HSD compares all possible pairs of means and adjusts for the
    fact that we are making multiple comparisons. It strictly controls
    FWER under the assumption of equal variances across groups.
    """
    # endog refers to the endogenous (response) variable
    # groups refers to the independent grouping variable
    return pairwise_tukeyhsd(
        endog=sample["cycle_time_seconds"],
        groups=sample["method"],
        alpha=ALPHA,
    )
# ------------------------------------------------------------------------------


# --- NEW (2) decision_table() ------------------------------------------------
def decision_table(tukey: object) -> pd.DataFrame:
    """
    Extract mean differences, adjusted p-values, and simultaneous CIs.

    Parameters
    ----------
    tukey : object
        The statsmodels Tukey HSD result object.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe of pairwise comparisons with adjusted bounds
        and p-values.

    Notes
    -----
    This unwraps the statsmodels custom object into a standard pandas
    DataFrame so it is easier to read, export, and plot.
    """
    # Get the list of unique groups
    unique_groups = list(tukey.groupsunique)
    # Generate all pairwise combinations
    pair_names = list(combinations(unique_groups, 2))

    rows = []
    # Zip together the various array properties from the tukey result object
    for (group1, group2), diff, p_adj, bounds, reject in zip(
        pair_names,
        tukey.meandiffs,
        tukey.pvalues,
        tukey.confint,
        tukey.reject,
    ):
        rows.append(
            {
                "group1": group1,
                "group2": group2,
                "meandiff": float(diff),
                "p-adj": float(p_adj),
                "lower": float(bounds[0]),  # Lower bound of confidence interval
                "upper": float(bounds[1]),  # Upper bound of confidence interval
                "reject": bool(reject),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(table: pd.DataFrame) -> Path:
    """
    Save Tukey simultaneous confidence intervals for every pair.

    Parameters
    ----------
    table : pd.DataFrame
        The pairwise comparison data with lower and upper CI bounds.

    Returns
    -------
    Path
        Absolute path to the saved PNG plot.

    Notes
    -----
    If a confidence interval overlaps the zero line, the difference between
    that pair is not statistically significant at our chosen FWER.
    """
    output_path = DIR_FIGURES / "tukey_hsd_02_tukey_hsd.png"

    # Format labels for the Y-axis
    labels = [f"{g1} -\n{g2}" for g1, g2 in zip(table["group1"], table["group2"])]

    # Extract numerical arrays for plotting
    diffs = table["meandiff"].to_numpy(dtype=float)
    lower = table["lower"].to_numpy(dtype=float)
    upper = table["upper"].to_numpy(dtype=float)

    # y-coordinates for each comparison
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Draw the confidence intervals as horizontal lines
    ax.hlines(y, lower, upper, color="#1A2E51", linewidth=2.2)
    # Plot the point estimates (mean differences) as dots
    ax.scatter(diffs, y, color="#EC2661", zorder=3, s=42, label="Mean difference")
    # Draw a vertical dashed line at zero (the null hypothesis line)
    ax.axvline(0.0, color="#646464", linestyle="--", linewidth=1.2)

    # Configure the y-axis labels
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    # Decorate plot
    ax.set_xlabel("Mean difference (seconds)")
    ax.set_title("Tukey HSD Simultaneous 95% Intervals")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="lower right")

    # Save the figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Rebuild the dataset
    sample = build_cycle_times()
    # 2. Fit the Tukey HSD model
    tukey = tukey_comparisons(sample)
    # 3. Extract the results into a DataFrame
    table = decision_table(tukey)
    # 4. Save the interval plot
    figure_path = save_figure(table)

    print("================================================================")
    print("LESSON 45 - STEP 2: TUKEY HSD")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Familywise alpha                : {ALPHA:.2f}")

    # Print the detailed decision matrix
    for _, row in table.iterrows():
        print(
            f"{row['group1']} vs {row['group2']:<10}: "
            f"diff={float(row['meandiff']):.6f}, "
            f"p-adj={float(row['p-adj']):.6f}, "
            f"CI=({float(row['lower']):.6f}, {float(row['upper']):.6f}), "
            f"reject={bool(row['reject'])}"
        )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

