"""
Lesson 29 - Step 3: Rare Events Make the Wald Interval Misleading
=================================================================
THE RECIPE
Start from prop_ci_02_wald_interval.py, then introduce:
    1. rare_event_snapshot()     x = 3 of n = 150 first-contact resolutions
    2. compare_wald_and_wilson() Wald can go negative; Wilson stays in (0, 1)
    3. save_figure()             contrast the two intervals on the same axis

Limit: a rare event with small x fails the success-failure check. The Wald
interval can then report a negative lower bound, which is not a valid
proportion. The Wilson interval is shown only as a diagnostic contrast.

How to read this file:
You already know Python through OOP. Steps 1-2 introduced the Wald interval
and the success-failure check (n*phat >= 5). This step shows what happens
when that condition is violated because of a rare event.

    x = 3                    a small number of successes
    n phat = 3 < 5           the success condition fails
    Wald lower < 0           a negative confidence bound for a proportion
    Wilson interval          a more robust alternative formula

main() prints the failed check, the negative Wald lower bound, and the
Wilson interval for comparison.

Run it:
    uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_03_rare_event_wald.py
"""

from pathlib import Path

import matplotlib
import numpy as np
# We use statsmodels to compute the Wilson score interval, an advanced
# method that performs better than Wald for rare events.
from statsmodels.stats.proportion import proportion_confint

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 150
# x = 3 makes phat = 0.02, so n*phat = 3, which is less than 5.
X_RARE = 3
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) rare_event_snapshot() -------------------------------------------
def rare_event_snapshot(n: int = N, x: int = X_RARE) -> dict[str, float]:
    """Build the rare-event counts that break the Wald conditions.

    Parameters
    ----------
    n:
        Total sample size.
    x:
        Observed rare successes.

    Returns
    -------
    dict[str, float]
        n, x, phat: sample sizes and proportion.
        n_phat: expected successes (equals x), here 3.0.
        n_qhat: expected failures, here 147.0.
        conditions_ok: 1.0 if both >= 5, here 0.0 because 3 < 5.

    Notes
    -----
    When an event is rare (x is small) or extremely common (n-x is small),
    the sampling distribution of phat is heavily skewed. The normal approximation
    fails, and the success-failure condition is designed to catch this.
    """
    phat = x / n
    return {
        "n": float(n),
        "x": float(x),
        "phat": phat,
        "n_phat": n * phat,
        "n_qhat": n * (1.0 - phat),
        "conditions_ok": float(n * phat >= 5 and n * (1.0 - phat) >= 5),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) compare_wald_and_wilson() ---------------------------------------
def compare_wald_and_wilson(n: int, x: int) -> dict[str, float]:
    """Compute Wald and Wilson 95% intervals for the same rare snapshot.

    Parameters
    ----------
    n:
        Total sample size.
    x:
        Observed rare successes.

    Returns
    -------
    dict[str, float]
        se: standard error for Wald.
        wald_lower, wald_upper: bounds using the Wald formula.
        wald_negative_lower: 1.0 if the lower bound is below 0.
        wilson_lower, wilson_upper: bounds using the Wilson score method.

    Notes
    -----
    The Wald lower bound here is 0.02 - 1.96 * SE = -0.0024. A negative
    proportion is impossible. The Wilson interval incorporates the critical
    value into its center and spread, ensuring bounds remain in [0, 1].
    """
    phat = x / n
    se = np.sqrt(phat * (1.0 - phat) / n)
    wald_lower = phat - Z_STAR * se
    wald_upper = phat + Z_STAR * se
    # proportion_confint returns (lower, upper). method="wilson" uses the
    # Wilson score interval which is robust for small x.
    wilson_lower, wilson_upper = proportion_confint(
        x, n, alpha=0.05, method="wilson"
    )
    return {
        "se": float(se),
        "wald_lower": float(wald_lower),
        "wald_upper": float(wald_upper),
        "wald_negative_lower": float(wald_lower < 0.0),
        "wilson_lower": float(wilson_lower),
        "wilson_upper": float(wilson_upper),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    phat: float,
    comparison: dict[str, float],
) -> Path:
    """Contrast the invalid Wald interval with the Wilson diagnostic.

    Parameters
    ----------
    phat:
        The sample proportion (point estimate).
    comparison:
        Dictionary with Wald and Wilson interval bounds.

    Returns
    -------
    Path
        Absolute path to the saved PNG file.
    """
    output_path = DIR_FIGURES / "prop_ci_03_rare_event_wald.png"
    labels = ["Wald (rare x=3)", "Wilson (diagnostic)"]
    lowers = [comparison["wald_lower"], comparison["wilson_lower"]]
    uppers = [comparison["wald_upper"], comparison["wilson_upper"]]
    centers = [phat, phat]

    # xerr is a 2xN array: [lower_errors, upper_errors]
    xerr = np.array(
        [
            [phat - lowers[0], phat - lowers[1]],
            [uppers[0] - phat, uppers[1] - phat],
        ]
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        centers,
        [1.0, 0.0],
        xerr=xerr,
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=2.8,
        capsize=8,
        markersize=8,
    )
    # Highlight the impossibility of a negative proportion
    ax.axvline(0.0, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label="Boundary p = 0")
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(labels)
    ax.set_xlabel("Population proportion p")
    ax.set_title("Rare Events: Wald Can Cross Below Zero")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_ylim(-0.7, 1.7)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the rare event analysis and write the plot.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    rare = rare_event_snapshot()
    comparison = compare_wald_and_wilson(N, X_RARE)
    figure_path = save_figure(rare["phat"], comparison)

    print("================================================================")
    print("LESSON 29 - STEP 3: RARE-EVENT WALD LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Rare successes x                : {X_RARE}")
    print(f"Sample proportion phat          : {rare['phat']:.6f}")
    print(f"n * phat                        : {rare['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {rare['n_qhat']:.6f}")
    print(f"Conditions satisfied            : {bool(rare['conditions_ok'])}")
    print(f"Wald standard error             : {comparison['se']:.6f}")
    print(f"Wald lower bound                : {comparison['wald_lower']:.6f}")
    print(f"Wald upper bound                : {comparison['wald_upper']:.6f}")
    print(
        "Wald lower is negative          : "
        f"{bool(comparison['wald_negative_lower'])}"
    )
    print(f"Wilson lower bound              : {comparison['wilson_lower']:.6f}")
    print(f"Wilson upper bound              : {comparison['wilson_upper']:.6f}")
    print("Limit                          : small x makes Wald misleading")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

