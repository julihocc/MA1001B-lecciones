"""
Lesson 34 - Step 3: Known Sigma Is Rarely True in Operations Data
=================================================================
THE RECIPE
Start from z_test_mean_02_p_value.py, then introduce:
    1. sample_sigma_estimate()  s from the same n = 40 deliveries
    2. compare_z_with_s()       z using sigma versus z using s
    3. save_figure()            contrast the two p-values

Context:
Limit: operations data almost never come with a known population sigma.
Replacing sigma by s but keeping the z reference distribution is the wrong
test. Lesson 35 replaces z by a t statistic with df = n - 1.

How to read this file:
For a student familiar with Python OOP, consider how substituting an estimated
parameter (the sample standard deviation 's') instead of the true population
parameter ('sigma') introduces more uncertainty. In this script, we calculate
two versions of the test statistic: one correct (using known sigma) and one
flawed (plugging 's' into the Z-formula instead of using a T-test). This
highlights why we must switch to the T-distribution when sigma is unknown.

Run it:
    uv run en/L34_Z_Test_One_Mean/src/z_test_mean_03_known_sigma_limit.py
"""

# Path handling for consistent cross-platform behavior.
from pathlib import Path

# matplotlib.use("Agg") prevents display errors in environments without a GUI.
import matplotlib
import numpy as np
# scipy.stats provides the standard normal distribution for our p-value calculations.
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same constants as previous steps to ensure we analyze the exact same sample.
SEED = 42
N = 40
MU0 = 80.0
MU_TRUE = 82.0
SIGMA = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """
    Draw n iid delivery times. The analyst knows sigma, not mu.

    Parameters
    ----------
    seed : int, optional
        The random seed to guarantee reproducibility.

    Returns
    -------
    np.ndarray
        The generated sample of n delivery times.
    """
    # Create random number generator and draw from normal distribution.
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


# --- NEW (1) sample_sigma_estimate() -----------------------------------------
def sample_sigma_estimate(sample: np.ndarray) -> dict[str, float]:
    """
    Estimate sigma from the sample. This s is not a known parameter.

    Parameters
    ----------
    sample : np.ndarray
        The generated sample data.

    Returns
    -------
    dict[str, float]
        Dictionary containing the sample mean (xbar), sample standard
        deviation (s), and the standard errors calculated using both
        the known sigma and the estimated s.

    Notes
    -----
    ddof=1 specifies Delta Degrees of Freedom. This calculates the sample
    standard deviation using n-1 in the denominator, which provides an
    unbiased estimate of the population standard deviation.
    """
    # Calculate sample mean.
    xbar = float(np.mean(sample))
    # Calculate sample standard deviation (unbiased estimator).
    s = float(np.std(sample, ddof=1))

    return {
        "xbar": xbar,
        "s": s,
        "se_known": SIGMA / np.sqrt(N),
        "se_plug_in": s / np.sqrt(N),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) compare_z_with_s() ----------------------------------------------
def compare_z_with_s(stats_s: dict[str, float]) -> dict[str, float]:
    """
    Keep the z reference curve but swap sigma for s.

    Parameters
    ----------
    stats_s : dict[str, float]
        A dictionary containing the calculated statistics, including both
        standard errors.

    Returns
    -------
    dict[str, float]
        A dictionary containing both calculated Z-statistics (known sigma vs
        estimated s), their respective p-values, and the difference between them.

    Notes
    -----
    Using 's' in the Z-formula and then evaluating it against the standard
    normal distribution (stats.norm.sf) is mathematically invalid because
    's' introduces extra variance. The proper approach (covered in Lesson 35)
    is to use the t-distribution.
    """
    # Calculate the valid Z-statistic using known sigma.
    z_known = (stats_s["xbar"] - MU0) / stats_s["se_known"]
    # Calculate the invalid "Z"-statistic by plugging in the sample s.
    z_plug = (stats_s["xbar"] - MU0) / stats_s["se_plug_in"]

    # Calculate p-values using the standard normal distribution.
    p_known = float(stats.norm.sf(z_known))
    p_plug = float(stats.norm.sf(z_plug))

    return {
        "z_known": float(z_known),
        "z_plug": float(z_plug),
        "p_known": p_known,
        "p_plug": p_plug,
        "p_difference": abs(p_plug - p_known),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """
    Contrast p-values from known-sigma z versus invalid z-with-s.

    Parameters
    ----------
    comparison : dict[str, float]
        Dictionary containing the p-values from the valid and invalid methods.

    Returns
    -------
    Path
        Absolute path to the saved bar chart.

    Notes
    -----
    This visualization clearly demonstrates how simply substituting 's' for
    'sigma' changes the resulting p-value, potentially altering the test's
    conclusion if it crosses the alpha threshold.
    """
    output_path = DIR_FIGURES / "z_test_mean_03_known_sigma_limit.png"

    # Setup data for the bar chart.
    labels = ["Valid z\n(sigma known)", "Invalid z-with-s\n(sigma unknown)"]
    values = [comparison["p_known"], comparison["p_plug"]]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Create bar chart comparing the two p-values.
    bars = ax.bar(labels, values, color=colors, width=0.55)

    # Add a reference line for our significance level alpha.
    ax.axhline(0.05, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label="alpha = 0.05")

    # Set titles and adjust axes for readability.
    ax.set_ylabel("Upper-tail p-value")
    ax.set_title("Known Sigma Is Rarely True in Operations Data")
    ax.set_ylim(0, max(0.12, max(values) + 0.03))
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate each bar with its exact value.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.004,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the same synthetic sample.
    sample = generate_delivery_sample()

    # 2. Compute statistics, both knowing sigma and estimating it (s).
    stats_s = sample_sigma_estimate(sample)

    # 3. Compare the outcomes of the valid vs invalid approach.
    comparison = compare_z_with_s(stats_s)

    # 4. Generate a chart comparing the p-values.
    figure_path = save_figure(comparison)

    # 5. Output the results.
    print("================================================================")
    print("LESSON 34 - STEP 3: KNOWN-SIGMA LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma                     : {SIGMA:.6f}")
    print(f"Sample mean xbar                : {stats_s['xbar']:.6f}")
    print(f"Sample standard deviation s     : {stats_s['s']:.6f}")
    print(f"Valid z (sigma known)           : {comparison['z_known']:.6f}")
    print(f"Valid p-value                   : {comparison['p_known']:.6f}")
    print(f"Invalid z-with-s                : {comparison['z_plug']:.6f}")
    print(f"Invalid p-value                 : {comparison['p_plug']:.6f}")
    print(f"Absolute p-value difference     : {comparison['p_difference']:.6f}")
    print("Limit                          : known sigma is rarely true; use t")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

