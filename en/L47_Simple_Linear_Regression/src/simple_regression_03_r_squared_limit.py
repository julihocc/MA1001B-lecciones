"""
Lesson 47 - Step 3: High R-squared Is Not a Causal Lever
========================================================
THE RECIPE
Start from simple_regression_02_least_squares.py, then introduce:
    1. r_squared()          SST, SSR, SSE, and R^2 = 1 - SSE/SST
    2. observational_warning()  the fit is not a randomized treatment effect
    3. save_figure()        R^2 decomposition with a causation warning

Context:
A high R-squared signifies a strong linear association but does not imply a
causal lever. Coaching hours were observed, not randomly assigned.
Weeks that already pack faster may also receive more coaching, so the slope
is not a direct policy button that guarantees production boosts. We decompose
the total sum of squares (SST) into explained (SSR) and unexplained (SSE)
parts to compute the coefficient of determination (R^2).

How to read this file:
- Examine `r_squared()` to see how variance is decomposed: SST = SSR + SSE.
- Notice the explicit `observational_warning()` emphasizing that model metrics
  don't guarantee causal impact.
- The `save_figure()` now generates a bar chart of the variance components
  rather than a scatter plot.

Run it:
    uv run en/L47_Simple_Linear_Regression/src/simple_regression_03_r_squared_limit.py
"""

# Path manipulations
from pathlib import Path

# Scientific and data computing libraries
import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

# Headless plotting
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CONSTANTS ---
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
        Seed for the random number generator. Defaults to SEED.

    Returns
    -------
    pd.DataFrame
        DataFrame with the identical sample dataset as previous steps.
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


# --- NEW (1) r_squared() -----------------------------------------------------
def r_squared(sample: pd.DataFrame) -> dict[str, float]:
    """
    Decompose total variation and form R^2 = 1 - SSE/SST.

    Parameters
    ----------
    sample : pd.DataFrame
        The weekly observation dataset.

    Returns
    -------
    dict[str, float]
        Dictionary holding regression coefficients, sum of squares components
        (SST, SSR, SSE), and R-squared calculations.

    Notes
    -----
    - SST (Total Sum of Squares): Total variance in Y.
    - SSE (Sum of Squared Errors): Unexplained variance (residuals).
    - SSR (Sum of Squares due to Regression): Variance explained by the model.
    - R^2 (Coefficient of Determination) equals the fraction of total variance
      explained by the predictor X.
    """
    x = sample["coaching_hours"].to_numpy()
    y = sample["units_per_hour"].to_numpy()

    # Compute the OLS fit
    slope, intercept, r_value, _, _ = stats.linregress(x, y)

    # Generate model predictions and calculate error arrays
    fitted = intercept + slope * x
    residual = y - fitted

    # SST: Total deviation of y from its mean
    sst = float(np.sum((y - y.mean()) ** 2))

    # SSE: Deviation of y from the regression line
    sse = float(np.sum(residual ** 2))

    # SSR: Deviation of regression line from the mean
    ssr = float(np.sum((fitted - y.mean()) ** 2))

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "sst": sst,
        "ssr": ssr,
        "sse": sse,
        "r_squared": 1.0 - sse / sst,
        "r_value_squared": float(r_value) ** 2,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) observational_warning() -----------------------------------------
def observational_warning(fit: dict[str, float]) -> dict[str, float]:
    """
    Quantify a 10-hour coaching increase as a fitted, not causal, change.

    Parameters
    ----------
    fit : dict[str, float]
        The dictionary containing regression results, primarily 'slope'.

    Returns
    -------
    dict[str, float]
        A warning payload indicating expected gain without causal guarantee.

    Notes
    -----
    A simple regression slope reflects correlation in historical data.
    Without random assignment or a controlled experiment, changing X
    arbitrarily does not guarantee Y will shift by (slope * deltaX).
    """
    return {
        "fitted_gain_10h": 10.0 * fit["slope"],
        "r_squared": fit["r_squared"],
        "randomized": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(fit: dict[str, float]) -> Path:
    """
    Save the SST = SSR + SSE decomposition and the R^2 warning.

    Parameters
    ----------
    fit : dict[str, float]
        The regression results with SSR, SSE, SST, and R^2 values.

    Returns
    -------
    Path
        Absolute path to the resulting bar chart image.

    Notes
    -----
    This plot visually verifies that SSR + SSE = SST. Bar charts here
    help contrast the explained vs unexplained magnitudes.
    """
    output_path = DIR_FIGURES / "simple_regression_03_r_squared_limit.png"

    # Define categorical labels and their corresponding scalar values
    labels = ["SSR\n(model)", "SSE\n(residual)", "SST\n(total)"]
    values = np.array([fit["ssr"], fit["sse"], fit["sst"]])
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Create the bar plot
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Sum of squares")

    # Inject an explicit caveat into the plot title
    ax.set_title(
        f"R^2 = {fit['r_squared']:.3f} Is Not a Causal Lever"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Expand upper y-limit for label visibility
    ymax = float(values.max()) * 1.18
    ax.set_ylim(0, ymax)

    # Annotate each bar with its exact value
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03 * ymax,
            f"{value:.1f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Generate identical data again
    sample = build_weekly_sample()

    # 2. Decompose variance and compute R^2
    fit = r_squared(sample)

    # 3. Generate causal caveats
    warning = observational_warning(fit)

    # 4. Render the decomposition graphic
    figure_path = save_figure(fit)

    # Output detailed findings
    print("================================================================")
    print("LESSON 47 - STEP 3: R-SQUARED LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"SST                             : {fit['sst']:.6f}")
    print(f"SSR                             : {fit['ssr']:.6f}")
    print(f"SSE                             : {fit['sse']:.6f}")
    print(f"SSR + SSE                       : {fit['ssr'] + fit['sse']:.6f}")
    print(f"R-squared                       : {fit['r_squared']:.6f}")
    print(f"r squared check                 : {fit['r_value_squared']:.6f}")
    print(f"Fitted gain for +10 hours       : {warning['fitted_gain_10h']:.6f}")
    print("Causal lever?                   : No; coaching was not randomized")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

