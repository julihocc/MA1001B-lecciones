"""
Lesson 46 - Step 1: ANOVA Residuals and Normality
=================================================

THE RECIPE
----------
NEW IN THIS STEP: build_cycle_times(), anova_residuals(), and save_figure().

Context:
--------
In Analysis of Variance (ANOVA), we compare the means of different groups to
see if there is a statistically significant difference between them. However,
ANOVA relies on certain mathematical assumptions to be valid. One of these
assumptions is that the residuals (the differences between each observed value
and its group's mean) are normally distributed.

The same synthetic packing experiment has three methods and n=12 stations
each. One-way ANOVA assumes that residuals are approximately normal. This
step forms e_ij = y_ij - ybar_i and inspects their histogram.

How to read this file:
----------------------
1. `build_cycle_times`: Generates the synthetic data for our experiment.
2. `anova_residuals`: Calculates the group means and computes the residuals.
3. `save_figure`: Visualizes the distribution of residuals with a histogram
   and compares it to a theoretical normal curve.
4. `main`: Orchestrates the steps and runs a Shapiro-Wilk test to formally
   test the residuals for normality.

Run it:
-------
    uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_01_residual_normality.py
"""

# Path manipulation for cross-platform file saving
from pathlib import Path

# matplotlib for plotting; setting backend to "Agg" for non-interactive rendering
import matplotlib
import numpy as np
import pandas as pd
# scipy.stats provides statistical functions like the Shapiro-Wilk test (normality)
from scipy import stats

# Ensure plots can be saved in environments without a display (e.g. CI/CD)
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reproducibility seed so that synthetic data is the same every time we run
SEED = 42
# Number of samples (stations) per group
N_PER_GROUP = 12
# Names of the categorical groups we are comparing
TREATMENTS = ("Standard", "Guided", "Automated")
# The true underlying population means for our synthetic data generation
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
# The true population standard deviation (assumed equal for all groups here)
SIGMA = 3.2
# Directory where output figures will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Create the figures directory if it doesn't already exist
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_cycle_times() ---------------------------------------------
def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 12 cycle times for each packing method from seed 42.

    Parameters
    ----------
    seed : int, optional
        The random seed used to initialize the NumPy random generator.
        Defaults to SEED (42).

    Returns
    -------
    pd.DataFrame
        A DataFrame with two columns: "method" (categorical) and
        "cycle_time_seconds" (numeric float).

    Notes
    -----
    This function uses `np.random.default_rng` which is the modern
    recommended approach in NumPy for random number generation.
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)
    frames = []

    # Loop over each treatment method to generate synthetic data
    for name in TREATMENTS:
        # Draw from a normal distribution with the specified true mean and sigma
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )

    # Combine the individual DataFrames into one large table
    return pd.concat(frames, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NEW (2) anova_residuals() -----------------------------------------------
def anova_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Form residuals e = y - group mean for each packing method.

    Parameters
    ----------
    sample : pd.DataFrame
        The input DataFrame containing "method" and "cycle_time_seconds".

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with two new columns:
        - "fitted": The group mean for each observation.
        - "residual": The difference between the actual cycle time and the fitted mean.

    Notes
    -----
    The `.transform("mean")` method returns a Series of the same length as the
    original DataFrame, filling each row with its corresponding group mean.
    """
    # Calculate the mean for each group and broadcast it to all rows in the group
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    out = sample.copy()

    # Add the fitted values (group means)
    out["fitted"] = fitted
    # Calculate residuals: Actual Value - Fitted Mean
    out["residual"] = out["cycle_time_seconds"] - fitted
    return out
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(diagnosed: pd.DataFrame) -> Path:
    """
    Save a residual histogram with a normal reference curve.

    Parameters
    ----------
    diagnosed : pd.DataFrame
        The DataFrame containing a "residual" column to be plotted.

    Returns
    -------
    Path
        The absolute file path where the PNG image was saved.

    Notes
    -----
    Visually inspecting a histogram of residuals helps verify if the normality
    assumption of ANOVA is roughly met. We overlay a theoretical normal
    distribution curve for comparison.
    """
    output_path = DIR_FIGURES / "anova_diagnostics_01_residual_normality.png"

    # Extract the residual values as a 1D NumPy array
    residuals = diagnosed["residual"].to_numpy()

    # Create an x-axis range that slightly extends past the min and max residuals
    x = np.linspace(residuals.min() - 1.0, residuals.max() + 1.0, 200)
    # Generate the theoretical normal density function with mean=0 and sd=residual.std
    density = stats.norm.pdf(x, loc=0.0, scale=float(residuals.std(ddof=1)))

    # Initialize a matplotlib figure
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot a histogram of the actual residuals
    # density=True normalizes the y-axis so it matches the scale of the PDF curve
    ax.hist(
        residuals,
        bins=10,
        color="#5B8DEF",
        edgecolor="white",
        density=True,
        alpha=0.85,
        label="Residuals",
    )
    # Overlay the theoretical normal reference curve
    ax.plot(x, density, color="#EC2661", linewidth=2.2, label="Normal reference")
    # Draw a vertical dashed line at 0 (the expected mean of residuals)
    ax.axvline(0.0, color="#1A2E51", linestyle="--", linewidth=1.2)

    # Add labels and formatting
    ax.set_xlabel("Residual (seconds)")
    ax.set_ylabel("Density")
    ax.set_title("ANOVA Residuals Look Approximately Normal")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    # Save the figure to disk
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the experimental data
    sample = build_cycle_times()

    # 2. Calculate group means and residuals
    diagnosed = anova_residuals(sample)
    residuals = diagnosed["residual"].to_numpy()

    # 3. Perform a formal Shapiro-Wilk test for normality
    # The null hypothesis is that the data was drawn from a normal distribution.
    # A p-value > 0.05 indicates we fail to reject this null hypothesis.
    shapiro = stats.shapiro(residuals)

    # 4. Generate and save the diagnostic plot
    figure_path = save_figure(diagnosed)

    # 5. Print the results directly to the console
    print("================================================================")
    print("LESSON 46 - STEP 1: RESIDUAL NORMALITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Residual count                  : {residuals.size}")
    print(f"Residual mean                   : {float(residuals.mean()):.6f}")
    print(f"Residual SD                     : {float(residuals.std(ddof=1)):.6f}")
    print(f"Shapiro-Wilk W                  : {float(shapiro.statistic):.6f}")
    print(f"Shapiro-Wilk p-value            : {float(shapiro.pvalue):.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

