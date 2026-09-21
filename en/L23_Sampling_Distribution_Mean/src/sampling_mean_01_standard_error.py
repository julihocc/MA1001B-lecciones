"""
Lesson 23 - Step 1: Standard Error of the Sample Mean
=====================================================
NEW IN THIS STEP: population_model(), standard_error(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. population_model()   frozen Normal(mu=80, sigma=12) cycle times
    2. standard_error()     SE(xbar) = sigma / sqrt(n) for an iid mean
    3. save_figure()        population density beside xbar densities

Context:
A fully synthetic cycle-time population is Normal(mu=80, sigma=12)
minutes. The sampling distribution of xbar has mean mu and standard
error sigma / sqrt(n). Sample sizes n = 9 and n = 36 are compared.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds the standard error of
the sample mean and overlays the sampling densities of xbar.

    stats.norm(loc, scale)   frozen Normal(mu, sigma) object
    model.pdf(x)             density of that Normal at an array of x
    sigma / np.sqrt(n)       SE of an iid sample mean (not of one X)
    ax.plot / ax.axvline     overlay densities and mark mu

main() reports SE for n = 9 and n = 36, prints their ratio, and writes the
evidence figure. No earlier lesson script is imported.

Run it:
    python sampling_mean_01_standard_error.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.norm is the
# Normal family used for both the population of X and the law of xbar.
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# mu: mean of one cycle time X, and also E[xbar] for an iid sample.
MU = 80.0
# sigma: sd of one cycle time X. It is NOT the sd of xbar.
SIGMA = 12.0
# Two sample sizes whose square roots are integers: sqrt(9)=3, sqrt(36)=6.
N_SMALL = 9
N_LARGE = 36
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) population_model() ----------------------------------------------
def population_model():
    """Return the Normal(80, 12) cycle-time population.

    Returns
    -------
    scipy.stats._distn_infrastructure.rv_frozen
        A frozen Normal(mu=80, sigma=12). loc is the mean; scale is the
        sd of one observation X, not of the sample mean.

    Notes
    -----
    stats.norm(loc=MU, scale=SIGMA) stores mu and sigma on the object so
    later .pdf / .cdf calls pass only the x values. This is the law of
    one cycle time. The sampling law of xbar is a different Normal: same
    mean mu, but scale SE = sigma / sqrt(n). save_figure() rebuilds the
    same frozen laws from constants so this file stays self-contained.
    """
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NEW (2) standard_error() ------------------------------------------------
def standard_error(n: int, sigma: float = SIGMA) -> float:
    """Return SE = sigma / sqrt(n) for an iid sample mean.

    Parameters
    ----------
    n:
        Sample size. Larger n shrinks SE; it does not change sigma.
    sigma:
        Population sd of one observation X. Default SIGMA = 12.

    Returns
    -------
    float
        sigma / sqrt(n), the standard deviation of xbar when the n
        draws are iid from the defined population.

    Notes
    -----
    For iid X_1, ..., X_n with Var(X_i) = sigma^2,
        Var(xbar) = sigma^2 / n, so SE(xbar) = sigma / sqrt(n).
    That is a property of the sampling distribution, not of one X.
    For n = 9, SE = 12 / 3 = 4. For n = 36, SE = 12 / 6 = 2.
    np.sqrt(n) is the square root; n must be positive.
    """
    return sigma / np.sqrt(n)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(se_small: float, se_large: float) -> Path:
    """Plot sampling densities of xbar for n = 9 and n = 36.

    Parameters
    ----------
    se_small, se_large:
        Theoretical SE(xbar) at n = 9 and n = 36, from standard_error().

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Three Normal densities share the mean mu = 80. The dotted curve is
    the population of X (scale = sigma = 12). The two solid curves are
    sampling distributions of xbar, with scales SE(9)=4 and SE(36)=2.
    Larger n peaks the density of xbar around mu; it does not shrink
    the population sigma.
    """
    output_path = DIR_FIGURES / "sampling_mean_01_standard_error.png"
    # Grid wide enough to show the population (mu +/- 4 sigma). The
    # sampling densities of xbar sit much tighter around mu.
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    # Frozen Normals: population of X, then xbar at each n.
    pop = stats.norm(loc=MU, scale=SIGMA)
    small = stats.norm(loc=MU, scale=se_small)
    large = stats.norm(loc=MU, scale=se_large)

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Dotted: one observation. Solid: the mean of n observations.
    ax.plot(x, pop.pdf(x), color="#646464", lw=1.6, ls=":",
            label="Population sigma = 12")
    ax.plot(x, small.pdf(x), color="#5B8DEF", lw=2.2,
            label=f"xbar n=9, SE={se_small:.2f}")
    ax.plot(x, large.pdf(x), color="#EC2661", lw=2.2,
            label=f"xbar n=36, SE={se_large:.2f}")
    # Vertical line at mu: E[xbar] = mu for every n.
    ax.axvline(MU, color="#1A2E51", ls="--", lw=1.2)
    ax.set_xlabel("Cycle time (minutes)")
    ax.set_ylabel("Density")
    ax.set_title("Larger n Shrinks SE = sigma / sqrt(n)")
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
    """Run the Step 1 SE report and write the sampling-density figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    se_small = standard_error(N_SMALL)
    se_large = standard_error(N_LARGE)
    figure_path = save_figure(se_small, se_large)

    print("================================================================")
    print("LESSON 23 - STEP 1: STANDARD ERROR")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Population mean mu              : {MU:.6f}")
    print(f"Population sd sigma             : {SIGMA:.6f}")
    print(f"SE for n = 9                    : {se_small:.6f}")
    print(f"SE for n = 36                   : {se_large:.6f}")
    # sqrt(36)/sqrt(9) = 6/3 = 2, so SE(9) is twice SE(36).
    print(f"SE ratio SE(9) / SE(36)         : {se_small / se_large:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

