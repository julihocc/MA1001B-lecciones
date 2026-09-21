"""
Lesson 15 - Step 1: Two Inspection Policies
===========================================
NEW IN THIS STEP: policy_a(), policy_b(), and save_figure().

Context:
A fully synthetic quality desk compares two binomial policies that share the
same mean number of defectives: Policy A inspects n = 50 units at p = 0.04,
and Policy B inspects n = 20 units at p = 0.10. Both have np = 2.

The Recipe
----------
Build the first complete program in this order:
    1. policy_a()     n = 50, p = 0.04: larger sample, smaller defect chance
    2. policy_b()     n = 20, p = 0.10: smaller sample, larger defect chance
    3. save_figure()  grouped bars for n, 10p, and the shared mean np

How to read this file:
You already know Python through OOP. Lesson 01 introduced pathlib, NumPy,
the Agg backend, unattended savefig/close, and if __name__. Those idioms
return here with a short pointer, not a second treatise. Lesson 14 introduced
the binomial model X ~ Binomial(n, p); this lesson applies it to risk.

New in this step:
    binomial mean np          E[X] = n p
    binomial variance         Var(X) = n p (1-p)
    equal means, different p  matching np does not match variance
    10 x p on the figure      scales p so it is visible next to n and np
    np.isclose                float comparison of the two means

main() builds both policies, reports matching means with different
variances, and writes the evidence figure.

Run it:
    python binomial_risk_01_two_policies.py
"""

from pathlib import Path

import matplotlib
import numpy as np

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Course-wide default. Reserved here: this script has no random draws, but
# later steps keep the same constant so the package stays uniform.
SEED = 42
# Two binomial inspection plans. Same mean np = 50*0.04 = 20*0.10 = 2.
# Different n and p will produce different variances np(1-p).
POLICY_A = {"name": "A", "n": 50, "p": 0.04}
POLICY_B = {"name": "B", "n": 20, "p": 0.10}
# figures/ next to this package. See Lesson 01 for the pathlib construction.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) policy_a() ------------------------------------------------------
def policy_a() -> dict[str, float | int | str]:
    """Return Policy A: larger sample, smaller defect chance.

    Returns
    -------
    dict[str, float | int | str]
        name, n, p, mean = n*p, and variance = n*p*(1-p). Policy A
        inspects 50 independent units, each defective with probability
        0.04. The type hint lists the value types; Python does not
        enforce it at run time.

    Notes
    -----
    For X ~ Binomial(n, p) the mean is np and the variance is np(1-p).
    Matching np across policies does not match variance unless p is
    also the same. Policy A has the larger variance of the pair.
    """
    n = POLICY_A["n"]
    p = POLICY_A["p"]
    # mean np = 2; variance 50*0.04*0.96 = 1.92, larger than Policy B.
    return {"name": "A", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}
# ------------------------------------------------------------------------------


# --- NEW (2) policy_b() ------------------------------------------------------
def policy_b() -> dict[str, float | int | str]:
    """Return Policy B: smaller sample, larger defect chance.

    Returns
    -------
    dict[str, float | int | str]
        Same keys as policy_a(). Policy B inspects 20 independent units,
        each defective with probability 0.10. Mean np is again 2.

    Notes
    -----
    Variance is 20*0.10*0.90 = 1.80. Equal means with different n and p
    are not interchangeable as risk models; Steps 2-3 show the tails.
    """
    n = POLICY_B["n"]
    p = POLICY_B["p"]
    # mean np = 2, matching Policy A; variance 1.80, smaller than Policy A.
    return {"name": "B", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    a: dict[str, float | int | str],
    b: dict[str, float | int | str],
) -> Path:
    """Save n, p, and mean for the two policies.

    Parameters
    ----------
    a, b:
        Policy dictionaries from policy_a() and policy_b().

    Returns
    -------
    Path
        Absolute path of the PNG. The only side effect is that file;
        the function never opens a window. See Lesson 01 for pathlib
        and savefig.

    Notes
    -----
    The middle bars plot 10*p rather than p so 0.40 and 1.00 share an
    axis with n (50 vs 20) and np (both 2). Without that scale, p would
    be invisible next to n. Grouped bars sit at x - width/2 and
    x + width/2.
    """
    output_path = DIR_FIGURES / "binomial_risk_01_two_policies.png"
    labels = ["n", "10 p", "mean np"]
    # 10.0 * p is a display scale, not a change to the binomial parameter.
    a_vals = [float(a["n"]), 10.0 * float(a["p"]), float(a["mean"])]
    b_vals = [float(b["n"]), 10.0 * float(b["p"]), float(b["mean"])]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - width / 2, a_vals, width, color="#1A2E51", label="Policy A")
    ax.bar(x + width / 2, b_vals, width, color="#EC2661", label="Policy B")
    ax.set_xticks(x)
    ax.set_xticklabels(["n (units)", "10 x p", "mean np"])
    ax.set_ylabel("Value")
    ax.set_title("Same Mean np = 2; Different n and p")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    # savefig/close: same unattended write as Lesson 01. Never plt.show().
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 comparison and print the verified lesson numbers.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    a = policy_a()
    b = policy_b()
    figure_path = save_figure(a, b)

    print("================================================================")
    print("LESSON 15 - STEP 1: TWO POLICIES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Policy A n                      : {a['n']}")
    print(f"Policy A p                      : {a['p']:.6f}")
    print(f"Policy A mean np                : {a['mean']:.6f}")
    print(f"Policy A variance               : {a['variance']:.6f}")
    print(f"Policy B n                      : {b['n']}")
    print(f"Policy B p                      : {b['p']:.6f}")
    print(f"Policy B mean np                : {b['mean']:.6f}")
    print(f"Policy B variance               : {b['variance']:.6f}")
    # isclose, not ==, is the right test for floating-point products.
    print(f"Means equal                     : {np.isclose(a['mean'], b['mean'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# See Lesson 01 for the if __name__ script-entry idiom.
if __name__ == "__main__":
    main()

