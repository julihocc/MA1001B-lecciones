"""
Lesson 23 - Step 3: SE Assumes iid Draws
========================================
THE RECIPE
Start from sampling_mean_02_n9_vs_n36.py, then introduce:
    1. simulate_clustered_means()  n = 36 as 6 clusters of 6 copies
    2. se_inflation()              empirical SE versus sigma / sqrt(36)
    3. save_figure()               iid histogram versus clustered histogram

The SE formula sigma / sqrt(n) assumes iid draws from the defined
population. Clustered copies make the effective sample closer to 6, so
the observed SE stays near 12 / sqrt(6), not 12 / sqrt(36).

How to read this file:
You already know Python through OOP. Steps 1-2 built SE(xbar) = sigma / sqrt(n)
and checked it with 5,000 iid samples. Lesson 01 covers pathlib and
unattended savefig. This step keeps n = 36 on paper but drops independence
by copying each of 6 draws six times.

    rng.normal(..., size=(n_reps, 6))   six unique cluster values per row
    np.repeat(..., 6, axis=1)           copy each cluster across columns
    copies.mean(axis=1)                 xbar of 36 copies, still 6 numbers
    clustered SE / iid SE               inflation when iid is broken

main() prints the formula SE at n = 36 and n = 6, both empirical SEs, and
the inflation ratio. Matching the row length 36 does not restore iid.

Run it:
    python sampling_mean_03_iid_limit.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 80.0
SIGMA = 12.0
N_LARGE = 36
# Six unique draws, each copied CLUSTER_SIZE times, still fill n = 36 slots.
N_CLUSTERS = 6
CLUSTER_SIZE = 6
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def simulate_sample_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps iid samples of size n and return the sample means.

    Rebuilt from Step 2 so this file does not import it. size=(n_reps, n)
    stores one sample per row; .mean(axis=1) is xbar for that row.
    """
    rng = np.random.default_rng(SEED)
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    # axis=1 averages the n iid observations in the row, not the replications.
    return draws.mean(axis=1)


# --- NEW (1) simulate_clustered_means() --------------------------------------
def simulate_clustered_means(n_reps: int = N_REPS) -> np.ndarray:
    """Repeat 6 cluster draws six times each, then average the 36 copies.

    Parameters
    ----------
    n_reps:
        Number of independent clustered samples. Default N_REPS = 5,000.

    Returns
    -------
    np.ndarray
        Length n_reps. Each entry is the mean of 36 numbers, but only 6
        of those numbers were drawn; the rest are copies.

    Notes
    -----
    A row that looks like size 36 is six unique Normal(mu, sigma) values,
    each written six times. Those copies are dependent, so the iid SE
    formula sigma / sqrt(36) does not apply. The mean of the 36 copies
    equals the mean of the 6 unique draws, so the sampling sd stays near
    sigma / sqrt(6).
    """
    rng = np.random.default_rng(SEED)
    # Only six unique cycle times per replication, not 36.
    clusters = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, N_CLUSTERS))
    # axis=1 repeats along the sample axis: each of the 6 columns is
    # written CLUSTER_SIZE times. Shape becomes (n_reps, 36).
    copies = np.repeat(clusters, CLUSTER_SIZE, axis=1)
    # Same axis=1 mean as the iid case, but the 36 entries are not iid.
    return copies.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NEW (2) se_inflation() --------------------------------------------------
def se_inflation(iid_means: np.ndarray, clustered_means: np.ndarray) -> dict[str, float]:
    """Contrast iid SE with the inflated clustered SE.

    Parameters
    ----------
    iid_means:
        Simulated xbar from 36 iid draws (Step 2 design).
    clustered_means:
        Simulated xbar from 6 unique draws copied six times each.

    Returns
    -------
    dict[str, float]
        iid_se and clustered_se are sample sds of those xbar arrays
        (ddof=1). formula_n36 is sigma / sqrt(36); formula_n6 is
        sigma / sqrt(6). inflation is clustered_se / iid_se.

    Notes
    -----
    The iid empirical SE should sit near 2. The clustered empirical SE
    should sit near 12 / sqrt(6) ≈ 4.90, about twice as wide, because
    repeating a cluster does not create new independent information.
    """
    iid_se = float(np.std(iid_means, ddof=1))
    clustered_se = float(np.std(clustered_means, ddof=1))
    return {
        "iid_se": iid_se,
        "clustered_se": clustered_se,
        "formula_n36": SIGMA / np.sqrt(N_LARGE),
        "formula_n6": SIGMA / np.sqrt(N_CLUSTERS),
        "inflation": clustered_se / iid_se,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(iid_means: np.ndarray, clustered_means: np.ndarray) -> Path:
    """Compare iid n = 36 means with clustered n = 36 means.

    Parameters
    ----------
    iid_means, clustered_means:
        Simulated xbar arrays from se_inflation().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Both histograms use 36 slots per sample. The navy/blue iid panel is
    tight around mu (SE near 2). The red clustered overlay is wider
    (SE near 12/sqrt(6)). Matching n on paper does not restore iid.
    """
    output_path = DIR_FIGURES / "sampling_mean_03_iid_limit.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(iid_means, bins=30, density=True, color="#5B8DEF", alpha=0.55,
            edgecolor="#1A2E51", label="iid n = 36")
    ax.hist(clustered_means, bins=30, density=True, color="#EC2661", alpha=0.45,
            edgecolor="#1A2E51", label="6 clusters of 6 copies")
    ax.axvline(MU, color="#1A2E51", ls="--", lw=1.2)
    ax.set_xlabel("Sample mean xbar")
    ax.set_ylabel("Density")
    ax.set_title("Clustered Copies Inflate SE Above sigma / sqrt(36)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 iid-limit comparison and write the overlay figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    iid_means = simulate_sample_means(N_LARGE)
    clustered_means = simulate_clustered_means()
    summary = se_inflation(iid_means, clustered_means)
    figure_path = save_figure(iid_means, clustered_means)

    print("================================================================")
    print("LESSON 23 - STEP 3: IID LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"Formula SE n = 36               : {summary['formula_n36']:.6f}")
    print(f"iid empirical SE                : {summary['iid_se']:.6f}")
    print(f"Formula SE n = 6                : {summary['formula_n6']:.6f}")
    print(f"Clustered empirical SE          : {summary['clustered_se']:.6f}")
    print(f"SE inflation ratio              : {summary['inflation']:.6f}")
    print("Limit: SE assumes iid draws from the defined population")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

