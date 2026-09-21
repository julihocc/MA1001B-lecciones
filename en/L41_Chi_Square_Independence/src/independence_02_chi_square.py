"""
Lesson 41 - Step 2: Chi-Square Test of Independence
===================================================
THE RECIPE
Start from independence_01_contingency_table.py, then introduce:
    1. chi_square_statistic()   sum of (O - E)^2 / E over the six cells
    2. independence_test()      df = (r-1)(c-1), p-value, Cramer's V
    3. save_figure()            heatmap of cell contributions

Context:
We want to test if conversion is statistically independent of acquisition
channel. The test statistic aggregates how far observed counts depart
from independence expectations. A large statistic leads to a small p-value,
rejecting independence.

How to read this file:
    1. Notice `expected_table()` is now a simplified helper.
    2. Read `chi_square_statistic()` to see the manual calculation of chi2.
    3. Read `independence_test()` to see scipy do it automatically and calculate Cramer's V.
    4. Run the script and compare the test's p-value against our alpha.

Run it:
    uv run en/L41_Chi_Square_Independence/src/independence_02_chi_square.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# We use the Agg backend to render plots without requiring a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# A fixed seed for reproducible random operations
SEED = 42

# The levels of our two categorical variables
CHANNELS = ("Email", "Search", "Social")
OUTCOMES = ("Converted", "Not converted")

# The synthetic 2 by 3 contingency table (rows=outcomes, cols=channels)
OBSERVED = np.array([[40, 55, 18], [80, 70, 62]], dtype=float)

# Our chosen significance level
ALPHA = 0.05

# Resolve the directory where our output figure will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def expected_table(observed: np.ndarray) -> np.ndarray:
    """
    Independence expected counts E = row total * column total / n.

    Parameters:
        observed (np.ndarray): The 2D array of observed counts.

    Returns:
        np.ndarray: The expected counts under the null hypothesis.
    """
    n = observed.sum()
    return np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n


# --- NEW (1) chi_square_statistic() ------------------------------------------
def chi_square_statistic(observed: np.ndarray, expected: np.ndarray) -> dict[str, np.ndarray | float]:
    """
    Return cell contributions and the chi-square total.

    Parameters:
        observed (np.ndarray): The observed 2D counts.
        expected (np.ndarray): The expected 2D counts under independence.

    Returns:
        dict: A dictionary containing:
            - 'contributions': A 2D array of each cell's (O - E)^2 / E.
            - 'chi2': The sum of all contributions (the test statistic).

    Notes:
        Cells with large contributions are where the data deviates most
        from what we would expect if variables were independent.
    """
    # Vectorized element-wise calculation for each cell
    contributions = (observed - expected) ** 2 / expected

    return {"contributions": contributions, "chi2": float(np.sum(contributions))}
# ------------------------------------------------------------------------------


# --- NEW (2) independence_test() ---------------------------------------------
def independence_test(observed: np.ndarray) -> dict[str, float]:
    """
    Chi-square test of independence plus Cramer's V.

    Parameters:
        observed (np.ndarray): The 2D array of observed counts.

    Returns:
        dict: A dictionary containing:
            - 'chi2': The test statistic from scipy.
            - 'p_value': The right-tailed p-value.
            - 'df': Degrees of freedom.
            - 'cramer_v': Effect size measure.
            - 'critical': The critical value at our ALPHA.
            - 'n': Total sample size.

    Notes:
        Degrees of freedom for a contingency table is (rows - 1) * (cols - 1).
        Cramer's V is an effect size between 0 and 1 indicating association strength.
        We use correction=False to avoid Yates' continuity correction.
    """
    # scipy automatically computes the expected table internally
    scipy_chi2, p_value, df, expected = stats.chi2_contingency(observed, correction=False)

    n = observed.sum()

    # Cramer's V formula: sqrt(chi2 / (n * (min(rows, cols) - 1)))
    cramer_v = float(np.sqrt(scipy_chi2 / (n * (min(observed.shape) - 1))))

    return {
        "chi2": float(scipy_chi2),
        "p_value": float(p_value),
        "df": float(df),
        "cramer_v": cramer_v,
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),  # Critical value
        "n": float(n),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(contributions: np.ndarray) -> Path:
    """
    Heatmap of (O - E)^2 / E in the 2 by 3 table.

    Parameters:
        contributions (np.ndarray): The 2D array of cell contributions.

    Returns:
        Path: The absolute path where the PNG is saved.

    Notes:
        Visualizing contributions helps identify which specific channel
        and outcome combinations are driving the rejection of independence.
    """
    output_path = DIR_FIGURES / "independence_02_chi_square.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Draw a heatmap where darker reds mean higher contribution to chi2
    image = ax.imshow(contributions, cmap="Reds", vmin=0, vmax=contributions.max())

    # Label axes
    ax.set_xticks(np.arange(len(CHANNELS)), CHANNELS)
    ax.set_yticks(np.arange(len(OUTCOMES)), OUTCOMES)
    ax.set_title("Chi-Square Cell Contributions, df = 2")

    # Overlay the exact numerical contribution value on each cell
    for i in range(contributions.shape[0]):
        for j in range(contributions.shape[1]):
            ax.text(
                j, i, f"{contributions[i, j]:.2f}",
                ha="center", va="center", color="#1A2E51", fontweight="bold",
            )

    # Add a color scale legend to the right of the heatmap
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="(O - E)^2 / E")

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    expected = expected_table(OBSERVED)
    parts = chi_square_statistic(OBSERVED, expected)
    test = independence_test(OBSERVED)
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"
    figure_path = save_figure(parts["contributions"])

    print("================================================================")
    print("LESSON 41 - STEP 2: CHI-SQUARE INDEPENDENCE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Hypotheses                      : H0: conversion independent of channel")
    print(f"Chi-square statistic            : {test['chi2']:.6f}")
    print(f"Degrees of freedom (r-1)(c-1)   : {int(test['df'])}")
    print(f"Right-tailed p-value            : {test['p_value']:.6f}")
    print(f"Critical chi2* (alpha = 0.05)   : {test['critical']:.6f}")
    print(f"Cramer's V                      : {test['cramer_v']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

