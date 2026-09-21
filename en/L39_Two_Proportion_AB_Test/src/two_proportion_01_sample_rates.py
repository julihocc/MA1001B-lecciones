"""
Lesson 39 - Step 1: Two Sample Conversion Rates
===============================================
THE RECIPE
Start from an empty file, then introduce:
    1. sample_rates()        Returns baseline proportions for arm A and arm B
    2. pooled_proportion()   Calculates the pooled proportion under the null
    3. save_figure()         Plots the empirical conversion rates

Context:
A fully synthetic A/B test of a checkout prompt records nA = 400 visitors
and xA = 72 conversions on version A, versus nB = 410 visitors and xB = 61
conversions on version B. The samples are independent, not paired.

When comparing two independent proportions, we usually want to know if they
are statistically different. We start by computing the sample proportions,
and then under the null hypothesis (H0: pA = pB), we pool the successes and
trials to find the overall 'pooled proportion'.

How to read this file:
Read `sample_rates` to see how we extract basic metrics.
Read `pooled_proportion` to see the logic of the null hypothesis in action:
if there's no difference between A and B, they are just two samples from
the same underlying binomial distribution.

Run it:
    python two_proportion_01_sample_rates.py
"""

from pathlib import Path

import matplotlib
import numpy as np

# Use the Agg backend so matplotlib doesn't require a GUI (useful for server scripts).
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Constants for our synthetic experiment ---
# Seed for any pseudo-random operations (unused here but standard in ML/stats).
SEED = 42

# Version A data
N_A = 400  # Number of visitors for version A
X_A = 72   # Number of conversions for version A

# Version B data
N_B = 410  # Number of visitors for version B
X_B = 61   # Number of conversions for version B

# Target directory for saving our plots
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) sample_rates() --------------------------------------------------
def sample_rates() -> dict[str, float]:
    """
    Return sample sizes, conversion counts, and sample proportions.

    Returns:
        dict[str, float]: A dictionary containing:
            - 'n_a': Sample size for version A.
            - 'x_a': Conversions for version A.
            - 'n_b': Sample size for version B.
            - 'x_b': Conversions for version B.
            - 'phat_a': Sample proportion (rate) for version A.
            - 'phat_b': Sample proportion (rate) for version B.
            - 'diff': Difference in proportions (phat_a - phat_b).

    Notes:
        These are the raw empirical metrics before any statistical testing.
    """
    return {
        "n_a": float(N_A),
        "x_a": float(X_A),
        "n_b": float(N_B),
        "x_b": float(X_B),
        "phat_a": X_A / N_A,
        "phat_b": X_B / N_B,
        "diff": X_A / N_A - X_B / N_B,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) pooled_proportion() ---------------------------------------------
def pooled_proportion(x_a: int = X_A, n_a: int = N_A, x_b: int = X_B, n_b: int = N_B) -> dict[str, float]:
    """
    Pool the two samples under H0: pA = pB.

    Parameters:
        x_a (int): Number of successes in sample A. Defaults to X_A.
        n_a (int): Number of trials in sample A. Defaults to N_A.
        x_b (int): Number of successes in sample B. Defaults to X_B.
        n_b (int): Number of trials in sample B. Defaults to N_B.

    Returns:
        dict[str, float]: A dictionary containing:
            - 'p_pool': Pooled proportion.
            - 'n_total': Combined sample size.
            - 'x_total': Combined successes.
            - 'np_a': Expected successes in A under H0.
            - 'nq_a': Expected failures in A under H0.
            - 'np_b': Expected successes in B under H0.
            - 'nq_b': Expected failures in B under H0.

    Notes:
        Under the null hypothesis (H0), there is no difference between the groups,
        so we estimate the single common success probability by combining all
        data: (Total Successes) / (Total Trials).
    """
    # Combine successes and divide by combined trials
    p_pool = (x_a + x_b) / (n_a + n_b)

    return {
        "p_pool": float(p_pool),
        "n_total": float(n_a + n_b),
        "x_total": float(x_a + x_b),
        "np_a": float(n_a * p_pool),
        "nq_a": float(n_a * (1.0 - p_pool)),
        "np_b": float(n_b * p_pool),
        "nq_b": float(n_b * (1.0 - p_pool)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(rates: dict[str, float]) -> Path:
    """
    Compare the two observed conversion rates in a bar chart.

    Parameters:
        rates (dict[str, float]): The dictionary returned by sample_rates().

    Returns:
        Path: The absolute path where the figure was saved.

    Notes:
        This visualizes the empirical proportions (phat_a and phat_b).
        Does not imply statistical significance on its own.
    """
    # Output file path
    output_path = DIR_FIGURES / "two_proportion_01_sample_rates.png"

    # Prepare data for plotting
    labels = ["Version A", "Version B"]
    values = [rates["phat_a"], rates["phat_b"]]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot bars with specific colors and width
    bars = ax.bar(labels, values, color=["#5B8DEF", "#EC2661"], width=0.55)

    # Configure axes and title
    ax.set_ylabel("Conversion rate")
    ax.set_title("Synthetic A/B Test: nA = 400, nB = 410")
    ax.set_ylim(0, 0.26)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate bars with counts and proportions
    for bar, value, count, n in zip(
        bars, values, [int(rates["x_a"]), int(rates["x_b"])], [int(rates["n_a"]), int(rates["n_b"])]
    ):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{count}/{n}\n{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )

    # Save and clean up
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Run the core logic
    rates = sample_rates()
    pooled = pooled_proportion()
    figure_path = save_figure(rates)

    # Output results identically to the unannotated version
    print("================================================================")
    print("LESSON 39 - STEP 1: TWO SAMPLE CONVERSION RATES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Version A nA, xA                : {int(rates['n_a'])}, {int(rates['x_a'])}")
    print(f"Version B nB, xB                : {int(rates['n_b'])}, {int(rates['x_b'])}")
    print(f"Sample proportion p-hat A       : {rates['phat_a']:.6f}")
    print(f"Sample proportion p-hat B       : {rates['phat_b']:.6f}")
    print(f"Difference p-hat A minus B      : {rates['diff']:.6f}")
    print(f"Pooled proportion under H0      : {pooled['p_pool']:.6f}")
    print(f"nA * p-pool                     : {pooled['np_a']:.6f}")
    print(f"nB * p-pool                     : {pooled['np_b']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

