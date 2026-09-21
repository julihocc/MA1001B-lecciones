"""
Lesson 44 - Step 2: SST, SSB, SSE, and Mean Squares
===================================================

THE RECIPE
----------
Start from one_way_anova_01_group_summaries.py, then introduce:
    1. sums_of_squares()   SST, SSB, and SSE from the three samples
    2. mean_squares()      MSB, MSE, and the manual F ratio
    3. save_figure()       visual ANOVA decomposition

Context:
--------
The same 36 cycle times are rebuilt from seed 42. No earlier lesson script is
imported. Between-group variation is compared with within-group variation
before a p-value is read.

For a student familiar with Object-Oriented Programming (OOP) in Python, ANOVA
is like profiling where memory is being consumed in an application. Total memory
used is SST (Sum of Squares Total). We can allocate that memory usage into
"memory used by specific classes" (SSB - Sum of Squares Between) and "memory
used by random instance variations" (SSE - Sum of Squares Error). ANOVA simply
compares the ratio of these partitions to see if the classes have a significant
systematic effect on memory consumption.

How to read this file:
----------------------
1. `sums_of_squares()`: Calculates total, between-group, and within-group sum of squares.
2. `mean_squares()`: Converts sum of squares to mean squares and computes the F statistic.
3. `save_figure()`: Visualizes the SS decomposition.

Run it:
-------
    uv run en/L44_One_Way_ANOVA/src/one_way_anova_02_ss_ms_table.py
"""

# Standard library imports for paths
from pathlib import Path

# Data and plotting imports
import matplotlib
import numpy as np
import pandas as pd

# Use non-interactive backend for matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Global constants for data generation and analysis
SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = N_PER_GROUP * K_GROUPS
TREATMENTS = ("Standard", "Guided", "Automated")
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
SIGMA = 3.2
# Directory to save generated figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild the three synthetic cycle-time samples from seed 42.

    Parameters
    ----------
    seed : int, optional
        Random seed for repeatability.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns "method" and "cycle_time_seconds".
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)
    frames = []

    # Generate data for each group
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)


# --- NEW (1) sums_of_squares() -----------------------------------------------
def sums_of_squares(sample: pd.DataFrame) -> dict[str, float]:
    """
    Decompose total variation into between-group and within-group pieces.

    Parameters
    ----------
    sample : pd.DataFrame
        DataFrame of cycle times containing "method" and "cycle_time_seconds".

    Returns
    -------
    dict[str, float]
        A dictionary containing:
        - "sst": Sum of Squares Total
        - "ssb": Sum of Squares Between (Treatment)
        - "sse": Sum of Squares Error (Residual)
        - "grand_mean": The overall mean

    Notes
    -----
    SST measures the total variance. SSB measures how much variance is explained
    by the group means differing from the grand mean. SSE measures the variance
    of individual observations around their respective group means. In ANOVA,
    SST = SSB + SSE.
    """
    # Extract all values to calculate total metrics
    values = sample["cycle_time_seconds"].to_numpy()
    grand_mean = float(values.mean())

    # Total Sum of Squares (SST): squared differences from the grand mean
    sst = float(np.sum((values - grand_mean) ** 2))

    # Initialize between and within (error) sum of squares
    ssb = 0.0
    sse = 0.0

    # Calculate SSB and SSE iteratively per group
    for name in TREATMENTS:
        # Get values for this specific group
        group = sample.loc[
            sample["method"] == name, "cycle_time_seconds"
        ].to_numpy()
        group_mean = float(group.mean())

        # SSB: n * (group_mean - grand_mean)^2
        ssb += N_PER_GROUP * (group_mean - grand_mean) ** 2

        # SSE: sum of squared differences from the group mean
        sse += float(np.sum((group - group_mean) ** 2))

    return {"sst": sst, "ssb": ssb, "sse": sse, "grand_mean": grand_mean}
# ------------------------------------------------------------------------------


# --- NEW (2) mean_squares() --------------------------------------------------
def mean_squares(squares: dict[str, float]) -> dict[str, float]:
    """
    Convert sums of squares into mean squares and a manual F ratio.

    Parameters
    ----------
    squares : dict[str, float]
        Dictionary of sums of squares from sums_of_squares().

    Returns
    -------
    dict[str, float]
        Dictionary containing degrees of freedom, mean squares, and F statistic.

    Notes
    -----
    Mean Squares are Sum of Squares divided by their respective degrees of
    freedom (df). This 'normalizes' the sums so we can compare them.
    The F-ratio is MSB / MSE. If the ratio is significantly larger than 1,
    the between-group variance is larger than expected by chance.
    """
    # Degrees of freedom between groups: number of groups - 1
    df_between = K_GROUPS - 1
    # Degrees of freedom for error: total observations - number of groups
    df_error = N_TOTAL - K_GROUPS
    # Total degrees of freedom: total observations - 1
    df_total = N_TOTAL - 1

    # Mean Square Between
    msb = squares["ssb"] / df_between
    # Mean Square Error
    mse = squares["sse"] / df_error

    return {
        "df_between": df_between,
        "df_error": df_error,
        "df_total": df_total,
        "msb": msb,
        "mse": mse,
        "f_manual": msb / mse,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(squares: dict[str, float], ms: dict[str, float]) -> Path:
    """
    Save the SST = SSB + SSE decomposition as labeled bars.

    Parameters
    ----------
    squares : dict[str, float]
        Dictionary containing sst, ssb, and sse.
    ms : dict[str, float]
        Dictionary containing mean squares and f_manual.

    Returns
    -------
    Path
        Path to the saved figure.

    Notes
    -----
    This visualizes the fundamental identity of ANOVA: SST = SSB + SSE.
    It graphically demonstrates how much of the total variation is attributed
    to the treatments (SSB) versus random noise (SSE).
    """
    output_path = DIR_FIGURES / "one_way_anova_02_ss_ms_table.png"

    # Prepare data for the bar chart
    labels = ["SSB\n(between)", "SSE\n(within)", "SST\n(total)"]
    values = np.array([squares["ssb"], squares["sse"], squares["sst"]])
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)

    # Add axis labels and title with the manual F statistic
    ax.set_ylabel("Sum of squares")
    ax.set_title(
        f"ANOVA Decomposition: F = MSB/MSE = {ms['f_manual']:.3f}"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Expand y-axis to fit text labels on top of bars
    ymax = float(values.max()) * 1.18
    ax.set_ylim(0, ymax)

    # Annotate bars with their exact values
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03 * ymax,
            f"{value:.2f}",
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
    # 1. Simulate data
    sample = build_cycle_times()
    # 2. Compute Sum of Squares
    squares = sums_of_squares(sample)
    # 3. Compute Mean Squares and F-statistic
    ms = mean_squares(squares)
    # 4. Save visualization
    figure_path = save_figure(squares, ms)

    # Check the fundamental ANOVA identity
    reconstruction = squares["ssb"] + squares["sse"]

    # Output results exactly as expected
    print("================================================================")
    print("LESSON 44 - STEP 2: SS, MS, AND F")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Grand mean                      : {squares['grand_mean']:.6f}")
    print(f"SST                             : {squares['sst']:.6f}")
    print(f"SSB (between / factor)          : {squares['ssb']:.6f}")
    print(f"SSE (within / error)            : {squares['sse']:.6f}")
    print(f"SSB + SSE                       : {reconstruction:.6f}")
    print(f"df between                      : {int(ms['df_between'])}")
    print(f"df error                        : {int(ms['df_error'])}")
    print(f"df total                        : {int(ms['df_total'])}")
    print(f"MSB                             : {ms['msb']:.6f}")
    print(f"MSE                             : {ms['mse']:.6f}")
    print(f"Manual F = MSB/MSE              : {ms['f_manual']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

