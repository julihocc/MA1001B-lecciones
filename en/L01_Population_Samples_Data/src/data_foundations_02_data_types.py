"""
Lesson 01 - Step 2: Business Data Types
========================================
NEW IN THIS STEP: add_business_variables(), classify_variables(), and
save_data_types_figure().

CHANGES FROM data_foundations_01_population_sample.py
Introduce them in this order:
    1. add_business_variables()    adds region and order value
    2. classify_variables()        separates roles from storage types
    3. save_data_types_figure()    compares categorical, discrete, continuous

How to read this file:
You already know Python through OOP. Step 1 introduced pathlib, NumPy, pandas,
the Agg backend, the seeded Generator, DataFrame.sample, and unattended
savefig. Those pieces are rebuilt here so the script stays self-contained;
they are commented only where this file does something new.

New in this step:
    DataFrame.copy()     protect the caller's table from in-place edits
    rng.gamma            a right-skewed continuous draw for unit value
    dict[str, str]       a type hint: keys are strings, values are strings
    Series.value_counts  tally how often each category or integer appears
    Series.reindex       force a bar chart to a chosen category order
    plt.subplots(1, 3)   three Axes side by side on one Figure

main() rebuilds the Step 1 population, attaches region and order value,
prints each variable's analytical role, and saves a three-panel figure.

Run it:
    python data_foundations_02_data_types.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Step 1: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POPULATION_SIZE = 12_000
SAMPLE_SIZE = 200
# Same path construction as Step 1: figures/ next to this package, not cwd.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the Step 1 register, then attach the Step 2 variables.

    The channel / items / processing-time generator is identical to Step 1
    so the two scripts describe the same synthetic world. After that table
    exists, this Step 2 version calls add_business_variables() before
    returning.

    Parameters
    ----------
    seed:
        Shared integer so Steps 1-3 rebuild the same 12,000 orders.

    Returns
    -------
    pd.DataFrame
        Step 1 columns plus region and order_value_mxn.
    """
    rng = np.random.default_rng(seed)
    channels = rng.choice(
        ["Retail", "Web", "Partner"],
        size=POPULATION_SIZE,
        p=[0.45, 0.35, 0.20],
    )
    channel_effect = pd.Series(channels).map(
        {"Retail": 6.0, "Web": -5.0, "Partner": 2.0}
    )
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)
    noise = rng.normal(loc=0.0, scale=7.0, size=POPULATION_SIZE)
    processing_time = np.clip(
        38.0 + channel_effect.to_numpy() + 1.4 * items + noise,
        8.0,
        None,
    )
    population = pd.DataFrame(
        {
            "order_id": np.arange(100_001, 100_001 + POPULATION_SIZE),
            "channel": channels,
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )
    # The same rng object continues here, so region and order value consume
    # the next numbers in the seed-42 stream rather than restarting it.
    return add_business_variables(population, rng)


def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw the same simple random sample introduced in Step 1."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


# --- NEW (1) add_business_variables() ----------------------------------------
def add_business_variables(
    population: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Add one categorical and one continuous business variable.

    Parameters
    ----------
    population:
        The Step 1 register (order_id, channel, items, processing time).
    rng:
        The Generator already used to build that register. Passing the
        same object (instead of calling default_rng(SEED) again) keeps
        the extra columns in the same random stream.

    Returns
    -------
    pd.DataFrame
        A copy of population with two new columns: region (categorical)
        and order_value_mxn (quantitative continuous).

    Notes
    -----
    np.random.Generator in the type hint names the class of rng. You do
    not construct that class yourself; default_rng(...) returns it.
    """
    # copy() allocates a new table. Without it, result["region"] = ... would
    # also write into the caller's DataFrame, which is a common pandas trap.
    result = population.copy()

    # Three operating regions with unequal shares. The probabilities 0.30,
    # 0.45, 0.25 sum to 1. len(result) is the number of rows, so every order
    # receives exactly one region label.
    result["region"] = rng.choice(
        ["North", "Central", "South"],
        size=len(result),
        p=[0.30, 0.45, 0.25],
    )

    # gamma(shape=3.0, scale=180.0) draws a right-skewed positive number:
    # most unit values cluster lower, a long tail produces a few expensive
    # items. Mean of a Gamma(shape, scale) is shape * scale = 540, but we
    # do not need that fact to run the lesson. Multiplying by items_per_order
    # makes larger baskets tend to cost more. .round(2) stores centavos.
    unit_value = rng.gamma(shape=3.0, scale=180.0, size=len(result))
    result["order_value_mxn"] = (
        unit_value * result["items_per_order"]
    ).round(2)
    return result
# ------------------------------------------------------------------------------


# --- NEW (2) classify_variables() --------------------------------------------
def classify_variables() -> dict[str, str]:
    """Return each variable's analytical role in the lesson.

    Returns
    -------
    dict[str, str]
        Keys are column names. Values are role labels used in the console
        report. dict[str, str] is a type hint: both keys and values are
        strings. Python 3.9+ allows this builtin-generic spelling; you do
        not need to import typing.Dict.

    Notes
    -----
    These roles are about meaning, not about how pandas stores the column.
    order_id is stored as integers, but arithmetic on an ID has no business
    interpretation, so its role is categorical (an identifier).
    """
    return {
        "order_id": "Identifier (categorical role)",
        "channel": "Categorical",
        "region": "Categorical",
        "items_per_order": "Quantitative discrete",
        "processing_time_minutes": "Quantitative continuous",
        "order_value_mxn": "Quantitative continuous",
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_data_types_figure() ----------------------------------------
def save_data_types_figure(sample: pd.DataFrame) -> Path:
    """Save examples of categorical, discrete, and continuous variables.

    Parameters
    ----------
    sample:
        The 200-row random sample. Using the sample (not the population)
        keeps the panels readable and matches what an analyst would see.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Panel 0 is a bar chart of named categories. Panel 1 is a bar chart of
    integer counts (discrete). Panel 2 is a histogram of a measurement
    (continuous). The visual contrast is the point of the figure.
    """
    output_path = DIR_FIGURES / "data_foundations_02_data_types.png"
    colors = ["#0039A6", "#EC2661", "#646464"]
    # 1 row, 3 columns of Axes. axes is a length-3 NumPy array of Axes,
    # so axes[0], axes[1], axes[2] are the left, middle, and right panels.
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.8))

    # value_counts() returns a Series: index = category, value = how many
    # rows. Without reindex, pandas would order bars by frequency (largest
    # first). reindex([...]) forces Retail, Web, Partner from left to right
    # so the legend of the data-generating process stays visible.
    channel_counts = sample["channel"].value_counts().reindex(
        ["Retail", "Web", "Partner"]
    )
    # .index holds the labels; .values holds the heights.
    axes[0].bar(channel_counts.index, channel_counts.values, color=colors)
    axes[0].set_title("Categorical")
    axes[0].set_ylabel("Orders")
    # rotation=20 tilts the tick labels so "Partner" is not clipped.
    axes[0].tick_params(axis="x", rotation=20)

    # sort_index() puts 1, 2, 3, ... items on the horizontal axis in numeric
    # order. A bar (not a histogram) is the right mark for a discrete count:
    # 3.5 items is not a possible value, so there should be a gap between
    # integer ticks rather than a filled area.
    item_counts = sample["items_per_order"].value_counts().sort_index()
    axes[1].bar(item_counts.index, item_counts.values, color="#0039A6")
    axes[1].set_title("Quantitative discrete")
    axes[1].set_xlabel("Items per order")

    # A histogram is appropriate once the variable can take any value in an
    # interval. bins=14 is a display choice, not a statistical estimator.
    axes[2].hist(
        sample["processing_time_minutes"],
        bins=14,
        color="#EC2661",
        alpha=0.85,
    )
    axes[2].set_title("Quantitative continuous")
    axes[2].set_xlabel("Processing time")

    # The same light horizontal grid on every panel. axes is iterable, so
    # this loop is ordinary Python over the three Axes objects.
    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("One Sample, Three Analytical Data Types", fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Classify the sample variables and write the three-panel figure."""
    population = build_population()
    sample = draw_random_sample(population)
    variable_roles = classify_variables()
    figure_path = save_data_types_figure(sample)

    print("================================================================")
    print("LESSON 01 - STEP 2: BUSINESS DATA TYPES")
    print("================================================================")
    print("Synthetic data notice: No real company data are used")
    # .items() yields (key, value) pairs. <28 left-aligns the column name
    # in a 28-character field so the roles line up in the console.
    for variable, role in variable_roles.items():
        print(f"{variable:<28}: {role}")
    print("----------------------------------------------------------------")
    print("Caution: order_id contains numbers but acts as a label.")
    print(f"Sample rows                     : {len(sample):,}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

