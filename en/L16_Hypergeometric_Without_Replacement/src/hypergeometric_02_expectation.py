"""
Lesson 16 - Step 2: Hypergeometric Expectation
==============================================
THE RECIPE
Start from hypergeometric_01_without_replacement.py, then introduce:
    1. hypergeometric_mean()    E[X] = n K / N
    2. hypergeometric_pmf()     full PMF on 0, ..., min(K, n)
    3. save_figure()            PMF with the mean marked

The same lot N = 80, K = 6, n = 10 is rebuilt from constants. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, the Agg
backend, and unattended savefig. Step 1 computed P(X = 0) from
scipy.stats.hypergeom; this script copies those lot constants and comments
only the NEW bands.

New in this step:
    E[X] = nK/N               hypergeometric mean; same arithmetic as np
                              with p = K/N, even though draws are dependent
    linearity of expectation  each of the n positions has P(defective) = K/N
    scipy.stats.hypergeom.mean  same awkward M, n, N names as pmf
    ax.axvline                a mean of 0.75 is not a possible value of X

main() prints nK/N = 0.750000, confirms it against SciPy, and marks that
mean on the PMF.

Run it:
    python hypergeometric_02_expectation.py
"""

# Path, Agg, savefig, and close: same unattended-figure idiom as Lesson 01.
from pathlib import Path

import matplotlib
import numpy as np
# hypergeom is the without-replacement family. Argument names M, n, N still
# do not match textbook N, K, n; see Step 1.
from scipy import stats

# Agg must be selected before pyplot; see Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical lot to Step 1. SEED stays reserved; this script does not draw.
SEED = 42
N_POP = 80
K_DEFECTIVE = 6
N_DRAW = 10
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def lot_parameters() -> dict[str, int | float]:
    """Return the hypergeometric ingredients N, K, n, and n/N.

    Same packaging as Step 1. n/N = 0.125 is not small, so the model
    remains hypergeometric even while this step studies the mean.

    Returns
    -------
    dict[str, int | float]
        N, K, n as integers and sampling_fraction = n/N as a float.
    """
    return {
        "N": N_POP,
        "K": K_DEFECTIVE,
        "n": N_DRAW,
        "sampling_fraction": N_DRAW / N_POP,
    }


def hypergeometric_p_zero() -> float:
    """Return P(X = 0) for X ~ Hypergeometric(N=80, K=6, n=10).

    Same SciPy call as Step 1: pmf(0, M=80, n=6, N=10). Keyword n is
    the number of defectives in the lot (textbook K), not the draw size.

    Returns
    -------
    float
        P(a clean sample). Kept so the console can reprint Step 1 next
        to the new mean.
    """
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))


# --- NEW (1) hypergeometric_mean() -------------------------------------------
def hypergeometric_mean() -> float:
    """Return E[X] = n K / N.

    Returns
    -------
    float
        10 * 6 / 80 = 0.75 defectives expected in the sample.

    Notes
    -----
    The draws are dependent because sampling is without replacement, yet
    the mean still factors as n times K/N. Linearity of expectation does
    not need independence: each of the n positions in the sample has the
    same marginal chance K/N of being defective, so those n indicators
    add to nK/N.

    That is also the binomial mean np with p = K/N. Matching means do
    not make the two models the same: P(X = 0) still differs. Step 3
    shows the gap.
    """
    return N_DRAW * K_DEFECTIVE / N_POP
# ------------------------------------------------------------------------------


# --- NEW (2) hypergeometric_pmf() --------------------------------------------
def hypergeometric_pmf() -> tuple[np.ndarray, np.ndarray]:
    """Return the support and the hypergeometric masses.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        xs: integers 0, 1, ..., min(K, n).
        masses: P(X = x) at each of those points, from
        scipy.stats.hypergeom.pmf. The type hint documents two NumPy
        arrays; Python does not enforce it at run time.

    Notes
    -----
    Support stops at min(K, n) = 6: the sample cannot hold more
    defectives than exist in the lot. SciPy names remain M = lot size,
    n = defectives in the lot, N = draws. Passing the whole xs array
    evaluates the PMF in one vectorized call.
    """
    xs = np.arange(0, min(K_DEFECTIVE, N_DRAW) + 1)
    masses = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    return xs, masses
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(xs: np.ndarray, masses: np.ndarray, mean: float) -> Path:
    """Save the PMF with a vertical line at E[X] = nK/N.

    Parameters
    ----------
    xs, masses:
        Support and probabilities from hypergeometric_pmf().
    mean:
        E[X] = 0.75 from hypergeometric_mean().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    ax.axvline draws a vertical line at a horizontal coordinate that
    need not be an integer. 0.75 sits between x = 0 and x = 1, which is
    allowed: the mean of a discrete random variable is not required to
    be a possible value.
    """
    output_path = DIR_FIGURES / "hypergeometric_02_expectation.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.62)
    ax.axvline(mean, color="#EC2661", linestyle="--", lw=2.0, label=f"E[X] = {mean:.2f}")
    ax.set_xlabel("Defectives in the sample x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Hypergeometric Mean E[X] = nK/N = 0.75")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Compare nK/N with SciPy's hypergeometric mean and export the PMF.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    params = lot_parameters()
    mean = hypergeometric_mean()
    xs, masses = hypergeometric_pmf()
    # Same M, n, N mapping as pmf: M is textbook N, n is textbook K.
    scipy_mean = float(stats.hypergeom.mean(M=N_POP, n=K_DEFECTIVE, N=N_DRAW))
    figure_path = save_figure(xs, masses, mean)

    print("================================================================")
    print("LESSON 16 - STEP 2: HYPERGEOMETRIC MEAN")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"n K / N                         : {mean:.6f}")
    print(f"scipy hypergeom mean            : {scipy_mean:.6f}")
    print(f"P(X = 0)                        : {hypergeometric_p_zero():.6f}")
    print(f"Sampling fraction n/N           : {params['sampling_fraction']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01.
if __name__ == "__main__":
    main()

