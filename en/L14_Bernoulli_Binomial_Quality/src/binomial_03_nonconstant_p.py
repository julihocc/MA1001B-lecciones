"""
Lesson 14 - Step 3: Nonconstant p Breaks the Binomial
=====================================================
THE RECIPE
Start from binomial_02_pmf_cdf.py, then introduce:
    1. mixed_lot_pmf()      half the lots have p=0.02, half have p=0.14
    2. compare_zero_and_variance()  mixture versus Binomial(20, 0.08)
    3. save_figure()        P(X = 0) and variance under both models

The average defect chance is still 0.08, but p is not constant across lots.
That mixture is the limit of the binomial assumption.

How to read this file:
You already know Python through OOP. Steps 1-2 built X ~ Binomial(20, 0.08)
and evaluated its PMF, CDF, mean, and variance with scipy.stats.binom.
Lesson 01 covers pathlib and unattended savefig. This step keeps the same
average p but drops the constant-p assumption.

    mixture PMF          0.5 * Binom(n, 0.02) + 0.5 * Binom(n, 0.14)
    np.sum(xs * mix)     mean of a discrete distribution given as an array
    E[X^2] - (E[X])^2    computational formula for variance
    plt.subplots(1, 2)   two Axes side by side on one Figure

main() prints P(X = 0) and Var(X) under both models. Matching the average
p does not restore the binomial: the mixture puts more mass at 0 and has
a larger variance.

Run it:
    python binomial_03_nonconstant_p.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.binom is reused from Step 2: PMF of Binomial(n, p) at an array of x.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_TRIALS = 20
# Average defect chance, still 0.08, but no single lot has this p.
P_DEFECT = 0.08
# Two lot types that average to P_DEFECT: 0.5 * 0.02 + 0.5 * 0.14 = 0.08.
# Constant p was binomial assumption 3; these two values break it.
P_LOW = 0.02
P_HIGH = 0.14
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def binomial_pmf_cdf(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Return P(X = 0) and P(X <= 2) for the Step 2 binomial, rebuilt here.

    stats.binom(n, p) is a frozen Binomial(n, p). .pmf(k) is P(X = k);
    .cdf(k) is P(X <= k). This file does not import Step 2.
    """
    model = stats.binom(n=n, p=p)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_most_two": float(model.cdf(2)),
    }


def binomial_moments(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Return the binomial mean np and variance np(1-p) from Step 2.

    These closed forms require constant p. The mixture below cannot use them.
    """
    return {
        "mean": n * p,
        "variance": n * p * (1.0 - p),
    }


# --- NEW (1) mixed_lot_pmf() -------------------------------------------------
def mixed_lot_pmf(n: int = N_TRIALS) -> np.ndarray:
    """Average Binomial(n, 0.02) and Binomial(n, 0.14) with equal weight.

    Parameters
    ----------
    n:
        Inspections per lot. Default N_TRIALS = 20.

    Returns
    -------
    np.ndarray
        Length n + 1. Index x holds
        0.5 * P(Y = x) + 0.5 * P(Z = x)
        where Y ~ Binomial(n, P_LOW) and Z ~ Binomial(n, P_HIGH).

    Notes
    -----
    This is the law of total probability on the lot type. A lot is low-p
    or high-p with chance 1/2 each, and then X is binomial given that p.
    The result is a valid PMF (nonnegative, sums to 1) but it is not a
    binomial PMF: no single p reproduces those masses.
    """
    # Support 0, 1, ..., n, the same integers as a binomial count.
    xs = np.arange(0, n + 1)
    # stats.binom.pmf(xs, n=n, p=...) evaluates the binomial PMF at every
    # x at once. Adding the two arrays with weight 0.5 mixes the lots.
    return 0.5 * stats.binom.pmf(xs, n=n, p=P_LOW) + 0.5 * stats.binom.pmf(
        xs, n=n, p=P_HIGH
    )
# ------------------------------------------------------------------------------


# --- NEW (2) compare_zero_and_variance() -------------------------------------
def compare_zero_and_variance(n: int = N_TRIALS) -> dict[str, float]:
    """Compare P(X = 0) and Var(X) for the binomial and the mixture.

    Parameters
    ----------
    n:
        Inspections per lot. Default N_TRIALS = 20.

    Returns
    -------
    dict[str, float]
        binomial_p_zero and mixture_p_zero are P(X = 0) under each model.
        binomial_variance is n p (1-p) at p = 0.08.
        mixture_mean and mixture_variance come from the mixture PMF.
        average_p is 0.5 * P_LOW + 0.5 * P_HIGH, still 0.08.

    Notes
    -----
    For a discrete PMF stored as an array, the mean is sum x P(X = x) and
    the second moment is sum x^2 P(X = x). Variance is E[X^2] - (E[X])^2.
    The mixture mean matches n * 0.08, but the mixture variance is larger
    (overdispersion) and P(X = 0) is larger because some lots are very
    clean. Matching the average p does not restore Binomial(n, 0.08).
    """
    xs = np.arange(0, n + 1)
    mix = mixed_lot_pmf(n)
    # Elementwise xs * mix is x P(X = x) at each integer; np.sum adds them.
    mix_mean = float(np.sum(xs * mix))
    # xs ** 2 is x-squared. Same weighted sum gives E[X^2].
    mix_second = float(np.sum((xs ** 2) * mix))
    # Computational formula: Var(X) = E[X^2] - (E[X])^2.
    mix_var = mix_second - mix_mean ** 2
    binomial = binomial_moments(n, P_DEFECT)
    return {
        # Unbound PMF at a single k: P(X = 0) under Binomial(n, 0.08).
        "binomial_p_zero": float(stats.binom.pmf(0, n=n, p=P_DEFECT)),
        # mix[0] is the mixture mass at x = 0, already a probability.
        "mixture_p_zero": float(mix[0]),
        "binomial_variance": binomial["variance"],
        "mixture_mean": mix_mean,
        "mixture_variance": mix_var,
        "average_p": 0.5 * P_LOW + 0.5 * P_HIGH,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Contrast P(X = 0) and variance when p is not constant.

    Parameters
    ----------
    comparison:
        Dict from compare_zero_and_variance() with both models' P(X = 0)
        and variances.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Left panel: the mixture puts more mass at a fully clean lot. Right
    panel: the mixture variance exceeds np(1-p). Both gaps are the visual
    of the constant-p limit.
    """
    output_path = DIR_FIGURES / "binomial_03_nonconstant_p.png"
    # 1 row, 2 columns of Axes. axes[0] is P(X = 0); axes[1] is variance.
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["Binomial\np=0.08", "Mixture\n0.02 and 0.14"]
    colors = ["#1A2E51", "#EC2661"]

    zeros = [comparison["binomial_p_zero"], comparison["mixture_p_zero"]]
    axes[0].bar(labels, zeros, color=colors, width=0.55)
    axes[0].set_ylabel("P(X = 0)")
    axes[0].set_title("Chance of a clean lot")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    # enumerate yields (0, first bar value) then (1, second). text at
    # x = idx sits centered on that bar.
    for idx, value in enumerate(zeros):
        axes[0].text(idx, value + 0.01, f"{value:.3f}", ha="center", fontsize=8)

    variances = [comparison["binomial_variance"], comparison["mixture_variance"]]
    axes[1].bar(labels, variances, color=colors, width=0.55)
    axes[1].set_ylabel("Var(X)")
    axes[1].set_title("Variance of the defect count")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(variances):
        axes[1].text(idx, value + 0.05, f"{value:.3f}", ha="center", fontsize=8)

    fig.suptitle("Average p = 0.08 Does Not Restore the Binomial")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 mixture comparison and write the two-panel figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    comparison = compare_zero_and_variance()
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LESSON 14 - STEP 3: NONCONSTANT p")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Low-p lots                      : {P_LOW:.6f}")
    print(f"High-p lots                     : {P_HIGH:.6f}")
    print(f"Average p                       : {comparison['average_p']:.6f}")
    print(f"Binomial P(X = 0)               : {comparison['binomial_p_zero']:.6f}")
    print(f"Mixture P(X = 0)                : {comparison['mixture_p_zero']:.6f}")
    print(f"Binomial variance               : {comparison['binomial_variance']:.6f}")
    print(f"Mixture mean                    : {comparison['mixture_mean']:.6f}")
    print(f"Mixture variance                : {comparison['mixture_variance']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

