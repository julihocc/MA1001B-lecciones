"""
Lesson 19 - Step 2: Interval Probability as Area
================================================
THE RECIPE
Start from continuous_rv_01_density.py, then introduce:
    1. interval_probability()   P(a < X < b) as area under the density
    2. closed_vs_open()         P(a < X < b) equals P(a <= X <= b)
    3. save_figure()            shade the target interval on the density

The same triangular service-time model on [2, 14] is rebuilt. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 built the triangular density
and showed that f(x) is a height, not a probability. Lesson 01 covers
pathlib and unattended savefig; they are rebuilt here only so the script
stays self-contained. This step reads P(a < X < b) as area under f.

    model.cdf(right) - model.cdf(left)   F(b) - F(a) = area on (a, b)
    open vs closed interval              endpoints do not change the area
    boolean mask (x >= a) & (x <= b)     elementwise AND on a NumPy grid
    ax.fill_between(x[mask], y[mask])    shade only the target interval

main() prints F(4), F(10), and the matching open/closed probabilities,
then shades (4, 10) on the density. Probability lives on intervals.

Run it:
    python continuous_rv_02_interval_probability.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.triang is reused from Step 1: pdf for the curve, cdf for area.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same support and mode as Step 1. This script still does
# not draw random numbers; SciPy evaluates exact CDF values.
SEED = 42
A = 2.0
B = 14.0
MODE = 6.0
# Target window for the area calculation: service between 4 and 10 min.
LOW = 4.0
HIGH = 10.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def service_time_model():
    """Return the triangular model for synthetic service time on [2, 14].

    Rebuilt from Step 1 so this file does not import that script. SciPy
    stores the triangle as triang(c, loc=a, scale=b-a) with
    c = (mode - a) / (b - a). model.pdf is the density height; model.cdf
    is F(x) = P(X <= x), the tool used below to read area as a difference.
    """
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)


# --- NEW (1) interval_probability() ------------------------------------------
def interval_probability(model, left: float, right: float) -> float:
    """Return P(left < X < right) as the area between the CDF values.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    left, right:
        Endpoints of the interval, in minutes. Require left < right.

    Returns
    -------
    float
        F(right) - F(left), which equals the integral of f from left to
        right. For a continuous X this is P(left < X < right).

    Notes
    -----
    Discrete lessons added PMF masses at isolated integers. A continuous
    density has no such masses, so probability is the area of a region
    under f. The fundamental theorem of calculus says that area is the
    CDF difference F(right) - F(left). float(...) converts SciPy's NumPy
    scalar into a plain Python float for printing.
    """
    return float(model.cdf(right) - model.cdf(left))
# ------------------------------------------------------------------------------


# --- NEW (2) closed_vs_open() ------------------------------------------------
def closed_vs_open(model, left: float, right: float) -> dict[str, float]:
    """Compare open and closed interval probabilities for continuous X.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    left, right:
        The same window passed to interval_probability().

    Returns
    -------
    dict[str, float]
        open is P(left < X < right). closed is P(left <= X <= right).
        cdf_left and cdf_right are F at the two endpoints, reported so
        the subtraction F(10) - F(4) is visible in the console.

    Notes
    -----
    For a continuous random variable, P(X = c) = 0 at every single c, so
        P(a < X < b) = P(a <= X <= b) = F(b) - F(a).
    Both keys therefore use the same CDF difference. Matching values are
    the lesson, not a rounding coincidence. Step 3 makes P(X = c) = 0
    geometric: the CDF has no jump.
    """
    open_prob = interval_probability(model, left, right)
    # Same F(right) - F(left): including the endpoints adds two zeros.
    closed_prob = float(model.cdf(right) - model.cdf(left))
    return {
        "open": open_prob,
        "closed": closed_prob,
        "cdf_left": float(model.cdf(left)),
        "cdf_right": float(model.cdf(right)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model, left: float, right: float, area: float) -> Path:
    """Shade P(4 < X < 10) on the triangular service-time density.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    left, right:
        Interval endpoints in minutes (4 and 10 in this lesson).
    area:
        The probability already computed as F(right) - F(left).

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy curve is the same f(x) as Step 1. Only the slice between 4
    and 10 is filled. That red region is the geometric picture of
    P(4 < X < 10): an area, not a point height.
    """
    output_path = DIR_FIGURES / "continuous_rv_02_interval_probability.png"
    x = np.linspace(A, B, 400)
    y = model.pdf(x)
    # Elementwise AND on two boolean arrays. Use & , not Python `and`,
    # which cannot combine NumPy masks. The mask selects grid points
    # inside [left, right] so fill_between shades only that interval.
    mask = (x >= left) & (x <= right)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    ax.fill_between(x[mask], y[mask], color="#EC2661", alpha=0.35,
                    label=f"P({left:.0f} < X < {right:.0f}) = {area:.4f}")
    ax.set_xlabel("Service time (minutes)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("Interval Probability Is Area, Not a Point Height")
    ax.set_xlim(A, B)
    ax.set_ylim(0, 0.22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 interval-probability report and write the figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = service_time_model()
    area = interval_probability(model, LOW, HIGH)
    comparison = closed_vs_open(model, LOW, HIGH)
    figure_path = save_figure(model, LOW, HIGH, area)

    print("================================================================")
    print("LESSON 19 - STEP 2: INTERVAL PROBABILITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Interval                        : ({LOW:.1f}, {HIGH:.1f})")
    print(f"F(4)                            : {comparison['cdf_left']:.6f}")
    print(f"F(10)                           : {comparison['cdf_right']:.6f}")
    # Area under f from 4 to 10, computed as F(10) - F(4).
    print(f"P(4 < X < 10)                   : {comparison['open']:.6f}")
    # Same number: each endpoint has probability 0.
    print(f"P(4 <= X <= 10)                 : {comparison['closed']:.6f}")
    print("Open and closed intervals match for continuous X")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

