"""
Lesson 42 - Step 2: Chi-Square Test of Homogeneity
==================================================
THE RECIPE
Start from homogeneity_01_three_samples.py, then introduce:
    1. expected_under_homogeneity()  E = row total * column total / n
    2. homogeneity_test()            same chi2 arithmetic as independence
    3. save_figure()                 cell contributions for three sites

Context:
H0 says the three independently sampled sites share one channel mix.
The statistic matches independence; the sampling story does not. No earlier
lesson script is imported.

How to read this file:
We use `scipy.stats.chi2_contingency` just as we did for the test of independence.
The math inside Python is identical! As a developer, you only need to call this
one function to compute the test statistic, p-value, and degrees of freedom.
The key difference is the interpretation (homogeneity compares multiple populations
across a single variable, while independence compares two variables from one population).

Run it:
    python homogeneity_02_chi_square.py
"""

from pathlib import Path  # For robust path operations

import matplotlib  # For setting the plotting backend
import numpy as np  # For arrays and array arithmetic
from scipy import stats  # For chi-square test functions

# Non-interactive backend to save plots without a GUI
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reproducibility seed for downstream or related operations
SEED = 42
# The three populations sampled
SITES = ("North", "Central", "South")
# The categories observed in each population
CATEGORIES = ("Phone", "Chat", "Email")
# The actual counts (rows: sites, cols: categories)
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
# Significance level for our hypothesis test
ALPHA = 0.05
# Directory path for saving plots
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists before saving anything
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) expected_under_homogeneity() ------------------------------------
def expected_under_homogeneity(observed: np.ndarray) -> np.ndarray:
    """Expected counts when independent samples share one mix.

    Parameters
    ----------
    observed : np.ndarray
        A 2D array of observed counts.

    Returns
    -------
    np.ndarray
        A 2D array of expected counts under H0.

    Notes
    -----
    Under the null hypothesis of homogeneity, all populations have the same
    proportion for each category. The expected count for a cell is its row
    total multiplied by its column total, divided by the grand total `n`.
    We compute this using `np.outer()` for the entire matrix at once.
    """
    n = observed.sum()
    # np.outer performs outer product: row vector * column vector
    # giving a matrix of E_{ij} = R_i * C_j / n
    return np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n
# ------------------------------------------------------------------------------


# --- NEW (2) homogeneity_test() ----------------------------------------------
def homogeneity_test(observed: np.ndarray) -> dict[str, float]:
    """Chi-square homogeneity test with df = (rows - 1)(columns - 1).

    Parameters
    ----------
    observed : np.ndarray
        A 2D array of observed counts.

    Returns
    -------
    dict[str, float]
        A dictionary with the test results: "chi2" (statistic), "p_value",
        "df" (degrees of freedom), "critical" (threshold), and "min_expected"
        (the smallest expected cell count).

    Notes
    -----
    The underlying math (and Python function) is identical to the test of
    independence. We set `correction=False` to avoid Yates' continuity
    correction, which we usually disable unless it's a 2x2 table.
    """
    # Compute chi-square stat, p-value, df, and expected counts all at once
    chi2, p_value, df, expected = stats.chi2_contingency(observed, correction=False)
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "df": float(df),
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),  # Critical chi-square value
        "min_expected": float(np.min(expected)),             # Check assumption: E >= 5
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(observed: np.ndarray, expected: np.ndarray) -> Path:
    """Heatmap of homogeneity cell contributions.

    Parameters
    ----------
    observed : np.ndarray
        A 2D array of observed counts.
    expected : np.ndarray
        A 2D array of expected counts.

    Returns
    -------
    Path
        The absolute path to the generated PNG heatmap.

    Notes
    -----
    This visualization shows which cells contribute the most to the total
    chi-square statistic. High values mean large deviations from homogeneity.
    """
    output_path = DIR_FIGURES / "homogeneity_02_chi_square.png"
    # Calculate cell-by-cell contribution: (O - E)^2 / E
    contributions = (observed - expected) ** 2 / expected

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Render heatmap based on contribution magnitudes
    image = ax.imshow(contributions, cmap="Reds", vmin=0, vmax=contributions.max())

    # Label axes
    ax.set_xticks(np.arange(len(CATEGORIES)), CATEGORIES)
    ax.set_yticks(np.arange(len(SITES)), SITES)
    ax.set_title("Homogeneity Cell Contributions, df = 4")

    # Overlay the numeric contribution values on each cell
    for i in range(contributions.shape[0]):
        for j in range(contributions.shape[1]):
            ax.text(
                j, i, f"{contributions[i, j]:.2f}",
                ha="center", va="center", color="#1A2E51", fontweight="bold",
            )

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="(O - E)^2 / E")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Compute expected counts under H0
    expected = expected_under_homogeneity(OBSERVED)

    # 2. Perform the test
    test = homogeneity_test(OBSERVED)

    # Determine significance based on p-value vs alpha
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"

    # 3. Save the contribution heatmap
    figure_path = save_figure(OBSERVED, expected)

    # Print exact original outputs
    print("================================================================")
    print("LESSON 42 - STEP 2: CHI-SQUARE HOMOGENEITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Hypotheses                      : H0: the three sites share one mix")
    print(
        "Expected North                  : "
        + ", ".join(f"{value:.3f}" for value in expected[0])
    )
    print(
        "Expected Central                : "
        + ", ".join(f"{value:.3f}" for value in expected[1])
    )
    print(
        "Expected South                  : "
        + ", ".join(f"{value:.3f}" for value in expected[2])
    )
    print(f"Minimum expected count          : {test['min_expected']:.6f}")
    print(f"Chi-square statistic            : {test['chi2']:.6f}")
    print(f"Degrees of freedom (r-1)(c-1)   : {int(test['df'])}")
    print(f"Right-tailed p-value            : {test['p_value']:.6f}")
    print(f"Critical chi2* (alpha = 0.05)   : {test['critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

