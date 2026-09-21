"""
Lesson 03 - Step 2: Standard Deviation and Interquartile Range
==============================================================
NEW IN THIS STEP: summarize_spread() and save_spread_figure().

CHANGES FROM descriptive_statistics_01_center.py
Introduce them in this order:
    1. summarize_spread()      calculates sample s, quartiles, and IQR
    2. save_spread_figure()    compares mean +/- s with Q1, median, and Q3

How to read this file:
You already know Python through OOP. Step 1 built the synthetic order sample
and computed mean and median. That generator is copied here so the script
stays self-contained; it is commented only where this file does something new.
Lesson 01 remains the reference for pathlib, Agg, savefig/close, and if __name__.

New in this step:
    Series.std(ddof=1)    sample standard deviation s, divisor n-1
    Series.quantile       0.25 and 0.75 as Q1 and Q3
    IQR                   Q3 minus Q1, the middle 50% of the ordered sample
    ax.errorbar           horizontal intervals in the original minutes
    asymmetric xerr       IQR arms from the median to Q1 and to Q3

main() rebuilds the same 240-order sample, reports s, Q1, Q3, and IQR, and
draws mean +/- s beside the quartile interval.

Run it:
    uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_02_spread.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic order sample introduced in Step 1.

    The generator, seed, and columns are identical so the two scripts
    describe one sample. See Step 1 for the Gamma queue and clip commentary.
    """
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


# --- NEW (1) summarize_spread() ----------------------------------------------
def summarize_spread(sample: pd.DataFrame) -> dict[str, float]:
    """Return sample standard deviation, quartiles, and IQR.

    Parameters
    ----------
    sample:
        Table with a processing_time_minutes column.

    Returns
    -------
    dict[str, float]
        sample_standard_deviation (s), first_quartile (Q1), third_quartile
        (Q3), and interquartile_range (Q3 - Q1). All four are in minutes.

    Notes
    -----
    s measures spread around the mean using every observation. IQR measures
    spread from ordered positions and spans the middle 50%. Pair mean with
    s, and median with IQR, when you report a center-and-spread pair.
    """
    values = sample["processing_time_minutes"]
    # quantile(q) is the sample q-quantile. 0.25 is Q1; 0.75 is Q3. pandas
    # interpolates linearly when q sits between two observations. This is
    # the Series method; np.percentile(values, 25) is the NumPy equivalent.
    first_quartile = values.quantile(0.25)
    third_quartile = values.quantile(0.75)
    return {
        # ddof=1 is the sample formula: divisor n-1. pandas .std() already
        # defaults to ddof=1; NumPy np.std() defaults to 0 (divisor n).
        # Pass ddof=1 explicitly so the sample convention is visible.
        "sample_standard_deviation": values.std(ddof=1),
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        # IQR is a length in minutes, not a point: Q3 minus Q1.
        "interquartile_range": third_quartile - first_quartile,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) save_spread_figure() --------------------------------------------
def save_spread_figure(
    center: dict[str, float],
    spread: dict[str, float],
) -> Path:
    """Save two center-and-spread summaries in the original time units.

    Parameters
    ----------
    center:
        Mean and median from summarize_center().
    spread:
        s, Q1, Q3, and IQR from summarize_spread().

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    The figure is two horizontal intervals, not a histogram. Top row:
    mean with symmetric arms of length s. Bottom row: median with arms
    to Q1 and Q3, which need not be equal. Both live on the minutes axis.
    """
    output_path = DIR_FIGURES / "descriptive_statistics_02_spread.png"
    mean = center["mean"]
    median = center["median"]
    standard_deviation = spread["sample_standard_deviation"]
    first_quartile = spread["first_quartile"]
    third_quartile = spread["third_quartile"]

    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    # errorbar with a scalar xerr draws a symmetric horizontal interval.
    # fmt="o" marks the center; capsize is the whisker end-cap length.
    ax.errorbar(
        mean,
        1,
        xerr=standard_deviation,
        fmt="o",
        markersize=9,
        capsize=7,
        linewidth=3,
        color="#EC2661",
    )
    ax.errorbar(
        median,
        0,
        # xerr shape (2, 1) is [[left arm], [right arm]]. The IQR need
        # not be symmetric around the median.
        xerr=np.array([[median - first_quartile], [third_quartile - median]]),
        fmt="o",
        markersize=9,
        capsize=7,
        linewidth=3,
        color="#0039A6",
    )
    ax.text(
        mean,
        1.14,
        f"mean {mean:.2f}; s {standard_deviation:.2f}",
        fontsize=13,
        ha="center",
    )
    ax.text(
        median,
        0.14,
        f"median {median:.2f}; IQR {spread['interquartile_range']:.2f}",
        fontsize=13,
        ha="center",
    )
    ax.set_yticks([0, 1], ["Middle 50%", "Around the mean"])
    ax.set_xlabel("Processing time (minutes)", fontsize=13)
    ax.set_ylim(-0.35, 1.45)
    ax.set_title("Two Descriptions of Spread", fontsize=16, fontweight="bold")
    ax.tick_params(labelsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Rebuild the sample, print s and IQR, and save the two-interval figure."""
    sample = build_order_sample()
    center = summarize_center(sample)
    spread = summarize_spread(sample)
    figure_path = save_spread_figure(center, spread)

    print("================================================================")
    print("LESSON 03 - STEP 2: STANDARD DEVIATION AND IQR")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size (n)                 : {len(sample):,}")
    print(f"Mean / median                   : {center['mean']:.2f} / "
          f"{center['median']:.2f} min")
    print("Sample standard deviation (s)   : "
          f"{spread['sample_standard_deviation']:.2f} min")
    print(f"First quartile (Q1)             : {spread['first_quartile']:.2f} min")
    print(f"Third quartile (Q3)             : {spread['third_quartile']:.2f} min")
    print(f"Interquartile range (IQR)       : {spread['interquartile_range']:.2f} min")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

