"""
Lesson 04 - Step 3: Boxplot Flags and Investigation
===================================================
NEW IN THIS STEP: inject_extreme_cases(), flag_with_iqr_rule(), and
save_boxplot_figure().

Changes from anomaly_detection_02_chebyshev.py
The Recipe
Introduce them in this order:
    1. inject_extreme_cases()  inserts four known synthetic extreme delays
    2. flag_with_iqr_rule()    calculates 1.5-IQR fences and potential outliers
    3. save_boxplot_figure()   distinguishes rule flags from known injections

How to read this file:
You already know Python through OOP. Steps 1-2 built the bell-shaped sample
and the right-tailed delayed sample. Those functions are copied here so the
script stays self-contained; comments concentrate on the NEW bands. Lesson 01
still covers pathlib, Agg, savefig/close, and if __name__.

New in this step:
    .copy() + .loc assign    replace four known rows without mutating Step 2
    construction label       known_injected_extreme is a teaching flag, not a finding
    quantile / IQR fences    Q1 - 1.5 IQR and Q3 + 1.5 IQR
    boolean | on Series      element-wise OR; Python `or` will not work here
    seaborn.boxplot          five-number summary plus 1.5-IQR whiskers
    scatter + axvline        overlay flags and the upper fence on the boxplot

main() injects four known extremes, flags every value outside the 1.5-IQR
fences, and writes a figure that separates those known injections from the
other rule flags.

Run it:
    uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_03_boxplot_flags.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 600
DELAY_PROBABILITY = 0.10
# Default RangeIndex row labels of the four orders that will be overwritten.
INJECTED_ROW_INDICES = np.array([41, 187, 333, 512])
# Replacement processing times, in minutes, far above the typical ~45.
INJECTED_DELAYS = np.array([95.0, 110.0, 130.0, 160.0])
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_baseline_orders(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same bell-shaped sample introduced in Step 1.

    See Step 1 for the Normal clip commentary.
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


def add_queue_delays(seed: int = SEED) -> tuple[pd.DataFrame, int]:
    """Rebuild the right-tailed sample introduced in Step 2.

    The unused Normal draw still advances the second Generator so the
    delay mask matches Step 2. See that file for the gamma/mask comments.
    """
    orders = build_baseline_orders(seed)
    rng = np.random.default_rng(seed)
    rng.normal(loc=45.0, scale=5.0, size=SAMPLE_SIZE)
    delayed = rng.random(SAMPLE_SIZE) < DELAY_PROBABILITY
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


def chebyshev_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Return the Step 2 coverage summaries on whatever sample is passed in.

    Copied so this file stays standalone. main() does not call it; the
    pedagogical close of this step is the IQR flag, not Chebyshev.
    """
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (2, 3)
    }
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "coverage_percent": coverage,
    }


# --- NEW (1) inject_extreme_cases() ------------------------------------------
def inject_extreme_cases(orders: pd.DataFrame) -> pd.DataFrame:
    """Replace four processing times with known synthetic extreme delays.

    Parameters
    ----------
    orders:
        Right-tailed table from add_queue_delays(). It is copied, not
        edited in place.

    Returns
    -------
    pd.DataFrame
        Same rows plus a boolean column known_injected_extreme. Exactly
        four rows are True, and those four times equal INJECTED_DELAYS.

    Notes
    -----
    The construction label exists because the data are synthetic. A real
    operations file almost never tells you in advance which extremes were
    planted. The IQR rule below cannot see this column; it only sees the
    numbers. That is the point of the later comparison.
    """
    # copy() so the delayed sample remains available unchanged if a later
    # line needs it. Assignment into modified would otherwise alias orders.
    modified = orders.copy()
    modified["known_injected_extreme"] = False
    # .loc[row_labels, column] = array writes the four delays in order.
    # The labels 41, 187, 333, 512 are the default integer index, not
    # order_id values.
    modified.loc[INJECTED_ROW_INDICES, "processing_time_minutes"] = INJECTED_DELAYS
    modified.loc[INJECTED_ROW_INDICES, "known_injected_extreme"] = True
    return modified
# ------------------------------------------------------------------------------


# --- NEW (2) flag_with_iqr_rule() --------------------------------------------
def flag_with_iqr_rule(orders: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Flag values outside the conventional 1.5-IQR fences.

    Parameters
    ----------
    orders:
        Table after inject_extreme_cases(), with processing_time_minutes.

    Returns
    -------
    tuple[pd.DataFrame, dict[str, float]]
        A copied table with boolean column flagged_by_iqr_rule, plus a
        dict of Q1, Q3, IQR, and both fences.

    Notes
    -----
    With IQR = Q3 - Q1, the fences are Q1 - 1.5 IQR and Q3 + 1.5 IQR.
    A value beyond either fence is a potential outlier: an investigation
    candidate, not a proven error. The 1.5 multiplier is a convention,
    not a scientific law. Quartiles respond less to the extremes than
    mean +/- k s would, which is why this screen is used after the tail
    and the injections have already stretched the mean and s.
    """
    result = orders.copy()
    values = result["processing_time_minutes"]
    # quantile(0.25) is Q1, the 25th percentile; quantile(0.75) is Q3.
    first_quartile = float(values.quantile(0.25))
    third_quartile = float(values.quantile(0.75))
    interquartile_range = third_quartile - first_quartile
    lower_fence = first_quartile - 1.5 * interquartile_range
    upper_fence = third_quartile + 1.5 * interquartile_range
    # .lt / .gt are element-wise comparisons that return a boolean Series.
    # | is element-wise OR on those Series. The Python keyword `or` cannot
    # combine them; it would try to treat each Series as a single truth value
    # and raise ValueError.
    result["flagged_by_iqr_rule"] = values.lt(lower_fence) | values.gt(upper_fence)
    return result, {
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        "interquartile_range": interquartile_range,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_boxplot_figure() -------------------------------------------
def save_boxplot_figure(
    orders: pd.DataFrame,
    fences: dict[str, float],
) -> Path:
    """Save a boxplot and separate known injections from other IQR flags.

    Parameters
    ----------
    orders:
        Flagged table from flag_with_iqr_rule().
    fences:
        Dict of quartiles and fences used to label the upper-fence line.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    seaborn.boxplot uses whis=1.5 by default, so the whiskers follow the
    same 1.5-IQR rule the function computed. The scatter overlay marks
    every flagged point; the right panel splits those flags into known
    injections versus other values that met the same positional rule.
    The other flags are not automatically false positives.
    """
    output_path = DIR_FIGURES / "anomaly_detection_03_boxplot_flags.png"
    # Boolean indexing: keep rows where the flag is True.
    flagged = orders[orders["flagged_by_iqr_rule"]]
    # .sum() on a boolean Series counts True as 1.
    known_flagged = int(flagged["known_injected_extreme"].sum())
    other_flagged = len(flagged) - known_flagged

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    # x= with no y draws a horizontal boxplot of that one numeric column.
    sns.boxplot(
        data=orders,
        x="processing_time_minutes",
        color="#A7B0BF",
        width=0.35,
        ax=axes[0],
    )
    # y = 0 places each flagged point on the boxplot's center line.
    # zorder=3 draws the points on top of the box.
    axes[0].scatter(
        flagged["processing_time_minutes"],
        np.zeros(len(flagged)),
        color="#EC2661",
        edgecolor="white",
        linewidth=0.6,
        s=44,
        label="IQR rule flag",
        zorder=3,
    )
    # Only the upper fence is drawn: the injected extremes, and the rest
    # of the flags in this right-tailed sample, sit on the high side.
    axes[0].axvline(
        fences["upper_fence"],
        color="#0039A6",
        linestyle="--",
        linewidth=2,
        label=f"Upper fence = {fences['upper_fence']:.2f}",
    )
    axes[0].set_xlabel("Processing time (minutes)", fontsize=12)
    axes[0].set_title("Boxplot and Potential Outliers", fontsize=15)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10, loc="upper right")

    categories = ["Known injected\nextremes", "Other\nrule flags"]
    bars = axes[1].bar(
        categories,
        [known_flagged, other_flagged],
        color=["#1A2E51", "#EC2661"],
        width=0.58,
    )
    axes[1].set_ylabel("Flagged orders", fontsize=12)
    axes[1].set_title("A Flag Does Not Identify Its Cause", fontsize=15)
    axes[1].tick_params(labelsize=10)
    axes[1].set_ylim(0, max(known_flagged, other_flagged) + 5)
    for bar in bars:
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.6,
            f"{int(bar.get_height())}",
            fontsize=12,
            ha="center",
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("The 1.5-IQR Rule Produces Investigation Candidates",
                 fontsize=17, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Inject known extremes, apply the IQR rule, and print verified numbers."""
    delayed_orders, delayed_count = add_queue_delays()
    modified_orders = inject_extreme_cases(delayed_orders)
    flagged_orders, fences = flag_with_iqr_rule(modified_orders)
    figure_path = save_boxplot_figure(flagged_orders, fences)

    flagged = flagged_orders[flagged_orders["flagged_by_iqr_rule"]]
    injected_count = int(flagged_orders["known_injected_extreme"].sum())
    injected_flagged = int(flagged["known_injected_extreme"].sum())
    other_flagged = len(flagged) - injected_flagged

    print("================================================================")
    print("LESSON 04 - STEP 3: BOXPLOT FLAGS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample size (n)                 : {len(flagged_orders):,}")
    print(f"Orders with added queue delay   : {delayed_count}")
    print(f"Known injected extremes         : {injected_count}")
    print(f"First quartile (Q1)             : {fences['first_quartile']:.2f} min")
    print(f"Third quartile (Q3)             : {fences['third_quartile']:.2f} min")
    print(f"Interquartile range (IQR)       : {fences['interquartile_range']:.2f} min")
    print(f"Lower fence                     : {fences['lower_fence']:.2f} min")
    print(f"Upper fence                     : {fences['upper_fence']:.2f} min")
    print(f"Orders flagged by IQR rule      : {len(flagged)}")
    print(f"Injected extremes flagged       : {injected_flagged} of {injected_count}")
    print(f"Other orders flagged            : {other_flagged}")
    print("Interpretation                  : Every flag requires investigation")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

