"""
Lesson 14 - Step 2: Binomial PMF, CDF, Mean, and Variance
=========================================================
THE RECIPE
Start from binomial_01_bernoulli_trials.py, then introduce:
    1. binomial_pmf_cdf()   P(X = 0) and P(X <= 2) from scipy.stats.binom
    2. binomial_moments()   mean np and variance np(1-p)
    3. save_figure()        binomial PMF with the left tail highlighted

The same n = 20 and p = 0.08 are rebuilt from constants. No earlier lesson
script is imported.

How to read this file:
You already know Python through OOP. Step 1 defined one Bernoulli trial and
the four binomial assumptions. Lesson 01 covers pathlib and unattended
savefig; they are rebuilt here only so the script stays self-contained.
This step evaluates the binomial PMF and CDF with scipy.stats.binom.

    stats.binom(n, p)    frozen Binomial(n, p) object (n and p locked)
    model.pmf(k)         P(X = k), the probability mass function
    model.cdf(k)         P(X <= k), the cumulative distribution function
    stats.binom.pmf(xs, n, p)   same PMF evaluated on a whole array of k
    np.arange(0, n + 1)  the support 0, 1, ..., n

main() prints P(X = 0), P(X <= 2), np, and np(1-p), then saves the PMF
with the left tail x = 0, 1, 2 in red.

Run it:
    python binomial_02_pmf_cdf.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.binom is the
# binomial family: PMF, CDF, and related methods for X ~ Binomial(n, p).
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same n and p as Step 1. This script still does not draw
# random numbers; scipy.stats.binom evaluates exact probabilities.
SEED = 42
N_TRIALS = 20
P_DEFECT = 0.08
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def bernoulli_trial() -> dict[str, float]:
    """Return the same two-point distribution introduced in Step 1.

    p_defect is the Bernoulli success chance p. p_clean is q = 1 - p.
    Rebuilt here so this file does not import Step 1.
    """
    return {
        "p_defect": P_DEFECT,
        "p_clean": 1.0 - P_DEFECT,
    }


# --- NEW (1) binomial_pmf_cdf() ----------------------------------------------
def binomial_pmf_cdf(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Return P(X = 0) and P(X <= 2) for X ~ Binomial(n, p).

    Parameters
    ----------
    n:
        Number of independent Bernoulli inspections. Default N_TRIALS = 20.
    p:
        Constant defect chance on each inspection. Default P_DEFECT = 0.08.

    Returns
    -------
    dict[str, float]
        p_zero is P(X = 0), the chance of a fully clean lot.
        p_at_most_two is P(X <= 2), the left-tail CDF at 2.

    Notes
    -----
    The binomial PMF is
        P(X = x) = C(n, x) * p^x * (1 - p)^(n - x),
    where C(n, x) counts the subsets of x defectives among n units.
    At x = 0 that formula collapses to (1 - p)^n = 0.92^20.
    The CDF at 2 is the sum of the PMF at 0, 1, and 2.

    stats.binom(n=n, p=p) freezes those two parameters into a model
    object. Then model.pmf(k) and model.cdf(k) evaluate one integer k.
    float(...) converts the NumPy scalar that SciPy returns into a plain
    Python float for printing.
    """
    # Frozen rv: n and p are stored on the object, so later calls pass
    # only the k values. The unbound form stats.binom.pmf(k, n=n, p=p)
    # is equivalent and is used in save_figure() below.
    model = stats.binom(n=n, p=p)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_most_two": float(model.cdf(2)),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) binomial_moments() ----------------------------------------------
def binomial_moments(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Return the binomial mean np and variance np(1-p).

    Parameters
    ----------
    n, p:
        Same binomial ingredients as binomial_pmf_cdf().

    Returns
    -------
    dict[str, float]
        mean is E[X] = n p (expected defect count).
        variance is Var(X) = n p (1 - p).

    Notes
    -----
    These closed forms follow from adding n i.i.d. Bernoulli(p) indicators.
    Each indicator has mean p and variance p(1-p); independence lets the
    variances add. np is a mean, not a probability. For n = 20 and
    p = 0.08, np = 1.6 and np(1-p) = 1.472.
    """
    return {
        "mean": n * p,
        "variance": n * p * (1.0 - p),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(n: int = N_TRIALS, p: float = P_DEFECT) -> Path:
    """Save the binomial PMF and highlight x = 0, 1, 2.

    Parameters
    ----------
    n, p:
        Parameters of X ~ Binomial(n, p). Defaults match the lesson lot.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The bar at integer x is P(X = x). Red bars are the left tail that the
    CDF call model.cdf(2) adds up. Navy bars are the rest of the support
    3, 4, ..., n. Because p is small, most mass sits on the left.
    """
    output_path = DIR_FIGURES / "binomial_02_pmf_cdf.png"
    # arange(0, n + 1) is 0, 1, ..., n: every integer the binomial can take.
    xs = np.arange(0, n + 1)
    # Unbound PMF: pass the whole array of x values plus n and p. SciPy
    # returns an array of masses that sums to 1 (up to rounding).
    masses = stats.binom.pmf(xs, n=n, p=p)
    # List comprehension paints x <= 2 red (the CDF event) and the rest navy.
    colors = ["#EC2661" if x <= 2 else "#1A2E51" for x in xs]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color=colors, width=0.8)
    ax.set_xlabel("Defect count x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Binomial(n=20, p=0.08); Left Tail x <= 2 in Red")
    # One tick per integer so the discrete support is visible.
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 PMF, CDF, and moment report.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    trial = bernoulli_trial()
    probs = binomial_pmf_cdf()
    moments = binomial_moments()
    figure_path = save_figure()

    print("================================================================")
    print("LESSON 14 - STEP 2: BINOMIAL PMF AND CDF")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"n                               : {N_TRIALS}")
    print(f"p                               : {trial['p_defect']:.6f}")
    print(f"P(X = 0)                        : {probs['p_zero']:.6f}")
    print(f"P(X <= 2)                       : {probs['p_at_most_two']:.6f}")
    print(f"Mean np                         : {moments['mean']:.6f}")
    print(f"Variance np(1-p)                : {moments['variance']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

