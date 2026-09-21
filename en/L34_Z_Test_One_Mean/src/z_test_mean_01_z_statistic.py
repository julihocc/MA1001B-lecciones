"""
Lesson 34 - Step 1: Z Statistic for a Mean with Known Sigma
===========================================================
THE RECIPE
NEW IN THIS STEP: generate_delivery_sample(), z_statistic(), and
save_figure().

Context:
A fully synthetic last-mile process treats sigma = 6 minutes as known.
A seed-42 sample of n = 40 deliveries is tested against H0: mu = 80
minutes. The z statistic is (xbar - mu0) / (sigma / sqrt(n)).

How to read this file:
For a student familiar with Python OOP, think of this script as setting up the "state"
and "behavior" of our statistical test sequentially rather than in a class. The constants
at the top are our initial state, representing a synthetic world (population) and our
specific test parameters. `generate_delivery_sample` represents the data collection
phase. `z_statistic` encapsulates the core logic of calculating the test statistic.
Finally, `save_figure` creates a visual representation of our data against the null
hypothesis threshold. In statistics, the Z-statistic tells us how many standard errors
our sample mean is away from the hypothesized population mean.

Run it:
    uv run en/L34_Z_Test_One_Mean/src/z_test_mean_01_z_statistic.py
"""

# pathlib handles filesystem paths in a cross-platform way.
from pathlib import Path

# matplotlib.use("Agg") is required for headless environments to prevent UI errors.
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# SEED ensures reproducibility of our synthetic data generation.
SEED = 42
# N is our sample size.
N = 40
# MU0 is the population mean under the null hypothesis (H0).
MU0 = 80.0
# MU_TRUE is the actual population mean used to generate the synthetic data.
MU_TRUE = 82.0
# SIGMA is the population standard deviation, assumed known in this specific test.
SIGMA = 6.0
# DIR_FIGURES is the destination directory for output plots.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists before trying to save into it.
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) generate_delivery_sample() --------------------------------------
def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """
    Draw n iid delivery times. The analyst knows sigma, not mu.

    Parameters
    ----------
    seed : int, optional
        The random seed for reproducibility. Default is SEED.

    Returns
    -------
    np.ndarray
        An array of N simulated delivery times drawn from a normal distribution.

    Notes
    -----
    This simulates the real-world process of collecting data, where the true mean
    is unknown to the analyst, but for this specific lesson's assumption, the
    population standard deviation (sigma) is known.
    """
    # Create a random number generator with the specified seed.
    rng = np.random.default_rng(seed)
    # Generate N samples from a normal distribution with mean MU_TRUE and std SIGMA.
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)
# ------------------------------------------------------------------------------


# --- NEW (2) z_statistic() ---------------------------------------------------
def z_statistic(sample: np.ndarray) -> dict[str, float]:
    """
    Compute xbar, SE, and the z statistic under H0: mu = 80.

    Parameters
    ----------
    sample : np.ndarray
        The observed sample data (e.g., delivery times).

    Returns
    -------
    dict[str, float]
        A dictionary containing the calculated metrics: n, mu0, sigma, xbar, se, and z.

    Notes
    -----
    The Standard Error (SE) is calculated as sigma / sqrt(n).
    The Z-statistic standardizes the difference between our sample mean (xbar) and
    the null hypothesis mean (MU0) using this standard error.
    """
    # Calculate the sample mean (xbar).
    xbar = float(np.mean(sample))
    # Calculate the standard error of the mean.
    se = SIGMA / np.sqrt(N)
    # Calculate the Z-statistic: how many SEs xbar is from MU0.
    z = (xbar - MU0) / se
    return {
        "n": float(N),
        "mu0": MU0,
        "sigma": SIGMA,
        "xbar": xbar,
        "se": float(se),
        "z": float(z),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """
    Save a histogram of deliveries with xbar and the H0 value.

    Parameters
    ----------
    sample : np.ndarray
        The observed sample data used to create the histogram.
    metrics : dict[str, float]
        The dictionary of computed statistics (must contain 'xbar').

    Returns
    -------
    Path
        The absolute path to the saved PNG figure.

    Notes
    -----
    This function generates a visual comparison between the distribution of the
    sample data, the sample mean, and the null hypothesis mean to provide an
    intuitive understanding of the Z-test.
    """
    # Define the output file path.
    output_path = DIR_FIGURES / "z_test_mean_01_z_statistic.png"

    # Initialize the figure and axes.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot the histogram of the sample.
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")

    # Plot a solid vertical line for the sample mean (xbar).
    ax.axvline(metrics["xbar"], color="#EC2661", linewidth=2.4,
               label=f"xbar = {metrics['xbar']:.2f} min")

    # Plot a dashed vertical line for the null hypothesis mean (MU0).
    ax.axvline(MU0, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label=f"H0 mu = {MU0:.0f} min")

    # Set labels, title, legend, and grid for better readability.
    ax.set_xlabel("Delivery time (minutes)")
    ax.set_ylabel("Count of deliveries")
    ax.set_title("Z Statistic from n = 40 Deliveries, sigma Known")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout and save the figure.
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)  # Close the figure to free up memory.

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the synthetic delivery sample.
    sample = generate_delivery_sample()

    # 2. Calculate the test statistic and related metrics.
    metrics = z_statistic(sample)

    # 3. Create and save the visualization.
    figure_path = save_figure(sample, metrics)

    # 4. Print the results to the console.
    print("================================================================")
    print("LESSON 34 - STEP 1: Z STATISTIC")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print("H0                             : mu = 80")
    print("H1                             : mu > 80")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma (min)               : {SIGMA:.6f}")
    print(f"Sample mean xbar (min)          : {metrics['xbar']:.6f}")
    print(f"SE = sigma/sqrt(n)              : {metrics['se']:.6f}")
    print(f"z = (xbar - 80) / SE            : {metrics['z']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

