"""
Lesson 18 - Step 1: Geometric Waiting Time
==========================================
NEW IN THIS STEP: geometric_parameters(), geometric_probabilities(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. geometric_parameters()      p, E[X] = 1/p, and Var(X) = (1-p)/p^2
    2. geometric_probabilities()   P(X = 1) and P(X <= 5) from scipy.stats.geom
    3. save_figure()               geometric PMF of trials until first success

Context:
A fully synthetic audit samples independent units until the first defective
is found. Each trial has success probability p = 0.12. The waiting time X is
the trial number of the first success, so P(X = 1) = p and E[X] = 1/p.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lesson 14 built the Bernoulli trial
that this wait is made of. This script adds the geometric waiting time.

    stats.geom(p)        frozen Geometric(p): X = trial of first success
    model.pmf(k)         P(X = k) = (1-p)^{k-1} p; support starts at 1
    model.cdf(k)         P(X <= k)
    stats.geom.mean(p)   E[X] = 1/p, matching the closed form
    ax.bar twice         navy PMF, then redraw x = 1 in red

main() reports p, P(X = 1), P(X <= 5), 1/p, and the matching SciPy mean,
then writes the geometric PMF. No earlier lesson script is imported.

Run it:
    python waiting_times_01_geometric.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy supplies the integer support of X.
# The aliases are the same ones used from Lesson 01 onward.
import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.geom is the
# geometric family: PMF, CDF, and mean for X = trial of first success.
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# p: P(defective) on one independent inspection. "Success" here means
# finding a defective, the same Bernoulli language as Lesson 14.
P_SUCCESS = 0.12
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) geometric_parameters() ------------------------------------------
def geometric_parameters() -> dict[str, float]:
    """Return p, E[X] = 1/p, and Var(X) = (1-p)/p^2 for the first success.

    Returns
    -------
    dict[str, float]
        p is the constant success chance on each independent trial.
        mean is E[X] = 1/p, the expected trial number of the first success.
        variance is Var(X) = (1 - p) / p^2.

    Notes
    -----
    X is the trial number of the first success, so X takes values 1, 2, 3,
    ... and P(X = 1) = p. That is SciPy's stats.geom parameterization and
    the OpenStax waiting-time model. A different convention counts failures
    before the first success and then has mean (1-p)/p; this lesson does
    not use that version.

    1/p is a mean wait, not a probability. For p = 0.12, E[X] = 8.333...
    trials. The closed forms require independent trials with this same p.
    Step 3 will drop both of those assumptions by letting p decline.
    """
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
        "variance": (1.0 - P_SUCCESS) / P_SUCCESS ** 2,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) geometric_probabilities() ---------------------------------------
def geometric_probabilities() -> dict[str, float]:
    """Return P(X = 1) and P(X <= 5) for X ~ Geometric(p).

    Returns
    -------
    dict[str, float]
        p_first_trial is P(X = 1) = p, success on the first inspection.
        p_at_most_five is P(X <= 5), the CDF at 5.

    Notes
    -----
    The geometric PMF is
        P(X = x) = (1 - p)^{x-1} p,    x = 1, 2, 3, ...
    At x = 1 the power is 0, so P(X = 1) = p. The CDF at 5 is
        P(X <= 5) = 1 - (1 - p)^5,
    the chance the first defective appears on or before trial 5.

    stats.geom(p=P_SUCCESS) freezes p into a model object. Then
    model.pmf(k) and model.cdf(k) evaluate one integer k. float(...)
    converts the NumPy scalar that SciPy returns into a plain Python
    float for printing. The unbound form stats.geom.pmf(xs, p=...) is
    equivalent and is used in save_figure() below.
    """
    # Frozen rv: p is stored on the object, so later calls pass only k.
    model = stats.geom(p=P_SUCCESS)
    return {
        "p_first_trial": float(model.pmf(1)),
        "p_at_most_five": float(model.cdf(5)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure() -> Path:
    """Save the geometric PMF of waiting times.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The bar at integer x is P(X = x). Support starts at 1, not 0: there is
    no "trial 0" when X is the trial of first success. The red bar is
    x = 1, where the mass equals p. Navy bars are x = 2, ..., 20. Because
    p = 0.12 is small, the PMF declines slowly to the right.
    """
    output_path = DIR_FIGURES / "waiting_times_01_geometric.png"
    # arange(1, 21) is 1, 2, ..., 20: the first 20 geometric outcomes.
    xs = np.arange(1, 21)
    # Unbound PMF: pass the whole array of x values plus p. SciPy returns
    # an array of masses. They do not sum to 1 here because the tail
    # x >= 21 is omitted from the plot.
    masses = stats.geom.pmf(xs, p=P_SUCCESS)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.8)
    # Second bar redraws only x = 1, on top of the navy bar, so P(X = 1)
    # = p is visually marked. masses[0] is P(X = 1) because xs starts at 1.
    ax.bar([1], [masses[0]], color="#EC2661", width=0.8)
    ax.set_xlabel("Trial of first success x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Geometric(p = 0.12): P(X = 1) = p")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 geometric report and write the waiting-time PMF.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    params = geometric_parameters()
    probs = geometric_probabilities()
    # Closed-form check: stats.geom.mean(p) must equal 1/p for this
    # trials-until-first-success parameterization.
    scipy_mean = float(stats.geom.mean(p=P_SUCCESS))
    figure_path = save_figure()

    print("================================================================")
    print("LESSON 18 - STEP 1: GEOMETRIC WAITING TIME")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"p                               : {params['p']:.6f}")
    print(f"P(X = 1)                        : {probs['p_first_trial']:.6f}")
    print(f"P(X <= 5)                       : {probs['p_at_most_five']:.6f}")
    print(f"E[X] = 1/p                      : {params['mean']:.6f}")
    print(f"scipy geom mean                 : {scipy_mean:.6f}")
    print(f"Var(X)                          : {params['variance']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

