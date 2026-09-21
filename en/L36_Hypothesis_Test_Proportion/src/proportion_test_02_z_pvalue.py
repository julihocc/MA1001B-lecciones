"""
Lesson 36 - Step 2: z Statistic with p0 in the Standard Error
=============================================================
THE RECIPE
Start from proportion_test_01_sample_and_conditions.py, then introduce:
    1. se_under_h0()          standard error uses p0, not phat
    2. z_and_p_value()        right-tailed z test for H1: p > p0
    3. save_figure()          shade the upper tail of N(0, 1)

Context:
The same n = 200, x = 28 synthetic inspection counts are rebuilt from
constants. No earlier lesson script is imported. We are testing whether the
late-flag proportion has increased above 10% (p0 = 0.10). This requires a
right-tailed test (H1: p > p0).
Because we assume the null hypothesis (H0: p = 0.10) is true until proven otherwise,
the sampling distribution of phat is centered at p0, and its standard error
is computed using p0. We then standardize our observed phat into a z statistic.

How to read this file:
You will see how a standard error is computed under the null hypothesis, how to
transform the sample proportion into a z statistic, and how to compute a p-value
for a right-tailed test using the survival function (`sf`) from `scipy.stats`.
For an OOP-minded student, consider `se_under_h0` and `z_and_p_value` as
methods calculating derived properties based on the state initialized in step 1.

Run it:
    python proportion_test_02_z_pvalue.py
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
    phat = x / n
    return {"n": float(n), "x": float(x), "phat": float(phat), "p0": P0}


# --- NEW (1) se_under_h0() ---------------------------------------------------
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
        The standard error of the sampling distribution of the sample proportion
        under the null hypothesis.

    Notes
    -----
    The true standard error of phat is sqrt(p(1-p)/n). Since we assume H0 is true,
    we substitute p0 for p. This is a critical distinction from a confidence interval,
    where we don't have a hypothesized p and must use phat instead.
    """
    return float(np.sqrt(p0 * (1.0 - p0) / n))
# ------------------------------------------------------------------------------


# --- NEW (2) z_and_p_value() -------------------------------------------------
def z_and_p_value(phat: float, p0: float, se: float) -> dict[str, float]:
    """
    Right-tailed z statistic and p-value for H1: p > p0.

    Parameters
    ----------
    phat : float
        The sample proportion.
    p0 : float
        The hypothesized population proportion.
    se : float
        The standard error under the null hypothesis.

    Returns
    -------
    dict[str, float]
        Dictionary containing the z statistic, p-value, critical z value, and alpha.

    Notes
    -----
    The z statistic measures how many standard errors phat is away from p0.
    We use stats.norm.sf (survival function, 1 - CDF) because this is a right-tailed test
    (we want the area to the right of z_stat).
    """
    # Standardize the sample proportion
    z_stat = (phat - p0) / se
    # Calculate right-tailed p-value
    p_value = float(stats.norm.sf(z_stat))
    # Find the critical value z* corresponding to alpha (right tail)
    z_critical = float(stats.norm.ppf(1.0 - ALPHA))
    return {
        "z_stat": float(z_stat),
        "p_value": p_value,
        "z_critical": z_critical,
        "alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(z_stat: float, z_critical: float) -> Path:
    """
    Shade the right tail of the standard normal beyond the observed z.

    Parameters
    ----------
    z_stat : float
        The calculated z statistic.
    z_critical : float
        The critical z value for alpha.

    Returns
    -------
    Path
        The absolute path to the saved figure file.

    Notes
    -----
    Visualizing the standard normal distribution N(0, 1) helps intuitively understand
    the p-value as the shaded area and the test decision based on whether z_stat
    crosses z_critical.
    """
    output_path = DIR_FIGURES / "proportion_test_02_z_pvalue.png"
    # Create x values for the standard normal curve
    x = np.linspace(-3.6, 3.6, 600)
    # Calculate y values (Probability Density Function)
    y = stats.norm.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Plot the N(0, 1) curve
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    # Shade the p-value area (right tail)
    ax.fill_between(x, y, where=(x >= z_stat), color="#EC2661", alpha=0.45)

    # Draw vertical line for the observed z statistic
    ax.axvline(z_stat, color="#EC2661", linewidth=1.6,
               label=f"observed z = {z_stat:.2f}")
    # Draw vertical line for the critical z value
    ax.axvline(z_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"z* = {z_critical:.2f}")

    # Set labels and title
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.set_title("Right-Tailed z Test for a Proportion")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    # Save the figure
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Run through the testing steps
    summary = sample_proportion()
    se = se_under_h0()
    test = z_and_p_value(summary["phat"], summary["p0"], se)
    # Decision rule: Reject H0 if p-value < alpha
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"
    figure_path = save_figure(test["z_stat"], test["z_critical"])

    # Output the results
    print("================================================================")
    print("LESSON 36 - STEP 2: z STATISTIC AND p-VALUE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Hypotheses                      : H0: p = {P0:.2f} vs H1: p > {P0:.2f}")
    print(f"Sample proportion phat          : {summary['phat']:.6f}")
    print(f"SE under H0 sqrt(p0(1-p0)/n)    : {se:.6f}")
    print(f"z statistic (phat - p0)/SE      : {test['z_stat']:.6f}")
    print(f"Right-tailed p-value            : {test['p_value']:.6f}")
    print(f"Critical z* (alpha = 0.05)      : {test['z_critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

