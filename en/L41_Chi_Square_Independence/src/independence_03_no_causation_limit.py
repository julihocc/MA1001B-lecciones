"""
Lesson 41 - Step 3: Significant Association Is Not a Causal Claim
=================================================================
THE RECIPE
Start from independence_02_chi_square.py, then introduce:
    1. device_strata()          desktop and mobile tables that add to the 2x3
    2. stratified_tests()       independence p-values inside each device
    3. save_figure()            conversion rates by channel, overall vs strata

Context:
The combined table can reject independence. However, after stratifying by device
(a confounder that was not randomly assigned), the channel association vanishes.
This demonstrates Simpson's Paradox and reinforces that a significant chi-square
test is not a causal claim.

How to read this file:
    1. Check `device_strata()` to see how the total data is split by a third variable.
    2. Look at `stratified_tests()` calculating chi-square and conversion rates per device.
    3. Notice how the p-values inside each stratum are no longer significant,
       even though the combined table's p-value was.

Run it:
    uv run en/L41_Chi_Square_Independence/src/independence_03_no_causation_limit.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# We use the Agg backend to render plots without requiring a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# A fixed seed for reproducible random operations
SEED = 42

# The levels of our channel variable
CHANNELS = ("Email", "Search", "Social")

# Strata tables for Desktop and Mobile.
# Notice their sum equals the combined 2x3 table from previous steps.
DESKTOP = np.array([[30, 50, 8], [20, 30, 10]], dtype=float)
MOBILE = np.array([[10, 5, 10], [60, 40, 52]], dtype=float)

# Our chosen significance level
ALPHA = 0.05

# Resolve the directory where our output figure will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) device_strata() -------------------------------------------------
def device_strata() -> dict[str, np.ndarray]:
    """
    Return device tables whose sum is the original 2 by 3 register.

    Returns:
        dict: A dictionary containing:
            - 'desktop': The observed counts for desktop users.
            - 'mobile': The observed counts for mobile users.
            - 'combined': The sum of desktop and mobile counts.

    Notes:
        We stratify our contingency table across a third variable (device type)
        to look for confounding effects.
    """
    combined = DESKTOP + MOBILE
    return {"desktop": DESKTOP.copy(), "mobile": MOBILE.copy(), "combined": combined}
# ------------------------------------------------------------------------------


# --- NEW (2) stratified_tests() ----------------------------------------------
def stratified_tests(tables: dict[str, np.ndarray]) -> dict[str, float]:
    """
    Chi-square p-values overall and inside each device stratum.

    Parameters:
        tables (dict): A mapping from stratum names to their contingency tables.

    Returns:
        dict: A dictionary of chi-square test metrics and conversion rates
              per channel, keyed by stratum name.

    Notes:
        A significant association in the combined table may disappear when
        testing within sub-populations, showing the limits of observational data.
    """
    results = {}

    # Iterate through our combined, desktop, and mobile tables
    for name, table in tables.items():
        # Perform chi-square test
        chi2, p_value, df, _ = stats.chi2_contingency(table, correction=False)

        results[f"{name}_chi2"] = float(chi2)
        results[f"{name}_p"] = float(p_value)
        results[f"{name}_df"] = float(df)

        # Calculate conversion rates per channel (row 0 / col total)
        rates = table[0] / table.sum(axis=0)
        results[f"{name}_rate_email"] = float(rates[0])
        results[f"{name}_rate_search"] = float(rates[1])
        results[f"{name}_rate_social"] = float(rates[2])

    return results
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(results: dict[str, float]) -> Path:
    """
    Conversion rates by channel overall and within device strata.

    Parameters:
        results (dict): The test and rate outputs from `stratified_tests()`.

    Returns:
        Path: The absolute path where the PNG is saved.

    Notes:
        We plot the conversion rates side-by-side to visually show how
        the overall trend differs from the trend inside specific devices.
    """
    output_path = DIR_FIGURES / "independence_03_no_causation_limit.png"

    # Define positions for the bars on the x-axis
    x = np.arange(len(CHANNELS))
    width = 0.25

    # Extract conversion rates into lists corresponding to our channels
    overall = [
        results["combined_rate_email"],
        results["combined_rate_search"],
        results["combined_rate_social"],
    ]
    desktop = [
        results["desktop_rate_email"],
        results["desktop_rate_search"],
        results["desktop_rate_social"],
    ]
    mobile = [
        results["mobile_rate_email"],
        results["mobile_rate_search"],
        results["mobile_rate_social"],
    ]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot bars side-by-side: left (overall), middle (desktop), right (mobile)
    ax.bar(x - width, overall, width, color="#EC2661", label="Overall")
    ax.bar(x, desktop, width, color="#1A2E51", label="Desktop")
    ax.bar(x + width, mobile, width, color="#5B8DEF", label="Mobile")

    # Add axis labels, title, and formatting
    ax.set_xticks(x, CHANNELS)
    ax.set_ylabel("Conversion rate")
    ax.set_title("Channel Association Vanishes inside Device Strata")
    ax.set_ylim(0, 0.85)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    tables = device_strata()
    results = stratified_tests(tables)
    figure_path = save_figure(results)

    print("================================================================")
    print("LESSON 41 - STEP 3: NO CAUSATION LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Combined chi-square p-value     : {results['combined_p']:.6f}")
    print(f"Desktop chi-square p-value      : {results['desktop_p']:.6f}")
    print(f"Mobile chi-square p-value       : {results['mobile_p']:.6f}")
    print(f"Combined conversion Search      : {results['combined_rate_search']:.6f}")
    print(f"Combined conversion Social      : {results['combined_rate_social']:.6f}")
    print(f"Desktop conversion Search       : {results['desktop_rate_search']:.6f}")
    print(f"Mobile conversion Social        : {results['mobile_rate_social']:.6f}")
    print("Random assignment of channel    : no")
    print("Causal claim from chi-square    : not justified")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

