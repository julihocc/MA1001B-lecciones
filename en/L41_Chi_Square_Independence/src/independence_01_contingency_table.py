"""
Lesson 41 - Step 1: A 2 by 3 Contingency Table
==============================================
THE RECIPE
Start from a clean slate. Introduce:
    1. observed_table()     sums rows and columns to find margins
    2. expected_table()     outer product of margins divided by n
    3. save_figure()        grouped bars by outcome

Context:
A fully synthetic checkout register classifies n = 325 visitors by conversion
(yes or no) and by acquisition channel (email, search, social). Under
independence, expected cell counts are row total times column total over n.
We want to compare these expected counts to the observed counts.

How to read this file:
    1. Review the OBSERVED numpy array, the 2x3 contingency table.
    2. Read `observed_table()` to see how we get row and column margins.
    3. Read `expected_table()` to see how the independence assumption generates
       expected counts for each cell.
    4. Scroll down to `main()` to see how these dictionaries are printed.

Run it:
    uv run en/L41_Chi_Square_Independence/src/independence_01_contingency_table.py
"""

from pathlib import Path

import matplotlib
import numpy as np

# We use the Agg backend to render plots without requiring a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# A fixed seed for reproducible random operations, though here counts are static
SEED = 42

# The levels of our two categorical variables
CHANNELS = ("Email", "Search", "Social")
OUTCOMES = ("Converted", "Not converted")

# The synthetic 2 by 3 contingency table (rows=outcomes, cols=channels)
# Explicitly float so we don't encounter integer division issues later
OBSERVED = np.array([[40, 55, 18], [80, 70, 62]], dtype=float)

# Resolve the directory where our output figure will be saved
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) observed_table() ------------------------------------------------
def observed_table() -> dict[str, np.ndarray | float]:
    """
    Return the 2 by 3 observed checkout table and its margins.

    Returns:
        dict: A dictionary containing:
            - 'observed': The 2D array of observed counts.
            - 'row_totals': The sum of counts for each row.
            - 'col_totals': The sum of counts for each column.
            - 'n': The total number of observations.

    Notes:
        Row totals correspond to total converted vs total not converted.
        Column totals correspond to total visitors per channel.
    """
    # Sum across columns (axis=1) to get the row totals
    row_totals = OBSERVED.sum(axis=1)

    # Sum across rows (axis=0) to get the column totals
    col_totals = OBSERVED.sum(axis=0)

    return {
        "observed": OBSERVED.copy(),
        "row_totals": row_totals,
        "col_totals": col_totals,
        "n": float(OBSERVED.sum()),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) expected_table() ------------------------------------------------
def expected_table(observed: np.ndarray) -> dict[str, np.ndarray | float]:
    """
    Independence expected counts E = row total * column total / n.

    Parameters:
        observed (np.ndarray): The 2D array of observed counts.

    Returns:
        dict: A dictionary containing:
            - 'expected': The 2D array of expected cell counts.
            - 'min_expected': The smallest expected cell count.
            - 'all_expected_ge_5': A float acting as boolean (1.0 if all >= 5, else 0.0).

    Notes:
        The expected count for a cell (i, j) under independence is
        P(row i) * P(col j) * n = (Row i total / n) * (Col j total / n) * n
        = (Row i total * Col j total) / n.
        np.outer() efficiently computes this matrix product.
    """
    n = observed.sum()

    # The expected count matrix under the null hypothesis of independence
    expected = np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n

    return {
        "expected": expected,
        "min_expected": float(np.min(expected)),
        "all_expected_ge_5": float(np.all(expected >= 5.0)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(observed: np.ndarray) -> Path:
    """
    Grouped bars of conversion counts by acquisition channel.

    Parameters:
        observed (np.ndarray): The 2D array of observed counts.

    Returns:
        Path: The absolute path where the PNG is saved.

    Notes:
        We plot two bars side-by-side for each channel to visually compare
        the number of converted vs. not converted visitors.
    """
    output_path = DIR_FIGURES / "independence_01_contingency_table.png"

    # Define positions for the bars on the x-axis
    x = np.arange(len(CHANNELS))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot 'Converted' bars slightly to the left
    ax.bar(x - width / 2, observed[0], width, color="#EC2661", label="Converted")

    # Plot 'Not converted' bars slightly to the right
    ax.bar(x + width / 2, observed[1], width, color="#1A2E51", label="Not converted")

    # Add axis labels, title, and formatting
    ax.set_xticks(x, CHANNELS)
    ax.set_ylabel("Visitor count")
    ax.set_title("Synthetic 2 by 3 Checkout Table, n = 325")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    observed = observed_table()
    expected = expected_table(observed["observed"])
    figure_path = save_figure(observed["observed"])

    print("================================================================")
    print("LESSON 41 - STEP 1: CONTINGENCY TABLE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {int(observed['n'])}")
    print("Observed converted               : 40, 55, 18")
    print("Observed not converted           : 80, 70, 62")
    print(
        "Row totals                      : "
        + ", ".join(f"{value:.0f}" for value in observed["row_totals"])
    )
    print(
        "Column totals                   : "
        + ", ".join(f"{value:.0f}" for value in observed["col_totals"])
    )
    print(
        "Expected converted              : "
        + ", ".join(f"{value:.3f}" for value in expected["expected"][0])
    )
    print(
        "Expected not converted          : "
        + ", ".join(f"{value:.3f}" for value in expected["expected"][1])
    )
    print(f"Minimum expected count          : {expected['min_expected']:.6f}")
    print(
        "All expected counts >= 5        : "
        f"{'yes' if expected['all_expected_ge_5'] else 'no'}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

