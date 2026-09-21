"""
Lesson 02 - Step 2: Proportional Stratified Sampling
====================================================
NEW IN THIS STEP: allocate_proportionally(), draw_stratified_sample(),
compare_designs(), and save_stratified_figure().

CHANGES FROM sampling_designs_01_simple_random.py
Introduce them in this order:
    1. allocate_proportionally()  assigns the sample across all regions
    2. draw_stratified_sample()   draws an SRS within every region
    3. compare_designs()          compares sample composition and mean error
    4. save_stratified_figure()   visualizes representation and estimation

How to read this file:
You already know Python through OOP. Step 1 built the facility/region frame
and drew an SRS. That generator is copied here so the script stays
self-contained; it is commented only where this file does something new.

New in this step:
    proportional allocation   n_h = round(N_h / N * n), then leftover seats
    np.floor + remainder      largest-remainder method for integer counts
    independent SRS per stratum   pandas .sample inside a region filter
    pd.concat                 stack the four stratum samples into one table
    seed + index              a distinct random_state in each stratum

main() allocates 60 orders to each equally sized region, draws the stratified
sample, and compares its error with the Step 1 SRS on the same population.

Run it:
    uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_02_stratified.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
FACILITY_COUNT = 24
ORDERS_PER_FACILITY = 500
POPULATION_SIZE = FACILITY_COUNT * ORDERS_PER_FACILITY
SAMPLE_SIZE = 240
REGION_ORDER = ["North", "Central", "West", "Southeast"]
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic population introduced in Step 1.

    The generator, seed, and columns are identical so the two scripts
    describe one world. See Step 1 for np.repeat / np.tile commentary.
    """
    rng = np.random.default_rng(seed)
    facility_numbers = np.arange(FACILITY_COUNT)
    facility_ids = np.array([f"F{number + 1:02d}" for number in facility_numbers])
    facility_region = np.repeat(REGION_ORDER, FACILITY_COUNT // len(REGION_ORDER))
    facility_effect = np.tile(np.array([-8.0, -5.0, -2.0, 0.0, 3.0, 7.0]), 4)
    region_effect = {
        "North": -4.0,
        "Central": 0.0,
        "West": 3.0,
        "Southeast": 7.0,
    }
    facility_index = np.repeat(facility_numbers, ORDERS_PER_FACILITY)
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)
    noise = rng.normal(loc=0.0, scale=6.0, size=POPULATION_SIZE)
    region_component = np.array(
        [region_effect[facility_region[index]] for index in facility_index]
    )
    processing_time = np.clip(
        42.0
        + region_component
        + facility_effect[facility_index]
        + 1.2 * items
        + noise,
        8.0,
        None,
    )
    return pd.DataFrame(
        {
            "order_id": np.arange(200_001, 200_001 + POPULATION_SIZE),
            "facility_id": facility_ids[facility_index],
            "region": facility_region[facility_index],
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )


def draw_simple_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw the simple random sample introduced in Step 1."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


# --- NEW (1) allocate_proportionally() ---------------------------------------
def allocate_proportionally(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
) -> pd.Series:
    """Allocate integer sample counts from population stratum shares.

    Parameters
    ----------
    population:
        Frame with a region column. Each distinct region is a stratum.
    sample_size:
        Total number of orders to allocate across strata (240).

    Returns
    -------
    pd.Series
        Index = region name in REGION_ORDER. Values = integer n_h that
        sum exactly to sample_size.

    Notes
    -----
    Proportional allocation wants n_h / n = N_h / N. Those products are
    usually not integers, so the function floors each quota and then
    gives the leftover seats to the strata with the largest leftover
    fractions (Hamilton / largest-remainder method). In this synthetic
    frame the four regions are equal, so the result is 60, 60, 60, 60.
    """
    counts = population["region"].value_counts().reindex(REGION_ORDER)
    # Raw (possibly fractional) quotas: N_h / N * n.
    raw_allocation = counts / len(population) * sample_size
    # Drop the fraction; each stratum starts with the integer part.
    allocation = np.floor(raw_allocation).astype(int)
    remaining = sample_size - int(allocation.sum())
    # Largest leftover fraction first. index[:remaining] takes that many
    # region names; each of those strata gains one extra order.
    fractions = (raw_allocation - allocation).sort_values(ascending=False)
    for region in fractions.index[:remaining]:
        allocation.loc[region] += 1
    return allocation
# ------------------------------------------------------------------------------


# --- NEW (2) draw_stratified_sample() ----------------------------------------
def draw_stratified_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a proportional simple random sample within every region.

    Parameters
    ----------
    population:
        Full frame. Sampling happens independently inside each region.
    sample_size:
        Total n; split across regions by allocate_proportionally().
    seed:
        Base integer. Stratum k uses random_state = seed + k so the four
        draws are reproducible and not identical copies of one stream.

    Returns
    -------
    pd.DataFrame
        Concatenated stratum samples, ignore_index=True so the row index
        is 0 .. n-1 rather than four recycled copies of the original
        frame index.

    Notes
    -----
    The randomized units are still orders. Regions are partitions of the
    frame, not the things being selected. Every region is guaranteed to
    appear because each receives a positive allocation.
    """
    allocation = allocate_proportionally(population, sample_size)
    pieces = []
    for index, region in enumerate(REGION_ORDER):
        stratum = population.loc[population["region"] == region]
        pieces.append(
            stratum.sample(
                n=int(allocation.loc[region]),
                replace=False,
                random_state=seed + index,
            )
        )
    # concat stacks the four small tables vertically into one sample.
    return pd.concat(pieces, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NEW (3) compare_designs() -----------------------------------------------
def compare_designs(
    population: pd.DataFrame,
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
) -> pd.DataFrame:
    """Compare the two sample means with the population parameter.

    Returns a two-row table (Simple random, Stratified) with size, mean,
    and absolute_error. Same list-of-dicts pattern as Lesson 01 Step 3.
    """
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for design, sample in [
        ("Simple random", simple_random),
        ("Stratified", stratified),
    ]:
        sample_mean = sample[variable].mean()
        rows.append(
            {
                "design": design,
                "size": len(sample),
                "mean": sample_mean,
                "absolute_error": abs(sample_mean - population_mean),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (4) save_stratified_figure() ----------------------------------------
def save_stratified_figure(
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
    comparison: pd.DataFrame,
) -> Path:
    """Save representation and error evidence for two probability designs.

    Left panel: grouped bars of how many orders each design took from
    each region. Stratification is flat at 60; SRS is not. Right panel:
    absolute errors for this seeded run, with the numeric value labeled
    above each bar. Side effect: writes the PNG.
    """
    output_path = DIR_FIGURES / "sampling_designs_02_stratified.png"
    simple_counts = simple_random["region"].value_counts().reindex(REGION_ORDER)
    stratified_counts = stratified["region"].value_counts().reindex(REGION_ORDER)

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1))
    positions = np.arange(len(REGION_ORDER))
    width = 0.36
    axes[0].bar(
        positions - width / 2,
        simple_counts,
        width,
        color="#1A2E51",
        label="Simple random",
    )
    axes[0].bar(
        positions + width / 2,
        stratified_counts,
        width,
        color="#EC2661",
        label="Stratified",
    )
    axes[0].set_xticks(positions, REGION_ORDER, rotation=15)
    axes[0].set_ylabel("Sampled orders")
    axes[0].set_title("Region representation")
    axes[0].legend(frameon=False)

    axes[1].bar(
        comparison["design"],
        comparison["absolute_error"],
        color=["#1A2E51", "#EC2661"],
    )
    axes[1].set_ylabel("Absolute error (minutes)")
    axes[1].set_title("Error in this seeded sample")
    # 1.25 * max error leaves room for the numeric labels above the bars.
    axes[1].set_ylim(0, comparison["absolute_error"].max() * 1.25)
    for index, value in enumerate(comparison["absolute_error"]):
        axes[1].text(index, value + 0.02, f"{value:.2f}", ha="center")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Stratification Guarantees Representation of Every Region",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Allocate, draw, compare, and print the verified stratified results."""
    population = build_population()
    simple_random = draw_simple_random_sample(population)
    stratified = draw_stratified_sample(population)
    allocation = allocate_proportionally(population)
    comparison = compare_designs(population, simple_random, stratified)
    figure_path = save_stratified_figure(simple_random, stratified, comparison)

    population_mean = population["processing_time_minutes"].mean()
    simple_row = comparison.loc[comparison["design"] == "Simple random"].iloc[0]
    stratified_row = comparison.loc[comparison["design"] == "Stratified"].iloc[0]

    print("================================================================")
    print("LESSON 02 - STEP 2: PROPORTIONAL STRATIFIED SAMPLING")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Population mean parameter       : {population_mean:.2f} min")
    print("Allocation by region            : " + ", ".join(
        f"{region}={int(allocation[region])}" for region in REGION_ORDER
    ))
    print(f"SRS mean / absolute error       : {simple_row['mean']:.2f} / "
          f"{simple_row['absolute_error']:.2f} min")
    print(f"Stratified mean / abs. error    : {stratified_row['mean']:.2f} / "
          f"{stratified_row['absolute_error']:.2f} min")
    print("All regions represented         : True")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

