"""
Lesson 25 - Step 3: Normal Approximation Fails When np < 5
==========================================================
THE RECIPE
Start from sampling_proportion_02_simulation.py, then introduce:
    1. small_sample_phat()      n = 20, p = 0.18 so np = 3.6 < 5
    2. discrete_vs_normal()     P(phat = 0) and a skewed histogram
    3. save_figure()            stem of possible phat versus a bell overlay

The np < 5 (or n(1-p) < 5) rule is the limit. A sample of 20 late-delivery
flags is too small for the normal model of phat.

How to read this file:
You already know Python through OOP. Steps 1-2 used n = 120 so np = 21.6
and the N(p, SE) overlay of phat was legal. Lesson 01 covers pathlib and
unattended savefig. This step drops n to 20 so the binomial law of phat
is visibly discrete, skewed, and stacked at 0.

    np = 3.6 < 5             the normal picture of phat is not licensed
    phat = k/n               only 21 possible values, spacing 1/20
    P(phat = 0) = (1-p)^n    a point mass the bell cannot represent
    continuity window 0.5/n  illegal normal mass assigned near 0
    pmf * n                  scale binomial masses onto a density axis
    positive skew            p = 0.18 is below 0.5 and n is small

main() prints np = 3.6, exact P(phat = 0) = 0.018892 versus simulated
0.016600, normal mass near 0 = 0.035594, and skewness = 0.430019.

Run it:
    python sampling_proportion_03_np_condition_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.binom is the exact discrete law of X (hence of phat = X/n).
# stats.norm is the illegal overlay, kept only to show the mismatch.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same seed and population p as Steps 1-2. Only the sample size changes.
SEED = 42
P = 0.18
# n = 20 makes np = 3.6, below the usual cutoff of 5. n(1-p) = 16.4 is
# still above 5; one failed count is enough to retire the bell.
N_SMALL = 20
N_REPS = 5_000
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) small_sample_phat() ---------------------------------------------
def small_sample_phat(n: int = N_SMALL, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps sample proportions from Binomial(20, 0.18).

    Parameters
    ----------
    n:
        Tickets per sample. Default N_SMALL = 20, not the n = 120 of
        Steps 1-2.
    n_reps:
        Number of independent samples. Default 5_000, same as Step 2.

    Returns
    -------
    np.ndarray
        Length n_reps of phat = X/n values on the coarse grid
        0, 1/20, ..., 1.

    Notes
    -----
    The mechanism is the same as Step 2: rng.binomial draws the late-
    ticket count X, then dividing by n converts it to phat. What changed
    is n. With only 20 tickets, np = 3.6 < 5, so the sampling
    distribution of phat is too coarse and too skewed for a bell.

    SEED is still 42, but the binomial arguments changed, so these
    5,000 draws are not a subset of the Step 2 draws.
    """
    rng = np.random.default_rng(SEED)
    successes = rng.binomial(n=n, p=P, size=n_reps)
    return successes / n
# ------------------------------------------------------------------------------


# --- NEW (2) discrete_vs_normal() --------------------------------------------
def discrete_vs_normal(phats: np.ndarray, n: int = N_SMALL) -> dict[str, float]:
    """Contrast the discrete law of phat with the illegal normal model.

    Parameters
    ----------
    phats:
        Simulated sample proportions from small_sample_phat().
    n:
        Sample size used both in the simulation and in the formulas.

    Returns
    -------
    dict[str, float]
        n, np, n_one_minus_p: the failed condition (np = 3.6).
        se: formula SE, still defined even when the bell is illegal.
        empirical_mean, empirical_se: Monte Carlo center and spread.
        p_phat_zero: exact P(phat = 0) = (1-p)^n from the binomial PMF.
        simulated_p_zero: fraction of simulated phat values equal to 0.
        normal_near_zero: N(p, SE) mass on (-inf, 0.5/n], a continuity
        window around the point 0.
        skewness: sample skewness of the simulated phat values.

    Notes
    -----
    P(phat = 0) = P(X = 0) = (1-p)^n is a point mass. A continuous
    normal curve has P(phat = 0) = 0 at every single number, so it
    cannot represent that spike. The cdf(0.5/n) comparison is already
    generous: it hands the bell the whole continuity-corrected cell
    around 0, and it still does not match the exact mass.

    Positive skewness is expected: p = 0.18 sits below 0.5 and n is
    small, so the right tail of phat is longer than the left. The
    formula SE remains sqrt(p(1-p)/n); the formula is not the problem.
    The normal shape is.
    """
    se = float(np.sqrt(P * (1.0 - P) / n))
    # Exact binomial mass at X = 0, which is the same event as phat = 0.
    p_zero = float(stats.binom.pmf(0, n=n, p=P))
    # Continuity-corrected cell for X = 0 is (-0.5, 0.5] on the count
    # scale, or (-0.5/n, 0.5/n] on the phat scale. cdf from -inf to
    # 0.5/n assigns the illegal bell that whole left cell.
    normal_p_zero = float(stats.norm(P, se).cdf(0.5 / n))
    return {
        "n": float(n),
        "np": n * P,
        "n_one_minus_p": n * (1.0 - P),
        "se": se,
        "empirical_mean": float(np.mean(phats)),
        "empirical_se": float(np.std(phats, ddof=1)),
        "p_phat_zero": p_zero,
        "simulated_p_zero": float(np.mean(phats == 0.0)),
        "normal_near_zero": normal_p_zero,
        "skewness": float(stats.skew(phats, bias=False)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """Stem the exact Binomial(20, 0.18) pmf against a normal overlay.

    Parameters
    ----------
    summary:
        The dict from discrete_vs_normal(). Only the key "se" is read;
        n and p come from the module constants.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    The exact law of phat is discrete: a stem at each k/n with height
    P(X = k). Multiplying the PMF by n puts those masses on a density
    scale, because the grid spacing of phat is 1/n. Without that
    Jacobian the stems would not be comparable to a pdf.

    The light-blue curve is N(p, SE), drawn anyway so the mismatch is
    visible: it leaks below 0, misses the spike at phat = 0, and
    pretends the distribution is symmetric. That is the limit of the
    lesson. np < 5 makes the bell the wrong tool for phat.
    """
    output_path = DIR_FIGURES / "sampling_proportion_03_np_condition_limit.png"
    n = N_SMALL
    # Support of X, then convert to the phat grid k/n.
    ks = np.arange(0, n + 1)
    phat_grid = ks / n
    pmf = stats.binom.pmf(ks, n=n, p=P)
    se = summary["se"]
    x = np.linspace(-0.05, 0.55, 300)
    normal_y = stats.norm(P, se).pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, normal_y, color="#5B8DEF", lw=2.0, label="Illegal normal curve")
    # pmf * n converts P(X = k) into a density-scale height for phat.
    ax.vlines(phat_grid, 0, pmf * n, color="#1A2E51", lw=1.6)
    ax.plot(phat_grid, pmf * n, "o", color="#EC2661", label="Exact binomial")
    ax.set_xlabel("Sample proportion phat")
    ax.set_ylabel("Density scale")
    ax.set_title("np = 3.6 < 5: The Normal Model of phat Fails")
    ax.set_xlim(-0.05, 0.55)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Show that np < 5 makes the normal model of phat fail.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    phats = small_sample_phat()
    summary = discrete_vs_normal(phats)
    figure_path = save_figure(summary)

    print("================================================================")
    print("LESSON 25 - STEP 3: NP CONDITION LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Small n                         : {int(summary['n'])}")
    print(f"np                              : {summary['np']:.6f}")
    print(f"n(1 - p)                        : {summary['n_one_minus_p']:.6f}")
    print(f"Formula SE                      : {summary['se']:.6f}")
    print(f"Empirical mean of phat          : {summary['empirical_mean']:.6f}")
    print(f"Empirical SE                    : {summary['empirical_se']:.6f}")
    print(f"Exact P(phat = 0)               : {summary['p_phat_zero']:.6f}")
    print(f"Simulated P(phat = 0)           : {summary['simulated_p_zero']:.6f}")
    print(f"Normal mass near 0              : {summary['normal_near_zero']:.6f}")
    print(f"Skewness of phat                : {summary['skewness']:.6f}")
    print("Limit: np < 5 makes the normal approximation fail")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01.
if __name__ == "__main__":
    main()

