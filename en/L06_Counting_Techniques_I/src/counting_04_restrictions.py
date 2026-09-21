"""
Lesson 06 - Step 4: Interacting Restrictions and Overcounting
==============================================================
NEW IN THIS STEP: naive_counting_trap(), rigorous_decomposition(), and exhaustive_check().

Changes from counting_03_combinations.py
The Recipe
Introduce them in this order:
    1. naive_counting_trap()     selects required categories before filling slots
    2. rigorous_decomposition()  removes invalid groups from the full universe
    3. exhaustive_check()        verifies every four-person candidate group
    4. save_breakdown_figure()   shows how the two restrictions reduce the count

How to read this file:
You already know Python through OOP. Lesson 01 covered pathlib, Agg, and
savefig. Step 3 used math.comb and itertools.combinations for unrestricted
subsets. This script is self-contained and does not import Step 3.

New in this step:
    overcounting trap       5 * 4 * C(7, 2) = 420 exceeds the universe C(9, 4)
    complement counting     valid = all - single-discipline - conflict
    math.comb for C(n, k)   same binomial coefficient as Step 3
    any(...)                True if at least one member belongs to a list
    two interacting rules   mixed-discipline AND not both O1 and D1

main() rejects 420 as larger than the 126-group universe, derives 99 valid
squads by complement, and confirms the count by listing every 4-subset.

Run it:
    uv run en/L06_Counting_Techniques_I/src/counting_04_restrictions.py
"""

# combinations enumerates each 4-subset once. That exhaustive list is the
# ground truth against which both counting arguments are checked.
from itertools import combinations
# math.comb(n, k) is C(n, k). No permutations: groups have no internal roles.
import math
# Path, Agg, and savefig: same unattended-figure idiom as Lesson 01.
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) naive_counting_trap() --------------------------------------------
def naive_counting_trap(n_o: int, n_d: int, k: int) -> int:
    """Return the overcount from filling mandatory categories first.

    Parameters
    ----------
    n_o:
        Number of operations analysts (5).
    n_d:
        Number of data specialists (4).
    k:
        Group size (4).

    Returns
    -------
    int
        n_o * n_d * C(n_o + n_d - 2, k - 2). Here 5 * 4 * C(7, 2) = 420.

    Notes
    -----
    Classic student mistake: "select 1 operations analyst (5 ways), select
    1 data specialist (4 ways), then choose the remaining 2 members from
    the 7 leftover candidates: 5 * 4 * C(7, 2) = 420."

    This overcounts because the "required" operations seat is not a
    distinguished role. A mixed group with 2 operations analysts and 2
    data specialists is generated 2 * 2 = 4 times: either operations
    member could have been the one counted in the factor of 5, and either
    data member in the factor of 4. Groups with 3+1 splits are counted
    three times. 420 is already larger than the entire universe C(9, 4)
    = 126, so the result is impossible even before the conflict rule.
    """
    return n_o * n_d * math.comb((n_o + n_d) - 2, k - 2)
# ------------------------------------------------------------------------------


# --- NEW (2) rigorous_decomposition() -----------------------------------------
def rigorous_decomposition(n_o: int, n_d: int, k: int) -> tuple[int, int, int, int]:
    """Count valid groups by removing invalid subsets from the universe.

    Parameters
    ----------
    n_o, n_d, k:
        Same pool sizes and group size as the trap function.

    Returns
    -------
    tuple[int, int, int, int]
        (universe, mixed_groups, conflict_both, valid_groups).
        Numerically: (126, 120, 21, 99).

    Notes
    -----
    Complement / inclusion of restrictions, not a sequential construction:

        Total universe               = C(9, 4) = 126
        Only operations analysts     = C(5, 4) = 5
        Only data specialists        = C(4, 4) = 1
        Mixed groups                 = 126 - 5 - 1 = 120
        Conflict groups with {O1, D1}:
            Fix O1 and D1, pick 2 from remaining 7 = C(7, 2) = 21
        Total valid squads           = 120 - 21 = 99

    The conflict groups already contain both disciplines, so they sit
    inside the mixed count. Subtracting them from mixed (not from the
    universe a second time after also removing single-discipline groups)
    is the correct complement.

    Two rules interact: "at least one of each discipline" and "not both
    O1 and D1." Applying them as independent sequential choices is what
    produced the trap in naive_counting_trap().
    """
    total_universe = math.comb(n_o + n_d, k)
    only_operations = math.comb(n_o, k)
    only_data = math.comb(n_d, k)
    mixed_groups = total_universe - only_operations - only_data

    # Fix O1 and D1, then choose the remaining k-2 members from the other 7.
    conflict_both = math.comb((n_o + n_d) - 2, k - 2)
    valid_groups = mixed_groups - conflict_both

    return total_universe, mixed_groups, conflict_both, valid_groups
# ------------------------------------------------------------------------------


# --- NEW (3) exhaustive_check() -----------------------------------------------
def exhaustive_check(
    operations_analysts: list[str], data_specialists: list[str], k: int
) -> list[tuple[str, ...]]:
    """Keep every k-subset that satisfies both restrictions.

    Parameters
    ----------
    operations_analysts, data_specialists:
        The two named pools. Concatenated they are the 9-person universe.
    k:
        Group size.

    Returns
    -------
    list[tuple[str, ...]]
        The valid 4-person groups. Length must match valid_groups from
        rigorous_decomposition().

    Notes
    -----
    combinations yields each 4-subset once, so there is no overcounting
    in this loop. any(...) is True if at least one member belongs to the
    given pool. The conflict test is a plain membership check on the
    two named people, not a counting formula.
    """
    # Concatenate the two lists: 5 + 4 = 9 named candidates.
    all_candidates = operations_analysts + data_specialists
    valid_groups = []

    for group in combinations(all_candidates, k):
        # At least one operations analyst and at least one data specialist.
        has_operations = any(member in operations_analysts for member in group)
        has_data = any(member in data_specialists for member in group)
        # Both named people present: the stated conflict.
        conflict = ("O1" in group) and ("D1" in group)

        if has_operations and has_data and not conflict:
            valid_groups.append(group)

    return valid_groups
# ------------------------------------------------------------------------------


# --- NEW (4) save_breakdown_figure() ------------------------------------------
def save_breakdown_figure(universe: int, non_diverse: int, conflict: int, valid: int) -> None:
    """Bar chart of the universe, the two exclusion counts, and the valid remainder.

    Parameters
    ----------
    universe, non_diverse, conflict, valid:
        C(9, 4), the 6 single-discipline groups, the 21 conflict groups,
        and the 99 valid groups. The middle two bars are counts removed,
        not running remainders.

    Returns
    -------
    None
        Side effect: writes counting_04_restrictions.png.

    Notes
    -----
    126 - 6 - 21 = 99. The figure is a four-bar comparison of those
    pieces, not a stacked waterfall whose heights add down the page.
    """
    # \n splits a tick label across two lines so the four categories fit.
    categories = ["All\ngroups", "Single-discipline\nexcluded", "Conflict\nexcluded", "Valid\ngroups"]
    values = [universe, non_diverse, conflict, valid]
    colors = ["#646464", "#EC2661", "#EC2661", "#0039A6"]

    fig, ax = plt.subplots(figsize=(7.5, 4))
    bars = ax.bar(categories, values, color=colors, edgecolor="#1A2E51", linewidth=1.2)
    ax.set_title("Filtering Four-Person Review Groups", fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel("Number of groups", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    output_path = DIR_FIGURES / "counting_04_restrictions.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    """Reject the 420 trap, derive 99 by complement, and confirm by enumeration."""
    operations_analysts = ["O1", "O2", "O3", "O4", "O5"]
    data_specialists = ["D1", "D2", "D3", "D4"]
    k = 4

    naive_error = naive_counting_trap(len(operations_analysts), len(data_specialists), k)
    universe, mixed, conflict, valid_theoretical = rigorous_decomposition(
        len(operations_analysts), len(data_specialists), k
    )

    # 126 mixed-and-pure minus 120 mixed = 6 single-discipline groups.
    single_discipline = universe - mixed
    save_breakdown_figure(universe, single_discipline, conflict, valid_theoretical)

    actual_groups = exhaustive_check(operations_analysts, data_specialists, k)
    actual_total = len(actual_groups)

    print("================================================================")
    print("LESSON 06 - STEP 4: INTERACTING RESTRICTIONS")
    print("================================================================")
    print("Synthetic data notice                : No real company data are used")
    print(
        f"Candidates: {len(operations_analysts)} operations analysts + "
        f"{len(data_specialists)} data specialists = 9; group size k = 4"
    )
    print(f"Total Universe binom(9, 4)           : {universe}")
    print(f"NAIVE FLAWED CALCULATION (The Trap)  : {naive_error}  <-- OVERCOUNTING!")
    print(f"Single-discipline groups excluded    : {single_discipline}")
    print(f"Groups excluded for ('O1', 'D1')     : {conflict}")
    print(f"Theoretical total by complement      : {valid_theoretical}")
    print(f"Exhaustive brute-force count         : {actual_total}")
    print(f"Exact match                          : {valid_theoretical == actual_total}")
    print(f"First 3 valid groups                 : {actual_groups[:3]}")
    print(f"Figure saved to                      : {DIR_FIGURES / 'counting_04_restrictions.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

