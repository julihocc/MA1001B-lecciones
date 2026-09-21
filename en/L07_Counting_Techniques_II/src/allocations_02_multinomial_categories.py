"""
Lesson 07 - Step 2: Multinomial Category Allocations
====================================================
NEW IN THIS STEP: enumerate_labeled_allocations(), first_request_counts(), and
save_multinomial_figure().

Changes from allocations_01_repeated_permutations.py
The Recipe
----------
Introduce these changes in order:
    1. enumerate_labeled_allocations() assigns labeled requests to fixed queues
    2. first_request_counts()          checks one request across all allocations
    3. save_multinomial_figure()       exports formula and allocation evidence

How to read this file:
You already know Python through OOP. Step 1 counted distinct sequences of
repeated labels. This step uses the same coefficient to count allocations of
eight *labeled* requests into three *labeled* queues of fixed sizes.

New in this step:
    itertools.combinations  unordered subsets (who goes to Priority)
    nested combinations     after Priority is filled, choose Standard
    leftover tuple          Audit gets whoever remains
    collections.Counter     tally how often R01 lands in each queue
    variable annotations    allocations: list[dict[str, tuple[str, ...]]]

main() verifies that the multinomial formula and the nested enumeration both
return 560, then counts how often request R01 appears in each queue.

Run from the repository root:
    uv run en/L07_Counting_Techniques_II/src/
    allocations_02_multinomial_categories.py
"""

# Counter is a dict subclass: missing keys start at 0, and += 1 is the
# usual tally pattern.
from collections import Counter
from itertools import combinations, permutations
from math import factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
QUEUE_COUNTS = {"Priority": 3, "Standard": 3, "Audit": 2}
# R01 .. R08. The :02d format matches Lesson 02 facility IDs.
REQUESTS = tuple(f"R{i:02d}" for i in range(1, 9))
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


def repeated_permutation_count(counts: tuple[int, ...]) -> int:
    """Return the number of distinct sequences with repeated labels.

    Same formula as Step 1. Here it is also the multinomial coefficient
    that counts allocations of labeled requests into labeled queues of
    those sizes.
    """
    total = sum(counts)
    denominator = 1
    for count in counts:
        denominator *= factorial(count)
    return factorial(total) // denominator


def enumerate_queue_sequences() -> list[tuple[str, ...]]:
    """Enumerate every distinct queue-label sequence for eight requests."""
    labels = [
        queue
        for queue, count in QUEUE_COUNTS.items()
        for _ in range(count)
    ]
    return sorted(set(permutations(labels)))


# --- NEW (1) enumerate_labeled_allocations() --------------------------------
def enumerate_labeled_allocations() -> list[dict[str, tuple[str, ...]]]:
    """Assign eight labeled requests to three labeled queues of fixed sizes.

    Returns
    -------
    list[dict[str, tuple[str, ...]]]
        Each dict has keys Priority, Standard, Audit. Values are tuples
        of request IDs of lengths 3, 3, and 2.

    Notes
    -----
    combinations(REQUESTS, 3) lists every unordered Priority trio. The
    remaining five IDs go to after_priority. combinations of those five
    choose the Standard trio; Audit is whoever is left. Because Audit's
    size is then forced, we do not loop over it. The number of leaves
    equals C(8,3)*C(5,3)*C(2,2) = 56*10*1 = 560.
    """
    allocations: list[dict[str, tuple[str, ...]]] = []
    for priority in combinations(REQUESTS, QUEUE_COUNTS["Priority"]):
        after_priority = tuple(item for item in REQUESTS if item not in priority)
        for standard in combinations(
            after_priority,
            QUEUE_COUNTS["Standard"],
        ):
            audit = tuple(item for item in after_priority if item not in standard)
            allocations.append(
                {
                    "Priority": priority,
                    "Standard": standard,
                    "Audit": audit,
                }
            )
    return allocations


# -----------------------------------------------------------------------------


# --- NEW (2) first_request_counts() -----------------------------------------
def first_request_counts(
    allocations: list[dict[str, tuple[str, ...]]],
) -> Counter[str]:
    """Count the queue containing R01 across every valid allocation.

    Parameters
    ----------
    allocations:
        The 560 dictionaries from enumerate_labeled_allocations().

    Returns
    -------
    Counter[str]
        Keys are queue names. Values are how many allocations place R01
        (REQUESTS[0]) in that queue. Because every allocation places R01
        somewhere, the three counts sum to 560. They should be
        3/8, 3/8, and 2/8 of 560: 210, 210, 140.

    Notes
    -----
    break after the first matching queue is a safety: R01 cannot sit in
    two queues of one allocation.
    """
    counts: Counter[str] = Counter()
    for allocation in allocations:
        for queue, requests in allocation.items():
            if REQUESTS[0] in requests:
                counts[queue] += 1
                break
    return counts


# -----------------------------------------------------------------------------


# --- NEW (3) save_multinomial_figure() --------------------------------------
def save_multinomial_figure(
    formula_count: int,
    enumerated_count: int,
    request_counts: Counter[str],
) -> Path:
    """Export formula verification and R01 allocation counts.

    Left panel: formula vs enumeration (both 560). Right panel: how often
    R01 lands in each queue. Side effect: writes the PNG.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "allocations_02_multinomial_categories.png"

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.9))
    bars = axes[0].bar(
        ["Multinomial\nformula", "Enumeration"],
        [formula_count, enumerated_count],
        color=[TEC_BLUE, TEC_NAVY],
        width=0.58,
    )
    axes[0].set_title("Total Fixed-Size Allocations", fontweight="bold")
    axes[0].set_ylabel("Number of allocations")
    axes[0].set_ylim(0, 640)
    axes[0].grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, [formula_count, enumerated_count], strict=True):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            value + 16,
            f"{value:,}",
            ha="center",
            fontweight="bold",
        )

    # list(QUEUE_COUNTS) is the insertion order of the dict: Priority,
    # Standard, Audit. That keeps the bars aligned with QUEUE_COUNTS.
    queues = list(QUEUE_COUNTS)
    values = [request_counts[queue] for queue in queues]
    bars = axes[1].bar(
        queues,
        values,
        color=[TEC_PINK, TEC_BLUE, TEC_NAVY],
        width=0.62,
    )
    axes[1].set_title("Where Does Request R01 Go?", fontweight="bold")
    axes[1].set_ylabel("Allocations containing R01")
    axes[1].set_ylim(0, 245)
    axes[1].grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 6,
            f"{value:,}",
            ha="center",
            fontweight="bold",
        )

    fig.suptitle(
        "One Multinomial Coefficient, Two Verifiable Views",
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 2 evidence."""
    formula_count = repeated_permutation_count(tuple(QUEUE_COUNTS.values()))
    allocations = enumerate_labeled_allocations()
    request_counts = first_request_counts(allocations)
    output_path = save_multinomial_figure(
        formula_count,
        len(allocations),
        request_counts,
    )

    print("LESSON 07 - STEP 2: MULTINOMIAL CATEGORY ALLOCATIONS")
    print(f"Labeled requests                  : {len(REQUESTS)}")
    print("Fixed queue sizes                 : Priority=3, Standard=3, Audit=2")
    print(f"Multinomial formula               : {formula_count:,}")
    print(f"Allocations enumerated            : {len(allocations):,}")
    for queue in QUEUE_COUNTS:
        print(f"Allocations with R01 in {queue:<8} : {request_counts[queue]:,}")
    print(f"Figure saved to                   : {output_path}")


if __name__ == "__main__":
    main()

