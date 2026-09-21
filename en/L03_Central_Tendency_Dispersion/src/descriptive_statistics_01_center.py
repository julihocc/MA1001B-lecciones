"""
Lesson 03 - Step 1: Mean and Median
===================================
NEW IN THIS STEP: build_order_sample(), summarize_center(), and
save_center_figure().

Context:
A fully synthetic sample contains processing times for 240 business orders.
The mean uses every numerical value, while the median is the midpoint of the
ordered observations.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy,
pandas, the Agg backend, unattended savefig/close, and if __name__. Those
idioms return here with a short pointer, not a second treatise.

New in this step:
    rng.gamma             positive waiting times for the queue
    Series.mean           arithmetic average; every observation equally
    Series.median         midpoint of the ordered sample (n even: average
                          of the two central values)
    axvline overlay       mean and median as vertical lines on one histogram

main() builds one 240-order sample, reports both centers and their difference,
and writes the evidence figure.

Run it:
    uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_01_center.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 240
# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_order_sample() --------------------------------------------
def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Build a fully synthetic sample of order processing times.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's Generator so Steps 2 and 3 rebuild
        the same 240 orders. Default is the module-level SEED.

    Returns
    -------
    pd.DataFrame
        One row per order. Columns: order_id, items_per_order, and
        processing_time_minutes. Nothing is read from disk.

    Notes
    -----
    This table is the dataset being described: n = 240 observations, not
    the 12,000-row sampling frame from Lessons 01-02. Processing time has
    four additive pieces: a 32-minute baseline, 1.4 minutes per item, a
    Gamma queue wait, and Normal measurement noise.
    """
    rng = np.random.default_rng(seed)
    # Poisson item counts, then clip to [1, 12], same idea as Lesson 01.
    items = np.clip(rng.poisson(lam=3.2, size=SAMPLE_SIZE) + 1, 1, 12)
    # Gamma draws are always positive: a waiting-time model for the queue.
    # Mean wait is shape * scale = 2.5 * 3.0 = 7.5 minutes.
    queue_time = rng.gamma(shape=2.5, scale=3.0, size=SAMPLE_SIZE)
    measurement_noise = rng.normal(loc=0.0, scale=3.0, size=SAMPLE_SIZE)
    # Linear predictor, then a floor at 8 minutes. None leaves the upper
    # end unbounded. .round(2) later stores hundredths of a minute.
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
# ------------------------------------------------------------------------------


# --- NEW (2) summarize_center() ----------------------------------------------
def summarize_center(sample: pd.DataFrame) -> dict[str, float]:
    """Return the arithmetic mean and median processing time.

    Parameters
    ----------
    sample:
        Table with a processing_time_minutes column.

    Returns
    -------
    dict[str, float]
        Keys "mean" and "median". The annotation names the contract;
        Python does not enforce it at run time.

    Notes
    -----
    pandas Series.mean is the arithmetic average. Series.median is the
    midpoint of the ordered values. n = 240 is even, so the median is the
    average of the two central observations (ranks 120 and 121).
    np.mean(values) and np.median(values) would return the same two
    numbers; this lesson uses the Series methods.
    """
    values = sample["processing_time_minutes"]
    # Two centers from the same column: every-value average vs ordered midpoint.
    return {
        "mean": values.mean(),
        "median": values.median(),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_center_figure() --------------------------------------------
def save_center_figure(
    sample: pd.DataFrame,
    center: dict[str, float],
) -> Path:
    """Save a histogram with mean and median reference lines.

    Parameters
    ----------
    sample:
        The 240-order table; the histogram uses processing_time_minutes.
    center:
        Dictionary from summarize_center() with keys "mean" and "median".

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Two axvline overlays sit on one count histogram so you can see whether
    the two centers land in the same place. This lesson does not use
    density=True; the vertical axis is a count of orders.
    """
    output_path = DIR_FIGURES / "descriptive_statistics_01_center.png"
    values = sample["processing_time_minutes"]

    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    # bins=18 asks for 18 equal-width bins. edgecolor="white" separates
    # adjacent bars. No density=True, so the y-axis is order counts.
    ax.hist(values, bins=18, color="#A7B0BF", edgecolor="white")
    # axvline draws a vertical reference at x = the summary. Solid magenta
    # is the mean; dashed blue is the median.
    ax.axvline(
        center["mean"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Mean = {center['mean']:.2f}",
    )
    ax.axvline(
        center["median"],
        color="#0039A6",
        linewidth=2.4,
        linestyle="--",
        label=f"Median = {center['median']:.2f}",
    )
    ax.set_title(
        "Center of Synthetic Order Processing Times",
        fontsize=16,
        fontweight="bold",
    )
    ax.set_xlabel("Processing time (minutes)", fontsize=13)
    ax.set_ylabel("Orders", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.legend(frameon=False, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Build the sample, print both centers, and save the figure."""
    sample = build_order_sample()
    center = summarize_center(sample)
    figure_path = save_center_figure(sample, center)

    print("================================================================")
    print("LESSON 03 - STEP 1: MEAN AND MEDIAN")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size (n)                 : {len(sample):,}")
    print(f"Arithmetic mean                 : {center['mean']:.2f} min")
    print(f"Median                          : {center['median']:.2f} min")
    print(f"Mean minus median               : {center['mean'] - center['median']:.2f} min")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

