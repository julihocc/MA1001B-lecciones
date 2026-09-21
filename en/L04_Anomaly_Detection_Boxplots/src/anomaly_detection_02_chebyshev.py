"""
Lesson 04 - Step 2: Chebyshev's Rule
====================================
NEW IN THIS STEP: add_queue_delays(), chebyshev_coverage(), and
save_chebyshev_figure().

Changes from anomaly_detection_01_empirical_rule.py
The Recipe
Introduce them in this order:
    1. add_queue_delays()       creates a right-tailed version of the sample
    2. chebyshev_coverage()     compares observed coverage with lower bounds
    3. save_chebyshev_figure()  shows shape and guarantee together

How to read this file:
You already know Python through OOP. Step 1 built the bell-shaped sample and
counted Empirical Rule coverage. That generator is copied here so the script
stays self-contained; comments concentrate on the NEW bands. Lesson 01 still
covers pathlib, Agg, savefig/close, and if __name__.

New in this step:
    discarded rng.normal()   advances a second Generator past the Step 1 draws
    boolean delay mask       rng.random(n) < p flags which orders get a delay
    rng.gamma / np.where     right-tailed extra minutes on the flagged rows
    Chebyshev 1 - 1/k^2      shape-free lower bound for k = 2 and k = 3
    Series.skew()            sample skewness; positive means a right tail
    grouped bars             bound vs observed coverage side by side

main() adds queue delays to a seeded subset, compares observed 2s/3s coverage
with Chebyshev's lower bounds, and writes the evidence figure.

Run it:
    uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_02_chebyshev.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 600
# Expected share of orders that receive a positive gamma delay.
DELAY_PROBABILITY = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_baseline_orders(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same bell-shaped sample introduced in Step 1.

    The generator, seed, and columns are identical so the two scripts
    describe one world. See Step 1 for the Normal clip commentary.
    """
    rng = np.random.default_rng(seed)
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


def empirical_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Return the Step 1 coverage summaries on whatever sample is passed in.

    Copied so this file stays standalone. The Chebyshev comparison below
    uses a narrower k set and adds lower bounds; this helper is unused by
    main() but documents the original interval-count.
    """
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (1, 2, 3)
    }
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "coverage_percent": coverage,
    }


# --- NEW (1) add_queue_delays() ----------------------------------------------
def add_queue_delays(seed: int = SEED) -> tuple[pd.DataFrame, int]:
    """Add gamma-distributed queue delays to a seeded subset of orders.

    Parameters
    ----------
    seed:
        Same integer used by build_baseline_orders(). A second Generator
        is created from this seed so the delay assignment is reproducible.

    Returns
    -------
    tuple[pd.DataFrame, int]
        The modified table plus the number of orders that received a
        delay. The type hint names both pieces; Python does not enforce it.

    Notes
    -----
    A gamma delay is always positive, so adding it to 10% of orders
    stretches the right tail. That breaks the Empirical Rule's
    bell-shaped condition while leaving Chebyshev applicable.
    """
    orders = build_baseline_orders(seed)
    rng = np.random.default_rng(seed)
    # build_baseline_orders() already consumed SAMPLE_SIZE Normal draws
    # from an identical Generator. This unused call advances the second
    # stream by the same amount so the delay flags are not the same
    # numbers that created the processing times.
    rng.normal(loc=45.0, scale=5.0, size=SAMPLE_SIZE)
    # rng.random(n) draws n Uniform(0, 1) values. Comparing with 0.10
    # produces a boolean mask: True on the delayed orders. Expected
    # count is 60; the seeded run yields 59.
    delayed = rng.random(SAMPLE_SIZE) < DELAY_PROBABILITY
    # np.where(mask, a, b) keeps a gamma draw where delayed is True and
    # 0.0 otherwise. Gamma(shape=2, scale=5) has mean 10 minutes and is
    # right-skewed, which is what creates the tail.
    queue_delay = np.where(
        delayed,
        rng.gamma(shape=2.0, scale=5.0, size=SAMPLE_SIZE),
        0.0,
    )
    orders["processing_time_minutes"] = (
        orders["processing_time_minutes"] + queue_delay
    ).round(2)
    orders["has_queue_delay"] = delayed
    return orders, int(delayed.sum())
# ------------------------------------------------------------------------------


# --- NEW (2) chebyshev_coverage() --------------------------------------------
def chebyshev_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Compare observed coverage with Chebyshev lower bounds for k = 2 and 3.

    Parameters
    ----------
    orders:
        Right-tailed sample from add_queue_delays().

    Returns
    -------
    dict[str, object]
        mean, sample_standard_deviation, skewness, coverage_percent, and
        lower_bound_percent. The last two are dicts keyed by k.

    Notes
    -----
    Chebyshev's inequality: for any distribution and k > 1, at least
    1 - 1/k^2 of the observations lie within k standard deviations of
    the mean. That is a lower bound, not a prediction. k = 1 is omitted
    because the bound would be 0%. The same boolean-mean coverage count
    as Step 1 is reused; only the k set and the bound formula are new.
    """
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (2, 3)
    }
    # k = 2 -> (1 - 1/4) * 100 = 75.00. k = 3 -> (1 - 1/9) * 100 = 88.89.
    bounds = {k: (1 - 1 / k**2) * 100 for k in (2, 3)}
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        # pandas .skew() is the adjusted Fisher-Pearson sample skewness.
        # A positive value confirms the right tail created above.
        "skewness": float(values.skew()),
        "coverage_percent": coverage,
        "lower_bound_percent": bounds,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_chebyshev_figure() -----------------------------------------
def save_chebyshev_figure(
    orders: pd.DataFrame,
    summary: dict[str, object],
) -> Path:
    """Save the right-tailed histogram beside bound-versus-observed bars.

    Parameters
    ----------
    orders:
        Delayed sample plotted in the left panel.
    summary:
        Dict from chebyshev_coverage(); supplies mean, coverage, and bounds.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: the shape that no longer matches the Empirical Rule.
    Right panel: grouped bars so each k shows the Chebyshev floor next
    to the percentage actually observed. Observed coverage may sit well
    above the bound; that is allowed.
    """
    output_path = DIR_FIGURES / "anomaly_detection_02_chebyshev.png"
    coverage = summary["coverage_percent"]
    bounds = summary["lower_bound_percent"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    axes[0].hist(
        orders["processing_time_minutes"],
        bins=28,
        color="#A7B0BF",
        edgecolor="white",
    )
    axes[0].axvline(
        summary["mean"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Mean = {summary['mean']:.2f}",
    )
    axes[0].set_title("Right-Tailed Processing Times", fontsize=15)
    axes[0].set_xlabel("Processing time (minutes)", fontsize=12)
    axes[0].set_ylabel("Orders", fontsize=12)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10)

    # Numeric x positions 0 and 1, one per k. width=0.34 leaves a gap;
    # subtracting/adding width/2 places bound and observed side by side.
    positions = np.arange(2)
    width = 0.34
    actual = [coverage[k] for k in (2, 3)]
    minimum = [bounds[k] for k in (2, 3)]
    axes[1].bar(
        positions - width / 2,
        minimum,
        width,
        color="#1A2E51",
        label="Chebyshev lower bound",
    )
    axes[1].bar(
        positions + width / 2,
        actual,
        width,
        color="#EC2661",
        label="Observed coverage",
    )
    axes[1].set_xticks(positions, ["Within 2s", "Within 3s"])
    axes[1].set_ylim(0, 108)
    axes[1].set_ylabel("Percentage", fontsize=12)
    axes[1].set_title("Guarantee and Observation", fontsize=15)
    axes[1].tick_params(labelsize=10)
    axes[1].legend(
        frameon=False,
        fontsize=10,
        loc="upper center",
        # Negative y in axes coordinates parks the legend below the bars.
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
    )
    for position, lower, observed in zip(positions, minimum, actual):
        axes[1].text(position - width / 2, lower + 1.5, f"{lower:.2f}%", ha="center")
        axes[1].text(position + width / 2, observed + 1.5, f"{observed:.2f}%", ha="center")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Chebyshev's Rule for Any Distribution Shape", fontsize=17,
                 fontweight="bold")
    # rect leaves a bottom margin so the outside legend is not clipped.
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Add the right tail, compare with Chebyshev, and print verified numbers."""
    orders, delayed_count = add_queue_delays()
    summary = chebyshev_coverage(orders)
    figure_path = save_chebyshev_figure(orders, summary)
    coverage = summary["coverage_percent"]
    bounds = summary["lower_bound_percent"]

    print("================================================================")
    print("LESSON 04 - STEP 2: CHEBYSHEV'S RULE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size (n)                 : {len(orders):,}")
    print(f"Orders with added queue delay   : {delayed_count}")
    print(f"Mean                            : {summary['mean']:.2f} min")
    print("Sample standard deviation (s)   : "
          f"{summary['sample_standard_deviation']:.2f} min")
    print(f"Sample skewness                 : {summary['skewness']:.2f}")
    for k in (2, 3):
        print(
            f"Within {k}s: observed / bound     : "
            f"{coverage[k]:.2f}% / {bounds[k]:.2f}%"
        )
    print("Scope                           : Any distribution shape")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

