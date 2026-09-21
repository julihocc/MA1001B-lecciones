"""
Lesson 06 - Step 2: Permutations and Ordered Assignments
========================================================
NEW IN THIS STEP: linear_permutations(), simulate_assignments(), and save_growth_figure().

Changes from counting_01_product_rule.py
The Recipe
Introduce them in this order:
    1. linear_permutations()   calculates ordered assignments without replacement
    2. simulate_assignments()  enumerates assignments for three distinct roles
    3. save_growth_figure()    shows growth as the number of assigned roles rises

How to read this file:
You already know Python through OOP. Lesson 01 covered pathlib, Agg, and
savefig. Step 1 used itertools.product for a Cartesian product of independent
stages. This script is self-contained and does not import Step 1.

New in this step:
    math.perm(n, k)           P(n, k) = n! / (n-k)! without writing factorials
    itertools.permutations    every ordered k-tuple without replacement
    tuple[str, ...]           a k-tuple of strings; k is not fixed in the type
    falling product           6 * 5 * 4 = 120 when roles are distinct

main() assigns three distinct roles from six analysts, checks that the
formula and the enumeration both give 120, and plots P(6, k) as k grows.

Run it:
    uv run en/L06_Counting_Techniques_I/src/counting_02_permutations.py
"""

# permutations(elements, k) yields every ordered k-tuple of distinct items.
# (A, B, C) and (B, A, C) are different outcomes because the roles differ.
from itertools import permutations
# math.perm(n, k) is the library form of P(n, k). Available since Python 3.8.
import math
# Path, Agg, and savefig: same unattended-figure idiom as Lesson 01.
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) linear_permutations() --------------------------------------------
def linear_permutations(n: int, k: int) -> int:
    """Return P(n, k), the number of ordered k-assignments from n people.

    Parameters
    ----------
    n:
        Size of the available pool.
    k:
        Number of distinct roles to fill. Must satisfy 0 <= k <= n.

    Returns
    -------
    int
        n * (n-1) * ... * (n-k+1). For n=6, k=3 that is 6 * 5 * 4 = 120.

    Notes
    -----
    Order matters because Lead, Validation, and Reporting are different
    jobs. Assigning Ana as Lead and Ben as Validation is not the same
    assignment as the reverse.

    math.perm(n, k) equals n! / (n-k)!. The library function uses the
    falling product so it never builds two huge factorials. Type hints
    are documentation only, as in Step 1.
    """
    return math.perm(n, k)
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_assignments() -------------------------------------------
def simulate_assignments(elements: list[str], k: int) -> list[tuple[str, ...]]:
    """Enumerate every ordered k-tuple drawn without replacement.

    Parameters
    ----------
    elements:
        The pool of distinct names.
    k:
        How many roles to fill.

    Returns
    -------
    list[tuple[str, ...]]
        One tuple per assignment. The ellipsis in tuple[str, ...] means
        "some number of strings," not a fixed triple. Length is P(n, k).

    Notes
    -----
    Without replacement: a person cannot hold two roles at once.
    itertools.permutations walks the ordered tuples in lexicographic
    order of the input list. list() stores them so we can take len()
    and print the first three.
    """
    return list(permutations(elements, k))
# ------------------------------------------------------------------------------


# --- NEW (3) save_growth_figure() ---------------------------------------------
def save_growth_figure(n_fixed: int) -> None:
    """Plot P(n, k) as the number of assigned roles k grows from 1 to n.

    Parameters
    ----------
    n_fixed:
        Pool size held constant on the figure. Here n = 6.

    Returns
    -------
    None
        Side effect: writes counting_02_permutations.png.

    Notes
    -----
    P(n, k) is a falling product of k factors. As k rises toward n the
    curve steepens; P(n, n) = n!, here 720. That growth is why listing
    assignments by hand stops being reasonable.
    """
    # k = 1, 2, ..., n. range stops before n_fixed + 1, so n is included.
    ks = list(range(1, n_fixed + 1))
    values = [math.perm(n_fixed, k) for k in ks]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ks, values, marker="o", color="#0039A6", linewidth=2, markersize=7)
    ax.set_title(f"Permutations Growth Curve P({n_fixed}, k)", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Selection size k (roles assigned)", fontsize=11)
    ax.set_ylabel("Total Permutations", fontsize=10)
    ax.set_xticks(ks)
    ax.grid(True, linestyle="--", alpha=0.5)

    # zip pairs each k with its P(n, k) so the label sits on the marker.
    for k, val in zip(ks, values):
        ax.annotate(f"{val}", xy=(k, val), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=9)

    plt.tight_layout()
    output_path = DIR_FIGURES / "counting_02_permutations.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    """Assign three distinct roles from six analysts and verify P(6, 3) = 120."""
    analysts = ["Analyst_A", "Analyst_B", "Analyst_C", "Analyst_D", "Analyst_E", "Analyst_F"]
    n = len(analysts)
    k = 3

    theoretical_total = linear_permutations(n, k)
    assignments = simulate_assignments(analysts, k)
    exhaustive_total = len(assignments)

    save_growth_figure(n)

    print("================================================================")
    print("LESSON 06 - STEP 2: PERMUTATIONS (ORDER MATTERS)")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Available pool n = {n} analysts, roles to assign k = {k}")
    print(f"Theoretical formula P({n}, {k})  : {theoretical_total}")
    print(f"Actual permutations generated   : {exhaustive_total}")
    print(f"Exact match                     : {theoretical_total == exhaustive_total}")
    print("First 3 ordered assignments (Lead, Validation, Reporting):")
    for triplet in assignments[:3]:
        print(f"   {triplet}")
    print(f"Figure saved to                : {DIR_FIGURES / 'counting_02_permutations.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

