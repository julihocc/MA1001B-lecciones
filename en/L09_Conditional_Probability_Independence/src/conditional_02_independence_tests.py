"""
Lesson 09 - Step 2: Independence tests
======================================
NEW IN THIS STEP: independence_tests() and save_evidence().

THE RECIPE
Start from conditional_01_reduced_sample_space.py, then introduce:
    1. independence_tests()     compare two equivalent independence criteria
    2. save_evidence()          show both failures against their benchmarks

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib and
unattended savefig. Step 1 reduced the 400-order table to a condition and
read P(Late | Manual). This step asks whether Late is independent of Manual
review, using two equalities that should agree.

New in this step:
    boolean Series as events   True where the named event occurs
    Series.mean() of 0/1       P(A) from the indicator of A
    elementwise &              intersection indicator; its mean is P(A and B)
    conditional test           independent iff P(A|B) = P(A)
    product test               independent iff P(A and B) = P(A)P(B)
    np.isclose                 numerical equality of two probabilities

main() prints P(Late), P(Late | Manual), the joint, the product of
marginals, and the False independence flag, then saves the paired bars.

Run it:
    uv run en/L09_Conditional_Probability_Independence/src/conditional_02_independence_tests.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 42
# Lesson 01 pathlib: figures/ next to this package, not the shell's cwd.
FIGURE_PATH = Path(__file__).resolve().parents[1] / "figures" / "conditional_02_independence.png"


def synthetic_orders() -> pd.DataFrame:
    """Return the same shuffled synthetic 400-order dataset as Step 1.

    Copied, not imported: each lesson script is self-contained. Same seed
    and cell counts as Step 1, so the joint distribution is unchanged.
    See Step 1 for the list-repetition and permutation comments.
    """
    records = (
        [("Manual review", "Late")] * 48
        + [("Manual review", "On time")] * 72
        + [("Automated", "Late")] * 32
        + [("Automated", "On time")] * 248
    )
    frame = pd.DataFrame(records, columns=["routing", "delivery"])
    rng = np.random.default_rng(SEED)
    return frame.iloc[rng.permutation(len(frame))].reset_index(drop=True)


# --- NEW (1) independence_tests() --------------------------------------------
def independence_tests(orders: pd.DataFrame) -> dict[str, float | bool]:
    """Evaluate conditional and product definitions of independence.

    Parameters
    ----------
    orders:
        The 400-row table from synthetic_orders().

    Returns
    -------
    dict[str, float | bool]
        p_manual, p_late, p_joint, p_late_given_manual, p_product, and
        independent (True only if both equalities hold).

    Notes
    -----
    Events A = Late and B = Manual review are independent when
    P(A|B) = P(A) and, equivalently when P(B) > 0, when
    P(A and B) = P(A)P(B). On this table 0.40 != 0.20 and 0.12 != 0.06,
    so both tests fail. That is association, not a causal claim.
    """
    # Boolean Series: True on rows in the event, False elsewhere.
    # Their means are P(Manual) and P(Late) because True counts as 1.
    manual = orders["routing"] == "Manual review"
    late = orders["delivery"] == "Late"
    p_manual = manual.mean()
    p_late = late.mean()
    # Elementwise AND is the intersection. Its mean is P(Manual and Late).
    p_joint = (manual & late).mean()
    # P(Late | Manual) = count(intersection) / count(Manual), the reduced
    # sample space from Step 1 written as a ratio of indicator sums.
    p_late_given_manual = (manual & late).sum() / manual.sum()
    return {
        "p_manual": p_manual,
        "p_late": p_late,
        "p_joint": p_joint,
        "p_late_given_manual": p_late_given_manual,
        "p_product": p_manual * p_late,
        "independent": bool(
            # Conditional test: P(Late | Manual) =? P(Late).
            np.isclose(p_late_given_manual, p_late)
            # Product test: P(Manual and Late) =? P(Manual) P(Late).
            and np.isclose(p_joint, p_manual * p_late)
        ),
    }
# -----------------------------------------------------------------------------


# --- NEW (2) save_evidence() -------------------------------------------------
def save_evidence(results: dict[str, float | bool]) -> None:
    """Save two paired comparisons used to assess independence.

    Parameters
    ----------
    results:
        Output of independence_tests().

    Returns
    -------
    None
        Side effect: writes the PNG. Unattended savefig/close as in Lesson 01.

    Notes
    -----
    Each pair is (observed, independence benchmark). The conditional pair
    is P(Late | Manual) versus P(Late). The product pair is P(joint)
    versus P(Manual)P(Late). Independence would make the bars equal.
    """
    pairs = [
        ("Conditional test", results["p_late_given_manual"], results["p_late"]),
        ("Product test", results["p_joint"], results["p_product"]),
    ]
    actual = [float(pair[1]) for pair in pairs]
    benchmark = [float(pair[2]) for pair in pairs]
    x = np.arange(len(pairs))
    width = 0.34

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    # Grouped bars: observed on the left of each tick, benchmark on the right.
    bars_a = ax.bar(x - width / 2, actual, width, label="Observed", color="#D81B60")
    bars_b = ax.bar(x + width / 2, benchmark, width, label="Independence benchmark", color="#1E88E5")
    ax.set_xticks(x, [pair[0] for pair in pairs])
    ax.set_ylabel("Probability")
    ax.set_ylim(0, 0.48)
    ax.set_title("Both independence equalities fail")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    for bars in (bars_a, bars_b):
        for bar in bars:
            value = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.015, f"{value:.2f}", ha="center")
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    """Print both independence tests and export the paired-bar figure."""
    orders = synthetic_orders()
    results = independence_tests(orders)
    print(f"P(Late): {results['p_late']:.6f}")
    print(f"P(Late | Manual review): {results['p_late_given_manual']:.6f}")
    print(f"P(Manual review AND Late): {results['p_joint']:.6f}")
    print(f"P(Manual review) x P(Late): {results['p_product']:.6f}")
    print("Independent events:", results["independent"])
    save_evidence(results)
    print("Figure saved:", FIGURE_PATH)


if __name__ == "__main__":
    main()

