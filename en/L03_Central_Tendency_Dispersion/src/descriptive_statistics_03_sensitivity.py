"""
Lesson 03 - Step 3: Sensitivity to One Extreme Delay
====================================================
NEW IN THIS STEP: inject_extreme_delay(), compare_summaries(), and
save_sensitivity_figure().

CHANGES FROM descriptive_statistics_02_spread.py
Introduce them in this order:
    1. inject_extreme_delay()      changes one order to a 180-minute delay
    2. compare_summaries()         measures changes in four summaries
    3. save_sensitivity_figure()   contrasts the original and modified samples

How to read this file:
You already know Python through OOP. Steps 1-2 built the sample and the four
summaries. Those functions are copied here so the script stays self-contained;
comments concentrate on the NEW bands. Lesson 01 remains the reference for
pathlib, Agg, savefig/close, and if __name__.

New in this step:
    DataFrame.copy        edit a second table without changing the original
    idxmax / loc          find the current maximum and replace that one cell
    one extreme value     180 minutes in place of the largest recorded time
    np.sort overlay       ordered observations before and after the change
    grouped summary bars  mean, median, s, and IQR in two scenarios
    tuple return          (modified table, row index, original value)

main() replaces one processing time, reprints the four summaries, and shows
that mean and sample s move while median and IQR stay put at two decimals.
The printed limit line is the pedagogical close: sensitivity is not diagnosis.

Run it:
    uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_03_sensitivity.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 240
# The single replacement value, in minutes. It is a modeling choice for this
# demonstration, not a recorded observation and not a detection threshold.
EXTREME_DELAY_MINUTES = 180.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic order sample used throughout the lesson."""
    rng = np.random.default_rng(seed)
    items = np.clip(rng.poisson(lam=3.2, size=SAMPLE_SIZE) + 1, 1, 12)
    queue_time = rng.gamma(shape=2.5, scale=3.0, size=SAMPLE_SIZE)
    measurement_noise = rng.normal(loc=0.0, scale=3.0, size=SAMPLE_SIZE)
    processing_time = np.clip(
        32.0 + 1.4 * items + queue_time + measurement_noise,
        8.0,
        None,
    )
    return pd.DataFrame(
        {
            "order_id": np.arange(300_001, 300_001 + SAMPLE_SIZE),
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )


def summarize_center(sample: pd.DataFrame) -> dict[str, float]:
    """Return the arithmetic mean and median introduced in Step 1."""
    values = sample["processing_time_minutes"]
    return {"mean": values.mean(), "median": values.median()}


def summarize_spread(sample: pd.DataFrame) -> dict[str, float]:
    """Return the spread measures introduced in Step 2.

    See Step 2 for ddof=1, quantile, and IQR commentary.
    """
    values = sample["processing_time_minutes"]
    first_quartile = values.quantile(0.25)
    third_quartile = values.quantile(0.75)
    return {
        "sample_standard_deviation": values.std(ddof=1),
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        "interquartile_range": third_quartile - first_quartile,
    }


# --- NEW (1) inject_extreme_delay() ------------------------------------------
def inject_extreme_delay(
    sample: pd.DataFrame,
    delay_minutes: float = EXTREME_DELAY_MINUTES,
) -> tuple[pd.DataFrame, int, float]:
    """Replace the current maximum with one extreme synthetic delay.

    Parameters
    ----------
    sample:
        Original 240-order table. It is not modified; the function copies it.
    delay_minutes:
        Replacement processing time in minutes. Default 180.0.

    Returns
    -------
    tuple[pd.DataFrame, int, float]
        (modified table, row index of the changed order, original processing
        time). tuple[...] is a type hint: three return values packed as one
        tuple. Callers unpack with modified, row_index, original_value = ...

    Notes
    -----
    Only one cell changes. n stays 240. The exercise is sensitivity of the
    four summaries, not a rule for labeling the value as an anomaly.
    """
    # copy() so loc assignment cannot write through to the caller's table.
    modified = sample.copy()
    # idxmax() is the index label of the first maximum. int() turns that
    # label into a plain Python integer for loc.
    row_index = int(modified["processing_time_minutes"].idxmax())
    original_value = float(modified.loc[row_index, "processing_time_minutes"])
    # One assignment: the current maximum becomes 180 minutes. Every other
    # row is untouched.
    modified.loc[row_index, "processing_time_minutes"] = delay_minutes
    return modified, row_index, original_value
# ------------------------------------------------------------------------------


# --- NEW (2) compare_summaries() ---------------------------------------------
def compare_summaries(
    original: pd.DataFrame,
    modified: pd.DataFrame,
) -> pd.DataFrame:
    """Compare center and spread before and after one extreme delay.

    Parameters
    ----------
    original, modified:
        The untouched sample and the copy with one cell replaced.

    Returns
    -------
    pd.DataFrame
        Two rows (Original, One extreme) and four summary columns: mean,
        median, sample_standard_deviation, interquartile_range.

    Notes
    -----
    Each scenario reuses summarize_center() and summarize_spread() so the
    formulas do not change, only the input table.
    """
    rows = []
    for scenario, sample in [("Original", original), ("One extreme", modified)]:
        center = summarize_center(sample)
        spread = summarize_spread(sample)
        rows.append(
            {
                "scenario": scenario,
                "mean": center["mean"],
                "median": center["median"],
                "sample_standard_deviation": spread["sample_standard_deviation"],
                "interquartile_range": spread["interquartile_range"],
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_sensitivity_figure() ---------------------------------------
def save_sensitivity_figure(
    original: pd.DataFrame,
    modified: pd.DataFrame,
    comparison: pd.DataFrame,
) -> Path:
    """Save the changed observation and its effect on four summaries.

    Parameters
    ----------
    original, modified:
        Samples plotted as ordered processing times in the left panel.
    comparison:
        Two-row table from compare_summaries() for the grouped bars.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: both samples sorted. The curves coincide until the last
    rank, where 180 minutes replaces the old maximum. Right panel: mean
    and sample s move; median and IQR do not, at two-decimal precision.
    """
    output_path = DIR_FIGURES / "descriptive_statistics_03_sensitivity.png"
    metric_labels = ["Mean", "Median", "Sample s", "IQR"]
    columns = [
        "mean",
        "median",
        "sample_standard_deviation",
        "interquartile_range",
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    # Sort both samples. The two sequences differ in only one position
    # (the last, once the old maximum is replaced by 180). ranks is 1..n
    # so the x-axis is "ordered observation," not clock time.
    original_sorted = np.sort(original["processing_time_minutes"].to_numpy())
    modified_sorted = np.sort(modified["processing_time_minutes"].to_numpy())
    ranks = np.arange(1, len(original_sorted) + 1)
    axes[0].plot(ranks, original_sorted, color="#1A2E51", label="Original")
    axes[0].plot(
        ranks,
        modified_sorted,
        color="#EC2661",
        linewidth=2,
        label="One extreme delay",
    )
    axes[0].set_xlabel("Ordered observation", fontsize=12)
    axes[0].set_ylabel("Processing time (minutes)", fontsize=12)
    axes[0].set_title("Only one recorded value changes", fontsize=14)
    axes[0].legend(frameon=False, fontsize=11)

    # Same grouped-bar layout as Lesson 02: numeric positions, width 0.36,
    # original on the left of each tick, modified on the right.
    positions = np.arange(len(columns))
    width = 0.36
    axes[1].bar(
        positions - width / 2,
        comparison.loc[0, columns],
        width,
        color="#1A2E51",
        label="Original",
    )
    axes[1].bar(
        positions + width / 2,
        comparison.loc[1, columns],
        width,
        color="#EC2661",
        label="One extreme",
    )
    axes[1].set_xticks(positions, metric_labels)
    axes[1].set_ylabel("Minutes", fontsize=12)
    axes[1].set_title("Mean and sample s respond most", fontsize=14)
    axes[1].legend(frameon=False, fontsize=11)

    for axis in axes:
        axis.tick_params(labelsize=10)
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle(
        "Sensitivity to One Extreme Synthetic Delay",
        fontsize=16,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Replace one value, print the four summary changes, and save the figure."""
    original = build_order_sample()
    modified, row_index, original_value = inject_extreme_delay(original)
    comparison = compare_summaries(original, modified)
    figure_path = save_sensitivity_figure(original, modified, comparison)
    # iloc[0] is the Original row; iloc[1] is the One extreme row.
    before = comparison.iloc[0]
    after = comparison.iloc[1]

    print("================================================================")
    print("LESSON 03 - STEP 3: SENSITIVITY TO ONE EXTREME DELAY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size in both scenarios   : {len(original):,}")
    print(f"Changed order ID                : {int(original.loc[row_index, 'order_id'])}")
    print(f"Changed value                   : {original_value:.2f} -> "
          f"{EXTREME_DELAY_MINUTES:.2f} min")
    print("----------------------------------------------------------------")
    for label, column in [
        ("Mean", "mean"),
        ("Median", "median"),
        ("Sample standard deviation", "sample_standard_deviation"),
        ("Interquartile range", "interquartile_range"),
    ]:
        change = after[column] - before[column]
        # :+.2f always prints a sign, so +0.00 is visible when a summary
        # does not move at two-decimal display precision.
        print(
            f"{label:<27}: {before[column]:>6.2f} -> "
            f"{after[column]:>6.2f} min (change {change:+.2f})"
        )
    print("----------------------------------------------------------------")
    print("Limit: sensitivity is not an automatic anomaly diagnosis.")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

