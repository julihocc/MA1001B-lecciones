"""
Lesson 32 - Step 2: F Ratio and Upper-Tail Probability
======================================================
THE RECIPE
Start from f_two_var_01_sample_variances.py, then introduce:
    1. f_ratio()            F = s1^2 / s2^2
    2. f_upper_tail()       p = scipy.stats.f.sf(F, df1, df2)
    3. save_figure()        shade the F tail beyond the observed ratio

H0: sigma1^2 = sigma2^2 versus H1: sigma1^2 > sigma2^2. The same two
station samples are rebuilt with SEED = 42. No earlier lesson script is
imported.

How to read this file:
You already know Python through OOP. Step 1 computed two sample variances
with np.var(..., ddof=1) and df = n-1. Lesson 01 covers pathlib and
unattended savefig; they are rebuilt here only so the script stays
self-contained. This step forms the F ratio and reads its upper tail
from scipy.stats.f.

    F = s1^2 / s2^2          ratio of independent sample variances
    df1, df2 = n1-1, n2-1    numerator and denominator degrees of freedom
    stats.f.sf(F, df1, df2)  P(F_{df1,df2} >= F), the upper-tail p-value
    stats.f.ppf(1-alpha, ...)  F critical value with upper tail alpha
    stats.f.pdf(x, df1, df2) density height of F(df1, df2), used to plot

Under H0 and two independent normal samples, F ~ F(df1, df2). sf is the
survival function 1 - cdf; it replaces a printed F table. ppf is the
inverse of cdf: the cutoff with left-tail probability 1-alpha.

main() prints F, the critical value, the upper-tail p-value, and the
reject/retain decision at alpha = 0.05.

Run it:
    python f_two_var_02_f_test.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats.f is the F family: pdf for the curve, sf for the upper
# tail P(F >= f_stat), and ppf for the critical value. dfn is df1
# (numerator) and dfd is df2 (denominator).
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same seed and station model as Step 1 so the two sample variances match.
SEED = 42
N1 = 25
N2 = 25
MU = 40.0
SIGMA1 = 8.0
SIGMA2 = 5.0
# Significance level for the upper-tail test of H0: sigma1^2 = sigma2^2.
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_two_stations(seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """Draw independent normal samples from two packing stations.

    Rebuilt from Step 1 so this file does not import the earlier script.
    loc is the mean and scale is the sd. The two rng.normal calls on one
    Generator produce independent Station A and Station B samples.
    """
    rng = np.random.default_rng(seed)
    station_a = rng.normal(loc=MU, scale=SIGMA1, size=N1)
    station_b = rng.normal(loc=MU, scale=SIGMA2, size=N2)
    return station_a, station_b


# --- NEW (1) f_ratio() -------------------------------------------------------
def f_ratio(station_a: np.ndarray, station_b: np.ndarray) -> dict[str, float]:
    """Compute F = s1^2 / s2^2 with numerator and denominator df.

    Parameters
    ----------
    station_a:
        n1 cycle times; its sample variance is the F numerator.
    station_b:
        n2 cycle times; its sample variance is the F denominator.

    Returns
    -------
    dict[str, float]
        s1_sq and s2_sq are the sample variances (ddof=1). f_stat is
        s1^2 / s2^2. df1 = n1-1 and df2 = n2-1 index the F law.

    Notes
    -----
    Under H0: sigma1^2 = sigma2^2 and independent normal samples,
        F = s1^2 / s2^2  ~  F(df1, df2).
    Station A is in the numerator because H1 is sigma1^2 > sigma2^2,
    an upper-tail alternative. Swapping the groups would invert F and
    move the tail. The ratio compares variances, not means.
    """
    s1_sq = float(np.var(station_a, ddof=1))
    s2_sq = float(np.var(station_b, ddof=1))
    return {
        "s1_sq": s1_sq,
        "s2_sq": s2_sq,
        # F statistic. Do not take a square root: F is a variance ratio.
        "f_stat": s1_sq / s2_sq,
        "df1": float(N1 - 1),
        "df2": float(N2 - 1),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) f_upper_tail() --------------------------------------------------
def f_upper_tail(f_stat: float, df1: float, df2: float) -> dict[str, float]:
    """Return the upper-tail p-value from scipy.stats.f.sf and the F critical.

    Parameters
    ----------
    f_stat:
        Observed ratio s1^2 / s2^2 from f_ratio().
    df1:
        Numerator degrees of freedom n1-1. SciPy calls this dfn.
    df2:
        Denominator degrees of freedom n2-1. SciPy calls this dfd.

    Returns
    -------
    dict[str, float]
        p_value is P(F_{df1,df2} >= f_stat) from stats.f.sf. alpha is
        the module-level significance level. f_crit is the upper-tail
        cutoff from stats.f.ppf. reject_h0 is 1.0 when p < alpha.

    Notes
    -----
    stats.f.sf(f, dfn, dfd) is 1 - stats.f.cdf(f, dfn, dfd), the
    survival function. For a continuous F law, P(F >= f) = P(F > f).
    stats.f.ppf(1-alpha, dfn, dfd) inverts the CDF: it is the F value
    with left-tail probability 1-alpha, so the upper tail equals alpha.
    Reject H0 when the observed F exceeds that cutoff, equivalently
    when the sf p-value is below alpha.
    """
    # Survival: P(F_{df1,df2} >= f_stat). Replaces a printed F table.
    p_value = float(stats.f.sf(f_stat, df1, df2))
    # Inverse CDF at 1-alpha: the critical value with upper tail 0.05.
    f_crit = float(stats.f.ppf(1.0 - ALPHA, df1, df2))
    return {
        "p_value": p_value,
        "alpha": ALPHA,
        "f_crit": f_crit,
        "reject_h0": float(p_value < ALPHA),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(ratio: dict[str, float], tail: dict[str, float]) -> Path:
    """Shade the F density to the right of the observed ratio.

    Parameters
    ----------
    ratio:
        Dict from f_ratio(); f_stat, df1, and df2 locate the curve and
        the observed line.
    tail:
        Dict from f_upper_tail(); p_value labels the shade and f_crit
        is the dashed critical line.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    y = stats.f.pdf(x, df1, df2) is a density height, not a probability.
    The shaded area to the right of the observed F is the p-value from
    sf. The dashed line is the alpha = 0.05 critical value from ppf.
    """
    output_path = DIR_FIGURES / "f_two_var_02_f_test.png"
    df1, df2 = ratio["df1"], ratio["df2"]
    # F support starts at 0. Start slightly above 0 and extend past the
    # observed ratio so both the critical line and the tail are visible.
    x = np.linspace(0.02, max(6.0, ratio["f_stat"] + 1.5), 400)
    y = stats.f.pdf(x, df1, df2)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    # Boolean mask x >= F. The area of this shade is stats.f.sf(F, df1, df2).
    ax.fill_between(
        x[x >= ratio["f_stat"]],
        y[x >= ratio["f_stat"]],
        color="#EC2661",
        alpha=0.55,
        label=f"P(F >= {ratio['f_stat']:.2f}) = {tail['p_value']:.4f}",
    )
    ax.axvline(ratio["f_stat"], color="#EC2661", linewidth=2.0)
    ax.axvline(tail["f_crit"], color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"F crit = {tail['f_crit']:.2f}")
    ax.set_xlabel("F statistic")
    ax.set_ylabel("Density")
    ax.set_title("F Distribution: Upper Tail for Two Variances")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 F-test report and write the upper-tail figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    station_a, station_b = generate_two_stations()
    ratio = f_ratio(station_a, station_b)
    tail = f_upper_tail(ratio["f_stat"], ratio["df1"], ratio["df2"])
    figure_path = save_figure(ratio, tail)

    print("================================================================")
    print("LESSON 32 - STEP 2: F RATIO AND UPPER TAIL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print("H0                             : sigma1^2 = sigma2^2")
    print("H1                             : sigma1^2 > sigma2^2")
    print(f"s1^2                            : {ratio['s1_sq']:.6f}")
    print(f"s2^2                            : {ratio['s2_sq']:.6f}")
    # Variance ratio, not a difference of means and not a t statistic.
    print(f"F = s1^2 / s2^2                 : {ratio['f_stat']:.6f}")
    print(f"df1, df2                        : {int(ratio['df1'])}, {int(ratio['df2'])}")
    print(f"F critical (alpha=0.05)         : {tail['f_crit']:.6f}")
    # stats.f.sf(F, 24, 24): P(F_{24,24} >= observed ratio).
    print(f"Upper-tail p-value (f.sf)       : {tail['p_value']:.6f}")
    print(f"Reject H0 at alpha=0.05         : {bool(tail['reject_h0'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

