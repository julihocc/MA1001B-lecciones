"""
Lesson 19 - Step 1: Continuous Density for Service Time
=======================================================
NEW IN THIS STEP: service_time_model(), density_at_points(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. service_time_model()     triangular density on [2, 14]
    2. density_at_points()      f(x) at the ends and the mode
    3. save_figure()            plot the density; shade total area 1

Context:
A fully synthetic help-desk clock records service time X on [2, 14]
minutes. The operating model is a triangular density with mode 6.
Unlike a discrete PMF, the height f(x) is not a probability.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds a continuous density
with scipy.stats.triang and numpy.

    stats.triang(c, loc, scale)  frozen triangular model on [loc, loc+scale]
    model.pdf(x)                 density height f(x), not P(X = x)
    model.cdf(x)                 F(x) = P(X <= x)
    model.mean()                 E[X] = (a + b + mode) / 3
    np.linspace(a, b, n)         n equally spaced x values from a to b
    ax.fill_between              shade area under the curve
    dict[str, float]             a type hint: string keys, float values

main() reports f(2), f(6), f(14), the mean, and total area 1, then writes
the density figure. No earlier lesson script is imported.

Run it:
    python continuous_rv_01_density.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the x-grid for the density curve.
# scipy.stats supplies the triangular family (pdf, cdf, mean).
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
# Support of X: service time lives on the closed interval [a, b] minutes.
A = 2.0
B = 14.0
# Mode: the peak of the triangle. Most likely *region*, not a point mass.
MODE = 6.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) service_time_model() --------------------------------------------
def service_time_model():
    """Return the triangular model for synthetic service time on [2, 14].

    Returns
    -------
    frozen stats.triang
        After this call, pdf/cdf/mean no longer need loc and scale:
        those parameters are stored on the object.

    Notes
    -----
    SciPy parameterizes the triangle as triang(c, loc=a, scale=b-a).
    The shape c is the relative location of the mode:
        c = (mode - a) / (b - a) = (6 - 2) / (14 - 2) = 1/3,
    so the mode sits at loc + c * scale = 2 + (1/3)*12 = 6.
    The peak height is 2 / (b - a) = 1/6. That number is a density
    height, not P(X = 6). A discrete PMF from Lessons 13-18 put mass on
    isolated points; a continuous density puts probability on intervals.
    """
    # Relative mode in SciPy's [0, 1] scale, not the minute-valued MODE.
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NEW (2) density_at_points() ---------------------------------------------
def density_at_points(model) -> dict[str, float]:
    """Evaluate density, mean, and total area for the service-time model.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().

    Returns
    -------
    dict[str, float]
        f_at_a and f_at_b are the endpoint heights (both 0 for a triangle
        that meets the axis). f_at_mode is the peak 2/(b-a) = 1/6.
        mean is E[X] = (a + b + mode) / 3. total_area is F(b) - F(a),
        which must be 1 for a valid density.

    Notes
    -----
    model.pdf(x) returns a density height. Reading f(6) = 0.166667 as
    "16.7% chance that service lasts exactly 6 minutes" is the lesson's
    main misconception: P(X = 6) is 0, shown in Step 3. float(...) turns
    the NumPy scalar that SciPy returns into a plain Python float.
    """
    return {
        "f_at_a": float(model.pdf(A)),
        "f_at_mode": float(model.pdf(MODE)),
        "f_at_b": float(model.pdf(B)),
        "mean": float(model.mean()),
        "total_area": float(model.cdf(B) - model.cdf(A)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model) -> Path:
    """Save the triangular density for the synthetic service-time clock.

    Parameters
    ----------
    model:
        Frozen triangular object from service_time_model().

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy curve is f(x). The shaded region is the entire support, so
    its area is 1. The dashed marker at 6 minutes flags the mode: the
    tallest height, still not a probability.
    """
    output_path = DIR_FIGURES / "continuous_rv_01_density.png"
    # 400 grid points from a to b inclusive; enough for a smooth triangle.
    x = np.linspace(A, B, 400)
    # pdf is vectorized: one call returns f at every grid point.
    y = model.pdf(x)

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Density f(x)")
    # fill_between shades the area under f. That area, not the height, is
    # the probability of the whole support.
    ax.fill_between(x, y, color="#5B8DEF", alpha=0.28)
    ax.axvline(MODE, color="#EC2661", ls="--", lw=1.4, label="Mode at 6 min")
    # "o" marks the peak. zorder=3 keeps the marker above the fill.
    ax.plot(MODE, model.pdf(MODE), "o", color="#EC2661", zorder=3)
    ax.set_xlabel("Service time (minutes)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("Triangular Density on [2, 14]: Height Is Not Probability")
    ax.set_xlim(A, B)
    # 0.22 sits just above the peak 1/6 so the marker is not clipped.
    ax.set_ylim(0, 0.22)
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
    """Run the Step 1 density report and write the triangular figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = service_time_model()
    values = density_at_points(model)
    figure_path = save_figure(model)

    print("================================================================")
    print("LESSON 19 - STEP 1: CONTINUOUS DENSITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Support [a, b]                  : [{A:.1f}, {B:.1f}]")
    print(f"Mode                            : {MODE:.1f}")
    print(f"f(2)                            : {values['f_at_a']:.6f}")
    # Peak height 1/6, not P(X = 6).
    print(f"f(6) at the mode                : {values['f_at_mode']:.6f}")
    print(f"f(14)                           : {values['f_at_b']:.6f}")
    # Closed form (a + b + mode) / 3 = (2 + 14 + 6) / 3 = 22/3.
    print(f"Mean (a + b + mode) / 3         : {values['mean']:.6f}")
    # A valid density integrates to 1; F(b) - F(a) is that integral.
    print(f"Total area under f              : {values['total_area']:.6f}")
    print("f(6) is a density height, not P(X = 6)")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

