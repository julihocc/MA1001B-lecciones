"""
Lesson 42 - Step 1: Three Independent Samples, Same Categories
==============================================================
THE RECIPE
Start from scratch, then introduce:
    1. site_counts()     summarize counts from three independent samples
    2. category_shares() convert raw counts into within-site proportions
    3. save_figure()     stacked bar chart of the channel mix

Context:
Three fully synthetic warehouses are sampled independently: North n = 120,
Central n = 100, and South n = 90. Each ticket is classified as phone, chat,
or email. Homogeneity asks whether the three sites share the same mix. The
row totals were fixed by the sampling plan.

How to read this file:
You already know Python classes and dictionaries. We are just using basic
NumPy operations to calculate row and column totals (summing along `axis=1`
and `axis=0`), similar to how we'd aggregate data in standard Python. This
file sets up the *data* (the counts and proportions) before we introduce
the formal statistical test. The focus here is on the sampling design: three
separate samples, each drawn independently.

Run it:
    python homogeneity_01_three_samples.py
"""

from pathlib import Path  # For handling directory and file paths safely

import matplotlib  # For setting the backend
import numpy as np  # For array manipulations and sums

# Use the Agg backend to generate figures without a GUI window
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # For creating the plots


# Random seed for reproducibility, though data is fixed here
SEED = 42
# The three sites that were independently sampled
SITES = ("North", "Central", "South")
# The categorical outcomes for each ticket
CATEGORIES = ("Phone", "Chat", "Email")
# The actual ticket counts observed for each site (rows) and category (cols)
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
# Path to the figures directory relative to this script
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Create the figures directory if it doesn't already exist
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) site_counts() ---------------------------------------------------
def site_counts() -> dict[str, np.ndarray | float]:
    """Return the three independently sampled site-by-channel counts.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, np.ndarray | float]
        A dictionary containing:
        - "observed": The observed count matrix.
        - "row_totals": The sum of counts for each site.
        - "col_totals": The sum of counts for each category.
        - "n": The total number of observations across all samples.

    Notes
    -----
    In a test of homogeneity, row totals are fixed by the sampling design,
    while in a test of independence, only the total `n` is fixed.
    """
    return {
        "observed": OBSERVED.copy(),         # Return a copy to prevent mutation
        "row_totals": OBSERVED.sum(axis=1),  # Sum across columns (channel) for each site
        "col_totals": OBSERVED.sum(axis=0),  # Sum across rows (site) for each channel
        "n": float(OBSERVED.sum()),          # Grand total of tickets
    }
# ------------------------------------------------------------------------------


# --- NEW (2) category_shares() -----------------------------------------------
def category_shares(observed: np.ndarray) -> np.ndarray:
    """Convert each independent sample into within-site category shares.

    Parameters
    ----------
    observed : np.ndarray
        A 2D array of observed counts (sites x categories).

    Returns
    -------
    np.ndarray
        A 2D array of proportions, where each row sums to 1.0.

    Notes
    -----
    This calculates the empirical distribution for each site.
    If the null hypothesis of homogeneity is true, we expect these
    distributions to be similar to each other and to the overall mix.
    """
    # Divide each count by its site's total (row total)
    # keepdims=True ensures the denominator remains a column vector (3, 1)
    # allowing broadcasting against the (3, 3) numerator array.
    return observed / observed.sum(axis=1, keepdims=True)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(shares: np.ndarray) -> Path:
    """Stacked bars of the three independently sampled channel mixes.

    Parameters
    ----------
    shares : np.ndarray
        A 2D array of proportions (sites x categories) representing
        the within-site shares.

    Returns
    -------
    Path
        The absolute path to the generated PNG image.

    Notes
    -----
    Visualizing shares helps assess homogeneity. Large visual disparities
    between the bars suggest the populations do not share the same mix.
    """
    output_path = DIR_FIGURES / "homogeneity_01_three_samples.png"
    # Specific colors for each category (Phone, Chat, Email)
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]

    # Initialize the plot
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Track the bottom edge for the stacked bars
    bottoms = np.zeros(len(SITES))

    # Iterate through categories to stack their shares
    for j, category in enumerate(CATEGORIES):
        ax.bar(
            SITES,
            shares[:, j],
            bottom=bottoms,
            color=colors[j],
            label=category,
            width=0.62,
        )
        # Update the bottom tracker for the next category
        bottoms = bottoms + shares[:, j]

    ax.set_ylabel("Within-site share")
    ax.set_title("Three Independent Samples of Ticket Mix")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust layout to prevent label clipping and save
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Summarize the counts from our independent samples
    counts = site_counts()

    # 2. Calculate the proportion of each category within each site
    shares = category_shares(counts["observed"])

    # 3. Generate and save the visualization
    figure_path = save_figure(shares)

    # Print precisely matching output
    print("================================================================")
    print("LESSON 42 - STEP 1: THREE INDEPENDENT SAMPLES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Sampling plan                   : three independent site samples")
    print(f"North n, counts                 : 120; 60, 40, 20")
    print(f"Central n, counts               : 100; 35, 40, 25")
    print(f"South n, counts                 : 90; 25, 30, 35")
    print(f"Combined n                      : {int(counts['n'])}")
    print(
        "North shares                    : "
        + ", ".join(f"{value:.6f}" for value in shares[0])
    )
    print(
        "Central shares                  : "
        + ", ".join(f"{value:.6f}" for value in shares[1])
    )
    print(
        "South shares                    : "
        + ", ".join(f"{value:.6f}" for value in shares[2])
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

