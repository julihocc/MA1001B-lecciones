"""
Lesson 35 - Step 1: Sample Mean, Sample s, and the t Statistic
==============================================================
THE RECIPE
----------
NEW IN THIS STEP: build_pack_times(), t_statistic(), and save_figure().

Context:
--------
A fully synthetic pack-out line claims that mean cycle time is 50 minutes.
Operations draws n = 40 completed packs. Unlike a z test, the population
standard deviation is unknown, so the standard error uses the sample s and
the reference distribution is Student t with df = n - 1.

How to read this file:
----------------------
If you know Python OOP, think of `t_statistic` as calculating the attributes
for a Student's t object: it stores the mean (xbar), standard deviation (s),
standard error (se), and degrees of freedom (df). Because we don't know the
population variance, we replace it with `s` and adjust the degrees of freedom.

Run it:
-------
    python t_test_mean_01_sample_standard_error.py
"""

# The pathlib module allows us to work with file paths in an OS-independent OOP way.
from pathlib import Path

# matplotlib is used for rendering our histograms and distribution plots.
import matplotlib
# numpy provides vectorised mathematical operations and random number generation.
import numpy as np

# We use the "Agg" backend so matplotlib can save files without requiring an active display.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
# SEED ensures that the pseudo-random number generator produces the same values every time.
SEED = 42
# N is our sample size (n=40).
N = 40
# MU0 is our null hypothesis mean. We test if the population mean equals this value.
MU0 = 50.0
# PROCESS_MEAN is the true underlying population mean for our synthetic dataset.
PROCESS_MEAN = 52.0
# PROCESS_SD is the true underlying standard deviation for our synthetic dataset.
PROCESS_SD = 6.0

# Define the absolute path for the directory where generated figures will be stored.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists; if it doesn't, create it.
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_pack_times() ----------------------------------------------
def build_pack_times(seed: int = SEED) -> np.ndarray:
    """
    Draw n = 40 synthetic pack-out cycle times in minutes.

    Parameters
    ----------
    seed : int, optional
        The random seed to ensure reproducibility. Defaults to SEED.

    Returns
    -------
    np.ndarray
        A 1-dimensional array containing N random normally distributed cycle times.

    Notes
    -----
    This function uses numpy's default random number generator to create synthetic
    data that mimics a real-world pack-out process.
    """
    # Initialise the random number generator using our seed.
    rng = np.random.default_rng(seed)
    # Generate N samples from a normal distribution with the specified mean and scale.
    return rng.normal(loc=PROCESS_MEAN, scale=PROCESS_SD, size=N)
# ------------------------------------------------------------------------------


# --- NEW (2) t_statistic() ---------------------------------------------------
def t_statistic(times: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """
    Compute x-bar, s, SE, degrees of freedom, and the one-sample t.

    Parameters
    ----------
    times : np.ndarray
        The array of sampled cycle times.
    mu0 : float, optional
        The hypothesized population mean under the null hypothesis (H0). Defaults to MU0.

    Returns
    -------
    dict[str, float]
        A dictionary containing the calculated statistics:
        - "n": sample size
        - "xbar": sample mean
        - "sample_sd": sample standard deviation (s)
        - "se": standard error of the mean
        - "df": degrees of freedom (n - 1)
        - "t_stat": the calculated t-statistic
        - "mu0": the hypothesized mean

    Notes
    -----
    Notice the use of `ddof=1` when calculating the standard deviation. This
    applies Bessel's correction, dividing by (N-1) rather than N, giving us
    an unbiased estimator of the population variance.
    """
    # Count the number of observations
    n = times.size
    # Calculate the arithmetic mean of the sample
    xbar = float(np.mean(times))
    # Calculate the sample standard deviation using ddof=1 for an unbiased estimate
    sample_sd = float(np.std(times, ddof=1))
    # Standard error is the sample standard deviation divided by the square root of n
    se = sample_sd / np.sqrt(n)
    # The t-statistic measures how many standard errors xbar is away from mu0
    t_stat = (xbar - mu0) / se

    # Return the dictionary containing all calculated values
    return {
        "n": float(n),
        "xbar": xbar,
        "sample_sd": sample_sd,
        "se": float(se),
        "df": float(n - 1),
        "t_stat": float(t_stat),
        "mu0": mu0,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(times: np.ndarray, summary: dict[str, float]) -> Path:
    """
    Save a histogram of pack times with the hypothesized and sample means.

    Parameters
    ----------
    times : np.ndarray
        The sample array of pack times.
    summary : dict[str, float]
        The dictionary returned by `t_statistic()`, containing mu0 and xbar.

    Returns
    -------
    Path
        The absolute path to the saved figure file.

    Notes
    -----
    This generates a 10-bin histogram and plots two vertical lines: one for the
    hypothesized mean (H0) and one for our calculated sample mean. This gives
    us a visual indication of how far our sample deviates from the hypothesis.
    """
    # Define the exact output file path inside our figures directory
    output_path = DIR_FIGURES / "t_test_mean_01_sample_standard_error.png"

    # Create a matplotlib figure and axis with specific dimensions
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot a histogram with 10 bins
    ax.hist(times, bins=10, color="#5B8DEF", edgecolor="#1A2E51", alpha=0.85)

    # Draw a vertical dashed line for the hypothesized mean
    ax.axvline(summary["mu0"], color="#646464", linestyle="--", linewidth=1.8,
               label=f"H0 mean = {summary['mu0']:.0f}")

    # Draw a vertical solid line for the actual sample mean
    ax.axvline(summary["xbar"], color="#EC2661", linestyle="-", linewidth=1.8,
               label=f"sample mean = {summary['xbar']:.2f}")

    # Add labels and formatting
    ax.set_xlabel("Pack-out cycle time (minutes)")
    ax.set_ylabel("Frequency")
    ax.set_title("n = 40 Synthetic Pack Times; Sigma Unknown")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout to prevent clipping and save the figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    # Return the file path so the main script can announce where the file is
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the synthetic sample data
    times = build_pack_times()
    # 2. Compute the t-statistic and related properties
    summary = t_statistic(times)
    # 3. Create and save a visualization of the data
    figure_path = save_figure(times, summary)

    # Output the results to the terminal
    print("================================================================")
    print("LESSON 35 - STEP 1: SAMPLE STANDARD ERROR AND t STATISTIC")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {int(summary['n'])}")
    print(f"Hypothesized mean mu0           : {summary['mu0']:.6f}")
    print(f"Sample mean x-bar               : {summary['xbar']:.6f}")
    print(f"Sample standard deviation s     : {summary['sample_sd']:.6f}")
    print(f"Standard error s/sqrt(n)        : {summary['se']:.6f}")
    print(f"Degrees of freedom n-1          : {int(summary['df'])}")
    print(f"t statistic (x-bar - mu0)/SE    : {summary['t_stat']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

