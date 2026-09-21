"""
Lesson 44 - Step 3: The F Test Does Not Name a Pair
===================================================

THE RECIPE
----------
Start from one_way_anova_02_ss_ms_table.py, then introduce:
    1. f_oneway_test()       scipy F statistic and p-value
    2. pairwise_mean_gaps()  three mean differences with no pair test
    3. save_figure()         observed F on the F distribution

Context:
--------
Limit: a significant F does not say which pair differs. Lesson 45 organizes
that next question as Tukey HSD.

To an OOP Python student, the F-test returns a single boolean: `is_different(groups)`.
If it returns `True`, we know *at least one* group is different, but the F-test
does not tell us *which* one(s). You can think of the F-test as an overall health
check (an 'omnibus' test). If it flags an issue, you still need to investigate
further (post-hoc tests like Tukey HSD) to find out which specific pairs of groups
are causing the difference.

How to read this file:
----------------------
1. `f_oneway_test()`: Runs the F-test using `scipy.stats` to get p-values easily.
2. `pairwise_mean_gaps()`: Computes the gaps between means without statistical testing.
3. `save_figure()`: Plots the F-distribution and the mean gaps.

Run it:
-------
    uv run en/L44_One_Way_ANOVA/src/one_way_anova_03_f_test_limit.py
"""

# Path manipulations
from pathlib import Path

# Scientific and plotting libraries
import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

# Configure matplotlib for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Global Constants
SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = N_PER_GROUP * K_GROUPS
TREATMENTS = ("Standard", "Guided", "Automated")
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
SIGMA = 3.2
# Alpha is the significance level for our hypothesis test
ALPHA = 0.05
# Directory to save generated figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild the three synthetic cycle-time samples from seed 42.

    Parameters
    ----------
    seed : int, optional
        Random seed for generation.

    Returns
    -------
    pd.DataFrame
        Simulated data frame.
    """
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)


def anova_pieces(sample: pd.DataFrame) -> dict[str, float]:
    """
    Return the manual ANOVA table pieces used to check scipy.

    Parameters
    ----------
    sample : pd.DataFrame
        Simulated data frame.

    Returns
    -------
    dict[str, float]
        Dictionary with manual F statistic and degrees of freedom.
    """
    values = sample["cycle_time_seconds"].to_numpy()
    grand_mean = float(values.mean())
    ssb = 0.0
    sse = 0.0
    for name in TREATMENTS:
        group = sample.loc[
            sample["method"] == name, "cycle_time_seconds"
        ].to_numpy()
        group_mean = float(group.mean())
        ssb += N_PER_GROUP * (group_mean - grand_mean) ** 2
        sse += float(np.sum((group - group_mean) ** 2))
    df_between = K_GROUPS - 1
    df_error = N_TOTAL - K_GROUPS
    msb = ssb / df_between
    mse = sse / df_error
    return {
        "f_manual": msb / mse,
        "df_between": df_between,
        "df_error": df_error,
    }


# --- NEW (1) f_oneway_test() -------------------------------------------------
def f_oneway_test(sample: pd.DataFrame) -> dict[str, float]:
    """
    Compute scipy.stats.f_oneway and the F critical value.

    Parameters
    ----------
    sample : pd.DataFrame
        DataFrame of cycle times.

    Returns
    -------
    dict[str, float]
        Dictionary containing the computed test statistic (f_stat), p_value,
        critical F value (f_crit), degrees of freedom, and rejection boolean.

    Notes
    -----
    Instead of calculating MSB and MSE manually, we can use scipy.stats.f_oneway.
    It returns the F-statistic and the p-value directly. We compute f_crit using
    the Percent Point Function (ppf), which is the inverse of the CDF, to find
    the threshold for our alpha. If f_stat > f_crit, we reject the null hypothesis.
    """
    # Group the data into a list of arrays for scipy
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]

    # Unpack the list into separate arguments using the * operator
    f_stat, p_value = stats.f_oneway(*groups)

    # Calculate degrees of freedom
    df_between = K_GROUPS - 1
    df_error = N_TOTAL - K_GROUPS

    # Find the critical F value at the given alpha level
    f_crit = float(stats.f.ppf(1.0 - ALPHA, df_between, df_error))

    return {
        "f_stat": float(f_stat),
        "p_value": float(p_value),
        "f_crit": f_crit,
        "df_between": df_between,
        "df_error": df_error,
        "reject": float(f_stat) > f_crit,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) pairwise_mean_gaps() --------------------------------------------
def pairwise_mean_gaps(sample: pd.DataFrame) -> dict[str, float]:
    """
    Report the three mean differences without testing any pair.

    Parameters
    ----------
    sample : pd.DataFrame
        DataFrame of cycle times.

    Returns
    -------
    dict[str, float]
        A dictionary containing pairwise differences between means, and the
        individual group means themselves.

    Notes
    -----
    This calculates the simple arithmetic differences between the sample means.
    However, these gaps alone do NOT tell us if a specific pair is statistically
    different. That's the limitation of the F-test - it tells us there is a
    difference *somewhere*, but we can't just pick the biggest gap and assume
    it's significant without further statistical testing (post-hoc tests).
    """
    # Calculate the mean for each group
    means = {
        name: float(
            sample.loc[sample["method"] == name, "cycle_time_seconds"].mean()
        )
        for name in TREATMENTS
    }

    # Calculate pairwise differences and return with means
    return {
        "standard_minus_guided": means["Standard"] - means["Guided"],
        "standard_minus_automated": means["Standard"] - means["Automated"],
        "guided_minus_automated": means["Guided"] - means["Automated"],
        "mean_standard": means["Standard"],
        "mean_guided": means["Guided"],
        "mean_automated": means["Automated"],
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(test: dict[str, float], gaps: dict[str, float]) -> Path:
    """
    Mark the observed F on the null F density and show unlabeled gaps.

    Parameters
    ----------
    test : dict[str, float]
        Dictionary of F-test results from f_oneway_test().
    gaps : dict[str, float]
        Dictionary of pairwise gaps from pairwise_mean_gaps().

    Returns
    -------
    Path
        Path to the saved figure.

    Notes
    -----
    The left plot shows the F-distribution under the null hypothesis. The area
    to the right of the critical value is the rejection region (alpha = 0.05).
    Our observed F falls in this region, so we reject H0.
    The right plot shows the gaps between means, reinforcing that we don't yet
    know which of these gaps is statistically significant.
    """
    output_path = DIR_FIGURES / "one_way_anova_03_f_test_limit.png"

    # Define x-axis range for the F-distribution
    x = np.linspace(0.0, 20.0, 400)
    # Get the probability density function (PDF) for the F-distribution
    y = stats.f.pdf(x, test["df_between"], test["df_error"])

    # Create a 1x2 subplot figure
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))

    # Left subplot: The F-Distribution
    axes[0].plot(x, y, color="#1A2E51", linewidth=2.0)

    # Plot the observed F-statistic line
    axes[0].axvline(
        test["f_stat"],
        color="#EC2661",
        linewidth=2.0,
        label=f"Observed F = {test['f_stat']:.3f}",
    )

    # Plot the critical F-statistic line
    axes[0].axvline(
        test["f_crit"],
        color="#5B8DEF",
        linestyle="--",
        linewidth=1.5,
        label=f"F crit = {test['f_crit']:.3f}",
    )

    # Shade the rejection region
    axes[0].fill_between(
        x[x >= test["f_crit"]],
        y[x >= test["f_crit"]],
        color="#EC2661",
        alpha=0.18,
    )

    axes[0].set_xlabel("F")
    axes[0].set_ylabel("Density")
    axes[0].set_title("Significant F, Still One Omnibus Test")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    # Right subplot: Bar chart of pairwise gaps
    gap_labels = [
        "Standard\n- Guided",
        "Standard\n- Automated",
        "Guided\n- Automated",
    ]
    gap_values = [
        gaps["standard_minus_guided"],
        gaps["standard_minus_automated"],
        gaps["guided_minus_automated"],
    ]
    colors = ["#5B8DEF", "#EC2661", "#1A2E51"]

    bars = axes[1].bar(gap_labels, gap_values, color=colors, width=0.62)

    # Reference line at zero gap
    axes[1].axhline(0.0, color="#646464", linewidth=1.0)

    axes[1].set_ylabel("Mean difference (seconds)")
    axes[1].set_title("F Does Not Identify Which Pair Differs")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate bars with the exact gap values
    for bar, value in zip(bars, gap_values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Simulate data
    sample = build_cycle_times()
    # 2. Get manual ANOVA pieces for verification
    pieces = anova_pieces(sample)
    # 3. Perform F-test using scipy
    test = f_oneway_test(sample)
    # 4. Calculate pairwise gaps
    gaps = pairwise_mean_gaps(sample)
    # 5. Generate and save visualizations
    figure_path = save_figure(test, gaps)

    # Output results to console, exactly as required
    print("================================================================")
    print("LESSON 44 - STEP 3: F TEST LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Manual F                        : {pieces['f_manual']:.6f}")
    print(f"scipy f_oneway F                : {test['f_stat']:.6f}")
    print(f"p-value                         : {test['p_value']:.6e}")
    print(f"F critical (alpha=0.05)         : {test['f_crit']:.6f}")
    print(f"Reject H0: equal means          : {bool(test['reject'])}")
    print(f"Mean Standard                   : {gaps['mean_standard']:.6f}")
    print(f"Mean Guided                     : {gaps['mean_guided']:.6f}")
    print(f"Mean Automated                  : {gaps['mean_automated']:.6f}")
    print(
        "Standard - Guided               : "
        f"{gaps['standard_minus_guided']:.6f}"
    )
    print(
        "Standard - Automated            : "
        f"{gaps['standard_minus_automated']:.6f}"
    )
    print(
        "Guided - Automated              : "
        f"{gaps['guided_minus_automated']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

