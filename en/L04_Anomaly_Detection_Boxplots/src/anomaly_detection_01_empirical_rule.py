"""
Lesson 04 - Step 1: The Empirical Rule
======================================
NEW IN THIS STEP: build_baseline_orders(), empirical_coverage(), and
save_empirical_rule_figure().

The Recipe
Create a bell-shaped synthetic processing-time sample, calculate its mean and
sample standard deviation, then compare observed coverage with the Empirical
Rule benchmarks. The rule is an approximation for bell-shaped, symmetric data.

How to read this file:
You already know Python through OOP: functions, classes, lists, dictionaries,
loops, and conditionals. Lesson 01 introduced pathlib, the Agg backend,
unattended savefig/close, and the if __name__ entry point. Those plumbing
idioms return here with a short pointer, not a second treatise.

New in this step:
    rng.normal + np.clip     mound-shaped times with a floor at 20 minutes
    Series.std(ddof=1)       sample standard deviation s, not population sigma
    boolean Series.mean()    True/False interval membership turned into a percent
    Empirical Rule           about 68% / 95% / more than 99% within 1s / 2s / 3s
    axvline                  vertical lines at the mean and at mean +/- k s
    dict[str, object]        a type hint: string keys, mixed value types

main() builds one synthetic sample, measures how much of it sits within one,
two, and three sample standard deviations of the mean, and writes the
evidence figure.

Run it:
    uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_01_empirical_rule.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Course-wide seed so every rerun rebuilds the same 600 times.
SEED = 42
SAMPLE_SIZE = 600
# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_baseline_orders() -----------------------------------------
def build_baseline_orders(seed: int = SEED) -> pd.DataFrame:
    """Build a fully synthetic, bell-shaped processing-time sample.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's Generator so Steps 2 and 3 rebuild
        the same 600 baseline times. Default is the module-level SEED.

    Returns
    -------
    pd.DataFrame
        One row per order and two columns: order_id (a label, not a
        quantity) and processing_time_minutes. Nothing is read from disk.

    Notes
    -----
    The annotation `-> pd.DataFrame` is a type hint. Python does not
    enforce it at run time. It documents the contract: callers receive a
    pandas table. Times are drawn from a Normal(45, 5) and then clipped
    below at 20 minutes so the sample stays mound-shaped and non-negative.
    """
    rng = np.random.default_rng(seed)
    # loc= mean, scale= standard deviation. size= one draw per order.
    # np.clip(..., 20.0, None) puts a floor at 20 minutes and leaves the
    # upper end unbounded. The floor is far enough from 45 that almost
    # every draw is untouched, so the histogram stays bell-shaped.
    processing_time = np.clip(
        rng.normal(loc=45.0, scale=5.0, size=SAMPLE_SIZE),
        20.0,
        None,
    )
    return pd.DataFrame(
        {
            "order_id": np.arange(400_001, 400_001 + SAMPLE_SIZE),
            "processing_time_minutes": processing_time.round(2),
        }
    )
# ------------------------------------------------------------------------------


# --- NEW (2) empirical_coverage() --------------------------------------------
def empirical_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Measure how much of the sample sits within 1s, 2s, and 3s of the mean.

    Parameters
    ----------
    orders:
        Table with a processing_time_minutes column.

    Returns
    -------
    dict[str, object]
        mean, sample_standard_deviation, and coverage_percent. The last
        value is itself a dict mapping k in {1, 2, 3} to the observed
        percentage. `object` in the type hint is required because the
        nested dict is not a float.

    Notes
    -----
    The Empirical Rule is an approximation for bell-shaped, symmetric
    data: about 68% within one sample standard deviation of the mean,
    about 95% within two, and more than 99% within three. It is not a
    guarantee and does not apply to every shape.
    """
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    # ddof=1 is the sample divisor (n - 1). That is the s used with the
    # Empirical Rule on a sample; ddof=0 would be the population sigma.
    standard_deviation = float(values.std(ddof=1))
    # For each k, build a boolean Series: True when |x - mean| <= k s.
    # .sub(mean) subtracts the scalar from every row. .abs() is the
    # distance to the mean. .mean() on True/False treats True as 1, so
    # the result is the coverage proportion; * 100 converts it to a
    # percent. float() unwraps the pandas scalar for printing.
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (1, 2, 3)
    }
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "coverage_percent": coverage,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_empirical_rule_figure() ------------------------------------
def save_empirical_rule_figure(
    orders: pd.DataFrame,
    summary: dict[str, object],
) -> Path:
    """Save the bell-shaped histogram and the observed coverage bars.

    Parameters
    ----------
    orders:
        Sample whose processing_time_minutes column is plotted.
    summary:
        Dict returned by empirical_coverage(); supplies mean, s, and
        the three observed percentages.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    Left panel: histogram plus vertical lines at the mean and at
    mean +/- k s. Right panel: observed coverage next to the Empirical
    Rule benchmarks written in the tick labels.
    """
    output_path = DIR_FIGURES / "anomaly_detection_01_empirical_rule.png"
    values = orders["processing_time_minutes"]
    mean = float(summary["mean"])
    standard_deviation = float(summary["sample_standard_deviation"])
    coverage = summary["coverage_percent"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    # bins=24 is a bin count, not a list of edges. edgecolor="white"
    # separates adjacent bars so the mound shape is readable.
    axes[0].hist(values, bins=24, color="#A7B0BF", edgecolor="white")
    # axvline draws a vertical line at one x value. The solid navy line
    # marks the sample mean.
    axes[0].axvline(mean, color="#1A2E51", linewidth=2.4, label="Mean")
    # Each k draws a matching pair: mean - k s on the left, mean + k s
    # on the right. Only the right line gets a legend label so each k
    # appears once rather than twice.
    for k, color in [(1, "#EC2661"), (2, "#FF8A3D"), (3, "#0039A6")]:
        axes[0].axvline(
            mean - k * standard_deviation,
            color=color,
            linestyle="--",
            linewidth=1.6,
        )
        axes[0].axvline(
            mean + k * standard_deviation,
            color=color,
            linestyle="--",
            linewidth=1.6,
            label=f"+/- {k}s",
        )
    axes[0].set_title("Bell-Shaped Synthetic Times", fontsize=15)
    axes[0].set_xlabel("Processing time (minutes)", fontsize=12)
    axes[0].set_ylabel("Orders", fontsize=12)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10)

    positions = np.arange(3)
    observed = [coverage[k] for k in (1, 2, 3)]
    bars = axes[1].bar(positions, observed, color="#EC2661", width=0.62)
    # Tick text carries the Empirical Rule benchmarks so the bars can be
    # compared with 68%, 95%, and more than 99% without a second series.
    axes[1].set_xticks(
        positions,
        ["Within 1s\nabout 68%", "Within 2s\nabout 95%", "Within 3s\nmore than 99%"],
    )
    axes[1].set_ylim(0, 108)
    axes[1].set_ylabel("Observed percentage", fontsize=12)
    axes[1].set_title("Coverage in This Sample", fontsize=15)
    axes[1].tick_params(labelsize=10)
    for bar, value in zip(bars, observed):
        # Center the label on the bar: left edge plus half the width.
        # value + 1.8 sits just above the bar top.
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.8,
            f"{value:.2f}%",
            fontsize=11,
            ha="center",
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Empirical Rule Check", fontsize=17, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 coverage check and print the verified lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    orders = build_baseline_orders()
    summary = empirical_coverage(orders)
    figure_path = save_empirical_rule_figure(orders, summary)
    coverage = summary["coverage_percent"]

    print("================================================================")
    print("LESSON 04 - STEP 1: THE EMPIRICAL RULE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size (n)                 : {len(orders):,}")
    print(f"Mean                            : {summary['mean']:.2f} min")
    print("Sample standard deviation (s)   : "
          f"{summary['sample_standard_deviation']:.2f} min")
    for k in (1, 2, 3):
        print(f"Observed within {k}s              : {coverage[k]:.2f}%")
    print("Condition                       : Bell-shaped and symmetric data")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Same script entry point as Lesson 01: run main() only when this file is
# executed, not if it were imported. These lessons never import each other.
if __name__ == "__main__":
    main()

