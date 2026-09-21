"""
Lesson 33 - Step 2: Simulated Type I Error Rate
===============================================

THE RECIPE
----------
Start from ht_foundations_01_hypotheses_alpha.py, then introduce:
    1. simulate_type_i()    10000 samples generated under H0: mu = 50
    2. type_i_rate()        share of samples that reject H0
    3. save_figure()        histogram of xbar under H0 with the cutoff

Context:
--------
A Type I error is rejecting a true H0. With alpha = 0.05 the simulated
rate should land near 0.05 when H0 is true. We are going to simulate
drawing many samples assuming our baseline (H0) is correct, and observe
how often we mistakenly trigger our rejection condition.

How to read this file:
----------------------
In software engineering terms, think of H0 as your production system
operating correctly. A Type I error is a "false positive" alert from your
monitoring system (rejecting H0). We set `alpha = 0.05`, meaning we accept
a 5% false positive rate. This script runs a Monte Carlo simulation (a large
loop of randomized tests) to verify that if the system is truly behaving normally
(mu = 50), our alerting logic (`xbars >= xbar_crit`) only fires about 5% of the time.

Run it:
-------
    uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_02_type_i_rate.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# Use the Agg backend for matplotlib for rendering plots to files without UI
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Global configuration and assumed parameters
SEED = 42           # Random seed for identical simulated draws
N = 36              # Sample size (n)
MU0 = 50.0          # The population mean under the null hypothesis
SIGMA = 8.0         # Population standard deviation
ALPHA = 0.05        # Targeted Type I error rate (Significance level)
N_REPS = 10_000     # Number of simulation iterations

# Setup output directory for figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def rejection_cutoff() -> dict[str, float]:
    """
    Return SE, z critical value, and xbar cutoff under H0.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, float]
        Dictionary with standard error (se), z critical value (z_crit),
        and the sample mean cutoff threshold (xbar_crit).
    """
    # Calculate Standard Error (SE)
    se = SIGMA / np.sqrt(N)

    # Calculate z-critical value for right-tailed test
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))

    return {
        "se": float(se),
        "z_crit": z_crit,
        "xbar_crit": float(MU0 + z_crit * se),
    }


# --- NEW (1) simulate_type_i() -----------------------------------------------
def simulate_type_i(n_reps: int = N_REPS) -> np.ndarray:
    """
    Draw sample means under H0: mu = 50 with seed 42.

    Parameters
    ----------
    n_reps : int, optional
        Number of simulated samples to draw. Defaults to N_REPS.

    Returns
    -------
    np.ndarray
        A 1D numpy array of length `n_reps` containing the mean of each
        simulated sample.

    Notes
    -----
    We simulate drawing `n_reps` batches of size `N` from a normal distribution
    centered exactly at MU0. This simulates a world where H0 is perfectly true.
    """
    # Initialize the random number generator with our SEED
    rng = np.random.default_rng(SEED)

    # Draw (n_reps x N) matrix of normally distributed values
    samples = rng.normal(MU0, SIGMA, size=(n_reps, N))

    # Calculate the mean for each simulated sample (along the columns axis)
    return np.mean(samples, axis=1)
# ------------------------------------------------------------------------------


# --- NEW (2) type_i_rate() ---------------------------------------------------
def type_i_rate(xbars: np.ndarray, xbar_crit: float) -> dict[str, float]:
    """
    Share of H0 samples whose mean falls in the rejection region.

    Parameters
    ----------
    xbars : np.ndarray
        Array of simulated sample means.
    xbar_crit : float
        The cutoff value above which we reject H0.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - n_reps: Total number of replications.
        - n_rejections: Number of times H0 was incorrectly rejected.
        - type_i_rate: The empirical Type I error rate (should be close to alpha).

    Notes
    -----
    This calculates our empirical false-positive rate. Because these samples
    were drawn from MU0, any rejection is by definition a Type I error.
    """
    # Create a boolean array where True means we rejected H0
    rejections = xbars >= xbar_crit

    return {
        "n_reps": float(xbars.size),
        "n_rejections": float(np.sum(rejections)),
        "type_i_rate": float(np.mean(rejections)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(xbars: np.ndarray, xbar_crit: float) -> Path:
    """
    Histogram of simulated xbar under H0, with the alpha cutoff.

    Parameters
    ----------
    xbars : np.ndarray
        Array of simulated sample means.
    xbar_crit : float
        The cutoff value for rejecting H0.

    Returns
    -------
    Path
        Absolute path to the saved histogram PNG file.

    Notes
    -----
    Provides a visual check that our simulated Type I errors (area to the
    right of the red line) correspond to our specified alpha.
    """
    output_path = DIR_FIGURES / "ht_foundations_02_type_i_rate.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot histogram of our simulated sample means
    ax.hist(xbars, bins=30, color="#A7B0BF", edgecolor="white", density=True)

    # Add vertical line for the rejection cutoff
    ax.axvline(xbar_crit, color="#EC2661", linewidth=2.2,
               label=f"Cutoff = {xbar_crit:.2f}")

    # Formatting
    ax.set_xlabel("Sample mean xbar under H0")
    ax.set_ylabel("Density")
    ax.set_title("Type I Errors: Rejecting a True H0")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    # Save and clean up
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Determine the exact rejection threshold
    cutoff = rejection_cutoff()

    # 2. Simulate 10,000 samples under the assumption H0 is true
    xbars = simulate_type_i()

    # 3. Calculate how often we incorrectly reject H0 (Type I error)
    rates = type_i_rate(xbars, cutoff["xbar_crit"])

    # 4. Save visualization
    figure_path = save_figure(xbars, cutoff["xbar_crit"])

    print("================================================================")
    print("LESSON 33 - STEP 2: TYPE I ERROR RATE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS}")
    print("True mu (H0 is true)            : 50.000000")
    print(f"xbar cutoff                     : {cutoff['xbar_crit']:.6f}")
    print(f"Rejections                      : {int(rates['n_rejections'])}")
    print(f"Simulated Type I rate           : {rates['type_i_rate']:.6f}")
    print(f"Nominal alpha                   : {ALPHA:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

