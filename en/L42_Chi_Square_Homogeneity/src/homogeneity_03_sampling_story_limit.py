"""
Lesson 42 - Step 3: Same Statistic, Different Sampling Story
============================================================
THE RECIPE
Start from homogeneity_02_chi_square.py, then introduce:
    1. two_sampling_stories()   homogeneity versus independence designs
    2. shared_statistic()       identical chi2 from the same numbers
    3. save_figure()            contrast the two sampling plans using the shared chi2

Context:
Homogeneity: three independent site samples, row totals fixed by design.
Independence: one sample of 310 tickets later classified by site and channel.
The arithmetic is the same. The question is not.

How to read this file:
We explicitly compare the two contexts using simple string descriptions and a
single diagram. In code, `stats.chi2_contingency` doesn't know whether you
sampled independently across rows (Homogeneity) or sampled a single large bucket
and cross-tabulated it (Independence). The code calculates identical numbers,
but as the data scientist, your interpretation defines the test.

Run it:
    python homogeneity_03_sampling_story_limit.py
"""

from pathlib import Path  # For handling filesystem paths

import matplotlib  # For setting the backend
import numpy as np  # For arrays
from matplotlib.patches import FancyBboxPatch  # For drawing rounded boxes
from scipy import stats  # For the chi-square test

# Use non-interactive backend
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Random seed for reproducibility
SEED = 42
# The exact same observed count matrix used in the previous steps
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
# Path to save figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure directory exists
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) two_sampling_stories() ------------------------------------------
def two_sampling_stories() -> dict[str, str]:
    """Describe the two designs that can produce the same table.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, str]
        A dictionary mapping the test type to its sampling narrative.

    Notes
    -----
    The crucial difference is the experimental design, not the numbers.
    Homogeneity fixes row or column totals in advance. Independence relies
    on a single random sample categorized after the fact.
    """
    return {
        "homogeneity": (
            "Three planned samples. North n=120, Central n=100, South n=90 "
            "were chosen first. Channel is the response."
        ),
        "independence": (
            "One sample of n=310 tickets. Site and channel are two later "
            "classifications of the same tickets."
        ),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) shared_statistic() ----------------------------------------------
def shared_statistic(observed: np.ndarray) -> dict[str, float]:
    """The chi-square number does not encode the sampling story.

    Parameters
    ----------
    observed : np.ndarray
        A 2D array of observed counts.

    Returns
    -------
    dict[str, float]
        Dictionary with test results: "chi2", "p_value", "df", "n", and
        a flag indicating if row totals were fixed.

    Notes
    -----
    The SciPy function `chi2_contingency` is identical for both tests.
    It returns the same test statistic and p-value regardless of the
    sampling story because the expected counts formula is identical.
    """
    chi2, p_value, df, _ = stats.chi2_contingency(observed, correction=False)
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "df": float(df),
        "n": float(observed.sum()),
        "row_totals_fixed_by_design": 1.0,  # Flag specific to the Homogeneity design
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(chi2: float, df: float) -> Path:
    """Diagram of two sampling stories that share one chi-square value.

    Parameters
    ----------
    chi2 : float
        The computed chi-square statistic.
    df : float
        The degrees of freedom for the test.

    Returns
    -------
    Path
        The absolute path to the generated diagram.

    Notes
    -----
    This generates a conceptual diagram rather than a data plot, visually
    separating the experimental designs while showing they converge on
    the same arithmetic result.
    """
    output_path = DIR_FIGURES / "homogeneity_03_sampling_story_limit.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Set arbitrary limits to position our diagram elements
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")  # Hide grid lines and axes
    ax.set_title("Same Chi-Square, Two Different Sampling Stories")

    # Helper function to draw rounded rectangles with text
    def box(x, y, w, h, text, color):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=color,
            edgecolor="#1A2E51",
            linewidth=1.1,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=8.5, color="#1A2E51", wrap=True)

    # Draw Homogeneity box on the left
    box(0.4, 3.4, 4.2, 2.0, "Homogeneity\n3 planned site samples\nRow totals fixed", "#D6E4F0")
    # Draw Independence box on the right
    box(5.4, 3.4, 4.2, 2.0, "Independence\n1 sample of 310 tickets\nSite is a classification", "#F8D5DE")
    # Draw Shared Arithmetic box at the bottom
    box(
        2.4,
        0.5,
        5.2,
        1.8,
        f"Shared arithmetic\nchi2 = {chi2:.6f}, df = {int(df)}\nThe question is not shared",
        "#F4F6F9",
    )

    # Draw arrows from the two sampling stories pointing to the shared math
    ax.annotate("", xy=(5.0, 2.3), xytext=(2.5, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(5.0, 2.3), xytext=(7.5, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Fetch our string descriptions
    stories = two_sampling_stories()

    # 2. Perform the test calculations
    stats_out = shared_statistic(OBSERVED)

    # 3. Create the conceptual diagram
    figure_path = save_figure(stats_out["chi2"], stats_out["df"])

    # Print exact original outputs
    print("================================================================")
    print("LESSON 42 - STEP 3: SAMPLING STORY LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Shared chi-square statistic     : {stats_out['chi2']:.6f}")
    print(f"Shared degrees of freedom       : {int(stats_out['df'])}")
    print(f"Shared p-value                  : {stats_out['p_value']:.6f}")
    print(f"Homogeneity story               : {stories['homogeneity']}")
    print(f"Independence story              : {stories['independence']}")
    print("Do the stories ask the same H0  : no")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

