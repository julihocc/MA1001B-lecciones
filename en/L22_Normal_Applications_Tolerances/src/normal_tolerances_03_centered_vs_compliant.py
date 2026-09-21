"""
Lesson 22 - Step 3: Compliance Is Not the Same as Centered
==========================================================
THE RECIPE
Start from normal_tolerances_02_mean_shift.py, then introduce:
    1. tight_offcenter_model()  mu = 52, sigma = 2 on the same spec
    2. compliance_table()       high yield can hide an off-center mean
    3. save_figure()            compare centered-wide versus tight-shifted

A process can meet the specification [44, 56] at a high rate and still
not be centered at 50. Spec compliance is not the same as a centered
process.

How to read this file:
You already know Python through OOP. Steps 1-2 computed yield for
Normal(50, 4) and showed that a mean shift to 52 drops that yield.
Lesson 01 covers pathlib and unattended savefig. This step keeps the
shifted mean and shrinks sigma, which raises yield while leaving the
process off target.

    SIGMA_TIGHT = 2          half the original spread, same spec
    tight z cuts             (44 - 52) / 2 = -4 and (56 - 52) / 2 = 2
    compliance_table         centered-wide yield versus tight-shifted yield
    limit                    high P(in spec) is not evidence of mu = 50

main() prints both (mu, sigma) pairs, both z-cut pairs, and both yields.
The tight off-center clock has the higher yield. Lesson 23 leaves one
unit and studies the sampling distribution of the sample mean.

Run it:
    python normal_tolerances_03_centered_vs_compliant.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm is reused from Steps 1-2: frozen Normal(mu, sigma) with .pdf
# and .cdf. loc is the mean; scale is the standard deviation.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 50.0
MU_SHIFT = 52.0
SIGMA = 4.0
# Half the original sigma. A smaller scale can raise yield even when mu
# is off the target; that is the limit this step is built to show.
SIGMA_TIGHT = 2.0
LSL = 44.0
USL = 56.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def process_model(mu: float = MU, sigma: float = SIGMA):
    """Return the Normal filling-process model rebuilt from Step 1.

    stats.norm(loc=mu, scale=sigma) freezes mean and standard deviation.
    Passing both arguments lets one constructor serve the centered-wide
    clock and the tight off-center clock. This file does not import
    earlier steps.
    """
    return stats.norm(loc=mu, scale=sigma)


def spec_yield(model, lsl: float = LSL, usl: float = USL) -> dict[str, float]:
    """Convert spec limits into z cuts and the in-spec probability.

    Yield is F(USL) - F(LSL). z cuts use the model's own mu and sigma,
    so shrinking sigma stretches the same gram-limits into larger |z|.
    sigma is stored in the dict this step because the two clocks no
    longer share a scale.
    """
    mu = float(model.mean())
    sigma = float(model.std())
    return {
        "mu": mu,
        "sigma": sigma,
        "z_low": (lsl - mu) / sigma,
        "z_high": (usl - mu) / sigma,
        "yield": float(model.cdf(usl) - model.cdf(lsl)),
    }


# --- NEW (1) tight_offcenter_model() -----------------------------------------
def tight_offcenter_model():
    """Return a tighter process that is shifted to 52 grams.

    Returns
    -------
    scipy.stats._distn_infrastructure.rv_frozen
        Frozen Normal(MU_SHIFT, SIGMA_TIGHT) = Normal(52, 2).

    Notes
    -----
    The mean is still 2 grams above the target 50, but sigma is now 2
    instead of 4. The spec is unchanged, so the z cuts become
        (44 - 52) / 2 = -4    and    (56 - 52) / 2 = 2.
    Almost all mass then sits inside [44, 56] even though the process
    is not centered. A smaller sigma can raise yield while hiding a
    mean shift.
    """
    return process_model(mu=MU_SHIFT, sigma=SIGMA_TIGHT)
# ------------------------------------------------------------------------------


# --- NEW (2) compliance_table() ----------------------------------------------
def compliance_table() -> dict[str, dict[str, float]]:
    """Compare centered-wide yield with tight off-center yield.

    Returns
    -------
    dict[str, dict[str, float]]
        Nested dict. 'centered' is spec_yield for Normal(50, 4).
        'tight' is spec_yield for Normal(52, 2). Each inner dict has
        mu, sigma, z_low, z_high, and yield.

    Notes
    -----
    Both rows use the same spec [44, 56]. The tight off-center row has
    the higher yield. Spec compliance answers "what fraction of units
    fall inside the interval?"; it does not answer "is the process
    sitting on the target?" Those are different questions, and a high
    yield can hide an off-center mean.
    """
    centered = spec_yield(process_model(MU, SIGMA))
    tight = spec_yield(tight_offcenter_model())
    return {"centered": centered, "tight": tight}
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(table: dict[str, dict[str, float]]) -> Path:
    """Overlay a centered-wide process and a tight off-center process.

    Parameters
    ----------
    table:
        Nested dict from compliance_table(); legend labels read the
        two yields.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Navy: centered at 50 with sigma 4. Magenta: centered at 52 with
    sigma 2. Gray dashed lines are the spec; the dotted blue line is
    the target 50. The taller, narrower curve has the higher yield and
    the wrong mean. High spec compliance is not visual evidence that
    the process is on target.
    """
    output_path = DIR_FIGURES / "normal_tolerances_03_centered_vs_compliant.png"
    centered = process_model(MU, SIGMA)
    tight = tight_offcenter_model()
    x = np.linspace(MU - 4 * SIGMA, MU + 5 * SIGMA, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(
        x,
        centered.pdf(x),
        color="#1A2E51",
        lw=2.2,
        label=f"Centered sigma=4, yield={table['centered']['yield']:.4f}",
    )
    ax.plot(
        x,
        tight.pdf(x),
        color="#EC2661",
        lw=2.2,
        label=f"Off-center sigma=2, yield={table['tight']['yield']:.4f}",
    )
    ax.axvline(LSL, color="#646464", ls="--", lw=1.2, label="Spec [44, 56]")
    ax.axvline(USL, color="#646464", ls="--", lw=1.2)
    # Target line at 50: the tight process peaks to the right of it.
    ax.axvline(MU, color="#5B8DEF", ls=":", lw=1.2, label="Target 50")
    ax.set_xlabel("Fill weight (grams)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("High Yield Can Hide a Process That Is Not Centered")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 centered-versus-compliant comparison.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    table = compliance_table()
    figure_path = save_figure(table)
    centered = table["centered"]
    tight = table["tight"]

    print("================================================================")
    print("LESSON 22 - STEP 3: CENTERED VERSUS COMPLIANT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Centered mu, sigma              : {centered['mu']:.6f}, {centered['sigma']:.6f}")
    print(f"Centered z cuts                 : {centered['z_low']:.6f} to {centered['z_high']:.6f}")
    print(f"Centered yield                  : {centered['yield']:.6f}")
    print(f"Tight mu, sigma                 : {tight['mu']:.6f}, {tight['sigma']:.6f}")
    print(f"Tight z cuts                    : {tight['z_low']:.6f} to {tight['z_high']:.6f}")
    # Higher yield, off-center mean: compliance is not the same as mu = 50.
    print(f"Tight yield                     : {tight['yield']:.6f}")
    print("Limit: spec compliance is not the same as being centered")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

