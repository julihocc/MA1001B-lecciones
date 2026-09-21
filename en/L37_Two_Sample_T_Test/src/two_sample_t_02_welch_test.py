"""
Lesson 37 - Step 2: Welch Two-Sample t Test
===========================================
THE RECIPE
Start from two_sample_t_01_group_summaries.py, then introduce:
    1. welch_standard_error()   SE that does not pool the two variances
    2. welch_t_test()           t statistic, Satterthwaite df, two-sided p
    3. save_figure()            t density with the observed Welch statistic

Context:
The same nA = 30 and nB = 32 synthetic shifts are rebuilt with SEED = 42.
Welch is the stated procedure because the sample sizes and sample s values
differ. No earlier lesson script is imported. The Welch's t-test is more
robust when the assumption of equal variances (homoscedasticity) is violated.

How to read this file:
- `welch_standard_error`: Calculates standard error without pooling variances,
  which accounts for the unequal dispersion in independent groups.
- `welch_t_test`: Calculates the test statistic and performs a two-sided
  hypothesis test by comparing it to the t-distribution.
- `save_figure`: Visualizes the t-distribution density curve, critical bounds,
  and the observed t-statistic to determine rejection.

Run it:
    python two_sample_t_02_welch_test.py
"""

# pathlib provides path manipulation logic
from pathlib import Path

# matplotlib for plotting data
import matplotlib
# numpy for array calculations
import numpy as np
# scipy.stats provides statistical functions and distributions
from scipy import stats

# Set non-interactive backend for file generation
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same constants for reproducible independent groups
SEED = 42
N_A = 30
N_B = 32
# Significance level for the two-tailed hypothesis test
ALPHA = 0.05

# Setup paths for figure artifact saving
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """
    Draw independent synthetic pick times and years of experience.

    Parameters
    ----------
    seed : int, optional
        Seed for the random number generator (default is SEED).

    Returns
    -------
    dict[str, np.ndarray]
        A dictionary containing the simulated pick times and experience
        levels for Shift A and Shift B as numpy arrays.
    """
    rng = np.random.default_rng(seed)
    return {
        "times_a": rng.normal(loc=48.0, scale=6.0, size=N_A),
        "times_b": rng.normal(loc=52.5, scale=7.5, size=N_B),
        "experience_a": rng.normal(loc=4.5, scale=1.0, size=N_A),
        "experience_b": rng.normal(loc=2.0, scale=0.8, size=N_B),
    }


# --- NEW (1) welch_standard_error() ------------------------------------------
def welch_standard_error(s_a: float, n_a: int, s_b: float, n_b: int) -> float:
    """
    Return sqrt(sA^2/nA + sB^2/nB) without pooling the variances.

    Parameters
    ----------
    s_a : float
        Sample standard deviation of group A.
    n_a : int
        Sample size of group A.
    s_b : float
        Sample standard deviation of group B.
    n_b : int
        Sample size of group B.

    Returns
    -------
    float
        The calculated standard error for the Welch t-test.

    Notes
    -----
    Instead of assuming the populations have identical standard deviation (pooled),
    we calculate the variance of the difference by summing the individual group
    variances divided by their sizes.
    """
    # The standard error of the difference between independent means
    return float(np.sqrt(s_a**2 / n_a + s_b**2 / n_b))
# ------------------------------------------------------------------------------


# --- NEW (2) welch_t_test() --------------------------------------------------
def welch_t_test(times_a: np.ndarray, times_b: np.ndarray) -> dict[str, float]:
    """
    Welch t, Satterthwaite df, and two-sided p-value.

    Parameters
    ----------
    times_a : np.ndarray
        Array containing the pick times for Shift A.
    times_b : np.ndarray
        Array containing the pick times for Shift B.

    Returns
    -------
    dict[str, float]
        Summary dictionary with means, test statistic, p-values, degrees
        of freedom, and test comparators.

    Notes
    -----
    Since variances are unequal, the degrees of freedom must be adjusted
    using the Welch-Satterthwaite equation to accurately model the distribution
    of the test statistic.
    """
    mean_a = float(np.mean(times_a))
    mean_b = float(np.mean(times_b))
    s_a = float(np.std(times_a, ddof=1))
    s_b = float(np.std(times_b, ddof=1))
    n_a = times_a.size
    n_b = times_b.size

    # Standard Error of the unpooled variances
    se = welch_standard_error(s_a, n_a, s_b, n_b)

    # Welch's t-statistic is the difference in means scaled by standard error
    t_stat = (mean_a - mean_b) / se

    # Welch-Satterthwaite equation to calculate adjusted degrees of freedom (df)
    df_num = (s_a**2 / n_a + s_b**2 / n_b) ** 2
    df_den = (s_a**2 / n_a) ** 2 / (n_a - 1) + (s_b**2 / n_b) ** 2 / (n_b - 1)
    df_welch = df_num / df_den

    # 2-sided p-value derived from the survival function (sf = 1 - cdf) of t-distribution
    p_value = float(2.0 * stats.t.sf(np.abs(t_stat), df_welch))

    # Compare with SciPy's automated test which has a parameter for unpooled variances
    scipy_test = stats.ttest_ind(times_a, times_b, equal_var=False)

    return {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "s_a": s_a,
        "s_b": s_b,
        "se": se,
        "t_stat": float(t_stat),
        "df_welch": float(df_welch),
        "p_value": p_value,
        "scipy_p": float(scipy_test.pvalue),
        "scipy_t": float(scipy_test.statistic),
        # Calculate critical t-value (percent point function = inverse cdf) for rejection boundaries
        "t_critical": float(stats.t.ppf(1.0 - ALPHA / 2.0, df_welch)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(t_stat: float, df_welch: float, t_critical: float) -> Path:
    """
    Shade both tails of the Welch t reference curve.

    Parameters
    ----------
    t_stat : float
        The observed Welch's t-statistic.
    df_welch : float
        The calculated Satterthwaite degrees of freedom.
    t_critical : float
        The theoretical critical t-value defining rejection bounds.

    Returns
    -------
    Path
        The absolute filepath where the plot was saved.

    Notes
    -----
    Visualizing the t-distribution demonstrates whether the observed statistic
    falls into the 'critical region' (the shaded tails).
    """
    output_path = DIR_FIGURES / "two_sample_t_02_welch_test.png"

    # Generate points across the relevant domain of the test statistic distribution
    x = np.linspace(-4.8, 4.8, 600)
    # Calculate the probability density function (pdf) for the Welch df
    y = stats.t.pdf(x, df_welch)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)

    # Highlight the probability regions outside the observed magnitude (the p-value area)
    ax.fill_between(x, y, where=(x <= -abs(t_stat)), color="#EC2661", alpha=0.45)
    ax.fill_between(x, y, where=(x >= abs(t_stat)), color="#EC2661", alpha=0.45)

    # Plot vertical markers for the observed statistic vs the critical threshold
    ax.axvline(t_stat, color="#EC2661", linewidth=1.6,
               label=f"observed t = {t_stat:.2f}")
    ax.axvline(-t_critical, color="#646464", linestyle="--", linewidth=1.2)
    ax.axvline(t_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"t* = {t_critical:.2f}")

    ax.set_xlabel("t")
    ax.set_ylabel("Density")
    ax.set_title(f"Welch Two-Sample t, df = {df_welch:.1f}")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Build synthetic sample groups
    samples = build_shift_samples()
    # Execute the hypothesis test checking for mean differences
    test = welch_t_test(samples["times_a"], samples["times_b"])

    # Null hypothesis (H0): Group means are identical
    # If the computed p-value drops below the threshold, reject the null hypothesis
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"

    # Plot the result density and decision regions
    figure_path = save_figure(test["t_stat"], test["df_welch"], test["t_critical"])

    print("================================================================")
    print("LESSON 37 - STEP 2: WELCH TWO-SAMPLE t TEST")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print("Hypotheses                      : H0: muA = muB vs H1: muA != muB")
    print(f"Mean difference A minus B       : {test['mean_a'] - test['mean_b']:.6f}")
    print(f"Welch SE                        : {test['se']:.6f}")
    print(f"Welch t statistic               : {test['t_stat']:.6f}")
    print(f"Satterthwaite df                : {test['df_welch']:.6f}")
    print(f"Two-sided p-value (manual)      : {test['p_value']:.6f}")
    print(f"Two-sided p-value (scipy)       : {test['scipy_p']:.6f}")
    print(f"Critical t* (two-sided)         : {test['t_critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

