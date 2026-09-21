"""
Lesson 29 - Step 1: Sample Proportion and Success-Failure Counts
================================================================
NEW IN THIS STEP: first_contact_counts(), sample_proportion(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. first_contact_counts()   n and x (successes) for the sample
    2. sample_proportion()      phat = x/n and the success-failure checks
    3. save_figure()            bar chart of the two categories

Context:
A fully synthetic service register records whether a ticket is resolved on
first contact. In a seed-42 classroom snapshot, x = 27 of n = 150 tickets
are first-contact resolutions. The point estimate is phat = x / n. The
normal approximation later requires checking n phat and n(1-phat).

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lessons 25-28 treated sampling distributions
and confidence intervals for means. This lesson switches the parameter to
a proportion.

    x                        count of successes (first-contact resolutions)
    phat                     sample proportion x/n; the point estimate
    n phat and n(1-phat)     success and failure counts; both must be >= 5
    bar chart                visualizes the categorical data

main() reports n = 150, x = 27, phat = 0.18, and checks the counts. No earlier
lesson script is imported.

Run it:
    uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_01_sample_proportion.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy is imported for consistency, though
# basic arithmetic is used in this step.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# Sample size: total number of tickets in the snapshot.
N = 150
# Observed number of first-contact resolutions (successes).
X_SUCCESS = 27
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) first_contact_counts() ------------------------------------------
def first_contact_counts() -> dict[str, int]:
    """Return the synthetic first-contact snapshot counts.

    Returns
    -------
    dict[str, int]
        n: total tickets.
        successes: number of first-contact resolutions (x).
        failures: number of tickets requiring multiple contacts (n - x).

    Notes
    -----
    The data is categorical (Yes/No), summarized into counts. The success
    count x = 27 is the numerator for the sample proportion.
    """
    return {
        "n": N,
        "successes": X_SUCCESS,
        "failures": N - X_SUCCESS,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) sample_proportion() ---------------------------------------------
def sample_proportion(counts: dict[str, int]) -> dict[str, float]:
    """Compute phat and the two success-failure products used in the check.

    Parameters
    ----------
    counts:
        The dictionary of sample counts from first_contact_counts().

    Returns
    -------
    dict[str, float]
        phat: the sample proportion x / n.
        qhat: the complement 1 - phat.
        n_phat: expected successes under phat (equals x).
        n_qhat: expected failures under phat (equals n - x).

    Notes
    -----
    To use a normal-based confidence interval later, both the number of
    successes (n*phat) and failures (n*(1-phat)) must be at least 5
    (or 10 in some textbooks). Here, 27 and 123 both exceed this threshold.
    """
    phat = counts["successes"] / counts["n"]
    return {
        "phat": phat,
        "qhat": 1.0 - phat,
        "n_phat": counts["n"] * phat,
        "n_qhat": counts["n"] * (1.0 - phat),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(counts: dict[str, int], props: dict[str, float]) -> Path:
    """Save a two-category bar chart of first-contact outcomes.

    Parameters
    ----------
    counts:
        The integer counts of successes and failures.
    props:
        The proportion dictionary, used only to display phat in the title.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window.

    Notes
    -----
    Unlike continuous data that uses a histogram, categorical data is
    visualized with a bar chart. The bars are separated to emphasize
    distinct categories.
    """
    output_path = DIR_FIGURES / "prop_ci_01_sample_proportion.png"
    labels = ["First-contact\nresolution", "Not first\ncontact"]
    values = [counts["successes"], counts["failures"]]
    colors = ["#EC2661", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Number of tickets")
    ax.set_title(f"Sample Proportion phat = {props['phat']:.4f} (n = {N})")
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Add count labels above each bar
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 3,
            str(value),
            ha="center",
            fontweight="bold",
            fontsize=11,
        )

    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 sample proportion report and write the bar chart.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    counts = first_contact_counts()
    props = sample_proportion(counts)
    figure_path = save_figure(counts, props)

    print("================================================================")
    print("LESSON 29 - STEP 1: SAMPLE PROPORTION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {counts['n']}")
    print(f"First-contact resolutions x     : {counts['successes']}")
    print(f"Not first-contact               : {counts['failures']}")
    print(f"Sample proportion phat          : {props['phat']:.6f}")
    print(f"Complement qhat                 : {props['qhat']:.6f}")
    # Expected success and failure counts using the sample proportion
    print(f"n * phat                        : {props['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {props['n_qhat']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

