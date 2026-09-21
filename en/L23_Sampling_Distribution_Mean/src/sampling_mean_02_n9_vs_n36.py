"""
Lesson 23 - Step 2: Simulated Sampling Distributions
====================================================
THE RECIPE
Start from sampling_mean_01_standard_error.py, then introduce:
    1. simulate_sample_means()  5,000 iid samples of size n, seed 42
    2. empirical_se()           observed sd of xbar versus sigma / sqrt(n)
    3. save_figure()            histograms of xbar for n = 9 and n = 36

The same Normal(80, 12) population is rebuilt. No earlier lesson script
is imported.

How to read this file:
You already know Python through OOP. Step 1 defined SE(xbar) = sigma / sqrt(n)
as a formula. Lesson 01 covers pathlib and unattended savefig; they are
rebuilt here only so the script stays self-contained. This step checks that
formula by simulating many sample means.

    rng.normal(..., size=(n_reps, n))   one row = one sample of n draws
    draws.mean(axis=1)                  xbar for each row (across columns)
    np.std(means, ddof=1)               sample sd of the simulated xbar
    stats.norm(MU, SE).pdf              theoretical sampling density overlay

main() prints the mean of means and both SEs for n = 9 and n = 36, then
saves the two-panel histogram.

Run it:
    python sampling_mean_02_n9_vs_n36.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm overlays the theoretical sampling density of xbar from Step 1.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Same seed, population, and sample sizes as Step 1. Now the seed is used:
# every Normal draw goes through default_rng(SEED).
SEED = 42
MU = 80.0
SIGMA = 12.0
N_SMALL = 9
N_LARGE = 36
# How many independent samples of size n. Each sample produces one xbar.
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def standard_error(n: int, sigma: float = SIGMA) -> float:
    """Return SE = sigma / sqrt(n) for an iid sample mean, rebuilt from Step 1.

    This is the sd of xbar, not of one cycle time X. n = 9 gives 4;
    n = 36 gives 2. Rebuilt here so this file does not import Step 1.
    """
    return sigma / np.sqrt(n)


# --- NEW (1) simulate_sample_means() -----------------------------------------
def simulate_sample_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps iid samples of size n and return the sample means.

    Parameters
    ----------
    n:
        Observations in one sample. Each row of the draw array has this
        many cycle times.
    n_reps:
        Number of independent samples (rows). Default N_REPS = 5,000.

    Returns
    -------
    np.ndarray
        Length n_reps. Entry i is xbar for the i-th sample: the mean of
        n iid Normal(mu, sigma) draws.

    Notes
    -----
    The sampling distribution of xbar is the distribution of this array.
    Its mean should sit near mu and its sd near sigma / sqrt(n). The same
    SEED is used for every n, so n = 9 and n = 36 are two separate
    streams that both start at 42; they are not one continued stream.
    """
    # One Generator per call, always seeded at 42. Do not mix this with
    # the older np.random.seed() global state.
    rng = np.random.default_rng(SEED)
    # size=(n_reps, n) is a 2-D array: rows are replications, columns are
    # the n observations inside one sample. Each entry is one cycle time.
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    # axis=1 averages across columns (the sample), so each row collapses
    # to one xbar. axis=0 would average down replications and is wrong.
    return draws.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NEW (2) empirical_se() --------------------------------------------------
def empirical_se(means: np.ndarray, n: int) -> dict[str, float]:
    """Compare the observed sd of xbar with the theoretical SE.

    Parameters
    ----------
    means:
        Simulated xbar values from simulate_sample_means().
    n:
        Sample size used to produce those means, forwarded to the formula.

    Returns
    -------
    dict[str, float]
        n is stored as a float for a uniform dict type.
        mean_of_means is the average of the simulated xbar (near mu).
        empirical_se is the sample sd of those xbar values.
        theoretical_se is sigma / sqrt(n) from standard_error().

    Notes
    -----
    np.std(..., ddof=1) divides by n_reps - 1, the sample sd of the
    Monte Carlo xbar list. That checks the formula; it does not replace
    sigma / sqrt(n). 5,000 replications should land close to 4 (n = 9)
    and 2 (n = 36).
    """
    return {
        "n": float(n),
        "mean_of_means": float(np.mean(means)),
        "empirical_se": float(np.std(means, ddof=1)),
        "theoretical_se": standard_error(n),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(means_small: np.ndarray, means_large: np.ndarray) -> Path:
    """Histogram the simulated sampling distributions side by side.

    Parameters
    ----------
    means_small, means_large:
        Simulated xbar arrays for n = 9 and n = 36.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Each panel is a histogram of 5,000 xbar values (density=True so the
    area is 1). The solid curve is the theoretical Normal(mu, SE) from
    Step 1. The n = 36 panel is narrower: larger n shrinks SE.
    """
    output_path = DIR_FIGURES / "sampling_mean_02_n9_vs_n36.png"
    # 1 row, 2 columns; sharey=True uses one density scale for both n.
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6), sharey=True)
    panels = [
        (axes[0], means_small, N_SMALL, "#5B8DEF"),
        (axes[1], means_large, N_LARGE, "#EC2661"),
    ]
    for ax, means, n, color in panels:
        ax.hist(means, bins=30, density=True, color=color, alpha=0.6,
                edgecolor="#1A2E51")
        # Fine grid for the theoretical sampling density of xbar.
        grid = np.linspace(means.min(), means.max(), 200)
        ax.plot(grid, stats.norm(MU, standard_error(n)).pdf(grid),
                color="#1A2E51", lw=2.0)
        # Vertical line at mu: the sampling distribution is centered there.
        ax.axvline(MU, color="#646464", ls="--", lw=1.2)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Sample mean xbar")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
    axes[0].set_ylabel("Density")
    fig.suptitle("5,000 Seed-42 Samples Recover SE = sigma / sqrt(n)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 Monte Carlo check of SE(xbar) at n = 9 and n = 36.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    means_small = simulate_sample_means(N_SMALL)
    means_large = simulate_sample_means(N_LARGE)
    small = empirical_se(means_small, N_SMALL)
    large = empirical_se(means_large, N_LARGE)
    figure_path = save_figure(means_small, means_large)

    print("================================================================")
    print("LESSON 23 - STEP 2: N=9 VERSUS N=36")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"n = 9 mean of means             : {small['mean_of_means']:.6f}")
    print(f"n = 9 theoretical SE            : {small['theoretical_se']:.6f}")
    print(f"n = 9 empirical SE              : {small['empirical_se']:.6f}")
    print(f"n = 36 mean of means            : {large['mean_of_means']:.6f}")
    print(f"n = 36 theoretical SE           : {large['theoretical_se']:.6f}")
    print(f"n = 36 empirical SE             : {large['empirical_se']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

