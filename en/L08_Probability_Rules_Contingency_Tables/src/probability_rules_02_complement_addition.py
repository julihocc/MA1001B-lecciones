"""
Lesson 08 - Step 2: Complement and Addition Rules
=================================================
NEW IN THIS STEP: complement_and_union() and save_addition_figure().

Changes from probability_rules_01_contingency_table.py
The Recipe
----------
Introduce these changes in order:
    1. complement_and_union() calculates complements and overlap-corrected OR
    2. save_addition_figure() compares naive addition with the correct union

How to read this file:
You already know Python through OOP. Step 1 built the 400-order table and
computed P(M), P(L), and P(M and L). This step uses those three numbers
to form the complement and the addition rule.

New in this step:
    complement            P(M^c) = 1 - P(M)
    naive union           P(M)+P(L) double-counts the intersection
    addition rule         P(M or L) = P(M)+P(L)-P(M and L)
    boolean OR on columns (routing==M) | (delivery==Late)
    Series.mean()         on 0/1 values equals a proportion
    ax.annotate           arrow calling out the subtracted overlap

main() prints the complement 0.70, the naive sum 0.50, and the corrected
union 0.38, then confirms 0.38 by counting rows directly.

Run from the repository root:
    uv run en/L08_Probability_Rules_Contingency_Tables/src/
    probability_rules_02_complement_addition.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
SEED = 42
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
TEC_PINK = "#EC2661"


def build_operations_data() -> pd.DataFrame:
    """Create and deterministically shuffle 400 synthetic order records."""
    records: list[dict[str, str]] = []
    for (routing, delivery), count in TABLE_COUNTS.items():
        records.extend(
            {"routing": routing, "delivery": delivery}
            for _ in range(count)
        )

    rng = np.random.default_rng(SEED)
    shuffled = rng.permutation(len(records))
    data = pd.DataFrame(records).iloc[shuffled].reset_index(drop=True)
    data.insert(0, "order_id", [f"SO-{i:03d}" for i in range(1, len(data) + 1)])
    return data


def contingency_table(data: pd.DataFrame) -> pd.DataFrame:
    """Return the fixed-order routing-by-delivery count table."""
    return pd.crosstab(data["routing"], data["delivery"]).reindex(
        index=ROUTING_ORDER,
        columns=DELIVERY_ORDER,
        fill_value=0,
    )


def table_probabilities(table: pd.DataFrame) -> dict[str, float]:
    """Calculate selected marginal and joint probabilities."""
    total = int(table.to_numpy().sum())
    manual = int(table.loc["Manual review"].sum())
    late = int(table["Late"].sum())
    manual_and_late = int(table.loc["Manual review", "Late"])
    return {
        "manual": manual / total,
        "late": late / total,
        "manual_and_late": manual_and_late / total,
    }


# --- NEW (1) complement_and_union() -----------------------------------------
def complement_and_union(probabilities: dict[str, float]) -> dict[str, float]:
    """Calculate complement, naive sum, and overlap-corrected union.

    Parameters
    ----------
    probabilities:
        The Step 1 dict with keys manual, late, and manual_and_late.

    Returns
    -------
    dict[str, float]
        not_manual = 1 - P(M),
        naive_sum = P(M)+P(L) (too large whenever the events overlap),
        overlap = P(M and L),
        corrected_union = P(M)+P(L)-P(M and L).

    Notes
    -----
    Adding P(M) and P(L) counts the 48 Manual-and-Late orders twice.
    Subtracting the intersection once restores a valid probability.
    """
    manual = probabilities["manual"]
    late = probabilities["late"]
    overlap = probabilities["manual_and_late"]
    return {
        "not_manual": 1 - manual,
        "naive_sum": manual + late,
        "overlap": overlap,
        "corrected_union": manual + late - overlap,
    }


# -----------------------------------------------------------------------------


# --- NEW (2) save_addition_figure() -----------------------------------------
def save_addition_figure(results: dict[str, float]) -> Path:
    """Export naive, corrected, and direct union probabilities.

    The second and third bars are the same number: the addition rule and
    a direct count of the union must agree. The first bar is the naive
    sum. Side effect: writes the PNG.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probability_02_addition.png"

    labels = ["Naive sum\n$P(M)+P(L)$", "Addition rule\nsubtract overlap", "Direct table\ncount"]
    values = [
        results["naive_sum"],
        results["corrected_union"],
        results["corrected_union"],
    ]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.58)
    ax.set_ylabel("Probability")
    ax.set_title(
        "The Addition Rule Removes the Double-Counted Overlap",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.015,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    # annotate draws an arrow from xytext down to the corrected-union height.
    ax.annotate(
        f"Subtract overlap = {results['overlap']:.2f}",
        xy=(0.5, results["corrected_union"]),
        xytext=(0.5, 0.53),
        ha="center",
        arrowprops={"arrowstyle": "->", "color": TEC_NAVY},
        color=TEC_NAVY,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 2 evidence."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    results = complement_and_union(probabilities)
    # Elementwise | on two boolean Series is logical OR. The mean of the
    # resulting 0/1 Series is the proportion of rows in the union, a
    # direct count that must match the addition rule.
    direct_union = float(
        ((data["routing"] == "Manual review") | (data["delivery"] == "Late")).mean()
    )
    output_path = save_addition_figure(results)

    print("LESSON 08 - STEP 2: COMPLEMENT AND ADDITION RULES")
    print(f"P(Manual review)                    : {probabilities['manual']:.4f}")
    print(f"P(NOT Manual review)                : {results['not_manual']:.4f}")
    print(f"P(Late)                             : {probabilities['late']:.4f}")
    print(f"P(Manual review AND Late)           : {results['overlap']:.4f}")
    print(f"Naive P(Manual review) + P(Late)    : {results['naive_sum']:.4f}")
    print(f"Addition-rule union                 : {results['corrected_union']:.4f}")
    print(f"Direct table union                  : {direct_union:.4f}")
    print(f"Figure saved to                     : {output_path}")


if __name__ == "__main__":
    main()

