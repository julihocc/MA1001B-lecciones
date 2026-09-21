"""
Lesson 29 - Step 2: Wald Confidence Interval for a Proportion
=============================================================
THE RECIPE
Start from prop_ci_01_sample_proportion.py, then introduce:
    1. success_failure_check()   n phat and n(1-phat) versus the cutoff 5
    2. wald_interval()           phat +/- 1.96 * sqrt(phat(1-phat)/n)
    3. save_figure()             draw the 95% Wald interval for p

The same x = 27, n = 150 snapshot is rebuilt from constants. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 calculated phat = 0.18.
This step checks the normal approximation conditions and computes the
standard Wald confidence interval for the population proportion p.

    n phat >= 5              check for enough successes
    n(1-phat) >= 5           check for enough failures
    Wald interval            the traditional formula for a CI for p
    z_star                   1.96 for a 95% confidence level

main() prints the standard error, margin of error, and the bounds
[0.1185, 0.2415].

Run it:
    uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_02_wald_interval.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 150
X_SUCCESS = 27
# For 95% confidence, z* is approx 1.96 from the standard normal.
Z_STAR = 1.96
# The traditional textbook cutoff for the success-failure condition is 5
# (or sometimes 10, depending on the text). We use 5.
CUTOFF = 5.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) success_failure_check() -----------------------------------------
def success_failure_check(n: int, x: int) -> dict[str, float]:
    """Check the np and n(1-p) conditions using phat in place of p.

    Parameters
    ----------
    n:
        Total sample size.
    x:
        Number of observed successes.

    Returns
    -------
    dict[str, float]
        phat: the sample proportion.
        n_phat: expected successes (equals x).
        n_qhat: expected failures (equals n - x).
        cutoff: the threshold used for the check (5.0).
        conditions_ok: 1.0 if both counts are >= cutoff, else 0.0.

    Notes
    -----
    Because the population p is unknown, the success-failure condition
    must be checked using the sample proportion phat. This is equivalent
    to checking if the observed counts of successes and failures are
    both at least 5.
    """
    phat = x / n
    n_phat = n * phat
    n_qhat = n * (1.0 - phat)
    return {
        "phat": phat,
        "n_phat": n_phat,
        "n_qhat": n_qhat,
        "cutoff": CUTOFF,
        "conditions_ok": float(n_phat >= CUTOFF and n_qhat >= CUTOFF),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) wald_interval() -------------------------------------------------
def wald_interval(n: int, x: int, z_star: float = Z_STAR) -> dict[str, float]:
    """Build the textbook Wald interval phat +/- z* SE_hat.

    Parameters
    ----------
    n:
        Total sample size.
    x:
        Number of observed successes.
    z_star:
        The critical value from the standard normal distribution.

    Returns
    -------
    dict[str, float]
        se: standard error estimated from phat.
        margin: the margin of error (z_star * se).
        lower: lower bound of the confidence interval.
        upper: upper bound of the confidence interval.
        width: total width of the interval (2 * margin).

    Notes
    -----
    The Wald interval is the standard interval taught in introductory
    statistics. It uses phat to estimate the standard error since p is
    unknown. It performs poorly when p is near 0 or 1, or when n is small.
    """
    phat = x / n
    se = np.sqrt(phat * (1.0 - phat) / n)
    margin = z_star * se
    lower = phat - margin
    upper = phat + margin
    return {
        "se": float(se),
        "margin": float(margin),
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(phat: float, interval: dict[str, float]) -> Path:
    """Save the Wald interval around the sample proportion.

    Parameters
    ----------
    phat:
        The sample proportion (point estimate).
    interval:
        Dictionary containing the 'lower' and 'upper' bounds.

    Returns
    -------
    Path
        Absolute path to the saved PNG file.
    """
    output_path = DIR_FIGURES / "prop_ci_02_wald_interval.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # errorbar visually represents the point estimate and its uncertainty
    ax.errorbar(
        [phat],
        [1],
        xerr=[[phat - interval["lower"]], [interval["upper"] - phat]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.set_yticks([1])
    ax.set_yticklabels(["95% Wald interval"])
    ax.set_xlabel("Population proportion p")
    ax.set_title("Wald Interval: phat +/- 1.96 * sqrt(phat(1-phat)/n)")
    ax.set_xlim(0.0, 0.40)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        phat,
        1.18,
        f"[{interval['lower']:.4f}, {interval['upper']:.4f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Wald interval calculation and generate the plot.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    check = success_failure_check(N, X_SUCCESS)
    interval = wald_interval(N, X_SUCCESS)
    figure_path = save_figure(check["phat"], interval)

    print("================================================================")
    print("LESSON 29 - STEP 2: WALD CONFIDENCE INTERVAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Successes x                     : {X_SUCCESS}")
    print(f"Sample proportion phat          : {check['phat']:.6f}")
    print(f"n * phat                        : {check['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {check['n_qhat']:.6f}")
    print(f"Cutoff for the check            : {check['cutoff']:.1f}")
    print(f"Conditions satisfied            : {bool(check['conditions_ok'])}")
    print(f"Textbook z-star                 : {Z_STAR:.6f}")
    print(f"Standard error                  : {interval['se']:.6f}")
    print(f"Margin of error                 : {interval['margin']:.6f}")
    print(f"Lower bound                     : {interval['lower']:.6f}")
    print(f"Upper bound                     : {interval['upper']:.6f}")
    print(f"Interval width                  : {interval['width']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

