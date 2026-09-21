"""
Lesson 44 - Step 1: Three-Group Summaries
=========================================

THE RECIPE
----------
NEW IN THIS STEP: build_cycle_times(), group_summaries(), and save_figure().

Context:
--------
A fully synthetic packing experiment assigns 12 stations to each of three
methods: Standard, Guided, and Automated. Cycle time in seconds is the
numerical response. Before any F test, the lesson reads n, means, and sample
standard deviations for the three independent samples.

For a student familiar with Object-Oriented Programming (OOP) in Python, think
of each experimental unit (a packing station) as an instance object. The
"method" is an attribute of the station, and the "cycle_time" is another
attribute (the numerical response we measure). One-Way ANOVA tests whether
grouping these instances by their "method" attribute explains a statistically
significant portion of the variance in their "cycle_time".

How to read this file:
----------------------
1. `build_cycle_times()`: Simulates the data. This creates our 'objects' (rows in pandas).
2. `group_summaries()`: Calculates sample statistics (n, mean, std) per group.
3. `save_figure()`: Generates a boxplot visualization comparing the groups.

Run it:
-------
    uv run en/L44_One_Way_ANOVA/src/one_way_anova_01_group_summaries.py
"""

# Standard library imports for path manipulation
from pathlib import Path

# Third-party imports for plotting and data manipulation
import matplotlib
import numpy as np
import pandas as pd

# Use non-interactive backend for matplotlib (saves images without opening windows)
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Fixed seed for reproducibility
SEED = 42
# Number of observations per group (n)
N_PER_GROUP = 12
# The three levels of our categorical factor
TREATMENTS = ("Standard", "Guided", "Automated")
# True population means for the simulation
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
# True population standard deviation (assumed equal across groups)
SIGMA = 3.2
# Directory to save generated figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_cycle_times() ---------------------------------------------
def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 12 cycle times for each packing method from seed 42.

    Parameters
    ----------
    seed : int, optional
        The random seed used to initialize the NumPy random number generator.
        Default is SEED (42).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the simulated cycle times with columns:
        - "method": Categorical label of the treatment.
        - "cycle_time_seconds": Simulated continuous response variable.

    Notes
    -----
    In ANOVA, we assume that samples are drawn from populations with normal
    distributions. Here we generate exactly that: independent normal samples.
    """
    # Initialize a random number generator for reproducibility
    rng = np.random.default_rng(seed)
    # List to collect DataFrames for each treatment
    frames = []

    # Iterate over each treatment group
    for name in TREATMENTS:
        # Generate random normal data for this group
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        # Append the new dataframe chunk to our list
        frames.append(
            pd.DataFrame(
                {
                    "method": name,
                    "cycle_time_seconds": cycle_time,
                }
            )
        )
    # Concatenate all group DataFrames into a single one
    return pd.concat(frames, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NEW (2) group_summaries() -----------------------------------------------
def group_summaries(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Return n, mean, and sample standard deviation by method.

    Parameters
    ----------
    sample : pd.DataFrame
        The DataFrame containing the experimental data, normally the output of
        build_cycle_times().

    Returns
    -------
    pd.DataFrame
        A DataFrame summarizing the statistics per group. Columns include:
        - "method": The treatment group name.
        - "n": The number of observations in that group.
        - "mean": The sample mean of the group.
        - "std": The sample standard deviation of the group.

    Notes
    -----
    These summary statistics form the basis of ANOVA. We compare the sample
    means ("mean") to each other, considering the variability ("std") and
    sample sizes ("n"). The ddof=1 argument calculates the unbiased sample
    standard deviation.
    """
    # List to accumulate summary dictionaries
    rows = []

    # Calculate statistics for each treatment group
    for name in TREATMENTS:
        # Filter the dataframe for the current method
        values = sample.loc[sample["method"] == name, "cycle_time_seconds"]
        # Compute and store the summary metrics
        rows.append(
            {
                "method": name,
                "n": int(values.size),
                "mean": float(values.mean()),
                "std": float(values.std(ddof=1)),
            }
        )
    # Return as a DataFrame for easy viewing
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: pd.DataFrame, summary: pd.DataFrame) -> Path:
    """
    Save boxplots of cycle time with group means marked.

    Parameters
    ----------
    sample : pd.DataFrame
        The raw dataset containing "method" and "cycle_time_seconds".
    summary : pd.DataFrame
        The summary dataset containing group "mean" values.

    Returns
    -------
    Path
        The absolute path to the saved figure file.

    Notes
    -----
    Boxplots provide a visual overview of the data distribution, highlighting
    the medians, spread (IQR), and potential outliers. By overlaying the
    group means (red dots) and grand mean (dashed line), we visually anticipate
    the ANOVA test, which assesses whether the spread of the group means around
    the grand mean is significant relative to the spread within the groups.
    """
    # Define the output file path
    output_path = DIR_FIGURES / "one_way_anova_01_group_summaries.png"
    # Corporate color palette for the groups
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]

    # Extract data arrays for each group to pass to ax.boxplot()
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    # Extract the pre-calculated group means
    means = summary["mean"].to_numpy()

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Draw the boxplots
    boxes = ax.boxplot(
        groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )

    # Style the boxplot patches (rectangles)
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)

    # Scatter plot for the group means
    ax.scatter([1, 2, 3], means, color="#EC2661", zorder=3, label="Group mean")

    # Draw a horizontal line for the grand mean (overall average)
    ax.axhline(
        float(sample["cycle_time_seconds"].mean()),
        color="#646464",
        linestyle="--",
        linewidth=1.2,
        label="Grand mean",
    )

    # Configure axes, labels, and title
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(TREATMENTS)
    ax.set_ylabel("Cycle time (seconds)")
    ax.set_title("Three Independent Samples of Packing Cycle Time")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False)

    # Finalize layout and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Simulate the data
    sample = build_cycle_times()
    # 2. Calculate summary statistics
    summary = group_summaries(sample)
    # 3. Generate and save the visualization
    figure_path = save_figure(sample, summary)
    # Calculate the grand mean for console output
    grand_mean = float(sample["cycle_time_seconds"].mean())

    # Print the requested console output exactly as required
    print("================================================================")
    print("LESSON 44 - STEP 1: GROUP SUMMARIES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Groups                          : {', '.join(TREATMENTS)}")
    print(f"Stations per method             : {N_PER_GROUP}")
    print(f"Grand mean                      : {grand_mean:.6f}")
    for _, row in summary.iterrows():
        print(
            f"n, mean, s ({row['method']:<10})     : "
            f"{int(row['n'])}, {row['mean']:.6f}, {row['std']:.6f}"
        )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

