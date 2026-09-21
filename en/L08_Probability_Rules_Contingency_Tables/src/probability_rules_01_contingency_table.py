"""
Lesson 08 - Step 1: Probabilities from a Contingency Table
==========================================================
NEW IN THIS STEP: build_operations_data(), contingency_table(),
table_probabilities(), and save_contingency_figure().

The Recipe
----------
Build the first complete program in this order:
    1. build_operations_data()   creates 400 shuffled synthetic order records
    2. contingency_table()       cross-classifies routing and delivery status
    3. table_probabilities()     calculates marginal and joint probabilities
    4. save_contingency_figure() exports the count-and-probability evidence

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, pandas
DataFrames, NumPy generators, and unattended savefig. This lesson adds a
two-way count table as the source of probabilities.

New in this step:
    list.extend with a generator  repeat a row-dict count times
    rng.permutation               shuffle row order without changing counts
    DataFrame.iloc + reset_index  apply that shuffle to the table
    pd.crosstab                   two-way frequency table
    table.loc[row, col]           one cell; .sum() on a row or column
    ax.imshow                     heatmap of the four cells

main() builds 400 synthetic orders from fixed cell counts, prints P(M), P(L),
and P(M and L), and saves a labeled heatmap.

Run from the repository root:
    uv run en/L08_Probability_Rules_Contingency_Tables/src/
    probability_rules_01_contingency_table.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
SEED = 42
# The four cells of the contingency table, written as (routing, delivery)
# keys. These counts ARE the population of the lesson: 48+72+32+248 = 400.
TABLE_COUNTS = {
    ("Manual review", "Late"): 48,
    ("Manual review", "On time"): 72,
    ("Automated", "Late"): 32,
    ("Automated", "On time"): 248,
}
ROUTING_ORDER = ["Manual review", "Automated"]
DELIVERY_ORDER = ["Late", "On time"]
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"


# --- NEW (1) build_operations_data() ----------------------------------------
def build_operations_data() -> pd.DataFrame:
    """Create and deterministically shuffle 400 synthetic order records.

    Returns
    -------
    pd.DataFrame
        Columns order_id, routing, delivery. Cell counts match TABLE_COUNTS
        exactly; only the row order is shuffled (seed 42).

    Notes
    -----
    Building from cell counts, then shuffling, gives a realistic-looking
    register without changing the joint distribution. Probabilities later
    depend only on the counts, not on the order of the rows.
    """
    records: list[dict[str, str]] = []
    for (routing, delivery), count in TABLE_COUNTS.items():
        # extend appends `count` copies of the same two-field dict.
        records.extend(
            {"routing": routing, "delivery": delivery}
            for _ in range(count)
        )

    rng = np.random.default_rng(SEED)
    # permutation(n) is a random ordering of 0..n-1. iloc[that] reorders
    # rows. reset_index(drop=True) replaces the old index with 0..399.
    shuffled = rng.permutation(len(records))
    data = pd.DataFrame(records).iloc[shuffled].reset_index(drop=True)
    # insert(0, ...) puts order_id as the leftmost column. SO-001 .. SO-400.
    data.insert(0, "order_id", [f"SO-{i:03d}" for i in range(1, len(data) + 1)])
    return data


# -----------------------------------------------------------------------------


# --- NEW (2) contingency_table() --------------------------------------------
def contingency_table(data: pd.DataFrame) -> pd.DataFrame:
    """Return the fixed-order routing-by-delivery count table.

    pd.crosstab(row_var, col_var) counts every (row, column) pair.
    reindex forces Manual review then Automated on the rows, Late then
    On time on the columns, so the printed table matches the slides.
    fill_value=0 would replace a missing combination with 0; none are
    missing in this lesson.
    """
    return pd.crosstab(data["routing"], data["delivery"]).reindex(
        index=ROUTING_ORDER,
        columns=DELIVERY_ORDER,
        fill_value=0,
    )


# -----------------------------------------------------------------------------


# --- NEW (3) table_probabilities() ------------------------------------------
def table_probabilities(table: pd.DataFrame) -> dict[str, float]:
    """Calculate selected marginal and joint probabilities.

    Parameters
    ----------
    table:
        2x2 count table from contingency_table().

    Returns
    -------
    dict[str, float]
        manual = P(M) = row total / N,
        late = P(L) = column total / N,
        manual_and_late = P(M and L) = one cell / N.

    Notes
    -----
    .loc["Manual review"] is a Series of two cells; .sum() is the row
    total. table["Late"] is the Late column. table.loc[row, col] is one
    integer cell. Dividing by N converts counts into relative frequencies,
    which this finite table treats as probabilities.
    """
    total = int(table.to_numpy().sum())
    manual = int(table.loc["Manual review"].sum())
    late = int(table["Late"].sum())
    manual_and_late = int(table.loc["Manual review", "Late"])
    return {
        "manual": manual / total,
        "late": late / total,
        "manual_and_late": manual_and_late / total,
    }


# -----------------------------------------------------------------------------


# --- NEW (4) save_contingency_figure() --------------------------------------
def save_contingency_figure(table: pd.DataFrame) -> Path:
    """Export a heatmap labeled with cell counts and joint probabilities.

    ax.imshow paints a 2x2 grid. Darker blue = larger count. Each cell is
    annotated with the count and the joint relative frequency as a percent.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probability_01_table.png"

    values = table.to_numpy()
    total = int(values.sum())
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    image = ax.imshow(values, cmap="Blues", vmin=0, vmax=values.max())
    ax.set_xticks(range(len(DELIVERY_ORDER)), DELIVERY_ORDER)
    ax.set_yticks(range(len(ROUTING_ORDER)), ROUTING_ORDER)
    ax.set_xlabel("Delivery status")
    ax.set_ylabel("Routing process")
    ax.set_title(
        "Synthetic Order Contingency Table",
        fontweight="bold",
        pad=12,
    )

    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            count = int(values[row, column])
            # White text on dark cells, navy text on light cells.
            color = "white" if count > values.max() / 2 else TEC_NAVY
            ax.text(
                column,
                row,
                f"{count}\n({count / total:.1%})",
                ha="center",
                va="center",
                color=color,
                fontsize=13,
                fontweight="bold",
            )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Order count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 1 evidence."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    output_path = save_contingency_figure(table)

    print("LESSON 08 - STEP 1: PROBABILITIES FROM A CONTINGENCY TABLE")
    print(f"Synthetic orders                    : {len(data):,}")
    print("Routing x delivery counts:")
    print(table.to_string())
    print(f"P(Manual review)                    : {probabilities['manual']:.4f}")
    print(f"P(Late)                             : {probabilities['late']:.4f}")
    print(
        "P(Manual review AND Late)           : "
        f"{probabilities['manual_and_late']:.4f}"
    )
    print(f"Figure saved to                     : {output_path}")


if __name__ == "__main__":
    main()

