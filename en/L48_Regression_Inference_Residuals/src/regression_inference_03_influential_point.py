"""
Lesson 48 - Step 3: An Influential Point Can Create a Significant Slope
=======================================================================
THE RECIPE
Start from regression_inference_02_residual_plot.py, then introduce:
    1. fit_with_and_without()  slope inference on n=40 versus n=39
    2. influence_contrast()    the significant slope vanishes when removed
    3. save_figure()           two fitted lines on the same scatter

Context:
This step demonstrates how a single highly influential data point (the
emergency weekend) can completely alter statistical conclusions. An influential
point can pull the regression line so strongly that a non-significant slope
becomes significant. Because the emergency weekend is fundamentally different
from ordinary operations, fitting a single model to all 40 weeks yields a
misleading t-test result that does not represent typical weeks.

How to read this file:
Notice how `_infer` encapsulates the regression logic, allowing us to cleanly
apply it in `fit_with_and_without` to both the full dataset (n=40) and the
reduced dataset (n=39). Look at the `# --- NEW (N) ... ---` bands to see how
we extract, contrast, and visualize the impact of an influential point.

Run it:
    uv run en/L48_Regression_Inference_Residuals/src/regression_inference_03_influential_point.py
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
        A DataFrame identical to previous steps, containing columns 'week_id',
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


def _infer(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """
    Return slope inference for a single (x, y) pair of arrays.

    Parameters
    ----------
    x : np.ndarray
        1D array of independent variable values (e.g. overtime hours).
    y : np.ndarray
        1D array of dependent variable values (e.g. units completed).

    Returns
    -------
    dict[str, float]
        Dictionary of core regression inference metrics: n, slope, intercept,
        se_slope, t_stat, p_value, and r_squared.
    """
    # Run the linear regression on the provided arrays
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Compute the t-statistic for the estimated slope
    t_stat = slope / std_err

    return {
        "n": float(x.size),
        "slope": float(slope),
        "intercept": float(intercept),
        "se_slope": float(std_err),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "r_squared": float(r_value) ** 2,
    }


# --- NEW (1) fit_with_and_without() ------------------------------------------
def fit_with_and_without(sample: pd.DataFrame) -> dict[str, dict[str, float]]:
    """
    Fit the line on all 40 weeks and again after dropping the emergency.

    Parameters
    ----------
    sample : pd.DataFrame
        The full dataset containing all ordinary and emergency weeks.

    Returns
    -------
    dict[str, dict[str, float]]
        A nested dictionary mapping 'with_point' to the regression results for
        n=40, and 'without_point' to the regression results for n=39.

    Notes
    -----
    This dual-fit approach is a standard technique for evaluating the leverage
    and influence of specific observations in a dataset.
    """
    # Fit model on the entire sample (n=40)
    full = _infer(
        sample["overtime_hours"].to_numpy(),
        sample["units_completed"].to_numpy(),
    )

    # Filter out the emergency weekend
    ordinary = sample.loc[~sample["emergency_weekend"]]

    # Fit model on the reduced sample (n=39)
    reduced = _infer(
        ordinary["overtime_hours"].to_numpy(),
        ordinary["units_completed"].to_numpy(),
    )

    return {"with_point": full, "without_point": reduced}
# ------------------------------------------------------------------------------


# --- NEW (2) influence_contrast() --------------------------------------------
def influence_contrast(
    fits: dict[str, dict[str, float]],
) -> dict[str, float]:
    """
    Contrast significance with and without the emergency weekend.

    Parameters
    ----------
    fits : dict[str, dict[str, float]]
        The dictionary of models returned by `fit_with_and_without`.

    Returns
    -------
    dict[str, float]
        A flat dictionary summarizing the change in the slope, p-value, and
        statistical significance (at alpha=0.05) when the outlier is removed.

    Notes
    -----
    This explicitly checks how the single outlier shifts our binary conclusion
    (reject vs. fail to reject H0).
    """
    with_pt = fits["with_point"]
    without = fits["without_point"]

    return {
        "slope_with": with_pt["slope"],
        "p_with": with_pt["p_value"],
        "slope_without": without["slope"],
        "p_without": without["p_value"],
        "significant_with": with_pt["p_value"] < 0.05,
        "significant_without": without["p_value"] < 0.05,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    sample: pd.DataFrame, fits: dict[str, dict[str, float]]
) -> Path:
    """
    Overlay the n=40 and n=39 lines on the same scatter.

    Parameters
    ----------
    sample : pd.DataFrame
        The full dataset.
    fits : dict[str, dict[str, float]]
        The dictionary of regression fits.

    Returns
    -------
    Path
        The absolute path where the generated PNG figure was saved.

    Notes
    -----
    By plotting both lines simultaneously, we visualize exactly how much the
    regression model is pulled by the influential point.
    """
    output_path = DIR_FIGURES / "regression_inference_03_influential_point.png"

    # Separate ordinary observations and the outlier
    ordinary = sample.loc[~sample["emergency_weekend"]]
    emergency = sample.loc[sample["emergency_weekend"]]

    # Generate x values for the regression lines
    x_full = np.linspace(5.0, 50.0, 60)

    # Calculate y values for both the n=40 and n=39 fitted lines
    y_with = (
        fits["with_point"]["intercept"]
        + fits["with_point"]["slope"] * x_full
    )
    y_without = (
        fits["without_point"]["intercept"]
        + fits["without_point"]["slope"] * x_full
    )

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

    # Plot the emergency weekend
    ax.scatter(
        emergency["overtime_hours"],
        emergency["units_completed"],
        color="#EC2661",
        s=70,
        zorder=3,
        label="Emergency weekend",
    )

    # Plot the regression line for the full dataset (n=40)
    ax.plot(
        x_full,
        y_with,
        color="#EC2661",
        linewidth=2.2,
        label="n = 40 line",
    )

    # Plot the regression line for the reduced dataset (n=39)
    ax.plot(
        x_full,
        y_without,
        color="#5B8DEF",
        linewidth=2.2,
        linestyle="--",
        label="n = 39 line",
    )

    # Configure axes, title, legend, and grid
    ax.set_xlabel("Overtime hours")
    ax.set_ylabel("Units completed")
    ax.set_title("An Influential Point Can Create a Significant Slope")
    ax.legend(frameon=False, fontsize=8)
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

    # 2. Fit the linear model with and without the outlier
    fits = fit_with_and_without(sample)

    # 3. Contrast the results to highlight influence
    contrast = influence_contrast(fits)

    # 4. Generate and save the visualization
    figure_path = save_figure(sample, fits)

    with_pt = fits["with_point"]
    without = fits["without_point"]

    # Output results to standard output
    print("================================================================")
    print("LESSON 48 - STEP 3: INFLUENTIAL POINT LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"n with emergency weekend        : {int(with_pt['n'])}")
    print(f"Slope with point                : {with_pt['slope']:.6f}")
    print(f"SE with point                   : {with_pt['se_slope']:.6f}")
    print(f"t with point                    : {with_pt['t_stat']:.6f}")
    print(f"p with point                    : {with_pt['p_value']:.6e}")
    print(f"R-squared with point            : {with_pt['r_squared']:.6f}")
    print(f"n without emergency weekend     : {int(without['n'])}")
    print(f"Slope without point             : {without['slope']:.6f}")
    print(f"SE without point                : {without['se_slope']:.6f}")
    print(f"t without point                 : {without['t_stat']:.6f}")
    print(f"p without point                 : {without['p_value']:.6f}")
    print(f"R-squared without point         : {without['r_squared']:.6f}")
    print(f"Significant at 0.05 with point  : {bool(contrast['significant_with'])}")
    print(
        "Significant at 0.05 without     : "
        f"{bool(contrast['significant_without'])}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

