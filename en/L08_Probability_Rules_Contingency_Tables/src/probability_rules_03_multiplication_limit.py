"""
Lesson 08 - Step 3: The Multiplication-Rule Limit
=================================================
NEW IN THIS STEP: multiplication_diagnostics() and
save_multiplication_limit_figure().

Changes from probability_rules_02_complement_addition.py
The Recipe
----------
Introduce these changes in order:
    1. multiplication_diagnostics() compares marginal and conditional products
    2. save_multiplication_limit_figure() exposes the independence assumption

How to read this file:
You already know Python through OOP. Steps 1-2 produced P(M), P(L), and
P(M and L) from the same 400-order table. This step asks whether
P(M and L) equals P(M)P(L). It does not, so the independence shortcut fails.

New in this step:
    independence shortcut   P(M and L) =? P(M)P(L)
    conditional probability P(L|M) = P(M and L) / P(M)
    general product rule    P(M and L) = P(M) P(L|M)  (always)
    the limit               0.06 vs 0.12 on this table

main() prints the observed intersection 0.12, the naive product 0.06, the
conditional 0.40, and the general product 0.12 that recovers the table.

Run from the repository root:
    uv run en/L08_Probability_Rules_Contingency_Tables/src/
    probability_rules_03_multiplication_limit.py
"""

from pathlib import Path

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


def complement_and_union(probabilities: dict[str, float]) -> dict[str, float]:
    """Calculate complement, naive sum, and overlap-corrected union."""
    manual = probabilities["manual"]
    late = probabilities["late"]
    overlap = probabilities["manual_and_late"]
    return {
        "not_manual": 1 - manual,
        "naive_sum": manual + late,
        "overlap": overlap,
        "corrected_union": manual + late - overlap,
    }


# --- NEW (1) multiplication_diagnostics() ----------------------------------
def multiplication_diagnostics(
    probabilities: dict[str, float],
) -> dict[str, float]:
    """Compare observed intersection with two probability products.

    Parameters
    ----------
    probabilities:
        Step 1 dict with manual, late, and manual_and_late.

    Returns
    -------
    dict[str, float]
        intersection: P(M and L) from the table,
        marginal_product: P(M)P(L), valid only under independence,
        late_given_manual: P(L|M) = P(M and L)/P(M),
        general_product: P(M)P(L|M), which equals the intersection
        whether or not the events are independent.

    Notes
    -----
    On this table P(L|M)=0.40 while P(L)=0.20, so Late is more common
    among Manual-review orders. Independence would require those two
    numbers to match, and would require P(M)P(L)=0.06 to equal 0.12.
    """
    manual = probabilities["manual"]
    late = probabilities["late"]
    intersection = probabilities["manual_and_late"]
    late_given_manual = intersection / manual
    return {
        "intersection": intersection,
        "marginal_product": manual * late,
        "late_given_manual": late_given_manual,
        "general_product": manual * late_given_manual,
    }


# -----------------------------------------------------------------------------


# --- NEW (2) save_multiplication_limit_figure() -----------------------------
def save_multiplication_limit_figure(results: dict[str, float]) -> Path:
    """Export marginal-product, general-rule, and table intersections.

    Pink bar: independence shortcut (too small). Blue and navy bars:
    general product and direct cell, which agree. Side effect: writes PNG.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probability_03_limit.png"

    labels = [
        "Assume independence\n$P(M)P(L)$",
        "General rule\n$P(M)P(L|M)$",
        "Direct table\n$P(M\\cap L)$",
    ]
    values = [
        results["marginal_product"],
        results["general_product"],
        results["intersection"],
    ]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.145)
    ax.set_ylabel("Probability")
    ax.set_title(
        "Multiplying Marginals Can Hide Dependence",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.004,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    ax.text(
        0.98,
        0.95,
        f"$P(L|M)={results['late_given_manual']:.2f}$ while $P(L)=0.20$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=TEC_NAVY,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# -----------------------------------------------------------------------------


def main() -> None:
    """Calculate, verify, display, and export Step 3 evidence."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    results = multiplication_diagnostics(probabilities)
    output_path = save_multiplication_limit_figure(results)

    print("LESSON 08 - STEP 3: THE MULTIPLICATION-RULE LIMIT")
    print(f"P(Manual review)                    : {probabilities['manual']:.4f}")
    print(f"P(Late)                             : {probabilities['late']:.4f}")
    print(f"Observed P(Manual review AND Late)  : {results['intersection']:.4f}")
    print(f"Naive marginal product              : {results['marginal_product']:.4f}")
    print(f"P(Late GIVEN Manual review)         : {results['late_given_manual']:.4f}")
    print(f"General multiplication rule         : {results['general_product']:.4f}")
    print(f"Figure saved to                     : {output_path}")


if __name__ == "__main__":
    main()

