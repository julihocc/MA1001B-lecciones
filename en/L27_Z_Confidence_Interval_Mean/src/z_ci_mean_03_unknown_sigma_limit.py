"""
Lesson 27 - Step 3: Unknown Sigma Makes the Z Interval the Wrong Tool
=====================================================================
THE RECIPE
Start from z_ci_mean_02_z_interval.py, then introduce:
    1. sample_standard_deviation()  s from the same n = 36 fills
    2. compare_known_vs_plug_in()   z interval with sigma versus z with s
    3. save_figure()                contrast the two intervals

Limit: operations data almost never come with a known population sigma.
Replacing sigma by s but keeping z* = 1.96 is not a valid z interval.
Lesson 28 replaces z* by a t critical value with df = n - 1.

How to read this file:
You already know Python through OOP. Steps 1-2 built the valid known-sigma
z interval xbar +/- 1.96 * sigma / sqrt(n). Lesson 01 covers pathlib and
unattended savefig. This step estimates sigma from the same sample and
keeps z* = 1.96 anyway.

    np.std(sample, ddof=1)        sample sd s; ddof=1 is the n-1 divisor
    s / sqrt(n)                   plug-in SE; s is a statistic, not sigma
    z* * s / sqrt(n)              invalid z-with-s margin (still z*, not t*)
    s != sigma                    8.390375 is not 10; the swap is the limit
    Lesson 28                     replace z* by t* with df = n - 1

main() prints s, both standard errors, both intervals, and the width
difference. The z-with-s interval is shown as the wrong tool, not as a
t interval.

Run it:
    uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_03_unknown_sigma_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical filling-line constants to Steps 1-2, including textbook z*.
SEED = 42
N = 36
SIGMA = 10.0
MU_TRUE = 502.0
# Still the known-sigma critical value. Keeping it after swapping s for
# sigma is exactly the invalid step this script is designed to show.
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills from N(mu_true, sigma). The analyst does not know mu.

    Rebuilt from Steps 1-2 so this file does not import those scripts.
    The same seed reproduces the same 36 fills, hence the same xbar.

    Parameters
    ----------
    seed:
        Generator seed. Default SEED = 42.

    Returns
    -------
    np.ndarray
        Length-n vector of synthetic fill volumes in millilitres.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


# --- NEW (1) sample_standard_deviation() -------------------------------------
def sample_standard_deviation(sample: np.ndarray) -> dict[str, float]:
    """Estimate sigma from the sample. This s is not a known parameter.

    Parameters
    ----------
    sample:
        The n = 36 fills from generate_fill_sample().

    Returns
    -------
    dict[str, float]
        xbar is the same point estimate as Steps 1-2. s is the sample
        standard deviation. se_known is sigma / sqrt(n). se_plug_in is
        s / sqrt(n), which is not a known-sigma standard error.

    Notes
    -----
    np.std(..., ddof=1) uses the n-1 divisor (Bessel's correction):
        s^2 = sum((x_i - xbar)^2) / (n - 1).
    ddof=0 would divide by n and estimate the population second moment
    of the sample, not the unbiased sample variance. s is a statistic:
    it changes from sample to sample. On this seed-42 draw,
    s = 8.390375, which is not sigma = 10. Treating s as if it were
    the known process sigma is the limit of the z procedure.
    """
    xbar = float(np.mean(sample))
    # Sample sd with n-1 in the denominator; this s is not SIGMA.
    s = float(np.std(sample, ddof=1))
    return {
        "xbar": xbar,
        "s": s,
        "se_known": SIGMA / np.sqrt(N),
        "se_plug_in": s / np.sqrt(N),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) compare_known_vs_plug_in() --------------------------------------
def compare_known_vs_plug_in(stats_s: dict[str, float]) -> dict[str, float]:
    """Keep z* = 1.96 but swap sigma for s. That swap is the pedagogical limit.

    Parameters
    ----------
    stats_s:
        Dictionary from sample_standard_deviation() with xbar and both SEs.

    Returns
    -------
    dict[str, float]
        known_* is the valid z interval from Step 2. plug_* is the same
        formula with s in place of sigma. width_difference is the
        absolute gap between those two widths. s_minus_sigma is s - 10.

    Notes
    -----
    The valid z interval is still
        xbar +/- z* * sigma / sqrt(n).
    The invalid companion is
        xbar +/- z* * s / sqrt(n),
    the same 1.96 times a data-dependent SE. That is not a z interval
    (sigma is unknown) and not a t interval (the critical value is still
    z*, not t* with df = n - 1). A shorter plug-in interval is not a
    better interval; it is the wrong procedure. Lesson 28 replaces z*
    by the t quantile.
    """
    # Valid margin: 1.96 * (sigma / sqrt(n)).
    known_margin = Z_STAR * stats_s["se_known"]
    # Invalid margin: 1.96 * (s / sqrt(n)). Same z*, different SE.
    plug_margin = Z_STAR * stats_s["se_plug_in"]
    return {
        "known_lower": stats_s["xbar"] - known_margin,
        "known_upper": stats_s["xbar"] + known_margin,
        "known_width": 2.0 * known_margin,
        "plug_lower": stats_s["xbar"] - plug_margin,
        "plug_upper": stats_s["xbar"] + plug_margin,
        "plug_width": 2.0 * plug_margin,
        "width_difference": 2.0 * abs(plug_margin - known_margin),
        "s_minus_sigma": stats_s["s"] - SIGMA,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    stats_s: dict[str, float],
    comparison: dict[str, float],
) -> Path:
    """Contrast the valid known-sigma z interval with the invalid z-with-s swap.

    Parameters
    ----------
    stats_s:
        Dictionary from sample_standard_deviation() with the shared xbar.
    comparison:
        Dictionary from compare_known_vs_plug_in() with both endpoints.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Two error bars share the same centre xbar. The upper bar is the
    valid z interval (sigma known). The lower bar is the invalid
    z-with-s interval. Because s < sigma on this sample, the lower bar
    is shorter; that is a warning, not an improvement. The dashed line
    is the hidden mu.
    """
    output_path = DIR_FIGURES / "z_ci_mean_03_unknown_sigma_limit.png"
    labels = ["Valid z interval\n(sigma known)", "Invalid z-with-s\n(sigma unknown)"]
    centers = [stats_s["xbar"], stats_s["xbar"]]
    # 2 x 2 xerr: row 0 is left errors, row 1 is right errors, one
    # column per interval. Distances from xbar, not the endpoints.
    xerr = np.array(
        [
            [
                stats_s["xbar"] - comparison["known_lower"],
                stats_s["xbar"] - comparison["plug_lower"],
            ],
            [
                comparison["known_upper"] - stats_s["xbar"],
                comparison["plug_upper"] - stats_s["xbar"],
            ],
        ]
    )
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        centers,
        [1.0, 0.0],
        xerr=xerr,
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=2.8,
        capsize=8,
        markersize=8,
    )
    ax.axvline(MU_TRUE, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"True mu = {MU_TRUE:.1f}")
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(labels)
    ax.set_xlabel("Fill volume (ml)")
    ax.set_title("Unknown Sigma Makes the Z Interval the Wrong Tool")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_ylim(-0.7, 1.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 unknown-sigma limit and write the contrast figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    stats_s = sample_standard_deviation(sample)
    comparison = compare_known_vs_plug_in(stats_s)
    figure_path = save_figure(stats_s, comparison)

    print("================================================================")
    print("LESSON 27 - STEP 3: UNKNOWN SIGMA LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma (ml)                : {SIGMA:.6f}")
    print(f"Sample mean xbar (ml)           : {stats_s['xbar']:.6f}")
    print(f"Sample standard deviation s     : {stats_s['s']:.6f}")
    print(f"s minus sigma                   : {comparison['s_minus_sigma']:.6f}")
    print(f"SE with known sigma             : {stats_s['se_known']:.6f}")
    print(f"SE with plug-in s               : {stats_s['se_plug_in']:.6f}")
    print(f"Valid z lower bound             : {comparison['known_lower']:.6f}")
    print(f"Valid z upper bound             : {comparison['known_upper']:.6f}")
    print(f"Valid z width                   : {comparison['known_width']:.6f}")
    print(f"Invalid z-with-s lower bound    : {comparison['plug_lower']:.6f}")
    print(f"Invalid z-with-s upper bound    : {comparison['plug_upper']:.6f}")
    print(f"Invalid z-with-s width          : {comparison['plug_width']:.6f}")
    print(f"Absolute width difference       : {comparison['width_difference']:.6f}")
    print("Limit                          : unknown sigma needs t, not z")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

