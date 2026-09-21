"""
Lesson 16 - Step 1: Sampling Without Replacement
================================================
NEW IN THIS STEP: lot_parameters(), hypergeometric_p_zero(), and save_figure().

Context:
A fully synthetic lot of N = 80 units contains K = 6 defectives. An inspector
draws n = 10 units without replacement. The defect count X follows a
hypergeometric distribution. The first quantity of interest is P(X = 0).

The Recipe
----------
Build the first complete program in this order:
    1. lot_parameters()         N, K, n, and the sampling fraction n/N
    2. hypergeometric_p_zero()  P(X = 0) from scipy.stats.hypergeom
    3. save_figure()            PMF with the clean-sample mass highlighted

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, the Agg
backend, and unattended savefig. Those idioms return here with a short
pointer, not a second treatise. Lessons 14-15 used scipy.stats.binom for
independent trials with a constant p. This lesson switches to hypergeom
because the lot is finite and units are not replaced.

New in this step:
    without replacement       each draw changes the remaining lot, so trials
                              are dependent (unlike binomial inspections)
    Hypergeometric(N, K, n)   X = defectives in a sample of n from a lot of
                              N that already holds K defectives
    scipy.stats.hypergeom     SciPy names M, n, N do not match textbook N, K, n
    sampling fraction n/N     10/80 = 0.125 is not small; binomial is Step 3
    np.arange support         X can be 0, 1, ..., min(K, n)

main() reports N, K, n, n/N = 0.125, and P(X = 0) = 0.436326, then writes
the PMF with the x = 0 bar highlighted.

Run it:
    python hypergeometric_01_without_replacement.py
"""

# Path, Agg, savefig, and close: same unattended-figure idiom as Lesson 01.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the distribution library from Lessons 14-15. hypergeom is
# the without-replacement family; binom (with replacement / independent
# trials) returns in Step 3 as an approximation, not as the true model.
from scipy import stats

# Agg must be selected before pyplot; see Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Course-wide seed. This step does not draw random numbers; the lot is
# fully specified by N, K, and n. The same 42 is reserved so later lessons
# can simulate from it.
SEED = 42
# Textbook hypergeometric ingredients. N is the finite lot, K the number
# of defectives already in it, n the draw size. Sampling is WITHOUT
# replacement: a unit cannot appear twice, so successive draws are
# dependent. Binomial would need independent trials with constant p.
N_POP = 80
K_DEFECTIVE = 6
N_DRAW = 10
# figures/ next to this package, independent of the shell's working directory.
# Path construction, mkdir, savefig, and close: see Lesson 01.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) lot_parameters() ------------------------------------------------
def lot_parameters() -> dict[str, int | float]:
    """Return the hypergeometric ingredients N, K, n, and n/N.

    Returns
    -------
    dict[str, int | float]
        N, K, n as integers and sampling_fraction = n/N as a float.
        dict[str, int | float] is a type hint: keys are strings; each
        value is an int or a float. Python does not enforce it at run time.

    Notes
    -----
    n/N = 10/80 = 0.125. A common rule of thumb is that a binomial
    approximation needs a small sampling fraction (often n/N < 0.05 or
    0.10). 0.125 is not small, so this lesson uses hypergeometric as the
    exact model. The function packages module constants; it does not
    read a warehouse file.
    """
    return {
        "N": N_POP,
        "K": K_DEFECTIVE,
        "n": N_DRAW,
        "sampling_fraction": N_DRAW / N_POP,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) hypergeometric_p_zero() -----------------------------------------
def hypergeometric_p_zero() -> float:
    """Return P(X = 0) for X ~ Hypergeometric(N=80, K=6, n=10).

    Returns
    -------
    float
        The probability that a without-replacement draw of 10 units
        contains zero defectives. float(...) unwraps SciPy's np.float64
        into a Python float for printing.

    Notes
    -----
    The hypergeometric PMF counts combinations, not independent trials:

        P(X = x) = C(K, x) * C(N - K, n - x) / C(N, n)

    For a clean sample, x = 0, so C(6, 0) = 1 and the chance is
    C(74, 10) / C(80, 10): every 10-subset of the 74 good units, over
    every 10-subset of the full lot. Combinations came from Lesson 06.

    SciPy's argument names do NOT match the textbook:

        Textbook:  N = lot size, K = defectives in the lot, n = draws
        SciPy:     M = lot size, n = defectives in the lot, N = draws

    This call is therefore pmf(0, M=80, n=6, N=10). The keyword n= is
    K_DEFECTIVE, not N_DRAW. Swapping them is the usual bug.

    Binomial P(X = 0) = (1 - K/N)^n would pretend each draw still has
    p = 6/80 even after units leave the lot. That comparison is Step 3.
    """
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(p_zero: float) -> Path:
    """Save the hypergeometric PMF with P(X = 0) highlighted.

    Parameters
    ----------
    p_zero:
        P(X = 0) from hypergeometric_p_zero(), used only as the text
        label above the red bar.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    A discrete PMF is a bar at each integer x. The support is
    0, 1, ..., min(K, n) because the sample cannot hold more defectives
    than exist in the lot or than were drawn. Course colors: red for
    the event of interest, navy for the rest.
    """
    output_path = DIR_FIGURES / "hypergeometric_01_without_replacement.png"
    # arange(0, m + 1) is 0, 1, ..., m. min(K, n) = 6 here.
    xs = np.arange(0, min(K_DEFECTIVE, N_DRAW) + 1)
    # One vectorized PMF call. Same SciPy names as hypergeometric_p_zero:
    # M is textbook N, n is textbook K, N is textbook n.
    masses = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    colors = ["#EC2661" if x == 0 else "#1A2E51" for x in xs]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(xs, masses, color=colors, width=0.62)
    ax.set_xlabel("Defectives in the sample x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Hypergeometric(N=80, K=6, n=10)")
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # Center the label on the x = 0 bar, slightly above its height.
    ax.text(
        bars[0].get_x() + bars[0].get_width() / 2,
        p_zero + 0.02,
        f"{p_zero:.4f}",
        ha="center",
        fontweight="bold",
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 hypergeometric calculation and print the lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    params = lot_parameters()
    p_zero = hypergeometric_p_zero()
    figure_path = save_figure(p_zero)

    print("================================================================")
    print("LESSON 16 - STEP 1: WITHOUT REPLACEMENT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Lot size N                      : {params['N']}")
    print(f"Defectives in lot K             : {params['K']}")
    print(f"Draw size n                     : {params['n']}")
    # .6f is six digits after the decimal, matching the lesson README.
    print(f"Sampling fraction n/N           : {params['sampling_fraction']:.6f}")
    print(f"P(X = 0) hypergeometric         : {p_zero:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Python sets __name__ to "__main__" only when this file is the program
# being executed. The idiom is the standard script entry point; keep it
# even though each lesson file is self-contained. See Lesson 01.
if __name__ == "__main__":
    main()

