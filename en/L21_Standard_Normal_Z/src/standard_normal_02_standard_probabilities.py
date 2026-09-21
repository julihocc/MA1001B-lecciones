"""
Lesson 21 - Step 2: Standard Normal Probabilities
=================================================
THE RECIPE
Start from standard_normal_01_z_scores.py, then introduce:
    1. standard_normal()        Z ~ N(0, 1) as the standardized ruler
    2. left_tail_probability()  P(Z <= 1.25) from scipy.stats.norm
    3. save_figure()            shade the standard left tail

The same Normal(50, 8) audit-score model is rebuilt. P(X <= 60) equals
P(Z <= 1.25). No earlier lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 defined z = (x - mu) / sigma
and a frozen Normal(50, 8). Lesson 01 covers pathlib and unattended
savefig; they are rebuilt here only so the script stays self-contained.
This step reads left-tail probabilities from the standard normal.

    stats.norm()             frozen Z ~ N(0, 1); loc=0, scale=1 by default
    z = (x - mu) / sigma     same formula as Step 1; here z(60) = 1.25
    model.cdf(z)             P(Z <= z), the CDF; replaces a printed z table
    1 - model.cdf(z)         P(Z > z), the right tail (survival)
    model.ppf(p)             inverse of cdf: the z with P(Z <= z) = p
    operating.cdf(x)         P(X <= x) on the raw Normal(50, 8) clock

main() prints P(Z <= 1.25), P(Z > 1.25), and P(X <= 60). The first and
the last match because 60 is 1.25 sd above 50. ppf is the inverse map
(probability -> z) and is not called in this script.

Run it:
    python standard_normal_02_standard_probabilities.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm is reused from Step 1: now cdf reads P(Z <= z) on N(0, 1)
# and P(X <= 60) on N(50, 8). ppf is the inverse of cdf and is not called.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same mu, sigma, and x as Step 1. This script still does
# not draw random numbers; scipy.stats.norm evaluates exact probabilities.
SEED = 42
MU = 50.0
SIGMA = 8.0
X_MARK = 60.0
# Same z-score formula as z_score() in Step 1: (60 - 50) / 8 = 1.25.
Z_MARK = (X_MARK - MU) / SIGMA
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) standard_normal() -----------------------------------------------
def standard_normal():
    """Return the standard normal model Z ~ N(0, 1).

    Returns
    -------
    frozen standard normal
        A stats.norm object with loc=0 and scale=1 stored on it.
        stats.norm() and stats.norm(loc=0.0, scale=1.0) match.

    Notes
    -----
    After z = (x - mu) / sigma, every Normal(mu, sigma) clock is read on
    this one ruler. pdf, cdf, and ppf live on the frozen object:
        cdf(z) = P(Z <= z),
        ppf(p) = the z with cdf(z) = p.
    This step uses cdf; ppf would invert the table (find z from a tail
    probability) and is left for later lessons that start from a chance.
    """
    return stats.norm(loc=0.0, scale=1.0)
# ------------------------------------------------------------------------------


# --- NEW (2) left_tail_probability() -----------------------------------------
def left_tail_probability(z_model, z_mark: float) -> dict[str, float]:
    """Compute P(Z <= z), P(Z > z), and the matching raw-score probability.

    Parameters
    ----------
    z_model:
        Frozen Z ~ N(0, 1) from standard_normal().
    z_mark:
        Standardized location of x = 60, here 1.25.

    Returns
    -------
    dict[str, float]
        z_mark is the input z. p_z_le is P(Z <= z) from z_model.cdf.
        p_z_gt is P(Z > z) = 1 - cdf(z). p_x_le is P(X <= 60) on the
        raw Normal(50, 8) clock.

    Notes
    -----
    For a continuous CDF, P(Z <= z) = P(Z < z); the point z has no mass.
    Standardization preserves left-tail area: P(X <= mu + z sigma) equals
    P(Z <= z). So P(X <= 60) on N(50, 8) equals P(Z <= 1.25) on N(0, 1).
    float(...) converts the NumPy scalar that SciPy returns into a plain
    Python float for printing.

    cdf and ppf are inverses on (0, 1): ppf(cdf(z)) returns z, and
    cdf(ppf(p)) returns p (up to rounding). This function only needs cdf.
    """
    # Left-tail probability on the standard ruler. Replaces a z table.
    p_left = float(z_model.cdf(z_mark))
    # Same family, original clock: loc=50, scale=8 (sd, not variance).
    operating = stats.norm(loc=MU, scale=SIGMA)
    return {
        "z_mark": z_mark,
        "p_z_le": p_left,
        "p_z_gt": 1.0 - p_left,
        # P(X <= 60). Matches p_left because z_mark = (60 - 50) / 8.
        "p_x_le": float(operating.cdf(X_MARK)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(z_model, z_mark: float, p_left: float) -> Path:
    """Shade P(Z <= 1.25) on the standard normal curve.

    Parameters
    ----------
    z_model:
        Frozen Z ~ N(0, 1) from standard_normal().
    z_mark:
        The cutoff z = 1.25.
    p_left:
        Already-computed P(Z <= 1.25), used in the legend.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The horizontal axis is now z, not the raw audit score. The shaded
    area is the CDF value p_left = model.cdf(z_mark). The density height
    pdf(z) is not that probability; the area under pdf is.
    """
    output_path = DIR_FIGURES / "standard_normal_02_standard_probabilities.png"
    # Standard normal is plotted on a conventional z window [-4, 4].
    z = np.linspace(-4, 4, 400)
    y = z_model.pdf(z)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(z, y, color="#1A2E51", lw=2.2)
    # Boolean mask z <= 1.25. The area of this shade is cdf(1.25).
    ax.fill_between(z[z <= z_mark], y[z <= z_mark], color="#5B8DEF", alpha=0.35,
                    label=f"P(Z <= {z_mark:.2f}) = {p_left:.4f}")
    ax.axvline(z_mark, color="#EC2661", ls="--", lw=1.4)
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.set_title("Standard Normal Left Tail at z = 1.25")
    ax.set_xlim(-4, 4)
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
    """Run the Step 2 standard-normal report and write the left-tail figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    z_model = standard_normal()
    values = left_tail_probability(z_model, Z_MARK)
    figure_path = save_figure(z_model, Z_MARK, values["p_z_le"])

    print("================================================================")
    print("LESSON 21 - STEP 2: STANDARD PROBABILITIES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"z = (60 - 50) / 8               : {values['z_mark']:.6f}")
    # cdf at 1.25 on N(0, 1). Same number as P(X <= 60) on N(50, 8).
    print(f"P(Z <= 1.25)                    : {values['p_z_le']:.6f}")
    print(f"P(Z > 1.25)                     : {values['p_z_gt']:.6f}")
    print(f"P(X <= 60) on Normal(50, 8)     : {values['p_x_le']:.6f}")
    print("P(X <= 60) equals P(Z <= 1.25)")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

