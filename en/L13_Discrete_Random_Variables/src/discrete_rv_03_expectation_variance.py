"""
Lesson 13 - Step 3: Expectation and Variance
============================================
THE RECIPE
Start from discrete_rv_02_cdf.py, then introduce:
    1. expected_value()     E[X] = sum x P(X = x)
    2. second_moment()      E[X^2] = sum x^2 P(X = x)
    3. variance_from_moments()  Var(X) = E[X^2] - (E[X])^2

The limit is the identity E[X^2] != (E[X])^2. Squaring the mean is not the
second moment, and the gap between them is the variance.

How to read this file:
You already know Python through OOP. Steps 1-2 built the PMF and CDF.
Those functions are copied here so the script stays self-contained;
comments concentrate on the NEW bands. pathlib / Agg / savefig are the
Lesson 01 figure idiom. scipy.stats is not used; every moment is a
weighted sum over the four masses.

New in this step:
    np.sum(support * masses)         E[X], the probability-weighted mean
    np.sum((support ** 2) * masses)  E[X^2], the second moment
    moment2 - mean ** 2              Var(X); not the square of the mean
    np.isclose                       exact == is the wrong check for floats

main() computes E[X], (E[X])^2, E[X^2], and Var(X), then shows they are
not the same number.

Run it:
    python discrete_rv_03_expectation_variance.py
"""

from pathlib import Path

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
# Same support and PMF as Steps 1-2. Copied, not imported.
SUPPORT = np.array([0, 1, 2, 3], dtype=int)
PMF = np.array([0.50, 0.30, 0.15, 0.05], dtype=float)
# figures/ next to this package. Same Path(__file__) construction as Lesson 01.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def defect_support() -> np.ndarray:
    """Return a copy of the defect-count support {0, 1, 2, 3}.

    Copied from Step 1 so this script stays self-contained. See
    discrete_rv_01_pmf.py for the longer notes.
    """
    return SUPPORT.copy()


def pmf_values() -> np.ndarray:
    """Return a copy of the masses P(X = x) on the support.

    Copied from Step 1. Expectation and variance are weighted sums
    that use these four masses as the weights.
    """
    return PMF.copy()


# --- NEW (1) expected_value() ------------------------------------------------
def expected_value(support: np.ndarray, masses: np.ndarray) -> float:
    """Return E[X] as a sum of x P(X = x).

    Parameters
    ----------
    support:
        The defect counts 0, 1, 2, 3.
    masses:
        P(X = x) at those counts, in the same order.

    Returns
    -------
    float
        The probability-weighted average of x.

    Notes
    -----
    For a discrete random variable, E[X] = sum_x x P(X = x). It is not
    the most likely value (the mode here is 0) and it need not be a
    support point. Elementwise support * masses multiplies each x by
    its mass; np.sum adds those four products.
    """
    # * on two arrays of equal length is elementwise, not a matrix product.
    # float(...) unwraps the NumPy scalar so callers receive a Python float.
    return float(np.sum(support * masses))
# ------------------------------------------------------------------------------


# --- NEW (2) second_moment() -------------------------------------------------
def second_moment(support: np.ndarray, masses: np.ndarray) -> float:
    """Return E[X^2] as a sum of x^2 P(X = x).

    Parameters
    ----------
    support, masses:
        Same arrays as expected_value().

    Returns
    -------
    float
        The probability-weighted average of x squared.

    Notes
    -----
    ** is elementwise exponentiation, so support ** 2 is [0, 1, 4, 9].
    E[X^2] is not (E[X])^2: squaring after averaging is a different
    operation from averaging the squares. The gap is the variance.
    """
    return float(np.sum((support ** 2) * masses))
# ------------------------------------------------------------------------------


# --- NEW (3) variance_from_moments() -----------------------------------------
def variance_from_moments(mean: float, moment2: float) -> float:
    """Return Var(X) = E[X^2] - (E[X])^2.

    Parameters
    ----------
    mean:
        E[X] from expected_value().
    moment2:
        E[X^2] from second_moment().

    Returns
    -------
    float
        The variance of X. Equivalent to E[(X - E[X])^2], but this
        computational form uses the two moments already in hand.

    Notes
    -----
    mean ** 2 is (E[X])^2, not E[X^2]. If those two numbers were equal,
    the variance would be zero and X would be constant.
    """
    return moment2 - mean ** 2
# ------------------------------------------------------------------------------


def save_figure(mean: float, mean_squared: float, moment2: float, variance: float) -> Path:
    """Contrast E[X]^2 with E[X^2] and display the variance.

    Parameters
    ----------
    mean, mean_squared, moment2, variance:
        E[X], (E[X])^2, E[X^2], and Var(X), in that order.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Four bars, one per quantity. The pedagogical point is visual: the
    third bar is taller than the second, and the fourth bar is their
    difference. tight_layout / savefig / close are the Lesson 01 idiom.
    """
    output_path = DIR_FIGURES / "discrete_rv_03_expectation_variance.png"
    labels = ["E[X]", "(E[X])^2", "E[X^2]", "Var(X)"]
    values = [mean, mean_squared, moment2, variance]
    colors = ["#1A2E51", "#5B8DEF", "#EC2661", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Value")
    ax.set_title("E[X^2] Is Not (E[X])^2; The Gap Is Var(X)")
    ax.set_ylim(0, 1.6)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each Rectangle with its numeric height so the label sits
    # just above the bar. get_x() + get_width()/2 is the bar's center.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.04,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path


def main() -> None:
    """Compute E[X], E[X^2], and Var(X), then reject E[X^2] = (E[X])^2.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    support = defect_support()
    masses = pmf_values()
    mean = expected_value(support, masses)
    moment2 = second_moment(support, masses)
    # Squaring the mean is a different operation from the second moment.
    mean_squared = mean ** 2
    variance = variance_from_moments(mean, moment2)
    figure_path = save_figure(mean, mean_squared, moment2, variance)

    print("================================================================")
    print("LESSON 13 - STEP 3: EXPECTATION AND VARIANCE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"E[X]                            : {mean:.6f}")
    print(f"(E[X])^2                        : {mean_squared:.6f}")
    print(f"E[X^2]                          : {moment2:.6f}")
    print(f"Var(X) = E[X^2] - (E[X])^2      : {variance:.6f}")
    # np.isclose tests approximate equality of floats. Exact == is the
    # wrong habit even when both numbers happen to be binary-exact.
    print(f"E[X^2] equals (E[X])^2          : {np.isclose(moment2, mean_squared)}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

