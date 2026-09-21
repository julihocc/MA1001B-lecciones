"""
Lesson 31 - Step 2: Chi-Square Confidence Interval for Variance
===============================================================
THE RECIPE
Start from chi2_var_01_sample_variance.py, then introduce:
    1. chi_square_criticals()   chi2.ppf at 0.025 and 0.975 with df = 19
    2. variance_interval()      ((n-1)s^2 / chi2_U, (n-1)s^2 / chi2_L)
    3. save_figure()            draw the interval for sigma^2

The same n = 20 synthetic cycles are rebuilt with SEED = 42. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 computed s^2 with divisor
n - 1, so df = 19. Lesson 01 covers pathlib and unattended savefig; they
are rebuilt here only so the script stays self-contained. This step wraps
that s^2 in a 95% chi-square interval for the population variance sigma^2.

    stats.chi2.ppf(p, df)   p-quantile of chi-square with df = n - 1
    alpha = 1 - 0.95        two-sided tail total; each tail is alpha / 2
    chi2_L = ppf(0.025, 19) lower critical value (left tail)
    chi2_U = ppf(0.975, 19) upper critical value (right tail)
    lower = df * s^2 / chi2_U
    upper = df * s^2 / chi2_L

If the cycles are iid Normal(mu, sigma^2), then
    (n - 1) s^2 / sigma^2  ~  chi-square with df = n - 1.
Inverting that pivot puts the critical values in the denominator, so the
larger chi-square quantile produces the lower bound. The interval is not
x-bar +/- z * SE and is not symmetric about s^2.

main() prints the two chi-square quantiles, the interval for sigma^2, and
whether this one sample covers the hidden value 9.

Run it:
    uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_02_variance_interval.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.chi2 is the
# chi-square family: here we need only the quantile function ppf.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same seed, n, and hidden Normal process as Step 1 so the sample, s^2,
# and df = 19 are identical.
SEED = 42
N = 20
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
# Nominal coverage of the two-sided interval. 0.95 is a long-run property
# of the method under normality, not a guarantee for one sample.
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_cycle_sample(seed: int = SEED) -> np.ndarray:
    """Rebuild the Step 1 sample of n iid normal cycle times.

    The generator, seed, loc, scale, and size are identical so this file
    describes the same 20 cycles. This script does not import Step 1.
    The analyst still does not know sigma^2.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


# --- NEW (1) chi_square_criticals() ------------------------------------------
def chi_square_criticals(df: int, confidence: float = CONFIDENCE) -> dict[str, float]:
    """Return lower and upper chi-square quantiles for a two-sided interval.

    Parameters
    ----------
    df:
        Degrees of freedom. For a variance interval this is n - 1, not n.
    confidence:
        Nominal coverage, default 0.95. The two-sided tail total is
        alpha = 1 - confidence, split equally as alpha / 2 on each side.

    Returns
    -------
    dict[str, float]
        df and alpha, plus chi2_lower = chi-square_{alpha/2, df} and
        chi2_upper = chi-square_{1 - alpha/2, df}.

    Notes
    -----
    stats.chi2.ppf(p, df) is the inverse CDF: the value c such that
    P(chi-square_df <= c) = p. For 95% and df = 19 that is ppf(0.025, 19)
    on the left and ppf(0.975, 19) on the right.

    Chi-square is right-skewed (mean = df, variance = 2 df), so those two
    quantiles are not equally far from 19. That skew is why the variance
    interval in variance_interval() is not symmetric about s^2.
    """
    # Two-sided: 2.5% in each tail when confidence is 0.95.
    alpha = 1.0 - confidence
    # ppf = percent-point function = quantile. float() unwraps SciPy's
    # NumPy scalar into a plain Python float for printing.
    chi2_lower = float(stats.chi2.ppf(alpha / 2.0, df))
    chi2_upper = float(stats.chi2.ppf(1.0 - alpha / 2.0, df))
    return {
        "df": float(df),
        "alpha": alpha,
        "chi2_lower": chi2_lower,
        "chi2_upper": chi2_upper,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) variance_interval() ---------------------------------------------
def variance_interval(
    s2: float,
    df: int,
    criticals: dict[str, float],
) -> dict[str, float]:
    """Build the 95% interval for sigma^2 from chi-square critical values.

    Parameters
    ----------
    s2:
        Sample variance with divisor n - 1, from np.var(..., ddof=1).
    df:
        n - 1. Multiplies s^2 in the numerator of both bounds.
    criticals:
        Dictionary from chi_square_criticals(), with chi2_lower and
        chi2_upper.

    Returns
    -------
    dict[str, float]
        s2, lower, upper, and width of the interval for sigma^2.
        hidden_sigma2 is the teaching value 9. covers_true is 1.0 if
        that hidden value sits inside [lower, upper] for this sample,
        else 0.0.

    Notes
    -----
    Under iid normality, (n-1) s^2 / sigma^2 ~ chi-square_df. A 95%
    probability statement for that pivot is
        chi2_L  <=  (n-1) s^2 / sigma^2  <=  chi2_U.
    Solving the two inequalities for sigma^2 reverses both, and the
    critical values move into the denominator:
        (n-1) s^2 / chi2_U  <=  sigma^2  <=  (n-1) s^2 / chi2_L.
    The larger quantile therefore produces the lower bound. This is not
    x-bar +/- z * SE: there is no symmetric margin around s^2.

    covers_true is a 0/1 outcome for one sample. Approximate 95% coverage
    is a property of repeating the method under normality, which Step 3
    will check.
    """
    # Larger chi-square in the denominator -> smaller bound.
    lower = df * s2 / criticals["chi2_upper"]
    # Smaller chi-square in the denominator -> larger bound.
    upper = df * s2 / criticals["chi2_lower"]
    hidden = SIGMA_TRUE ** 2
    return {
        "s2": s2,
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
        "hidden_sigma2": hidden,
        # Comparison chained: True if hidden sits inside [lower, upper].
        # float(True) is 1.0 and float(False) is 0.0.
        "covers_true": float(lower <= hidden <= upper),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(interval: dict[str, float]) -> Path:
    """Save the chi-square interval for the population variance.

    Parameters
    ----------
    interval:
        Dictionary from variance_interval(), with lower, upper, and
        hidden_sigma2.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    errorbar draws one horizontal interval. The marker is the midpoint of
    [lower, upper], which is a plotting convenience, not a point estimate:
    the point estimate remains s^2, and the chi-square interval is not
    symmetric about s^2. The dashed line is the hidden sigma^2 = 9.
    """
    output_path = DIR_FIGURES / "chi2_var_02_variance_interval.png"
    # Midpoint is only where the marker sits. It is not the interval's
    # center of probability and is not equal to s^2.
    midpoint = (interval["lower"] + interval["upper"]) / 2.0
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # xerr is [left arm, right arm] as column vectors. The two arms
    # differ because the chi-square interval is asymmetric.
    ax.errorbar(
        [midpoint],
        [1],
        xerr=[[midpoint - interval["lower"]],
              [interval["upper"] - midpoint]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.axvline(interval["hidden_sigma2"], color="#5B8DEF", linestyle="--",
               linewidth=1.6, label=f"True sigma^2 = {interval['hidden_sigma2']:.1f}")
    ax.set_yticks([1])
    ax.set_yticklabels(["95% chi-square interval"])
    ax.set_xlabel("Population variance (min^2)")
    ax.set_title("Chi-Square Interval for sigma^2, df = 19")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        midpoint,
        1.18,
        f"[{interval['lower']:.2f}, {interval['upper']:.2f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 chi-square interval and write the evidence figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_cycle_sample()
    # Same s^2 as Step 1: divisor n - 1, not n.
    s2 = float(np.var(sample, ddof=1))
    # df = n - 1 = 19. This is the chi-square parameter, not the sample size.
    df = N - 1
    criticals = chi_square_criticals(df)
    interval = variance_interval(s2, df, criticals)
    figure_path = save_figure(interval)

    print("================================================================")
    print("LESSON 31 - STEP 2: CHI-SQUARE VARIANCE INTERVAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Degrees of freedom              : {df}")
    print(f"Sample variance s^2             : {s2:.6f}")
    # chi2_L = chi-square_{0.025, 19}; used in the upper bound's denominator.
    print(f"chi2 lower (0.025)              : {criticals['chi2_lower']:.6f}")
    # chi2_U = chi-square_{0.975, 19}; used in the lower bound's denominator.
    print(f"chi2 upper (0.975)              : {criticals['chi2_upper']:.6f}")
    print(f"Lower bound for sigma^2         : {interval['lower']:.6f}")
    print(f"Upper bound for sigma^2         : {interval['upper']:.6f}")
    print(f"Interval width                  : {interval['width']:.6f}")
    print(f"Hidden sigma^2                  : {interval['hidden_sigma2']:.6f}")
    # True/False for THIS sample. 95% coverage is a long-run claim.
    print(f"Covers true sigma^2             : {bool(interval['covers_true'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

