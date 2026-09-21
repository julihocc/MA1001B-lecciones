"""
Lesson 24 - Step 3: Small n Plus Skew Is a Poor CLT Approximation
=================================================================
THE RECIPE
Start from clt_02_means_n4_n40.py, then introduce:
    1. tail_comparison()        P(xbar > mu + 2 SE) exact-vs-normal
    2. normal_error()           CLT tail error at n = 4 versus n = 40
    3. save_figure()            bar the true tail against the normal tail

For exponential delays, xbar has an exact Gamma law. At n = 4 the normal
two-SE tail is about half the true tail. At n = 40 the same z = 2 cut is
closer, but skew has not vanished.

How to read this file:
You already know Python through OOP. Steps 1-2 built a right-skewed
Exponential(mean=10) clock and simulated xbar for n = 4 and n = 40.
Lesson 01 covers pathlib and unattended savefig. This step is the CLT
limit: matching mean and SE does not make the tails match when n is
small and the population is skewed.

    xbar ~ Gamma(shape=n, scale=10/n)  exact law for exponential means
    N(10, 10/sqrt(n))                  CLT working model for xbar
    cut = mu + 2 SE                    the same z = 2 event at every n
    1 - model.cdf(cut)                 right-tail probability
    n = 4 vs n = 40                    small n + skew: normal tail too thin

main() prints the exact Gamma tail against the normal tail at both
sample sizes. The normal two-SE tail is always about 0.022750; the
true tail is larger and shrinks only as n grows.

Run it:
    python clt_03_small_n_skew_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.gamma is the exact sampling law of an exponential mean.
# stats.norm is the CLT approximation from Step 2. This script does
# not redraw the exponential delays; it uses the closed-form laws.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed. Step 3 is deterministic: Gamma and Normal CDFs, no
# Monte Carlo. The same 42 keeps the package aligned with Steps 1-2.
SEED = 42
# Same exponential mean (and sd) as Steps 1-2.
MEAN = 10.0
N_SMALL = 4
N_LARGE = 40
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) tail_comparison() -----------------------------------------------
def tail_comparison(n: int) -> dict[str, float]:
    """Compare the exact Gamma tail of xbar with the CLT normal tail at z=2.

    Parameters
    ----------
    n:
        Sample size. The exact law of xbar and the CLT scale both
        depend on n.

    Returns
    -------
    dict[str, float]
        cut is mu + 2 SE. exact_tail is P(xbar > cut) under Gamma.
        normal_tail is the same probability under N(mu, SE).
        abs_error is |normal - exact|. exact_skew is 2/sqrt(n).

    Notes
    -----
    If X_1, ..., X_n are iid Exponential(scale=theta), their sum is
    Gamma(shape=n, scale=theta) and their mean is
        xbar ~ Gamma(shape=n, scale=theta/n).
    SciPy writes that as stats.gamma(a=n, scale=MEAN / n).

    The CLT replaces that Gamma law by N(mu, SE) with SE = 10/sqrt(n).
    The event xbar > mu + 2 SE is z = 2 on the normal scale, so the
    normal tail is 1 - Phi(2) at every n. The Gamma tail is larger
    because the sampling distribution is still right-skewed; at n = 4
    the normal value is about half the truth.
    """
    se = MEAN / np.sqrt(n)
    cut = MEAN + 2.0 * se
    # a= is SciPy's shape. scale=MEAN/n so E[xbar] = n * (MEAN/n) = MEAN.
    exact = stats.gamma(a=n, scale=MEAN / n)
    normal = stats.norm(loc=MEAN, scale=se)
    exact_tail = float(1.0 - exact.cdf(cut))
    normal_tail = float(1.0 - normal.cdf(cut))
    return {
        "n": float(n),
        "cut": cut,
        "se": se,
        "exact_tail": exact_tail,
        "normal_tail": normal_tail,
        "abs_error": abs(normal_tail - exact_tail),
        # Same 2/sqrt(n) exponential-mean skew as in Step 2.
        "exact_skew": 2.0 / np.sqrt(n),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) normal_error() --------------------------------------------------
def normal_error() -> dict[str, dict[str, float]]:
    """Return z = 2 tail comparisons for n = 4 and n = 40.

    Returns
    -------
    dict[str, dict[str, float]]
        Keys "n4" and "n40", each a tail_comparison() record.

    Notes
    -----
    The CLT is a large-sample shape statement, not a promise at n = 4
    on a skewness-2 clock. Comparing the two sample sizes shows the
    tail error shrinking as n grows, without claiming it has vanished
    at n = 40.
    """
    return {
        "n4": tail_comparison(N_SMALL),
        "n40": tail_comparison(N_LARGE),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(table: dict[str, dict[str, float]]) -> Path:
    """Bar exact versus normal tails at z = 2.

    Parameters
    ----------
    table:
        Dict from normal_error() with "n4" and "n40" records.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Four bars: exact Gamma and CLT normal at each n. The two normal
    bars are the same height (z = 2 always has tail about 0.0228).
    The exact bars are taller; the gap is the visual of "small n +
    skew makes the CLT a poor approximation."
    """
    output_path = DIR_FIGURES / "clt_03_small_n_skew_limit.png"
    labels = ["n = 4\nexact", "n = 4\nnormal", "n = 40\nexact", "n = 40\nnormal"]
    values = [
        table["n4"]["exact_tail"],
        table["n4"]["normal_tail"],
        table["n40"]["exact_tail"],
        table["n40"]["normal_tail"],
    ]
    colors = ["#1A2E51", "#5B8DEF", "#EC2661", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("P(xbar > mu + 2 SE)")
    ax.set_title("Small n + Skew: The Normal Tail Is a Poor Approximation")
    ax.set_ylim(0, 0.07)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each bar patch with its probability so the label sits
    # centered, slightly above the top.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.002,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 exact-versus-CLT tail comparison.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    table = normal_error()
    figure_path = save_figure(table)

    print("================================================================")
    print("LESSON 24 - STEP 3: SMALL N SKEW LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Tail event                      : xbar > mu + 2 SE")
    print(f"n = 4 cut                       : {table['n4']['cut']:.6f}")
    print(f"n = 4 exact tail                : {table['n4']['exact_tail']:.6f}")
    print(f"n = 4 normal tail               : {table['n4']['normal_tail']:.6f}")
    print(f"n = 4 absolute error            : {table['n4']['abs_error']:.6f}")
    print(f"n = 4 skewness of xbar          : {table['n4']['exact_skew']:.6f}")
    print(f"n = 40 cut                      : {table['n40']['cut']:.6f}")
    print(f"n = 40 exact tail               : {table['n40']['exact_tail']:.6f}")
    print(f"n = 40 normal tail              : {table['n40']['normal_tail']:.6f}")
    print(f"n = 40 absolute error           : {table['n40']['abs_error']:.6f}")
    print(f"n = 40 skewness of xbar         : {table['n40']['exact_skew']:.6f}")
    print("Limit: small n + skew makes the CLT a poor approximation")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

