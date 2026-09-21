"""
Lesson 06 - Step 3: Combinations and Unordered Subsets
======================================================
NEW IN THIS STEP: subset_combinations(), simulate_committees(), and save_comparison_figure().

Changes from counting_02_permutations.py
The Recipe
Introduce them in this order:
    1. subset_combinations()     calculates selections when order has no effect
    2. simulate_committees()     enumerates the unique three-person panels
    3. save_comparison_figure()  compares ordered and unordered counts

How to read this file:
You already know Python through OOP. Lesson 01 covered pathlib, Agg, and
savefig. Step 2 used math.perm and itertools.permutations because the three
roles were distinct. This script is self-contained and does not import Step 2.

New in this step:
    math.comb(n, k)         C(n, k) = n! / (k! (n-k)!); order does not matter
    itertools.combinations  each k-subset once, as a tuple in input order
    k! reduction            P(n, k) = C(n, k) * k!, because a subset of k
                            people can be lined up in k! role assignments
    math.factorial(k)       k * (k-1) * ... * 1; here 3! = 6
    integer division //     total_perms // total_combs should equal k!

main() forms unranked three-person panels from six analysts, checks that
C(6, 3) = 20, and shows that 120 ordered assignments collapse by 3! = 6.

Run it:
    uv run en/L06_Counting_Techniques_I/src/counting_03_combinations.py
"""

# combinations(elements, k) yields each k-subset once. The tuple is ordered
# by position in the input list, not by any role ranking. (A, B, C) appears;
# (B, A, C) does not, because those names are the same panel.
from itertools import combinations
# math.comb(n, k) is C(n, k). math.perm and math.factorial are reused to
# show the k! bridge between ordered and unordered counts.
import math
# Path, Agg, and savefig: same unattended-figure idiom as Lesson 01.
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) subset_combinations() --------------------------------------------
def subset_combinations(n: int, k: int) -> int:
    """Return C(n, k), the number of k-subsets of an n-element pool.

    Parameters
    ----------
    n:
        Size of the available pool.
    k:
        Panel size. Must satisfy 0 <= k <= n.

    Returns
    -------
    int
        n! / (k! (n-k)!). For n=6, k=3 that is 20.

    Notes
    -----
    Order does not matter because a peer panel has no internal roles.
    {A, B, C} is one committee, however the three names are listed.

    math.comb is the binomial coefficient. It is related to Step 2 by
    P(n, k) = C(n, k) * k!: first choose the people, then assign the k
    roles in k! ways. Type hints are documentation only, as in Step 1.
    """
    return math.comb(n, k)
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_committees() --------------------------------------------
def simulate_committees(elements: list[str], k: int) -> list[tuple[str, ...]]:
    """Enumerate every unique k-subset of the pool.

    Parameters
    ----------
    elements:
        The pool of distinct names.
    k:
        How many people sit on the panel.

    Returns
    -------
    list[tuple[str, ...]]
        One tuple per subset. Length is C(n, k). tuple[str, ...] is the
        same variable-length hint as in Step 2.

    Notes
    -----
    itertools.combinations is the unordered counterpart of permutations.
    Each subset appears once. list() stores the iterator so we can take
    len() and print the first three panels.
    """
    return list(combinations(elements, k))
# ------------------------------------------------------------------------------


# --- NEW (3) save_comparison_figure() -----------------------------------------
def save_comparison_figure(n_fixed: int) -> None:
    """Plot P(n, k) against C(n, k) to show the k! reduction.

    Parameters
    ----------
    n_fixed:
        Pool size held constant on the figure. Here n = 6.

    Returns
    -------
    None
        Side effect: writes counting_03_combinations.png.

    Notes
    -----
    For each k the permutation marker sits k! times above the combination
    marker. Combinations are also symmetric: C(n, k) = C(n, n-k), so the
    red curve peaks in the middle and falls. Permutations keep growing
    until k = n.
    """
    ks = list(range(1, n_fixed + 1))
    perms = [math.perm(n_fixed, k) for k in ks]
    combs = [math.comb(n_fixed, k) for k in ks]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ks, perms, marker="o", color="#0039A6", label="Permutations P(n, k)", linewidth=2)
    ax.plot(ks, combs, marker="s", color="#EC2661", label="Combinations C(n, k)", linewidth=2)
    ax.set_title(f"Permutations vs Combinations for n = {n_fixed}", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Subset Size k", fontsize=10)
    ax.set_ylabel("Cardinality", fontsize=10)
    ax.set_xticks(ks)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path = DIR_FIGURES / "counting_03_combinations.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    """Form unranked panels, verify C(6, 3) = 20, and show the 3! reduction."""
    analysts = ["Analyst_A", "Analyst_B", "Analyst_C", "Analyst_D", "Analyst_E", "Analyst_F"]
    n = len(analysts)
    k = 3

    total_perms = math.perm(n, k)
    total_combs = subset_combinations(n, k)

    committees = simulate_committees(analysts, k)
    exhaustive_total = len(committees)

    save_comparison_figure(n)

    print("================================================================")
    print("LESSON 06 - STEP 3: COMBINATIONS (ORDER DOES NOT MATTER)")
    print("================================================================")
    print("Synthetic data notice         : No real company data are used")
    print(f"Available pool n = {n}, panel size k = {k}")
    print(f"Total permutations P({n}, {k})  : {total_perms}")
    print(f"Total combinations C({n}, {k})  : {total_combs}")
    print(f"Actual combinations generated : {exhaustive_total}")
    # // is integer division. 120 // 20 == 6, which must equal 3!.
    print(f"Reduction factor (k!)         : {total_perms // total_combs} (must equal {math.factorial(k)})")
    print(f"Exact match                   : {total_combs == exhaustive_total}")
    print("First 3 panels:")
    for panel in committees[:3]:
        print(f"   {panel}")
    print(f"Figure saved to               : {DIR_FIGURES / 'counting_03_combinations.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

