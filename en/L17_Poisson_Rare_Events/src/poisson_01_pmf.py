"""
Lesson 17 - Step 1: Poisson PMF for Rare Events
===============================================
NEW IN THIS STEP: poisson_rate(), poisson_probabilities(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. poisson_rate()            lambda, and the equal-mean variance
    2. poisson_probabilities()   P(X = 0) and P(X >= 6) from scipy.stats.poisson
    3. save_figure()             Poisson PMF with those two events in red

Context:
A fully synthetic operations desk records the number of stoppage events X
on one shift. The mean rate is lambda = 3.2 events per shift. The Poisson
model gives P(X = 0) and the upper tail P(X >= 6).

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds the Poisson count and
the equal-mean-and-variance property.

    stats.poisson(mu)    frozen Poisson(lambda) object (rate locked as mu)
    model.pmf(k)         P(X = k), the probability mass function
    model.sf(k)          P(X > k); for integer X, sf(5) = P(X >= 6)
    dict[str, float]     a type hint: string keys, float values
    np.arange(0, 13)     plotting window 0, 1, ..., 12, not the full support

main() reports lambda, the Poisson mean and variance, P(X = 0), and
P(X >= 6) for one synthetic shift and writes the PMF evidence figure.
No earlier lesson script is imported.

Run it:
    python poisson_01_pmf.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the integer support for the PMF
# bars. The aliases are the same ones used from Lesson 01 onward.
import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.poisson is
# the Poisson family: PMF, CDF, and survival for X ~ Poisson(mu).
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# lambda: mean number of stoppage events on one shift. It is a rate, not
# a probability, and under Poisson it equals both E[X] and Var(X).
LAMBDA = 3.2
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) poisson_rate() --------------------------------------------------
def poisson_rate() -> dict[str, float]:
    """Return the Poisson mean and the equal-mean variance.

    Returns
    -------
    dict[str, float]
        lambda is the mean rate of events per shift. mean and variance
        are both equal to that same lambda: the equality is a Poisson
        property, not a fact measured from data.

    Notes
    -----
    A Poisson random variable X counts events in a fixed interval when
    events are independent and occur at a constant rate. Here the interval
    is one synthetic shift and the rate is lambda = 3.2. The PMF is
        P(X = x) = e^{-lambda} * lambda^x / x!,    x = 0, 1, 2, ...
    Unlike the binomial there is no fixed n and no per-trial p. X is a
    count of events, not a waiting time (waiting times appear in Lesson 18).
    """
    return {
        "lambda": LAMBDA,
        "mean": LAMBDA,
        "variance": LAMBDA,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) poisson_probabilities() -----------------------------------------
def poisson_probabilities() -> dict[str, float]:
    """Return P(X = 0) and P(X >= 6) for X ~ Poisson(3.2).

    Returns
    -------
    dict[str, float]
        p_zero is P(X = 0), a quiet shift with no stoppages.
        p_at_least_six is P(X >= 6), a busy upper tail.

    Notes
    -----
    At x = 0 the Poisson PMF collapses to e^{-lambda}. The upper tail
    is P(X >= 6) = 1 - P(X <= 5) = 1 - F(5). SciPy's survival function
    model.sf(k) is P(X > k), so for an integer count sf(5) = P(X >= 6).

    stats.poisson(mu=LAMBDA) freezes the rate. SciPy names the Poisson
    mean mu because lambda is a Python keyword; numpy.random uses lam
    for the same reason. float(...) unwraps the NumPy scalar SciPy
    returns into a plain Python float for printing.
    """
    # Frozen rv: mu is stored on the object, so later calls pass only
    # the k values. The unbound form stats.poisson.pmf(k, mu=LAMBDA)
    # is equivalent and is used in save_figure() below.
    model = stats.poisson(mu=LAMBDA)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_least_six": float(model.sf(5)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure() -> Path:
    """Save the Poisson PMF with x = 0 and x >= 6 highlighted.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The bar at integer x is P(X = x). Red bars are the two events in
    poisson_probabilities(): a quiet shift (x = 0) and the busy tail
    (x >= 6). Navy bars are the rest of the plotting window. The Poisson
    support is all nonnegative integers; arange(0, 13) is only a window
    so the figure stays readable.
    """
    output_path = DIR_FIGURES / "poisson_01_pmf.png"
    # arange(0, 13) is 0, 1, ..., 12: enough integers to see the shape
    # around lambda = 3.2 without drawing a long empty right tail.
    xs = np.arange(0, 13)
    # Unbound PMF: pass the whole array of x values plus mu. SciPy
    # returns an array of masses; the infinite support sums to 1, so
    # this truncated window sums to a little less than 1.
    masses = stats.poisson.pmf(xs, mu=LAMBDA)
    # List comprehension paints x = 0 and x >= 6 red and the rest navy.
    colors = ["#EC2661" if (x == 0 or x >= 6) else "#1A2E51" for x in xs]

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color=colors, width=0.8)
    ax.set_xlabel("Events per shift x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Poisson(lambda = 3.2); x = 0 and x >= 6 in Red")
    # One tick per integer so the discrete support is visible.
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 Poisson PMF report and write the evidence figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    rate = poisson_rate()
    probs = poisson_probabilities()
    figure_path = save_figure()

    print("================================================================")
    print("LESSON 17 - STEP 1: POISSON PMF")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    # lambda = 3.2 is a mean rate of events per shift, not a chance.
    print(f"lambda                          : {rate['lambda']:.6f}")
    print(f"Poisson mean                    : {rate['mean']:.6f}")
    # Equal mean and variance is the Poisson assumption, not a data fact.
    print(f"Poisson variance                : {rate['variance']:.6f}")
    # P(X = 0) = exp(-3.2). P(X >= 6) is the survival function at 5.
    print(f"P(X = 0)                        : {probs['p_zero']:.6f}")
    print(f"P(X >= 6)                       : {probs['p_at_least_six']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

