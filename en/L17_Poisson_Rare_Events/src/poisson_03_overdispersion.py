"""
Lesson 17 - Step 3: Clustering Produces Overdispersion
======================================================
THE RECIPE
Start from poisson_02_simulate_shifts.py, then introduce:
    1. clustered_rate()     70% of shifts have lambda=2.0, 30% have lambda=6.0
    2. simulate_clustered() seed-42 mixture with the same overall mean 3.2
    3. save_figure()        Poisson variance versus clustered variance

If events cluster, the variance exceeds lambda. That overdispersion is the
limit of the Poisson equal-mean-and-variance assumption.

How to read this file:
You already know Python through OOP. Steps 1-2 built X ~ Poisson(3.2) and
compared exact probabilities with a seed-42 simulation. Lesson 01 covers
pathlib and unattended savefig. This step keeps the same overall mean
rate but drops the constant-lambda assumption.

    mixture of rates      70% Poisson(2.0) and 30% Poisson(6.0)
    law of total variance E[lambda] + Var(lambda)
    overdispersion        Var(X) > lambda when events cluster
    rng.random(n) < p     Bernoulli assignment of busy vs quiet shifts
    np.where(mask, a, b)  per-shift rate vector
    rng.poisson(lam=rates) Poisson draws with a different lambda each shift
    ax.axhline            horizontal reference line at a variance

main() prints the theoretical mixture variance and the simulated clustered
variance. Matching the average rate does not restore Poisson(3.2).

Run it:
    python poisson_03_overdispersion.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.poisson is imported so the file keeps the same scientific stack
# as Steps 1-2, even though this step's figure is a variance comparison.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
# Overall mean rate, still 3.2, but no single clustered shift has this lambda.
LAMBDA = 3.2
N_SHIFTS = 10_000
# 30% of shifts are busy. The complementary 70% are quiet.
P_BUSY = 0.30
# Two rates that average to LAMBDA: 0.70 * 2.0 + 0.30 * 6.0 = 3.2.
# Constant lambda was the Poisson assumption; these two values break it.
LAMBDA_QUIET = 2.0
LAMBDA_BUSY = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def simulate_shifts(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Draw n_shifts Poisson(lambda) event counts, rebuilt from Step 2.

    np.random.default_rng(seed) is a fresh Generator. rng.poisson draws
    independent Poisson(LAMBDA) counts. This file does not import Step 2.
    """
    rng = np.random.default_rng(seed)
    return rng.poisson(lam=LAMBDA, size=n_shifts)


# --- NEW (1) clustered_rate() ------------------------------------------------
def clustered_rate() -> dict[str, float]:
    """Return the two-point mixture of rates with mean 3.2.

    Returns
    -------
    dict[str, float]
        mean_lambda is E[lambda] = 0.70 * 2.0 + 0.30 * 6.0 = 3.2.
        var_lambda is Var(lambda) across quiet and busy shifts.
        mixture_variance is E[X] + Var(lambda), the law of total variance.

    Notes
    -----
    Given the shift type, X is still Poisson, so E[X | type] = lambda and
    Var(X | type) = lambda. Averaging those pieces gives
        Var(X) = E[Var(X | type)] + Var(E[X | type])
               = E[lambda] + Var(lambda).
    With these two rates, Var(lambda) = 3.36, so the mixture variance is
    3.2 + 3.36 = 6.56, which already exceeds lambda. A mixture of Poisson
    rates with the same mean is not Poisson: overdispersion is the gap
    Var(X) > lambda.
    """
    mean_lambda = (1.0 - P_BUSY) * LAMBDA_QUIET + P_BUSY * LAMBDA_BUSY
    var_lambda = (1.0 - P_BUSY) * (LAMBDA_QUIET - mean_lambda) ** 2 + P_BUSY * (
        LAMBDA_BUSY - mean_lambda
    ) ** 2
    return {
        "mean_lambda": mean_lambda,
        "var_lambda": var_lambda,
        "mixture_variance": mean_lambda + var_lambda,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_clustered() --------------------------------------------
def simulate_clustered(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Draw clustered counts from a Poisson mixture with seed 42.

    Parameters
    ----------
    n_shifts:
        Number of independent synthetic shifts. Default N_SHIFTS = 10_000.
    seed:
        Generator seed. Default SEED = 42. This function builds its own
        Generator, so it does not share a stream with simulate_shifts().

    Returns
    -------
    np.ndarray
        Length n_shifts. Each entry is Poisson given that shift's rate:
        lambda = 6.0 on a busy shift, lambda = 2.0 on a quiet shift.

    Notes
    -----
    rng.random(n) draws Uniform(0, 1). Comparing with P_BUSY assigns each
    shift to busy or quiet (a Bernoulli trial). np.where builds the
    per-shift rate vector, and rng.poisson(lam=rates) then draws a Poisson
    count with a different lambda on each shift. Clustering is this
    extra layer of randomness in the rate.
    """
    rng = np.random.default_rng(seed)
    is_busy = rng.random(n_shifts) < P_BUSY
    rates = np.where(is_busy, LAMBDA_BUSY, LAMBDA_QUIET)
    return rng.poisson(lam=rates)
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    poisson_draws: np.ndarray,
    clustered_draws: np.ndarray,
    expected_clustered_var: float,
) -> Path:
    """Contrast Poisson variance with clustered overdispersion.

    Parameters
    ----------
    poisson_draws:
        Constant-lambda simulation from simulate_shifts().
    clustered_draws:
        Mixture simulation from simulate_clustered().
    expected_clustered_var:
        Theoretical mixture variance E[lambda] + Var(lambda) from
        clustered_rate().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The navy bar is simulated Var(X) under Poisson(3.2) and should sit
    near lambda. The red bar is simulated Var(X) under the clustered
    mixture and sits near 6.56, above both reference lines. Overdispersion
    is that red bar exceeding lambda: matching the average rate does not
    restore the Poisson variance.
    """
    output_path = DIR_FIGURES / "poisson_03_overdispersion.png"
    labels = ["Poisson\nvariance", "Clustered\nvariance"]
    values = [float(np.var(poisson_draws, ddof=0)), float(np.var(clustered_draws, ddof=0))]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    # Dashed line at lambda: the Poisson equal-mean-and-variance target.
    ax.axhline(LAMBDA, color="#5B8DEF", linestyle="--", lw=1.6, label="lambda = 3.2")
    ax.axhline(
        expected_clustered_var,
        color="#EC2661",
        linestyle=":",
        lw=1.6,
        label=f"mixture Var = {expected_clustered_var:.2f}",
    )
    ax.set_ylabel("Variance of event count")
    ax.set_title("Clustering Makes Variance Exceed lambda")
    ax.set_ylim(0, 8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(fontsize=8)
    # zip pairs each BarContainer patch with its variance so the label
    # can sit at the center of the bar, slightly above the top.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 overdispersion report and write the variance figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    rates = clustered_rate()
    poisson_draws = simulate_shifts()
    clustered_draws = simulate_clustered()
    poisson_var = float(np.var(poisson_draws, ddof=0))
    clustered_mean = float(np.mean(clustered_draws))
    clustered_var = float(np.var(clustered_draws, ddof=0))
    figure_path = save_figure(poisson_draws, clustered_draws, rates["mixture_variance"])

    print("================================================================")
    print("LESSON 17 - STEP 3: OVERDISPERSION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Quiet lambda                    : {LAMBDA_QUIET:.6f}")
    print(f"Busy lambda                     : {LAMBDA_BUSY:.6f}")
    print(f"Mixture mean lambda             : {rates['mean_lambda']:.6f}")
    # E[lambda] + Var(lambda) = 3.2 + 3.36 = 6.56, already above lambda.
    print(f"Theoretical mixture variance    : {rates['mixture_variance']:.6f}")
    print(f"Poisson simulated variance      : {poisson_var:.6f}")
    print(f"Clustered simulated mean        : {clustered_mean:.6f}")
    print(f"Clustered simulated variance    : {clustered_var:.6f}")
    # True when the clustered simulation exceeds the Poisson property.
    print(f"Variance exceeds lambda         : {clustered_var > LAMBDA}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

