"""
Lesson 20 - Step 3: Uniform Fails When Density Piles at One End
==============================================================
THE RECIPE
Start from uniform_mc_02_monte_carlo.py, then introduce:
    1. piled_model()            right-triangular density on the same [8, 20]
    2. compare_tails()          Uniform P(X > 16) versus the piled tail
    3. save_figure()            overlay the flat density and the piled density

If tickets cluster near 20 minutes, the Uniform(8, 20) tail 1/3 is the
wrong number. The limit is that a flat model fails when density piles
at one end.

How to read this file:
You already know Python through OOP. Steps 1-2 treated a flat Uniform(8, 20)
clock and checked P(X > 16) = 1/3 with a seed-42 Monte Carlo. Lesson 01
covers pathlib and unattended savefig. This step keeps the same support
[8, 20] but replaces the flat density with a right triangle that piles
at 20 minutes.

    stats.triang(c, loc, scale)  triangular density on [loc, loc + scale]
    c = 1.0                      mode at the right endpoint (a pile at 20)
    1 - model.cdf(CUT)           tail P(X > 16) under either density
    overlay two pdf curves       flat 1/12 versus a rising triangle

The Monte Carlo of Step 2 is not reused here: both tails are exact CDF
values. rng.uniform / model.rvs would still draw from the *uniform*
model, which is the wrong sampler once the density is no longer flat.

main() prints Uniform versus piled tails, means, and heights. Matching
the interval [8, 20] does not restore the uniform tail.

Run it:
    python uniform_mc_03_piled_density_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.uniform is the Step 1 flat model. stats.triang is the piled
# alternative on the same interval.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Seed reserved for catalog alignment. This script evaluates exact pdf
# and cdf values and does not draw rng.uniform samples.
SEED = 42
A = 8.0
B = 20.0
CUT = 16.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def uniform_model():
    """Return the continuous uniform model on [8, 20] minutes.

    Rebuilt from Step 1. loc=A and scale=B-A is SciPy's Uniform(8, 20).
    The density is the constant 1/12; P(X > 16) is the length ratio 1/3.
    """
    return stats.uniform(loc=A, scale=B - A)


# --- NEW (1) piled_model() ---------------------------------------------------
def piled_model():
    """Return a right-triangular density on [8, 20] that piles at 20.

    Returns
    -------
    frozen scipy.stats distribution
        Frozen triangular law on [8, 20] with mode at 20.

    Notes
    -----
    stats.triang(c, loc, scale) lives on [loc, loc + scale]. The shape
    c in [0, 1] is the mode as a fraction of that scale:
        mode = loc + c * scale.
    c = 1.0 puts the mode at loc + scale = 20, so the density rises
    from 0 at 8 minutes to a peak of 2/(b - a) = 1/6 at 20 minutes.
    That is a pile at the slow end, not a flat uniform rectangle.
    """
    # c=1.0 is the right-endpoint mode. loc/scale match Uniform(8, 20)
    # so the two models share support and differ only in shape.
    return stats.triang(c=1.0, loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NEW (2) compare_tails() -------------------------------------------------
def compare_tails(flat, piled) -> dict[str, float]:
    """Contrast Uniform and piled-density tails and means.

    Parameters
    ----------
    flat:
        Frozen Uniform(8, 20) from uniform_model().
    piled:
        Frozen right-triangular model from piled_model().

    Returns
    -------
    dict[str, float]
        uniform_tail and piled_tail are P(X > 16) under each density.
        uniform_mean is 14; piled_mean is 16 for this right triangle.
        uniform_height is the flat 1/12. piled_at_cut and piled_at_b
        are the triangular density at 16 and at 20.

    Notes
    -----
    For the right triangle, F(x) = ((x - a) / (b - a))^2 on [a, b], so
        P(X > 16) = 1 - (8 / 12)^2 = 5/9 = 0.555556,
    not the uniform 1/3. The mean of a right triangle that piles at b
    is (a + 2b) / 3 = 16, two minutes slower than the uniform mean 14.
    Same support, same cut, different area to the right of 16: that is
    the limit of the flat model.
    """
    return {
        "uniform_tail": float(1.0 - flat.cdf(CUT)),
        "piled_tail": float(1.0 - piled.cdf(CUT)),
        "uniform_mean": float(flat.mean()),
        "piled_mean": float(piled.mean()),
        # 14.0 is the uniform midpoint, where the flat pdf equals 1/12.
        "uniform_height": float(flat.pdf(14.0)),
        "piled_at_cut": float(piled.pdf(CUT)),
        "piled_at_b": float(piled.pdf(B)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(flat, piled, comparison: dict[str, float]) -> Path:
    """Overlay the flat uniform density and the right-piled alternative.

    Parameters
    ----------
    flat, piled:
        The two frozen models compared in compare_tails().
    comparison:
        Dict with piled_tail, used in the shaded-region legend.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Navy is Uniform(8, 20). Red is the right triangle. The fill is the
    piled event X > 16, whose area is 5/9 rather than 1/3. The visual
    of the limit is that extra red mass near 20 minutes.
    """
    output_path = DIR_FIGURES / "uniform_mc_03_piled_density_limit.png"
    x = np.linspace(A, B, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, flat.pdf(x), color="#1A2E51", lw=2.2, label="Uniform(8, 20)")
    ax.plot(x, piled.pdf(x), color="#EC2661", lw=2.2,
            label="Right-triangular pile")
    # Boolean index x >= CUT selects the tail grid points. piled.pdf
    # on those points is the height of the red fill.
    ax.fill_between(
        x[x >= CUT],
        piled.pdf(x[x >= CUT]),
        color="#EC2661",
        alpha=0.25,
        label=f"Piled P(X > 16) = {comparison['piled_tail']:.4f}",
    )
    ax.axvline(CUT, color="#646464", ls="--", lw=1.2)
    ax.set_xlabel("Processing time (minutes)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("A Flat Uniform Model Misses a Density Pile at 20")
    ax.set_xlim(A, B)
    ax.set_ylim(0, 0.20)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 piled-density comparison and write the overlay figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    flat = uniform_model()
    piled = piled_model()
    comparison = compare_tails(flat, piled)
    figure_path = save_figure(flat, piled, comparison)

    print("================================================================")
    print("LESSON 20 - STEP 3: PILED DENSITY LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Uniform P(X > 16)               : {comparison['uniform_tail']:.6f}")
    print(f"Piled P(X > 16)                 : {comparison['piled_tail']:.6f}")
    print(f"Uniform mean                    : {comparison['uniform_mean']:.6f}")
    print(f"Piled mean                      : {comparison['piled_mean']:.6f}")
    print(f"Uniform height                  : {comparison['uniform_height']:.6f}")
    print(f"Piled density at 16             : {comparison['piled_at_cut']:.6f}")
    print(f"Piled density at 20             : {comparison['piled_at_b']:.6f}")
    print("Limit: uniform fails if density piles at one end")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom.
if __name__ == "__main__":
    main()

