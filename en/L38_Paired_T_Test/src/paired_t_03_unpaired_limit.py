"""
Lesson 38 - Step 3: Unpaired Analysis of Paired Data Ignores the Matching
=========================================================================

THE RECIPE
----------
1. unpaired_t_test()       : Compute a two-sample Welch t-test that incorrectly pretends the times are independent.
2. compare_procedures()    : Contrast the correct paired p-value versus the incorrect unpaired p-value.
3. save_figure()           : Plot the two p-values side-by-side against an alpha threshold of 0.05.

Context:
--------
The stations are matched, meaning the 'before' and 'after' times are physically
linked to the same workstation. Treating these measurements as two independent
samples discards their strong positive correlation. This drastically inflates the
standard error, weakens the t-statistic, and incorrectly yields a much higher
p-value, potentially changing the conclusion of the experiment.

How to read this file:
----------------------
In Python OOP terms, this script demonstrates the consequence of destroying the
relationship between an object's properties. By placing all `.before` values in
one independent list and all `.after` values in another, the analysis is blinded
to the per-station variance reduction that the paired design achieved.

Run it:
-------
    uv run en/L38_Paired_T_Test/src/paired_t_03_unpaired_limit.py
(Or from within the src directory:)
    python paired_t_03_unpaired_limit.py
"""

# pathlib is used to handle cross-platform file paths cleanly
from pathlib import Path

# matplotlib is used for rendering graphics and visual comparisons
import matplotlib
# numpy is used for array manipulations and calculations
import numpy as np
# scipy.stats provides testing functions (ttest_ind for independent, ttest_rel for related)
from scipy import stats

# Force matplotlib to use the non-interactive 'Agg' backend
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Constant random seed ensures the generated synthetic data matches previous steps exactly
SEED = 42
# Number of stations (paired observations)
N_PAIRS = 25
# Significance level for deciding whether to reject the null hypothesis
ALPHA = 0.05
# Directory path where output plots will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pairs(seed: int = SEED) -> dict[str, np.ndarray]:
    """
    Draw 25 matched before-after handle times in minutes.

    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility, by default SEED.

    Returns
    -------
    dict[str, np.ndarray]
        A dictionary containing "before", "after", and "diff" arrays.

    Notes
    -----
    This replicates the exact dataset generated in Steps 1 and 2 to demonstrate
    how the same data yields different results depending on the test chosen.
    """
    rng = np.random.default_rng(seed)
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    return {"before": before, "after": after, "diff": before - after}


# --- NEW (1) unpaired_t_test() -----------------------------------------------
def unpaired_t_test(before: np.ndarray, after: np.ndarray) -> dict[str, float]:
    """
    Welch two-sample t that incorrectly ignores the matching.

    Parameters
    ----------
    before : np.ndarray
        1D array of 'before' observations.
    after : np.ndarray
        1D array of 'after' observations.

    Returns
    -------
    dict[str, float]
        A dictionary containing the t-statistic, p-value, degrees of freedom, and standard error.

    Notes
    -----
    We use Welch's t-test (`equal_var=False`) which is standard for independent samples,
    but applying it here is logically incorrect because the data are paired. Notice how
    the standard error is calculated by pooling the variances of the two groups, ignoring
    the covariance between them.
    """
    # Perform Welch's independent samples t-test
    test = stats.ttest_ind(before, after, equal_var=False)
    # Calculate the combined standard error manually for comparison
    se = float(
        np.sqrt(
            np.var(before, ddof=1) / before.size
            + np.var(after, ddof=1) / after.size
        )
    )
    return {
        "t_stat": float(test.statistic),
        "p_value": float(test.pvalue),
        "df": float(test.df),
        "se": se,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) compare_procedures() --------------------------------------------
def compare_procedures(pairs: dict[str, np.ndarray]) -> dict[str, float]:
    """
    Place the correct paired t beside the incorrect unpaired t.

    Parameters
    ----------
    pairs : dict[str, np.ndarray]
        A dictionary containing "before", "after", and "diff" arrays of paired data.

    Returns
    -------
    dict[str, float]
        A dictionary comparing the correlation, t-statistics, p-values, and
        standard errors of both the correct (paired) and incorrect (unpaired) procedures.

    Notes
    -----
    The key insight here is how standard error behaves. The strong positive
    correlation between before and after measurements reduces the variance of
    the differences (paired SE). Ignoring this correlation (unpaired SE) results
    in a larger standard error and thus a smaller t-statistic and larger p-value.
    """
    # Correct procedure: paired t-test using scipy's ttest_rel
    paired = stats.ttest_rel(pairs["before"], pairs["after"])
    # Incorrect procedure: independent t-test using our function from above
    unpaired = unpaired_t_test(pairs["before"], pairs["after"])
    # Correct standard error (based on the variance of the differences)
    se_paired = float(
        np.std(pairs["diff"], ddof=1) / np.sqrt(pairs["diff"].size)
    )

    return {
        "corr": float(np.corrcoef(pairs["before"], pairs["after"])[0, 1]),
        "paired_t": float(paired.statistic),
        "paired_p": float(paired.pvalue),
        "paired_se": se_paired,
        "unpaired_t": unpaired["t_stat"],
        "unpaired_p": unpaired["p_value"],
        "unpaired_se": unpaired["se"],
        "unpaired_df": unpaired["df"],
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """
    Compare paired and unpaired p-values on the same matched data.

    Parameters
    ----------
    comparison : dict[str, float]
        Dictionary output from compare_procedures containing the p-values.

    Returns
    -------
    Path
        The absolute path to the saved figure image.

    Notes
    -----
    This bar chart visually contrasts the p-values from both methods against
    the alpha=0.05 significance threshold. It clearly shows how an incorrect
    (unpaired) analysis could lead to a Type II error (failing to reject a false H0).
    """
    output_path = DIR_FIGURES / "paired_t_03_unpaired_limit.png"
    # Setup labels and values for the bar chart
    labels = ["Paired t\n(correct)", "Unpaired t\n(ignores matching)"]
    values = [comparison["paired_p"], comparison["unpaired_p"]]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Draw bars with distinct colors
    bars = ax.bar(labels, values, color=["#1A2E51", "#EC2661"], width=0.55)
    # Add a horizontal line representing the significance level (alpha)
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.4,
               label="alpha = 0.05")

    ax.set_ylabel("Two-sided p-value")
    ax.set_title("Unpaired Analysis of Paired Data Ignores the Matching")
    # Fix the y-axis limit to ensure the alpha line is clearly visible
    ax.set_ylim(0, 0.20)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate each bar with its exact value
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4g}",
            ha="center",
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    pairs = build_pairs()
    comparison = compare_procedures(pairs)
    figure_path = save_figure(comparison)

    # Evaluate conclusions based on the two different methods
    paired_decision = (
        "reject H0" if comparison["paired_p"] < ALPHA else "do not reject H0"
    )
    unpaired_decision = (
        "reject H0" if comparison["unpaired_p"] < ALPHA else "do not reject H0"
    )

    print("================================================================")
    print("LESSON 38 - STEP 3: UNPAIRED LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Correlation before with after   : {comparison['corr']:.6f}")
    print(f"Paired SE of mean difference    : {comparison['paired_se']:.6f}")
    print(f"Unpaired Welch SE               : {comparison['unpaired_se']:.6f}")
    print(f"Paired t statistic              : {comparison['paired_t']:.6f}")
    print(f"Unpaired t statistic            : {comparison['unpaired_t']:.6f}")
    print(f"Paired two-sided p-value        : {comparison['paired_p']:.6e}")
    print(f"Unpaired two-sided p-value      : {comparison['unpaired_p']:.6f}")
    print(f"Paired decision                 : {paired_decision}")
    print(f"Unpaired decision               : {unpaired_decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

