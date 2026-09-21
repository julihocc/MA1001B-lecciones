"""
Lesson 47 - Step 1: Scatter of a Numerical Predictor and Response
=================================================================
THE RECIPE
Start from a blank script, then introduce:
    1. build_weekly_sample()  simulate predictor and response data
    2. describe_scatter()     compute basic descriptive statistics
    3. save_figure()          plot the scatter of the two variables

Context:
A fully synthetic mail-center sample records 40 weeks. The predictor x is
coaching hours that week. The response y is units packed per labor hour.
The true line is y = 12 + 0.45 x plus noise. This step draws the scatter
before any line is fitted. In statistics, this scatter visualization is
essential before any regression analysis to check for linearity, outliers,
and variance patterns.

How to read this file:
- Read the imports and constants first.
- Explore the data generation in `build_weekly_sample()`.
- See how simple metrics are computed in `describe_scatter()`.
- Understand the visualization setup in `save_figure()`.
- The `main()` function orchestrates the script flow.

Run it:
    uv run en/L47_Simple_Linear_Regression/src/simple_regression_01_scatter.py
"""

# Standard library imports for file path manipulations
from pathlib import Path

# Third-party imports for data manipulation, arrays, and plotting
import matplotlib
import numpy as np
import pandas as pd

# Use a non-interactive backend for matplotlib, suitable for scripts
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CONSTANTS ---
# SEED ensures reproducible random numbers so every run yields the exact same data
SEED = 42
# N_WEEKS is our sample size (n = 40)
N_WEEKS = 40
# TRUE_INTERCEPT (beta_0) is the theoretical baseline if coaching hours = 0
TRUE_INTERCEPT = 12.0
# TRUE_SLOPE (beta_1) is the theoretical increase in units for 1 unit of coaching
TRUE_SLOPE = 0.45
# NOISE_SIGMA is the standard deviation of the normally distributed error term (epsilon)
NOISE_SIGMA = 2.4
# Directory for saving generated plots, resolved dynamically based on this file's path
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists before trying to save anything
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_weekly_sample() -------------------------------------------
def build_weekly_sample(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 40 weeks of coaching hours and units packed per labor hour.

    Parameters
    ----------
    seed : int
        The random seed used for reproducibility. Defaults to SEED.

    Returns
    -------
    pd.DataFrame
        A DataFrame with 40 rows and columns: ['week_id', 'coaching_hours',
        'units_per_hour'].

    Notes
    -----
    The underlying true model is: y = 12.0 + 0.45x + epsilon, where epsilon
    follows a normal distribution with mean 0 and standard deviation 2.4.
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)

    # Generate random uniform coaching hours (x) between 8 and 40
    coaching_hours = rng.uniform(8.0, 40.0, N_WEEKS)

    # Generate the response (y) using the linear equation plus Gaussian noise
    units_per_hour = (
        TRUE_INTERCEPT
        + TRUE_SLOPE * coaching_hours
        + rng.normal(0.0, NOISE_SIGMA, N_WEEKS)
    )

    # Wrap everything into a pandas DataFrame for easier OOP-like column manipulation
    return pd.DataFrame(
        {
            "week_id": np.arange(1, N_WEEKS + 1),
            "coaching_hours": coaching_hours,
            "units_per_hour": units_per_hour,
        }
    )
# ------------------------------------------------------------------------------


# --- NEW (2) describe_scatter() ----------------------------------------------
def describe_scatter(sample: pd.DataFrame) -> dict[str, float]:
    """
    Summarize the two numerical variables before fitting a line.

    Parameters
    ----------
    sample : pd.DataFrame
        The weekly data sample containing predictor and response variables.

    Returns
    -------
    dict[str, float]
        A dictionary containing sample size (n), means (x_mean, y_mean),
        range metrics (x_min, x_max), and Pearson correlation (corr).

    Notes
    -----
    In object-oriented pandas, you can access columns like attributes.
    The correlation measures linear association strength, scaling from -1 to 1.
    """
    # Extract the predictor (x) and response (y) series
    x = sample["coaching_hours"]
    y = sample["units_per_hour"]

    # Compute descriptive metrics and cast to native Python floats
    return {
        "n": float(len(sample)),
        "x_mean": float(x.mean()),
        "y_mean": float(y.mean()),
        "x_min": float(x.min()),
        "x_max": float(x.max()),
        # np.corrcoef returns a 2x2 matrix; we take the off-diagonal element
        "corr": float(np.corrcoef(x, y)[0, 1]),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: pd.DataFrame) -> Path:
    """
    Save the unlabeled scatter of units versus coaching hours.

    Parameters
    ----------
    sample : pd.DataFrame
        The generated weekly data.

    Returns
    -------
    Path
        The absolute path where the figure image was saved.

    Notes
    -----
    Plotting before modeling helps verify the relationship looks linear
    and checks for anomalous data points visually.
    """
    output_path = DIR_FIGURES / "simple_regression_01_scatter.png"

    # Create the figure and axes objects using OOP style
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot x against y as a scatter plot with specific aesthetics
    ax.scatter(
        sample["coaching_hours"],
        sample["units_per_hour"],
        color="#1A2E51",
        s=42,
        alpha=0.9,
    )

    # Decorate the axes
    ax.set_xlabel("Coaching hours in the week")
    ax.set_ylabel("Units packed per labor hour")
    ax.set_title("Forty Synthetic Weeks, No Line Fitted Yet")

    # Add a faint grid for readability
    ax.grid(linestyle="--", alpha=0.3)

    # Adjust layout and save using the figure object's methods
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate the synthetic sample
    sample = build_weekly_sample()

    # 2. Compute basic summary metrics
    summary = describe_scatter(sample)

    # 3. Render and save the scatter plot
    figure_path = save_figure(sample)

    # Output the results to the terminal
    print("================================================================")
    print("LESSON 47 - STEP 1: SCATTER")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Weeks                           : {int(summary['n'])}")
    print(f"True intercept                  : {TRUE_INTERCEPT:.2f}")
    print(f"True slope                      : {TRUE_SLOPE:.2f}")
    print(f"Mean coaching hours             : {summary['x_mean']:.6f}")
    print(f"Mean units per hour             : {summary['y_mean']:.6f}")
    print(f"Coaching hours range            : {summary['x_min']:.6f} to {summary['x_max']:.6f}")
    print(f"Sample correlation              : {summary['corr']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

