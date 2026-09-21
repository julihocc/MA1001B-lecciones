"""
Lesson 35 - Step 2: Two-Sided p-Value from Student t
====================================================
THE RECIPE
----------
Start from t_test_mean_01_sample_standard_error.py, then introduce:
    1. two_sided_p_value()     two-tail probability from t with df = n - 1
    2. critical_t_and_decision()  t* at alpha = 0.05 and the reject/retain rule
    3. save_figure()           shade both tails of the t density

The same n = 40 synthetic pack times are rebuilt with SEED = 42. No earlier
lesson script is imported.

Context:
--------
Now that we have computed our t-statistic, we need to convert it into a p-value
so we can test our hypothesis against a significance level (alpha). Since this
is a two-sided test, we check the probability of seeing a t-statistic at least
as extreme in *either* direction (positive or negative).

How to read this file:
----------------------
If you know Python OOP, observe how `scipy.stats` provides statistical objects
(like `stats.t`). We use methods on the `stats.t` object to perform lookups:
`sf()` (survival function, the right tail) for finding the p-value, and `ppf()`
(percent point function, the inverse CDF) to look up our critical t value (t*).

Run it:
-------
    python t_test_mean_02_two_sided_pvalue.py
"""

from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats provides classes for statistical distributions and testing
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
SEED = 42
N = 40
MU0 = 50.0
PROCESS_MEAN = 52.0
PROCESS_SD = 6.0
# ALPHA is our threshold for significance (5%)
ALPHA = 0.05

DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pack_times(seed: int = SEED) -> np.ndarray:
    """Draw n = 40 synthetic pack-out cycle times in minutes."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=PROCESS_MEAN, scale=PROCESS_SD, size=N)


def t_statistic(times: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """Compute x-bar, s, SE, degrees of freedom, and the one-sample t."""
    n = times.size
    xbar = float(np.mean(times))
    sample_sd = float(np.std(times, ddof=1))
    se = sample_sd / np.sqrt(n)
    t_stat = (xbar - mu0) / se
    return {
        "n": float(n),
        "xbar": xbar,
        "sample_sd": sample_sd,
        "se": float(se),
        "df": float(n - 1),
        "t_stat": float(t_stat),
        "mu0": mu0,
    }


# --- NEW (1) two_sided_p_value() ---------------------------------------------
def two_sided_p_value(t_stat: float, df: float) -> dict[str, float]:
    """
    Return the two-sided p-value from Student t and from ttest_1samp.

    Parameters
    ----------
    t_stat : float
        The calculated t-statistic from our sample.
    df : float
        The degrees of freedom (n - 1).

    Returns
    -------
    dict[str, float]
        Dictionary containing the manually calculated two-sided p-value.

    Notes
    -----
    We use `stats.t.sf(np.abs(t_stat), df)` which is the Survival Function
    (1 - CDF). This gives the probability to the right of `abs(t_stat)`.
    Because it is a two-sided test, we multiply by 2 to account for both tails.
    """
    # sf() gives the area under the right tail. Multiply by 2 for both tails.
    p_manual = float(2.0 * stats.t.sf(np.abs(t_stat), df))

    return {"p_value": p_manual}
# ------------------------------------------------------------------------------


# --- NEW (2) critical_t_and_decision() ---------------------------------------
def critical_t_and_decision(
    t_stat: float,
    df: float,
    p_value: float,
    alpha: float = ALPHA,
) -> dict[str, float | str]:
    """
    Compare |t| with t* and the p-value with alpha.

    Parameters
    ----------
    t_stat : float
        The calculated t-statistic from our sample.
    df : float
        The degrees of freedom (n - 1).
    p_value : float
        The calculated two-sided p-value.
    alpha : float, optional
        The significance level (default is 0.05).

    Returns
    -------
    dict[str, float | str]
        Dictionary containing alpha, critical t value, a string decision message,
        and a boolean flag indicating if we reject H0.

    Notes
    -----
    We use `stats.t.ppf(1.0 - alpha / 2.0, df)` to find the critical t value (t*).
    Since this is a two-tailed test, alpha is split in half (alpha / 2.0).
    """
    # ppf() is the inverse CDF. It returns the value of x such that CDF(x) = probability.
    t_critical = float(stats.t.ppf(1.0 - alpha / 2.0, df))

    # We reject the null hypothesis if our calculated p-value is less than alpha.
    reject = bool(p_value < alpha)

    return {
        "alpha": alpha,
        "t_critical": t_critical,
        "decision": "reject H0" if reject else "do not reject H0",
        "reject": float(reject),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(t_stat: float, df: float, t_critical: float) -> Path:
    """
    Shade the two-sided t tails beyond the observed statistic.

    Parameters
    ----------
    t_stat : float
        The observed t-statistic.
    df : float
        The degrees of freedom.
    t_critical : float
        The critical t value defining the rejection regions.

    Returns
    -------
    Path
        The absolute path to the saved figure.

    Notes
    -----
    This visualizes the theoretical t-distribution for our degrees of freedom.
    It shades the areas corresponding to the calculated p-value (both tails)
    and plots vertical lines for our critical boundaries and observed statistic.
    """
    output_path = DIR_FIGURES / "t_test_mean_02_two_sided_pvalue.png"

    # Generate 600 points evenly spaced between -4.5 and 4.5
    x = np.linspace(-4.5, 4.5, 600)
    # Calculate the Probability Density Function (PDF) curve at each point
    y = stats.t.pdf(x, df)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot the full curve
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)

    # Shade the left tail (values less than or equal to -|t|)
    ax.fill_between(x, y, where=(x <= -abs(t_stat)), color="#EC2661", alpha=0.45)
    # Shade the right tail (values greater than or equal to |t|)
    ax.fill_between(x, y, where=(x >= abs(t_stat)), color="#EC2661", alpha=0.45)

    # Draw a line representing our observed t statistic
    ax.axvline(t_stat, color="#EC2661", linestyle="-", linewidth=1.6,
               label=f"observed t = {t_stat:.2f}")

    # Draw dashed lines for the critical boundaries (t* and -t*)
    ax.axvline(t_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"t* = {t_critical:.2f}")
    ax.axvline(-t_critical, color="#646464", linestyle="--", linewidth=1.2)

    # Formatting
    ax.set_xlabel("t")
    ax.set_ylabel("Density")
    ax.set_title(f"Two-Sided t Test, df = {int(df)}")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate sample and calculate statistics
    times = build_pack_times()
    summary = t_statistic(times)

    # 2. Calculate the p-value manually
    p_info = two_sided_p_value(summary["t_stat"], summary["df"])

    # Verify our manual calculation against scipy's built-in one-sample t-test
    scipy_test = stats.ttest_1samp(times, MU0)

    # 3. Make the statistical decision
    decision = critical_t_and_decision(
        summary["t_stat"], summary["df"], p_info["p_value"]
    )

    # 4. Save visualization
    figure_path = save_figure(
        summary["t_stat"], summary["df"], float(decision["t_critical"])
    )

    print("================================================================")
    print("LESSON 35 - STEP 2: TWO-SIDED t p-VALUE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {int(summary['n'])}")
    print(f"Hypotheses                      : H0: mu = {MU0:.0f} vs H1: mu != {MU0:.0f}")
    print(f"Sample mean x-bar               : {summary['xbar']:.6f}")
    print(f"t statistic                     : {summary['t_stat']:.6f}")
    print(f"Degrees of freedom              : {int(summary['df'])}")
    print(f"Two-sided p-value (manual)      : {p_info['p_value']:.6f}")
    print(f"Two-sided p-value (scipy)       : {float(scipy_test.pvalue):.6f}")
    print(f"Significance level alpha        : {float(decision['alpha']):.2f}")
    print(f"Critical t* (two-sided)         : {float(decision['t_critical']):.6f}")
    print(f"Decision at alpha = 0.05        : {decision['decision']}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

