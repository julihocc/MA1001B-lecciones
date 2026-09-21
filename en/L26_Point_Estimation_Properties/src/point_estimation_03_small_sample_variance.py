"""
Lesson 26 - Step 3: Unbiasedness Does Not Imply Small Variance
=============================================================
THE RECIPE
Start from point_estimation_02_efficiency_consistency.py, then introduce:
    1. small_sample_xbar()      n = 5, still unbiased
    2. decision_error_rate()    P(|xbar - mu| > 10) at n = 5 versus n = 200
    3. save_figure()            contrast the two sampling spreads

An unbiased estimator can still be too noisy for a decision. At n = 5,
xbar recovers 100 on average but often misses mu by more than 10.

How to read this file:
You already know Python through OOP. Steps 1-2 showed unbiasedness,
efficiency, and consistency of xbar. Lesson 01 covers pathlib and
unattended savefig; they are rebuilt here only so the script stays
self-contained. This step is the limit: unbiasedness does not imply a
small variance in a small sample.

    n = 5 still unbiased         E[xbar] = mu, but SE = 15/sqrt(5) ~ 6.71
    MSE = Var + Bias^2           Bias = 0, so MSE = 225/5 = 45
    P(|xbar - mu| > 10)          a decision error, not a bias
    np.abs(means - MU) > 10      boolean mask; mean is the Monte Carlo rate

main() prints bias, SD, and P(|error| > 10) at n = 5 and n = 200. No
earlier lesson script is imported.

Run it:
    python point_estimation_03_small_sample_variance.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same seed, mu, and sigma as Steps 1-2. This file rebuilds the
# Normal(100, 15) clock; it does not import those scripts.
SEED = 42
MU = 100.0
SIGMA = 15.0
# Tiny sample: xbar is still unbiased, but Var(xbar) = 225/5 = 45.
N_TINY = 5
# Large sample from Step 2, used here as the consistent contrast.
N_LARGE = 200
# Decision threshold: miss mu by more than 10 cost units. This is not
# a confidence interval; Lesson 27 wraps xbar in a z interval.
TOLERANCE = 10.0
N_REPS = 8_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def draw_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps sample means of size n from N(100, 15).

    Parameters
    ----------
    n:
        Sample size inside each replication. SE(xbar) = SIGMA / sqrt(n).
    n_reps:
        Number of independent xbar values. Default N_REPS = 8_000.

    Returns
    -------
    np.ndarray
        Length n_reps. Each entry is the mean of n iid N(MU, SIGMA)
        draws. Rebuilt here so this file does not import Step 2.

    Notes
    -----
    default_rng(SEED) is created inside the call, so a given n always
    rebuilds the same list of means. .mean(axis=1) collapses each row
    of the (n_reps, n) matrix into one xbar.
    """
    rng = np.random.default_rng(SEED)
    return rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n)).mean(axis=1)


# --- NEW (1) small_sample_xbar() ---------------------------------------------
def small_sample_xbar() -> np.ndarray:
    """Simulate xbar from samples of size 5.

    Returns
    -------
    np.ndarray
        8,000 copies of xbar at n = 5.

    Notes
    -----
    Unbiasedness does not depend on n: E[xbar] = mu for every n >= 1.
    Variance does: Var(xbar) = sigma^2/n = 225/5 = 45, so the SD is
    15/sqrt(5) ~ 6.71. Mean squared error is MSE = Var + Bias^2 = 45
    because Bias = 0. That large MSE is why a single n = 5 sample can
    sit far from 100 even though the estimator is unbiased.

    Consistency is about n -> infinity, not about one n = 5 draw.
    """
    return draw_means(N_TINY)
# ------------------------------------------------------------------------------


# --- NEW (2) decision_error_rate() -------------------------------------------
def decision_error_rate(means: np.ndarray, n: int) -> dict[str, float]:
    """Report bias, spread, and P(|xbar - mu| > 10).

    Parameters
    ----------
    means:
        Monte Carlo list of xbar values from draw_means() or
        small_sample_xbar().
    n:
        Sample size that produced those means. Used for the formula SE
        sigma/sqrt(n) and stored in the returned dictionary.

    Returns
    -------
    dict[str, float]
        n, the Monte Carlo mean, bias = mean - mu, empirical SD, the
        formula SE, and p_miss_10 = P(|xbar - mu| > TOLERANCE).

    Notes
    -----
    Bias is the long-run average error E[xbar] - mu. p_miss_10 is a
    different quantity: the chance that one sample misses mu by more
    than 10. An unbiased estimator can have a large miss probability
    when its variance (and therefore its MSE) is large.

    np.abs(means - MU) > TOLERANCE is a boolean array. np.mean of
    booleans is the proportion True, the Monte Carlo estimate of
    that miss probability.

    At n = 5, 10 units is about 10/6.71 ~ 1.49 SEs, so misses are
    common. At n = 200, 10 units is about 10/1.06 ~ 9.4 SEs, so the
    event is essentially unseen in 8,000 replications.
    """
    return {
        "n": float(n),
        "mean": float(np.mean(means)),
        "bias": float(np.mean(means) - MU),
        "sd": float(np.std(means, ddof=1)),
        "formula_se": SIGMA / np.sqrt(n),
        "p_miss_10": float(np.mean(np.abs(means - MU) > TOLERANCE)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(tiny: np.ndarray, large: np.ndarray) -> Path:
    """Overlay sampling distributions of xbar at n = 5 and n = 200.

    Parameters
    ----------
    tiny:
        8,000 copies of xbar at n = 5 from small_sample_xbar().
    large:
        8,000 copies of xbar at n = 200 from draw_means(N_LARGE).

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Both histograms are centered at mu = 100 (unbiasedness). The n = 5
    histogram is wide: MSE = 45, and the dotted lines at 90 and 110
    mark the |error| = 10 decision. A non-trivial fraction of the red
    mass sits outside those lines. The n = 200 histogram is a spike
    inside the same window: same unbiasedness, much smaller variance.
    """
    output_path = DIR_FIGURES / "point_estimation_03_small_sample_variance.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(tiny, bins=30, density=True, color="#EC2661", alpha=0.45,
            edgecolor="#1A2E51", label="xbar n=5")
    ax.hist(large, bins=30, density=True, color="#1A2E51", alpha=0.55,
            edgecolor="#1A2E51", label="xbar n=200")
    ax.axvline(MU, color="#646464", ls="--", lw=1.3, label="True mu = 100")
    # Decision window |xbar - mu| = 10. Mass outside these lines is the
    # error rate printed as p_miss_10; it is not bias.
    ax.axvline(MU - TOLERANCE, color="#5B8DEF", ls=":", lw=1.2)
    ax.axvline(MU + TOLERANCE, color="#5B8DEF", ls=":", lw=1.2,
               label="|error| = 10")
    ax.set_xlabel("Estimator xbar")
    ax.set_ylabel("Density")
    ax.set_title("Unbiased at n = 5, but Too Noisy for a 10-Unit Decision")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 small-sample report and write the overlay figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    tiny = small_sample_xbar()
    large = draw_means(N_LARGE)
    tiny_summary = decision_error_rate(tiny, N_TINY)
    large_summary = decision_error_rate(large, N_LARGE)
    figure_path = save_figure(tiny, large)

    print("================================================================")
    print("LESSON 26 - STEP 3: SMALL SAMPLE VARIANCE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"n = 5 mean of xbar              : {tiny_summary['mean']:.6f}")
    # Near-zero bias: n = 5 is still unbiased. The problem is variance.
    print(f"n = 5 bias                      : {tiny_summary['bias']:.6f}")
    # Empirical SD should track 15/sqrt(5) ~ 6.708. MSE = 45 because
    # Bias = 0, so MSE equals Var(xbar) = sigma^2/n.
    print(f"n = 5 empirical SD              : {tiny_summary['sd']:.6f}")
    print(f"n = 5 formula SE                : {tiny_summary['formula_se']:.6f}")
    # Decision error, not bias: about 14% of n = 5 samples miss by > 10.
    print(f"n = 5 P(|xbar - mu| > 10)       : {tiny_summary['p_miss_10']:.6f}")
    print(f"n = 200 mean of xbar            : {large_summary['mean']:.6f}")
    print(f"n = 200 bias                    : {large_summary['bias']:.6f}")
    print(f"n = 200 empirical SD            : {large_summary['sd']:.6f}")
    # Same event at n = 200: MSE = 225/200 = 1.125, so the miss rate
    # collapses toward 0. Unbiasedness was never the missing piece.
    print(f"n = 200 P(|xbar - mu| > 10)     : {large_summary['p_miss_10']:.6f}")
    print("Limit: unbiasedness does not imply small variance")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

