"""
Lesson 36 - Step 3: Using phat in the SE Is the Wrong Test Statistic
====================================================================
THE RECIPE
Start from proportion_test_02_z_pvalue.py, then introduce:
    1. se_using_phat()         the Wald SE that does not belong in this test
    2. compare_statistics()    correct z versus the wrong z
    3. save_figure()           side-by-side z and p-value comparison

Context:
A hypothesis test of H0: p = p0 must use p0 in the standard error because the
sampling distribution is built under the assumption that H0 is true. Replacing
p0 with phat yields the Wald standard error, which is meant for confidence intervals
where no hypothesized proportion is available.
In our example (n=200, x=28, p0=0.10, phat=0.14), this mistake changes the SE
and the test statistic just enough to flip the decision at alpha = 0.05.

How to read this file:
You will see a direct comparison of the correct and incorrect SE computations,
and the dramatic effect it can have on the p-value. In OOP terms, this demonstrates
a classic error where an object's method uses an estimated parameter (`phat`)
when the theoretical parameter (`p0`) is mandated by the hypothesis test's design.

Run it:
    python proportion_test_03_wrong_se_limit.py
"""

# Import Path for robust, cross-platform file path handling
from pathlib import Path

# matplotlib is used for generating figures
import matplotlib
# numpy is used for numerical operations
import numpy as np
# scipy.stats provides statistical distributions and functions (like norm)
from scipy import stats

# Use the non-interactive "Agg" backend for matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Random seed (reserved)
SEED = 42
# Sample size
N = 200
# Observed successes
X_LATE = 28
# Hypothesized proportion
P0 = 0.10
# Significance level for the test
ALPHA = 0.05
# Directory for saving figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


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
        Dictionary with sample size, successes, sample proportion, and p0.
    """
    return {"n": float(n), "x": float(x), "phat": x / n, "p0": P0}


def se_under_h0(n: int = N, p0: float = P0) -> float:
    """
    Standard error of phat when H0: p = p0 is true.

    Parameters
    ----------
    n : int
        The total sample size.
    p0 : float
        The hypothesized population proportion.

    Returns
    -------
    float
        The correct standard error using p0.
    """
    return float(np.sqrt(p0 * (1.0 - p0) / n))


# --- NEW (1) se_using_phat() -------------------------------------------------
def se_using_phat(phat: float, n: int = N) -> float:
    """
    Wald standard error that uses phat instead of p0.

    Parameters
    ----------
    phat : float
        The observed sample proportion.
    n : int
        The total sample size.

    Returns
    -------
    float
        The incorrect standard error for a hypothesis test.

    Notes
    -----
    This standard error is perfectly valid for Wald confidence intervals,
    but it is incorrect for a hypothesis test where p0 is given.
    """
    return float(np.sqrt(phat * (1.0 - phat) / n))
# ------------------------------------------------------------------------------


# --- NEW (2) compare_statistics() --------------------------------------------
def compare_statistics(phat: float, p0: float, se0: float, se_hat: float) -> dict[str, float]:
    """
    Contrast the H0-based z test with the incorrect phat-based z.

    Parameters
    ----------
    phat : float
        The sample proportion.
    p0 : float
        The hypothesized population proportion.
    se0 : float
        The correct standard error using p0.
    se_hat : float
        The incorrect standard error using phat.

    Returns
    -------
    dict[str, float]
        A dictionary containing the test statistics, p-values, and boolean rejection decisions
        for both the correct and incorrect calculations.

    Notes
    -----
    Notice that the numerator (phat - p0) is exactly the same for both statistics;
    only the denominator changes. When phat is farther from 0.5 than p0 is, se_hat
    is smaller than se0, leading to a more extreme (but incorrect) z statistic.
    """
    # Correct z statistic and p-value
    z_correct = (phat - p0) / se0
    p_correct = float(stats.norm.sf(z_correct))

    # Incorrect z statistic and p-value
    z_wrong = (phat - p0) / se_hat
    p_wrong = float(stats.norm.sf(z_wrong))

    return {
        "z_correct": float(z_correct),
        "z_wrong": float(z_wrong),
        "p_correct": p_correct,
        "p_wrong": p_wrong,
        "reject_correct": float(p_correct < ALPHA),
        "reject_wrong": float(p_wrong < ALPHA),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(se0: float, se_hat: float, comparison: dict[str, float]) -> Path:
    """
    Compare correct and incorrect standard errors, z values, and p-values.

    Parameters
    ----------
    se0 : float
        The correct standard error using p0.
    se_hat : float
        The incorrect standard error using phat.
    comparison : dict[str, float]
        Dictionary with comparison results.

    Returns
    -------
    Path
        The absolute path to the saved figure file.

    Notes
    -----
    Creates a two-panel side-by-side plot comparing the standard errors and
    the resulting p-values relative to alpha.
    """
    output_path = DIR_FIGURES / "proportion_test_03_wrong_se_limit.png"
    # Create a figure with two subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6))

    # Panel 1: Compare Standard Errors
    se_labels = ["SE uses p0\n(correct test)", "SE uses phat\n(wrong test)"]
    se_vals = [se0, se_hat]
    axes[0].bar(se_labels, se_vals, color=["#1A2E51", "#EC2661"], width=0.55)
    axes[0].set_ylabel("Standard error")
    axes[0].set_title("Which Number Belongs in the SE?")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for i, value in enumerate(se_vals):
        axes[0].text(i, value + 0.0004, f"{value:.4f}", ha="center", fontweight="bold")

    # Panel 2: Compare p-values
    p_labels = ["p-value with p0", "p-value with phat"]
    p_vals = [comparison["p_correct"], comparison["p_wrong"]]
    axes[1].bar(p_labels, p_vals, color=["#1A2E51", "#EC2661"], width=0.55)

    # Draw horizontal line for alpha
    axes[1].axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.3,
                    label="alpha = 0.05")

    axes[1].set_ylabel("Right-tailed p-value")
    axes[1].set_title("Wrong SE Can Flip the Decision")
    axes[1].set_ylim(0, 0.09)
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for i, value in enumerate(p_vals):
        axes[1].text(i, value + 0.002, f"{value:.4f}", ha="center", fontweight="bold")

    fig.tight_layout()
    # Save the figure
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Compute all values
    summary = sample_proportion()
    se0 = se_under_h0()
    se_hat = se_using_phat(summary["phat"])
    comparison = compare_statistics(summary["phat"], summary["p0"], se0, se_hat)
    figure_path = save_figure(se0, se_hat, comparison)

    # Print results summary
    print("================================================================")
    print("LESSON 36 - STEP 3: WRONG SE LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample proportion phat          : {summary['phat']:.6f}")
    print(f"Correct SE using p0             : {se0:.6f}")
    print(f"Wrong SE using phat             : {se_hat:.6f}")
    print(f"Correct z (p0 in SE)            : {comparison['z_correct']:.6f}")
    print(f"Wrong z (phat in SE)            : {comparison['z_wrong']:.6f}")
    print(f"Correct right-tailed p-value    : {comparison['p_correct']:.6f}")
    print(f"Wrong right-tailed p-value      : {comparison['p_wrong']:.6f}")
    print(
        "Decision with correct SE        : "
        f"{'reject H0' if comparison['reject_correct'] else 'do not reject H0'}"
    )
    print(
        "Decision with wrong SE          : "
        f"{'reject H0' if comparison['reject_wrong'] else 'do not reject H0'}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

