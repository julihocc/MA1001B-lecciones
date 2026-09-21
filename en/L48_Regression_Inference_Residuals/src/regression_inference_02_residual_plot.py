"""
Lesson 48 - Step 2: Residual Plot for the Fitted Line
=====================================================
THE RECIPE
Start from regression_inference_01_slope_se_t.py, then introduce:
    1. fitted_residuals()   yhat and e = y - yhat for all 40 weeks
    2. residual_summaries() residual mean, SD, and the emergency residual
    3. save_figure()        residual versus fitted, outlier marked

Context:
This step introduces the calculation and visualization of residuals, which are
the differences between observed values (y) and the values predicted by our
model (yhat). A residual plot acts as a visual decision tool. It helps evaluate
whether a linear model is appropriate: if we see a funnel or fan shape (changing
variance), a curve (non-linearity), or extreme outliers, the model's assumptions
might be violated. In our synthetic data, the emergency weekend clearly stands out.

How to read this file:
Notice how `fitted_residuals` uses vectorized pandas and numpy operations to
efficiently compute the predicted values and residuals. For a student with OOP
experience, `fitted_residuals` acts as a transformation function, mutating a
copy of the dataframe to add new columns. Look for the `# --- NEW (N) ... ---`
bands to identify the logic introduced in this step.

Run it:
    uv run en/L48_Regression_Inference_Residuals/src/regression_inference_02_residual_plot.py
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


# Reproducibility seed for synthetic data generation
SEED = 42

# Define dataset constants
N_ORDINARY = 39
OUTLIER_X = 48.0
OUTLIER_Y = 42.0

# Define output directory for figures, ensuring it exists
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_overtime_sample(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild 39 ordinary weeks plus one emergency weekend from seed 42.

    Parameters
    ----------
    seed : int, default SEED
        The seed used to initialize the numpy random number generator.

    Returns
    -------
    pd.DataFrame
        A DataFrame identical to the one in step 1, with columns 'week_id',
        'overtime_hours', 'units_completed', and 'emergency_weekend'.
    """
    rng = np.random.default_rng(seed)

    # Generate random overtime hours and units with noise
    overtime = rng.uniform(6.0, 22.0, N_ORDINARY)
    units = 18.0 + 0.04 * overtime + rng.normal(0.0, 3.2, N_ORDINARY)

    # Append outlier data representing an emergency weekend
    x = np.append(overtime, OUTLIER_X)
    y = np.append(units, OUTLIER_Y)

    # Construct and return the dataset as a DataFrame
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


# --- NEW (1) fitted_residuals() ----------------------------------------------
def fitted_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Attach fitted values and residuals from the 40-week least-squares line.

    Parameters
    ----------
    sample : pd.DataFrame
        The original dataset containing 'overtime_hours' and 'units_completed'.

    Returns
    -------
    pd.DataFrame
        A new DataFrame copied from `sample`, augmented with 'fitted' (yhat)
        and 'residual' (e = y - yhat) columns.

    Notes
    -----
    The residuals represent the vertical distance from each observed point
    to the regression line. Positive residuals mean the model under-predicted,
    and negative residuals mean the model over-predicted.
    """
    # Extract independent (x) and dependent (y) variables
    x = sample["overtime_hours"].to_numpy()
    y = sample["units_completed"].to_numpy()

    # Fit the linear model to get slope and intercept
    slope, intercept, _, _, _ = stats.linregress(x, y)

    # Create a copy to prevent mutation of the original DataFrame
    out = sample.copy()

    # Calculate fitted values (yhat = b0 + b1*x)
    out["fitted"] = intercept + slope * out["overtime_hours"]

    # Calculate residuals (e = y - yhat)
    out["residual"] = out["units_completed"] - out["fitted"]

    return out
# ------------------------------------------------------------------------------


# --- NEW (2) residual_summaries() --------------------------------------------
def residual_summaries(fitted: pd.DataFrame) -> dict[str, float]:
    """
    Summarize residuals and isolate the emergency-weekend residual.

    Parameters
    ----------
    fitted : pd.DataFrame
        The dataset returned by `fitted_residuals`, containing a 'residual' column.

    Returns
    -------
    dict[str, float]
        A dictionary with aggregate metrics: residual_mean, residual_sd,
        emergency_residual, max_abs_residual, and n (sample size).

    Notes
    -----
    In OLS regression with an intercept, the mathematical mean of the residuals
    is always essentially zero. We compute it here to verify this property.
    """
    # Extract the residual column as a numpy array for fast aggregation
    residuals = fitted["residual"].to_numpy()

    # Isolate the specific residual corresponding to the emergency weekend
    emergency = fitted.loc[fitted["emergency_weekend"], "residual"].iloc[0]

    return {
        "residual_mean": float(residuals.mean()),
        "residual_sd": float(residuals.std(ddof=1)),
        "emergency_residual": float(emergency),
        "max_abs_residual": float(np.max(np.abs(residuals))),
        "n": float(len(fitted)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(fitted: pd.DataFrame) -> Path:
    """
    Save residual versus fitted values with the emergency week marked.

    Parameters
    ----------
    fitted : pd.DataFrame
        The DataFrame output from `fitted_residuals` containing 'fitted' and
        'residual' columns, along with the 'emergency_weekend' boolean flag.

    Returns
    -------
    Path
        The absolute path where the generated PNG figure was saved.

    Notes
    -----
    A residual plot with a horizontal line at 0 makes it easy to visually assess
    variance and spot outliers.
    """
    # Define output destination
    output_path = DIR_FIGURES / "regression_inference_02_residual_plot.png"

    # Separate ordinary observations and the outlier for distinct styling
    ordinary = fitted.loc[~fitted["emergency_weekend"]]
    emergency = fitted.loc[fitted["emergency_weekend"]]

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot residuals for ordinary weeks
    ax.scatter(
        ordinary["fitted"],
        ordinary["residual"],
        color="#1A2E51",
        s=42,
        label="Ordinary weeks",
    )

    # Plot the residual for the emergency weekend with distinct style
    ax.scatter(
        emergency["fitted"],
        emergency["residual"],
        color="#EC2661",
        s=70,
        zorder=3,
        label="Emergency weekend",
    )

    # Add a dashed reference line at residual = 0
    ax.axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)

    # Configure axes, title, legend, and grid
    ax.set_xlabel("Fitted units completed")
    ax.set_ylabel("Residual")
    ax.set_title("Residual Plot: One Week Stands Apart")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)

    # Clean layout and save figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Build the sample dataset
    sample = build_overtime_sample()

    # 2. Attach fitted values and residuals
    fitted = fitted_residuals(sample)

    # 3. Compute summaries for the residuals
    summary = residual_summaries(fitted)

    # 4. Generate and save the residual plot
    figure_path = save_figure(fitted)

    # Output results to standard output
    print("================================================================")
    print("LESSON 48 - STEP 2: RESIDUAL PLOT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Weeks                           : {int(summary['n'])}")
    print(f"Residual mean                   : {summary['residual_mean']:.6f}")
    print(f"Residual SD                     : {summary['residual_sd']:.6f}")
    print(f"Emergency-weekend residual      : {summary['emergency_residual']:.6f}")
    print(f"Largest |residual|              : {summary['max_abs_residual']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

