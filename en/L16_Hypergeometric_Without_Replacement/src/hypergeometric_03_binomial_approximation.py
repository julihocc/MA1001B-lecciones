"""
Lesson 16 - Step 3: Binomial Approximation When n/N Is Not Small
================================================================
THE RECIPE
Start from hypergeometric_02_expectation.py, then introduce:
    1. binomial_p_zero()    Binomial(n=10, p=K/N) chance of a clean sample
    2. compare_models()     hypergeometric versus binomial P(X = 0)
    3. save_figure()        overlay the two PMFs

The sampling fraction n/N = 10/80 = 0.125 is not small. Drawing without
replacement depletes defectives, so the binomial overstates P(X = 0).

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, the Agg
backend, and unattended savefig. Steps 1-2 computed hypergeometric
P(X = 0) and E[X] = nK/N. This script copies those lot constants and
comments only the NEW bands.

New in this step:
    binomial with p = K/N     independent trials; sampling with replacement
                              or an infinite lot, not this finite draw
    (1 - p)^n vs C(N-K, n)/C(N, n)  two formulas for P(X = 0)
    sampling fraction 0.125   too large for the binomial shortcut
    matching means            nK/N = np, but P(X = 0) still differs
    grouped bars              two PMFs side by side at each integer x

main() prints binomial P(X = 0) = 0.458582 against hypergeometric
0.436326, an overstatement of 0.022257, and matching means of 0.75.

Run it:
    python hypergeometric_03_binomial_approximation.py
"""

# Path, Agg, savefig, and close: same unattended-figure idiom as Lesson 01.
from pathlib import Path

import matplotlib
import numpy as np
# hypergeom is the exact without-replacement model. binom is the independent-
# trials approximation from Lessons 14-15. Both live in scipy.stats.
from scipy import stats

# Agg must be selected before pyplot; see Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical lot to Steps 1-2. SEED stays reserved; this script does not draw.
SEED = 42
N_POP = 80
K_DEFECTIVE = 6
N_DRAW = 10
# Binomial success probability if one pretended p never changed. K/N =
# 6/80 = 0.075 is the lot defective rate, not a new parameter.
P_BINOM = K_DEFECTIVE / N_POP
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def hypergeometric_p_zero() -> float:
    """Return P(X = 0) for X ~ Hypergeometric(N=80, K=6, n=10).

    Exact clean-sample probability under sampling without replacement.
    SciPy names: M is textbook N, n is textbook K, N is textbook n.
    See Step 1.

    Returns
    -------
    float
        C(74, 10) / C(80, 10), evaluated by scipy.stats.hypergeom.pmf.
    """
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))


def hypergeometric_mean() -> float:
    """Return E[X] = n K / N.

    Same mean as Step 2. It will match the binomial mean n p with
    p = K/N, which is the point of the comparison: equal expectations
    do not imply equal P(X = 0).

    Returns
    -------
    float
        10 * 6 / 80 = 0.75.
    """
    return N_DRAW * K_DEFECTIVE / N_POP


# --- NEW (1) binomial_p_zero() -----------------------------------------------
def binomial_p_zero() -> float:
    """Return P(X = 0) for the binomial approximation with p = K/N.

    Returns
    -------
    float
        (1 - p)^n with p = 6/80 and n = 10, from scipy.stats.binom.pmf.

    Notes
    -----
    Binomial trials are independent with a constant success probability.
    That describes sampling with replacement, or from an infinite lot.
    This inspection draws 10 units without replacement from 80, so p is
    not constant: after a good unit leaves, the remaining defective rate
    ticks up slightly, and a clean sample becomes a little less likely.

    stats.binom uses the textbook names n (trials) and p (success chance).
    stats.hypergeom does not; do not reuse these keywords there.
    """
    return float(stats.binom.pmf(0, n=N_DRAW, p=P_BINOM))
# ------------------------------------------------------------------------------


# --- NEW (2) compare_models() ------------------------------------------------
def compare_models() -> dict[str, float]:
    """Compare hypergeometric and binomial P(X = 0) and means.

    Returns
    -------
    dict[str, float]
        hyper_p_zero, binom_p_zero: the two clean-sample probabilities.
        hyper_mean, binom_mean: nK/N and n p, which match.
        sampling_fraction: n/N = 0.125, not small.
        overstatement: binomial P(X = 0) minus hypergeometric P(X = 0).

    Notes
    -----
    The binomial overstates P(X = 0) when n/N is not small because it
    ignores depletion. On the all-clean path the inspector keeps drawing
    good units, so goods leave faster than the lot shrinks and the
    remaining defective rate rises. Hypergeometric multiplies those
    changing fractions; binomial keeps multiplying 74/80.

    The means still agree: dependence changes the shape of the PMF
    without changing E[X] = nK/N.
    """
    return {
        "hyper_p_zero": hypergeometric_p_zero(),
        "binom_p_zero": binomial_p_zero(),
        "hyper_mean": hypergeometric_mean(),
        "binom_mean": N_DRAW * P_BINOM,
        "sampling_fraction": N_DRAW / N_POP,
        "overstatement": binomial_p_zero() - hypergeometric_p_zero(),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Overlay hypergeometric and binomial PMFs.

    Parameters
    ----------
    comparison:
        The dict from compare_models(). The figure rebuilds both PMFs
        from the same module constants; the argument keeps the call
        signature stable and is not read inside the plot.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    Grouped bars: shift one series left and the other right by half a
    bar width so both sit at the same integer x. Hypergeometric (navy)
    is the exact without-replacement model. Binomial (red) is the
    independent-trials approximation that overstates the x = 0 bar.
    """
    output_path = DIR_FIGURES / "hypergeometric_03_binomial_approximation.png"
    # min(K, n) = K here, so 0..K is the shared plotting support.
    xs = np.arange(0, K_DEFECTIVE + 1)
    # hypergeom: M = textbook N, n = textbook K, N = textbook n.
    hyper = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    # binom: n = trials, p = K/N. These keyword names are the usual ones.
    binom = stats.binom.pmf(xs, n=N_DRAW, p=P_BINOM)
    width = 0.38

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs - width / 2, hyper, width=width, color="#1A2E51", label="Hypergeometric")
    ax.bar(xs + width / 2, binom, width=width, color="#EC2661", label="Binomial approx.")
    ax.set_xlabel("Defectives in the sample x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Binomial Overstates P(X = 0) When n/N = 0.125")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Contrast binomial and hypergeometric P(X = 0) when n/N is not small.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    comparison = compare_models()
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LESSON 16 - STEP 3: BINOMIAL APPROXIMATION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"p = K/N                         : {P_BINOM:.6f}")
    print(f"Sampling fraction n/N           : {comparison['sampling_fraction']:.6f}")
    print(f"Hypergeometric P(X = 0)         : {comparison['hyper_p_zero']:.6f}")
    print(f"Binomial P(X = 0)               : {comparison['binom_p_zero']:.6f}")
    print(f"Binomial overstatement          : {comparison['overstatement']:.6f}")
    print(f"Hypergeometric mean             : {comparison['hyper_mean']:.6f}")
    print(f"Binomial mean                   : {comparison['binom_mean']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01.
if __name__ == "__main__":
    main()

