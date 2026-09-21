"""
Lesson 25 - Step 1: Standard Error of a Sample Proportion
=========================================================
NEW IN THIS STEP: proportion_se(), np_conditions(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. proportion_se()      SE(phat) = sqrt(p (1 - p) / n)
    2. np_conditions()      np and n(1-p) checks for a normal picture
    3. save_figure()        N(p, SE) density for the sampling distribution

Context:
A fully synthetic late-delivery indicator has population proportion
p = 0.18. Samples of n = 120 tickets have
SE(phat) = sqrt(p(1-p)/n). The np and n(1-p) checks both exceed 5.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lessons 23-24 treated the sampling
distribution of xbar. This script switches the statistic to phat.

    phat                     sample proportion X/n; a statistic, not p
    SE(phat)                 sqrt(p (1 - p) / n), the SD of that statistic
    np and n(1-p)            expected success and failure counts
    stats.norm(loc, scale)   Normal(p, SE) overlay for phat
    dict[str, float]         a type hint: string keys, float values

main() reports p, n, np = 21.6, n(1-p) = 98.4, and SE = 0.035071, then
writes the normal density of phat. No earlier lesson script is imported.

Run it:
    python sampling_proportion_01_se_phat.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy evaluates the SE square root. scipy.stats
# supplies the Normal(p, SE) family used as the overlay for phat.
import matplotlib
import numpy as np
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# Population proportion of late tickets. p is a parameter; phat is not.
P = 0.18
# Sample size: number of iid tickets in one sample, not the number of
# replications. Those replications arrive in Step 2.
N = 120
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) proportion_se() -------------------------------------------------
def proportion_se(p: float = P, n: int = N) -> float:
    """Return SE(phat) = sqrt(p (1 - p) / n).

    Parameters
    ----------
    p:
        Population proportion of late tickets. Default is the module
        constant P = 0.18. This is the parameter, not a sample phat.
    n:
        Sample size. Default N = 120 tickets.

    Returns
    -------
    float
        The standard error of the sample proportion. float(...) unwraps
        NumPy's np.float64 into a Python float for printing.

    Notes
    -----
    If X ~ Binomial(n, p) counts late tickets and phat = X/n, then
    E[phat] = p and Var(phat) = p(1-p)/n. The standard error is the
    square root of that variance: the SD of the sampling distribution
    of phat, not the SD of one Bernoulli ticket.

    The formula uses the population p. Substituting a single observed
    phat belongs to later inference lessons, not to this sampling
    distribution. Larger n shrinks SE by 1/sqrt(n), the same rate as
    SE(xbar) in Lessons 23-24.
    """
    return float(np.sqrt(p * (1.0 - p) / n))
# ------------------------------------------------------------------------------


# --- NEW (2) np_conditions() -------------------------------------------------
def np_conditions(p: float = P, n: int = N) -> dict[str, float]:
    """Check the np and n(1-p) counts used for a normal approximation.

    Parameters
    ----------
    p, n:
        Same population proportion and sample size as proportion_se().

    Returns
    -------
    dict[str, float]
        p and n (n stored as float so the dict is homogeneous).
        np = n*p: expected late-ticket count.
        n_one_minus_p = n*(1-p): expected on-time count.
        se: SE(phat) from proportion_se().
        mean: E[phat] = p.

    Notes
    -----
    A common classroom rule is that both np and n(1-p) should be at
    least 5 before drawing phat as a bell. Those counts are conditions
    for the normal picture, not for the existence of phat: X/n is
    defined for any n >= 1.

    Here np = 120 * 0.18 = 21.6 and n(1-p) = 98.4, both well above 5,
    so Step 1 is allowed to overlay N(p, SE). Step 3 drops n to 20 so
    np = 3.6 < 5 and that overlay fails.
    """
    return {
        "p": p,
        "n": float(n),
        "np": n * p,
        "n_one_minus_p": n * (1.0 - p),
        "se": proportion_se(p, n),
        "mean": p,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """Plot the approximating normal density for phat when n = 120.

    Parameters
    ----------
    summary:
        The dict from np_conditions(). Only the key "se" is read; p
        and n come from the module constants so the curve stays locked
        to this lesson.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy curve is N(p, SE(phat)), a continuous overlay for a
    discrete statistic: phat = X/n only hits 0, 1/120, ..., 1. With
    np and n(1-p) both above 5 the spacing 1/n is small relative to
    SE, so the bell is a usable picture of the sampling distribution.

    The dashed marker is the parameter p = 0.18, which is E[phat], not
    a realized sample proportion.
    """
    output_path = DIR_FIGURES / "sampling_proportion_01_se_phat.png"
    se = summary["se"]
    # Four SEs on each side of p covers essentially all of the bell.
    x = np.linspace(P - 4 * se, P + 4 * se, 400)
    # loc is the mean of phat (the parameter p). scale is SE(phat), not
    # the Bernoulli SD sqrt(p(1-p)).
    y = stats.norm(loc=P, scale=se).pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="N(p, SE)")
    ax.axvline(P, color="#EC2661", ls="--", lw=1.4, label="p = 0.18")
    ax.set_xlabel("Sample proportion phat")
    ax.set_ylabel("Density")
    ax.set_title("n = 120, p = 0.18: SE = sqrt(p(1-p)/n)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 SE report and write the N(p, SE) figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    summary = np_conditions()
    figure_path = save_figure(summary)

    print("================================================================")
    print("LESSON 25 - STEP 1: SE OF PHAT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Population p                    : {summary['p']:.6f}")
    print(f"Sample size n                   : {int(summary['n'])}")
    # Expected late-ticket count; both this and n(1-p) must exceed 5
    # before the normal overlay is used as a picture of phat.
    print(f"np                              : {summary['np']:.6f}")
    print(f"n(1 - p)                        : {summary['n_one_minus_p']:.6f}")
    print(f"SE(phat)                        : {summary['se']:.6f}")
    print("np and n(1-p) both exceed 5")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

