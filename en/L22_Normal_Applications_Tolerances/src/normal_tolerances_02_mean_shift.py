"""
Lesson 22 - Step 2: A Mean Shift Drops Yield
============================================
THE RECIPE
Start from normal_tolerances_01_spec_yield.py, then introduce:
    1. shifted_model()          move the filling mean from 50 to 52
    2. yield_drop()             compare centered yield with shifted yield
    3. save_figure()            overlay both processes on the same spec

The specification [44, 56] does not move. Shifting mu to 52 changes the
z cuts and lowers the in-spec probability. No earlier lesson script is
imported.

How to read this file:
You already know Python through OOP. Step 1 defined the centered
Normal(50, 4) filling process, converted [44, 56] into z cuts, and
computed yield as F(USL) - F(LSL). Lesson 01 covers pathlib and
unattended savefig; they are rebuilt here only so the script stays
self-contained. This step keeps the spec and sigma fixed and moves mu.

    MU_SHIFT = 52            new mean; spec and sigma are unchanged
    shifted z cuts           (LSL - 52) / 4 = -2 and (USL - 52) / 4 = 1
    yield_drop               centered yield minus shifted yield
    overlay                  two pdf curves, one spec pair

main() prints both z-cut pairs, both yields, the drop, and the shifted
tails. The spec does not chase the mean: only the z cuts move.

Run it:
    python normal_tolerances_02_mean_shift.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm is reused from Step 1: frozen Normal(mu, sigma) with .pdf
# and .cdf. loc is the mean; scale is the standard deviation.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same centered process as Step 1. This script still does
# not draw random numbers; scipy.stats.norm evaluates exact probabilities.
SEED = 42
MU = 50.0
# Mean after the +2 gram shift. Sigma and the spec stay where they were.
MU_SHIFT = 52.0
SIGMA = 4.0
LSL = 44.0
USL = 56.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def process_model(mu: float = MU, sigma: float = SIGMA):
    """Return the Normal filling-process model rebuilt from Step 1.

    stats.norm(loc=mu, scale=sigma) freezes mean and standard deviation.
    This file does not import Step 1. Passing mu=MU_SHIFT builds the
    shifted clock without a second constructor.
    """
    return stats.norm(loc=mu, scale=sigma)


def spec_yield(model, lsl: float = LSL, usl: float = USL) -> dict[str, float]:
    """Convert spec limits into z cuts and the in-spec probability.

    Yield is F(USL) - F(LSL). z_low and z_high use the model's own mean,
    so a shift in mu changes the z cuts even though lsl and usl do not
    move. below and above are the two tails that are no longer equal
    after the mean leaves the center of the spec.
    """
    mu = float(model.mean())
    sigma = float(model.std())
    return {
        "mu": mu,
        "z_low": (lsl - mu) / sigma,
        "z_high": (usl - mu) / sigma,
        "yield": float(model.cdf(usl) - model.cdf(lsl)),
        "below": float(model.cdf(lsl)),
        "above": float(1.0 - model.cdf(usl)),
    }


# --- NEW (1) shifted_model() -------------------------------------------------
def shifted_model():
    """Return the filling process after a +2 gram mean shift.

    Returns
    -------
    scipy.stats._distn_infrastructure.rv_frozen
        Frozen Normal(MU_SHIFT, SIGMA) = Normal(52, 4). Same scale as
        the centered process; only loc has moved.

    Notes
    -----
    A mean shift is a change in mu with sigma held fixed. The spec
    interval [44, 56] is a customer or engineering requirement: it does
    not travel with the process. After the shift the z cuts become
        (44 - 52) / 4 = -2    and    (56 - 52) / 4 = 1,
    so more mass sits above USL than below LSL.
    """
    return process_model(mu=MU_SHIFT, sigma=SIGMA)
# ------------------------------------------------------------------------------


# --- NEW (2) yield_drop() ----------------------------------------------------
def yield_drop(centered: dict[str, float], shifted: dict[str, float]) -> float:
    """Return how much in-spec probability is lost after the shift.

    Parameters
    ----------
    centered:
        spec_yield() dict for Normal(50, 4).
    shifted:
        spec_yield() dict for Normal(52, 4).

    Returns
    -------
    float
        centered yield minus shifted yield. Positive means the shift
        reduced the in-spec probability.

    Notes
    -----
    Yield is not a density height, so a two-gram move of the peak does
    not tell you the drop by itself. Recompute F(USL) - F(LSL) under the
    new mean. The drop here is about 0.0478: the right tail grows more
    than the left tail shrinks because the spec is no longer symmetric
    around mu.
    """
    return centered["yield"] - shifted["yield"]
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(centered_model, shifted_m, drop: float) -> Path:
    """Overlay the centered and shifted filling processes.

    Parameters
    ----------
    centered_model:
        Frozen Normal(50, 4).
    shifted_m:
        Frozen Normal(52, 4).
    drop:
        Yield loss from yield_drop(), printed in the title.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Both curves share the same spec lines. The navy density is centered
    at 50; the magenta density has slid 2 grams to the right. The area
    inside [44, 56] is smaller after the shift even though the spec did
    not move.
    """
    output_path = DIR_FIGURES / "normal_tolerances_02_mean_shift.png"
    # The shifted mean is 52, so the grid extends one extra sigma on the
    # right to keep that right tail on the .
    x = np.linspace(MU - 4 * SIGMA, MU + 5 * SIGMA, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, centered_model.pdf(x), color="#1A2E51", lw=2.2,
            label="Centered mu = 50")
    ax.plot(x, shifted_m.pdf(x), color="#EC2661", lw=2.2,
            label="Shifted mu = 52")
    # Spec lines stay at 44 and 56; they are not recomputed from mu.
    ax.axvline(LSL, color="#646464", ls="--", lw=1.2)
    ax.axvline(USL, color="#646464", ls="--", lw=1.2)
    ax.set_xlabel("Fill weight (grams)")
    ax.set_ylabel("Density f(x)")
    ax.set_title(f"Mean Shift of +2 g Drops Yield by {drop:.4f}")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 mean-shift comparison and write the overlay.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    centered_model = process_model()
    shifted_m = shifted_model()
    centered = spec_yield(centered_model)
    shifted = spec_yield(shifted_m)
    drop = yield_drop(centered, shifted)
    figure_path = save_figure(centered_model, shifted_m, drop)

    print("================================================================")
    print("LESSON 22 - STEP 2: MEAN SHIFT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Centered mu                     : {centered['mu']:.6f}")
    print(f"Centered z cuts                 : {centered['z_low']:.6f} to {centered['z_high']:.6f}")
    print(f"Centered yield                  : {centered['yield']:.6f}")
    print(f"Shifted mu                      : {shifted['mu']:.6f}")
    # z cuts moved from +/-1.5 to -2 and +1; the spec itself did not.
    print(f"Shifted z cuts                  : {shifted['z_low']:.6f} to {shifted['z_high']:.6f}")
    print(f"Shifted yield                   : {shifted['yield']:.6f}")
    print(f"Yield drop                      : {drop:.6f}")
    print(f"Shifted P(below LSL)            : {shifted['below']:.6f}")
    print(f"Shifted P(above USL)            : {shifted['above']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()
