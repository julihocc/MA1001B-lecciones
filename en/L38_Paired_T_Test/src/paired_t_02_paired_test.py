"""
Lesson 38 - Step 2: One-Sample t on the Differences
===================================================

THE RECIPE
----------
1. paired_standard_error() : Compute standard error of the mean difference, s_d / sqrt(n).
2. paired_t_test()         : Compute t-statistic on df = n - 1 and the two-sided p-value.
3. save_figure()           : Draw a histogram of d showing the sample mean versus the hypothesized 0.

Context:
--------
A paired t-test is mechanically identical to a one-sample t-test performed on
the differences between paired observations. Here, we analyze the same 25 matched
stations (before - after) from Step 1. Instead of comparing two independent sample
means, we test whether the mean of these differences is significantly different
from zero.

How to read this file:
----------------------
In Python OOP terms, we have mapped a collection of `Station` objects, each with
`.before` and `.after` properties, to a 1D array of `.diff` values. The problem
reduces from a two-sample scenario to a single vector of numbers. We then apply
the standard one-sample formulas: mean, standard deviation, standard error, and
finally the t-statistic and p-value against H0: mu = 0.

Run it:
-------
    uv run en/L38_Paired_T_Test/src/paired_t_02_paired_test.py
(Or from within the src directory:)
    python paired_t_02_paired_test.py
"""

# pathlib handles object-oriented file system paths natively
from pathlib import Path

# matplotlib is used for rendering graphics and charts
import matplotlib
# numpy provides fast array processing and numerical operations
import numpy as np
# scipy.stats provides statistical functions and distributions (like the t-distribution)
from scipy import stats

# Force matplotlib to use the 'Agg' backend to avoid trying to open a window on headless servers
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Random seed ensures reproducible synthetic data generation
SEED = 42
# Number of stations (paired observations)
N_PAIRS = 25
# Hypothesized mean difference under the null hypothesis (typically 0)
MU0 = 0.0
# Significance level for the hypothesis test
ALPHA = 0.05
# Define and create the directory for output figures
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
        A dictionary with "before", "after", and "diff" arrays.

    Notes
    -----
    This replicates the exact data generation process from Step 1 to ensure continuity.
    """
    # Create a random number generator with the specified seed
    rng = np.random.default_rng(seed)
    # Generate random 'before' values
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    # Generate dependent 'after' values
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    # Return the simulated dataset
    return {"before": before, "after": after, "diff": before - after}


# --- NEW (1) paired_standard_error() -----------------------------------------
def paired_standard_error(diff: np.ndarray) -> float:
    """
    Standard error of the mean difference.

    Parameters
    ----------
    diff : np.ndarray
        1D array of differences between paired observations.

    Returns
    -------
    float
        The standard error of the mean of the differences.

    Notes
    -----
    The formula is s_d / sqrt(n), where s_d is the sample standard deviation
    of the differences and n is the number of pairs. This quantifies the
    uncertainty in our estimate of the true mean difference.
    """
    # Calculate sample standard deviation (ddof=1) divided by the square root of n
    return float(np.std(diff, ddof=1) / np.sqrt(diff.size))
# ------------------------------------------------------------------------------


# --- NEW (2) paired_t_test() -------------------------------------------------
def paired_t_test(diff: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """
    One-sample t test of H0: mean difference = 0.

    Parameters
    ----------
    diff : np.ndarray
        1D array of differences between paired observations.
    mu0 : float, optional
        The hypothesized mean difference under the null hypothesis, by default MU0.

    Returns
    -------
    dict[str, float]
        Dictionary containing sample size (n), sample mean (dbar), sample standard
        deviation (s_d), standard error (se), test statistic (t_stat), degrees of
        freedom (df), manual p-value (p_value), scipy p-value (scipy_p), and
        critical t-value (t_critical).

    Notes
    -----
    The t-statistic is calculated as (dbar - mu0) / se. The p-value is calculated
    using the survival function (sf) of the t-distribution, multiplied by 2 for a
    two-sided test. We also run scipy's built-in 1-sample t-test to verify our math.
    """
    # Number of observations (pairs)
    n = diff.size
    # Sample mean of the differences
    dbar = float(np.mean(diff))
    # Sample standard deviation of the differences
    s_d = float(np.std(diff, ddof=1))
    # Standard error of the mean difference
    se = paired_standard_error(diff)

    # Calculate the t-statistic (how many standard errors dbar is away from mu0)
    t_stat = (dbar - mu0) / se
    # Degrees of freedom for a one-sample test on n differences is n - 1
    df = n - 1

    # Calculate the two-sided p-value manually using the t-distribution's survival function
    p_value = float(2.0 * stats.t.sf(np.abs(t_stat), df))

    # Verify the results against scipy's built-in ttest_1samp
    scipy_test = stats.ttest_1samp(diff, mu0)

    # Return all calculated components in a structured dictionary
    return {
        "n": float(n),
        "dbar": dbar,
        "s_d": s_d,
        "se": se,
        "t_stat": float(t_stat),
        "df": float(df),
        "p_value": p_value,
        "scipy_p": float(scipy_test.pvalue),
        # Calculate the critical t-value for the two-sided test using the percent point function (inverse CDF)
        "t_critical": float(stats.t.ppf(1.0 - ALPHA / 2.0, df)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(diff: np.ndarray, dbar: float) -> Path:
    """
    Histogram of matched differences with H0 at zero.

    Parameters
    ----------
    diff : np.ndarray
        1D array of differences between paired observations.
    dbar : float
        The sample mean of the differences.

    Returns
    -------
    Path
        The absolute path to the saved figure image.

    Notes
    -----
    Visualizing the distribution of the differences, alongside the hypothesized
    mean (0) and the actual sample mean, helps intuitively understand the t-test's
    result. If the sample mean is far from 0 relative to the spread of the data,
    the p-value will be low.
    """
    # Define output path
    output_path = DIR_FIGURES / "paired_t_02_paired_test.png"
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot a histogram of the differences
    ax.hist(diff, bins=8, color="#5B8DEF", edgecolor="#1A2E51", alpha=0.9)
    # Add a vertical dashed line at the hypothesized mean (0)
    ax.axvline(MU0, color="#646464", linestyle="--", linewidth=1.6,
               label="H0: mean d = 0")
    # Add a vertical solid line at the actual sample mean
    ax.axvline(dbar, color="#EC2661", linewidth=1.8,
               label=f"mean d = {dbar:.2f}")

    # Configure axes labels and title
    ax.set_xlabel("Difference d = before - after (minutes)")
    ax.set_ylabel("Frequency")
    ax.set_title("Paired t Is a One-Sample t on the Differences")
    # Add legend without a bounding box frame
    ax.legend(frameon=False)
    # Add horizontal gridlines
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout
    fig.tight_layout()
    # Save the figure to disk
    fig.savefig(output_path, dpi=170)
    # Close the figure
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Generate the paired data
    pairs = build_pairs()
    # Perform the paired t-test on the differences
    test = paired_t_test(pairs["diff"])
    # Determine whether to reject H0 based on the p-value and alpha
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"
    # Create and save the histogram visualization
    figure_path = save_figure(pairs["diff"], test["dbar"])

    # Print the detailed output report
    print("================================================================")
    print("LESSON 38 - STEP 2: PAIRED t TEST")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print("Hypotheses                      : H0: mu_d = 0 vs H1: mu_d != 0")
    print(f"Mean difference d-bar           : {test['dbar']:.6f}")
    print(f"SE of the mean difference       : {test['se']:.6f}")
    print(f"t statistic                     : {test['t_stat']:.6f}")
    print(f"Degrees of freedom n-1          : {int(test['df'])}")
    print(f"Two-sided p-value (manual)      : {test['p_value']:.6e}")
    print(f"Two-sided p-value (scipy)       : {test['scipy_p']:.6e}")
    print(f"Critical t* (two-sided)         : {test['t_critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

