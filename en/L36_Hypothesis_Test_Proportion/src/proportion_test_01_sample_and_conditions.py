"""
Lesson 36 - Step 1: Sample Proportion and Normal Conditions
===========================================================
THE RECIPE
Start from a blank script, then introduce:
    1. sample_proportion()    calculates phat from observed count x and sample size n
    2. normal_conditions()    checks np0 >= 5 and n(1-p0) >= 5 under H0
    3. save_figure()          generates a bar chart comparing p0 and phat

Context:
A fully synthetic inbound-inspection process claims that the late-flag
proportion is 10 percent (p0 = 0.10). A sample of n = 200 lots records x = 28 late flags.
Before a z test for a proportion is used, the sampling distribution of the proportion must
be approximately normal. This requires np0 and n(1 - p0) to both exceed 5. Note that
we use p0 (the hypothesized proportion) because the sampling distribution is constructed
under the assumption that the null hypothesis (H0: p = p0) is true.

How to read this file:
This file demonstrates the preliminary steps for a one-proportion z-test.
You will see how to define the hypothesized proportion, compute the sample
proportion, and verify the conditions required to use the normal approximation.
For a student familiar with OOP, consider the parameters (n, x, p0) as state
that would initialize a `ProportionTest` object, and these functions as its
methods.

Run it:
    python proportion_test_01_sample_and_conditions.py
"""

# Import Path for robust, cross-platform file path handling
from pathlib import Path

# matplotlib is used for generating figures
import matplotlib
# numpy is used for numerical operations
import numpy as np

# Use the non-interactive "Agg" backend for matplotlib to generate files without a GUI
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Random seed (reserved for future steps if random sampling is introduced)
SEED = 42
# Sample size: number of lots inspected
N = 200
# Observed number of successes (late flags) in the sample
X_LATE = 28
# Hypothesized population proportion under the null hypothesis (H0)
P0 = 0.10
# Resolve the path to the figures directory relative to this script
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Create the directory if it does not exist
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) sample_proportion() ---------------------------------------------
def sample_proportion(x: int = X_LATE, n: int = N) -> dict[str, float]:
    """
    Return the observed late-flag count and sample proportion.

    Parameters
    ----------
    x : int
        The number of observed successes (late flags) in the sample.
    n : int
        The total sample size.

    Returns
    -------
    dict[str, float]
        A dictionary containing the sample size ('n'), successes ('x'),
        sample proportion ('phat'), and hypothesized proportion ('p0').

    Notes
    -----
    The sample proportion (phat) is an unbiased estimator of the true population proportion.
    """
    # Calculate the sample proportion phat = x / n
    phat = x / n
    return {"n": float(n), "x": float(x), "phat": float(phat), "p0": P0}
# ------------------------------------------------------------------------------


# --- NEW (2) normal_conditions() ---------------------------------------------
def normal_conditions(n: int = N, p0: float = P0) -> dict[str, float]:
    """
    Check the np0 and n(1-p0) conditions under H0.

    Parameters
    ----------
    n : int
        The total sample size.
    p0 : float
        The hypothesized population proportion.

    Returns
    -------
    dict[str, float]
        A dictionary containing the expected successes ('np0'), expected failures
        ('nq0'), and a boolean flag indicating if both are > 5 ('conditions_ok').

    Notes
    -----
    The normal approximation is considered valid if both the expected number of
    successes (np0) and failures (n(1-p0)) are at least 5. Some textbooks use 10.
    Importantly, we use p0 (not phat) because we construct the sampling distribution
    assuming H0 is true.
    """
    # Expected number of successes if H0 is true
    np0 = n * p0
    # Expected number of failures if H0 is true
    nq0 = n * (1.0 - p0)
    return {
        "np0": float(np0),
        "nq0": float(nq0),
        "conditions_ok": float(np0 > 5.0 and nq0 > 5.0),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """
    Compare the hypothesized proportion with the sample proportion.

    Parameters
    ----------
    summary : dict[str, float]
        Dictionary from sample_proportion containing 'p0' and 'phat'.

    Returns
    -------
    Path
        The absolute path to the saved figure file.

    Notes
    -----
    This visualizes the gap between our expectation under H0 and the reality
    observed in the sample. A large gap will lead to a small p-value.
    """
    output_path = DIR_FIGURES / "proportion_test_01_sample_and_conditions.png"
    # Labels for the bar chart
    labels = ["H0 proportion p0", "Sample proportion phat"]
    # Values to plot
    values = [summary["p0"], summary["phat"]]
    # Colors for the bars: blue for H0, pink for sample
    colors = ["#1A2E51", "#EC2661"]

    # Initialize the plot with specific dimensions
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)

    # Configure axes and title
    ax.set_ylabel("Proportion late")
    ax.set_title("n = 200 Lots; x = 28 Late Flags")
    ax.set_ylim(0, 0.22)
    # Add a subtle grid to help with visual estimation
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Add text labels on top of each bar
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )

    fig.tight_layout()
    # Save the figure
    fig.savefig(output_path, dpi=170)
    # Close the figure to free memory
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Execute the recipe steps
    summary = sample_proportion()
    conditions = normal_conditions()
    figure_path = save_figure(summary)

    # Print the lesson summary and results to stdout
    print("================================================================")
    print("LESSON 36 - STEP 1: SAMPLE PROPORTION AND CONDITIONS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {int(summary['n'])}")
    print(f"Late-flag count x               : {int(summary['x'])}")
    print(f"Sample proportion phat          : {summary['phat']:.6f}")
    print(f"Hypothesized proportion p0      : {summary['p0']:.6f}")
    print(f"np0 under H0                    : {conditions['np0']:.6f}")
    print(f"n(1-p0) under H0                : {conditions['nq0']:.6f}")
    print(
        "Normal conditions np0, nq0 > 5  : "
        f"{'yes' if conditions['conditions_ok'] else 'no'}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

