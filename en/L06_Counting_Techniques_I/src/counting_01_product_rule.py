"""
Lesson 06 - Step 1: Product Rule and Configuration Space
========================================================
NEW IN THIS STEP: product_rule(), generate_sample_space(), and save_figure().

The Recipe
Enumerate a fully synthetic operations-review configuration across three
fulfillment centers, four workflow stages, and two evidence types. Verify that
the product rule and exhaustive enumeration both produce 24 outcomes.

How to read this file:
You already know Python through OOP: functions, lists, dictionaries, loops,
and conditionals. Lesson 01 introduced pathlib, the Agg backend, and
unattended savefig. Those file-system and plotting idioms return here with a
short pointer, not a second treatise. This lesson does not use NumPy, pandas,
or a random seed: every count is exact.

New in this step:
    type hints            list[int], tuple[str, str, str], dict[str, int]
                          document contracts; Python does not enforce them
    itertools.product     Cartesian product of independent finite lists
    running product       multiply the stage sizes n1 * n2 * n3
    BarContainer          ax.bar returns rectangles used to place labels

main() builds a 3 x 4 x 2 configuration space, checks that the product rule
and exhaustive enumeration both give 24, and writes the evidence figure.

Run it:
    uv run en/L06_Counting_Techniques_I/src/counting_01_product_rule.py
"""

# product(A, B, C) yields every (a, b, c) with a in A, b in B, and c in C.
# That iterator is the Cartesian product of the three lists.
from itertools import product
# Path, Agg, and savefig: same unattended-figure idiom as Lesson 01.
# __file__ locates figures/ next to this package; Agg must be selected
# before pyplot so no GUI window is opened. See L01 Step 1 for the full
# explanation.
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) product_rule() ---------------------------------------------------
def product_rule(stages: list[int]) -> int:
    """Return the number of outcomes in a sequence of independent finite stages.

    Parameters
    ----------
    stages:
        One integer per choice stage: the number of options at that stage.
        The names of the options are not needed for the count.

    Returns
    -------
    int
        The product n1 * n2 * ... * nm. For this lesson, 3 * 4 * 2 = 24.

    Notes
    -----
    `stages: list[int] -> int` is a type hint. Python does not enforce it
    at run time. It documents the contract: pass a list of integers, get
    an integer back.

    The stages are independent in the Cartesian sense: choosing a center
    does not shrink the workflow or evidence lists. That is why the sizes
    multiply rather than a permutation-style falling product.
    """
    # 1 is the identity for multiplication. Each stage size is folded in.
    total = 1
    for n in stages:
        total *= n
    return total
# ------------------------------------------------------------------------------


# --- NEW (2) generate_sample_space() ------------------------------------------
def generate_sample_space(
    centers: list[str], stages: list[str], evidence_types: list[str]
) -> list[tuple[str, str, str]]:
    """Build every configuration triplet by exhaustive Cartesian product.

    Parameters
    ----------
    centers, stages, evidence_types:
        The three finite option lists. One value is chosen from each list.

    Returns
    -------
    list[tuple[str, str, str]]
        All (center, workflow stage, evidence type) triples. Length equals
        len(centers) * len(stages) * len(evidence_types).

    Notes
    -----
    itertools.product is nested looping: for each center, for each stage,
    for each evidence type, yield the triple. The last iterable varies
    fastest, so the first three triples all start at Center_A, Receiving.
    """
    # list() materializes the iterator so we can take len() and slice it.
    return list(product(centers, stages, evidence_types))
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ----------------------------------------------------
def save_figure(counts_by_center: dict[str, int]) -> None:
    """Render and save the configuration counts per center without a window.

    Parameters
    ----------
    counts_by_center:
        Map from center name to how many (stage, evidence) pairs it has.
        With 4 stages and 2 evidence types, each center should show 8.

    Returns
    -------
    None
        Side effect: writes counting_01_product_rule.png. No window is shown.

    Notes
    -----
    ax.bar returns a BarContainer of Rectangle patches. Each patch knows its
    left edge, width, and height, which is how the numeric labels are placed
    above the bars. savefig is the same unattended write as Lesson 01.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(
        list(counts_by_center.keys()),
        list(counts_by_center.values()),
        color="#1A2E51",
        edgecolor="#EC2661",
        linewidth=1.5,
    )
    ax.set_title(
        "Review Configurations per Fulfillment Center",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Fulfillment center", fontsize=11)
    ax.set_ylabel("Workflow stage and evidence combinations", fontsize=11)
    # Each center has 4 * 2 = 8 configurations; 12 leaves room for labels.
    ax.set_ylim(0, 12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        # get_x() is the left edge. Adding half the width centers the label.
        # xytext=(0, 3) with offset points shifts it 3 points above the bar.
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    output_path = DIR_FIGURES / "counting_01_product_rule.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    """Enumerate the 3 x 4 x 2 space, verify the product rule, and save the figure."""
    # Three independent stages: who is reviewed, which workflow step, which evidence.
    centers = ["Center_A", "Center_B", "Center_C"]
    workflow_stages = ["Receiving", "Picking", "Packing", "Dispatch"]
    evidence_types = ["Record", "Observation"]

    # Sizes only. product_rule never sees the labels.
    stages = [len(centers), len(workflow_stages), len(evidence_types)]
    theoretical_total = product_rule(stages)

    sample_space = generate_sample_space(centers, workflow_stages, evidence_types)
    exhaustive_total = len(sample_space)

    # item[0] is the center in each (center, stage, evidence) triple.
    # sum(1 for ... if ...) counts matches without building a second list.
    counts_by_center = {
        center: sum(1 for item in sample_space if item[0] == center)
        for center in centers
    }
    save_figure(counts_by_center)

    print("================================================================")
    print("LESSON 06 - STEP 1: PRODUCT RULE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(
        "Stages                          : "
        f"Centers ({len(centers)}) x Workflow ({len(workflow_stages)}) "
        f"x Evidence ({len(evidence_types)})"
    )
    print(f"Theoretical product rule total : {theoretical_total}")
    print(f"Exhaustive enumeration total   : {exhaustive_total}")
    print(f"Exact match                    : {theoretical_total == exhaustive_total}")
    print("First 3 configurations :")
    for triplet in sample_space[:3]:
        print(f"   {triplet}")
    print(f"Figure saved to               : {DIR_FIGURES / 'counting_01_product_rule.png'}")
    print("================================================================")


# Python sets __name__ to "__main__" only when this file is the program
# being executed. See L01 Step 1 if this idiom is new.
if __name__ == "__main__":
    main()

