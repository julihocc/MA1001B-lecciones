"""
Lesson 24 - Step 1: A Right-Skewed Operating Population
=======================================================
NEW IN THIS STEP: delay_population(), population_summaries(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. delay_population()      Exponential delay clock, mean 10 minutes
    2. population_summaries()  mean, sd, median, skewness, P(X > 20)
    3. save_figure()           density with mean and median marked

Context:
A fully synthetic delay clock is Exponential with mean 10 minutes. The
population is right-skewed: mean = sd = 10, skewness = 2. The sampling
distribution of xbar is not yet in view.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script builds a right-skewed
population so Lesson 24 can show the Central Limit Theorem (CLT) later.
The CLT is about xbar, not about the original delays becoming normal; that
comparison starts in Step 2.

    scipy.stats.expon(scale=10)  frozen Exponential with mean = scale = 10
    model.mean / .std / .median  closed-form moments of that frozen rv
    model.stats(moments="s")     skewness; "s" requests the third moment
    1 - model.cdf(20)            P(X > 20), the survival function at 20
    mean > median                algebraic signature of right skew

main() reports mean = sd = 10, median about 6.93, skewness 2, and
P(X > 20), then writes the density figure. No earlier lesson script is
imported.

Run it:
    python clt_01_skewed_population.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the distribution library. stats.expon is the exponential
# family: SciPy uses scale = mean = 1/rate, not the rate lambda that some
# textbooks write first.
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers; the seed is reserved so later steps stay aligned.
SEED = 42
# Mean delay in minutes. For an exponential clock this one number is also
# the standard deviation, so mean = sd = 10 and skewness = 2.
MEAN = 10.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) delay_population() ----------------------------------------------
def delay_population():
    """Return the exponential delay population with mean 10 minutes.

    Returns
    -------
    frozen rv
        A frozen Exponential rv with scale = MEAN. Callers use .mean(),
        .std(), .median(), .pdf(), and .cdf() without passing parameters
        again.

    Notes
    -----
    scipy.stats.expon(scale=theta) is Exponential with pdf
        f(x) = (1/theta) * exp(-x/theta)  for x >= 0.
    The mean and the sd both equal theta. Skewness is 2 for every
    exponential, so this population is right-skewed no matter which
    mean we pick. The CLT will later say that xbar, not X itself,
    becomes approximately normal for large n.
    """
    # scale=MEAN locks the mean at 10. loc defaults to 0, so delays
    # cannot be negative: the support starts at the origin.
    return stats.expon(scale=MEAN)
# ------------------------------------------------------------------------------


# --- NEW (2) population_summaries() ------------------------------------------
def population_summaries(model) -> dict[str, float]:
    """Report mean, sd, skewness, and P(X > 20) for the delay clock.

    Parameters
    ----------
    model:
        Frozen exponential returned by delay_population().

    Returns
    -------
    dict[str, float]
        mean and sd are both 10. median is theta * ln(2) about 6.93.
        skewness is 2. p_gt_20 is P(X > 20) = exp(-2).

    Notes
    -----
    Right skew means a long right tail: the mean is pulled above the
    median. P(X > 20) is the chance a single delay exceeds twice the
    mean. float(...) converts each NumPy scalar that SciPy returns
    into a plain Python float for printing. The annotation
    `-> dict[str, float]` is a type hint; Python does not enforce it
    at run time.
    """
    return {
        "mean": float(model.mean()),
        "sd": float(model.std()),
        # moments="s" asks for skewness only. "mvsk" would also return
        # mean, variance, and kurtosis from the same frozen rv.
        "skewness": float(model.stats(moments="s")),
        # Survival at 20: 1 - F(20). For Exponential(10) this is e^{-2}.
        "p_gt_20": float(1.0 - model.cdf(20.0)),
        "median": float(model.median()),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(model) -> Path:
    """Plot the right-skewed exponential delay density.

    Parameters
    ----------
    model:
        Frozen exponential returned by delay_population().

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The curve is a density f(x), not a probability. The dashed red line
    is the mean; the dotted blue line is the median. Mean to the right
    of the median is the picture of right skew that Step 2 will try to
    wash out of xbar by taking larger n.
    """
    output_path = DIR_FIGURES / "clt_01_skewed_population.png"
    # 400 evaluation points on [0, 50] minutes. The exponential tail
    # continues forever, but density past 50 is already tiny.
    x = np.linspace(0, 50, 400)
    y = model.pdf(x)

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Exponential mean 10")
    ax.axvline(model.mean(), color="#EC2661", ls="--", lw=1.4, label="Mean 10")
    ax.axvline(model.median(), color="#5B8DEF", ls=":", lw=1.4, label="Median")
    ax.set_xlabel("Delay time (minutes)")
    ax.set_ylabel("Density f(x)")
    ax.set_title("Right-Skewed Delay Population: Skewness = 2")
    ax.set_xlim(0, 50)
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
    """Run the Step 1 population report and write the density figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = delay_population()
    values = population_summaries(model)
    figure_path = save_figure(model)

    print("================================================================")
    print("LESSON 24 - STEP 1: SKEWED POPULATION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Population mean                 : {values['mean']:.6f}")
    print(f"Population sd                   : {values['sd']:.6f}")
    # Median below the mean is the numerical signature of right skew.
    print(f"Population median               : {values['median']:.6f}")
    print(f"Population skewness             : {values['skewness']:.6f}")
    print(f"P(X > 20)                       : {values['p_gt_20']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

