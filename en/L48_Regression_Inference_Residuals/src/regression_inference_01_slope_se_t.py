"""
Lesson 48 - Step 1: Slope Standard Error and t Test
===================================================
THE RECIPE
NEW IN THIS STEP: build_overtime_sample(), slope_inference(), and
save_figure().

Context:
A fully synthetic mail-center sample records 40 weeks of overtime hours (x)
and units completed (y). Thirty-nine ordinary weeks are a weak cloud. One
emergency weekend sits at (48, 42). This step estimates the slope, its
standard error, and performs a t test of H0: beta1 = 0 using all 40 weeks.
Statistically, the slope's standard error (SE) tells us how much the slope
would vary from sample to sample. The t statistic is the ratio of the estimated
slope to its SE, and the p-value helps us decide if the true population slope
is significantly different from zero.

How to read this file:
For a student familiar with Python OOP, consider `stats.linregress` as a
procedural factory that returns multiple attributes of the fitted line. Pay
attention to the `# --- NEW (N) ... ---` bands, which introduce the core logic
for sampling, computing inference metrics, and plotting.

Run it:
    uv run en/L48_Regression_Inference_Residuals/src/regression_inference_01_slope_se_t.py
"""

from pathlib import Path

# Standard data science and plotting imports
import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

# Use the 'Agg' backend to save plots without requiring a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reproducibility seed to generate the exact same synthetic data every time
SEED = 42

# Define constants for the dataset structure
N_ORDINARY = 39
OUTLIER_X = 48.0
OUTLIER_Y = 42.0

# Ensure the output directory for figures exists
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_overtime_sample() -----------------------------------------
def build_overtime_sample(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 39 ordinary weeks plus one emergency weekend.

    Parameters
    ----------
    seed : int, default SEED
        The seed used to initialize the numpy random number generator.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns 'week_id', 'overtime_hours',
        'units_completed', and 'emergency_weekend'.

    Notes
    -----
    The synthetic generation uses a weak linear relationship with normal noise
    for the 39 weeks and explicitly appends an outlier for the emergency week.
    """
    rng = np.random.default_rng(seed)

    # Generate random overtime hours and units with some noise
    overtime = rng.uniform(6.0, 22.0, N_ORDINARY)
    units = 18.0 + 0.04 * overtime + rng.normal(0.0, 3.2, N_ORDINARY)

    # Append the predetermined outlier (emergency weekend)
    x = np.append(overtime, OUTLIER_X)
    y = np.append(units, OUTLIER_Y)

    # Build and return the sample data frame
    return pd.DataFrame(
        {
            "week_id": np.arange(1, x.size + 1),
            "overtime_hours": x,
            "units_completed": y,
            "emergency_weekend": np.append(
                np.zeros(N_ORDINARY, dtype=bool), True
            ),
        }
    )
# ------------------------------------------------------------------------------


# --- NEW (2) slope_inference() -----------------------------------------------
def slope_inference(sample: pd.DataFrame) -> dict[str, float]:
    """
    Estimate slope, SE, t statistic, and two-sided p-value.

    Parameters
    ----------
    sample : pd.DataFrame
        The dataset containing 'overtime_hours' (x) and 'units_completed' (y).

    Returns
    -------
    dict[str, float]
        A dictionary containing inference metrics including the slope, intercept,
        standard error (se_slope), t_stat, p_value, degrees of freedom (df),
        critical t value (t_crit), R-squared (r_squared), and hypothesis
        rejection boolean (reject).

    Notes
    -----
    The degrees of freedom (df) is calculated as n - 2 for simple linear
    regression because we estimate two parameters (slope and intercept).
    """
    # Extract independent (x) and dependent (y) variables
    x = sample["overtime_hours"].to_numpy()
    y = sample["units_completed"].to_numpy()

    # Perform linear regression to get slope, intercept, and inference metrics
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Degrees of freedom for n points in a simple linear regression
    df = x.size - 2

    # Calculate the t-statistic for the slope
    t_stat = slope / std_err

    # Retrieve the critical t-value for a 95% confidence level (two-tailed)
    t_crit = float(stats.t.ppf(0.975, df))

    return {
        "n": float(x.size),
        "slope": float(slope),
        "intercept": float(intercept),
        "se_slope": float(std_err),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "df": float(df),
        "t_crit": t_crit,
        "r_squared": float(r_value) ** 2,
        "reject": abs(t_stat) > t_crit,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: pd.DataFrame, inf: dict[str, float]) -> Path:
    """
    Save the 40-week scatter with the fitted line, outlier highlighted.

    Parameters
    ----------
    sample : pd.DataFrame
        The data sample containing ordinary and emergency week points.
    inf : dict[str, float]
        The dictionary returned by `slope_inference` with fitted parameters.

    Returns
    -------
    Path
        The absolute path where the generated PNG figure was saved.

    Notes
    -----
    The scatter plot uses matplotlib's `zorder` to ensure the emergency
    weekend marker is drawn on top of the ordinary points.
    """
    # Define output destination
    output_path = DIR_FIGURES / "regression_inference_01_slope_se_t.png"

    # Separate ordinary points from the emergency outlier for different styling
    ordinary = sample.loc[~sample["emergency_weekend"]]
    emergency = sample.loc[sample["emergency_weekend"]]

    # Generate x values covering the full range to draw the fitted line
    x_line = np.linspace(
        float(sample["overtime_hours"].min()),
        float(sample["overtime_hours"].max()),
        50,
    )

    # Calculate y values for the fitted line using intercept and slope
    y_line = inf["intercept"] + inf["slope"] * x_line

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot ordinary weeks
    ax.scatter(
        ordinary["overtime_hours"],
        ordinary["units_completed"],
        color="#1A2E51",
        s=42,
        label="Ordinary weeks",
    )

    # Plot the emergency weekend with distinct styling and higher zorder
    ax.scatter(
        emergency["overtime_hours"],
        emergency["units_completed"],
        color="#EC2661",
        s=70,
        zorder=3,
        label="Emergency weekend",
    )

    # Plot the regression line
    ax.plot(x_line, y_line, color="#5B8DEF", linewidth=2.2, label="Fitted line")

    # Configure axes, title, legend, and grid
    ax.set_xlabel("Overtime hours")
    ax.set_ylabel("Units completed")
    ax.set_title(
        f"Slope t = {inf['t_stat']:.2f}, p = {inf['p_value']:.2e} (n = 40)"
    )
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)

    # Clean layout and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Build the sample dataset
    sample = build_overtime_sample()

    # 2. Compute regression inference metrics
    inf = slope_inference(sample)

    # 3. Create and save the figure based on the fitted metrics
    figure_path = save_figure(sample, inf)

    # Output results to standard output
    print("================================================================")
    print("LESSON 48 - STEP 1: SLOPE SE AND t")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Weeks including emergency       : {int(inf['n'])}")
    print(f"Slope                           : {inf['slope']:.6f}")
    print(f"Intercept                       : {inf['intercept']:.6f}")
    print(f"SE of slope                     : {inf['se_slope']:.6f}")
    print(f"t statistic                     : {inf['t_stat']:.6f}")
    print(f"df                              : {int(inf['df'])}")
    print(f"t critical (two-sided 0.05)     : {inf['t_crit']:.6f}")
    print(f"p-value                         : {inf['p_value']:.6e}")
    print(f"R-squared                       : {inf['r_squared']:.6f}")
    print(f"Reject H0: slope = 0            : {bool(inf['reject'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

