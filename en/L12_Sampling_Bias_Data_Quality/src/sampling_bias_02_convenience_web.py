"""
Lesson 12 - Step 2: Convenience Sample from Web-Only Tickets
===========================================================
THE RECIPE
Start from sampling_bias_01_srs.py, then introduce:
    1. draw_web_convenience()   take a large sample from the Web channel only
    2. compare_estimates()      SRS error versus convenience error
    3. save_figure()            sample size does not repair selection bias

The same 8,000-row synthetic register is rebuilt with SEED = 42. No earlier
lesson script is imported. Web tickets have a lower complaint rate, so a
larger web-only sample can miss the population parameter by more than the SRS.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, Agg,
unattended savefig, Boolean filters, DataFrame.head, and comparison tables.
Lesson 02 introduced DataFrame.sample. Step 1 built this ticket register and
drew the SRS. Those pieces are copied here so the script stays self-contained;
they are commented only where this file does something new.

New in this step:
    Boolean channel filter   register.loc[register["channel"] == "Web"]
    DataFrame.head(n)        first n Web tickets in current table order
    raise ValueError         fail loudly if the Web slice is too small
    list-of-dicts -> table   assemble the SRS-versus-convenience comparison
    Series.iloc[0]           pick one row of that comparison table
    two-panel bar chart      sample size versus absolute error

main() rebuilds the register, draws the n=400 SRS and the n=1,200 Web
convenience sample, and shows that the larger sample can have more error.

Run it:
    uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_02_convenience_web.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_ROWS = 8_000
SRS_SIZE = 400
# Intentionally three times the SRS. Extra rows do not repair a biased
# selection rule: the sample never sees Store tickets.
CONVENIENCE_SIZE = 1_200
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_register(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic register introduced in Step 1.

    The generator, seed, and columns are identical so the two scripts
    describe one world. See Step 1 for np.repeat, shuffle, and Bernoulli
    commentary.
    """
    rng = np.random.default_rng(seed)
    regions = np.repeat(
        np.array(["North", "South", "East", "West"]),
        np.array([2400, 2400, 2000, 1200]),
    )
    rng.shuffle(regions)
    p_web = {"North": 0.45, "South": 0.40, "East": 0.75, "West": 0.20}
    p_web_arr = np.array([p_web[region] for region in regions])
    channel = np.where(rng.random(N_ROWS) < p_web_arr, "Web", "Store")
    p_complaint = np.where(channel == "Web", 0.05, 0.14)
    p_complaint = p_complaint + np.where(regions == "West", 0.16, 0.00)
    complaint = (rng.random(N_ROWS) < p_complaint).astype(int)
    p_missing = np.where(regions == "West", 0.22, 0.05)
    complaint_missing = (rng.random(N_ROWS) < p_missing).astype(int)
    recorded = complaint.astype(float)
    recorded[complaint_missing == 1] = np.nan
    return pd.DataFrame(
        {
            "ticket_id": np.arange(100_001, 100_001 + N_ROWS),
            "region": regions,
            "channel": channel,
            "complaint": complaint,
            "complaint_missing": complaint_missing,
            "complaint_recorded": recorded,
        }
    )


def draw_srs(
    register: pd.DataFrame,
    sample_size: int = SRS_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw the simple random sample introduced in Step 1.

    Same DataFrame.sample call as Lesson 02 and Step 1: n distinct tickets,
    without replacement, pinned by random_state.
    """
    return register.sample(n=sample_size, replace=False, random_state=seed)


# --- NEW (1) draw_web_convenience() ------------------------------------------
def draw_web_convenience(
    register: pd.DataFrame,
    sample_size: int = CONVENIENCE_SIZE,
) -> pd.DataFrame:
    """Take the first available Web tickets as a convenience sample.

    Parameters
    ----------
    register:
        Full ticket register. Must contain a channel column.
    sample_size:
        How many Web rows to keep. Default is 1,200, three times the
        SRS size.

    Returns
    -------
    pd.DataFrame
        The first sample_size Web rows in the table's current order.

    Raises
    ------
    ValueError
        If the synthetic register has fewer Web tickets than sample_size.
        That would be a bug in the generator, not a sampling result.

    Notes
    -----
    A convenience sample is defined by an easy access rule, not by equal
    chance. Here the rule is "take Web tickets from the top of the table."
    Web tickets were generated with a lower complaint probability, so this
    slice systematically understates the population rate. There is no
    random_state because the selection is not a probability sample.
    """
    # register["channel"] == "Web" is a boolean Series, True on Web rows.
    # .loc[boolean_series] keeps only the True rows. This is pandas Boolean
    # indexing, not Python's list.filter. Lesson 01 Step 3 uses the same
    # pattern on a channel column.
    web_tickets = register.loc[register["channel"] == "Web"]
    if len(web_tickets) < sample_size:
        raise ValueError("The synthetic register has too few Web tickets.")
    # head(n) returns the first n rows in whatever order the table currently
    # has (here, the shuffled generation order). It is the software image of
    # "grab the first records that are easy to reach."
    return web_tickets.head(sample_size)
# ------------------------------------------------------------------------------


# --- NEW (2) compare_estimates() ---------------------------------------------
def compare_estimates(
    register: pd.DataFrame,
    srs: pd.DataFrame,
    convenience: pd.DataFrame,
) -> pd.DataFrame:
    """Compare each sample complaint rate with the population parameter.

    Parameters
    ----------
    register:
        Full frame; its complaint mean is the parameter.
    srs, convenience:
        The two samples to score.

    Returns
    -------
    pd.DataFrame
        Two rows (SRS, Web convenience) and four columns: sample, size,
        rate, and absolute_error. Building a small table from a list of
        dicts is a standard pandas pattern: each dict is one row, the
        keys become column names.

    Notes
    -----
    absolute_error = |sample rate - population rate|. The sign is dropped
    so the later bar chart can compare magnitudes directly. Same
    list-of-dicts pattern as Lesson 01 Step 3 and Lesson 02 Step 2.
    """
    population_rate = float(register["complaint"].mean())
    rows = []
    for label, sample in [("SRS", srs), ("Web convenience", convenience)]:
        sample_rate = float(sample["complaint"].mean())
        rows.append(
            {
                "sample": label,
                "size": len(sample),
                "rate": sample_rate,
                "absolute_error": abs(sample_rate - population_rate),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(comparison: pd.DataFrame) -> Path:
    """Save sample sizes beside absolute errors for SRS and web convenience.

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
    Left panel: how many tickets each sample used. Right panel: how far
    each sample rate sat from the population rate. Reading the two panels
    together is the lesson: the Web convenience sample is taller on the
    left and taller on the right.
    """
    output_path = DIR_FIGURES / "sampling_bias_02_convenience_web.png"
    colors = ["#5B8DEF", "#EC2661"]
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))

    axes[0].bar(comparison["sample"], comparison["size"], color=colors, width=0.55)
    axes[0].set_title("Sample size")
    axes[0].set_ylabel("Tickets")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    axes[1].bar(
        comparison["sample"],
        comparison["absolute_error"],
        color=colors,
        width=0.55,
    )
    axes[1].set_title("Absolute error from population rate")
    axes[1].set_ylabel("Absolute error")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.suptitle("A Larger Web-Only Sample Can Produce More Error")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the SRS-versus-convenience comparison and print the verdict."""
    register = build_register()
    srs = draw_srs(register)
    convenience = draw_web_convenience(register)
    comparison = compare_estimates(register, srs, convenience)
    population_rate = float(register["complaint"].mean())
    # Boolean filter on channel, then the complaint column, then the mean.
    # These two rates explain the direction of the convenience-sample bias:
    # Web is lower than the population; Store is higher.
    web_rate = float(register.loc[register["channel"] == "Web", "complaint"].mean())
    store_rate = float(
        register.loc[register["channel"] == "Store", "complaint"].mean()
    )
    # comparison["sample"] == "SRS" is a boolean mask. .loc[mask] keeps the
    # matching row (still a one-row DataFrame). .iloc[0] then converts that
    # one-row table into a Series so we can write srs_row["rate"].
    srs_row = comparison.loc[comparison["sample"] == "SRS"].iloc[0]
    conv_row = comparison.loc[comparison["sample"] == "Web convenience"].iloc[0]
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LESSON 12 - STEP 2: WEB CONVENIENCE SAMPLE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Population complaint rate       : {population_rate:.6f}")
    print(f"Web-channel complaint rate      : {web_rate:.6f}")
    print(f"Store-channel complaint rate    : {store_rate:.6f}")
    print(f"SRS size n                      : {int(srs_row['size']):,}")
    print(f"SRS complaint rate              : {srs_row['rate']:.6f}")
    print(f"SRS absolute error              : {srs_row['absolute_error']:.6f}")
    print(f"Convenience size n              : {int(conv_row['size']):,}")
    print(f"Convenience complaint rate      : {conv_row['rate']:.6f}")
    print(f"Convenience absolute error      : {conv_row['absolute_error']:.6f}")
    # A boolean printed as True/False. This is the pedagogical punch line:
    # the 1,200-row Web sample misses the parameter by more than the 400-row
    # SRS. Sample size did not repair the selection rule.
    print(
        "Larger sample has more error    : "
        f"{conv_row['absolute_error'] > srs_row['absolute_error']}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

