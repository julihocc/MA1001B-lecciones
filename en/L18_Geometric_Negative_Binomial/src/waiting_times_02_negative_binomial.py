"""
Lesson 18 - Step 2: Negative-Binomial Waiting Time
==================================================
THE RECIPE
Start from waiting_times_01_geometric.py, then introduce:
    1. negative_binomial_parameters()  r = 3 successes, E[X] = r/p
    2. trials_until_r()    convert scipy nbinom failures into trial counts
    3. save_figure()       PMF of trials until the third success

X is the number of independent trials until r = 3 defectives are found, each
with p = 0.12. The geometric model is the special case r = 1.

How to read this file:
You already know Python through OOP. Step 1 defined X ~ Geometric(p) as
the trial of the first success and evaluated it with scipy.stats.geom.
Lesson 01 covers pathlib and unattended savefig; they are rebuilt here
only so the script stays self-contained. This step waits for r = 3
successes instead of one.

    stats.nbinom         SciPy counts failures before r successes
    x_trials - r         convert trial count X into that failure count
    E[X] = r/p           mean trials until r successes; r = 1 is geometric
    P(X = r) = p^r       all r successes on the first r trials
    ax.axvline           mark the mean r/p = 25 on the PMF

main() prints r, p, r/p, the variance, and P(X = 3) = p^3, then saves the
negative-binomial PMF. No earlier lesson script is imported.

Run it:
    python waiting_times_02_negative_binomial.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.geom is reused from Step 1. stats.nbinom is new: it counts
# failures before r successes, not the trial number of the r-th success.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same p as Step 1. This script still does not draw
# random numbers; scipy.stats.nbinom evaluates exact probabilities.
SEED = 42
P_SUCCESS = 0.12
# r: stop at the third defective. The geometric model is the case r = 1.
R_SUCCESSES = 3
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def geometric_parameters() -> dict[str, float]:
    """Return p and E[X] = 1/p for trials until the first success.

    Rebuilt from Step 1 so this file does not import that script. The
    geometric mean 1/p is the r = 1 special case of the negative-binomial
    mean r/p printed below.
    """
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
    }


# --- NEW (1) negative_binomial_parameters() ----------------------------------
def negative_binomial_parameters() -> dict[str, float | int]:
    """Return r, p, and E[X] = r/p for trials until r successes.

    Returns
    -------
    dict[str, float | int]
        r is the required number of successes (an int). p is the constant
        success chance. mean is E[X] = r/p, the expected trial of the
        r-th success. variance is Var(X) = r (1-p) / p^2.

    Notes
    -----
    X is the number of independent Bernoulli(p) trials until r successes.
    The geometric waiting time is the special case r = 1, which recovers
    E[X] = 1/p and Var(X) = (1-p)/p^2 from Step 1.

    For r = 3 and p = 0.12, E[X] = 25 trials. r/p is a mean wait, not a
    probability. These closed forms need independent trials with constant
    p; Step 3 will drop both assumptions.

    The annotation float | int means a value may be either type; Python
    does not enforce it at run time.
    """
    return {
        "r": R_SUCCESSES,
        "p": P_SUCCESS,
        "mean": R_SUCCESSES / P_SUCCESS,
        "variance": R_SUCCESSES * (1.0 - P_SUCCESS) / P_SUCCESS ** 2,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) trials_until_r() ------------------------------------------------
def trials_until_r(x_trials: np.ndarray) -> np.ndarray:
    """Return P(X = x) for X = failures before r successes plus r.

    Parameters
    ----------
    x_trials:
        Integer trial numbers of the r-th success. Each value must be at
        least r, because r successes cannot occur in fewer than r trials.

    Returns
    -------
    np.ndarray
        P(X = x) at each entry of x_trials, using the OpenStax trial-count
        parameterization.

    Notes
    -----
    scipy.stats.nbinom does not use this parameterization. Its PMF is
        stats.nbinom.pmf(k, n=r, p=p) = P(Y = k),
    where Y is the number of failures before r successes and n is r, not
    a trial count. The conversion is
        Y = X - r,    so    P(X = x) = nbinom.pmf(x - r, n=r, p=p).
    At the left endpoint x = r there are zero failures, so
        P(X = r) = p^r.
    For r = 3 that is p^3 = 0.12^3 = 0.001728.
    """
    # Shift the trial count down by r to reach SciPy's failure count.
    failures = x_trials - R_SUCCESSES
    # Unbound nbinom PMF: n is the success target r, p is the Bernoulli
    # chance. Passing an array of failure counts returns an array of masses.
    return stats.nbinom.pmf(failures, n=R_SUCCESSES, p=P_SUCCESS)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure() -> Path:
    """Save the negative-binomial PMF of trials until r = 3.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Support starts at x = r = 3, not at 0 or 1: the third success cannot
    occur before trial 3. The dashed line is E[X] = r/p = 25, a location
    on the trial axis, not a probability. The plotted window stops at 40,
    so a long right tail is omitted from the figure.
    """
    output_path = DIR_FIGURES / "waiting_times_02_negative_binomial.png"
    # arange(r, 41) is 3, 4, ..., 40: every plotted trial of the 3rd success.
    xs = np.arange(R_SUCCESSES, 41)
    masses = trials_until_r(xs)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.8)
    # Vertical guide at the closed-form mean, not at a PMF bar.
    ax.axvline(
        R_SUCCESSES / P_SUCCESS,
        color="#EC2661",
        linestyle="--",
        lw=2.0,
        label="E[X] = r/p = 25",
    )
    ax.set_xlabel("Trial of the third success x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Negative Binomial: Trials Until r = 3 Successes")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 negative-binomial report and write the PMF.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    geom = geometric_parameters()
    nb = negative_binomial_parameters()
    # np.array([r]) is the left endpoint: zero failures, so P(X = r) = p^r.
    p_min = float(trials_until_r(np.array([R_SUCCESSES]))[0])
    figure_path = save_figure()

    print("================================================================")
    print("LESSON 18 - STEP 2: NEGATIVE BINOMIAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Geometric E[X] = 1/p            : {geom['mean']:.6f}")
    print(f"r                               : {nb['r']}")
    print(f"p                               : {nb['p']:.6f}")
    print(f"E[X] = r/p                      : {nb['mean']:.6f}")
    print(f"Var(X)                          : {nb['variance']:.6f}")
    print(f"P(X = 3) = p^3                  : {p_min:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

