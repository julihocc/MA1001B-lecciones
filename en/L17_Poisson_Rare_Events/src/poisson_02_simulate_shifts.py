"""
Lesson 17 - Step 2: Simulate 10,000 Shifts
==========================================
THE RECIPE
Start from poisson_01_pmf.py, then introduce:
    1. simulate_shifts()    10,000 Poisson(3.2) draws with SEED = 42
    2. simulation_summary() empirical P(X = 0), P(X >= 6), mean, variance
    3. save_figure()        histogram versus the Poisson PMF

The same lambda = 3.2 is rebuilt from constants. No earlier lesson script is
imported.

How to read this file:
You already know Python through OOP. Step 1 defined X ~ Poisson(3.2) and
evaluated its PMF and upper tail with scipy.stats.poisson. Lesson 01
covers pathlib and unattended savefig; they are rebuilt here only so the
script stays self-contained. This step simulates 10,000 independent shifts.

    np.random.default_rng(seed)  Generator with a fixed seed (42)
    rng.poisson(lam, size=n)     n independent Poisson(lam) draws
    np.mean(draws == 0)          empirical P(X = 0) as a True/False mean
    np.var(draws, ddof=0)        Monte Carlo variance, divide by n
    np.bincount(...)             integer histogram of the simulated counts
    stats.poisson.pmf(xs, mu)    exact PMF overlaid on that histogram

main() prints exact versus simulated P(X = 0) and P(X >= 6), plus the
simulated mean and variance. A simulation can land close to the PMF
without replacing it.

Run it:
    python poisson_02_simulate_shifts.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.poisson is reused from Step 1: exact PMF and survival at lambda.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Seed 42 now drives the Generator in simulate_shifts(). Same lambda as
# Step 1 so the Monte Carlo can be compared with the exact PMF.
SEED = 42
LAMBDA = 3.2
# 10_000 independent synthetic shifts. The underscore is a thousands
# separator; Python reads it as 10000.
N_SHIFTS = 10_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def poisson_probabilities() -> dict[str, float]:
    """Return P(X = 0) and P(X >= 6) for the Step 1 Poisson, rebuilt here.

    stats.poisson(mu) is a frozen Poisson(lambda). .pmf(k) is P(X = k);
    .sf(k) is P(X > k), so sf(5) = P(X >= 6) for an integer count.
    This file does not import Step 1.
    """
    model = stats.poisson(mu=LAMBDA)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_least_six": float(model.sf(5)),
    }


# --- NEW (1) simulate_shifts() -----------------------------------------------
def simulate_shifts(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Draw n_shifts Poisson(lambda) event counts.

    Parameters
    ----------
    n_shifts:
        Number of independent synthetic shifts. Default N_SHIFTS = 10_000.
    seed:
        Generator seed. Default SEED = 42, the course-wide value.

    Returns
    -------
    np.ndarray
        Length n_shifts. Each entry is an integer count drawn from
        Poisson(LAMBDA). Re-running with the same seed reproduces the
        identical array.

    Notes
    -----
    np.random.default_rng(seed) builds a Generator, the current NumPy
    API for reproducible draws. rng.poisson(lam=..., size=...) draws
    independent Poisson counts. NumPy names the rate lam because lambda
    is a Python keyword; SciPy uses mu for the same number.
    """
    rng = np.random.default_rng(seed)
    return rng.poisson(lam=LAMBDA, size=n_shifts)
# ------------------------------------------------------------------------------


# --- NEW (2) simulation_summary() --------------------------------------------
def simulation_summary(draws: np.ndarray) -> dict[str, float]:
    """Return empirical tail rates, mean, and variance.

    Parameters
    ----------
    draws:
        Integer array from simulate_shifts(), one count per shift.

    Returns
    -------
    dict[str, float]
        n is the number of draws. p_zero and p_at_least_six are empirical
        frequencies of X = 0 and X >= 6. mean and variance are the Monte
        Carlo moments of the same array.

    Notes
    -----
    draws == 0 is a boolean array; np.mean of booleans is the proportion
    True, which estimates P(X = 0). The same trick with draws >= 6
    estimates the upper tail. np.var(..., ddof=0) divides by n, not n-1,
    because the 10,000 draws are the whole Monte Carlo sample, not a
    sample from a larger finite population. These frequencies can sit
    close to the exact PMF without replacing it.
    """
    return {
        "n": float(len(draws)),
        "p_zero": float(np.mean(draws == 0)),
        "p_at_least_six": float(np.mean(draws >= 6)),
        "mean": float(np.mean(draws)),
        "variance": float(np.var(draws, ddof=0)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(draws: np.ndarray) -> Path:
    """Save a histogram of simulated shifts against the Poisson PMF.

    Parameters
    ----------
    draws:
        Integer array from simulate_shifts().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Blue bars are relative frequencies from the seed-42 simulation.
    The red line is the exact Poisson(3.2) PMF from scipy.stats.poisson.
    Overlaying them shows that 10,000 draws recover the shape without
    making the histogram a substitute for the formula.
    """
    output_path = DIR_FIGURES / "poisson_02_simulate_shifts.png"
    xs = np.arange(0, 13)
    masses = stats.poisson.pmf(xs, mu=LAMBDA)
    # bincount tallies how many draws equal 0, 1, 2, ... minlength=13
    # guarantees bins 0..12 even if a count is missing. [:13] keeps that
    # plotting window; any rare draw of 13 or more is omitted from the
    # bars but still sits in draws for the printed summary.
    counts = np.bincount(draws, minlength=13)[:13] / len(draws)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, counts, color="#5B8DEF", width=0.8, label="Seed-42 simulation")
    # "o-" is circles connected by a line: the exact PMF, not a fit.
    ax.plot(xs, masses, "o-", color="#EC2661", lw=1.8, label="Poisson PMF")
    ax.set_xlabel("Events per shift x")
    ax.set_ylabel("Relative frequency / probability")
    ax.set_title("10,000 Simulated Shifts versus Poisson(3.2)")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 simulation report and write the overlay figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    exact = poisson_probabilities()
    draws = simulate_shifts()
    summary = simulation_summary(draws)
    figure_path = save_figure(draws)

    print("================================================================")
    print("LESSON 17 - STEP 2: SIMULATED SHIFTS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Simulated shifts                : {int(summary['n']):,}")
    print(f"Exact P(X = 0)                  : {exact['p_zero']:.6f}")
    # Empirical frequency, not a replacement for the PMF e^{-lambda}.
    print(f"Simulated P(X = 0)              : {summary['p_zero']:.6f}")
    print(f"Exact P(X >= 6)                 : {exact['p_at_least_six']:.6f}")
    print(f"Simulated P(X >= 6)             : {summary['p_at_least_six']:.6f}")
    print(f"Simulated mean                  : {summary['mean']:.6f}")
    # Under Poisson this should sit near lambda = 3.2, not prove it.
    print(f"Simulated variance              : {summary['variance']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

