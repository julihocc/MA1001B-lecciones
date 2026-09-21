"""
Lesson 40 - Step 3: Expected Count below 5 Makes the Approximation Poor
=======================================================================

THE RECIPE
----------
1. small_sample_counts(): Analyze a small sample size (n=20) where some expected counts fall below the standard threshold of 5.
2. monte_carlo_pvalue(): Since the Chi-Square approximation is poor for small expected counts, use a Monte Carlo simulation (drawing from a multinomial distribution) to estimate the true p-value.
3. save_figure(): Visualize the expected counts and highlight those that violate the E >= 5 guideline.

Context:
The Chi-Square Goodness-of-Fit test relies on a large-sample approximation. A common rule of thumb is that all expected counts must be at least 5. When n is small (e.g., n = 20), expected counts in rare categories (like 'App' at 10%) can drop below 5 (E = 2).
When E is very small, the test statistic (O - E)^2 / E becomes highly sensitive to small changes in O (e.g., jumping from O=0 to O=1), making the theoretical Chi-Square distribution a poor fit for the actual sampling distribution.

How to read this file:
- For a student who knows Python OOP, think of `monte_carlo_pvalue()` as bypassing the theoretical model (`stats.chi2`) and instead physically simulating thousands of datasets to empirically measure the p-value.
- We deliberately set up a failing scenario (n=20) to demonstrate what happens when the E >= 5 assumption is violated.
- The Monte Carlo simulation draws from `numpy.random.default_rng().multinomial()`, acting as our synthetic data generator.

Run it:
    uv run goodness_of_fit_03_small_expected_limit.py
"""

from pathlib import Path

# Use the Agg backend for matplotlib, avoiding GUI requirements
import matplotlib
import numpy as np
# scipy.stats provides the theoretical chi-square distribution functions
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# SEED: Fixed seed to ensure our Monte Carlo simulation yields exactly the same results every time
SEED = 42
# N_SMALL: A deliberately small sample size to trigger the E < 5 condition
N_SMALL = 20
# N_SIM: Number of simulated datasets to generate for the Monte Carlo p-value
N_SIM = 20_000
# CATEGORIES: The four ticket types
CATEGORIES = ("Phone", "Chat", "Email", "App")
# HYPOTHESIZED: The claimed probabilities under H0
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
# OBSERVED_SMALL: Synthetic observed counts for n=20
OBSERVED_SMALL = np.array([14, 4, 2, 0], dtype=float)
# ALPHA: The significance level
ALPHA = 0.05

# DIR_FIGURES: Path to the directory where we will save our charts
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) small_sample_counts() -------------------------------------------
def small_sample_counts() -> dict[str, np.ndarray | float]:
    """
    n = 20 ticket mix with two expected counts below 5.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, np.ndarray | float]
        A dictionary containing:
        - "observed": A copy of the small sample observed counts.
        - "expected": The expected counts array (E = N_SMALL * p).
        - "contributions": The array of (O - E)^2 / E values.
        - "min_expected": The lowest expected count.
        - "n_cells_below_5": The number of categories where E < 5.
        - "chi2": The total Chi-Square test statistic.

    Notes
    -----
    Because N is only 20, the 'Email' (20%) and 'App' (10%) categories will
    have expected counts of 4 and 2 respectively, violating the E >= 5 rule.
    """
    # Calculate the expected counts E = n * p
    expected = N_SMALL * HYPOTHESIZED
    # Calculate cell contributions
    contributions = (OBSERVED_SMALL - expected) ** 2 / expected

    return {
        "observed": OBSERVED_SMALL.copy(),
        "expected": expected,
        "contributions": contributions,
        "min_expected": float(np.min(expected)),
        "n_cells_below_5": float(np.sum(expected < 5.0)),
        "chi2": float(np.sum(contributions)),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) monte_carlo_pvalue() --------------------------------------------
def monte_carlo_pvalue(observed: np.ndarray, expected: np.ndarray, chi2: float) -> dict[str, float]:
    """
    Simulate multinomial samples under H0 and compare chi-square values.

    Parameters
    ----------
    observed : np.ndarray
        The actual counts observed in the small sample.
    expected : np.ndarray
        The theoretical counts expected under the null hypothesis.
    chi2 : float
        The observed Chi-Square statistic from the sample data.

    Returns
    -------
    dict[str, float]
        A dictionary containing:
        - "p_chi2": The theoretical p-value using the Chi-Square distribution.
        - "p_monte_carlo": The empirical p-value via simulation.
        - "n_sim": The number of simulation iterations.
        - "chi2_app_zero": The contribution of the App cell if O=0.
        - "chi2_app_one": The contribution of the App cell if O=1.

    Notes
    -----
    When expected counts are small, the theoretical Chi-Square distribution
    inaccurately models the true distribution of the test statistic. By repeatedly
    simulating data from the true multinomial distribution, we can calculate a
    more accurate empirical p-value (the proportion of simulated statistics >=
    our observed statistic).
    """
    # Initialize the random number generator with our fixed seed
    rng = np.random.default_rng(SEED)

    # Draw N_SIM samples of size N_SMALL from a multinomial distribution under H0
    draws = rng.multinomial(N_SMALL, HYPOTHESIZED, size=N_SIM)

    # Compute the chi-square statistic for every simulated sample across axis 1 (rows)
    simulated_chi2 = np.sum((draws - expected) ** 2 / expected, axis=1)

    # The Monte Carlo p-value is the fraction of simulations where the statistic >= observed chi2
    p_mc = float(np.mean(simulated_chi2 >= chi2))

    # Calculate the theoretical p-value for comparison
    p_chi2 = float(stats.chi2.sf(chi2, observed.size - 1))

    return {
        "p_chi2": p_chi2,
        "p_monte_carlo": p_mc,
        "n_sim": float(N_SIM),
        # Demonstrate the instability when E is small: a tiny change in O (0 to 1)
        # causes a massive change in the penalty because we divide by E (which is only 2).
        "chi2_app_zero": float((0.0 - expected[-1]) ** 2 / expected[-1]),
        "chi2_app_one": float((1.0 - expected[-1]) ** 2 / expected[-1]),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(expected: np.ndarray) -> Path:
    """
    Highlight expected counts that fall below the E = 5 guideline.

    Parameters
    ----------
    expected : np.ndarray
        The theoretical counts expected under the null hypothesis.

    Returns
    -------
    Path
        The absolute path to the saved PNG figure.

    Notes
    -----
    The plot draws a line at E = 5 and colors the bars red if they fall
    below this threshold, visually indicating the violation of the test's assumptions.
    """
    output_path = DIR_FIGURES / "goodness_of_fit_03_small_expected_limit.png"

    # Color bars red if their expected value is < 5, else dark blue
    colors = ["#EC2661" if value < 5 else "#1A2E51" for value in expected]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(CATEGORIES, expected, color=colors, width=0.62)

    # Draw the E=5 guideline
    ax.axhline(5.0, color="#646464", linestyle="--", linewidth=1.4,
               label="E = 5 guideline")

    # Format axes and titles
    ax.set_ylabel("Expected count")
    ax.set_title("n = 20: Two Expected Counts Fall below 5")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Add text labels on top of each bar
    for bar, value in zip(bars, expected):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.1f}",
            ha="center",
            fontweight="bold",
        )

    # Finalize and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate counts for our problematically small sample
    small = small_sample_counts()

    # 2. Compute theoretical vs Monte Carlo p-values
    mc = monte_carlo_pvalue(small["observed"], small["expected"], small["chi2"])

    # 3. Create the warning plot
    figure_path = save_figure(small["expected"])

    # Output the exact required console log format
    print("================================================================")
    print("LESSON 40 - STEP 3: SMALL EXPECTED COUNT LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Small-sample n                  : {N_SMALL}")
    print("Observed counts                 : 14, 4, 2, 0")
    print(
        "Expected counts                 : "
        + ", ".join(f"{value:.1f}" for value in small["expected"])
    )
    print(f"Cells with E < 5                : {int(small['n_cells_below_5'])}")
    print(f"Minimum expected count          : {small['min_expected']:.6f}")
    print(f"Chi-square statistic            : {small['chi2']:.6f}")
    print(f"Chi-square p-value              : {mc['p_chi2']:.6f}")
    print(f"Monte Carlo p-value             : {mc['p_monte_carlo']:.6f}")
    print(f"App cell contribution if O = 0  : {mc['chi2_app_zero']:.6f}")
    print(f"App cell contribution if O = 1  : {mc['chi2_app_one']:.6f}")
    print(f"Simulated samples               : {int(mc['n_sim'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

