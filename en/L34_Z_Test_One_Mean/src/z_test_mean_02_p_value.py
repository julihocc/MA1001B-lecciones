"""
Lesson 34 - Step 2: P-Value for the One-Sided Z Test
====================================================
THE RECIPE
Start from z_test_mean_01_z_statistic.py, then introduce:
    1. p_value_upper()      p = scipy.stats.norm.sf(z)
    2. test_decision()      compare p with alpha = 0.05
    3. save_figure()        shade the standard-normal tail beyond z

Context:
The same n = 40 synthetic deliveries are rebuilt with SEED = 42. No earlier
lesson script is imported. We are now computing the p-value, which represents
the probability of observing a Z-statistic as extreme as ours, assuming the
null hypothesis is true.

How to read this file:
For a student familiar with Python OOP, you can think of `scipy.stats.norm` as
a class representing the standard normal distribution, and its `.sf()` method
(Survival Function) as returning the area under the curve to the right of a
given z-value. This directly gives us our upper-tail p-value. The functions here
add the decision-making logic based on this p-value and a pre-defined
significance level (alpha).

Run it:
    uv run en/L34_Z_Test_One_Mean/src/z_test_mean_02_p_value.py
"""

# pathlib handles filesystem paths across different operating systems.
from pathlib import Path

# matplotlib.use("Agg") is required to generate plots without a display server.
import matplotlib
import numpy as np
# scipy.stats provides statistical functions and probability distributions.
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Constant parameters for our synthetic data and hypothesis test.
SEED = 42
N = 40
MU0 = 80.0
MU_TRUE = 82.0
SIGMA = 6.0
# ALPHA is our significance level, the threshold for rejecting H0.
ALPHA = 0.05
# Directory setup for output figures.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """
    Draw n iid delivery times. The analyst knows sigma, not mu.

    Parameters
    ----------
    seed : int, optional
        The random seed to use. Defaults to SEED.

    Returns
    -------
    np.ndarray
        Array of generated delivery times.
    """
    # Create the generator and draw samples from a normal distribution.
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


def z_statistic(sample: np.ndarray) -> dict[str, float]:
    """
    Compute xbar, SE, and the z statistic under H0: mu = 80.

    Parameters
    ----------
    sample : np.ndarray
        The sample data.

    Returns
    -------
    dict[str, float]
        Calculated metrics including sample mean, standard error, and Z-statistic.
    """
    # Calculate mean and standard error, then standardize to find Z.
    xbar = float(np.mean(sample))
    se = SIGMA / np.sqrt(N)
    z = (xbar - MU0) / se
    return {"xbar": xbar, "se": float(se), "z": float(z)}


# --- NEW (1) p_value_upper() -------------------------------------------------
def p_value_upper(z: float) -> float:
    """
    Upper-tail p-value P(Z >= z) under the standard normal.

    Parameters
    ----------
    z : float
        The calculated Z-statistic.

    Returns
    -------
    float
        The probability of observing a Z-statistic greater than or equal to z.

    Notes
    -----
    Uses the Survival Function (`sf`), which is equivalent to 1 - CDF.
    It calculates the area under the right tail of the standard normal distribution.
    """
    # stats.norm.sf calculates the survival function (1 - CDF) for the normal distribution.
    return float(stats.norm.sf(z))
# ------------------------------------------------------------------------------


# --- NEW (2) test_decision() -------------------------------------------------
def test_decision(p_value: float, alpha: float = ALPHA) -> dict[str, float]:
    """
    Reject H0 when the p-value is smaller than alpha.

    Parameters
    ----------
    p_value : float
        The calculated p-value from our test statistic.
    alpha : float, optional
        The significance level threshold. Default is ALPHA (0.05).

    Returns
    -------
    dict[str, float]
        A dictionary containing alpha, p_value, and a boolean flag (represented as
        a float for consistency) indicating whether to reject H0.

    Notes
    -----
    If p < alpha, our result is statistically significant, leading us to reject
    the null hypothesis.
    """
    # Determine whether the p-value crosses our significance threshold.
    return {
        "alpha": alpha,
        "p_value": p_value,
        "reject_h0": float(p_value < alpha),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(z: float, p_value: float) -> Path:
    """
    Shade the standard-normal upper tail beyond the observed z.

    Parameters
    ----------
    z : float
        The observed Z-statistic.
    p_value : float
        The calculated p-value.

    Returns
    -------
    Path
        The absolute path to the saved figure.

    Notes
    -----
    Visualizes the standard normal distribution (mean=0, std=1) and highlights
    the region representing the p-value.
    """
    output_path = DIR_FIGURES / "z_test_mean_02_p_value.png"

    # Generate x values covering the main part of the standard normal curve.
    x = np.linspace(-4.0, 4.0, 400)
    # Calculate the Probability Density Function (PDF) for each x.
    y = stats.norm.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Plot the normal curve.
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)

    # Shade the area under the curve to the right of our observed z-statistic.
    ax.fill_between(
        x[x >= z],
        y[x >= z],
        color="#EC2661",
        alpha=0.55,
        label=f"p-value = {p_value:.4f}",
    )

    # Mark the observed z-statistic with a vertical line.
    ax.axvline(z, color="#EC2661", linewidth=2.0)

    # Add titles, labels, and formatting.
    ax.set_xlabel("Standard normal z")
    ax.set_ylabel("Density")
    ax.set_title("Upper-Tail P-Value for the Z Test")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate data and calculate Z-statistic.
    sample = generate_delivery_sample()
    metrics = z_statistic(sample)

    # 2. Calculate the p-value.
    p_value = p_value_upper(metrics["z"])

    # 3. Make a decision based on the p-value.
    decision = test_decision(p_value)

    # 4. Generate the visualization.
    figure_path = save_figure(metrics["z"], p_value)

    # 5. Output results.
    print("================================================================")
    print("LESSON 34 - STEP 2: P-VALUE AND DECISION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample mean xbar (min)          : {metrics['xbar']:.6f}")
    print(f"z statistic                     : {metrics['z']:.6f}")
    print(f"Upper-tail p-value              : {p_value:.6f}")
    print(f"Significance level alpha        : {decision['alpha']:.6f}")
    print(f"Reject H0 at alpha=0.05         : {bool(decision['reject_h0'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

