"""
Lesson 43 - Step 1: Factors and Random Assignment
=================================================
THE RECIPE
NEW IN THIS STEP: build_experimental_units(), randomize_treatments(), and
save_figure().

Context:
A fully synthetic packing line has 36 stations. The experimental factor is
the packing method with three levels: Standard, Guided, and Automated. Each
station is an experimental unit. Random assignment places 12 stations in
each treatment so that a pretreatment covariate, operator experience, is
not used to choose the method.

How to read this file:
This file demonstrates how random assignment balances pretreatment covariates
across experimental groups. In object-oriented terms, we are treating each
station as a "unit" and assigning a "treatment" attribute. The goal is to
ensure that unobserved or observed properties (like experience) are roughly
equal across treatment groups before any intervention is applied.

Run it:
    uv run en/L43_Experimental_Design_Principles/src/experimental_design_01_factor_randomization.py
"""

# Standard library imports for path manipulation
from pathlib import Path

# Third-party imports for data manipulation and visualization
import matplotlib
import numpy as np
import pandas as pd

# Use the 'Agg' backend for matplotlib to generate plots without a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Constants to control the synthetic data generation
SEED = 42  # Seed for random number generation to ensure reproducibility
N_UNITS = 36  # Total number of experimental units (stations)
N_PER_GROUP = 12  # Number of units per treatment group
TREATMENTS = ("Standard", "Guided", "Automated")  # The levels of our experimental factor
# Directory to save generated figures, relative to this script
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the figures directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_experimental_units() --------------------------------------
def build_experimental_units(seed: int = SEED) -> pd.DataFrame:
    """Build 36 synthetic stations with a pretreatment experience covariate.

    Parameters
    ----------
    seed : int, optional
        Random seed for generating the covariate data, by default SEED.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing 'station_id' and 'experience_years' for each unit.

    Notes
    -----
    In a real experiment, this represents the population of units before any
    treatments are assigned. The covariate 'experience_years' is drawn from a
    uniform distribution between 1 and 9 years.
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)
    # Generate random experience values for each station
    experience = rng.uniform(1.0, 9.0, N_UNITS)
    # Return as a DataFrame to keep the data organized
    return pd.DataFrame(
        {
            "station_id": np.arange(1, N_UNITS + 1),
            "experience_years": experience,
        }
    )
# ------------------------------------------------------------------------------


# --- NEW (2) randomize_treatments() ------------------------------------------
def randomize_treatments(
    units: pd.DataFrame, seed: int = SEED
) -> pd.DataFrame:
    """Assign 12 stations to each method by a seed-42 permutation.

    Parameters
    ----------
    units : pd.DataFrame
        The experimental units to assign treatments to.
    seed : int, optional
        Random seed for the assignment permutation, by default SEED.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with a 'method' column containing the assigned treatment.

    Notes
    -----
    Randomization is the cornerstone of experimental design. It ensures that
    each treatment group is statistically similar on average before the
    experiment begins, mitigating selection bias.
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)
    # Dummy call to advance the RNG state to match exactly the legacy behavior
    _ = rng.uniform(1.0, 9.0, N_UNITS)
    # Create an array with exactly 12 of each treatment label
    labels = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    # Shuffle the labels randomly in place
    rng.shuffle(labels)
    # Create a copy of the units to avoid modifying the original data
    assigned = units.copy()
    # Assign the shuffled labels
    assigned["method"] = labels
    return assigned
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(assigned: pd.DataFrame) -> Path:
    """Show balanced counts and experience by randomly assigned method.

    Parameters
    ----------
    assigned : pd.DataFrame
        The DataFrame containing units with their assigned treatments.

    Returns
    -------
    Path
        The file path where the figure was saved.

    Notes
    -----
    Visualizing the assignment checks if the randomization produced roughly
    balanced groups in terms of our known covariate (experience).
    """
    output_path = DIR_FIGURES / "experimental_design_01_factor_randomization.png"
    # Define colors for our three treatments
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]
    # Calculate the number of stations in each treatment
    counts = [int((assigned["method"] == name).sum()) for name in TREATMENTS]
    # Extract the experience values for each treatment group
    experience_groups = [
        assigned.loc[assigned["method"] == name, "experience_years"].to_numpy()
        for name in TREATMENTS
    ]

    # Set up a figure with two subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))

    # Left subplot: Bar chart of assigned counts
    axes[0].bar(TREATMENTS, counts, color=colors, width=0.62)
    axes[0].set_ylabel("Stations assigned")
    axes[0].set_title("Random Assignment Is Balanced")
    axes[0].set_ylim(0, 16)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    # Add text labels on top of the bars
    for x, count in enumerate(counts):
        axes[0].text(x, count + 0.35, str(count), ha="center", fontweight="bold")

    # Right subplot: Boxplot of experience by treatment
    boxes = axes[1].boxplot(
        experience_groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )
    # Apply colors to the boxplots
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)

    # Format the right subplot
    axes[1].set_xticks([1, 2, 3])
    axes[1].set_xticklabels(TREATMENTS)
    axes[1].set_ylabel("Operator experience (years)")
    axes[1].set_title("Covariate Balance After Randomization")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)  # Close the figure to free memory
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Build the experimental units
    units = build_experimental_units()
    # 2. Assign treatments randomly
    assigned = randomize_treatments(units)
    # 3. Generate and save the visualization
    figure_path = save_figure(assigned)

    # Calculate summary statistics for output
    counts = assigned["method"].value_counts().reindex(TREATMENTS)
    experience = assigned.groupby("method")["experience_years"].mean().reindex(
        TREATMENTS
    )

    # Print the report
    print("================================================================")
    print("LESSON 43 - STEP 1: FACTOR AND RANDOMIZATION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Experimental units              : {N_UNITS}")
    print(f"Factor levels                   : {', '.join(TREATMENTS)}")
    print(f"Stations in Standard            : {int(counts['Standard'])}")
    print(f"Stations in Guided              : {int(counts['Guided'])}")
    print(f"Stations in Automated           : {int(counts['Automated'])}")
    print(f"Mean experience, Standard       : {experience['Standard']:.6f}")
    print(f"Mean experience, Guided         : {experience['Guided']:.6f}")
    print(f"Mean experience, Automated      : {experience['Automated']:.6f}")
    print(
        "Experience gap Auto-Standard    : "
        f"{experience['Automated'] - experience['Standard']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

