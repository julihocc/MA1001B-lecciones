"""
Lesson 09 - Step 3: Dependence without replacement
==================================================
NEW IN THIS STEP: exact_sequence_probability(), simulate_sequences(), and
save_evidence().

THE RECIPE
Start from conditional_02_independence_tests.py, then introduce:
    1. exact_sequence_probability()  update the second-draw denominator
    2. simulate_sequences()          verify the result with seed 42
    3. save_evidence()               expose the naive-independence error

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy
generators, and unattended savefig. Steps 1-2 tested independence on a
fixed 400-order table. This step leaves that table and draws two orders
from a 10-order inspection batch without replacement, so the first draw
changes the second probability.

New in this step:
    sequential product      P(both) = P(first) P(second | first)
    without replacement     4/10, then 3/9; numerator and denominator both drop
    naive independence      (4/10)^2 pretends the batch never shrinks
    skip-the-drawn-index    map a 0..8 draw onto the nine labels that remain
    Monte Carlo mean        0/1 both-flagged indicator, averaged over trials

main() prints the exact product 4/10 * 3/9, the naive square 0.16, and a
seed-42 simulation of 500,000 ordered pairs, then saves the three bars.

Run it:
    uv run en/L09_Conditional_Probability_Independence/src/conditional_03_without_replacement_limit.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SEED = 42
# Large enough that the simulated proportion sits near the exact 2/15.
SIMULATIONS = 500_000
# Lesson 01 pathlib: figures/ next to this package, not the shell's cwd.
FIGURE_PATH = Path(__file__).resolve().parents[1] / "figures" / "conditional_03_sequence.png"


# --- NEW (1) exact_sequence_probability() ------------------------------------
def exact_sequence_probability() -> tuple[float, float, float]:
    """Return first, conditional second, and both-flagged probabilities.

    Returns
    -------
    tuple[float, float, float]
        P(first flagged) = 4/10,
        P(second flagged | first flagged) = 3/9,
        P(both flagged) = (4/10)*(3/9) = 2/15.

    Notes
    -----
    Two orders are drawn without replacement from a batch of 10 that
    contains 4 flagged orders. After a flagged first draw, 3 flagged
    orders remain among 9, so the second probability is not still 4/10.
    The product of those two terms is the general multiplication rule
    from Lesson 08, not the independence shortcut.
    """
    p_first_flagged = 4 / 10
    # Reduced sample space: one flagged order has already left the batch.
    p_second_flagged_given_first = 3 / 9
    p_both_flagged = p_first_flagged * p_second_flagged_given_first
    return p_first_flagged, p_second_flagged_given_first, p_both_flagged
# -----------------------------------------------------------------------------


# --- NEW (2) simulate_sequences() --------------------------------------------
def simulate_sequences() -> float:
    """Simulate ordered pairs drawn uniformly without replacement.

    Returns
    -------
    float
        Monte Carlo estimate of P(both flagged): the mean of a 0/1
        indicator over SIMULATIONS seeded trials.

    Notes
    -----
    Labels 0..9 stand for the ten orders; 0..3 are the four flagged ones.
    The second index is drawn from the nine labels that are not `first`
    by mapping a uniform 0..8 integer past the occupied slot. That is
    sampling without replacement, not two independent draws from 0..9.
    """
    rng = np.random.default_rng(SEED)
    # First draw: uniform among 10 labels.
    first = rng.integers(0, 10, size=SIMULATIONS)
    # Second draw starts as uniform among 9 remaining slots.
    second_reduced = rng.integers(0, 9, size=SIMULATIONS)
    # If the reduced index is already at or past `first`, add 1 to skip
    # the occupied label. True counts as 1, so this is an index shift,
    # not a probability. Example: first=3, reduced=3 -> second=4.
    second = second_reduced + (second_reduced >= first)
    # Both labels in {0,1,2,3} means both selected orders are flagged.
    # The mean of that 0/1 array is the simulated probability.
    return float(np.mean((first < 4) & (second < 4)))
# -----------------------------------------------------------------------------


# --- NEW (3) save_evidence() -------------------------------------------------
def save_evidence(naive: float, exact: float, simulated: float) -> None:
    """Save the naive, exact, and simulated sequence probabilities.

    Parameters
    ----------
    naive, exact, simulated:
        Independence shortcut (4/10)^2, exact without-replacement product,
        and the seed-42 Monte Carlo estimate.

    Returns
    -------
    None
        Side effect: writes the PNG. Unattended savefig/close as in Lesson 01.

    Notes
    -----
    The grey bar is too high: it pretends the second draw still sees 4 of
    10. The pink and blue bars should agree, up to simulation noise.
    """
    labels = ["Naive\nindependence", "Exact without\nreplacement", "Seed-42\nsimulation"]
    values = [naive, exact, simulated]
    colors = ["#9E9E9E", "#D81B60", "#1E88E5"]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.19)
    ax.set_ylabel("P(both selected orders are flagged)")
    ax.set_title("Without replacement, the second draw depends on the first")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    """Compare naive independence with the exact and simulated products."""
    p_first, p_second_given_first, exact = exact_sequence_probability()
    # Independence shortcut: second draw still 4/10, so square the first.
    naive = p_first**2
    simulated = simulate_sequences()
    print("Synthetic inspection batch: 10 orders, 4 flagged")
    print(f"P(first flagged): {p_first:.6f}")
    print(f"P(second flagged | first flagged): {p_second_given_first:.6f}")
    print(f"Naive independence probability: {naive:.6f}")
    print(f"Exact probability without replacement: {exact:.6f}")
    print(f"Seed-42 simulation ({SIMULATIONS:,} trials): {simulated:.6f}")
    save_evidence(naive, exact, simulated)
    print("Figure saved:", FIGURE_PATH)


if __name__ == "__main__":
    main()

