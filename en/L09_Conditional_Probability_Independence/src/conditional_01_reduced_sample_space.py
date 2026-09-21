"""
Lesson 09 - Step 1: Conditional probability
===========================================
NEW IN THIS STEP: synthetic_orders(), conditional_rates(), and save_evidence().

THE RECIPE
Build the first lesson step in this order:
    1. synthetic_orders()       create and shuffle the 400-order population
    2. conditional_rates()      restrict the denominator to a condition
    3. save_evidence()          compare conditional probabilities visually

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, pandas
DataFrames, NumPy generators, and unattended savefig. Lesson 08 built this
same 400-order routing-by-delivery table and read joint and marginal
probabilities from it. This step shrinks the sample space to a condition
and reads a proportion from the reduced table.

New in this step:
    DataFrame boolean filter  orders[condition] is the reduced sample space
    Series.mean() of 0/1      True/False average equals a probability
    P(A|B) vs P(B|A)          different denominators, different questions
    list * count              repeat a (routing, delivery) pair to a cell total
    rng.permutation + iloc    shuffle rows without changing those counts

main() rebuilds the 400-order table, prints P(Late | Manual),
P(Late | Automated), and P(Manual | Late), and saves the bar chart.

Run it:
    uv run en/L09_Conditional_Probability_Independence/src/conditional_01_reduced_sample_space.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Course-wide seed so the shuffle matches Lesson 08 and later L09 steps.
SEED = 42
# Lesson 01 pathlib: resolve this file, climb to the lesson folder, then figures/.
FIGURE_PATH = Path(__file__).resolve().parents[1] / "figures" / "conditional_01_rates.png"


# --- NEW (1) synthetic_orders() ----------------------------------------------
def synthetic_orders() -> pd.DataFrame:
    """Return a shuffled synthetic table with fixed routing/outcome counts.

    Returns
    -------
    pd.DataFrame
        400 rows, columns routing and delivery. Cell counts are the Lesson 08
        table: Manual-Late 48, Manual-On time 72, Automated-Late 32,
        Automated-On time 248. Only the row order is random (seed 42).

    Notes
    -----
    Repeating each (routing, delivery) pair, then shuffling, gives a
    realistic-looking register without changing the joint distribution.
    Conditional probabilities later depend only on the counts, not on the
    order of the rows.
    """
    # list * n repeats that pair n times so the four cells match the table.
    records = (
        [("Manual review", "Late")] * 48
        + [("Manual review", "On time")] * 72
        + [("Automated", "Late")] * 32
        + [("Automated", "On time")] * 248
    )
    frame = pd.DataFrame(records, columns=["routing", "delivery"])
    rng = np.random.default_rng(SEED)
    # permutation shuffles 0..399; iloc reorders rows; counts stay the same.
    return frame.iloc[rng.permutation(len(frame))].reset_index(drop=True)
# -----------------------------------------------------------------------------


# --- NEW (2) conditional_rates() ---------------------------------------------
def conditional_rates(orders: pd.DataFrame) -> dict[str, float]:
    """Calculate probabilities after restricting the relevant denominator.

    Parameters
    ----------
    orders:
        The 400-row table from synthetic_orders().

    Returns
    -------
    dict[str, float]
        P(Late | Manual) = 48/120 among Manual-review rows,
        P(Late | Automated) = 32/280 among Automated rows,
        P(Manual | Late) = 48/80 among Late rows.

    Notes
    -----
    Boolean subsetting is the reduced sample space: the condition after
    the vertical bar becomes the new denominator. Reversing the condition
    changes the question, so P(Late | Manual) and P(Manual | Late) need
    not agree.
    """
    # Each filter keeps only the rows that satisfy the condition. That
    # smaller table is the sample space for the matching P(· | condition).
    manual = orders[orders["routing"] == "Manual review"]
    automated = orders[orders["routing"] == "Automated"]
    late = orders[orders["delivery"] == "Late"]
    return {
        # (col == value) is a 0/1 Series; .mean() is the proportion, hence
        # the conditional probability on the reduced table.
        "P(Late | Manual)": (manual["delivery"] == "Late").mean(),
        "P(Late | Automated)": (automated["delivery"] == "Late").mean(),
        "P(Manual | Late)": (late["routing"] == "Manual review").mean(),
    }
# -----------------------------------------------------------------------------


# --- NEW (3) save_evidence() -------------------------------------------------
def save_evidence(rates: dict[str, float]) -> None:
    """Save a bar chart of three condition-dependent probabilities.

    Parameters
    ----------
    rates:
        The three conditionals from conditional_rates(), in dict order.

    Returns
    -------
    None
        Side effect: writes the PNG. Unattended savefig/close as in Lesson 01.

    Notes
    -----
    The first two bars share the event Late but not the condition; the
    third reverses the condition. Heights differ because the reference
    groups differ.
    """
    labels = ["Late |\nManual", "Late |\nAutomated", "Manual |\nLate"]
    values = list(rates.values())
    colors = ["#D81B60", "#1E88E5", "#FFC107"]

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.70)
    ax.set_ylabel("Conditional probability")
    ax.set_title("Conditioning changes the reference group")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    """Print the three conditionals and export the Step 1 bar chart."""
    orders = synthetic_orders()
    rates = conditional_rates(orders)
    print("Synthetic order records:", len(orders))
    print(f"P(Late | Manual review): {rates['P(Late | Manual)']:.6f}")
    print(f"P(Late | Automated): {rates['P(Late | Automated)']:.6f}")
    print(f"P(Manual review | Late): {rates['P(Manual | Late)']:.6f}")
    save_evidence(rates)
    print("Figure saved:", FIGURE_PATH)


if __name__ == "__main__":
    main()

