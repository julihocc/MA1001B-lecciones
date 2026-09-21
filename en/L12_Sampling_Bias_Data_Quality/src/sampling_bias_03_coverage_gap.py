"""
Lesson 12 - Step 3: Coverage Gap, Missingness, and Cleaning
===========================================================
THE RECIPE
Start from sampling_bias_02_convenience_web.py, then introduce:
    1. coverage_gap_frame()     drop the West region from the sampling frame
    2. clean_incomplete_rows()  listwise deletion of missing complaint flags
    3. save_figure()            cleaning a biased frame does not restore West

West tickets have a higher complaint rate and a higher missingness rate. A
frame that never included West, then "cleaned" of incomplete rows, still
contains zero West units. Nonsampling error is not sampling error.

How to read this file:
You already know Python through OOP. Steps 1-2 introduced the register, the
SRS, and the Web convenience sample. Those functions are copied here so the
script stays self-contained; they are commented only where this file does
something new. Lesson 01 remains the reference for pathlib, Agg, Boolean
filters, and comparison tables; Lesson 02 remains the reference for SRS.

New in this step:
    coverage-gap filter     keep every region except West
    DataFrame.copy()        detach the incomplete frame from the register
    listwise deletion       drop any row whose complaint flag is missing
    four-way error bars     SRS, Web-only, no-West, cleaned no-West
    West count after clean  stays 0 because West was never in the frame

main() drops West from the frame, cleans missing flags, and shows that
tidying the table restores no West tickets.

Run it:
    uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_03_coverage_gap.py
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
CONVENIENCE_SIZE = 1_200
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_register(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same synthetic register introduced in Step 1.

    The generator, seed, and columns are identical so the three scripts
    describe one world. See Step 1 for np.repeat, shuffle, Bernoulli
    flags, and the West missingness design.
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
    """Draw the simple random sample introduced in Step 1."""
    return register.sample(n=sample_size, replace=False, random_state=seed)


def draw_web_convenience(
    register: pd.DataFrame,
    sample_size: int = CONVENIENCE_SIZE,
) -> pd.DataFrame:
    """Take the first available Web tickets as in Step 2.

    Boolean filter on channel, then head(n). See Step 2 for the convenience
    sampling comments.
    """
    web_tickets = register.loc[register["channel"] == "Web"]
    if len(web_tickets) < sample_size:
        raise ValueError("The synthetic register has too few Web tickets.")
    return web_tickets.head(sample_size)


# --- NEW (1) coverage_gap_frame() --------------------------------------------
def coverage_gap_frame(register: pd.DataFrame) -> pd.DataFrame:
    """Return the operational frame that never included the West region.

    Parameters
    ----------
    register:
        Complete 8,000-row register from build_register().

    Returns
    -------
    pd.DataFrame
        North, South, and East tickets only. West is absent, not missing
        at random inside the frame.

    Notes
    -----
    A coverage gap is a frame problem: some units in the target population
    have no chance of selection because they were never listed. That is
    nonsampling error. Cleaning later rows cannot put West back.
    """
    # != "West" is a boolean Series. .loc keeps North, South, and East.
    # .copy() detaches this slice so later cleaning cannot write through
    # to the full register.
    return register.loc[register["region"] != "West"].copy()
# ------------------------------------------------------------------------------


# --- NEW (2) clean_incomplete_rows() -----------------------------------------
def clean_incomplete_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows whose complaint flag is missing (listwise deletion).

    Parameters
    ----------
    frame:
        The operational table being cleaned. In this step it is already
        the no-West coverage-gap frame.

    Returns
    -------
    pd.DataFrame
        Rows with complaint_missing == 0. The table is tidier; the
        coverage gap is unchanged.

    Notes
    -----
    Listwise deletion drops the entire ticket if one field is missing.
    It is a data-quality operation, not a sampling design. Because West
    was already excluded, the cleaned table still contains zero West
    units even though West had the highest missingness rate.
    """
    # complaint_missing == 0 keeps rows whose flag was observed.
    # .copy() again so the cleaned table is independent of `frame`.
    return frame.loc[frame["complaint_missing"] == 0].copy()
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    population_rate: float,
    srs_error: float,
    convenience_error: float,
    coverage_error: float,
    cleaned_error: float,
    west_after_cleaning: int,
) -> Path:
    """Contrast errors and show that cleaning restores no West tickets.

    Parameters
    ----------
    population_rate:
        Full-register complaint rate, shown in the figure title.
    srs_error, convenience_error, coverage_error, cleaned_error:
        Absolute errors of the four estimators, in that left-to-right
        bar order.
    west_after_cleaning:
        Count of West tickets remaining after listwise deletion of the
        no-West frame. The pedagogical value is 0.

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file.

    Notes
    -----
    Left panel: sampling error (SRS) versus selection bias (Web only)
    versus coverage error (no West) versus "cleaned" coverage error.
    Right panel: 1,200 West tickets in the population, zero after
    cleaning a frame that never listed them.
    """
    output_path = DIR_FIGURES / "sampling_bias_03_coverage_gap.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["SRS", "Web only", "No West", "Cleaned\nno-West"]
    errors = [srs_error, convenience_error, coverage_error, cleaned_error]
    colors = ["#5B8DEF", "#EC2661", "#1A2E51", "#F4A6B8"]

    axes[0].bar(labels, errors, color=colors, width=0.62)
    axes[0].set_ylabel("Absolute error")
    axes[0].set_title("Error from the population rate")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(errors):
        axes[0].text(idx, value + 0.002, f"{value:.3f}", ha="center", fontsize=8)

    # 1200 is the designed West size from build_register, not a computed
    # count, so the right panel still shows the coverage gap if a later
    # edit changed west_after_cleaning.
    axes[1].bar(
        ["West in\npopulation", "West after\ncleaning"],
        [1200, west_after_cleaning],
        color=["#1A2E51", "#EC2661"],
        width=0.55,
    )
    axes[1].set_ylabel("West tickets")
    axes[1].set_title("Cleaning does not restore missing units")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    axes[1].text(0, 1200 + 30, "1200", ha="center", fontsize=8)
    axes[1].text(1, west_after_cleaning + 30, str(west_after_cleaning), ha="center", fontsize=8)

    fig.suptitle(f"Population complaint rate = {population_rate:.4f}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Drop West, clean missing flags, and print the coverage-gap limit."""
    register = build_register()
    srs = draw_srs(register)
    convenience = draw_web_convenience(register)
    frame = coverage_gap_frame(register)
    cleaned = clean_incomplete_rows(frame)

    population_rate = float(register["complaint"].mean())
    # Same Boolean-filter pattern as Step 2, now on region. West is the
    # high-complaint stratum the coverage gap removes; "other" is what
    # remains in the operational frame.
    west_rate = float(register.loc[register["region"] == "West", "complaint"].mean())
    other_rate = float(register.loc[register["region"] != "West", "complaint"].mean())
    missing_total = int(register["complaint_missing"].sum())
    missing_west = int(
        register.loc[register["region"] == "West", "complaint_missing"].sum()
    )
    srs_rate = float(srs["complaint"].mean())
    conv_rate = float(convenience["complaint"].mean())
    coverage_rate = float(frame["complaint"].mean())
    cleaned_rate = float(cleaned["complaint"].mean())
    # Sum of a boolean Series counts True as 1. After cleaning a no-West
    # frame this value is 0: listwise deletion cannot restore units that
    # were never listed.
    west_after_cleaning = int((cleaned["region"] == "West").sum())

    srs_error = abs(srs_rate - population_rate)
    conv_error = abs(conv_rate - population_rate)
    coverage_error = abs(coverage_rate - population_rate)
    cleaned_error = abs(cleaned_rate - population_rate)
    figure_path = save_figure(
        population_rate,
        srs_error,
        conv_error,
        coverage_error,
        cleaned_error,
        west_after_cleaning,
    )

    print("================================================================")
    print("LESSON 12 - STEP 3: COVERAGE GAP AND CLEANING")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Population complaint rate       : {population_rate:.6f}")
    print(f"West complaint rate             : {west_rate:.6f}")
    print(f"Non-West complaint rate         : {other_rate:.6f}")
    print(f"Missing complaint flags         : {missing_total:,}")
    print(f"Missing flags in West           : {missing_west:,}")
    print(f"SRS absolute error              : {srs_error:.6f}")
    print(f"Web-convenience absolute error  : {conv_error:.6f}")
    print(f"No-West frame size              : {len(frame):,}")
    print(f"No-West frame rate              : {coverage_rate:.6f}")
    print(f"No-West absolute error          : {coverage_error:.6f}")
    print(f"Cleaned no-West size            : {len(cleaned):,}")
    print(f"Cleaned no-West rate            : {cleaned_rate:.6f}")
    print(f"Cleaned no-West absolute error  : {cleaned_error:.6f}")
    print(f"West tickets after cleaning     : {west_after_cleaning}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

