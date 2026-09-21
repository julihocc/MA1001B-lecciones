"""
Lesson 02 - Step 3: One-Stage Cluster Sampling
==============================================
NEW IN THIS STEP: draw_cluster_sample(), compare_all_designs(), and
save_cluster_figure().

CHANGES FROM sampling_designs_02_stratified.py
Introduce them in this order:
    1. draw_cluster_sample()   selects facilities, then keeps all their orders
    2. compare_all_designs()   compares unit counts and mean-estimation errors
    3. save_cluster_figure()   shows selected clusters and the design contrast

How to read this file:
You already know Python through OOP. Steps 1-2 built the frame, the SRS, and
the proportional stratified sample. Those functions are copied here so the
script stays self-contained; comments concentrate on the NEW bands.

New in this step:
    sampling clusters       the randomized units are facilities, not orders
    Series.unique / isin    keep every order whose facility was selected
    one-stage design        no second-stage subsample inside a facility
    groupby().mean()        one bar per facility for the cluster figure
    itertuples              print a comparison table without .loc loops
    tuple return            (sample table, list of selected facility IDs)

main() selects four facilities, includes all 2,000 of their orders, and
compares that design with the SRS and stratified samples on one seeded run.
The printed limit line is the pedagogical close: this ranking is not a theorem.

Run it:
    uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_03_cluster.py
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
# First-stage sample size: how many facilities, not how many orders.
CLUSTERS_TO_SELECT = 4
REGION_ORDER = ["North", "Central", "West", "Southeast"]
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic population used throughout the lesson."""
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


def allocate_proportionally(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
) -> pd.Series:
    """Allocate integer sample counts from population stratum shares."""
    counts = population["region"].value_counts().reindex(REGION_ORDER)
    raw_allocation = counts / len(population) * sample_size
    allocation = np.floor(raw_allocation).astype(int)
    remaining = sample_size - int(allocation.sum())
    fractions = (raw_allocation - allocation).sort_values(ascending=False)
    for region in fractions.index[:remaining]:
        allocation.loc[region] += 1
    return allocation


def draw_stratified_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a proportional simple random sample within every region."""
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
    return pd.concat(pieces, ignore_index=True)


# --- NEW (1) draw_cluster_sample() -------------------------------------------
def draw_cluster_sample(
    population: pd.DataFrame,
    clusters_to_select: int = CLUSTERS_TO_SELECT,
    seed: int = SEED,
) -> tuple[pd.DataFrame, list[str]]:
    """Select facilities randomly and include every order in each facility.

    Parameters
    ----------
    population:
        Frame with a facility_id column. Each distinct ID is a cluster.
    clusters_to_select:
        How many facilities to draw. Default 4.
    seed:
        Seed for a NumPy Generator used only for the facility draw.

    Returns
    -------
    tuple[pd.DataFrame, list[str]]
        (sample of all orders in the selected facilities, sorted list of
        those facility IDs). tuple[...] is a type hint: two return values
        packed as one tuple. Python callers unpack with
        sample, selected = draw_cluster_sample(...).

    Notes
    -----
    One-stage cluster sampling randomizes clusters, then takes a census
    of every unit inside each selected cluster. The inclusion chance for
    an order equals the inclusion chance of its facility: 4 / 24 = 16.67%.
    Sample size in orders is then 4 * 500 = 2,000, much larger than the
    SRS, but the 2,000 orders are not 2,000 independent pieces of
    information because they share facility effects.
    """
    # unique() lists each facility once. np.sort makes the choice order
    # independent of DataFrame row order.
    facilities = np.sort(population["facility_id"].unique())
    rng = np.random.default_rng(seed)
    # replace=False: a facility cannot be selected twice. selected is a
    # NumPy array of four ID strings.
    selected = rng.choice(facilities, size=clusters_to_select, replace=False)
    # isin tests membership in that array. .copy() so later edits would
    # not write through to the population table.
    sample = population.loc[population["facility_id"].isin(selected)].copy()
    return sample, sorted(selected.tolist())
# ------------------------------------------------------------------------------


# --- NEW (2) compare_all_designs() -------------------------------------------
def compare_all_designs(
    population: pd.DataFrame,
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
    cluster: pd.DataFrame,
) -> pd.DataFrame:
    """Compare sample size and mean-estimation error across three designs.

    Same list-of-dicts pattern as Step 2, now with a Cluster row. The
    cluster sample is larger in n but may still miss mu by more because
    whole facilities (and their region/facility shifts) enter together.
    """
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for design, sample in [
        ("Simple random", simple_random),
        ("Stratified", stratified),
        ("Cluster", cluster),
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


# --- NEW (3) save_cluster_figure() -------------------------------------------
def save_cluster_figure(
    population: pd.DataFrame,
    selected_facilities: list[str],
    comparison: pd.DataFrame,
) -> Path:
    """Save selected-facility and estimation-error evidence.

    Parameters
    ----------
    population:
        Full frame; used for per-facility means and the population mu line.
    selected_facilities:
        The four IDs returned by draw_cluster_sample().
    comparison:
        Three-row table from compare_all_designs().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: one bar per facility, highlighted if selected, with a
    dashed line at mu. Right panel: the three absolute errors and their
    sample sizes. Reading both panels together is the limit of the lesson:
    a large clustered n can still sit farther from mu than a small SRS.
    """
    output_path = DIR_FIGURES / "sampling_designs_03_cluster.png"
    # groupby("facility_id") splits the frame into 24 groups; .mean() of
    # processing_time_minutes is one number per facility.
    facility_means = population.groupby("facility_id")[
        "processing_time_minutes"
    ].mean()
    # A list comprehension paints selected facilities magenta and the
    # others gray. The order follows facility_means.index.
    colors = [
        "#EC2661" if facility in selected_facilities else "#A7B0BF"
        for facility in facility_means.index
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    axes[0].bar(facility_means.index, facility_means.values, color=colors)
    # axhline draws a horizontal reference at the population mean.
    axes[0].axhline(
        population["processing_time_minutes"].mean(),
        color="#1A2E51",
        linestyle="--",
        linewidth=1.6,
        label="Population mean",
    )
    axes[0].set_ylabel("Facility mean (minutes)")
    axes[0].set_title("Four selected facility clusters")
    axes[0].tick_params(axis="x", rotation=90, labelsize=7)
    axes[0].legend(frameon=False, fontsize=8)

    design_colors = ["#1A2E51", "#0039A6", "#EC2661"]
    axes[1].bar(
        comparison["design"],
        comparison["absolute_error"],
        color=design_colors,
    )
    axes[1].set_ylabel("Absolute error (minutes)")
    axes[1].set_title("Error in this seeded comparison")
    axes[1].tick_params(axis="x", rotation=12)
    axes[1].set_ylim(0, comparison["absolute_error"].max() * 1.28)
    # iterrows() yields (index, Series) pairs. The text sits above each
    # bar with both the error and the sample size.
    for index, row in comparison.iterrows():
        axes[1].text(
            index,
            row["absolute_error"] + 0.04,
            f"{row['absolute_error']:.2f}\nn={int(row['size']):,}",
            ha="center",
            fontsize=8,
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Cluster Sampling Selects Groups, Not Individual Orders",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Draw all three designs and print the seeded comparison, including the limit."""
    population = build_population()
    simple_random = draw_simple_random_sample(population)
    stratified = draw_stratified_sample(population)
    cluster, selected_facilities = draw_cluster_sample(population)
    comparison = compare_all_designs(
        population,
        simple_random,
        stratified,
        cluster,
    )
    figure_path = save_cluster_figure(
        population,
        selected_facilities,
        comparison,
    )
    cluster_row = comparison.loc[comparison["design"] == "Cluster"].iloc[0]
    # unique() of the region column, then a sorted Python list for printing.
    selected_regions = sorted(cluster["region"].unique().tolist())

    print("================================================================")
    print("LESSON 02 - STEP 3: ONE-STAGE CLUSTER SAMPLING")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Facilities in frame             : {FACILITY_COUNT}")
    print(f"Facilities selected             : {', '.join(selected_facilities)}")
    print(f"Orders included                 : {len(cluster):,}")
    print(f"Order inclusion chance          : {CLUSTERS_TO_SELECT / FACILITY_COUNT:.2%}")
    print(f"Regions represented             : {', '.join(selected_regions)}")
    print(f"Cluster mean estimate           : {cluster_row['mean']:.2f} min")
    print(f"Cluster absolute error          : {cluster_row['absolute_error']:.2f} min")
    print("----------------------------------------------------------------")
    # itertuples(index=False) yields named tuples of the comparison rows.
    # row.design, row.size, row.mean, row.absolute_error are attributes.
    for row in comparison.itertuples(index=False):
        print(
            f"{row.design:<14} n={row.size:>4,}, "
            f"mean={row.mean:>5.2f}, error={row.absolute_error:.2f} min"
        )
    print("----------------------------------------------------------------")
    print("Limit: this seeded result is not a universal ranking of designs.")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

