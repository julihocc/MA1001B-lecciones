"""
Lesson 15 - Step 3: Same Mean Can Hide Different Tails
======================================================
THE RECIPE
Start from binomial_risk_02_tail_probabilities.py, then introduce:
    1. policy_pmf()         full binomial PMF for a policy
    2. overlay_pmfs()       Policy A versus Policy B on the same axis
    3. save_figure()        both PMFs with the x >= 3 region marked

The limit is that matching np is not matching risk. Policy A puts more mass
on large defect counts even though both means equal 2.

How to read this file:
You already know Python through OOP. Steps 1-2 showed that np = 2 for
both policies, that variances differ, and that P(X >= 3) can match
while P(X >= 8) does not. This step overlays the two PMFs. Lesson 01
still covers pathlib, Agg, savefig/close, and if __name__.

New in this step:
    stats.binom.pmf on an array   one call returns P(X = 0), ..., P(X = 12)
    grouped bars at each x        Policy A left, Policy B right
    ax.axvspan                    shade the far-tail region x >= 8
    the limit                     matching np is not matching tail risk

main() reprints P(X = 0), both tails, and the far-tail ratio A/B.

Run it:
    python binomial_risk_03_same_mean_different_tails.py
"""

from pathlib import Path

import matplotlib
import numpy as np
# stats.binom.pmf accepts a scalar k or an array of k values.
from scipy import stats

# Same unattended-figure setup as Lesson 01: Agg before pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POLICY_A = {"name": "A", "n": 50, "p": 0.04}
POLICY_B = {"name": "B", "n": 20, "p": 0.10}
# figures/ next to this package. See Lesson 01 for pathlib and savefig.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def tail_probability(n: int, p: float, threshold: int = 3) -> float:
    """Return P(X >= threshold) for X ~ Binomial(n, p).

    Copied from Step 2. stats.binom.sf(k, n, p) is P(X > k), so
    sf(threshold - 1) equals P(X >= threshold) for integer X.
    """
    return float(stats.binom.sf(threshold - 1, n=n, p=p))


# --- NEW (1) policy_pmf() ----------------------------------------------------
def policy_pmf(n: int, p: float, max_x: int = 12) -> tuple[np.ndarray, np.ndarray]:
    """Return x values and binomial masses up to max_x.

    Parameters
    ----------
    n, p:
        Binomial size and success probability.
    max_x:
        Last integer plotted. Default 12 covers the far tail x >= 8
        without drawing the whole 0..n support.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        xs = 0, 1, ..., max_x and the matching PMF values P(X = x).
        stats.binom.pmf accepts an array of k values and returns an
        array of the same length.

    Notes
    -----
    Truncating the plot at 12 is a display choice, not a change to the
    distribution. Printed tail probabilities still use the full support.
    """
    xs = np.arange(0, max_x + 1)
    return xs, stats.binom.pmf(xs, n=n, p=p)
# ------------------------------------------------------------------------------


# --- NEW (2) overlay_pmfs() --------------------------------------------------
def overlay_pmfs() -> dict[str, np.ndarray | float]:
    """Return both PMFs and both tail probabilities.

    Returns
    -------
    dict[str, np.ndarray | float]
        xs, pmf_a, pmf_b for the overlay, plus the Step 2 tail numbers
        and P(X = 0) for the console report. The type hint is a union:
        some values are arrays and some are floats.

    Notes
    -----
    Equal means do not make these two PMFs equal. Policy A has larger
    variance np(1-p) and the heavier far tail P(X >= 8).
    """
    xs, pmf_a = policy_pmf(POLICY_A["n"], POLICY_A["p"])
    # _ discards the second xs: both policies share the same 0..12 grid.
    _, pmf_b = policy_pmf(POLICY_B["n"], POLICY_B["p"])
    return {
        "xs": xs,
        "pmf_a": pmf_a,
        "pmf_b": pmf_b,
        "tail3_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 3),
        "tail3_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 3),
        "tail8_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 8),
        "tail8_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 8),
        "p0_a": float(stats.binom.pmf(0, n=POLICY_A["n"], p=POLICY_A["p"])),
        "p0_b": float(stats.binom.pmf(0, n=POLICY_B["n"], p=POLICY_B["p"])),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(overlay: dict[str, np.ndarray | float]) -> Path:
    """Overlay the two PMFs and shade the x >= 3 tail.

    Parameters
    ----------
    overlay:
        Dictionary from overlay_pmfs(), including xs, pmf_a, and pmf_b.

    Returns
    -------
    Path
        Absolute path of the PNG. See Lesson 01 for pathlib and savefig.

    Notes
    -----
    ax.axvspan(7.5, 12.5) paints a vertical band from just left of 8 to
    just right of 12, so the far-tail region x >= 8 is visible behind
    the bars. Grouped bars at xs +/- width/2 keep integer ticks aligned
    with both policies. Matching np hides a heavier far tail for
    Policy A, the policy with larger n and smaller p.
    """
    output_path = DIR_FIGURES / "binomial_risk_03_same_mean_different_tails.png"
    xs = overlay["xs"]
    width = 0.38

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Shade x >= 8 (the far tail), not the near-mean cutoff x >= 3.
    ax.axvspan(7.5, 12.5, color="#F8D5DE", alpha=0.55, label="x >= 8")
    ax.bar(
        xs - width / 2,
        overlay["pmf_a"],
        width=width,
        color="#1A2E51",
        label="Policy A",
    )
    ax.bar(
        xs + width / 2,
        overlay["pmf_b"],
        width=width,
        color="#EC2661",
        label="Policy B",
    )
    ax.set_xlabel("Defect count x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Matching np Hides a Heavier Far Tail for Policy A")
    ax.set_xticks(xs)
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 overlay and print the verified lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    overlay = overlay_pmfs()
    figure_path = save_figure(overlay)

    print("================================================================")
    print("LESSON 15 - STEP 3: SAME MEAN, DIFFERENT TAILS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Shared mean np                  : {POLICY_A['n'] * POLICY_A['p']:.6f}")
    print(f"Policy A P(X = 0)               : {overlay['p0_a']:.6f}")
    print(f"Policy B P(X = 0)               : {overlay['p0_b']:.6f}")
    print(f"Policy A P(X >= 3)              : {overlay['tail3_a']:.6f}")
    print(f"Policy B P(X >= 3)              : {overlay['tail3_b']:.6f}")
    print(f"Policy A P(X >= 8)              : {overlay['tail8_a']:.6f}")
    print(f"Policy B P(X >= 8)              : {overlay['tail8_b']:.6f}")
    print(
        "Far-tail ratio A/B               : "
        f"{overlay['tail8_a'] / overlay['tail8_b']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# See Lesson 01 for the if __name__ script-entry idiom.
if __name__ == "__main__":
    main()

