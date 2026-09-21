"""
Lesson 31 - Step 3: Non-Normal Data Invalidate the Chi-Square Interval
======================================================================
THE RECIPE
Start from chi2_var_02_variance_interval.py, then introduce:
    1. coverage_normal()       seed-42 coverage of the chi-square interval
    2. coverage_exponential()  same interval formula on right-skewed cycles
    3. save_figure()           contrast the two empirical coverage rates

Limit: the chi-square interval for sigma^2 assumes a normal population.
When cycle times are exponential, the same formula no longer covers near
95% of the time.

How to read this file:
You already know Python through OOP. Steps 1-2 built s^2 with df = n - 1
and inverted (n-1)s^2 / chi-square_df into a 95% interval for sigma^2.
Lesson 01 covers pathlib and unattended savefig. This step keeps that
formula and drops the normality assumption.

    stats.chi2.ppf(p, df)        same 0.025 and 0.975 quantiles, df = 19
    rng.normal(mu, sigma, (R, n))  R samples of size n under normality
    rng.exponential(scale, (R, n)) R samples of size n, right-skewed
    np.var(..., axis=1, ddof=1)  one s^2 per row, still divisor n-1
    DF * s2 / chi2_U, DF * s2 / chi2_L
                                 vectorized Step 2 interval
    np.mean((lo <= true) & (true <= hi))
                                 empirical coverage: fraction of hits

Coverage is the long-run fraction of intervals that contain the true
sigma^2. Under normality it should sit near 0.95. Exponential cycles
keep s^2 defined and keep the formula runnable, but (n-1)s^2 / sigma^2
is then not chi-square_df, so coverage collapses.

main() prints both true variances and both empirical coverage rates
from 5,000 seed-42 replications.

Run it:
    uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_03_nonnormal_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.chi2.ppf is the same quantile function as Step 2. The critical
# values do not change; only the data-generating process does.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 20
# df = n - 1 = 19, locked once so every replication uses the same
# chi-square critical values as Step 2.
DF = N - 1
# 5_000 independent samples of size n. The underscore is a thousands
# separator; Python reads it as 5000.
N_REPS = 5000
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
# Exponential scale is the mean. Variance of Exponential(scale) is
# scale^2, so the hidden sigma^2 under this alternative is 144, not 9.
EXP_SCALE = 12.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def chi_square_bounds(s2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return chi-square interval bounds for one or many sample variances.

    Parameters
    ----------
    s2:
        Sample variance or an array of them, each with divisor n - 1.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (lower, upper) using the Step 2 inversion
            lower = df * s^2 / chi2_U,
            upper = df * s^2 / chi2_L,
        with chi2_L = chi-square_{0.025, 19} and
        chi2_U = chi-square_{0.975, 19}. NumPy broadcasts so a vector
        of s^2 values yields a vector of intervals.

    Notes
    -----
    The critical values are computed from the chi-square distribution
    with df = n - 1. That sampling distribution holds when the cycles
    are iid normal. The function still returns numbers when they are
    not; those numbers are then not 95% intervals.
    """
    # Same two-sided 95% quantiles as chi_square_criticals() in Step 2.
    chi2_l = float(stats.chi2.ppf(0.025, DF))
    chi2_u = float(stats.chi2.ppf(0.975, DF))
    # Larger chi-square -> lower bound; smaller chi-square -> upper bound.
    return DF * s2 / chi2_u, DF * s2 / chi2_l


# --- NEW (1) coverage_normal() -----------------------------------------------
def coverage_normal(n_reps: int = N_REPS) -> dict[str, float]:
    """Empirical coverage when the normal assumption is true.

    Parameters
    ----------
    n_reps:
        Number of independent samples of size n. Default N_REPS = 5000.

    Returns
    -------
    dict[str, float]
        n_reps, true_var = SIGMA_TRUE ** 2 = 9, and coverage = the
        fraction of the n_reps intervals that contain that true variance.

    Notes
    -----
    Each row of samples is one n = 20 draw from Normal(12, 3), the same
    process as Steps 1-2. axis=1 takes the sample variance across the 20
    columns of each row, still with ddof=1 so df = 19.

    Under this generator, (n-1)s^2 / sigma^2 is chi-square_19, so the
    empirical coverage should land near the nominal 0.95. Monte Carlo
    error of order 1/sqrt(5000) remains; a value such as 0.9494 is a
    hit for the method, not a miss.
    """
    rng = np.random.default_rng(SEED)
    # Shape (n_reps, N): 5000 rows, 20 cycle times each.
    samples = rng.normal(MU_TRUE, SIGMA_TRUE, size=(n_reps, N))
    s2 = np.var(samples, axis=1, ddof=1)
    lower, upper = chi_square_bounds(s2)
    true_var = SIGMA_TRUE ** 2
    return {
        "n_reps": float(n_reps),
        "true_var": true_var,
        # Elementwise AND of two boolean arrays, then the mean of 0/1.
        "coverage": float(np.mean((lower <= true_var) & (true_var <= upper))),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) coverage_exponential() ------------------------------------------
def coverage_exponential(n_reps: int = N_REPS) -> dict[str, float]:
    """Empirical coverage when cycle times are exponential, hence skewed.

    Parameters
    ----------
    n_reps:
        Number of independent samples of size n. Default N_REPS = 5000.
        The Generator is seeded with the same 42, but the draws are
        exponential rather than normal, so the stream is a different
        experiment from coverage_normal().

    Returns
    -------
    dict[str, float]
        n_reps, true_var = EXP_SCALE ** 2 = 144, and coverage of that
        variance by the same chi-square formula.

    Notes
    -----
    rng.exponential(scale=12) has mean 12 and variance 144. The sample
    variance s^2 with divisor n-1 is still defined. The interval formula
    is unchanged: df * s^2 / chi2_U and df * s^2 / chi2_L with df = 19.

    What fails is the pivot. Exponential cycles are right-skewed, so
    (n-1)s^2 / sigma^2 is not chi-square_19. Coverage then falls well
    below 95% even though every line of the formula still runs.
    """
    rng = np.random.default_rng(SEED)
    samples = rng.exponential(scale=EXP_SCALE, size=(n_reps, N))
    s2 = np.var(samples, axis=1, ddof=1)
    lower, upper = chi_square_bounds(s2)
    # Exponential(scale) variance is scale^2, not scale.
    true_var = EXP_SCALE ** 2
    return {
        "n_reps": float(n_reps),
        "true_var": true_var,
        "coverage": float(np.mean((lower <= true_var) & (true_var <= upper))),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    normal_cov: float,
    exponential_cov: float,
) -> Path:
    """Contrast nominal 95% coverage with the two simulated rates.

    Parameters
    ----------
    normal_cov:
        Empirical coverage under Normal(12, 3), from coverage_normal().
    exponential_cov:
        Empirical coverage under Exponential(12), from
        coverage_exponential().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The dashed line is the nominal 0.95. The navy bar should sit near
    that line; the magenta bar should sit well below it. The figure is
    the limit of the lesson: a runnable formula is not a valid interval
    once the normal assumption is gone.
    """
    output_path = DIR_FIGURES / "chi2_var_03_nonnormal_limit.png"
    labels = ["Normal cycles", "Exponential cycles"]
    values = [normal_cov, exponential_cov]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(0.95, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label="Nominal 95%")
    ax.set_ylabel("Empirical coverage")
    ax.set_title("Non-Normal Data Invalidate the Chi-Square Variance Interval")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 coverage contrast and write the evidence figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    normal = coverage_normal()
    exponential = coverage_exponential()
    figure_path = save_figure(normal["coverage"], exponential["coverage"])

    print("================================================================")
    print("LESSON 31 - STEP 3: NON-NORMAL COVERAGE LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Replications                    : {N_REPS}")
    print(f"Normal true sigma^2             : {normal['true_var']:.6f}")
    # Near 0.95: the chi-square pivot holds under normality.
    print(f"Normal empirical coverage       : {normal['coverage']:.6f}")
    print(f"Exponential true sigma^2        : {exponential['true_var']:.6f}")
    # Well below 0.95: the same formula is not a 95% interval when skewed.
    print(f"Exponential empirical coverage  : {exponential['coverage']:.6f}")
    print("Limit                          : non-normal data invalidate chi-square CI")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

