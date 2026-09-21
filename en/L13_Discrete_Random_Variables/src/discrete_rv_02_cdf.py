"""
Lesson 13 - Step 2: Cumulative Distribution Function
====================================================
THE RECIPE
Start from discrete_rv_01_pmf.py, then introduce:
    1. cdf_values()     F(x) = P(X <= x) by accumulating the PMF
    2. interval_from_cdf()  P(a < X <= b) = F(b) - F(a)
    3. save_figure()    step-function CDF on the defect support

The same synthetic defect-count distribution is rebuilt from the same
constants. No earlier lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 defined the support and the
PMF. Those functions are copied here so the script stays self-contained;
comments concentrate on the NEW bands. pathlib / Agg / savefig are the
Lesson 01 figure idiom. scipy.stats is not used.

New in this step:
    np.cumsum           running sum of the masses, which is the CDF
    F(b) - F(a)         interval probability P(a < X <= b)
    ax.step(..., where="post")  right-continuous step plot of F

main() accumulates the PMF into F, reads F(0) through F(3), and computes
P(X <= 1) and P(1 < X <= 3) from the CDF.

Run it:
    python discrete_rv_02_cdf.py
"""

from pathlib import Path

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
# Same support and PMF as Step 1. Copied, not imported, so the script
# stays self-contained. dtype=int for counts; dtype=float for masses.
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

    Copied from Step 1. The PMF is the input to the CDF: F accumulates
    these four numbers from left to right.
    """
    return PMF.copy()


# --- NEW (1) cdf_values() ----------------------------------------------------
def cdf_values(masses: np.ndarray) -> np.ndarray:
    """Return F(x) = P(X <= x) on the ordered support.

    Parameters
    ----------
    masses:
        P(X = x) in increasing-x order, from pmf_values().

    Returns
    -------
    np.ndarray
        The running sums: F(0) = P(X=0), F(1) = P(X=0)+P(X=1), ...,
        F(3) = 1 when the masses form a valid PMF.

    Notes
    -----
    The CDF of a discrete random variable is a right-continuous step
    function: it is flat between support points and jumps by P(X = x)
    at each x. np.cumsum does that accumulation when the masses are
    already ordered by x. scipy.stats.rv_discrete is not used.
    """
    # cumsum([p0, p1, p2, p3]) = [p0, p0+p1, p0+p1+p2, p0+p1+p2+p3].
    return np.cumsum(masses)
# ------------------------------------------------------------------------------


# --- NEW (2) interval_from_cdf() ---------------------------------------------
def interval_from_cdf(cdf: np.ndarray, left: int, right: int) -> float:
    """Return P(left < X <= right) from CDF values on {0, 1, 2, 3}.

    Parameters
    ----------
    cdf:
        F(0), F(1), F(2), F(3) in that order, from cdf_values().
    left, right:
        Integers used as indexes into cdf. Because the support is
        {0, 1, 2, 3}, the value x is stored at index x.

    Returns
    -------
    float
        F(right) - F(left), which equals P(left < X <= right).
        If left < 0, F(left) is taken to be 0 so the result is F(right)
        = P(X <= right).

    Notes
    -----
    For a discrete CDF, P(X <= b) = F(b) and P(X <= a) = F(a), so
    P(a < X <= b) = F(b) - F(a). The left endpoint is excluded because
    F(a) already includes the mass at a.
    """
    # cdf[right] is F(right) because support values equal their indexes.
    f_right = float(cdf[right])
    # left = -1 is the convention in main() for "no lower cutoff":
    # P(X <= 1) = F(1) - 0. Any left < 0 is treated the same way.
    f_left = 0.0 if left < 0 else float(cdf[left])
    return f_right - f_left
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(support: np.ndarray, cdf: np.ndarray) -> Path:
    """Save the CDF as a right-continuous step function.

    Parameters
    ----------
    support:
        The defect counts 0, 1, 2, 3.
    cdf:
        F at those counts, from cdf_values().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    F(x) = 0 for x < 0 and F(x) = 1 for x >= 3. Between support points
    the function is constant; at each support point it jumps by the
    corresponding PMF mass. tight_layout / savefig / close are the
    Lesson 01 figure idiom.
    """
    output_path = DIR_FIGURES / "discrete_rv_02_cdf.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Extra x-coordinates so the step is visible left of 0 and right of 3.
    x_plot = np.array([-0.6, 0, 1, 2, 3, 3.6])
    # y_plot[0] is F just left of 0. The remaining entries are F at 0, 1,
    # 2, 3 and then 1.0 to the right of 3.
    y_plot = np.array([0.0, cdf[0], cdf[1], cdf[2], cdf[3], 1.0])
    # where="post" holds the current y until the next x, then jumps. That
    # is the right-continuous convention for a discrete CDF: F(x) includes
    # the mass at x.
    ax.step(x_plot, y_plot, where="post", color="#1A2E51", lw=2.2)
    # Markers at the support points so the jump heights are easy to read.
    ax.plot(support, cdf, "o", color="#EC2661", markersize=9)
    for x_value, value in zip(support, cdf):
        ax.text(
            x_value,
            value + 0.04,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    ax.set_xticks(support)
    ax.set_xlabel("Defect count x")
    ax.set_ylabel("F(x) = P(X <= x)")
    ax.set_title("CDF Accumulates the PMF")
    ax.set_ylim(-0.05, 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Accumulate the PMF into a CDF and print two interval probabilities.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    support = defect_support()
    masses = pmf_values()
    cdf = cdf_values(masses)
    # left = -1 means "no lower cutoff", so this is F(1) = P(X <= 1).
    p_at_most_1 = interval_from_cdf(cdf, -1, 1)
    # P(1 < X <= 3) = F(3) - F(1). The mass at 1 is excluded.
    p_between_1_and_3 = interval_from_cdf(cdf, 1, 3)
    figure_path = save_figure(support, cdf)

    print("================================================================")
    print("LESSON 13 - STEP 2: CUMULATIVE DISTRIBUTION FUNCTION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"F(0) = P(X <= 0)                : {cdf[0]:.6f}")
    print(f"F(1) = P(X <= 1)                : {cdf[1]:.6f}")
    print(f"F(2) = P(X <= 2)                : {cdf[2]:.6f}")
    print(f"F(3) = P(X <= 3)                : {cdf[3]:.6f}")
    print(f"P(X <= 1) from CDF              : {p_at_most_1:.6f}")
    print(f"P(1 < X <= 3) = F(3)-F(1)       : {p_between_1_and_3:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

