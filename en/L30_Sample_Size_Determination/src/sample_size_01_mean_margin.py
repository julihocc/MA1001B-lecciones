"""
Lesson 30 - Step 1: Sample Size for a Mean Margin of Error
==========================================================
NEW IN THIS STEP: mean_sample_size(), round_up_n(), and save_figure().

Context:
A fully synthetic operations study wants a 95% interval for mean handling
time with margin of error E = 2 minutes. A planning value s = 10 minutes
is treated as the scale. The mean sample-size formula is n = (z* s / E)^2,
then rounded up to the next integer.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds the mean sample-size
formula and the round-up rule used before any data are collected.

    n = (z_star * s / E) ** 2    rearrange E = z* s / sqrt(n) for n
    np.ceil(raw_n)               next whole observation; never round down
    ax.bar                       required n versus target E, z* and s fixed
    zip(bars, ns)                pair each bar with its height for labels

main() plugs in z* = 1.96, s = 10 minutes, and E = 2 minutes, prints the
raw and rounded-up n, and writes the evidence figure. No earlier lesson
script is imported.

Run it:
    python sample_size_01_mean_margin.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# Textbook z* for a 95% normal interval. Same critical value used to
# build the mean CI in Lesson 27; here it enters the sample-size formula.
Z_STAR = 1.96
# Planning standard deviation, in minutes. Chosen before sampling; it is
# not computed from a future sample.
S_PLAN = 10.0
# Target margin of error for the mean, in minutes. Smaller E demands a
# larger n because n grows with 1/E^2.
E_MEAN = 2.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) mean_sample_size() ----------------------------------------------
def mean_sample_size(z_star: float, s: float, margin: float) -> dict[str, float]:
    """Return the raw n = (z* s / E)^2 before integer rounding.

    Parameters
    ----------
    z_star:
        Normal critical value for the planned confidence level. The
        lesson uses 1.96 for 95%.
    s:
        Planning standard deviation of one observation, in the same
        units as the margin. Here s = 10 minutes.
    margin:
        Target margin of error E. Here E = 2 minutes.

    Returns
    -------
    dict[str, float]
        z_star, s, and margin echo the inputs. raw_n is the unrounded
        sample size (z* s / E)^2. dict[str, float] is a type hint: keys
        are strings and values are floats. Python does not enforce it.

    Notes
    -----
    A 95% mean interval has half-width E = z* s / sqrt(n). Solving for
    n gives n = (z* s / E)^2. The arithmetic below is that formula:
    multiply z* by s, divide by E, then square. The result is usually
    not an integer, so Step 1 still has to round up.
    """
    # n = (z* s / E)^2. Parentheses force (z* s / E) before the square.
    # For z*=1.96, s=10, E=2: (1.96 * 10 / 2)^2 = 9.8^2 = 96.04.
    raw = (z_star * s / margin) ** 2
    return {
        "z_star": z_star,
        "s": s,
        "margin": margin,
        # float(...) makes a plain Python float for printing, even if
        # the ** 2 result arrived as a NumPy scalar.
        "raw_n": float(raw),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) round_up_n() ----------------------------------------------------
def round_up_n(raw_n: float) -> int:
    """Round a raw sample size up to the next whole observation.

    Parameters
    ----------
    raw_n:
        Unrounded n = (z* s / E)^2 from mean_sample_size().

    Returns
    -------
    int
        The smallest integer greater than or equal to raw_n. 96.04
        becomes 97, not 96.

    Notes
    -----
    np.ceil returns a float (or a NumPy floating scalar). int(...)
    converts that ceiling to a whole count of observations. Rounding
    down would plan a sample whose interval is slightly wider than E.
    """
    return int(np.ceil(raw_n))
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(raw_n: float, n_required: int) -> Path:
    """Save n versus margin of error for a mean, holding z* and s fixed.

    Parameters
    ----------
    raw_n:
        Unrounded n at the lesson margin E = 2. The bar heights are
        rebuilt from Z_STAR, S_PLAN, and a grid of E values; this
        argument documents the planned case.
    n_required:
        Rounded-up n at E = 2, the magenta bar in the figure.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Each bar is ceil((z* s / E)^2) at that E. Halving E multiplies n
    by four because E sits in the denominator and is then squared.
    Magenta marks the lesson target E = 2 minutes.
    """
    output_path = DIR_FIGURES / "sample_size_01_mean_margin.png"
    # Five planning margins, in minutes. E_MEAN = 2.0 sits in the middle.
    margins = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
    # Same n = (z* s / E)^2 formula, now as a vector. NumPy divides the
    # scalar (Z_STAR * S_PLAN) by each margin, squares, then ceil.
    ns = np.ceil((Z_STAR * S_PLAN / margins) ** 2)
    # Magenta for the lesson E; blue for the other planning values.
    colors = ["#5B8DEF" if m != E_MEAN else "#EC2661" for m in margins]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # str(m) makes categorical x labels ("1.0", "1.5", ...) so the bars
    # are evenly spaced rather than placed on a numeric minute axis.
    bars = ax.bar([str(m) for m in margins], ns, color=colors, width=0.62)
    ax.set_xlabel("Target margin of error E (minutes)")
    ax.set_ylabel("Required sample size n")
    ax.set_title("Mean Sample Size n = (z* s / E)^2, Rounded Up")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each BarContainer patch with its height so the label
    # can sit at the bar center, a few units above the top.
    for bar, value in zip(bars, ns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2,
            f"{int(value)}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 mean sample-size report and write the E-versus-n figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    plan = mean_sample_size(Z_STAR, S_PLAN, E_MEAN)
    # 96.04 observations cannot be sampled; ceil to 97.
    n_required = round_up_n(plan["raw_n"])
    figure_path = save_figure(plan["raw_n"], n_required)

    print("================================================================")
    print("LESSON 30 - STEP 1: SAMPLE SIZE FOR A MEAN")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Textbook z-star                 : {plan['z_star']:.6f}")
    print(f"Planning s (minutes)            : {plan['s']:.6f}")
    print(f"Target margin E (minutes)       : {plan['margin']:.6f}")
    # Same n = (z s / E)^2 printed with six decimals so the README can
    # quote the exact raw value 96.040000 before rounding.
    print(f"Raw n = (z s / E)^2             : {plan['raw_n']:.6f}")
    print(f"Rounded-up n                    : {n_required}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

