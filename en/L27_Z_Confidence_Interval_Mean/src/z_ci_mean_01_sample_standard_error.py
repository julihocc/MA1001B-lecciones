"""
Lesson 27 - Step 1: Sample Mean and Known-Sigma Standard Error
==============================================================
NEW IN THIS STEP: generate_fill_sample(), sampling_metrics(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. generate_fill_sample()   n = 36 iid fills from N(502, 10)
    2. sampling_metrics()       xbar and SE = sigma / sqrt(n)
    3. save_figure()            histogram with the mean and one SE band

Context:
A fully synthetic filling line produces beverage bottles. Historical process
capability treats the population standard deviation as known: sigma = 10 ml.
A seed-42 sample of n = 36 bottles is drawn to estimate the unknown mean
fill volume. The sampling standard error is sigma / sqrt(n).

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lessons 23-24 built SE = sigma / sqrt(n)
and the sampling distribution of xbar. Lesson 26 treated xbar as a point
estimator of mu. This script draws one n = 36 sample and reports that SE.

    np.random.default_rng(seed)   reproducible Generator; 42 is the course seed
    rng.normal(loc, scale, size)  iid N(mu, sigma) fills; loc is mu, scale is sd
    np.mean(sample)               the point estimate xbar
    SIGMA / np.sqrt(N)            known-sigma standard error of xbar
    ax.axvline / ax.axvspan       mark xbar and shade one SE around it
    dict[str, float]              a type hint: string keys, float values

main() reports n, sigma, hidden mu, xbar, and SE = 10/sqrt(36) = 1.666667,
then writes the histogram. No earlier lesson script is imported. The SE
band is not yet a confidence interval; that is Step 2.

Run it:
    uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_01_sample_standard_error.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the sample and the SE arithmetic.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. Every Normal draw goes through this seed.
SEED = 42
# n = 36 bottles. sqrt(36) = 6, so SE = 10/6 is a clean textbook value.
N = 36
# Known population sd from long-run process capability, not from this sample.
SIGMA = 10.0
# True mean used only to generate data and, in later steps, to check coverage.
# The analyst who sees the 36 fills does not know this number.
MU_TRUE = 502.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) generate_fill_sample() ------------------------------------------
def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills from N(mu_true, sigma). The analyst does not know mu.

    Parameters
    ----------
    seed:
        Generator seed. Default SEED = 42 so this sample is identical
        every run and matches Steps 2-3.

    Returns
    -------
    np.ndarray
        Length-n vector of fill volumes in millilitres, one bottle per
        entry. dtype is NumPy's default float.

    Notes
    -----
    default_rng(seed) is NumPy's modern Generator. rng.normal uses loc
    for the mean and scale for the sd of one fill X, not of xbar.
    The draws are iid N(502, 10). mu is hidden from the analyst; it is
    in the code only so later steps can check whether an interval covers
    the data-generating mean. Fully synthetic: no plant file is read.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)
# ------------------------------------------------------------------------------


# --- NEW (2) sampling_metrics() ----------------------------------------------
def sampling_metrics(sample: np.ndarray) -> dict[str, float]:
    """Return the sample mean and the known-sigma standard error.

    Parameters
    ----------
    sample:
        The n = 36 fills from generate_fill_sample().

    Returns
    -------
    dict[str, float]
        n and sigma are stored as floats so every value in the dict has
        the same type. xbar is the point estimate of mu. se is
        sigma / sqrt(n), the sd of xbar when sigma is known.

    Notes
    -----
    Lessons 23-24 derived SE(xbar) = sigma / sqrt(n) for an iid mean.
    Here sigma = 10 is treated as known from process capability, so the
    SE does not use the sample standard deviation. For this n,
        SE = 10 / sqrt(36) = 10 / 6 = 1.666667 ml.
    float(np.mean(...)) unwraps a NumPy scalar into a Python float for
    printing. This function does not yet form an interval; it only
    reports the centre and the SE that Step 2 will multiply by z*.
    """
    xbar = float(np.mean(sample))
    # Known-sigma SE of the sample mean, not the sd of one bottle.
    se = SIGMA / np.sqrt(N)
    return {
        "n": float(N),
        "sigma": SIGMA,
        "xbar": xbar,
        "se": float(se),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Save a histogram of fills with the sample mean and SE band.

    Parameters
    ----------
    sample:
        The n = 36 fills plotted as the histogram.
    metrics:
        Dictionary from sampling_metrics() with xbar and se.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The red line is the observed mean, the point estimate of mu. The
    blue band is xbar +/- one SE, a picture of sampling variability of
    the mean, not a 95% confidence interval. Step 2 multiplies that SE
    by z* = 1.96 to get the interval half-width.
    """
    output_path = DIR_FIGURES / "z_ci_mean_01_sample_standard_error.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")
    ax.axvline(
        metrics["xbar"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Sample mean = {metrics['xbar']:.2f} ml",
    )
    # One SE on each side of xbar. This band is not the z interval.
    ax.axvspan(
        metrics["xbar"] - metrics["se"],
        metrics["xbar"] + metrics["se"],
        color="#5B8DEF",
        alpha=0.22,
        label=f"SE = {metrics['se']:.4f} ml",
    )
    ax.set_xlabel("Fill volume (ml)")
    ax.set_ylabel("Count of bottles")
    ax.set_title("Known Sigma: Standard Error of the Sample Mean")
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
    """Run the Step 1 mean-and-SE report and write the histogram.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    metrics = sampling_metrics(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LESSON 27 - STEP 1: SAMPLE MEAN AND STANDARD ERROR")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma (ml)                : {metrics['sigma']:.6f}")
    print(f"True mu (hidden from analyst)   : {MU_TRUE:.6f}")
    print(f"Sample mean xbar (ml)           : {metrics['xbar']:.6f}")
    print(f"Standard error sigma/sqrt(n)    : {metrics['se']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

