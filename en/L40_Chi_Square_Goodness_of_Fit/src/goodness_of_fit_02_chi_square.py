"""
Lesson 40 - Step 2: Chi-Square Goodness-of-Fit Statistic
========================================================

THE RECIPE
----------
1. chi_square_contributions(): Calculate the squared difference between observed and expected counts, divided by expected counts, for each category: (O - E)^2 / E.
2. goodness_of_fit_test(): Sum the contributions to get the Chi-Square statistic. Determine the degrees of freedom (k - 1) and calculate the right-tailed p-value.
3. save_figure(): Visualize the contribution of each category to the total Chi-Square statistic.

Context:
We continue with the fully synthetic support desk data from Step 1. We claimed the ticket mix is 40% phone, 30% chat, 20% email, and 10% app. Now, we actually test this claim (H0) by calculating the Chi-Square Goodness-of-Fit statistic. If our observed sample is very different from the hypothesized mix, the test statistic will be large, and the p-value small, leading us to reject H0.

How to read this file:
- For an OOP-minded student, consider `chi_square_contributions()` as a transformer that computes per-category residuals, and `goodness_of_fit_test()` as the aggregator that combines them into a single test object containing the statistic and p-value.
- We compare our manual calculation against `scipy.stats.chisquare` to verify our understanding of the underlying math.
- The same n = 200 synthetic ticket counts are rebuilt from constants. No earlier lesson script is imported to keep this script self-contained.

Run it:
    uv run goodness_of_fit_02_chi_square.py
"""

from pathlib import Path

# Use the Agg backend for matplotlib, enabling plotting without a graphical display
import matplotlib
import numpy as np
# scipy.stats provides functions for statistical distributions and tests
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# SEED: Fixed seed for reproducibility
SEED = 42
# N: Total sample size (200 tickets)
N = 200
# CATEGORIES: The four ticket types
CATEGORIES = ("Phone", "Chat", "Email", "App")
# HYPOTHESIZED: The claimed probabilities under H0
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
# OBSERVED: The observed counts in our sample
OBSERVED = np.array([100, 50, 30, 20], dtype=float)
# ALPHA: The significance level for our hypothesis test (5%)
ALPHA = 0.05

# DIR_FIGURES: Path to the directory where we will save our charts
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Create the directory if it does not exist yet
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) chi_square_contributions() --------------------------------------
def chi_square_contributions(observed: np.ndarray, expected: np.ndarray) -> np.ndarray:
    """
    Return the four (O - E)^2 / E terms.

    Parameters
    ----------
    observed : np.ndarray
        The actual counts observed in the sample data.
    expected : np.ndarray
        The theoretical counts expected if the null hypothesis is true.

    Returns
    -------
    np.ndarray
        An array containing the computed contribution of each category
        to the total Chi-Square statistic.

    Notes
    -----
    This formula penalizes categories where the observation deviates strongly
    from the expectation, relative to the size of that expectation.
    """
    # Calculate per-category contribution: (Observed - Expected)^2 / Expected
    return (observed - expected) ** 2 / expected
# ------------------------------------------------------------------------------


# --- NEW (2) goodness_of_fit_test() ------------------------------------------
def goodness_of_fit_test(observed: np.ndarray, expected: np.ndarray) -> dict[str, float]:
    """
    Chi-square GOF test with df = number of categories minus 1.

    Parameters
    ----------
    observed : np.ndarray
        The actual counts observed in the sample data.
    expected : np.ndarray
        The theoretical counts expected under the null hypothesis (H0).

    Returns
    -------
    dict[str, float]
        A dictionary containing the test results:
        - "chi2": The manual computed Chi-Square test statistic.
        - "df": The degrees of freedom (k - 1).
        - "p_value": The manual right-tailed p-value.
        - "scipy_chi2": The statistic computed via scipy.stats.chisquare.
        - "scipy_p": The p-value computed via scipy.stats.chisquare.
        - "critical": The critical value of chi2 at the alpha level.

    Notes
    -----
    The degrees of freedom for a simple Goodness-of-Fit test is the number of
    categories minus 1 (k - 1) because the sum of expected counts must equal
    the sum of observed counts. We compute the p-value using the survival
    function (`sf`) of the chi-square distribution.
    """
    # 1. Compute individual cell contributions
    contributions = chi_square_contributions(observed, expected)
    # 2. Sum them to obtain the overall chi-square test statistic
    chi2 = float(np.sum(contributions))
    # 3. Calculate degrees of freedom (k categories minus 1)
    df = observed.size - 1

    # 4. Compute the p-value manually using the survival function (1 - CDF)
    p_value = float(stats.chi2.sf(chi2, df))

    # 5. Compute the same values using scipy's built-in chisquare function for verification
    scipy_test = stats.chisquare(observed, expected)

    return {
        "chi2": chi2,
        "df": float(df),
        "p_value": p_value,
        "scipy_chi2": float(scipy_test.statistic),
        "scipy_p": float(scipy_test.pvalue),
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),  # Percent point function (inverse of CDF)
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(contributions: np.ndarray) -> Path:
    """
    Bar chart of each category's contribution to chi-square.

    Parameters
    ----------
    contributions : np.ndarray
        An array of individual (O - E)^2 / E values per category.

    Returns
    -------
    Path
        The absolute path to the saved PNG figure.

    Notes
    -----
    This visualization helps identify which categories deviate most from the
    hypothesized model. Large bars indicate large discrepancies.
    """
    output_path = DIR_FIGURES / "goodness_of_fit_02_chi_square.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot each category's contribution
    bars = ax.bar(CATEGORIES, contributions, color=["#EC2661", "#5B8DEF", "#1A2E51", "#F4A6B8"])

    # Format axes and titles
    ax.set_ylabel("(O - E)^2 / E")
    ax.set_title("Chi-Square Contributions, df = 3")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Add text labels on top of each bar showing the exact contribution value
    for bar, value in zip(bars, contributions):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.08,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )

    # Finalize layout and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Compute expected counts (E = n * p)
    expected = N * HYPOTHESIZED
    # 2. Compute individual contributions to chi2
    contributions = chi_square_contributions(OBSERVED, expected)
    # 3. Perform the full Goodness-of-Fit hypothesis test
    test = goodness_of_fit_test(OBSERVED, expected)

    # 4. Make a decision: reject H0 if p-value < alpha, else do not reject
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"

    # 5. Save the contributions plot
    figure_path = save_figure(contributions)

    # Output the exact required console log format
    print("================================================================")
    print("LESSON 40 - STEP 2: CHI-SQUARE GOODNESS OF FIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Hypotheses                      : H0: mix = (0.40, 0.30, 0.20, 0.10)")
    print(
        "Cell contributions              : "
        + ", ".join(f"{value:.6f}" for value in contributions)
    )
    print(f"Chi-square statistic            : {test['chi2']:.6f}")
    print(f"Degrees of freedom k-1          : {int(test['df'])}")
    print(f"Right-tailed p-value (manual)   : {test['p_value']:.6f}")
    print(f"Right-tailed p-value (scipy)    : {test['scipy_p']:.6f}")
    print(f"Critical chi2* (alpha = 0.05)   : {test['critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

