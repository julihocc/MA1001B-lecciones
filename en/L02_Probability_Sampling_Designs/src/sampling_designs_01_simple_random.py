"""
Lesson 02 - Step 1: Simple Random Sampling
==========================================
NEW IN THIS STEP: build_population(), draw_simple_random_sample(),
summarize_sample(), and save_figure().

Context:
A fully synthetic operations register contains every order handled by 24
facilities during one planning period. The complete register is the sampling
frame. A simple random sample gives every possible sample of 240 orders the
same chance of selection.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy,
pandas, the Agg backend, DataFrame.sample, and unattended savefig. Those
idioms return here with a short pointer, not a second treatise.

New in this step:
    np.repeat / np.tile   expand facility labels and effects to every order
    f"{n:02d}"            zero-padded facility IDs such as F01, F24
    inclusion probability n / N, the chance that any one order is selected
    grouped bar chart     two bars per region using numeric x positions
    value_counts(normalize=True)  convert counts into shares that sum to 1
    format spec .2%       print 0.02 as 2.00%

main() builds the frame, draws one SRS of 240 orders, reports mu, x-bar,
absolute error, and the equal inclusion chance, and writes the evidence figure.

Run it:
    uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_01_simple_random.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
FACILITY_COUNT = 24
ORDERS_PER_FACILITY = 500
# 24 * 500 = 12,000 orders: a complete sampling frame, not a sample.
POPULATION_SIZE = FACILITY_COUNT * ORDERS_PER_FACILITY
SAMPLE_SIZE = 240
# Fixed display and generation order so North, Central, West, Southeast always
# appear left to right. Six facilities belong to each region.
REGION_ORDER = ["North", "Central", "West", "Southeast"]
# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_population() ----------------------------------------------
def build_population(seed: int = SEED) -> pd.DataFrame:
    """Build a fully synthetic population with region and facility structure.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's Generator so Steps 2 and 3 rebuild
        the same 12,000 orders. Default is the module-level SEED.

    Returns
    -------
    pd.DataFrame
        One row per order. Columns: order_id, facility_id, region,
        items_per_order, processing_time_minutes.

    Notes
    -----
    Processing time has four additive pieces: a 42-minute baseline, a region
    shift, a facility shift (the cluster effect), 1.2 minutes per item, and
    Normal noise. Orders in the same facility therefore share a mean shift.
    That shared shift is why cluster sampling in Step 3 is not the same as
    drawing 2,000 independent orders.
    """
    rng = np.random.default_rng(seed)
    # 0, 1, ..., 23. These integers index the facility arrays below.
    facility_numbers = np.arange(FACILITY_COUNT)
    # :02d means "print as a two-digit integer with a leading zero".
    # Facility 0 becomes F01; facility 23 becomes F24.
    facility_ids = np.array([f"F{number + 1:02d}" for number in facility_numbers])
    # np.repeat(list, k) repeats EACH element k times in order.
    # Six facilities per region: F01-F06 North, F07-F12 Central, and so on.
    facility_region = np.repeat(REGION_ORDER, FACILITY_COUNT // len(REGION_ORDER))
    # np.tile(array, k) concatenates the WHOLE array k times. The six facility
    # shifts therefore recur in every region: one slow facility, one fast, etc.
    facility_effect = np.tile(np.array([-8.0, -5.0, -2.0, 0.0, 3.0, 7.0]), 4)
    region_effect = {
        "North": -4.0,
        "Central": 0.0,
        "West": 3.0,
        "Southeast": 7.0,
    }

    # Repeat each facility index 500 times so every order knows its facility.
    # Length is 12,000: [0,0,...,0, 1,1,...,1, ..., 23,23,...,23].
    facility_index = np.repeat(facility_numbers, ORDERS_PER_FACILITY)
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)
    noise = rng.normal(loc=0.0, scale=6.0, size=POPULATION_SIZE)
    # A list comprehension looks up the region shift for each order's facility.
    # Wrapping in np.array makes it addable to the other numeric arrays.
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
# ------------------------------------------------------------------------------


# --- NEW (2) draw_simple_random_sample() -------------------------------------
def draw_simple_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a simple random sample of orders without replacement.

    Parameters
    ----------
    population:
        The complete sampling frame.
    sample_size:
        Number of distinct orders to keep. Default 240.
    seed:
        pandas random_state so the same 240 rows are selected every run.

    Returns
    -------
    pd.DataFrame
        sample_size rows; the frame itself is not modified.

    Notes
    -----
    Every subset of 240 distinct orders is equally likely. That is the
    definition of a simple random sample of size n from a finite frame.
    """
    return population.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NEW (3) summarize_sample() ----------------------------------------------
def summarize_sample(
    population: pd.DataFrame,
    sample: pd.DataFrame,
) -> dict[str, float]:
    """Return the parameter, estimate, error, and inclusion probability.

    Parameters
    ----------
    population, sample:
        Frame and SRS; both must contain processing_time_minutes.

    Returns
    -------
    dict[str, float]
        population_mean (mu), sample_mean (x-bar), absolute_error, and
        inclusion_probability = n / N. For SRS without replacement, that
        ratio is also the chance that any specific order is selected.
    """
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    sample_mean = sample[variable].mean()
    return {
        "population_mean": population_mean,
        "sample_mean": sample_mean,
        "absolute_error": abs(sample_mean - population_mean),
        "inclusion_probability": len(sample) / len(population),
    }
# ------------------------------------------------------------------------------


# --- NEW (4) save_figure() ----------------------------------------------------
def save_figure(population: pd.DataFrame, sample: pd.DataFrame) -> Path:
    """Save SRS composition and distribution evidence without a window.

    Parameters
    ----------
    population, sample:
        Frame and SRS used for the two-panel figure.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: grouped bars compare each region's share in the frame with
    its share in the SRS. An SRS does not force those shares to match.
    Right panel: density histograms, same idea as Lesson 01 Step 1.
    """
    output_path = DIR_FIGURES / "sampling_designs_01_simple_random.png"
    bins = np.linspace(
        population["processing_time_minutes"].min(),
        population["processing_time_minutes"].max(),
        28,
    )
    # normalize=True turns counts into proportions that sum to 1. reindex
    # forces REGION_ORDER so the bars line up with the x-tick labels.
    population_share = (
        population["region"].value_counts(normalize=True).reindex(REGION_ORDER)
    )
    sample_share = sample["region"].value_counts(normalize=True).reindex(REGION_ORDER)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.1))
    # Numeric x positions 0, 1, 2, 3, one per region. width=0.36 leaves a
    # gap; subtracting/adding width/2 places the two bars side by side
    # around each integer tick.
    positions = np.arange(len(REGION_ORDER))
    width = 0.36
    axes[0].bar(
        positions - width / 2,
        population_share * 100,
        width,
        color="#1A2E51",
        label="Population",
    )
    axes[0].bar(
        positions + width / 2,
        sample_share * 100,
        width,
        color="#EC2661",
        label="SRS",
    )
    # set_xticks(positions, labels) places a named tick at each integer.
    axes[0].set_xticks(positions, REGION_ORDER, rotation=15)
    axes[0].set_ylabel("Share of orders (%)")
    axes[0].set_title("Region composition")
    axes[0].legend(frameon=False)

    axes[1].hist(
        population["processing_time_minutes"],
        bins=bins,
        density=True,
        alpha=0.55,
        color="#1A2E51",
        label="Population",
    )
    axes[1].hist(
        sample["processing_time_minutes"],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=2.2,
        color="#EC2661",
        label="SRS",
    )
    axes[1].set_xlabel("Processing time (minutes)")
    axes[1].set_ylabel("Density")
    axes[1].set_title("Processing-time distribution")
    axes[1].legend(frameon=False)

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Simple Random Sample from a Complete Frame", fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Draw one SRS, print the verified numbers, and save the figure."""
    population = build_population()
    sample = draw_simple_random_sample(population)
    summary = summarize_sample(population, sample)
    figure_path = save_figure(population, sample)
    region_counts = sample["region"].value_counts().reindex(REGION_ORDER)

    print("================================================================")
    print("LESSON 02 - STEP 1: SIMPLE RANDOM SAMPLING")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sampling-frame size (N)         : {len(population):,}")
    print(f"Simple random sample size (n)   : {len(sample):,}")
    print(
        "Equal order inclusion chance   : "
        f"{summary['inclusion_probability']:.2%}"
    )
    print(f"Population mean parameter       : {summary['population_mean']:.2f} min")
    print(f"SRS mean estimate               : {summary['sample_mean']:.2f} min")
    print(f"SRS absolute error              : {summary['absolute_error']:.2f} min")
    # join turns the four "North=63" pieces into one comma-separated line.
    print("SRS orders by region            : " + ", ".join(
        f"{region}={int(region_counts[region])}" for region in REGION_ORDER
    ))
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

