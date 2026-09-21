"""
Lesson 31 - Step 1: Sample Variance from a Small Normal Sample
==============================================================
NEW IN THIS STEP: generate_cycle_sample(), sample_variance(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. generate_cycle_sample()  n = 20 iid N(12, 3) cycle times, seed 42
    2. sample_variance()        s^2 with divisor n - 1, so df = 19
    3. save_figure()            histogram with mean and s marked

Context:
A fully synthetic packing station records n = 20 cycle times. The process
is treated as normal. The sample variance s^2 estimates the unknown
population variance sigma^2, with df = n - 1 = 19.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lesson 03 introduced sample s with
divisor n-1. This script is the point estimate that later steps wrap in a
chi-square interval for sigma^2.

    np.random.default_rng(seed)  Generator with the course-wide seed 42
    rng.normal(loc, scale, n)    n iid Normal(mu, sigma) cycle times
    np.var(sample, ddof=1)       sample variance s^2, divisor n-1
    df = n - 1                   degrees of freedom once the mean is estimated
    ax.axvline                   vertical reference at x-bar and at x-bar +/- s

The analyst sees n, x-bar, s, and s^2. Hidden sigma^2 = 9 is a teaching
check, not an observed value. Step 2 will use (n-1)s^2 / chi-square
quantiles; Step 3 will show that formula fails when the cycles are not
normal.

main() reports n, df, x-bar, s, s^2, and the hidden sigma^2, then writes
the histogram. No earlier lesson script is imported.

Run it:
    uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_01_sample_variance.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the numeric sample and computes
# mean and variance. The aliases are the same ones used from Lesson 01.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. Change it only if a later lesson says so.
SEED = 42
# n = 20 cycle times: large enough to compute s^2, small enough that the
# chi-square interval in Step 2 is visibly asymmetric.
N = 20
# Hidden Normal(mu, sigma) process. loc is the mean; scale is the standard
# deviation, not the variance. The analyst does not know these values.
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) generate_cycle_sample() -----------------------------------------
def generate_cycle_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid normal cycle times. The analyst does not know sigma^2.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's generator. Default is the
        module-level SEED = 42 so Steps 2 and 3 rebuild the same sample.

    Returns
    -------
    np.ndarray
        Length N = 20. Each entry is one synthetic cycle time in minutes,
        drawn iid from Normal(MU_TRUE, SIGMA_TRUE). Re-running with the
        same seed reproduces the identical array.

    Notes
    -----
    iid means independent and identically distributed: every cycle is an
    independent draw from the same Normal(12, 3) process. That normality
    is an assumption the chi-square interval in Step 2 will require, not
    a fact the analyst can read off 20 numbers.

    rng.normal uses loc for the mean and scale for the standard deviation.
    The hidden variance is therefore SIGMA_TRUE ** 2 = 9, not 3.
    """
    # default_rng(seed) returns a Generator. All draws in this function go
    # through rng so they form one reproducible stream. See Lesson 01.
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)
# ------------------------------------------------------------------------------


# --- NEW (2) sample_variance() -----------------------------------------------
def sample_variance(sample: np.ndarray) -> dict[str, float]:
    """Return s^2 with divisor n - 1 and the hidden population variance.

    Parameters
    ----------
    sample:
        Length-n array of cycle times from generate_cycle_sample().

    Returns
    -------
    dict[str, float]
        n is the sample size. df is n - 1. xbar is the sample mean.
        s is the sample standard deviation. s2 is the sample variance,
        the point estimate of sigma^2. hidden_sigma2 is the teaching
        value SIGMA_TRUE ** 2 = 9; an analyst would not observe it.

    Notes
    -----
    Sample variance uses divisor n - 1, not n. One degree of freedom is
    spent estimating the mean from the same sample, so
        s^2 = sum((x_i - x-bar)^2) / (n - 1),    df = n - 1 = 19.
    NumPy's np.var defaults to ddof=0 (divisor n). Pass ddof=1 explicitly
    so the sample convention is visible. pandas Series.std already
    defaults to ddof=1; that is the same Bessel correction as Lesson 03.

    s = sqrt(s^2) is a scale in minutes. s^2 is the quantity the
    chi-square interval in Step 2 will bound, in minutes squared.
    """
    # ddof=1 is "delta degrees of freedom": subtract 1 from n in the
    # divisor. float(...) unwraps the NumPy scalar into a plain Python
    # float for printing.
    s2 = float(np.var(sample, ddof=1))
    return {
        "n": float(N),
        "df": float(N - 1),
        "xbar": float(np.mean(sample)),
        "s": float(np.sqrt(s2)),
        "s2": s2,
        "hidden_sigma2": SIGMA_TRUE ** 2,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Save a histogram of cycle times with s marked as the scale.

    Parameters
    ----------
    sample:
        The n = 20 cycle times.
    metrics:
        Dictionary from sample_variance(), used here for x-bar and s.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The filled histogram is the sample of 20 times. The solid line is
    x-bar. The dashed lines are x-bar +/- s, a visual scale for spread,
    not a confidence interval. The interval for sigma^2 appears in Step 2.
    """
    output_path = DIR_FIGURES / "chi2_var_01_sample_variance.png"
    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=8, color="#A7B0BF", edgecolor="white")
    # Solid magenta: the sample mean, a location. Dashed blue: one
    # sample standard deviation on each side, a scale in minutes.
    ax.axvline(metrics["xbar"], color="#EC2661", linewidth=2.4,
               label=f"Mean = {metrics['xbar']:.2f} min")
    ax.axvline(metrics["xbar"] - metrics["s"], color="#5B8DEF",
               linestyle="--", linewidth=1.6)
    ax.axvline(metrics["xbar"] + metrics["s"], color="#5B8DEF",
               linestyle="--", linewidth=1.6,
               label=f"s = {metrics['s']:.2f} min")
    ax.set_xlabel("Cycle time (minutes)")
    ax.set_ylabel("Count of cycles")
    ax.set_title("Sample Variance from n = 20 Normal Cycle Times")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 sample-variance report and write the evidence figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_cycle_sample()
    metrics = sample_variance(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LESSON 31 - STEP 1: SAMPLE VARIANCE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    # df = n - 1 = 19. This is the chi-square degrees of freedom in Step 2.
    print(f"Degrees of freedom n-1          : {int(metrics['df'])}")
    print(f"Sample mean (min)               : {metrics['xbar']:.6f}")
    print(f"Sample standard deviation s     : {metrics['s']:.6f}")
    # s^2 with divisor n-1 is the point estimate of sigma^2.
    print(f"Sample variance s^2             : {metrics['s2']:.6f}")
    # Teaching check only: the analyst would not know this value.
    print(f"Hidden sigma^2                  : {metrics['hidden_sigma2']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

