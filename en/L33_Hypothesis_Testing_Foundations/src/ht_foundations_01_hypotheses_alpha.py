"""
Lesson 33 - Step 1: Hypotheses, Alpha, and the Rejection Region
===============================================================

THE RECIPE
----------
NEW IN THIS STEP: state_hypotheses(), rejection_cutoff(), and
save_figure().

Context:
--------
A fully synthetic packing target is mu = 50 minutes. The test is
H0: mu = 50 versus H1: mu > 50, with alpha = 0.05. For this foundation
lesson, sigma = 8 is treated as known and n = 36, so the cutoff is a
z critical value.

How to read this file:
----------------------
If you know Python OOP, think of H0 as a base state or default assumption
about our population parameter (mu). We set a "significance level" (alpha),
which acts like an error tolerance threshold for incorrectly rejecting H0.
The `state_hypotheses` function sets up our baseline configuration.
The `rejection_cutoff` function determines the exact value (critical value)
that will trigger an exception (rejection of H0) based on our alpha tolerance.

Run it:
-------
    uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_01_hypotheses_alpha.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# Use the Agg backend for matplotlib, which is ideal for saving files without a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Global constants representing our experimental setup
SEED = 42           # Random seed for reproducibility (used in later steps)
N = 36              # Sample size
MU0 = 50.0          # The population mean under the null hypothesis (H0)
SIGMA = 8.0         # The known population standard deviation
ALPHA = 0.05        # The significance level (Type I error rate tolerance)

# Setup output directory for figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) state_hypotheses() ----------------------------------------------
def state_hypotheses() -> dict[str, float]:
    """
    Return the one-sided mean hypotheses and the known-sigma SE.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - mu0: Null hypothesis mean.
        - n: Sample size.
        - sigma: Population standard deviation.
        - alpha: Significance level.
        - se: Standard error of the mean (sigma / sqrt(n)).

    Notes
    -----
    The standard error (SE) describes the spread of the sampling
    distribution of the sample mean.
    """
    # Calculate the Standard Error (SE) of the mean
    se = SIGMA / np.sqrt(N)

    return {
        "mu0": MU0,
        "n": float(N),
        "sigma": SIGMA,
        "alpha": ALPHA,
        "se": float(se),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) rejection_cutoff() ----------------------------------------------
def rejection_cutoff(se: float) -> dict[str, float]:
    """
    Convert alpha into a z critical value and an xbar cutoff.

    Parameters
    ----------
    se : float
        The standard error of the mean.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - z_crit: The z-score corresponding to the (1 - alpha) percentile.
        - xbar_crit: The sample mean threshold that separates the rejection
                     and non-rejection regions.

    Notes
    -----
    Since this is a right-tailed test (H1: mu > 50), the rejection region
    is entirely in the right tail of the normal distribution.
    """
    # Find the z-score where cumulative probability is (1 - ALPHA)
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))

    # Scale and shift the z-score to our sample mean distribution
    xbar_crit = MU0 + z_crit * se

    return {
        "z_crit": z_crit,
        "xbar_crit": float(xbar_crit),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(se: float, cutoff: dict[str, float]) -> Path:
    """
    Shade the alpha = 0.05 rejection region in the sampling distribution.

    Parameters
    ----------
    se : float
        The standard error of the mean.
    cutoff : dict[str, float]
        Dictionary from rejection_cutoff() containing 'xbar_crit'.

    Returns
    -------
    Path
        The absolute path where the generated figure is saved.

    Notes
    -----
    This visualization helps illustrate where sample means must fall to
    provide enough evidence to reject the null hypothesis.
    """
    output_path = DIR_FIGURES / "ht_foundations_01_hypotheses_alpha.png"

    # Generate x-values for the sampling distribution curve (+/- 4 SEs from mean)
    x = np.linspace(MU0 - 4 * se, MU0 + 4 * se, 400)
    # Calculate Probability Density Function (PDF) values
    y = stats.norm.pdf(x, loc=MU0, scale=se)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)

    # Fill the rejection region (values greater than or equal to xbar_crit)
    ax.fill_between(
        x[x >= cutoff["xbar_crit"]],
        y[x >= cutoff["xbar_crit"]],
        color="#EC2661",
        alpha=0.55,
        label=f"alpha = {ALPHA:.2f} rejection region",
    )

    # Add a vertical line exactly at the cutoff point
    ax.axvline(cutoff["xbar_crit"], color="#EC2661", linewidth=2.0)

    # Formatting
    ax.set_xlabel("Sample mean xbar (minutes)")
    ax.set_ylabel("Density under H0")
    ax.set_title("H0: mu = 50 vs H1: mu > 50, alpha = 0.05")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    # Save and cleanup
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. State the hypotheses and parameters
    setup = state_hypotheses()

    # 2. Determine our rejection thresholds
    cutoff = rejection_cutoff(setup["se"])

    # 3. Visualize the theoretical distribution
    figure_path = save_figure(setup["se"], cutoff)

    print("================================================================")
    print("LESSON 33 - STEP 1: HYPOTHESES AND ALPHA")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("H0                             : mu = 50")
    print("H1                             : mu > 50")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma                     : {SIGMA:.6f}")
    print(f"SE = sigma/sqrt(n)              : {setup['se']:.6f}")
    print(f"Significance level alpha        : {ALPHA:.6f}")
    print(f"z critical                      : {cutoff['z_crit']:.6f}")
    print(f"xbar cutoff                     : {cutoff['xbar_crit']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

