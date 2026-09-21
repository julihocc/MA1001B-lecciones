"""
Lesson 01 - Step 1: Population, Sample, Parameter, and Statistic
================================================================
NEW IN THIS STEP: build_population(), draw_random_sample(), and save_figure().

Context:
A synthetic business operations register represents every order processed during
one planning period. We can inspect the full register in this simulation, but an
analyst normally observes only a sample and uses a statistic to estimate a
population parameter.

How to read this file:
You already know Python through object-oriented programming: functions, classes,
lists, dictionaries, loops, and conditionals. This script adds four libraries
that later lessons reuse, plus a few file-system and plotting idioms that are
not the statistics topic but are required to run the program unattended.

    pathlib.Path     locate the figures/ folder from this file's own path
    numpy            draw random numbers and build numeric arrays
    pandas           store the register as a table (rows = orders, columns =
                     variables)
    matplotlib       draw and save a PNG without opening a window

main() builds one synthetic population, draws one simple random sample, compares
the population mean (a parameter) with the sample mean (a statistic), and writes
the evidence figure.

Run it:
    python data_foundations_01_population_sample.py
"""

# Path is a class for file-system locations. Using Path objects instead of
# raw strings lets us join folders with / and ask for .parent without caring
# whether the operating system uses \ or /.
from pathlib import Path

# matplotlib is the plotting library. numpy (imported as np by convention) is
# the numeric-array library. pandas (imported as pd) is the table library.
# The short aliases np and pd are universal in data work; you will see them
# in every later lesson.
import matplotlib
import numpy as np
import pandas as pd

# Agg is a "headless" drawing backend: it renders pixels into a file and never
# tries to open a GUI window. It MUST be selected before pyplot is imported,
# otherwise pyplot may lock onto a display backend that fails on a server or
# in automated runs. This line is infrastructure, not statistics.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# A fixed seed makes the "random" draws identical every time the script runs.
# 42 is the course-wide default. Change it only if a later lesson says so.
SEED = 42
# N: every order in the synthetic planning period. Large enough to look like
# an operations register, small enough to build in a fraction of a second.
POPULATION_SIZE = 12_000
# n: how many rows the simple random sample keeps. The underscore in 12_000
# is only a readability separator; Python treats it as 12000.
SAMPLE_SIZE = 200

# __file__ is the path of THIS script, even if you launched Python from the
# repository root. .resolve() turns any relative pieces into an absolute path.
# .parent is src/; the next .parent is the lesson folder. / "figures" then
# points at L01_Population_Samples_Data/figures/. Building the path from
# __file__ means the PNG is written next to the package, not into whatever
# folder your shell happens to be in.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# parents=True creates any missing intermediate folders. exist_ok=True means
# "do nothing if figures/ already exists" instead of raising FileExistsError.
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_population() ----------------------------------------------
def build_population(seed: int = SEED) -> pd.DataFrame:
    """Build a fully synthetic register of business operations.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's generator so the same register is
        rebuilt in Steps 2 and 3. Default is the module-level SEED.

    Returns
    -------
    pd.DataFrame
        One row per order and four columns: order_id, channel,
        items_per_order, and processing_time_minutes. Nothing is read from
        disk; every value is generated in memory.

    Notes
    -----
    The annotation `-> pd.DataFrame` is a type hint. Python does not enforce
    it at run time. It documents the contract: callers receive a pandas table.
    """
    # default_rng(seed) returns a Generator object. All later random draws
    # in this function go through rng, so they form one reproducible stream.
    # Do not mix this with the older np.random.seed() global state.
    rng = np.random.default_rng(seed)

    # choice picks from a discrete list. size=POPULATION_SIZE asks for one
    # label per order. p= is a probability vector that MUST sum to 1: 45%
    # Retail, 35% Web, 20% Partner. The result is a NumPy array of strings,
    # not a pandas column yet.
    channels = rng.choice(
        ["Retail", "Web", "Partner"],
        size=POPULATION_SIZE,
        p=[0.45, 0.35, 0.20],
    )

    # pd.Series(channels) wraps the array so we can use .map, which replaces
    # each label with a number. Retail orders are 6 minutes slower than the
    # baseline, Web orders 5 minutes faster, Partner orders 2 minutes slower.
    # These shifts are a modeling choice so the three channels have different
    # typical times; they are not estimated from real data.
    channel_effect = pd.Series(channels).map(
        {"Retail": 6.0, "Web": -5.0, "Partner": 2.0}
    )

    # poisson(lam=3.2) draws counts of "extra" items around a mean of 3.2.
    # Adding 1 shifts the support so every order has at least one item.
    # np.clip(..., 1, 12) then forces any draw outside [1, 12] onto the
    # nearest endpoint. The result is a discrete quantitative variable.
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)

    # Independent Normal noise, mean 0, standard deviation 7 minutes. This
    # is the leftover order-to-order variation after channel and item count
    # have been accounted for.
    noise = rng.normal(loc=0.0, scale=7.0, size=POPULATION_SIZE)

    # Linear predictor: 38-minute baseline + channel shift + 1.4 minutes per
    # item + noise. .to_numpy() converts the pandas Series of channel shifts
    # into a plain NumPy array so it can be added to the other arrays.
    # np.clip(..., 8.0, None) puts a floor at 8 minutes and leaves the upper
    # end unbounded (None). .round(2) later stores hundredths of a minute.
    processing_time = np.clip(
        38.0 + channel_effect.to_numpy() + 1.4 * items + noise,
        8.0,
        None,
    )

    # A DataFrame is a labeled table. The dict keys become column names; each
    # value must be a sequence of length POPULATION_SIZE. np.arange(a, b)
    # produces a, a+1, ..., b-1, so the IDs run from 100001 through 112000.
    # Those integers are identifiers (labels), not quantities to average.
    return pd.DataFrame(
        {
            "order_id": np.arange(100_001, 100_001 + POPULATION_SIZE),
            "channel": channels,
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )
# ------------------------------------------------------------------------------


# --- NEW (2) draw_random_sample() --------------------------------------------
def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a simple random sample without replacement.

    Parameters
    ----------
    population:
        The full register returned by build_population().
    sample_size:
        Number of rows to keep. Default SAMPLE_SIZE is 200.
    seed:
        Forwarded to pandas as random_state so the same 200 rows are
        selected on every run.

    Returns
    -------
    pd.DataFrame
        A new table with sample_size rows and the same columns as
        population. The original population is not modified.

    Notes
    -----
    "Without replacement" means an order cannot appear twice in the sample.
    That is the default meaning of a simple random sample of distinct units.
    pandas DataFrame.sample uses its own RNG seeded by random_state; it does
    not reuse the NumPy Generator from build_population(). Using the same
    integer 42 in both places is enough for a reproducible lesson, even
    though the two streams are technically separate.
    """
    # n= how many rows. replace=False forbids repeats. random_state=seed
    # pins the draw. The method returns a new DataFrame; population is
    # unchanged.
    return population.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ----------------------------------------------------
def save_figure(
    population: pd.DataFrame,
    sample: pd.DataFrame,
) -> Path:
    """Save the population and sample distributions without opening a window.

    Parameters
    ----------
    population, sample:
        Tables that both contain the column processing_time_minutes.

    Returns
    -------
    Path
        Absolute path of the PNG that was written. The function's only
        side effect is that file; it does not display a window.

    Notes
    -----
    Two histograms share the same bin edges so a bar in the population
    panel covers the same minutes as the matching bar in the sample overlay.
    density=True scales each histogram to area 1, which makes a large
    population and a small sample comparable on one vertical axis.
    """
    output_path = DIR_FIGURES / "data_foundations_01_population_sample.png"

    # linspace(start, stop, num) returns num equally spaced numbers from
    # start to stop inclusive. Using the population min and max as the
    # endpoints, 28 points define 27 bins that cover every observed time.
    bins = np.linspace(
        population["processing_time_minutes"].min(),
        population["processing_time_minutes"].max(),
        28,
    )

    # subplots returns (Figure, Axes). figsize is width x height in inches.
    # Almost all drawing methods are called on ax, not on fig.
    fig, ax = plt.subplots(figsize=(8.0, 4.5))

    # First histogram: filled bars for the population. alpha=0.55 makes
    # them translucent so the sample outline remains visible on top.
    # The f-string {len(population):,} inserts a thousands separator
    # (12,000 rather than 12000).
    ax.hist(
        population["processing_time_minutes"],
        bins=bins,
        density=True,
        alpha=0.55,
        color="#1A2E51",
        label=f"Population (N = {len(population):,})",
    )
    # Second histogram: histtype="step" draws only the outline, which is
    # the usual way to overlay a smaller sample on a filled population.
    ax.hist(
        sample["processing_time_minutes"],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=2.2,
        color="#EC2661",
        label=f"Random sample (n = {len(sample)})",
    )
    ax.set_title("Population and Sample: Processing Time")
    ax.set_xlabel("Processing time (minutes)")
    ax.set_ylabel("Density")
    # frameon=False drops the legend box so the plot stays uncluttered.
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout shrinks unused margins so labels are not clipped in the
    # PNG. Always call it before savefig.
    fig.tight_layout()
    # dpi=170 is the course default for Beamer-readable figures.
    fig.savefig(output_path, dpi=170)
    # close() releases the Figure from memory. Without it, a long sequence
    # of scripts can accumulate hidden figures. Never call plt.show().
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 comparison and print the verified lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    population = build_population()
    sample = draw_random_sample(population)

    # ["processing_time_minutes"] selects one column as a Series. .mean()
    # is the arithmetic average. On the full register this number is a
    # parameter, written mu. On the sample it is a statistic, written x-bar.
    population_mean = population["processing_time_minutes"].mean()
    sample_mean = sample["processing_time_minutes"].mean()
    # Absolute error ignores the sign: we care how far the statistic sits
    # from the parameter, not whether it over- or under-shot.
    estimation_error = abs(sample_mean - population_mean)
    figure_path = save_figure(population, sample)

    print("================================================================")
    print("LESSON 01 - STEP 1: POPULATION AND SAMPLE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    # :>, :<, and :.2f are format specs. :, adds thousands separators;
    # .2f prints two digits after the decimal point.
    print(f"Population size (N)             : {len(population):,}")
    print(f"Random sample size (n)          : {len(sample):,}")
    print(f"Population mean parameter (mu)  : {population_mean:.2f} min")
    print(f"Sample mean statistic (x-bar)   : {sample_mean:.2f} min")
    print(f"Absolute estimation error       : {estimation_error:.2f} min")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Python sets __name__ to the string "__main__" only when this file is the
# program being executed. If another file imported this module (these
# lessons never do), main() would not run automatically. The idiom is the
# standard script entry point; keep it even though each lesson file is
# self-contained.
if __name__ == "__main__":
    main()

