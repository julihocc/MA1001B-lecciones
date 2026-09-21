"""
Lesson 21 - Step 1: Standardizing an Operating Score
====================================================
NEW IN THIS STEP: operating_model(), z_score(), and save_figure().

Context:
A fully synthetic audit-score clock is modeled as Normal(mu=50, sigma=8).
The z-score (x - mu) / sigma locates a raw score on the standard normal
ruler. A score of 60 is 1.25 standard deviations above the mean.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds the z-score and a
frozen Normal(mu, sigma) from scipy.stats.norm.

    stats.norm(loc, scale)   frozen Normal(mean, sd) object; scale is sd,
                             not variance
    z = (x - mu) / sigma     location in standard-deviation units, not a
                             probability
    model.pdf(x)             density height f(x); not P(X = x)
    model.cdf(x)             P(X <= x), the left-tail CDF (used in Step 2)
    model.ppf(p)             inverse CDF: the x with P(X <= x) = p

main() standardizes x = 60 on Normal(50, 8), reports z = 1.25 and the
z values at mu +/- sigma, and writes the operating-density figure. No
earlier lesson script is imported.

Run it:
    python standard_normal_01_z_scores.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the x-grid for the density.
# The aliases are the same ones used from Lesson 01 onward.
import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.norm is the
# normal family: pdf, cdf, and ppf for X ~ Normal(loc, scale).
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# Mean of the synthetic audit-score clock. loc= in stats.norm.
MU = 50.0
# Standard deviation of that clock. scale= in stats.norm, not the variance.
SIGMA = 8.0
# Raw score that will be standardized: one operating observation x = 60.
X_MARK = 60.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) operating_model() -----------------------------------------------
def operating_model():
    """Return the Normal(50, 8) model for the synthetic audit score.

    Returns
    -------
    frozen normal
        A stats.norm object with loc and scale stored on it, so later
        calls pass only x. There is no return annotation on this
        function; Python does not enforce one at run time.

    Notes
    -----
    stats.norm(loc=MU, scale=SIGMA) is X ~ N(50, 8^2). loc is the mean.
    scale is the standard deviation, not the variance: passing 64 here
    would be a different clock. The frozen object exposes pdf, cdf, and
    ppf. This step uses pdf to draw the density; cdf and ppf wait until
    probabilities are read in Step 2.
    """
    # Frozen rv: mu and sigma are locked on the object. The unbound form
    # stats.norm.pdf(x, loc=MU, scale=SIGMA) is equivalent.
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NEW (2) z_score() -------------------------------------------------------
def z_score(x: float, mu: float = MU, sigma: float = SIGMA) -> float:
    """Convert a raw score into standard-deviation units.

    Parameters
    ----------
    x:
        Raw operating score on the original clock.
    mu:
        Mean of that clock. Default is the module-level MU = 50.
    sigma:
        Standard deviation of that clock. Default SIGMA = 8. Must be
        nonzero; a zero scale would divide by zero.

    Returns
    -------
    float
        z = (x - mu) / sigma. z = 0 at the mean, z = 1 one sd above it,
        z = -1 one sd below it. The value is a location, not a chance.

    Notes
    -----
    For x = 60, mu = 50, sigma = 8 the arithmetic is (60 - 50) / 8 = 1.25.
    Every normal clock maps onto the same standard ruler Z ~ N(0, 1) by
    this formula. Equal z values are comparable only when the shapes are
    similar; Step 3 shows a skewed delay clock that breaks that reading.
    """
    return (x - mu) / sigma
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model, z_mark: float) -> Path:
    """Plot the operating density and mark the raw score x = 60.

    Parameters
    ----------
    model:
        Frozen Normal(50, 8) from operating_model().
    z_mark:
        Already-computed z at x = 60, used only in the legend.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The curve is f(x) = model.pdf(x), a density height, not P(X = x).
    The navy dotted line is mu = 50 (z = 0). The magenta dashed line is
    x = 60 (z = 1.25). The shaded region is the left tail X <= 60; its
    area is a probability, computed with cdf in Step 2, not here.
    """
    output_path = DIR_FIGURES / "standard_normal_01_z_scores.png"
    # Four sd on each side of mu covers essentially all of a normal curve.
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    # pdf evaluates the density on the whole grid at once.
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Normal(50, 8)")
    ax.axvline(MU, color="#5B8DEF", ls=":", lw=1.3, label="Mean 50")
    ax.axvline(X_MARK, color="#EC2661", ls="--", lw=1.4,
               label=f"x = 60, z = {z_mark:.2f}")
    # Boolean masks x <= 60 and the matching density heights. The area of
    # this shade is P(X <= 60), but Step 1 only draws it.
    ax.fill_between(x[x <= X_MARK], y[x <= X_MARK], color="#5B8DEF", alpha=0.25)
    ax.set_xlabel("Audit score")
    ax.set_ylabel("Density f(x)")
    ax.set_title("A Raw Score of 60 Is z = 1.25 on the Standard Ruler")
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
    """Run the Step 1 z-score report and write the operating-density figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = operating_model()
    # (60 - 50) / 8 = 1.25. z is a location on the standard ruler.
    z_mark = z_score(X_MARK)
    # By construction, the point one sd below the mean has z = -1.
    z_low = z_score(MU - SIGMA)
    # The point one sd above the mean has z = +1.
    z_high = z_score(MU + SIGMA)
    figure_path = save_figure(model, z_mark)

    print("================================================================")
    print("LESSON 21 - STEP 1: Z SCORES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Mean mu                         : {MU:.6f}")
    print(f"Standard deviation sigma        : {SIGMA:.6f}")
    print(f"Raw score x                     : {X_MARK:.6f}")
    print(f"z = (x - mu) / sigma            : {z_mark:.6f}")
    print(f"z at mu - sigma                 : {z_low:.6f}")
    print(f"z at mu + sigma                 : {z_high:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

