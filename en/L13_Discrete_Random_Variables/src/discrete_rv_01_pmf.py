"""
Lesson 13 - Step 1: Probability Mass Function
=============================================
NEW IN THIS STEP: defect_support(), pmf_values(), and save_figure().

Context:
A fully synthetic incoming-lot inspection records the defect count X in
{0, 1, 2, 3} with probabilities 0.50, 0.30, 0.15, and 0.05. A discrete
random variable is specified by its support and its probability mass
function (PMF). The masses must be nonnegative and sum to 1.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy,
the Agg backend, and unattended savefig. Those idioms return here with a
short pointer, not a second treatise. This lesson does not use pandas or
scipy.stats: the PMF is a pair of NumPy arrays typed in by hand.

New in this step:
    np.array(..., dtype=int/float)  lock the support and the masses
    .copy()                         return a new array, not a view of the constant
    ax.vlines + ax.plot             stem plot of the point masses P(X = x)
    masses.sum() / np.all           the two PMF conditions

main() reads the support and masses, checks that they form a valid PMF, and
writes the stem-plot evidence figure.

Run it:
    python discrete_rv_01_pmf.py
"""

from pathlib import Path

# numpy (imported as np) is the numeric-array library. matplotlib draws the
# stem plot. pathlib / Agg / savefig are the same unattended-figure setup as
# Lesson 01; see data_foundations_01_population_sample.py for the full notes.
import matplotlib
import numpy as np

# Agg must be selected before pyplot is imported. Same Lesson 01 idiom.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved so later lessons that simulate from this PMF can reuse seed 42.
# This script is deterministic: the masses are constants, not random draws.
SEED = 42
# Support of X: the finite list of values that can occur. A discrete random
# variable puts all of its probability on a countable set; here that set is
# the four integers 0, 1, 2, 3. dtype=int keeps them as counts, not floats.
SUPPORT = np.array([0, 1, 2, 3], dtype=int)
# Probability mass function: P(X = x) at each support point, in the same
# order as SUPPORT. The masses must be nonnegative and sum to 1. dtype=float
# so later arithmetic (CDF, expectation) stays in floating point.
PMF = np.array([0.50, 0.30, 0.15, 0.05], dtype=float)
# figures/ next to this package. Same Path(__file__) construction as Lesson 01.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) defect_support() ------------------------------------------------
def defect_support() -> np.ndarray:
    """Return the possible defect counts for the synthetic lot.

    Returns
    -------
    np.ndarray
        A copy of SUPPORT: the integers 0, 1, 2, 3. The annotation
        `-> np.ndarray` is a type hint; Python does not enforce it at
        run time.

    Notes
    -----
    The support is the set of x with P(X = x) > 0. Returning .copy()
    means a caller who mutates the array cannot change the module
    constant. Nothing is read from disk; the values are written above.
    """
    # .copy() allocates a new array with the same values. Without it,
    # the caller would receive a view of SUPPORT and could overwrite it.
    return SUPPORT.copy()
# ------------------------------------------------------------------------------


# --- NEW (2) pmf_values() ----------------------------------------------------
def pmf_values() -> np.ndarray:
    """Return the probability masses P(X = x) on the support.

    Returns
    -------
    np.ndarray
        A copy of PMF: 0.50, 0.30, 0.15, 0.05, aligned with SUPPORT.

    Notes
    -----
    A PMF assigns a nonnegative mass to every point in the support.
    For a discrete random variable these masses must sum to 1: they
    are probabilities of mutually exclusive, exhaustive outcomes.
    This is not a density; there is no area under a curve between
    integers. scipy.stats is not used; the masses are typed in by hand.
    """
    return PMF.copy()
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(support: np.ndarray, masses: np.ndarray) -> Path:
    """Save the probability mass function as a stem plot.

    Parameters
    ----------
    support:
        The defect counts 0, 1, 2, 3.
    masses:
        P(X = x) at those counts, in the same order.

    Returns
    -------
    Path
        Absolute path of the PNG that was written. The function's only
        side effect is that file; it does not display a window.

    Notes
    -----
    A stem plot (vertical lines plus markers) is the usual picture of a
    discrete PMF: probability lives at isolated points, not on intervals.
    tight_layout / savefig / close are the Lesson 01 figure idiom.
    """
    output_path = DIR_FIGURES / "discrete_rv_01_pmf.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # vlines draws one vertical segment from y=0 to y=mass at each x.
    # That segment is the "stem" of the point mass.
    ax.vlines(support, 0, masses, colors="#1A2E51", lw=2.4)
    # Overlay a marker at the top of each stem so the mass is easy to see.
    ax.plot(support, masses, "o", color="#EC2661", markersize=9)
    # zip pairs each x with its mass so the numeric label sits above the
    # marker. ha="center" centers the text on the stem.
    for x_value, mass in zip(support, masses):
        ax.text(
            x_value,
            mass + 0.025,
            f"{mass:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    # Force ticks at the four support points; do not interpolate extra x ticks.
    ax.set_xticks(support)
    ax.set_xlabel("Defect count x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("PMF of Synthetic Defect Count X")
    ax.set_ylim(0, 0.65)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    # dpi=170 is the course default. Never call plt.show(); close() frees memory.
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Check the PMF conditions, print the masses, and save the stem plot.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    support = defect_support()
    masses = pmf_values()
    # Two PMF conditions: the masses sum to 1, and none is negative.
    # float(...) unwraps the NumPy scalar so the printed value is a Python float.
    mass_sum = float(masses.sum())
    # np.all is True only when every entry satisfies masses >= 0.
    nonnegative = bool(np.all(masses >= 0))
    figure_path = save_figure(support, masses)

    print("================================================================")
    print("LESSON 13 - STEP 1: PROBABILITY MASS FUNCTION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    # .tolist() turns the NumPy array into a Python list for readable printing.
    print(f"Support                         : {support.tolist()}")
    print(f"P(X = 0)                        : {masses[0]:.6f}")
    print(f"P(X = 1)                        : {masses[1]:.6f}")
    print(f"P(X = 2)                        : {masses[2]:.6f}")
    print(f"P(X = 3)                        : {masses[3]:.6f}")
    print(f"Sum of masses                   : {mass_sum:.6f}")
    print(f"All masses nonnegative          : {nonnegative}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Python sets __name__ to the string "__main__" only when this file is the
# program being executed. The idiom is the standard script entry point.
if __name__ == "__main__":
    main()

