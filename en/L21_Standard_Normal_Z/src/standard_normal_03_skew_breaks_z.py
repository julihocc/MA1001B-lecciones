"""
Lesson 21 - Step 3: Skew Breaks a z-Score Comparison
====================================================
THE RECIPE
Start from standard_normal_02_standard_probabilities.py, then introduce:
    1. delay_model()            exponential delays with mean 20 (so sd = 20)
    2. percentile_mismatch()    z = -1 is 16% on a bell and 0% on a delay clock
    3. save_figure()            overlay standardized bell and delay densities

A z-score comparison requires similar shape. Right-skewed delay times cannot
go below 0, so z = -1 is off the support. Skew breaks the percentile reading.

How to read this file:
You already know Python through OOP. Steps 1-2 built z = (x - mu) / sigma
and read P(Z <= z) with scipy.stats.norm.cdf. Lesson 01 covers pathlib and
unattended savefig. This step keeps the same z formula on a skewed clock.

    stats.expon(scale=mu)    exponential delays; scale is the mean, loc=0
    z = (x - mu) / sigma     same location formula; not a portable percentile
    stats.norm().cdf(z)      bell left tail, here P(Z <= -1) ~ 0.158655
    delay.cdf(x)             P(X <= x) on the delay clock; cdf(0) = 0
    stats.norm.ppf(p)        inverse CDF on the bell (not called here)
    f_X(mu + z sigma) * sigma   change of variable that plots delay on z

main() compares P(Z <= -1) on the bell with P(X <= 0) on the delay clock.
Matching z does not match percentiles when the shapes differ.

Run it:
    python standard_normal_03_skew_breaks_z.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm is the bell from Steps 1-2 (cdf / pdf / ppf). stats.expon is
# the right-skewed delay clock whose support starts at 0.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed. This script still does not draw random numbers; cdf and
# pdf are evaluated on the two frozen models.
SEED = 42
# Same audit-score bell as Steps 1-2, used only as the comparable shape.
MU_BELL = 50.0
SIGMA_BELL = 8.0
# Exponential mean. For this family, mean equals sd, so SIGMA_DELAY = 20.
MU_DELAY = 20.0
SIGMA_DELAY = 20.0
# One sd below the delay mean is x = 0, the left edge of the support.
Z_LEFT = -1.0
# Same z = 1.25 used in Step 2, now read on both clocks.
Z_RIGHT = 1.25
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) delay_model() ---------------------------------------------------
def delay_model():
    """Return an exponential delay clock with mean 20 minutes.

    Returns
    -------
    frozen exponential
        A stats.expon object with scale=20. loc defaults to 0, so the
        support is [0, infinity). scale is the mean, not a z-score.

    Notes
    -----
    An exponential clock is right-skewed and cannot go negative. Its mean
    equals its standard deviation, so z = (x - 20) / 20. The left-tail
    methods are the same names as on stats.norm: pdf, cdf, and ppf. cdf
    is used below; ppf would invert the delay CDF and is not called.
    """
    return stats.expon(scale=MU_DELAY)
# ------------------------------------------------------------------------------


# --- NEW (2) percentile_mismatch() -------------------------------------------
def percentile_mismatch(delay) -> dict[str, float]:
    """Compare bell and delay percentiles at the same z values.

    Parameters
    ----------
    delay:
        Frozen exponential from delay_model().

    Returns
    -------
    dict[str, float]
        Delay mean and sd (both 20), the raw x at z = -1 on each clock,
        left- and right-tail probabilities on each clock, and the z at
        which the delay support starts.

    Notes
    -----
    stats.norm() is Z ~ N(0, 1). Its cdf at -1 is the usual bell
    percentile ~ 0.158655. The matching delay point is
        x = mu + z * sigma = 20 + (-1) * 20 = 0,
    which is the left endpoint of the exponential support, so
    delay.cdf(0) = 0. The same z formula therefore does not carry the
    same percentile across shapes.

    ppf is the inverse of cdf on each family. On the bell,
    stats.norm.ppf(0.158655) returns about -1; on the delay clock
    delay.ppf(0) is 0, not a negative z. This function only needs cdf.
    """
    # Default loc=0, scale=1: the standard ruler from Step 2.
    bell = stats.norm()
    # Inverse of z = (x - mu) / sigma, applied on each clock.
    x_left_bell = MU_BELL + Z_LEFT * SIGMA_BELL
    x_left_delay = MU_DELAY + Z_LEFT * SIGMA_DELAY
    x_right_delay = MU_DELAY + Z_RIGHT * SIGMA_DELAY
    return {
        "delay_mean": float(delay.mean()),
        "delay_sd": float(delay.std()),
        "x_left_bell": x_left_bell,
        "x_left_delay": x_left_delay,
        # Bell left tail at z = -1. This is NOT P(delay <= 0).
        "bell_p_left": float(bell.cdf(Z_LEFT)),
        # Exponential support starts at 0, so the left-tail chance is 0.
        "delay_p_left": float(delay.cdf(x_left_delay)),
        "bell_p_right": float(bell.cdf(Z_RIGHT)),
        "delay_p_right": float(delay.cdf(x_right_delay)),
        # z at x = 0 on the delay clock: (0 - 20) / 20 = -1.
        "delay_support_min_z": (0.0 - MU_DELAY) / SIGMA_DELAY,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(delay, comparison: dict[str, float]) -> Path:
    """Plot standardized bell and delay densities on the z axis.

    Parameters
    ----------
    delay:
        Frozen exponential from delay_model().
    comparison:
        Dict from percentile_mismatch(); accepted so the signature
        matches the call in main(), and unused in the drawing.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Both curves are drawn against z, not raw x. The bell is
    stats.norm.pdf(z). The delay uses the change of variable
        X = mu + sigma Z,  f_Z(z) = f_X(mu + sigma z) * sigma
    so the areas remain probabilities on the z axis. Where
    mu + sigma z < 0 the exponential density is zero, which is why
    z = -1 sits at the left wall instead of at a 16% tail.
    """
    output_path = DIR_FIGURES / "standard_normal_03_skew_breaks_z.png"
    z = np.linspace(-3.5, 4.5, 500)
    # Unbound standard-normal pdf on the z grid.
    bell_y = stats.norm.pdf(z)
    # Map each z back to a delay time, then rescale the density by sigma.
    x_delay = MU_DELAY + z * SIGMA_DELAY
    delay_y = delay.pdf(x_delay) * SIGMA_DELAY
    # Negative delay times are outside the support; force those heights to 0.
    delay_y = np.where(x_delay >= 0, delay_y, 0.0)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(z, bell_y, color="#1A2E51", lw=2.2, label="Standard normal")
    ax.plot(z, delay_y, color="#EC2661", lw=2.2, label="Standardized exponential")
    ax.axvline(Z_LEFT, color="#646464", ls="--", lw=1.3, label="z = -1")
    ax.set_xlabel("z = (x - mu) / sigma")
    ax.set_ylabel("Density")
    ax.set_title("z = -1 Is 16% on a Bell and 0% on a Delay Clock")
    ax.set_xlim(-3.5, 4.5)
    ax.set_ylim(0, 1.05)
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
    """Run the Step 3 skew-limit report and write the overlay figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    delay = delay_model()
    comparison = percentile_mismatch(delay)
    figure_path = save_figure(delay, comparison)

    print("================================================================")
    print("LESSON 21 - STEP 3: SKEW BREAKS Z")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Delay mean = delay sd           : {comparison['delay_mean']:.6f}")
    print(f"Delay support starts at z       : {comparison['delay_support_min_z']:.6f}")
    print(f"Bell x at z = -1                : {comparison['x_left_bell']:.6f}")
    print(f"Delay x at z = -1               : {comparison['x_left_delay']:.6f}")
    # cdf on N(0, 1), not a probability that transfers to the delay clock.
    print(f"Normal P(Z <= -1)               : {comparison['bell_p_left']:.6f}")
    print(f"Delay P(X <= 0)                 : {comparison['delay_p_left']:.6f}")
    print(f"Normal P(Z <= 1.25)             : {comparison['bell_p_right']:.6f}")
    print(f"Delay P(Z <= 1.25)              : {comparison['delay_p_right']:.6f}")
    print("Limit: z-score comparison requires similar shape")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

