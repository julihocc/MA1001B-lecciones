"""
Lesson 37 - Step 1: Two Independent Samples and Group Summaries
===============================================================
THE RECIPE
Start from a blank file, then introduce:
    1. build_shift_samples()    independent samples, nA != nB
    2. group_summaries()        n, mean, and sample standard deviation
    3. save_figure()            side-by-side boxplots

Context:
A fully synthetic warehouse records pick times from two independently sampled
shifts: n1 = 30 on Shift A and n2 = 32 on Shift B. Each group has its own
mean and sample standard deviation. The samples are not paired. This script
generates the independent samples and summarizes their basic properties to
compare the shifts conceptually before performing rigorous statistical tests.

How to read this file:
- `build_shift_samples`: Generates the observational data representing pick
  times and years of experience.
- `group_summaries`: Extracts standard summary statistics (mean, variance)
  independently for each group.
- `save_figure`: Visualizes the distributions, making differences apparent.

Run it:
    python two_sample_t_01_group_summaries.py
"""

# pathlib handles filesystem paths in an object-oriented way
from pathlib import Path

# matplotlib is used for creating static, animated, and interactive visualizations
import matplotlib
# numpy provides support for large, multi-dimensional arrays and matrices
import numpy as np

# 'Agg' is a non-interactive backend for matplotlib; used for saving files
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reproducibility seed for synthetic data generation
SEED = 42
# Number of observations sampled from Shift A
N_A = 30
# Number of observations sampled from Shift B
N_B = 32

# Determine the absolute path to the 'figures' directory relative to this script
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists before saving figures
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_shift_samples() -------------------------------------------
def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """
    Draw independent synthetic pick times and years of experience.

    Parameters
    ----------
    seed : int, optional
        Seed for the random number generator (default is SEED).

    Returns
    -------
    dict[str, np.ndarray]
        A dictionary containing the simulated pick times and experience
        levels for Shift A and Shift B as numpy arrays.

    Notes
    -----
    The shifts represent independent operational blocks, meaning there is no
    one-to-one mapping between the rows of Shift A and Shift B. The distributions
    are modeled as Gaussian random variables.
    """
    # Initialize the NumPy random generator with the specified seed
    rng = np.random.default_rng(seed)

    # Generate random normally distributed data for times and experience
    times_a = rng.normal(loc=48.0, scale=6.0, size=N_A)
    times_b = rng.normal(loc=52.5, scale=7.5, size=N_B)
    experience_a = rng.normal(loc=4.5, scale=1.0, size=N_A)
    experience_b = rng.normal(loc=2.0, scale=0.8, size=N_B)

    return {
        "times_a": times_a,
        "times_b": times_b,
        "experience_a": experience_a,
        "experience_b": experience_b,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) group_summaries() -----------------------------------------------
def group_summaries(times_a: np.ndarray, times_b: np.ndarray) -> dict[str, float]:
    """
    Return n, mean, and sample s for each independent shift.

    Parameters
    ----------
    times_a : np.ndarray
        Array containing the pick times for Shift A.
    times_b : np.ndarray
        Array containing the pick times for Shift B.

    Returns
    -------
    dict[str, float]
        A dictionary of the computed summary statistics: counts (n),
        means, sample standard deviations (s), and the mean difference.

    Notes
    -----
    For standard deviation, delta degrees of freedom (ddof) is set to 1
    to provide an unbiased estimator of the population variance (sample s).
    """
    return {
        # .size yields the number of elements in a numpy array
        "n_a": float(times_a.size),
        "n_b": float(times_b.size),

        # Calculate sample means
        "mean_a": float(np.mean(times_a)),
        "mean_b": float(np.mean(times_b)),

        # Calculate sample standard deviations with ddof=1 for unbiased estimation
        "s_a": float(np.std(times_a, ddof=1)),
        "s_b": float(np.std(times_b, ddof=1)),

        # Absolute difference between the independent sample means
        "mean_diff": float(np.mean(times_a) - np.mean(times_b)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(times_a: np.ndarray, times_b: np.ndarray) -> Path:
    """
    Save side-by-side boxplots of the two independent shifts.

    Parameters
    ----------
    times_a : np.ndarray
        Array containing the pick times for Shift A.
    times_b : np.ndarray
        Array containing the pick times for Shift B.

    Returns
    -------
    Path
        The absolute filepath where the plot was saved.

    Notes
    -----
    A boxplot provides a concise visual summary showing the median, interquartile
    range (IQR), and potential outliers of each independent sample distribution.
    """
    output_path = DIR_FIGURES / "two_sample_t_01_group_summaries.png"

    # Initialize matplotlib subplots for fine-grained plotting control
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Create the boxplot with two input arrays representing the independent groups
    box = ax.boxplot(
        [times_a, times_b],
        tick_labels=["Shift A", "Shift B"],
        patch_artist=True,  # Enables setting face color for the boxes
        widths=0.55,
    )

    # Style the graphical elements of the boxplot patches
    colors = ["#5B8DEF", "#EC2661"]
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
        patch.set_edgecolor("#1A2E51")

    # Configure axes labels, title, and grid for clarity
    ax.set_ylabel("Pick time (minutes)")
    ax.set_title("Two Independent Shifts, nA = 30 and nB = 32")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Clean up margins to ensure text elements aren't cut off
    fig.tight_layout()
    # Save the file and close the figure explicitly to manage memory
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Build synthetic data representing two independent shift populations
    samples = build_shift_samples()
    # Extract descriptive statistics from the numerical arrays
    summary = group_summaries(samples["times_a"], samples["times_b"])
    # Visually compare the distributions
    figure_path = save_figure(samples["times_a"], samples["times_b"])

    # Output standard terminal display
    print("================================================================")
    print("LESSON 37 - STEP 1: TWO INDEPENDENT GROUP SUMMARIES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Shift A sample size nA          : {int(summary['n_a'])}")
    print(f"Shift B sample size nB          : {int(summary['n_b'])}")
    print(f"Shift A mean (minutes)          : {summary['mean_a']:.6f}")
    print(f"Shift B mean (minutes)          : {summary['mean_b']:.6f}")
    print(f"Shift A sample s                : {summary['s_a']:.6f}")
    print(f"Shift B sample s                : {summary['s_b']:.6f}")
    print(f"Mean difference A minus B       : {summary['mean_diff']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

