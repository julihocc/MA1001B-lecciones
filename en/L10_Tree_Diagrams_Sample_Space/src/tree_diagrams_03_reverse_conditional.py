"""
Lesson 10 - Step 3: Reverse Conditional from Combined Paths
===========================================================
THE RECIPE
Start from tree_diagrams_02_probability_branches.py, then introduce:
    1. reverse_conditional()   P(defective | flagged) from combined flag paths
    2. simulate_lots()         seed-42 check of the reversed conditional
    3. save_figure()           contrast a branch label with the reversed question

The tree is drawn in time order: lot status, then inspection. P(flagged |
defective) is a single downward branch. P(defective | flagged) is not. That
inversion is the limit that Lesson 11 names as Bayes' theorem.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy
generators, the Agg backend, and unattended savefig. Steps 1-2 built the
tree and multiplied along branches. This script copies those counts and
comments only the NEW bands.

New in this step:
    reverse conditional       P(D | F) = P(D and F) / P(F), not a tree branch
    two flagged paths         numerator is one path; denominator adds both
    np.where on a boolean     vectorized P(flag | status) for each simulated lot
    boolean index             is_defective[is_flagged] keeps only flagged lots
    three-bar contrast        0.80 branch vs 0.470588 reverse vs simulation

main() prints P(F | D) = 0.80 against P(D | F) = 8/17, then a seed-42
simulation of 100,000 lots that lands nearby.

Run it:
    python tree_diagrams_03_reverse_conditional.py
"""

from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Identical register to Steps 1-2. SEED now drives the 100,000-lot check.
SEED = 42
N_LOTS = 100
N_DEFECTIVE = 10
N_CLEAN = 90
N_FLAGGED_DEFECTIVE = 8
N_MISSED_DEFECTIVE = 2
N_FLAGGED_CLEAN = 9
N_CLEARED_CLEAN = 81
N_SIMULATIONS = 100_000
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) reverse_conditional() -------------------------------------------
def reverse_conditional() -> dict[str, float]:
    """Compute the reverse conditional by combining the two flagged paths.

    Returns
    -------
    dict[str, float]
        p_flagged_given_defective: the downward branch P(F | D) = 8/10.
        p_defective: stage-1 P(D) = 10/100.
        p_flagged: P(F) = P(D and F) + P(C and F).
        p_defective_given_flagged: P(D | F) = P(D and F) / P(F).
        frequency_defective_given_flagged: the same ratio as 8 / (8 + 9).

    Notes
    -----
    P(F | D) is one edge on the time-ordered tree. P(D | F) asks a
    different question: given that inspection already flagged the lot,
    what is the chance it was defective? That information is spread
    across two leaves, so the tree does not display it as a single
    branch. Lesson 11 will name the inversion Bayes' theorem; here it
    is just path arithmetic.

        P(D | F) = [P(D) P(F | D)] / [P(D) P(F | D) + P(C) P(F | C)]
                 = 0.08 / 0.17 = 8/17.
    """
    p_defective = N_DEFECTIVE / N_LOTS
    p_flagged_given_defective = N_FLAGGED_DEFECTIVE / N_DEFECTIVE
    p_flagged_given_clean = N_FLAGGED_CLEAN / N_CLEAN
    # Joint along the defective-and-flagged path (multiply).
    p_defective_and_flagged = p_defective * p_flagged_given_defective
    # 1.0 - p_defective is P(clean); same as N_CLEAN / N_LOTS.
    p_clean_and_flagged = (1.0 - p_defective) * p_flagged_given_clean
    # Add the two mutually exclusive flagged paths (Step 2 rule).
    p_flagged = p_defective_and_flagged + p_clean_and_flagged
    # Definition of conditional probability: joint over the new given.
    p_defective_given_flagged = p_defective_and_flagged / p_flagged
    return {
        "p_flagged_given_defective": p_flagged_given_defective,
        "p_defective": p_defective,
        "p_flagged": p_flagged,
        "p_defective_given_flagged": p_defective_given_flagged,
        "frequency_defective_given_flagged": (
            N_FLAGGED_DEFECTIVE / (N_FLAGGED_DEFECTIVE + N_FLAGGED_CLEAN)
        ),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_lots() -------------------------------------------------
def simulate_lots() -> float:
    """Simulate the two-stage tree and estimate P(defective | flagged).

    Returns
    -------
    float
        Mean of is_defective among the simulated lots that were flagged.
        Close to 8/17 under seed 42, not a replacement for the exact
        path ratio.

    Notes
    -----
    Each lot is two Uniform(0, 1) draws: first the status coin, then
    the inspection coin with a rate that depends on status. Boolean
    indexing is_defective[is_flagged] restricts the mean to the
    flagged subset, which is the simulated reverse conditional.
    """
    rng = np.random.default_rng(SEED)
    # Bernoulli(0.10) via a Uniform comparison. True = defective.
    is_defective = rng.random(N_SIMULATIONS) < (N_DEFECTIVE / N_LOTS)
    # np.where(condition, a, b) picks 8/10 when defective, 9/90 otherwise.
    # The result is a length-N array of flag probabilities, not a scalar.
    p_flag = np.where(
        is_defective,
        N_FLAGGED_DEFECTIVE / N_DEFECTIVE,
        N_FLAGGED_CLEAN / N_CLEAN,
    )
    is_flagged = rng.random(N_SIMULATIONS) < p_flag
    # [is_flagged] keeps only flagged lots; mean of True/False is a proportion.
    return float(np.mean(is_defective[is_flagged]))
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    branch_label: float,
    reversed_exact: float,
    reversed_simulated: float,
) -> Path:
    """Contrast the downward branch with the reversed conditional.

    Parameters
    ----------
    branch_label:
        P(flagged | defective) = 0.80, a single tree edge.
    reversed_exact:
        P(defective | flagged) from combined paths, 8/17.
    reversed_simulated:
        Seed-42 Monte Carlo estimate of that same reverse conditional.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. See
        Lesson 01 for savefig/close.

    Notes
    -----
    Three bars, one idea: the time-ordered tree displays the first
    number and does not display the second. The third bar is a check,
    not a third definition. ylim 0-1.05 leaves room for the labels.
    """
    output_path = DIR_FIGURES / "tree_diagrams_03_reverse_conditional.png"
    labels = [
        "P(flagged |\ndefective)\nbranch",
        "P(defective |\nflagged)\ncombined paths",
        "Seed-42\nsimulation",
    ]
    values = [branch_label, reversed_exact, reversed_simulated]
    colors = ["#1A2E51", "#EC2661", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probability")
    ax.set_title("A Time-Ordered Tree Does Not Display the Reverse Conditional")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # Same bar-label pattern as Step 2: center horizontally, lift by 0.03.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Print the branch, the reverse conditional, and the simulation check.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    results = reverse_conditional()
    simulated = simulate_lots()
    figure_path = save_figure(
        results["p_flagged_given_defective"],
        results["p_defective_given_flagged"],
        simulated,
    )

    print("================================================================")
    print("LESSON 10 - STEP 3: REVERSE CONDITIONAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Simulated lots                  : {N_SIMULATIONS:,}")
    print(
        "P(flagged | defective)          : "
        f"{results['p_flagged_given_defective']:.6f}"
    )
    print(f"P(defective)                    : {results['p_defective']:.6f}")
    print(f"P(flagged)                      : {results['p_flagged']:.6f}")
    print(
        "P(defective | flagged)          : "
        f"{results['p_defective_given_flagged']:.6f}"
    )
    print(
        "Frequency check 8/17            : "
        f"{results['frequency_defective_given_flagged']:.6f}"
    )
    print(f"Seed-42 simulation              : {simulated:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()

