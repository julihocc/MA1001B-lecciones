"""
Lesson 24 - Step 2: Sample Means for n = 4 and n = 40
=====================================================
THE RECIPE
Start from clt_01_skewed_population.py, then introduce:
    1. simulate_means()         5,000 sample means, seed 42
    2. sampling_summaries()     mean, SE, and skewness of xbar
    3. save_figure()            histograms with a normal overlay

The same exponential delay population is rebuilt. For n = 40 the
histogram of xbar is much closer to a bell than for n = 4. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 built a right-skewed
Exponential(mean=10) delay clock. Lesson 01 covers pathlib and unattended
savefig; they are rebuilt here only so the script stays self-contained.
This step is the Central Limit Theorem (CLT) in pictures: xbar, not X,
becomes more normal as n grows.

    simulate_means(n)        5,000 iid samples of size n; each row mean
                             is one draw of xbar
    SE = 10 / sqrt(n)        sampling sd of xbar from Lesson 23
    skew(xbar) = 2 / sqrt(n) exponential mean-skew formula
    stats.norm(mu, SE).pdf   CLT overlay: N(10, 10/sqrt(n))
    n = 4 vs n = 40          small n still skewed; larger n closer to a bell

main() prints empirical versus theoretical SE and skewness for both
sample sizes, then saves the two-panel histogram.

Run it:
    python clt_02_means_n4_n40.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.expon rebuilds the Step 1 delay clock. stats.norm is the CLT
# overlay. stats.skew measures how far the simulated xbar values remain
# from a symmetric bell.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Course-wide seed. Each simulate_means() call starts a fresh Generator
# from 42, so the n = 4 and n = 40 streams are independent, not sequential.
SEED = 42
# Same exponential mean (and sd) as Step 1.
MEAN = 10.0
# Small n: CLT is a poor shape match. Large n: closer to a bell.
N_SMALL = 4
N_LARGE = 40
# 5,000 replications make the histogram and the empirical SE stable
# without a long run. Underscore in 5_000 is only readability.
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def delay_population():
    """Return the same Exponential(mean=10) delay clock as Step 1.

    scipy.stats.expon(scale=MEAN) freezes an exponential with mean =
    scale = 10. Rebuilt here so this file does not import Step 1.
    """
    return stats.expon(scale=MEAN)


# --- NEW (1) simulate_means() ------------------------------------------------
def simulate_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps samples of size n from the delay population.

    Parameters
    ----------
    n:
        Sample size inside each replication (4 or 40 in this lesson).
    n_reps:
        How many independent samples to draw. Default N_REPS = 5,000.

    Returns
    -------
    np.ndarray
        Length n_reps. Entry i is the sample mean xbar of the i-th
        iid sample of n exponential delays.

    Notes
    -----
    This is a Monte Carlo picture of the sampling distribution of xbar.
    The CLT claims that for large n those means look approximately
    Normal(mu, sigma/sqrt(n)), even though each delay X is exponential
    and right-skewed. n = 4 is not large on a skewness-2 clock; n = 40
    is closer.

    model.rvs(size=(n_reps, n), random_state=rng) fills a 2-D array:
    n_reps rows, n columns. .mean(axis=1) averages across columns, so
    each row collapses to one xbar. A new Generator(SEED) is created
    on every call, which keeps each sample size reproducible on its
    own seed-42 stream.
    """
    rng = np.random.default_rng(SEED)
    model = delay_population()
    # rvs = random variates from the frozen exponential. random_state
    # consumes rng so the draws are the seed-42 sequence, not a global
    # np.random stream.
    draws = model.rvs(size=(n_reps, n), random_state=rng)
    return draws.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NEW (2) sampling_summaries() --------------------------------------------
def sampling_summaries(means: np.ndarray, n: int) -> dict[str, float]:
    """Summarize the simulated sampling distribution of xbar.

    Parameters
    ----------
    means:
        The length-n_reps array returned by simulate_means(n).
    n:
        Sample size used to produce those means. Needed for the
        theoretical SE and theoretical skew formulas.

    Returns
    -------
    dict[str, float]
        mean_of_means should sit near 10. empirical_se is the sample
        sd of the simulated xbars (ddof=1). theoretical_se is
        10/sqrt(n). skewness is the bias-corrected sample skew of
        the xbars. theoretical_skew is 2/sqrt(n).

    Notes
    -----
    For iid observations with mean mu and sd sigma,
        E[xbar] = mu,    SE(xbar) = sigma / sqrt(n).
    Those two facts already held in Lesson 23. The CLT adds a shape
    statement: xbar is approximately normal for large n. For this
    exponential family the skewness of xbar is exactly 2/sqrt(n), so
    larger n shrinks skew at the same 1/sqrt(n) rate as it shrinks SE.
    """
    se = MEAN / np.sqrt(n)
    return {
        "n": float(n),
        "mean_of_means": float(np.mean(means)),
        # ddof=1 is the sample sd (divide by n_reps - 1), comparable
        # to the theoretical SE rather than a population sd of the 5,000.
        "empirical_se": float(np.std(means, ddof=1)),
        "theoretical_se": se,
        # bias=False uses the adjusted Fisher-Pearson coefficient.
        "skewness": float(stats.skew(means, bias=False)),
        # Exponential X has skew 2; the mean of n of them has skew 2/sqrt(n).
        "theoretical_skew": 2.0 / np.sqrt(n),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(means_small: np.ndarray, means_large: np.ndarray) -> Path:
    """Histogram xbar for n = 4 and n = 40 with a normal overlay.

    Parameters
    ----------
    means_small, means_large:
        Simulated xbar arrays from simulate_means(4) and
        simulate_means(40).

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Each panel is a density histogram of 5,000 sample means. The solid
    navy curve is the CLT approximation N(10, 10/sqrt(n)). The left
    panel (n = 4) still leans right; the right panel (n = 40) is closer
    to the overlay. The CLT does not claim the original delays X are
    normal — only that xbar is approximately normal for large n.
    """
    output_path = DIR_FIGURES / "clt_02_means_n4_n40.png"
    # 1 row, 2 columns of Axes. sharey=False because n = 40 is much
    # more concentrated, so a shared vertical scale would squash it.
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6), sharey=False)
    panels = [
        (axes[0], means_small, N_SMALL, "#5B8DEF"),
        (axes[1], means_large, N_LARGE, "#EC2661"),
    ]
    for ax, means, n, color in panels:
        se = MEAN / np.sqrt(n)
        ax.hist(means, bins=30, density=True, color=color, alpha=0.6,
                edgecolor="#1A2E51")
        grid = np.linspace(means.min(), means.max(), 200)
        # Frozen Normal(mu, SE): the CLT working model for xbar.
        ax.plot(grid, stats.norm(MEAN, se).pdf(grid), color="#1A2E51", lw=2.0)
        ax.axvline(MEAN, color="#646464", ls="--", lw=1.2)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Sample mean xbar")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
    axes[0].set_ylabel("Density")
    fig.suptitle("CLT: n = 40 Is Closer to Normal Than n = 4")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 CLT comparison for n = 4 and n = 40.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    means_small = simulate_means(N_SMALL)
    means_large = simulate_means(N_LARGE)
    small = sampling_summaries(means_small, N_SMALL)
    large = sampling_summaries(means_large, N_LARGE)
    figure_path = save_figure(means_small, means_large)

    print("================================================================")
    print("LESSON 24 - STEP 2: MEANS N=4 AND N=40")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"n = 4 mean of means             : {small['mean_of_means']:.6f}")
    print(f"n = 4 theoretical SE            : {small['theoretical_se']:.6f}")
    print(f"n = 4 empirical SE              : {small['empirical_se']:.6f}")
    print(f"n = 4 theoretical skew          : {small['theoretical_skew']:.6f}")
    print(f"n = 4 empirical skew            : {small['skewness']:.6f}")
    print(f"n = 40 mean of means            : {large['mean_of_means']:.6f}")
    print(f"n = 40 theoretical SE           : {large['theoretical_se']:.6f}")
    print(f"n = 40 empirical SE             : {large['empirical_se']:.6f}")
    print(f"n = 40 theoretical skew         : {large['theoretical_skew']:.6f}")
    print(f"n = 40 empirical skew           : {large['skewness']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

