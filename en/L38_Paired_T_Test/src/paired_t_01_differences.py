"""
Lesson 38 - Step 1: Paired Differences from Before-After Times
==============================================================

THE RECIPE
----------
1. Generate paired data: `build_pairs()`
2. Compute basic statistical summaries of before, after, and differences: `difference_summaries()`
3. Visualize the paired data points: `save_figure()`

Context:
--------
A fully synthetic packing cell records handle time on the same 25 stations
before and after a layout change. The observational unit is the station, so
the data are 25 paired differences d = before - after, not two independent
samples. This script creates the paired data and computes basic summary statistics,
as well as generating a graph to visualize the change for each station.

How to read this file:
----------------------
If you know Python OOP, think of each station as an object possessing two attributes:
`before` and `after`. Instead of putting all `before` values in one bucket and `after`
values in another (which discards the relationship), we analyze the difference
(`before - after`) as a single derived property of the station.

Run it:
-------
    uv run en/L38_Paired_T_Test/src/paired_t_01_differences.py
(Or from within the src directory:)
    python paired_t_01_differences.py
"""

# pathlib is used for object-oriented filesystem paths
from pathlib import Path

# matplotlib is used for rendering graphs
import matplotlib
# numpy is used for numerical operations and array data structures
import numpy as np

# Force matplotlib to use the non-interactive 'Agg' backend so it doesn't try to open windows
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Constant for reproducibility of random numbers
SEED = 42
# Total number of matched pairs (stations) to simulate
N_PAIRS = 25
# Compute the absolute path for the directory where figures will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists; create it and parent directories if it does not
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_pairs() ---------------------------------------------------
def build_pairs(seed: int = SEED) -> dict[str, np.ndarray]:
    """
    Draw 25 matched before-after handle times in minutes.

    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility, by default SEED.

    Returns
    -------
    dict[str, np.ndarray]
        A dictionary with three keys:
        - "before": 1D array of before times.
        - "after": 1D array of after times.
        - "diff": 1D array of the differences (before - after).

    Notes
    -----
    The 'after' array is constructed by taking the 'before' values, subtracting
    a mean shift of 3.2, and adding some random noise. This ensures a strong
    positive correlation between before and after measurements.
    """
    # Initialize the random number generator using the provided seed
    rng = np.random.default_rng(seed)
    # Generate 'before' times from a normal distribution (mean=55.0, std=8.0)
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    # Generate 'after' times dependent on 'before' times, reducing by 3.2 on average
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    # Return a dictionary grouping the pairs and their calculated differences
    return {"before": before, "after": after, "diff": before - after}
# ------------------------------------------------------------------------------


# --- NEW (2) difference_summaries() ------------------------------------------
def difference_summaries(pairs: dict[str, np.ndarray]) -> dict[str, float]:
    """
    Summarize before, after, and the matched differences.

    Parameters
    ----------
    pairs : dict[str, np.ndarray]
        A dictionary containing "before", "after", and "diff" arrays of equal length.

    Returns
    -------
    dict[str, float]
        A dictionary containing the following summary statistics:
        - "n": number of pairs.
        - "mean_before": mean of before values.
        - "mean_after": mean of after values.
        - "s_before": sample standard deviation of before values.
        - "s_after": sample standard deviation of after values.
        - "mean_diff": mean of differences.
        - "s_diff": sample standard deviation of differences.
        - "corr": Pearson correlation coefficient between before and after values.

    Notes
    -----
    We use `ddof=1` for sample standard deviation (Bessel's correction). The
    correlation coefficient quantifies the linear relationship between paired
    observations.
    """
    # Extract the arrays from the dictionary
    before = pairs["before"]
    after = pairs["after"]
    diff = pairs["diff"]
    # Calculate and store the statistics in a dictionary
    return {
        "n": float(diff.size),
        "mean_before": float(np.mean(before)),
        "mean_after": float(np.mean(after)),
        "s_before": float(np.std(before, ddof=1)),
        "s_after": float(np.std(after, ddof=1)),
        "mean_diff": float(np.mean(diff)),
        "s_diff": float(np.std(diff, ddof=1)),
        "corr": float(np.corrcoef(before, after)[0, 1]),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(pairs: dict[str, np.ndarray]) -> Path:
    """
    Draw matched before-after lines for the 25 stations.

    Parameters
    ----------
    pairs : dict[str, np.ndarray]
        A dictionary containing "before" and "after" numpy arrays of paired data.

    Returns
    -------
    Path
        The absolute path to the saved figure image.

    Notes
    -----
    This slope graph is highly effective for paired data. Each line segment connects
    a specific station's 'before' value to its 'after' value, visually representing
    the direction and magnitude of the change for that individual station.
    """
    # Define the output file path in the figures directory
    output_path = DIR_FIGURES / "paired_t_01_differences.png"
    # Create the figure and axes objects with a specific size
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Define the x-axis coordinates for 'before' (0) and 'after' (1)
    x = np.array([0, 1])

    # Iterate over each paired observation
    for before, after in zip(pairs["before"], pairs["after"]):
        # Color red if the time decreased (improvement), blue otherwise
        color = "#EC2661" if before > after else "#5B8DEF"
        # Plot the line connecting before and after
        ax.plot(x, [before, after], color=color, alpha=0.55, linewidth=1.2)
        # Plot the start and end points as scatter dots
        ax.scatter(x, [before, after], color=color, s=18, zorder=3)

    # Configure the axes ticks, labels, and title
    ax.set_xticks([0, 1], ["Before", "After"])
    ax.set_ylabel("Handle time (minutes)")
    ax.set_title("25 Matched Stations: Before versus After")
    # Add horizontal grid lines
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout to prevent clipping
    fig.tight_layout()
    # Save the figure to disk with high resolution
    fig.savefig(output_path, dpi=170)
    # Close the figure to free up memory
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Generate the dataset
    pairs = build_pairs()
    # Calculate summary statistics for the dataset
    summary = difference_summaries(pairs)
    # Create and save the slope graph visualization
    figure_path = save_figure(pairs)

    # Print a formatted report to the console
    print("================================================================")
    print("LESSON 38 - STEP 1: PAIRED DIFFERENCES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Number of matched pairs         : {int(summary['n'])}")
    print(f"Mean before (minutes)           : {summary['mean_before']:.6f}")
    print(f"Mean after (minutes)            : {summary['mean_after']:.6f}")
    print(f"Sample s before                 : {summary['s_before']:.6f}")
    print(f"Sample s after                  : {summary['s_after']:.6f}")
    print(f"Mean difference d = before-after: {summary['mean_diff']:.6f}")
    print(f"Sample s of differences         : {summary['s_diff']:.6f}")
    print(f"Correlation before with after   : {summary['corr']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

