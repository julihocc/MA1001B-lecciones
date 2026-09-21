"""
Lesson 07 - Step 1: Repeated Permutations
=========================================
NEW IN THIS STEP: repeated_permutation_count(), enumerate_queue_sequences(),
and save_repeated_permutations_figure().

The Recipe
----------
Build the first complete program in this order:
    1. repeated_permutation_count()  removes duplicate rearrangements
    2. enumerate_queue_sequences()   verifies the formula exhaustively
    3. save_repeated_permutations_figure() exports the counting evidence

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, matplotlib
savefig/close, and the script entry point. This file adds counting tools from
the standard library rather than pandas.

New in this step:
    math.factorial        n! as an integer, not a float
    itertools.permutations  every ordered rearrangement of a sequence
    set(...)              drop duplicate rearrangements of identical labels
    integer division //   keep counts as exact integers
    ax.set_yscale("log")  compare 40,320 with 560 on one vertical axis
    zip(..., strict=True) fail if the two sequences have different lengths

main() computes 8!, the repeated-label formula 8!/(3!3!2!)=560, enumerates
the 560 distinct sequences, and saves a log-scale bar chart.

Run from the repository root:
    uv run en/L07_Counting_Techniques_II/src/
    allocations_01_repeated_permutations.py
"""

# permutations(seq) yields every ordered rearrangement of seq, including
# rearrangements that look identical when some labels repeat.
from itertools import permutations
# factorial(n) returns the integer n! = 1*2*...*n. Using the math module
# (not a hand-rolled loop) keeps the formula readable.
from math import factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# .parents[1] is the lesson folder (src/ -> L07_...). Same idea as
# .parent.parent in Lessons 01-02.
FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
# Three Priority, three Standard, two Audit labels: eight slots, three
# indistinguishable labels of the first kind, and so on.
QUEUE_COUNTS = {"Priority": 3, "Standard": 3, "Audit": 2}
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


# --- NEW (1) repeated_permutation_count() -----------------------------------
def repeated_permutation_count(counts: tuple[int, ...]) -> int:
    """Return the number of distinct sequences with repeated labels.

    Parameters
    ----------
    counts:
        The multiplicity of each label, e.g. (3, 3, 2). Order of the
        tuple does not matter because only the factorials enter.

    Returns
    -------
    int
        n! / (n1! n2! ... nk!) where n = sum(counts). Integer division
        is exact here because each ni! divides n!.

    Notes
    -----
    If every request had a unique queue label, there would be 8! sequences.
    Repeating a label 3 times means those 3! internal swaps are the same
    sequence, so we divide them out.
    """
    total = sum(counts)
    denominator = 1
    for count in counts:
        denominator *= factorial(count)
    return factorial(total) // denominator


# -----------------------------------------------------------------------------


# --- NEW (2) enumerate_queue_sequences() ------------------------------------
def enumerate_queue_sequences() -> list[tuple[str, ...]]:
    """Enumerate every distinct queue-label sequence for eight requests.

    Returns
    -------
    list[tuple[str, ...]]
        Sorted unique 8-tuples such as ('Audit', 'Audit', 'Priority', ...).

    Notes
    -----
    The nested list comprehension expands QUEUE_COUNTS into a concrete
    list of eight labels: three 'Priority', three 'Standard', two 'Audit'.
    permutations() then produces 8! = 40,320 tuples, many of them identical.
    Wrapping in set(...) keeps each distinct tuple once; sorted(...) makes
    the list deterministic for tests and display.
    """
    labels = [
        queue
        for queue, count in QUEUE_COUNTS.items()
        for _ in range(count)
    ]
    return sorted(set(permutations(labels)))


# -----------------------------------------------------------------------------


# --- NEW (3) save_repeated_permutations_figure() ----------------------------
def save_repeated_permutations_figure(
    naive_count: int,
    formula_count: int,
    enumerated_count: int,
) -> Path:
    """Export a chart comparing naive and duplicate-adjusted counts.

    Parameters
    ----------
    naive_count, formula_count, enumerated_count:
        8!, the closed formula, and len(enumerated sequences). The last
        two must match; the first is larger by 3!3!2! = 72.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "allocations_01_repeated_permutations.png"

    labels = ["Naive $8!$", "Repeated-label\nformula", "Enumeration"]
    values = [naive_count, formula_count, enumerated_count]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    # Log scale is required: 40,320 and 560 cannot share a linear axis
    # without flattening the two matching bars to invisibility.
    ax.set_yscale("log")
    ax.set_ylabel("Number of sequences (log scale)")
    ax.set_title(
        "Repeated Labels Collapse Duplicate Rearrangements",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    # strict=True raises if bars and values ever drift out of sync
    # (Python 3.10+). The label is placed at 1.12 * height so it sits
    # above the bar on the log axis.
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value * 1.12,
            f"{value:,}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    # transform=ax.transAxes uses axes coordinates: (1, 0) is the lower
    # right of the panel, independent of the data scale.
    ax.text(
        0.98,
        0.05,
        "Synthetic service-network example",
        transform=ax.transAxes,
        ha="right",
        color="#646464",
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 1 evidence."""
    counts = tuple(QUEUE_COUNTS.values())
    naive_count = factorial(sum(counts))
    formula_count = repeated_permutation_count(counts)
    sequences = enumerate_queue_sequences()
    duplicate_factor = naive_count // formula_count
    output_path = save_repeated_permutations_figure(
        naive_count,
        formula_count,
        len(sequences),
    )

    print("LESSON 07 - STEP 1: REPEATED PERMUTATIONS")
    print("Synthetic queue counts           : Priority=3, Standard=3, Audit=2")
    print(f"Naive count 8!                   : {naive_count:,}")
    print(f"Repeated-permutation formula     : {formula_count:,}")
    print(f"Distinct sequences enumerated    : {len(sequences):,}")
    print(f"Duplicate rearrangement factor   : {duplicate_factor}")
    print(f"Figure saved to                  : {output_path}")


if __name__ == "__main__":
    main()

