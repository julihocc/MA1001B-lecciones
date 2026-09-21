"""
Lesson 25 - Step 2: Simulated Sampling Distribution of phat
===========================================================
THE RECIPE
Start from sampling_proportion_01_se_phat.py, then introduce:
    1. simulate_phat()          5,000 binomial samples of n = 120, seed 42
    2. empirical_summaries()    mean and SE of phat versus p and formula SE
    3. save_figure()            histogram of phat with the normal overlay

The same late-delivery proportion p = 0.18 is rebuilt. No earlier lesson
script is imported.

How to read this file:
You already know Python through OOP. Step 1 defined SE(phat) and the np
checks. Lesson 01 covers pathlib and unattended savefig; they are rebuilt
here only so the script stays self-contained. This step draws many phat
values from Binomial(n, p) and overlays N(p, SE).

    rng.binomial(n, p, size)   5,000 late-ticket counts X
    phat = X / n               convert each count into a sample proportion
    empirical SE               sample SD of those 5,000 phat values
    theoretical SE             sqrt(p(1-p)/n) from Step 1, using population p
    histogram + N(p, SE)       simulated sampling distribution vs the bell
    1 - Phi((0.22 - p)/SE)     normal tail P(phat > 0.22)

main() prints mean of phat = 0.179663, empirical SE = 0.035079 against
formula SE = 0.035071, and simulated P(phat > 0.22) = 0.119800 versus
normal 0.127032.

Run it:
    python sampling_proportion_02_simulation.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm is the N(p, SE) overlay. The binomial draws themselves come
# from NumPy's Generator, not from scipy.stats.binom.rvs.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Course-wide seed. Unlike Step 1, this script consumes it: every
# replication of phat is drawn from default_rng(42).
SEED = 42
# Same population proportion and sample size as Step 1.
P = 0.18
N = 120
# How many independent samples of n tickets. 5_000 is large enough for
# the histogram and the empirical SE to sit next to the formula.
N_REPS = 5_000
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def proportion_se(p: float = P, n: int = N) -> float:
    """Return SE(phat) = sqrt(p (1 - p) / n).

    Same formula as Step 1. Rebuilt here so this file does not import
    that script. Uses the population p, not a simulated mean of phat.

    Returns
    -------
    float
        Theoretical SD of the sampling distribution of phat.
    """
    return float(np.sqrt(p * (1.0 - p) / n))


# --- NEW (1) simulate_phat() -------------------------------------------------
def simulate_phat(n: int = N, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps sample proportions from Binomial(n, p).

    Parameters
    ----------
    n:
        Tickets per sample. Default N = 120.
    n_reps:
        Number of independent samples. Default N_REPS = 5_000.

    Returns
    -------
    np.ndarray
        Length n_reps. Each entry is one phat = X/n, so the values live
        on the grid 0, 1/n, ..., 1.

    Notes
    -----
    rng.binomial draws the COUNT of late tickets, X ~ Binomial(n, p).
    Dividing by n converts the count into the sample proportion phat.
    That is the definition, not an extra modeling choice: one sample of
    120 tickets produces one phat, and 5,000 such samples produce the
    Monte Carlo picture of the sampling distribution.

    default_rng(SEED) is a local Generator. Do not mix it with the older
    np.random.seed() global state. The same integer 42 rebuilds the same
    5,000 phat values on every run.
    """
    rng = np.random.default_rng(SEED)
    # X, not phat: an integer 0..n for each replication.
    successes = rng.binomial(n=n, p=P, size=n_reps)
    return successes / n
# ------------------------------------------------------------------------------


# --- NEW (2) empirical_summaries() -------------------------------------------
def empirical_summaries(phats: np.ndarray, n: int = N) -> dict[str, float]:
    """Compare simulated mean and SE of phat with the formulas.

    Parameters
    ----------
    phats:
        The 5,000 sample proportions from simulate_phat().
    n:
        Sample size used both to form those phat values and to compute
        the theoretical SE.

    Returns
    -------
    dict[str, float]
        mean_phat: average of the simulated phat values, near p.
        empirical_se: sample SD of those phat values (ddof=1).
        theoretical_se: sqrt(p(1-p)/n) from proportion_se().
        p_gt_0_22: Monte Carlo P(phat > 0.22).
        normal_p_gt_0_22: the same tail under N(p, SE).

    Notes
    -----
    E[phat] = p, so the simulated mean should sit near 0.18. The
    empirical SE should sit near the formula SE; that is the check that
    the sampling distribution recovered sqrt(p(1-p)/n).

    ddof=1 is Bessel's correction: divide by 4,999 rather than 5,000
    when estimating a SD from the simulated phat values. The theoretical
    SE still uses the known p, not mean_phat.

    The tail P(phat > 0.22) is a single number the histogram and the
    bell can both report. The normal value is 1 - Phi((0.22 - p)/SE),
    evaluated here as 1 - cdf(0.22).
    """
    se = proportion_se(P, n)
    return {
        "mean_phat": float(np.mean(phats)),
        "empirical_se": float(np.std(phats, ddof=1)),
        "theoretical_se": se,
        "p_gt_0_22": float(np.mean(phats > 0.22)),
        "normal_p_gt_0_22": float(1.0 - stats.norm(P, se).cdf(0.22)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(phats: np.ndarray) -> Path:
    """Histogram 5,000 values of phat against N(p, SE).

    Parameters
    ----------
    phats:
        Simulated sample proportions from simulate_phat().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    density=True scales the histogram to area 1 so it can share a
    vertical axis with the normal pdf. The navy curve is the same
    N(p, SE(phat)) overlay from Step 1. Agreement of the bars with
    that curve is the visual version of "empirical SE recovered the
    formula."

    The dashed line is again the parameter p, the center of both the
    histogram and the bell, not one realized phat.
    """
    output_path = DIR_FIGURES / "sampling_proportion_02_simulation.png"
    se = proportion_se()
    grid = np.linspace(P - 4 * se, P + 4 * se, 200)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(phats, bins=25, density=True, color="#5B8DEF", alpha=0.6,
            edgecolor="#1A2E51", label="Seed-42 phat")
    # Normal overlay of the sampling distribution, not of one ticket.
    ax.plot(grid, stats.norm(P, se).pdf(grid), color="#1A2E51", lw=2.2,
            label="Normal approximation")
    ax.axvline(P, color="#EC2661", ls="--", lw=1.3, label="p = 0.18")
    ax.set_xlabel("Sample proportion phat")
    ax.set_ylabel("Density")
    ax.set_title("5,000 Samples of n = 120 Recover SE(phat)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Simulate the sampling distribution of phat and compare it to N(p, SE).

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    phats = simulate_phat()
    summary = empirical_summaries(phats)
    figure_path = save_figure(phats)

    print("================================================================")
    print("LESSON 25 - STEP 2: SIMULATION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"Mean of phat                    : {summary['mean_phat']:.6f}")
    print(f"Theoretical SE                  : {summary['theoretical_se']:.6f}")
    print(f"Empirical SE                    : {summary['empirical_se']:.6f}")
    print(f"Simulated P(phat > 0.22)        : {summary['p_gt_0_22']:.6f}")
    print(f"Normal P(phat > 0.22)           : {summary['normal_p_gt_0_22']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01.
if __name__ == "__main__":
    main()

