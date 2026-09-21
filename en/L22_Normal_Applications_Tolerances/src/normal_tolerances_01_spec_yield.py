"""
Lesson 22 - Step 1: Yield Inside a Specification Interval
=========================================================
NEW IN THIS STEP: process_model(), spec_yield(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. process_model()    frozen Normal(mu, sigma) filling process
    2. spec_yield()       z cuts at LSL/USL and the in-spec probability
    3. save_figure()      shade the yield region on the centered density

Context:
A fully synthetic filling process is modeled as Normal(mu=50, sigma=4)
grams. The specification interval is [44, 56]. Yield is the probability
that a unit falls inside the spec, computed from two z cuts.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lesson 21 built z = (x - mu) / sigma
and standard normal areas. This script applies that ruler to a tolerance
interval.

    stats.norm(loc, scale)   frozen Normal(mu, sigma) object
    model.cdf(x)             P(X <= x) = Phi((x - mu) / sigma)
    model.pdf(x)             density height at x, not a probability
    z_low, z_high            spec limits in standard-deviation units
    yield                    P(LSL < X < USL), an interval probability

main() reports the centered z cuts, both tails, and the in-spec yield,
then writes the shaded-density figure. No earlier lesson script is imported.

Run it:
    python normal_tolerances_01_spec_yield.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the x-grid for the density curve.
# The aliases are the same ones used from Lesson 01 onward.
import matplotlib
import numpy as np
# scipy.stats is the probability-distribution library. stats.norm is the
# Normal family: PDF, CDF, mean, and std for X ~ Normal(mu, sigma^2).
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This script does not draw random numbers;
# scipy.stats.norm evaluates exact probabilities. The seed is reserved so
# later lessons that simulate from this process stay aligned.
SEED = 42
# Target fill weight in grams: the center of the specification interval.
MU = 50.0
# Process standard deviation in grams. Four grams is large enough that the
# spec [44, 56] sits only 1.5 sigma from the mean, so yield is not 1.
SIGMA = 4.0
# Lower and upper specification limits. A unit is in spec when LSL < X < USL.
LSL = 44.0
USL = 56.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) process_model() -------------------------------------------------
def process_model(mu: float = MU, sigma: float = SIGMA):
    """Return the Normal filling-process model.

    Parameters
    ----------
    mu:
        Process mean in grams. Default MU = 50, the target fill.
    sigma:
        Process standard deviation in grams. Default SIGMA = 4.

    Returns
    -------
    scipy.stats._distn_infrastructure.rv_frozen
        A frozen Normal(mu, sigma) object. Frozen means loc and scale are
        stored on the object, so later calls pass only the x values.

    Notes
    -----
    stats.norm(loc=mu, scale=sigma) is SciPy's Normal(mu, sigma^2).
    loc is the mean; scale is the standard deviation, not the variance.
    The object exposes .pdf, .cdf, .mean, and .std. Lesson 21 used the
    same constructor for the audit-score clock.
    """
    # loc= mean, scale= standard deviation. Do not pass sigma**2 here.
    return stats.norm(loc=mu, scale=sigma)
# ------------------------------------------------------------------------------


# --- NEW (2) spec_yield() ----------------------------------------------------
def spec_yield(model, lsl: float = LSL, usl: float = USL) -> dict[str, float]:
    """Convert spec limits into z cuts and the in-spec probability.

    Parameters
    ----------
    model:
        Frozen Normal returned by process_model().
    lsl, usl:
        Lower and upper specification limits in grams. Defaults are 44
        and 56, a symmetric window around the target 50.

    Returns
    -------
    dict[str, float]
        mu and sigma from the model. z_low and z_high are the spec limits
        in standard-deviation units. yield is P(LSL < X < USL). below is
        P(X <= LSL); above is P(X >= USL). The three probabilities sum
        to 1.

    Notes
    -----
    Yield is an interval probability, not the density height at the
    target. For a Normal,
        z = (x - mu) / sigma,    P(a < X < b) = F(b) - F(a),
    where F is the CDF. model.cdf(x) is Phi((x - mu) / sigma).
    On the centered process the z cuts are +/- 1.5 and the two tails
    match; that symmetry is a consequence of a centered mean inside a
    symmetric spec, not a property of every filling line.
    """
    # .mean() and .std() read loc and scale back off the frozen rv.
    mu = float(model.mean())
    sigma = float(model.std())
    # Standardize each spec limit. Negative z_low means LSL is below mu.
    z_low = (lsl - mu) / sigma
    z_high = (usl - mu) / sigma
    # CDF difference is P(LSL < X <= USL). For a continuous law the
    # equality at an endpoint has probability 0, so this is the yield.
    yield_p = float(model.cdf(usl) - model.cdf(lsl))
    return {
        "mu": mu,
        "sigma": sigma,
        "z_low": z_low,
        "z_high": z_high,
        "yield": yield_p,
        # Left tail: mass at or below the lower spec.
        "below": float(model.cdf(lsl)),
        # Right tail: 1 - F(USL) is P(X > USL).
        "above": float(1.0 - model.cdf(usl)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model, summary: dict[str, float]) -> Path:
    """Shade the in-spec region on the centered filling process.

    Parameters
    ----------
    model:
        Frozen Normal used to evaluate the density curve.
    summary:
        Dict from spec_yield(); the legend reads summary['yield'].

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy curve is f(x), the Normal density. The shaded band is the
    event LSL <= X <= USL whose area is the yield. Density height is not
    a probability; the area under the curve between the spec lines is.
    """
    output_path = DIR_FIGURES / "normal_tolerances_01_spec_yield.png"
    # Four sigma on each side of mu covers essentially the whole Normal.
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    y = model.pdf(x)
    # Boolean mask: True where the grid point sits inside the spec.
    mask = (x >= LSL) & (x <= USL)

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    # fill_between shades only the in-spec slice. alpha=0.35 keeps the
    # density curve visible through the fill.
    ax.fill_between(x[mask], y[mask], color="#5B8DEF", alpha=0.35,
                    label=f"Yield = {summary['yield']:.4f}")
    ax.axvline(LSL, color="#EC2661", ls="--", lw=1.3, label="LSL = 44")
    ax.axvline(USL, color="#EC2661", ls="--", lw=1.3, label="USL = 56")
    ax.axvline(MU, color="#646464", ls=":", lw=1.2, label="mu = 50")
    ax.set_xlabel("Fill weight (grams)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("Centered Process: Yield Inside [44, 56]")
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
    """Run the Step 1 spec-yield report and write the shaded figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = process_model()
    summary = spec_yield(model)
    figure_path = save_figure(model, summary)

    print("================================================================")
    print("LESSON 22 - STEP 1: SPEC YIELD")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Mean mu                         : {summary['mu']:.6f}")
    print(f"Standard deviation sigma        : {summary['sigma']:.6f}")
    print(f"Spec interval                   : [{LSL:.1f}, {USL:.1f}]")
    print(f"z at LSL                        : {summary['z_low']:.6f}")
    print(f"z at USL                        : {summary['z_high']:.6f}")
    print(f"P(below LSL)                    : {summary['below']:.6f}")
    print(f"P(above USL)                    : {summary['above']:.6f}")
    # Yield is F(USL) - F(LSL), not the density at mu = 50.
    print(f"Yield P(in spec)                : {summary['yield']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

