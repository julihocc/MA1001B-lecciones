"""
Lesson 20 - Step 1: Exact Uniform Processing Time
=================================================
NEW IN THIS STEP: uniform_model(), exact_summaries(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. uniform_model()      frozen Uniform(8, 20) via scipy.stats.uniform
    2. exact_summaries()    height 1/12, mean (a + b) / 2, tail P(X > 16)
    3. save_figure()        flat density with the tail X > 16 shaded

Context:
A fully synthetic ticket-processing clock is modeled as Uniform(8, 20)
minutes. The density is flat, so probability is length divided by 12.
The exact tail P(X > 16) and the mean (a + b) / 2 are the reference
values for the Monte Carlo check in Step 2.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib.Path,
the Agg backend, and unattended fig.savefig; those idioms are reused
here without being re-taught. Lesson 19 treated a continuous density as
area, not as a point probability. This script specialises that idea to
the continuous uniform: a rectangle of height 1/(b - a).

    stats.uniform(loc, scale)  frozen Uniform(loc, loc + scale)
    model.pdf(x)               density height at x (1/12 on [8, 20])
    model.cdf(x)               P(X <= x) = length from 8 to x, over 12
    1 - model.cdf(CUT)         the right tail P(X > 16)
    ax.fill_between            shade that tail on the density plot

SciPy parameterises Uniform(a, b) as loc=a and scale=b-a, not as
(low, high). NumPy's rng.uniform(a, b) uses the endpoint form; Step 2
draws with that Generator through model.rvs(..., random_state=rng).

main() prints the exact height, mean, length ratio, and P(X > 16), then
writes the flat-density figure. No earlier lesson script is imported.

Run it:
    python uniform_mc_01_exact_uniform.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.uniform is
# the continuous uniform family: pdf, cdf, mean, and later rvs.
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so the Monte Carlo in Step 2 stays
# aligned with the rest of the catalog.
SEED = 42
# Support of the continuous uniform clock: every minute in [8, 20] is
# equally likely. Outside that interval the density is zero.
A = 8.0
B = 20.0
# Cut used for the right-tail probability P(X > 16). Remaining length
# is B - CUT = 4 minutes out of B - A = 12, so the exact tail is 1/3.
CUT = 16.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) uniform_model() -------------------------------------------------
def uniform_model():
    """Return the continuous uniform model on [8, 20] minutes.

    Returns
    -------
    frozen scipy.stats distribution
        A frozen Uniform(8, 20). Later calls pass only the x values:
        model.pdf, model.cdf, and model.mean already know a and b.

    Notes
    -----
    A continuous uniform random variable on [a, b] has density
        f(x) = 1 / (b - a)    for a <= x <= b
    and f(x) = 0 otherwise. Here a = 8, b = 20, so the height is 1/12.
    Probability is area, which for a flat density is just length over
    (b - a). SciPy stores that interval as loc=a and scale=b-a, so
    stats.uniform(loc=8, scale=12) is Uniform(8, 20), not Uniform(8, 12).
    """
    # loc is the left endpoint a. scale is the length b - a, not b.
    return stats.uniform(loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NEW (2) exact_summaries() -----------------------------------------------
def exact_summaries(model) -> dict[str, float]:
    """Compute the flat height, mean, and exact tail P(X > 16).

    Parameters
    ----------
    model:
        Frozen Uniform(8, 20) returned by uniform_model().

    Returns
    -------
    dict[str, float]
        height is f(x) = 1/12, evaluated at the midpoint so we sit
        inside the support. mean is (a + b) / 2 = 14. p_gt_cut is
        P(X > 16) from the CDF. length_ratio is (20 - 16) / 12, the
        same tail computed as remaining length over total length.

    Notes
    -----
    For a continuous variable, P(X = 16) = 0, so P(X > 16) = P(X >= 16)
    = 1 - F(16). The length-ratio formula is the geometry of a rectangle:
    the shaded width 4 divided by the base 12. The two routes must match.
    float(...) converts SciPy's NumPy scalars into plain Python floats
    for printing.
    """
    return {
        # Midpoint (A + B) / 2 is safely inside [8, 20], so pdf returns
        # the constant height 1/(B - A) rather than a boundary zero.
        "height": float(model.pdf((A + B) / 2)),
        # Closed form (a + b) / 2. Uniform mean sits at the rectangle's
        # center, not at a mode (every point on [a, b] is a mode).
        "mean": float(model.mean()),
        # Survival function by hand: 1 - F(16). Equivalent to model.sf(CUT).
        "p_gt_cut": float(1.0 - model.cdf(CUT)),
        # Geometry check: remaining length over total length. Must equal
        # p_gt_cut for a flat density; Step 3 will break that equality.
        "length_ratio": (B - CUT) / (B - A),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model, height: float, tail: float) -> Path:
    """Save the flat uniform density with the tail X > 16 shaded.

    Parameters
    ----------
    model:
        Frozen Uniform(8, 20) used to evaluate the density curve.
    height:
        Constant density 1/12, drawn as a horizontal guide.
    tail:
        Exact P(X > 16), shown in the shaded-region legend.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy curve is the rectangle of height 1/12 on [8, 20] and zero
    outside. The red fill is the event X > 16. Because the density is
    flat, that red area equals the length ratio 4/12.
    """
    output_path = DIR_FIGURES / "uniform_mc_01_exact_uniform.png"
    # 500 points from just left of 8 to just right of 20 so the drop to
    # height 0 is visible at both endpoints.
    x = np.linspace(A - 1, B + 1, 500)
    y = model.pdf(x)
    # Shade only the tail interval [16, 20], not the whole support.
    shade_x = np.linspace(CUT, B, 200)
    shade_y = model.pdf(shade_x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    # fill_between draws the area under the density between shade_x
    # values. That area is the probability, not the height 1/12.
    ax.fill_between(shade_x, shade_y, color="#EC2661", alpha=0.35,
                    label=f"P(X > 16) = {tail:.4f}")
    # Dotted guide at the constant height so the rectangle is readable.
    ax.axhline(height, color="#5B8DEF", ls=":", lw=1.2)
    ax.set_xlabel("Processing time (minutes)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("Uniform(8, 20): Probability Equals Length over 12")
    ax.set_xlim(A - 1, B + 1)
    ax.set_ylim(0, 0.14)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 exact-uniform report and write the density figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = uniform_model()
    values = exact_summaries(model)
    figure_path = save_figure(model, values["height"], values["p_gt_cut"])

    print("================================================================")
    print("LESSON 20 - STEP 1: EXACT UNIFORM")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Support [a, b]                  : [{A:.1f}, {B:.1f}]")
    print(f"Density height 1/(b - a)        : {values['height']:.6f}")
    print(f"Mean (a + b) / 2                : {values['mean']:.6f}")
    print(f"Length ratio (20 - 16) / 12     : {values['length_ratio']:.6f}")
    print(f"P(X > 16) exact                 : {values['p_gt_cut']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

