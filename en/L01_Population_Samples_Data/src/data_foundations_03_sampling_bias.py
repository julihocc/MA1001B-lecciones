"""
Lesson 01 - Step 3: Sample Size Does Not Remove Selection Bias
===============================================================
NEW IN THIS STEP: draw_convenience_sample(), compare_estimates(), and
save_bias_figure().

CHANGES FROM data_foundations_02_data_types.py
Introduce them in this order:
    1. draw_convenience_sample()  selects only easily available Web orders
    2. compare_estimates()        measures error against the population mean
    3. save_bias_figure()         contrasts sample size and estimation error

How to read this file:
You already know Python through OOP. Steps 1-2 introduced the synthetic
register, pathlib, NumPy, pandas, Agg, DataFrame.sample, copy, gamma draws,
value_counts, and unattended savefig. Those pieces are rebuilt here so the
script stays self-contained; they are commented only where this file does
something new.

New in this step:
    Boolean column filter   population.loc[population["channel"] == "Web"]
    DataFrame.head(n)       take the first n rows in current order
    raise ValueError        fail loudly if the Web slice is too small
    list-of-dicts -> table  a common way to assemble a comparison DataFrame
    Series.iloc[0]          pick the first row of a filtered comparison table
    two-panel bar chart     sample size versus absolute error

main() draws a small random sample and a larger convenience sample, compares
each mean with the population parameter, and shows that the larger sample
can still have more error.

Run it:
    python data_foundations_03_sampling_bias.py
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
RANDOM_SAMPLE_SIZE = 200
# Intentionally larger than the random sample. The lesson claim is that
# extra rows do not repair a biased selection rule.
CONVENIENCE_SAMPLE_SIZE = 1_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic register used throughout the lesson.

    Identical generator to Step 2, including region and order value, so
    the three scripts describe one world. Step 3 does not use region or
    order value in the comparison, but keeping the columns avoids a
    silent change in the random stream.

    Parameters
    ----------
    seed:
        Shared integer so Steps 1-3 rebuild the same 12,000 orders.

    Returns
    -------
    pd.DataFrame
        Full register with the Step 2 columns.
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
    return add_business_variables(population, rng)


def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int = RANDOM_SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a simple random sample without replacement."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


def add_business_variables(
    population: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Add region and order value as introduced in Step 2."""
    result = population.copy()
    result["region"] = rng.choice(
        ["North", "Central", "South"],
        size=len(result),
        p=[0.30, 0.45, 0.25],
    )
    unit_value = rng.gamma(shape=3.0, scale=180.0, size=len(result))
    result["order_value_mxn"] = (
        unit_value * result["items_per_order"]
    ).round(2)
    return result


def classify_variables() -> dict[str, str]:
    """Return the analytical roles introduced in Step 2.

    Kept so this file remains a complete copy of the Step 2 register
    contract, even though main() does not print the roles in Step 3.
    """
    return {
        "order_id": "Identifier (categorical role)",
        "channel": "Categorical",
        "region": "Categorical",
        "items_per_order": "Quantitative discrete",
        "processing_time_minutes": "Quantitative continuous",
        "order_value_mxn": "Quantitative continuous",
    }


# --- NEW (1) draw_convenience_sample() ---------------------------------------
def draw_convenience_sample(
    population: pd.DataFrame,
    sample_size: int = CONVENIENCE_SAMPLE_SIZE,
) -> pd.DataFrame:
    """Take the first available Web orders as a convenience sample.

    Parameters
    ----------
    population:
        Full register. Must contain a channel column.
    sample_size:
        How many Web rows to keep. Default is 1,000, five times the
        random-sample size.

    Returns
    -------
    pd.DataFrame
        The first sample_size Web rows in the table's current order.

    Raises
    ------
    ValueError
        If the synthetic population has fewer Web orders than sample_size.
        That would be a bug in the generator, not a sampling result.

    Notes
    -----
    A convenience sample is defined by an easy access rule, not by equal
    chance. Here the rule is "take Web orders from the top of the table."
    Web orders were generated with a -5 minute channel shift, so this
    slice is systematically faster than the full population. There is no
    random_state because the selection is not a probability sample.
    """
    # population["channel"] == "Web" is a boolean Series, True on Web rows.
    # .loc[boolean_series] keeps only the True rows. This is pandas Boolean
    # indexing, not Python's list.filter.
    available_web_orders = population.loc[population["channel"] == "Web"]
    if len(available_web_orders) < sample_size:
        raise ValueError("The synthetic population has too few Web orders.")
    # head(n) returns the first n rows in whatever order the table currently
    # has (here, the original generation order). It is the software image of
    # "grab the first records that are easy to reach."
    return available_web_orders.head(sample_size)
# ------------------------------------------------------------------------------


# --- NEW (2) compare_estimates() ---------------------------------------------
def compare_estimates(
    population: pd.DataFrame,
    random_sample: pd.DataFrame,
    convenience_sample: pd.DataFrame,
) -> pd.DataFrame:
    """Compare each sample mean with the full population parameter.

    Parameters
    ----------
    population:
        Full register; its mean is the parameter mu.
    random_sample, convenience_sample:
        The two samples to score.

    Returns
    -------
    pd.DataFrame
        Two rows (Random, Convenience) and four columns: sample, size,
        mean, and absolute_error. Building a small table from a list of
        dicts is a standard pandas pattern: each dict is one row, the
        keys become column names.

    Notes
    -----
    absolute_error = |x-bar - mu|. The sign is dropped so the later bar
    chart can compare magnitudes directly.
    """
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for label, sample in [
        ("Random", random_sample),
        ("Convenience", convenience_sample),
    ]:
        sample_mean = sample[variable].mean()
        rows.append(
            {
                "sample": label,
                "size": len(sample),
                "mean": sample_mean,
                "absolute_error": abs(sample_mean - population_mean),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_bias_figure() ----------------------------------------------
def save_bias_figure(comparison: pd.DataFrame) -> Path:
    """Save sample sizes and estimation errors in one evidence figure.

    Parameters
    ----------
    comparison:
        The two-row table from compare_estimates().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: how many orders each sample used. Right panel: how far
    each sample mean sat from mu. Reading the two panels together is the
    lesson: the convenience sample is taller on the left and taller on
    the right.
    """
    output_path = DIR_FIGURES / "data_foundations_03_sampling_bias.png"
    colors = ["#0039A6", "#EC2661"]
    # 1 row, 2 columns. axes[0] is size; axes[1] is error.
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.0))

    axes[0].bar(comparison["sample"], comparison["size"], color=colors)
    axes[0].set_title("Sample size")
    axes[0].set_ylabel("Number of orders")

    axes[1].bar(
        comparison["sample"],
        comparison["absolute_error"],
        color=colors,
    )
    axes[1].set_title("Error from population mean")
    axes[1].set_ylabel("Absolute error (minutes)")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("A Larger Biased Sample Can Produce More Error", fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the random-versus-convenience comparison and print the verdict."""
    population = build_population()
    random_sample = draw_random_sample(population)
    convenience_sample = draw_convenience_sample(population)
    comparison = compare_estimates(
        population,
        random_sample,
        convenience_sample,
    )
    figure_path = save_bias_figure(comparison)

    population_mean = population["processing_time_minutes"].mean()
    # comparison["sample"] == "Random" is a boolean mask. .loc[mask] keeps
    # the matching row (still a one-row DataFrame). .iloc[0] then converts
    # that one-row table into a Series so we can write random_row["mean"].
    random_row = comparison.loc[comparison["sample"] == "Random"].iloc[0]
    convenience_row = comparison.loc[
        comparison["sample"] == "Convenience"
    ].iloc[0]

    print("================================================================")
    print("LESSON 01 - STEP 3: SAMPLE SIZE AND SELECTION BIAS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Population mean parameter       : {population_mean:.2f} min")
    print(
        f"Random sample (n={int(random_row['size']):,}) mean     : "
        f"{random_row['mean']:.2f} min"
    )
    print(f"Random sample absolute error    : {random_row['absolute_error']:.2f} min")
    print(
        f"Convenience sample (n={int(convenience_row['size']):,}) mean: "
        f"{convenience_row['mean']:.2f} min"
    )
    print(
        "Convenience absolute error      : "
        f"{convenience_row['absolute_error']:.2f} min"
    )
    # A boolean printed as True/False. This is the pedagogical punch line:
    # the 1,000-row convenience sample misses mu by more than the 200-row
    # random sample.
    print(
        "Larger sample has more error    : "
        f"{convenience_row['absolute_error'] > random_row['absolute_error']}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

