"""
Lesson 35 - Step 3: Small n plus Skew Makes the t p-Value Fragile
================================================================
THE RECIPE
----------
Start from t_test_mean_02_two_sided_pvalue.py, then introduce:
    1. skewed_small_sample()     n = 8 right-skewed pack times
    2. leave_one_out_pvalues()   how one observation moves the p-value
    3. save_figure()             full-sample p versus leave-one-out p

The n = 40 approximately symmetric sample is rebuilt only as a robustness
contrast. The limit is the rushed n = 8 draw: a long delay inflates s and
the two-sided p-value is no longer a stable decision input.

Context:
--------
The t-test assumes the underlying population is normally distributed. While
large sample sizes (like n=40) are robust to deviations from normality due
to the Central Limit Theorem, small sample sizes (like n=8) are very fragile.
A single outlier or extreme skewness can inflate the standard deviation, shrink
the t-statistic, and dramatically alter the p-value.

How to read this file:
----------------------
Notice how we combine two distributions in `skewed_small_sample` to simulate
a right-skewed dataset (typical operations plus one large delay). Then, in
`leave_one_out_pvalues`, we loop through the sample, temporarily deleting one
observation at a time using `np.delete`, and recalculating the p-value. This
"leave-one-out" technique is a great diagnostic for sensitivity analysis.

Run it:
-------
    python t_test_mean_03_small_n_skew_limit.py
"""

from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats provides testing functions like ttest_1samp and shapiro
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
SEED = 42
N = 40
N_SMALL = 8
MU0 = 50.0
PROCESS_MEAN = 52.0
PROCESS_SD = 6.0
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pack_times(seed: int = SEED) -> np.ndarray:
    """Draw n = 40 synthetic pack-out cycle times in minutes."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=PROCESS_MEAN, scale=PROCESS_SD, size=N)


# --- NEW (1) skewed_small_sample() -------------------------------------------
def skewed_small_sample(seed: int = SEED) -> np.ndarray:
    """
    Draw n = 8 times: seven typical packs plus one long delay.

    Parameters
    ----------
    seed : int, optional
        The random seed to ensure reproducibility. Defaults to SEED.

    Returns
    -------
    np.ndarray
        A 1-dimensional array containing N_SMALL (8) cycle times.

    Notes
    -----
    We construct this by combining 7 normal observations ("bulk") and 1 highly
    skewed observation from a lognormal distribution ("tail"). This perfectly
    simulates a process that is mostly stable but occasionally experiences a
    severe delay.
    """
    rng = np.random.default_rng(seed)
    # Generate 7 typical observations
    bulk = rng.normal(loc=48.0, scale=3.5, size=N_SMALL - 1)
    # Generate 1 extreme outlier (long delay)
    tail = rng.lognormal(mean=4.5, sigma=0.25, size=1)

    # Concatenate them into a single 1D array
    return np.concatenate([bulk, tail])
# ------------------------------------------------------------------------------


# --- NEW (2) leave_one_out_pvalues() -----------------------------------------
def leave_one_out_pvalues(times: np.ndarray, mu0: float = MU0) -> dict[str, object]:
    """
    Compute the full-sample t test and each leave-one-out p-value.

    Parameters
    ----------
    times : np.ndarray
        The array of sampled cycle times.
    mu0 : float, optional
        The hypothesized population mean. Defaults to MU0.

    Returns
    -------
    dict[str, object]
        A comprehensive dictionary containing descriptive stats, test results,
        and the leave-one-out p-value array.

    Notes
    -----
    A robust p-value should not change drastically if one data point is removed.
    Here we recalculate the p-value n times. If removing just one specific
    observation crosses the alpha threshold, our conclusion is dangerously fragile.
    We also run a Shapiro-Wilk test to formally check for non-normality.
    """
    # 1. Full sample test
    full = stats.ttest_1samp(times, mu0)

    # 2. Leave-one-out analysis
    loo_p = []
    for i in range(times.size):
        # Delete the item at index i, returning a new smaller array
        reduced = np.delete(times, i)
        # Calculate and store the p-value for this reduced sample
        loo_p.append(float(stats.ttest_1samp(reduced, mu0).pvalue))

    # Convert list back to numpy array for easier manipulation
    loo = np.array(loo_p)

    return {
        "xbar": float(np.mean(times)),
        "sample_sd": float(np.std(times, ddof=1)),
        "skewness": float(stats.skew(times)),
        "t_stat": float(full.statistic),
        "p_value": float(full.pvalue),
        # Shapiro-Wilk test for normality. Small p-value means data is non-normal.
        "shapiro_p": float(stats.shapiro(times).pvalue),
        "loo_pvalues": loo,
        "min_loo_p": float(np.min(loo)),
        "max_loo_p": float(np.max(loo)),
        # Find which observation was the highest (the outlier)
        "dropped_index": int(np.argmax(times)),
        "dropped_value": float(np.max(times)),
        # Find the p-value specifically when that outlier was removed
        "p_without_max": float(loo[int(np.argmax(times))]),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(times: np.ndarray, results: dict[str, object]) -> Path:
    """
    Contrast the n = 8 histogram with leave-one-out p-values.

    Parameters
    ----------
    times : np.ndarray
        The small skewed sample.
    results : dict[str, object]
        The analysis results from leave_one_out_pvalues().

    Returns
    -------
    Path
        The absolute path to the saved dual-pane figure.

    Notes
    -----
    This creates a side-by-side plot.
    Left pane: Histogram of the sample to visually identify the skew.
    Right pane: Bar chart showing how the p-value changes when each data point
    is omitted. The bar for the deleted outlier is highlighted.
    """
    output_path = DIR_FIGURES / "t_test_mean_03_small_n_skew_limit.png"
    loo = np.asarray(results["loo_pvalues"], dtype=float)

    # Create a figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6))

    # --- Left subplot: Histogram ---
    axes[0].hist(times, bins=6, color="#F4A6B8", edgecolor="#1A2E51")
    axes[0].axvline(MU0, color="#646464", linestyle="--", linewidth=1.5,
                    label="H0 mean = 50")
    axes[0].axvline(float(results["xbar"]), color="#EC2661", linewidth=1.6,
                    label=f"x-bar = {float(results['xbar']):.1f}")
    axes[0].set_xlabel("Cycle time (minutes)")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("n = 8, Right-Skewed Pack Times")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    # --- Right subplot: Leave-one-out bar chart ---
    # Highlight the specific bar where the outlier was dropped
    colors = ["#EC2661" if i == int(results["dropped_index"]) else "#1A2E51"
              for i in range(len(loo))]

    axes[1].bar(np.arange(1, len(loo) + 1), loo, color=colors, width=0.7)

    # Horizontal line showing what the p-value is WITH the full sample
    axes[1].axhline(float(results["p_value"]), color="#5B8DEF", linestyle="-",
                    linewidth=1.6, label=f"full p = {float(results['p_value']):.3f}")
    # Horizontal line showing the alpha rejection threshold
    axes[1].axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.2,
                    label="alpha = 0.05")

    axes[1].set_xlabel("Observation dropped")
    axes[1].set_ylabel("Two-sided p-value")
    axes[1].set_title("Leave-One-Out p-Values")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Run the n=40 full sample as a robustness baseline
    large = build_pack_times()
    large_test = stats.ttest_1samp(large, MU0)
    # List comprehension to do leave-one-out on the large sample
    large_loo = [
        float(stats.ttest_1samp(np.delete(large, i), MU0).pvalue)
        for i in range(large.size)
    ]

    # 2. Run the n=8 skewed sample to see fragility
    small = skewed_small_sample()
    results = leave_one_out_pvalues(small)
    figure_path = save_figure(small, results)

    print("================================================================")
    print("LESSON 35 - STEP 3: SMALL n PLUS SKEW LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"n = 40 two-sided p-value        : {float(large_test.pvalue):.6f}")
    print(f"n = 40 leave-one-out p min      : {min(large_loo):.6f}")
    print(f"n = 40 leave-one-out p max      : {max(large_loo):.6f}")
    print(f"n = 8 sample size               : {N_SMALL}")
    print(f"n = 8 sample mean               : {float(results['xbar']):.6f}")
    print(f"n = 8 sample s                  : {float(results['sample_sd']):.6f}")
    print(f"n = 8 skewness                  : {float(results['skewness']):.6f}")
    print(f"n = 8 Shapiro-Wilk p-value      : {float(results['shapiro_p']):.6f}")
    print(f"n = 8 t statistic               : {float(results['t_stat']):.6f}")
    print(f"n = 8 two-sided p-value         : {float(results['p_value']):.6f}")
    print(f"Longest delay (minutes)         : {float(results['dropped_value']):.6f}")
    print(f"p-value without the longest     : {float(results['p_without_max']):.6f}")
    print(f"Leave-one-out p minimum         : {float(results['min_loo_p']):.6f}")
    print(f"Leave-one-out p maximum         : {float(results['max_loo_p']):.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

