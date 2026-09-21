"""
Lesson 10 - Step 2: Probability Labels and Path Multiplication
==============================================================
THE RECIPE
Start from tree_diagrams_01_frequency_tree.py, then introduce:
    1. branch_probabilities()   convert frequencies to branch probabilities
    2. path_probabilities()     multiply along branches; add mutually exclusive paths
    3. save_figure()            compare the four terminal-path probabilities

The same 100-lot synthetic register is rebuilt from the same constants. No
earlier lesson script is imported.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, the Agg
backend, and unattended savefig. Step 1 drew the frequency tree; this
script copies the same counts and comments only the NEW bands.

New in this step:
    count / parent            a branch probability is conditional on its node
    product along a path      P(status and result) = P(status) P(result | status)
    sum of disjoint paths     P(flagged) = flagged-defective + flagged-clean
    ax.bar                    four terminal probabilities on one vertical axis

main() prints each branch, each joint path, P(flagged) = 0.17, and a
four-path total of 1.

Run it:
    python tree_diagrams_02_probability_branches.py
"""

from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Identical register to Step 1. SEED stays reserved until Step 3.
SEED = 42
N_LOTS = 100
N_DEFECTIVE = 10
N_CLEAN = 90
N_FLAGGED_DEFECTIVE = 8
N_MISSED_DEFECTIVE = 2
N_FLAGGED_CLEAN = 9
N_CLEARED_CLEAN = 81
# figures/ next to this package; see Lesson 01 for Path(__file__) and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) branch_probabilities() ------------------------------------------
def branch_probabilities() -> dict[str, float]:
    """Convert first- and second-stage frequencies into branch probabilities.

    Returns
    -------
    dict[str, float]
        p_defective, p_clean: stage-1 splits, each divided by N_LOTS.
        p_flagged_given_defective and p_missed_given_defective: stage-2
        splits among the 10 defective lots.
        p_flagged_given_clean and p_cleared_given_clean: stage-2 splits
        among the 90 clean lots.

    Notes
    -----
    A branch label is P(this child | we already reached the parent).
    8/10 is P(flagged | defective), not P(flagged). Dividing by the
    wrong denominator (N_LOTS instead of the parent count) would turn
    a conditional into a joint.
    """
    return {
        "p_defective": N_DEFECTIVE / N_LOTS,
        "p_clean": N_CLEAN / N_LOTS,
        "p_flagged_given_defective": N_FLAGGED_DEFECTIVE / N_DEFECTIVE,
        "p_missed_given_defective": N_MISSED_DEFECTIVE / N_DEFECTIVE,
        "p_flagged_given_clean": N_FLAGGED_CLEAN / N_CLEAN,
        "p_cleared_given_clean": N_CLEARED_CLEAN / N_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) path_probabilities() --------------------------------------------
def path_probabilities(branches: dict[str, float]) -> dict[str, float]:
    """Multiply along each branch and add the two flagged paths.

    Parameters
    ----------
    branches:
        The six branch probabilities from branch_probabilities().

    Returns
    -------
    dict[str, float]
        Four joint path probabilities, plus flagged (the two flagged
        paths added) and total (all four paths added).

    Notes
    -----
    Multiplication rule along a path:
        P(D and F) = P(D) P(F | D) = 0.10 * 0.80 = 0.08.
    Addition of mutually exclusive paths:
        P(F) = P(D and F) + P(C and F) = 0.08 + 0.09 = 0.17.
    The four terminals partition the sample space, so their sum is 1.
    """
    # Each product is one complete path: first-stage times second-stage.
    p_def_flag = (
        branches["p_defective"] * branches["p_flagged_given_defective"]
    )
    p_def_miss = (
        branches["p_defective"] * branches["p_missed_given_defective"]
    )
    p_clean_flag = branches["p_clean"] * branches["p_flagged_given_clean"]
    p_clean_clear = branches["p_clean"] * branches["p_cleared_given_clean"]
    return {
        "defective_flagged": p_def_flag,
        "defective_missed": p_def_miss,
        "clean_flagged": p_clean_flag,
        "clean_cleared": p_clean_clear,
        # Two leaves, one event: a lot is flagged by either path.
        "flagged": p_def_flag + p_clean_flag,
        "total": p_def_flag + p_def_miss + p_clean_flag + p_clean_clear,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(paths: dict[str, float]) -> Path:
    """Save the four mutually exclusive path probabilities.

    Parameters
    ----------
    paths:
        Joint probabilities from path_probabilities(). Only the four
        terminal keys are drawn; flagged and total are console checks.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. See
        Lesson 01 for savefig/close.

    Notes
    -----
    A bar chart, not a tree: Step 1 already showed the topology. The
    four bars are a partition of 1, so ylim runs from 0 to 1. Colors
    match the Step 1 leaves (pink defective, blue clean).
    """
    output_path = DIR_FIGURES / "tree_diagrams_02_path_probabilities.png"
    # "\n" inside a tick label wraps the text onto two lines.
    labels = [
        "Defective\nand flagged",
        "Defective\nand missed",
        "Clean\nand flagged",
        "Clean\nand cleared",
    ]
    values = np.array(
        [
            paths["defective_flagged"],
            paths["defective_missed"],
            paths["clean_flagged"],
            paths["clean_cleared"],
        ]
    )
    colors = ["#EC2661", "#F4A6B8", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Path probability")
    ax.set_title("Multiply Along Branches; Add Mutually Exclusive Paths")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each Rectangle with its height. get_x() + width/2 is
    # the bar center; value + 0.03 lifts the label above the cap.
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
    """Print branch labels, path products, and the flagged-path sum.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    branches = branch_probabilities()
    paths = path_probabilities(branches)
    figure_path = save_figure(paths)

    print("================================================================")
    print("LESSON 10 - STEP 2: PROBABILITY BRANCHES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"P(defective)                    : {branches['p_defective']:.6f}")
    print(f"P(clean)                        : {branches['p_clean']:.6f}")
    print(
        "P(flagged | defective)          : "
        f"{branches['p_flagged_given_defective']:.6f}"
    )
    print(
        "P(missed | defective)           : "
        f"{branches['p_missed_given_defective']:.6f}"
    )
    print(
        "P(flagged | clean)              : "
        f"{branches['p_flagged_given_clean']:.6f}"
    )
    print(
        "P(cleared | clean)              : "
        f"{branches['p_cleared_given_clean']:.6f}"
    )
    print(f"P(defective and flagged)        : {paths['defective_flagged']:.6f}")
    print(f"P(defective and missed)         : {paths['defective_missed']:.6f}")
    print(f"P(clean and flagged)            : {paths['clean_flagged']:.6f}")
    print(f"P(clean and cleared)            : {paths['clean_cleared']:.6f}")
    print(f"P(flagged) = sum of flag paths  : {paths['flagged']:.6f}")
    print(f"Sum of all four paths           : {paths['total']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()

