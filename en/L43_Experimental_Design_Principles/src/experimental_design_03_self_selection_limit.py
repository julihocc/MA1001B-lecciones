"""
Lesson 43 - Step 3: Self-Selection Is Not a Treatment
=====================================================
THE RECIPE
Start from experimental_design_02_randomized_outcomes.py, then introduce:
    1. self_selected_assignment()  operators choose a method by experience
    2. observational_contrast()    confounded cycle times versus randomized
    3. save_figure()               randomized means beside self-selected means

Context:
An observational factor is not a randomized treatment. If operators who
already work faster choose the Automated method, the self-selected gap mixes
the effect of the method with the characteristics of who selected it. This is
called confounding or selection bias.

How to read this file:
This file compares a randomized experiment (where we assign the method) to an
observational study (where operators choose based on their experience). It
shows how observational data can lead to misleading conclusions about the true
treatment effect. In OOP terms, we create two parallel sets of attributes on
our stations to compare the resulting states.

Run it:
    uv run en/L43_Experimental_Design_Principles/src/experimental_design_03_self_selection_limit.py
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

# Constants for synthetic data generation
SEED = 42  # Seed for reproducibility
N_UNITS = 36  # Total number of stations
N_PER_GROUP = 12  # Number of stations per group (for randomized)
TREATMENTS = ("Standard", "Guided", "Automated")  # Experimental factor levels
BASE_MEAN = 52.0  # Base cycle time
EFFECTS = {"Standard": 0.0, "Guided": -2.0, "Automated": -7.0}  # True effects

# Different experience slopes simulate that experience matters differently
# depending on whether the assignment was forced or chosen.
RAND_EXPERIENCE_SLOPE = -0.35  # Mild effect of experience in randomized setup
OBS_EXPERIENCE_SLOPE = -1.6   # Stronger effect of experience in observational setup

NOISE_SIGMA = 2.4  # Standard deviation of the random noise
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_both_designs(seed: int = SEED) -> pd.DataFrame:
    """Rebuild randomized and self-selected designs from the same stations.

    Parameters
    ----------
    seed : int, optional
        Random seed for data generation, by default SEED.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing both randomized and self-selected assignments
        and their respective simulated outcomes.

    Notes
    -----
    This function creates two parallel universes for the same stations: one
    where treatments are randomized, and one where treatments are selected
    based on operator experience (a confounder).
    """
    rng = np.random.default_rng(seed)

    # Base covariate: experience
    experience = rng.uniform(1.0, 9.0, N_UNITS)

    # 1. Randomized Design
    randomized = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    rng.shuffle(randomized)
    noise_rand = rng.normal(0.0, NOISE_SIGMA, N_UNITS)

    # Calculate randomized outcomes
    y_rand = (
        BASE_MEAN
        + np.array([EFFECTS[name] for name in randomized])
        + RAND_EXPERIENCE_SLOPE * (experience - experience.mean())
        + noise_rand
    )

    # 2. Observational Design (Self-selection)
    # The most experienced operators choose Automated, the least choose Standard
    tertiles = np.quantile(experience, [1.0 / 3.0, 2.0 / 3.0])
    self_selected = np.where(
        experience <= tertiles[0],
        "Standard",
        np.where(experience <= tertiles[1], "Guided", "Automated"),
    )

    noise_obs = rng.normal(0.0, NOISE_SIGMA, N_UNITS)

    # Calculate observational outcomes
    y_obs = (
        BASE_MEAN
        + np.array([EFFECTS[name] for name in self_selected])
        + OBS_EXPERIENCE_SLOPE * (experience - experience.mean())
        + noise_obs
    )

    # Return both designs side-by-side
    return pd.DataFrame(
        {
            "station_id": np.arange(1, N_UNITS + 1),
            "experience_years": experience,
            "randomized_method": randomized,
            "randomized_cycle_time": y_rand,
            "self_selected_method": self_selected,
            "observational_cycle_time": y_obs,
        }
    )


# --- NEW (1) self_selected_assignment() --------------------------------------
def self_selected_assignment(designs: pd.DataFrame) -> pd.DataFrame:
    """Summarize who chooses each method when experience drives selection.

    Parameters
    ----------
    designs : pd.DataFrame
        The DataFrame containing the self-selected assignments and covariates.

    Returns
    -------
    pd.DataFrame
        A summary DataFrame showing the count and mean experience for each
        self-selected method.

    Notes
    -----
    This highlights the confounding factor: notice how the mean experience
    differs drastically between the chosen methods, unlike in the randomized
    design.
    """
    rows = []
    for name in TREATMENTS:
        # Filter for rows where this method was self-selected
        block = designs.loc[designs["self_selected_method"] == name]
        rows.append(
            {
                "method": name,
                "n": int(len(block)),
                "mean_experience": float(block["experience_years"].mean()),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (2) observational_contrast() ----------------------------------------
def observational_contrast(designs: pd.DataFrame) -> dict[str, float]:
    """Compare Automated-minus-Standard gaps in both designs.

    Parameters
    ----------
    designs : pd.DataFrame
        The DataFrame containing both experimental designs and their outcomes.

    Returns
    -------
    dict[str, float]
        A dictionary containing the gaps (differences) between Automated and
        Standard methods for both outcomes and covariates across both designs.

    Notes
    -----
    This calculates the "estimated treatment effect" (difference in means) for
    both designs. The observational gap will exaggerate the benefit of the
    Automated method because it includes the benefit of having more experienced
    operators.
    """
    def gap(method_col: str, value_col: str) -> float:
        # Helper function to calculate the difference in means between
        # Automated and Standard for a given assignment and outcome column
        auto = designs.loc[designs[method_col] == "Automated", value_col].mean()
        std = designs.loc[designs[method_col] == "Standard", value_col].mean()
        return float(auto - std)

    return {
        "randomized_y_gap": gap("randomized_method", "randomized_cycle_time"),
        "observational_y_gap": gap(
            "self_selected_method", "observational_cycle_time"
        ),
        "randomized_experience_gap": gap(
            "randomized_method", "experience_years"
        ),
        "observational_experience_gap": gap(
            "self_selected_method", "experience_years"
        ),
        "true_automated_effect": EFFECTS["Automated"],
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(designs: pd.DataFrame) -> Path:
    """Contrast randomized means with self-selected observational means.

    Parameters
    ----------
    designs : pd.DataFrame
        The DataFrame containing both experimental designs and their outcomes.

    Returns
    -------
    Path
        The file path where the figure was saved.

    Notes
    -----
    Visually comparing the means side-by-side illustrates how self-selection
    distorts the apparent effect of the treatments.
    """
    output_path = DIR_FIGURES / "experimental_design_03_self_selection_limit.png"

    # Calculate the means for the randomized design
    rand_means = [
        float(
            designs.loc[
                designs["randomized_method"] == name, "randomized_cycle_time"
            ].mean()
        )
        for name in TREATMENTS
    ]

    # Calculate the means for the observational design
    obs_means = [
        float(
            designs.loc[
                designs["self_selected_method"] == name,
                "observational_cycle_time",
            ].mean()
        )
        for name in TREATMENTS
    ]

    # Setup x positions for grouped bar chart
    x = np.arange(len(TREATMENTS))
    width = 0.36

    # Create the figure
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot randomized means
    ax.bar(
        x - width / 2,
        rand_means,
        width=width,
        color="#1A2E51",
        label="Randomized experiment",
    )

    # Plot observational means
    ax.bar(
        x + width / 2,
        obs_means,
        width=width,
        color="#EC2661",
        label="Self-selected groups",
    )

    # Format axes and labels
    ax.set_xticks(x)
    ax.set_xticklabels(TREATMENTS)
    ax.set_ylabel("Mean cycle time (seconds)")
    ax.set_title("An Observational Factor Is Not a Randomized Treatment")
    ax.set_ylim(0, 70)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False)

    # Add text labels above the bars
    for offset, values in ((-width / 2, rand_means), (width / 2, obs_means)):
        for i, value in enumerate(values):
            ax.text(
                x[i] + offset,
                value + 1.2,
                f"{value:.1f}",
                ha="center",
                fontsize=8,
                fontweight="bold",
            )

    # Save the figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Build the dataset with both designs
    designs = build_both_designs()
    # 2. Summarize self-selection
    selection = self_selected_assignment(designs)
    # 3. Compute the contrast (differences in gaps)
    contrast = observational_contrast(designs)
    # 4. Save the comparison figure
    figure_path = save_figure(designs)

    # Print the report
    print("================================================================")
    print("LESSON 43 - STEP 3: SELF-SELECTION LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"True Automated effect           : {contrast['true_automated_effect']:.6f}")

    # Print self-selected summaries
    for _, row in selection.iterrows():
        print(
            f"Self-selected n, experience ({row['method']:<10}): "
            f"{int(row['n']):>2}, {row['mean_experience']:.6f}"
        )

    # Print the computed gaps
    print(
        "Randomized experience gap       : "
        f"{contrast['randomized_experience_gap']:.6f}"
    )
    print(
        "Observational experience gap    : "
        f"{contrast['observational_experience_gap']:.6f}"
    )
    print(
        "Randomized Auto-Standard Y gap  : "
        f"{contrast['randomized_y_gap']:.6f}"
    )
    print(
        "Observational Auto-Standard gap : "
        f"{contrast['observational_y_gap']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

