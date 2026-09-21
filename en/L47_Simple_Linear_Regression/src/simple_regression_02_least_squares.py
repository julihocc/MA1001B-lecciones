"""
Lesson 47 - Step 2: Least-Squares Slope and Intercept
=====================================================
THE RECIPE
Start from simple_regression_01_scatter.py, then introduce:
    1. least_squares_fit()  slope and intercept from the normal equations
    2. fitted_values()      yhat = b0 + b1 x
    3. save_figure()        scatter with the least-squares line

Context:
The same 40 weeks are rebuilt from seed 42. No earlier lesson script is
imported. The fitted line is the unique line that minimizes the sum of
squared vertical residuals (the ordinary least squares approach). This is
the backbone of simple linear regression, mapping observed x values to
estimated y values through a calculated slope and intercept.

How to read this file:
- Note the addition of `scipy.stats` for library-based regression.
- Look at `least_squares_fit()` to see both manual calculation (using sums
  of squares) and the library approach (`linregress`).
- Understand how `fitted_values()` computes model predictions (yhat) and
  errors (residuals).
- Review `save_figure()` where the line of best fit is plotted over data.

Run it:
    uv run en/L47_Simple_Linear_Regression/src/simple_regression_02_least_squares.py
"""

# Standard library imports for paths
from pathlib import Path

# Data manipulation and statistical computation libraries
import matplotlib
import numpy as np
import pandas as pd
from scipy import stats  # For ordinary least squares function linregress

# Use non-interactive backend
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CONSTANTS ---
# Random seed to lock data generation identical to step 1
SEED = 42
N_WEEKS = 40
TRUE_INTERCEPT = 12.0
TRUE_SLOPE = 0.45
NOISE_SIGMA = 2.4
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_weekly_sample(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild the 40-week synthetic coaching sample from seed 42.

    Parameters
    ----------
    seed : int
        The RNG seed to match the dataset from Step 1.

    Returns
    -------
    pd.DataFrame
        Identical sample of weeks, coaching hours, and units per hour.
    """
    rng = np.random.default_rng(seed)
    coaching_hours = rng.uniform(8.0, 40.0, N_WEEKS)
    units_per_hour = (
        TRUE_INTERCEPT
        + TRUE_SLOPE * coaching_hours
        + rng.normal(0.0, NOISE_SIGMA, N_WEEKS)
    )
    return pd.DataFrame(
        {
            "week_id": np.arange(1, N_WEEKS + 1),
            "coaching_hours": coaching_hours,
            "units_per_hour": units_per_hour,
        }
    )


# --- NEW (1) least_squares_fit() ---------------------------------------------
def least_squares_fit(sample: pd.DataFrame) -> dict[str, float]:
    """
    Estimate intercept and slope by ordinary least squares.

    Parameters
    ----------
    sample : pd.DataFrame
        The weekly data sample.

    Returns
    -------
    dict[str, float]
        Dictionary with both scipy-computed ('slope', 'intercept', 'r_value')
        and manually computed ('manual_slope', 'manual_intercept') statistics.

    Notes
    -----
    OLS finds the line that minimizes the sum of squared errors.
    The manual slope formula is b1 = S_xy / S_xx.
    The manual intercept formula is b0 = y_mean - b1 * x_mean.
    """
    # Extract arrays using pandas OOP syntax `.to_numpy()`
    x = sample["coaching_hours"].to_numpy()
    y = sample["units_per_hour"].to_numpy()

    # 1. Using scipy.stats for a production-ready calculation
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # 2. Manual calculation to demonstrate the underlying math
    # Sum of squares of X
    sxx = float(np.sum((x - x.mean()) ** 2))
    # Sum of products of X and Y
    sxy = float(np.sum((x - x.mean()) * (y - y.mean())))

    # Compute manual slope and intercept
    manual_slope = sxy / sxx
    manual_intercept = float(y.mean() - manual_slope * x.mean())

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "manual_slope": manual_slope,
        "manual_intercept": manual_intercept,
        "r_value": float(r_value),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) fitted_values() -------------------------------------------------
def fitted_values(
    sample: pd.DataFrame, fit: dict[str, float]
) -> pd.DataFrame:
    """
    Attach yhat = b0 + b1 x to the weekly sample.

    Parameters
    ----------
    sample : pd.DataFrame
        The original sample data.
    fit : dict[str, float]
        The dictionary containing 'intercept' and 'slope'.

    Returns
    -------
    pd.DataFrame
        A new DataFrame extending the original sample with 'fitted' (yhat)
        and 'residual' (y - yhat) columns.

    Notes
    -----
    Residuals represent the vertical distance between an observed point
    and the regression line. They capture the error in our prediction.
    """
    # Make a copy to avoid mutating the original pandas object
    out = sample.copy()

    # Calculate fitted values (predictions) using broadcasting
    out["fitted"] = fit["intercept"] + fit["slope"] * out["coaching_hours"]

    # Calculate residuals (observed - predicted)
    out["residual"] = out["units_per_hour"] - out["fitted"]
    return out
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(fitted: pd.DataFrame, fit: dict[str, float]) -> Path:
    """
    Save the scatter with the least-squares line overlaid.

    Parameters
    ----------
    fitted : pd.DataFrame
        The data containing original values and predictions.
    fit : dict[str, float]
        Regression results for drawing the line.

    Returns
    -------
    Path
        Absolute path to the saved figure image.

    Notes
    -----
    Using a continuous line (x_line, y_line) emphasizes that the model
    interpolates across the full continuous domain of X.
    """
    output_path = DIR_FIGURES / "simple_regression_02_least_squares.png"

    # Generate 50 points across the observed x-domain for a smooth line
    x_line = np.linspace(
        float(fitted["coaching_hours"].min()),
        float(fitted["coaching_hours"].max()),
        50,
    )
    # Compute the theoretical y-values for the line
    y_line = fit["intercept"] + fit["slope"] * x_line

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot the original sample points
    ax.scatter(
        fitted["coaching_hours"],
        fitted["units_per_hour"],
        color="#1A2E51",
        s=42,
        alpha=0.9,
        label="Observed weeks",
    )

    # Plot the regression line
    ax.plot(
        x_line,
        y_line,
        color="#EC2661",
        linewidth=2.2,
        label=(
            f"y = {fit['intercept']:.3f} + "
            f"{fit['slope']:.3f} x"
        ),
    )

    # Labels and legend configuration
    ax.set_xlabel("Coaching hours in the week")
    ax.set_ylabel("Units packed per labor hour")
    ax.set_title("Least-Squares Line for the Synthetic Mail Center")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Regenerate identical dataset
    sample = build_weekly_sample()

    # 2. Compute OLS regression
    fit = least_squares_fit(sample)

    # 3. Calculate predictions and residuals
    fitted = fitted_values(sample, fit)

    # 4. Save visualization
    figure_path = save_figure(fitted, fit)

    # Compute the Sum of Squared Errors (SSE)
    sse = float(np.sum(fitted["residual"] ** 2))

    # Output details
    print("================================================================")
    print("LESSON 47 - STEP 2: LEAST SQUARES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Manual slope                    : {fit['manual_slope']:.6f}")
    print(f"scipy slope                     : {fit['slope']:.6f}")
    print(f"Manual intercept                : {fit['manual_intercept']:.6f}")
    print(f"scipy intercept                 : {fit['intercept']:.6f}")
    print(f"True slope                      : {TRUE_SLOPE:.2f}")
    print(f"True intercept                  : {TRUE_INTERCEPT:.2f}")
    print(f"SSE                             : {sse:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

