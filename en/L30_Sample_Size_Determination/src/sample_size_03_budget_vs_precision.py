"""
Lesson 30 - Step 3: Desired E = 0.01 Can Exceed the Budget
==========================================================
THE RECIPE
Start from sample_size_02_proportion_conservative.py, then introduce:
    1. tight_margin_n()        conservative n for E = 0.01
    2. budget_capacity()       observations the budget can actually fund
    3. save_figure()           required n versus affordable n

Limit: shrinking the margin of error to 0.01 inflates n with the square of
1/E. A $20,000 study at $12 per observation cannot fund that sample.

How to read this file:
You already know Python through OOP. Steps 1-2 planned n for a mean and
for a proportion, with p = 0.5 as the conservative choice. Lesson 01
covers pathlib and unattended savefig. This step keeps the proportion
formula and shrinks E from 0.03 to 0.01, then asks whether the budget
can buy that n.

    n = z*^2 * 0.5 * 0.5 / E^2   same conservative formula, smaller E
    n grows with 1/E^2           E / 3 multiplies n by 9
    floor(budget / cost)         whole observations the budget can buy
    required n vs affordable n   a statistically nice E can be unfundable

main() prints required n = 9604, affordable n = 1666, and the cost of
the required sample. Matching E = 0.01 on paper does not fund it.

Run it:
    python sample_size_03_budget_vs_precision.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed. Planning arithmetic still uses no random draws.
SEED = 42
# Same 95% z* and conservative p as Step 2. Only E and the money
# constants are new.
Z_STAR = 1.96
P_CONSERVATIVE = 0.5
# Tighter margin: 1 percentage point instead of Step 2's 0.03.
# Because n scales with 1/E^2, (0.03/0.01)^2 = 9 times as many rows.
E_TIGHT = 0.01
# Synthetic cost of one observation, in dollars. Not a real vendor rate.
COST_PER_OBS = 12.0
# Synthetic study budget. Underscore in 20_000 is a readability separator.
BUDGET = 20_000.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) tight_margin_n() ------------------------------------------------
def tight_margin_n(margin: float = E_TIGHT) -> dict[str, float]:
    """Compute conservative n for a very small margin of error.

    Parameters
    ----------
    margin:
        Target E on the proportion scale. Default E_TIGHT = 0.01.

    Returns
    -------
    dict[str, float]
        margin echoes the input. raw_n is z*^2 p(1-p) / E^2 at p = 0.5.
        n_required is that value rounded up.

    Notes
    -----
    Same proportion formula as Step 2: n = z*^2 p(1-p) / E^2, with
    p = 0.5 so p(1-p) = 0.25. Only the margin changed. For z*=1.96
    and E=0.01: 3.8416 * 0.25 / 0.0001 = 9604 exactly after ceil.
    Rebuilt here so this file does not import Step 2.
    """
    # n = z*^2 * p * (1-p) / E^2 with p fixed at the conservative 0.5.
    # Shrinking E from 0.03 to 0.01 multiplies the denominator's E^2 by
    # 1/9, so n grows about ninefold relative to Step 2.
    raw = (Z_STAR ** 2) * P_CONSERVATIVE * (1.0 - P_CONSERVATIVE) / (margin ** 2)
    return {
        "margin": margin,
        "raw_n": float(raw),
        "n_required": int(np.ceil(raw)),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) budget_capacity() -----------------------------------------------
def budget_capacity(
    n_required: int,
    cost: float = COST_PER_OBS,
    budget: float = BUDGET,
) -> dict[str, float]:
    """Compare required n with the number of observations the budget can buy.

    Parameters
    ----------
    n_required:
        Rounded-up statistical n from tight_margin_n().
    cost:
        Dollars per observation. Default COST_PER_OBS = 12.
    budget:
        Total dollars available. Default BUDGET = 20,000.

    Returns
    -------
    dict[str, float]
        cost_per_obs and budget echo the money inputs. affordable_n is
        floor(budget / cost). shortfall is required minus affordable.
        cost_required is n_required * cost. can_fund is 1.0 when the
        budget covers n_required and 0.0 otherwise (a boolean stored
        as a float so the dict stays dict[str, float]).

    Notes
    -----
    floor, not ceil: a leftover $8 cannot buy the next $12 observation.
    A positive shortfall means the statistically required n is larger
    than the fundable n. Desired E is then infeasible at this budget.
    """
    # Whole observations the budget can purchase. 20000 / 12 = 1666.66...,
    # so floor yields 1666.
    affordable = int(np.floor(budget / cost))
    shortfall = n_required - affordable
    # Dollars needed to fund the statistical n: 9604 * 12 = 115248.
    cost_required = n_required * cost
    return {
        "cost_per_obs": cost,
        "budget": budget,
        "affordable_n": float(affordable),
        "shortfall": float(shortfall),
        "cost_required": float(cost_required),
        # True -> 1.0, False -> 0.0. main() prints this with bool().
        "can_fund": float(affordable >= n_required),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(n_required: int, affordable_n: int) -> Path:
    """Contrast statistically required n with budget-affordable n.

    Parameters
    ----------
    n_required:
        Conservative rounded-up n at E = 0.01.
    affordable_n:
        floor(budget / cost), the largest whole sample the money buys.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Two bars, not a formula grid. Magenta is the n the margin demands;
    navy is the n the budget can fund. The gap is the lesson limit:
    shrinking E is not free, and a desired precision can be unfundable.
    """
    output_path = DIR_FIGURES / "sample_size_03_budget_vs_precision.png"
    # \n splits each tick label onto two lines so the category names fit.
    labels = ["Required n\nfor E = 0.01", "Affordable n\nat $12 / obs"]
    values = [n_required, affordable_n]
    colors = ["#EC2661", "#1A2E51"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Number of observations")
    ax.set_title("Desired E = 0.01 Exceeds the Study Budget")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 120,
            f"{value:,}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 budget-versus-precision report and write the figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    plan = tight_margin_n()
    money = budget_capacity(plan["n_required"])
    figure_path = save_figure(plan["n_required"], int(money["affordable_n"]))

    print("================================================================")
    print("LESSON 30 - STEP 3: BUDGET VERSUS PRECISION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Textbook z-star                 : {Z_STAR:.6f}")
    print(f"Conservative p                  : {P_CONSERVATIVE:.6f}")
    print(f"Tight margin E                  : {plan['margin']:.6f}")
    print(f"Raw n for E=0.01                : {plan['raw_n']:.6f}")
    print(f"Rounded-up n                    : {plan['n_required']}")
    print(f"Cost per observation            : {money['cost_per_obs']:.2f}")
    print(f"Study budget                    : {money['budget']:.2f}")
    print(f"Affordable n                    : {int(money['affordable_n'])}")
    print(f"Cost of required n              : {money['cost_required']:.2f}")
    print(f"Shortfall in observations       : {int(money['shortfall'])}")
    # bool(0.0) is False; bool(1.0) is True. Stored as float in the dict.
    print(f"Budget can fund required n      : {bool(money['can_fund'])}")
    print("Limit                          : E=0.01 can exceed the budget")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

