"""
Lesson 12 - Step 1: Simple Random Sample from a Complete Register
=================================================================
NEW IN THIS STEP: build_register(), draw_srs(), and save_figure().

Context:
A fully synthetic 8,000-row service-ticket register records region, channel,
and a complaint flag. The population parameter is the complaint rate. A simple
random sample of 400 tickets estimates that rate with sampling error only.

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy,
pandas, the Agg backend, DataFrame.sample, and unattended savefig. Lesson 02
used those same sampling idioms on a complete frame. They return here with a
short pointer, not a second treatise.

New in this step:
    np.repeat(labels, counts)  expand four region names to unequal sizes
    rng.shuffle                mix the stacked region blocks in place
    np.where + Uniform draws   Bernoulli channel, complaint, and missing flags
    0/1 column mean            the complaint rate (a proportion)
    np.nan in a float column   recorded complaint when the flag is missing
    two-bar comparison         population parameter beside the SRS estimate

main() builds the 8,000-ticket register, draws one SRS of 400 tickets, reports
the population rate, the SRS rate, and the absolute error, and writes the
evidence figure.

Run it:
    uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_01_srs.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_ROWS = 8_000
SRS_SIZE = 400
# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_register() ------------------------------------------------
def build_register(seed: int = SEED) -> pd.DataFrame:
    """Build the synthetic 8,000-row ticket register used in every step.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's Generator so Steps 2 and 3 rebuild
        the same 8,000 tickets. Default is the module-level SEED.

    Returns
    -------
    pd.DataFrame
        One row per ticket. Columns: ticket_id, region, channel,
        complaint, complaint_missing, and complaint_recorded. Nothing is
        read from disk; every value is generated in memory.

    Notes
    -----
    Region sizes are unequal (West is the smallest). Web share, complaint
    risk, and missingness all vary by region or channel. Those design
    choices become the convenience-sample and coverage-gap stories in
    Steps 2 and 3; Step 1 only needs the complete frame and its rate.
    """
    rng = np.random.default_rng(seed)
    # np.repeat(labels, counts) expands each region name that many times.
    # West is the smallest stratum (1,200 of 8,000). Lesson 02 used equal
    # region sizes; unequal sizes here make a dropped region more costly.
    regions = np.repeat(
        np.array(["North", "South", "East", "West"]),
        np.array([2400, 2400, 2000, 1200]),
    )
    # shuffle mixes the stacked blocks in place so later "first Web rows"
    # are not a pure North-then-South slice. Same seed => same order.
    rng.shuffle(regions)
    p_web = {"North": 0.45, "South": 0.40, "East": 0.75, "West": 0.20}
    # Per-ticket Web probability, looked up from that ticket's region.
    p_web_arr = np.array([p_web[region] for region in regions])
    # rng.random(N) draws Uniform(0, 1). True where the draw is below the
    # regional Web probability: a Bernoulli trial with heterogeneous p.
    # np.where(condition, "Web", "Store") writes the channel labels.
    channel = np.where(rng.random(N_ROWS) < p_web_arr, "Web", "Store")
    # Web tickets complain less often (0.05) than Store tickets (0.14).
    # A Web-only sample will therefore understate the population rate.
    p_complaint = np.where(channel == "Web", 0.05, 0.14)
    # West adds 0.16 to the complaint probability. Dropping West from the
    # frame in Step 3 therefore understates the population rate again.
    p_complaint = p_complaint + np.where(regions == "West", 0.16, 0.00)
    # Another Bernoulli: 1 = complaint, 0 = no complaint. The mean of this
    # 0/1 column is the population complaint rate.
    complaint = (rng.random(N_ROWS) < p_complaint).astype(int)
    # Missingness is also higher in West (0.22 vs 0.05). Listwise deletion
    # in Step 3 will therefore drop West rows faster than the other regions.
    p_missing = np.where(regions == "West", 0.22, 0.05)
    complaint_missing = (rng.random(N_ROWS) < p_missing).astype(int)
    # recorded starts as a float copy of complaint so np.nan can be stored.
    # Integer columns cannot hold NaN; float64 can.
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
# ------------------------------------------------------------------------------


# --- NEW (2) draw_srs() ------------------------------------------------------
def draw_srs(
    register: pd.DataFrame,
    sample_size: int = SRS_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Draw a simple random sample without replacement from the full register.

    Parameters
    ----------
    register:
        The complete sampling frame from build_register().
    sample_size:
        Number of distinct tickets to keep. Default SRS_SIZE is 400.
    seed:
        Forwarded to pandas as random_state so the same 400 rows are
        selected on every run.

    Returns
    -------
    pd.DataFrame
        sample_size rows; the register itself is not modified.

    Notes
    -----
    Same DataFrame.sample idiom as Lesson 02. Every subset of 400 distinct
    tickets is equally likely. The only error in Step 1 is sampling error.
    """
    return register.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(population_rate: float, srs_rate: float) -> Path:
    """Save the population complaint rate next to the SRS estimate.

    Parameters
    ----------
    population_rate, srs_rate:
        Parameter mu and the SRS statistic, both as proportions in [0, 1].

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Two bars, one parameter and one estimate. An SRS from a complete frame
    tracks the population rate up to sampling error; later steps add
    selection bias and a coverage gap on the same register.
    """
    output_path = DIR_FIGURES / "sampling_bias_01_srs.png"
    labels = ["Population\nparameter", "SRS n=400\nestimate"]
    values = [population_rate, srs_rate]
    colors = ["#1A2E51", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Complaint rate")
    ax.set_title("Simple Random Sample Tracks the Population Rate")
    ax.set_ylim(0, 0.25)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each BarContainer patch with its numeric height so the
    # label sits at the visual center of the bar, slightly above the top.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Draw one SRS, print the verified numbers, and save the figure."""
    register = build_register()
    srs = draw_srs(register)
    # Mean of a 0/1 column is the complaint rate (a proportion). float()
    # unwraps the NumPy scalar so the printed value is a plain Python float.
    population_rate = float(register["complaint"].mean())
    srs_rate = float(srs["complaint"].mean())
    abs_error = abs(srs_rate - population_rate)
    # value_counts() tallies tickets per region; to_dict() makes key lookup
    # in the print block (region_counts["North"]) straightforward.
    region_counts = register["region"].value_counts().to_dict()
    figure_path = save_figure(population_rate, srs_rate)

    print("================================================================")
    print("LESSON 12 - STEP 1: SIMPLE RANDOM SAMPLE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Register rows N                 : {len(register):,}")
    print(f"North tickets                   : {region_counts['North']:,}")
    print(f"South tickets                   : {region_counts['South']:,}")
    print(f"East tickets                    : {region_counts['East']:,}")
    print(f"West tickets                    : {region_counts['West']:,}")
    print(f"Population complaint rate       : {population_rate:.6f}")
    print(f"SRS size n                      : {len(srs):,}")
    print(f"SRS complaint rate              : {srs_rate:.6f}")
    print(f"SRS absolute error              : {abs_error:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

