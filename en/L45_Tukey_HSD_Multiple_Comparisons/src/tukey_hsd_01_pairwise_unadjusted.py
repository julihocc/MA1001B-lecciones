"""
Lesson 45 - Step 1: Unadjusted Pairwise t Tests
===============================================

THE RECIPE
----------
NEW IN THIS STEP: build_cycle_times(), unadjusted_pairwise(), and
save_figure().

Context:
--------
In analysis of variance (ANOVA), we determine if there are any statistically
significant differences between the means of three or more independent groups.
If we find a significant result (an overall significant F-test), we know that
at least one mean is different, but not *which* ones.
The same synthetic packing experiment has three methods and n=12 stations
each. After a significant ANOVA F, three pairwise t tests are tempting. This
step runs those unadjusted tests and records every p-value, before any
familywise correction.

How to read this file:
----------------------
1. `build_cycle_times()` generates the synthetic data for three groups.
2. `unadjusted_pairwise()` manually computes the independent two-sample
   t-tests for every pair of groups.
3. `save_figure()` visualizes the mean differences and their unadjusted p-values.

Run it:
-------
    uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_01_pairwise_unadjusted.py
"""

# itertools provides combinations to easily generate all unique pairs of groups
from itertools import combinations
# pathlib makes handling file paths more robust across operating systems
from pathlib import Path

# matplotlib is used for generating plots
import matplotlib
# numpy handles numerical arrays and random number generation
import numpy as np
# pandas handles tabular data structures (DataFrames)
import pandas as pd
# scipy.stats gives us the statistical tests like t-tests
from scipy import stats

# Use 'Agg' backend so Matplotlib doesn't try to open a GUI window
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# --- CONSTANTS ---
# SEED ensures reproducibility of our random synthetic data
SEED = 42
# N_PER_GROUP is the sample size for each treatment method
N_PER_GROUP = 12
# TREATMENTS are the three different packing methods being tested
TREATMENTS = ("Standard", "Guided", "Automated")
# TRUE_MEANS are the underlying population means for our synthetic data
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
# SIGMA is the true population standard deviation (assumed equal across groups)
SIGMA = 3.2
# ALPHA is our standard significance level
ALPHA = 0.05
# DIR_FIGURES is the directory where we will save the generated plot
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_cycle_times() ---------------------------------------------
def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 12 cycle times for each packing method from seed 42.

    Parameters
    ----------
    seed : int, optional
        The random seed to ensure reproducibility (default is SEED).

    Returns
    -------
    pd.DataFrame
        A DataFrame with two columns: 'method' (categorical string) and
        'cycle_time_seconds' (float).

    Notes
    -----
    This creates three normally distributed samples with known true means
    and the same standard deviation, matching standard ANOVA assumptions.
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)
    frames = []

    # Generate data for each packing method
    for name in TREATMENTS:
        # Sample cycle times from a Normal distribution
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        # Store the samples in a pandas DataFrame
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )

    # Combine all individual DataFrames into one large table
    return pd.concat(frames, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NEW (2) unadjusted_pairwise() -------------------------------------------
def unadjusted_pairwise(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Run every two-sample t test at alpha=0.05 with no multiplicity correction.

    Parameters
    ----------
    sample : pd.DataFrame
        The dataset containing 'method' and 'cycle_time_seconds'.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the pairwise comparisons, mean differences,
        t-statistics, unadjusted p-values, and boolean rejection flags.

    Notes
    -----
    This is what we explicitly try NOT to do in practice when multiple groups
    are involved, because running many unadjusted t-tests inflates the
    Type I error rate (false positive rate) across the family of tests.
    """
    rows = []
    # Generate all unique pairs from the TREATMENTS list
    for left, right in combinations(TREATMENTS, 2):
        # Extract the cycle times for the 'left' group
        a = sample.loc[sample["method"] == left, "cycle_time_seconds"]
        # Extract the cycle times for the 'right' group
        b = sample.loc[sample["method"] == right, "cycle_time_seconds"]

        # Perform an independent two-sample t-test (assuming equal variances)
        t_stat, p_value = stats.ttest_ind(a, b, equal_var=True)
        # Calculate the raw mean difference
        diff = float(a.mean() - b.mean())

        # Store the results for this pair
        rows.append(
            {
                "pair": f"{left} - {right}",
                "mean_diff": diff,
                "t_stat": float(t_stat),
                "p_value": float(p_value),
                "reject": float(p_value) < ALPHA,
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(pairs: pd.DataFrame) -> Path:
    """
    Save unadjusted pairwise mean differences as labeled bars.

    Parameters
    ----------
    pairs : pd.DataFrame
        The tabular results from unadjusted_pairwise().

    Returns
    -------
    Path
        The absolute path to the generated PNG file.

    Notes
    -----
    Visualizing mean differences helps us quickly see which pairs are furthest
    apart, and the annotated p-values show significance.
    """
    output_path = DIR_FIGURES / "tukey_hsd_01_pairwise_unadjusted.png"
    # Hex colors for the bars
    colors = ["#5B8DEF", "#EC2661", "#1A2E51"]

    # Initialize the plot layout
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot the mean differences as a bar chart
    bars = ax.bar(pairs["pair"], pairs["mean_diff"], color=colors, width=0.62)
    # Add a horizontal line at 0 for reference
    ax.axhline(0.0, color="#646464", linewidth=1.0)

    # Decorate axes and titles
    ax.set_ylabel("Mean difference (seconds)")
    ax.set_title("Unadjusted Pairwise Differences")

    # Set y-axis limit dynamically so text annotations fit above bars
    ax.set_ylim(0, float(pairs["mean_diff"].max()) * 1.38)
    # Add a subtle background grid
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Loop over bars to annotate each with its p-value and rejection status
    for bar, p_value, reject in zip(bars, pairs["p_value"], pairs["reject"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # Center text horizontally on the bar
            height + 0.22,                      # Position text slightly above the bar
            f"p={p_value:.4f}\n{'reject' if reject else 'retain'}",
            ha="center",
            fontsize=8,
            fontweight="bold",
        )

    # Optimize layout and save the plot
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    # Close the figure to free up memory
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the synthetic cycle time dataset
    sample = build_cycle_times()
    # 2. Run unadjusted pairwise tests on the sample
    pairs = unadjusted_pairwise(sample)
    # 3. Create and save a bar chart of the results
    figure_path = save_figure(pairs)

    print("================================================================")
    print("LESSON 45 - STEP 1: UNADJUSTED PAIRWISE t")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Number of pairwise tests        : {len(pairs)}")
    print(f"Unadjusted alpha                : {ALPHA:.2f}")
    # Print out each test result
    for _, row in pairs.iterrows():
        print(
            f"{row['pair']:<24} : diff={row['mean_diff']:.6f}, "
            f"t={row['t_stat']:.6f}, p={row['p_value']:.6f}, "
            f"reject={bool(row['reject'])}"
        )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

