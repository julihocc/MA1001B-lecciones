"""
Lesson 10 - Step 1: Frequency Tree and Sample-Space Decomposition
================================================================
NEW IN THIS STEP: lot_status_counts(), inspection_joint_counts(), and
save_figure().

The Recipe
----------
Build the first complete program in this order:
    1. lot_status_counts()       first-stage frequencies (defective vs clean)
    2. inspection_joint_counts() four mutually exclusive terminal-path counts
    3. save_figure()             draw the two-stage frequency tree

Context:
A fully synthetic incoming-lot register has 100 lots: 10 defective and 90
clean. Each lot is inspected once. Among defective lots, 8 are flagged and 2
are missed. Among clean lots, 9 are flagged and 81 are cleared. A tree diagram
decomposes this two-stage experiment into mutually exclusive terminal paths.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, the Agg
backend, and unattended savefig. Those idioms return here with a short
pointer, not a second treatise.

New in this step:
    dict of counts            named frequencies, not a pandas table
    FancyBboxPatch            rounded boxes at (x, y) data coordinates
    nested helper box()       local function that draws one labeled node
    ax.annotate arrows        directed edges from parent to child
    axis("off")               hide ticks; the axes are a , not a chart

main() reports the four terminal counts, checks that they sum to 100, and
writes the frequency-tree figure.

Run it:
    python tree_diagrams_01_frequency_tree.py
"""

from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# FancyBboxPatch is a Patch subclass: a rectangle with rounded corners.
# Lesson 01 used only ax.hist; this figure is a diagram, not a histogram.
from matplotlib.patches import FancyBboxPatch


# SEED is declared in every lesson script. Step 1 does not draw random
# numbers; the same 42 is reserved so Step 3 can simulate from it.
SEED = 42
# These eight integers ARE the synthetic register. They are not estimated
# from a larger file. 10 + 90 = 100, and 8 + 2 + 9 + 81 = 100.
N_LOTS = 100
N_DEFECTIVE = 10
N_CLEAN = 90
N_FLAGGED_DEFECTIVE = 8
N_MISSED_DEFECTIVE = 2
N_FLAGGED_CLEAN = 9
N_CLEARED_CLEAN = 81
# figures/ next to this package, independent of the shell's working directory.
# Path construction and mkdir: see Lesson 01.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) lot_status_counts() ---------------------------------------------
def lot_status_counts() -> dict[str, int]:
    """Return the first-stage frequencies in the synthetic lot register.

    Returns
    -------
    dict[str, int]
        defective = 10, clean = 90, total = 100. Keys are stage-1 node
        names; values are counts, not probabilities.

    Notes
    -----
    Stage 1 splits the sample space by lot status, before inspection.
    Every lot is exactly one of these two nodes, so the two counts sum
    to N_LOTS. The function packages the module constants; it does not
    read a table.
    """
    return {
        "defective": N_DEFECTIVE,
        "clean": N_CLEAN,
        "total": N_LOTS,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) inspection_joint_counts() ---------------------------------------
def inspection_joint_counts() -> dict[str, int]:
    """Return the four mutually exclusive terminal-path frequencies.

    Returns
    -------
    dict[str, int]
        One count per complete path through the tree:
        defective_flagged = 8, defective_missed = 2,
        clean_flagged = 9, clean_cleared = 81.

    Notes
    -----
    A terminal path is a joint outcome: status AND inspection result.
    The four paths partition the 100 lots, so they are mutually
    exclusive and exhaustive. "Flagged" is not a single leaf: it is
    the union of the two flagged paths (8 + 9 = 17).
    """
    return {
        "defective_flagged": N_FLAGGED_DEFECTIVE,
        "defective_missed": N_MISSED_DEFECTIVE,
        "clean_flagged": N_FLAGGED_CLEAN,
        "clean_cleared": N_CLEARED_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(joints: dict[str, int]) -> Path:
    """Save a frequency tree for the two-stage inspection experiment.

    Parameters
    ----------
    joints:
        The four terminal-path counts from inspection_joint_counts().
        The boxes below hard-code the same integers so the PNG matches
        the slides exactly; joints documents which leaves those numbers
        are.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    The axes are a  (xlim 0-10, ylim 0-6) with ticks hidden.
    Three columns read left to right: start, lot status, inspection
    result. Each lot follows exactly one path from Start to a leaf.
    """
    output_path = DIR_FIGURES / "tree_diagrams_01_frequency_tree.png"
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    # Data coordinates, not a numeric chart. axis("off") drops the frame.
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Frequency Tree: 100 Synthetic Lots")

    def box(x, y, text, color):
        """Draw one rounded node centered at (x, y).

        FancyBboxPatch wants the lower-left corner, so subtract half the
        width and height. ax.text then places the label at the same
        center. Nested so the helper closes over this Axes only.
        """
        patch = FancyBboxPatch(
            (x - 1.15, y - 0.38),
            2.30,
            0.76,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            facecolor=color,
            edgecolor="#1A2E51",
            linewidth=1.1,
        )
        ax.add_patch(patch)
        ax.text(x, y, text, ha="center", va="center", fontsize=9, color="#1A2E51")

    # Column 1: the whole sample space. Column 2: stage-1 split.
    # Column 3: four mutually exclusive leaves.
    box(1.4, 3.0, "Start\n100 lots", "#F4F6F9")
    box(4.6, 4.6, "Defective\n10", "#F8D5DE")
    box(4.6, 1.4, "Clean\n90", "#D6E4F0")
    box(8.3, 5.3, "Flagged\n8", "#EC2661")
    box(8.3, 3.9, "Missed\n2", "#F4A6B8")
    box(8.3, 2.1, "Flagged\n9", "#5B8DEF")
    box(8.3, 0.7, "Cleared\n81", "#A9C4EA")

    # xy is the arrow head (child), xytext is the tail (parent).
    # "-|>" is a line with a triangle tip, not a data annotation.
    ax.annotate("", xy=(3.4, 4.4), xytext=(2.55, 3.35),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(3.4, 1.6), xytext=(2.55, 2.65),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 5.2), xytext=(5.75, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 4.0), xytext=(5.75, 4.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 2.0), xytext=(5.75, 1.6),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 0.8), xytext=(5.75, 1.2),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))

    # Branch labels are frequencies given the parent node, not yet
    # decimal probabilities. 8/10 is "of the 10 defective lots."
    ax.text(3.15, 4.15, "10/100", fontsize=8, color="#646464")
    ax.text(3.15, 1.85, "90/100", fontsize=8, color="#646464")
    ax.text(6.35, 5.45, "8/10", fontsize=8, color="#646464")
    ax.text(6.35, 3.55, "2/10", fontsize=8, color="#646464")
    ax.text(6.35, 2.35, "9/90", fontsize=8, color="#646464")
    ax.text(6.35, 0.45, "81/90", fontsize=8, color="#646464")

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Print the four terminal counts and export the frequency tree.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    status = lot_status_counts()
    joints = inspection_joint_counts()
    # A partition of the sample space must recover N_LOTS.
    path_sum = sum(joints.values())
    # Flagged is two leaves, not one: defective-and-flagged plus
    # clean-and-flagged. Step 2 will add those paths as probabilities.
    flagged = joints["defective_flagged"] + joints["clean_flagged"]
    figure_path = save_figure(joints)

    print("================================================================")
    print("LESSON 10 - STEP 1: FREQUENCY TREE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Total lots                      : {status['total']}")
    print(f"Defective lots                  : {status['defective']}")
    print(f"Clean lots                      : {status['clean']}")
    print(f"Defective and flagged           : {joints['defective_flagged']}")
    print(f"Defective and missed            : {joints['defective_missed']}")
    print(f"Clean and flagged               : {joints['clean_flagged']}")
    print(f"Clean and cleared               : {joints['clean_cleared']}")
    print(f"Terminal-path sum               : {path_sum}")
    print(f"Flagged lots                    : {flagged}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()
