"""
Lesson 19 - Step 3: A Continuous Point Carries No Probability
=============================================================
THE RECIPE
Start from continuous_rv_02_interval_probability.py, then introduce:
    1. shrinking_windows()      P(|X - c| < h) collapses toward 0
    2. cdf_has_no_jump()        F is continuous, so P(X = c) = 0
    3. save_figure()            plot the CDF with no jump at the mode

The same triangular service-time model is rebuilt. The limit is that
P(X = c) = 0 for every single minute c, even the mode.

How to read this file:
You already know Python through OOP. Steps 1-2 built the triangular
density and read P(a < X < b) as F(b) - F(a). Lesson 01 covers pathlib
and unattended savefig. This step shrinks that interval onto one point.

    P(|X - c| < h)           F(c + h) - F(c - h), area of a window
    h = 0.50, 0.10, 0.01     successive half-widths; the area falls
    F(c) - F(c - 1e-9)       numerical jump of the CDF at the mode
    P(X = c) = 0             a continuous CDF has no vertical step
    plt.subplots(1, 2)       CDF panel beside shrinking-window bars

main() prints the three window probabilities, F(6), the jump 0, and
P(X = 6) = 0. The mode is the tallest density, still a point of mass 0.

Run it:
    python continuous_rv_03_point_mass_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.triang is reused from Steps 1-2: cdf differences measure window
# area, and the CDF curve itself is the geometric test for a jump.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
A = 2.0
B = 14.0
MODE = 6.0
# Half-widths of nested windows around the mode. The sequence 0.50,
# 0.10, 0.01 forces the shaded area toward a single point.
WINDOWS = (0.50, 0.10, 0.01)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def service_time_model():
    """Return the triangular model for synthetic service time on [2, 14].

    Rebuilt from Step 1 so this file does not import earlier scripts.
    model.cdf(x) is F(x) = P(X <= x). A jump in F at c would be P(X = c);
    a continuous F has no jump, so every single minute has probability 0.
    """
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)


# --- NEW (1) shrinking_windows() ---------------------------------------------
def shrinking_windows(model, center: float) -> dict[str, float]:
    """Compute P(|X - center| < h) for successively smaller windows.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    center:
        The point c being tested. The lesson uses the mode 6, the
        tallest density, so the collapse is not an artifact of a tail.

    Returns
    -------
    dict[str, float]
        Keys "h_0.50", "h_0.10", "h_0.01" store
        F(center + h) - F(center - h) for each half-width in WINDOWS.

    Notes
    -----
    |X - c| < h is the open interval (c - h, c + h). Step 2 already
    identified that probability with a CDF difference. As h falls, the
    shaded area under f collapses onto a line, whose area is 0. That
    limit is P(X = c). The f-string f"h_{half_width:.2f}" builds the
    key from the numeric h so later prints can look up "h_0.50".
    """
    results: dict[str, float] = {}
    for half_width in WINDOWS:
        left = center - half_width
        right = center + half_width
        # Same area recipe as Step 2, now on a window that shrinks.
        results[f"h_{half_width:.2f}"] = float(
            model.cdf(right) - model.cdf(left)
        )
    return results
# ------------------------------------------------------------------------------


# --- NEW (2) cdf_has_no_jump() -----------------------------------------------
def cdf_has_no_jump(model, center: float) -> dict[str, float]:
    """Show that F has no jump at the mode, so a single point has mass 0.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    center:
        Evaluation point c. The lesson uses MODE = 6.

    Returns
    -------
    dict[str, float]
        F_at_mode is F(c). F_just_left is F(c - 1e-9), a numerically
        tiny step left of c. jump is the difference. P_X_equals_mode
        is the theoretical value 0, not a simulated estimate.

    Notes
    -----
    For any random variable, P(X = c) = F(c) - F(c-), the size of the
    jump at c. A discrete CDF jumps at every mass point. A continuous
    CDF is a continuous function, so that jump is 0 and P(X = c) = 0.
    1e-9 is small enough to stand in for "just left of c" without
    leaving the support [2, 14].
    """
    f_center = float(model.cdf(center))
    # 1e-9 minutes left of the mode: a numerical proxy for F(c-).
    f_left = float(model.cdf(center - 1e-9))
    return {
        "F_at_mode": f_center,
        "F_just_left": f_left,
        "jump": f_center - f_left,
        "P_X_equals_mode": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model, windows: dict[str, float]) -> Path:
    """Plot the continuous CDF and shrinking-window probabilities.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().
    windows:
        Dict from shrinking_windows() with keys "h_0.50", "h_0.10",
        "h_0.01".

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Left panel: F(x) rises smoothly through x = 6. A discrete mass would
    appear as a vertical step; there is none, so P(X = 6) = 0. Right
    panel: the three window areas fall toward 0, the same statement in
    bar-chart form.
    """
    output_path = DIR_FIGURES / "continuous_rv_03_point_mass_limit.png"
    x = np.linspace(A, B, 400)
    # Vectorized CDF: F at every grid point, a continuous curve.
    y = model.cdf(x)
    labels = ["h = 0.50", "h = 0.10", "h = 0.01"]
    values = [windows["h_0.50"], windows["h_0.10"], windows["h_0.01"]]

    # 1 row, 2 columns of Axes. axes[0] is the CDF; axes[1] is the bars.
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))

    axes[0].plot(x, y, color="#1A2E51", lw=2.2)
    axes[0].axvline(MODE, color="#EC2661", ls="--", lw=1.3)
    # Marker on F(6): the curve passes through it with no vertical jump.
    axes[0].plot(MODE, model.cdf(MODE), "o", color="#EC2661")
    axes[0].set_xlabel("Service time (minutes)")
    axes[0].set_ylabel("F(x) = P(X <= x)")
    axes[0].set_title("CDF Has No Jump at x = 6")
    axes[0].set_xlim(A, B)
    axes[0].set_ylim(0, 1.05)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    bars = axes[1].bar(labels, values, color=["#1A2E51", "#5B8DEF", "#EC2661"],
                       width=0.62)
    axes[1].set_ylabel("P(|X - 6| < h)")
    axes[1].set_title("Shrinking Windows Collapse to 0")
    axes[1].set_ylim(0, 0.18)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each bar with its probability so the label sits centered
    # just above the top. The three heights fall toward 0.
    for bar, value in zip(bars, values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4f}",
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
    """Run the Step 3 point-mass limit and write the two-panel figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = service_time_model()
    windows = shrinking_windows(model, MODE)
    jump = cdf_has_no_jump(model, MODE)
    figure_path = save_figure(model, windows)

    print("================================================================")
    print("LESSON 19 - STEP 3: POINT MASS LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Center c                        : {MODE:.1f}")
    # Three nested areas around the mode; each is smaller than the last.
    print(f"P(|X - 6| < 0.50)               : {windows['h_0.50']:.6f}")
    print(f"P(|X - 6| < 0.10)               : {windows['h_0.10']:.6f}")
    print(f"P(|X - 6| < 0.01)               : {windows['h_0.01']:.6f}")
    print(f"F(6)                            : {jump['F_at_mode']:.6f}")
    print(f"F(6-)                           : {jump['F_just_left']:.6f}")
    # Jump of 0 is the CDF statement of P(X = 6) = 0.
    print(f"Jump F(6) - F(6-)               : {jump['jump']:.6f}")
    print(f"P(X = 6)                        : {jump['P_X_equals_mode']:.6f}")
    print("Limit: a continuous point carries probability 0")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

