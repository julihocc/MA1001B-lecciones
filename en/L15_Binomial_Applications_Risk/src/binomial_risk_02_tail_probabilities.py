"""
Lesson 15 - Step 2: Tail Probabilities P(X >= 3)
================================================
THE RECIPE
Start from binomial_risk_01_two_policies.py, then introduce:
    1. tail_probability()   P(X >= 3) = 1 - F(2) for a binomial policy
    2. compare_tails()      Policy A versus Policy B
    3. save_figure()        bar comparison of the two tails

Same mean np = 2 does not imply the same chance of three or more defectives.

How to read this file:
You already know Python through OOP. Step 1 built two binomial policies
that share np = 2 but not variance. This step copies those helpers so the
script stays self-contained; comments concentrate on the NEW bands.
Lesson 01 still covers pathlib, Agg, savefig/close, and if __name__.

New in this step:
    scipy.stats.binom     binomial PMF, CDF, and survival function
    binom.pmf(k, n, p)    P(X = k) = C(n,k) p^k (1-p)^{n-k}
    binom.sf(k, n, p)     P(X > k), SciPy's survival function
    P(X >= m)             sf(m - 1) because X is integer-valued
    two-panel bars        P(X = 0) versus the far tail P(X >= 8)

main() reprints the shared mean, then P(X = 0), P(X >= 3), P(X >= 8),
and the far-tail ratio A/B. P(X >= 3) can match while a farther tail
does not.

Run it:
    python binomial_risk_02_tail_probabilities.py
"""

from pathlib import Path

import matplotlib
import numpy as np
# stats.binom is SciPy's binomial family: pmf, cdf, and sf live here.
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


def policy_a() -> dict[str, float | int | str]:
    """Return Policy A: n = 50, p = 0.04, mean np, variance np(1-p).

    Copied from Step 1 so this file stays standalone. Equal means with
    different n and p produce different variances; see Step 1.
    """
    n = POLICY_A["n"]
    p = POLICY_A["p"]
    return {"name": "A", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}


def policy_b() -> dict[str, float | int | str]:
    """Return Policy B: n = 20, p = 0.10, mean np, variance np(1-p).

    Copied from Step 1. Mean matches Policy A; variance is smaller.
    """
    n = POLICY_B["n"]
    p = POLICY_B["p"]
    return {"name": "B", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}


# --- NEW (1) tail_probability() ----------------------------------------------
def tail_probability(n: int, p: float, threshold: int = 3) -> float:
    """Return P(X >= threshold) for X ~ Binomial(n, p).

    Parameters
    ----------
    n, p:
        Binomial size and success probability for one policy.
    threshold:
        Left endpoint of the upper tail. Default 3 is the lesson's
        operational "too many defectives" cutoff.

    Returns
    -------
    float
        P(X >= threshold). float() unwraps SciPy's 0-dimensional array
        into a Python float.

    Notes
    -----
    stats.binom.sf(k, n, p) is P(X > k), not P(X >= k). For an
    integer-valued X, P(X >= m) = P(X > m - 1) = sf(m - 1). With
    m = 3 that is 1 - F(2), the chance of three or more defectives.
    Using sf avoids subtracting a CDF from 1 by hand.
    """
    return float(stats.binom.sf(threshold - 1, n=n, p=p))
# ------------------------------------------------------------------------------


# --- NEW (2) compare_tails() -------------------------------------------------
def compare_tails() -> dict[str, float]:
    """Return P(X = 0), P(X >= 3), and the far tail P(X >= 8).

    Returns
    -------
    dict[str, float]
        p0_a, p0_b: clean-sample probabilities P(X = 0),
        tail3_a, tail3_b: P(X >= 3),
        tail8_a, tail8_b: P(X >= 8).

    Notes
    -----
    P(X >= 3) can be almost identical for two policies even when
    P(X = 0) and P(X >= 8) are not. Matching a near-mean tail is not
    matching the whole distribution. Policy A, with larger variance,
    puts more mass on the far tail x >= 8.
    """
    return {
        # pmf(0) is the chance of a clean sample: no defectives.
        "p0_a": float(stats.binom.pmf(0, n=POLICY_A["n"], p=POLICY_A["p"])),
        "p0_b": float(stats.binom.pmf(0, n=POLICY_B["n"], p=POLICY_B["p"])),
        "tail3_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 3),
        "tail3_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 3),
        # Farther cutoff: same helper, different threshold.
        "tail8_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 8),
        "tail8_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 8),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(tails: dict[str, float]) -> Path:
    """Save P(X = 0) and the far tail P(X >= 8) for both policies.

    Parameters
    ----------
    tails:
        Dictionary from compare_tails().

    Returns
    -------
    Path
        Absolute path of the PNG. See Lesson 01 for pathlib and savefig.

    Notes
    -----
    The figure does not plot P(X >= 3): those near-mean tails almost
    match and would hide the lesson. The two panels contrast a clean
    sample with the far tail, where the policies disagree. Bar labels
    use ax.text; the tiny far-tail offset 0.00002 sits just above the
    bars.
    """
    output_path = DIR_FIGURES / "binomial_risk_02_tail_probabilities.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["Policy A", "Policy B"]
    colors = ["#1A2E51", "#EC2661"]

    zeros = [tails["p0_a"], tails["p0_b"]]
    axes[0].bar(labels, zeros, color=colors, width=0.55)
    axes[0].set_ylabel("P(X = 0)")
    axes[0].set_title("Clean-sample probability")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(zeros):
        axes[0].text(idx, value + 0.003, f"{value:.4f}", ha="center", fontsize=8)

    far = [tails["tail8_a"], tails["tail8_b"]]
    axes[1].bar(labels, far, color=colors, width=0.55)
    axes[1].set_ylabel("P(X >= 8)")
    axes[1].set_title("Far-tail risk")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(far):
        axes[1].text(idx, value + 0.00002, f"{value:.6f}", ha="center", fontsize=8)

    fig.suptitle("Same np = 2 Does Not Match P(X = 0) or P(X >= 8)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 tail comparison and print the verified lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    a = policy_a()
    b = policy_b()
    tails = compare_tails()
    figure_path = save_figure(tails)

    print("================================================================")
    print("LESSON 15 - STEP 2: TAIL PROBABILITIES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Policy A mean                   : {a['mean']:.6f}")
    print(f"Policy B mean                   : {b['mean']:.6f}")
    print(f"Policy A P(X = 0)               : {tails['p0_a']:.6f}")
    print(f"Policy B P(X = 0)               : {tails['p0_b']:.6f}")
    print(f"Policy A P(X >= 3)              : {tails['tail3_a']:.6f}")
    print(f"Policy B P(X >= 3)              : {tails['tail3_b']:.6f}")
    print(f"Policy A P(X >= 8)              : {tails['tail8_a']:.6f}")
    print(f"Policy B P(X >= 8)              : {tails['tail8_b']:.6f}")
    print(
        "Far-tail ratio A/B               : "
        f"{tails['tail8_a'] / tails['tail8_b']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# See Lesson 01 for the if __name__ script-entry idiom.
if __name__ == "__main__":
    main()

