"""
Lesson 07 - Step 3: Stars and Bars, Then the Probability Limit
==============================================================
NEW IN THIS STEP: enumerate_occupancy_profiles(), multinomial_probability(),
simulate_profile_probabilities(), and save_probability_limit_figure().

Changes from allocations_02_multinomial_categories.py
The Recipe
----------
Introduce these changes in order:
    1. enumerate_occupancy_profiles() counts nonnegative allocation profiles
    2. multinomial_probability()      weights a profile under random routing
    3. simulate_profile_probabilities() verifies probabilities with seed 42
    4. save_probability_limit_figure() contrasts counting and probability

How to read this file:
You already know Python through OOP. Steps 1-2 counted sequences and labeled
allocations with a multinomial coefficient. This step counts *occupancy
profiles* (how many units each of four centers receives) and then shows that
counting profiles does not make them equally likely.

New in this step:
    math.comb(n, k)          binomial coefficient C(n, k)
    itertools.product        Cartesian power: all 4-tuples of 0..8
    stars and bars           C(n+k-1, k-1) nonnegative integer solutions
    rng.multinomial          simulate n independent categorical assignments
    np.all(..., axis=1)      which simulated rows match a target profile

main() enumerates 165 occupancy profiles, computes exact multinomial
probabilities for three of them, estimates those probabilities with 500,000
seed-42 draws, and contrasts both with the incorrect 1/165 shortcut.

Run from the repository root:
    uv run en/L07_Counting_Techniques_II/src/
    allocations_03_star_bars_probability_limit.py
"""

from collections import Counter
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
QUEUE_COUNTS = {"Priority": 3, "Standard": 3, "Audit": 2}
REQUESTS = tuple(f"R{i:02d}" for i in range(1, 9))
TOTAL_REQUESTS = 8
SERVICE_CENTERS = 4
SIMULATIONS = 500_000
SEED = 42
# Three occupancy 4-tuples used in the figure. (5,1,1,1) is more "lopsided"
# than (3,2,2,1) and therefore less likely under uniform independent routing.
SELECTED_PROFILES = ((5, 1, 1, 1), (4, 2, 1, 1), (3, 2, 2, 1))
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


def repeated_permutation_count(counts: tuple[int, ...]) -> int:
    """Return the number of distinct sequences with repeated labels."""
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


def enumerate_labeled_allocations() -> list[dict[str, tuple[str, ...]]]:
    """Assign eight labeled requests to three labeled queues of fixed sizes."""
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


def first_request_counts(
    allocations: list[dict[str, tuple[str, ...]]],
) -> Counter[str]:
    """Count the queue containing R01 across every valid allocation."""
    counts: Counter[str] = Counter()
    for allocation in allocations:
        for queue, requests in allocation.items():
            if REQUESTS[0] in requests:
                counts[queue] += 1
                break
    return counts


# --- NEW (1) enumerate_occupancy_profiles() ---------------------------------
def enumerate_occupancy_profiles(
    total: int,
    categories: int,
) -> list[tuple[int, ...]]:
    """Enumerate all ordered nonnegative profiles summing to total.

    Parameters
    ----------
    total:
        Number of indistinguishable units to place (8 requests).
    categories:
        Number of labeled centers (4).

    Returns
    -------
    list[tuple[int, ...]]
        Every ordered 4-tuple of integers in 0..8 whose entries sum to 8,
        for example (8,0,0,0) and (2,2,2,2). Order matters: (5,1,1,1) is
        a different profile from (1,5,1,1) because the centers are labeled.

    Notes
    -----
    product(range(9), repeat=4) is the Cartesian power {0,...,8}^4: 9^4
    = 6561 tuples. The comprehension keeps only those that sum to 8.
    That filtered list has length C(8+4-1, 4-1) = C(11,3) = 165, which
    is the stars-and-bars count of nonnegative integer solutions.
    """
    return [
        profile
        for profile in product(range(total + 1), repeat=categories)
        if sum(profile) == total
    ]


# -----------------------------------------------------------------------------


# --- NEW (2) multinomial_probability() --------------------------------------
def multinomial_probability(profile: tuple[int, ...]) -> float:
    """Return the exact probability under independent uniform routing.

    Parameters
    ----------
    profile:
        Occupancy counts (n1, n2, n3, n4) with sum ni = 8.

    Returns
    -------
    float
        [8! / (n1! n2! n3! n4!)] * (1/4)^8.

    Notes
    -----
    Each request independently picks one of four centers with probability
    1/4. The multinomial coefficient counts the sequences that produce
    this occupancy. Lopsided profiles have smaller coefficients, so they
    are not as likely as balanced ones. Counting 165 profiles therefore
    does not make P(profile) = 1/165.
    """
    multiplicity = repeated_permutation_count(profile)
    return multiplicity * (1 / len(profile)) ** sum(profile)


# -----------------------------------------------------------------------------


# --- NEW (3) simulate_profile_probabilities() -------------------------------
def simulate_profile_probabilities(
    profiles: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], float]:
    """Estimate selected occupancy probabilities with deterministic RNG.

    Parameters
    ----------
    profiles:
        The three occupancy tuples to score.

    Returns
    -------
    dict[tuple[int, ...], float]
        Simulated relative frequency of each profile among SIMULATIONS
        independent multinomial draws, seed 42.

    Notes
    -----
    rng.multinomial(n, p, size=N) draws N independent count-vectors, each
    the result of n categorical trials with probabilities p. Here n=8,
    p=(1/4,1/4,1/4,1/4), N=500,000. draws has shape (500000, 4).
    np.all(draws == profile, axis=1) is a length-N boolean: True when
    that row equals the target 4-tuple. The mean of those 0/1 values is
    the estimated probability.
    """
    rng = np.random.default_rng(SEED)
    draws = rng.multinomial(
        TOTAL_REQUESTS,
        [1 / SERVICE_CENTERS] * SERVICE_CENTERS,
        size=SIMULATIONS,
    )
    return {
        profile: float(np.mean(np.all(draws == profile, axis=1)))
        for profile in profiles
    }


# -----------------------------------------------------------------------------


# --- NEW (4) save_probability_limit_figure() --------------------------------
def save_probability_limit_figure(
    uniform_profile_probability: float,
    exact_probabilities: dict[tuple[int, ...], float],
    simulated_probabilities: dict[tuple[int, ...], float],
) -> Path:
    """Export incorrect uniform, exact, and simulated profile probabilities.

    Three grouped bars per selected profile: the false 1/165 shortcut,
    the exact multinomial probability, and the seed-42 simulation. The
    pink bars are equal; the blue/navy bars are not, which is the limit.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "allocations_03_star_bars_probability_limit.png"

    x = np.arange(len(SELECTED_PROFILES))
    width = 0.25
    uniform_values = [uniform_profile_probability] * len(SELECTED_PROFILES)
    exact_values = [exact_probabilities[item] for item in SELECTED_PROFILES]
    simulated_values = [
        simulated_probabilities[item] for item in SELECTED_PROFILES
    ]

    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    ax.bar(
        x - width,
        uniform_values,
        width,
        label="Incorrect: $1/165$",
        color=TEC_PINK,
    )
    ax.bar(
        x,
        exact_values,
        width,
        label="Exact multinomial",
        color=TEC_BLUE,
    )
    ax.bar(
        x + width,
        simulated_values,
        width,
        label="Simulation (seed 42)",
        color=TEC_NAVY,
    )
    ax.set_xticks(x, [str(profile) for profile in SELECTED_PROFILES])
    ax.set_xlabel("Ordered occupancy profile across four centers")
    ax.set_ylabel("Probability")
    ax.set_title(
        "Counting Profiles Does Not Make Them Equally Likely",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 3 evidence."""
    profiles = enumerate_occupancy_profiles(TOTAL_REQUESTS, SERVICE_CENTERS)
    # C(n + k - 1, k - 1) nonnegative integer solutions of x1+...+xk = n.
    stars_and_bars_count = comb(
        TOTAL_REQUESTS + SERVICE_CENTERS - 1,
        SERVICE_CENTERS - 1,
    )
    uniform_profile_probability = 1 / stars_and_bars_count
    exact_probabilities = {
        profile: multinomial_probability(profile)
        for profile in SELECTED_PROFILES
    }
    simulated_probabilities = simulate_profile_probabilities(SELECTED_PROFILES)
    output_path = save_probability_limit_figure(
        uniform_profile_probability,
        exact_probabilities,
        simulated_probabilities,
    )

    print("LESSON 07 - STEP 3: STARS AND BARS, THEN THE PROBABILITY LIMIT")
    print(f"Requests / allocation units       : {TOTAL_REQUESTS}")
    print(f"Labeled service centers           : {SERVICE_CENTERS}")
    print(f"Stars-and-bars formula             : {stars_and_bars_count:,}")
    print(f"Occupancy profiles enumerated      : {len(profiles):,}")
    print(f"Incorrect equal-profile probability: {uniform_profile_probability:.8f}")
    print(f"Simulations with seed {SEED:<2}          : {SIMULATIONS:,}")
    for profile in SELECTED_PROFILES:
        print(
            f"Profile {profile}: exact={exact_probabilities[profile]:.8f}, "
            f"simulated={simulated_probabilities[profile]:.8f}"
        )
    print(f"Figure saved to                    : {output_path}")


if __name__ == "__main__":
    main()

