"""
Lesson 33 - Step 3: Failing to Reject H0 Is Not Proof that H0 Is True
=====================================================================

THE RECIPE
----------
Start from ht_foundations_02_type_i_rate.py, then introduce:
    1. simulate_power()         10000 samples at mu = 53 (H1 is true)
    2. one_nonrejection()       a seed-42 sample at mu = 51 that does not reject
    3. save_figure()            power at mu = 53 versus one non-rejection

Context:
--------
Limit: power at mu = 53 is less than 1, and a nearby alternative mu = 51
can easily fail to reject. Not rejecting H0 is not proof that mu = 50.
A Type II error happens when H0 is false, but we fail to reject it. Statistical
power is our ability to correctly reject a false H0.

How to read this file:
----------------------
In Python terms, imagine our test is a function `detect_anomaly()` that
returns True if it thinks the system shifted. If `detect_anomaly()` returns
False, it DOES NOT PROVE the system is normal (mu = 50). It might just mean
the shift was too small to reliably detect given our sample size.
This script simulates a true shift to mu = 53 and mu = 51. You will see that
even when the system has definitely changed (H0 is false), our test doesn't
catch it 100% of the time. This "miss rate" is the Type II error rate.

Run it:
-------
    uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_03_type_ii_not_proof.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# Set the matplotlib backend for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Simulation parameters and constants
SEED = 42           # Random seed for replicability
N = 36              # Sample size per simulation
MU0 = 50.0          # The assumed null hypothesis mean
MU_ALT = 53.0       # A true alternative mean (system has shifted)
MU_NEAR = 51.0      # A small shift in mean, very hard to detect
SIGMA = 8.0         # The known standard deviation
ALPHA = 0.05        # Significance level
N_REPS = 10_000     # Number of simulation passes

# Setup output directory
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def rejection_cutoff() -> dict[str, float]:
    """
    Return SE and the xbar cutoff under H0.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, float]
        Contains standard error (se) and sample mean cutoff (xbar_crit).
    """
    # Calculate SE and the z-critical value for right-tailed test
    se = SIGMA / np.sqrt(N)
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))
    return {
        "se": float(se),
        "xbar_crit": float(MU0 + z_crit * se),
    }


# --- NEW (1) simulate_power() ------------------------------------------------
def simulate_power(xbar_crit: float, n_reps: int = N_REPS) -> dict[str, float]:
    """
    Power at mu = 53: share of samples that reject H0 when H1 is true.

    Parameters
    ----------
    xbar_crit : float
        The sample mean cutoff above which we reject H0.
    n_reps : int, optional
        Number of simulated samples. Defaults to N_REPS.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - mu_alt: The true population mean used for simulation.
        - power: The proportion of correct rejections (1 - Type II error rate).
        - type_ii: The proportion of missed detections (Type II error rate).

    Notes
    -----
    Statistical power is the probability of correctly rejecting a false null.
    Here, H0 (mu=50) is false because the true mean is MU_ALT (53).
    """
    # Initialize RNG
    rng = np.random.default_rng(SEED)

    # Simulate samples from the ALTERNATIVE distribution (mu = 53)
    samples = rng.normal(MU_ALT, SIGMA, size=(n_reps, N))
    xbars = np.mean(samples, axis=1)

    # Power is the fraction of times we correctly reject H0
    power = float(np.mean(xbars >= xbar_crit))

    # Type II error is failing to reject when we should have
    type_ii = 1.0 - power

    return {
        "mu_alt": MU_ALT,
        "power": power,
        "type_ii": type_ii,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) one_nonrejection() ----------------------------------------------
def one_nonrejection(xbar_crit: float) -> dict[str, float]:
    """
    One nearby alternative sample that fails to reject H0.

    Parameters
    ----------
    xbar_crit : float
        The sample mean cutoff threshold.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - mu_near: The nearby true mean.
        - xbar: The mean of the single drawn sample.
        - xbar_crit: The threshold used.
        - rejected: 1.0 if rejected, 0.0 if failed to reject.

    Notes
    -----
    This demonstrates that even when the null hypothesis is false
    (true mean is 51, not 50), a single sample can easily fail to
    provide enough evidence to reject H0.
    """
    rng = np.random.default_rng(SEED)

    # Draw exactly one sample from a slightly shifted distribution (mu = 51)
    sample = rng.normal(MU_NEAR, SIGMA, size=N)
    xbar = float(np.mean(sample))

    return {
        "mu_near": MU_NEAR,
        "xbar": xbar,
        "xbar_crit": xbar_crit,
        "rejected": float(xbar >= xbar_crit),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    power: dict[str, float],
    nearby: dict[str, float],
) -> Path:
    """
    Bar chart of power at mu = 53 and a nearby non-rejection flag.

    Parameters
    ----------
    power : dict[str, float]
        Output dictionary from simulate_power().
    nearby : dict[str, float]
        Output dictionary from one_nonrejection().

    Returns
    -------
    Path
        Absolute path to the saved bar chart PNG.

    Notes
    -----
    Visualizes the relationship between Statistical Power and Type II Error.
    They must sum to 1.0. Also annotates the graph with our single
    failed rejection at mu=51 to emphasize the core lesson.
    """
    output_path = DIR_FIGURES / "ht_foundations_03_type_ii_not_proof.png"

    labels = ["Power at mu = 53", "Type II at mu = 53"]
    values = [power["power"], power["type_ii"]]
    colors = ["#1A2E51", "#EC2661"]

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)

    # Formatting
    ax.set_ylabel("Rate")
    ax.set_title("Failing to Reject H0 Is Not Proof that H0 Is True")
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Add text labels on top of the bars
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )

    # Annotate with the specific mu=51 failure example
    ax.text(
        0.5,
        1.05,
        f"Nearby mu=51 sample: xbar={nearby['xbar']:.2f} "
        f"(cutoff {nearby['xbar_crit']:.2f}); reject={bool(nearby['rejected'])}",
        ha="center",
        fontsize=8,
        color="#1A2E51",
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Establish the cutoff assuming H0 (mu=50) is true
    cutoff = rejection_cutoff()

    # 2. Simulate test performance if true mean is actually 53
    power = simulate_power(cutoff["xbar_crit"])

    # 3. Observe a single sample if true mean is 51
    nearby = one_nonrejection(cutoff["xbar_crit"])

    # 4. Save results to a figure
    figure_path = save_figure(power, nearby)

    print("================================================================")
    print("LESSON 33 - STEP 3: TYPE II AND NON-PROOF")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS}")
    print(f"xbar cutoff                     : {cutoff['xbar_crit']:.6f}")
    print(f"Alternative mu                  : {power['mu_alt']:.6f}")
    print(f"Power at mu=53                  : {power['power']:.6f}")
    print(f"Type II rate at mu=53           : {power['type_ii']:.6f}")
    print(f"Nearby alternative mu           : {nearby['mu_near']:.6f}")
    print(f"Nearby sample xbar              : {nearby['xbar']:.6f}")
    print(f"Nearby sample rejects H0        : {bool(nearby['rejected'])}")
    print("Limit                          : failing to reject H0 is not proof")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

