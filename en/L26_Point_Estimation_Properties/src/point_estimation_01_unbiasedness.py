"""
Lesson 26 - Step 1: Two Unbiased Estimators of mu
=================================================
NEW IN THIS STEP: population_model(), estimator_means(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. population_model()     Normal(100, 15) synthetic cost clock
    2. estimator_means()      sampling means of xbar and of X1
    3. save_figure()          two bars against the true mu = 100

Context:
A fully synthetic cost clock is Normal(mu=100, sigma=15). Two estimators
of mu are compared: the sample mean xbar from n = 20 and the first
observation X1. Both are unbiased: their sampling means recover 100.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lessons 23-25 built sampling
distributions of xbar and phat. This script asks whether an estimator is
correct on average.

    stats.norm(loc, scale)   frozen Normal(mu, sigma) population
    rng.normal(...)          Monte Carlo draws from that same Normal
    draws.mean(axis=1)       xbar for each of 8,000 samples of size n
    draws[:, 0]              the one-observation estimator X1
    Bias = E[theta_hat] - theta     unbiased means this difference is 0
    MSE = Var + Bias^2       for unbiased estimators, MSE equals variance

main() reports the Monte Carlo means and biases of xbar and X1, then
writes the two-bar figure. No earlier lesson script is imported.

Run it:
    python point_estimation_01_unbiasedness.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the Monte Carlo samples.
# scipy.stats supplies the frozen Normal population in population_model().
import matplotlib
import numpy as np
from scipy import stats

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. estimator_means() forwards it to NumPy's
# Generator so every run rebuilds the same 8,000 samples.
SEED = 42
# True mean of the synthetic cost clock. Both estimators target this mu.
MU = 100.0
# Population SD. Var(X) = 15^2 = 225; that variance is the MSE of X1
# because X1 is unbiased. Step 2 compares it with Var(xbar) = 225/n.
SIGMA = 15.0
# Sample size for xbar. X1 ignores the other 19 draws on purpose.
N = 20
# Monte Carlo replications of the sampling distribution, not the sample
# size n. 8_000 is an integer literal 8000; the underscore is readability.
N_REPS = 8_000
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) population_model() ----------------------------------------------
def population_model():
    """Return the Normal(100, 15) synthetic cost population.

    Returns
    -------
    scipy.stats._distn_infrastructure.rv_frozen
        A frozen stats.norm object with loc=MU and scale=SIGMA. After
        this call, pdf/cdf/mean no longer need those parameters: they
        are stored on the object.

    Notes
    -----
    This is the population, not an estimator. A point estimator is a
    function of the sample that produces one number for mu. Unbiasedness
    is a property of that function: E[theta_hat] = theta.

    The Monte Carlo in estimator_means() draws with rng.normal using the
    same MU and SIGMA rather than calling this object, so the sampling
    step stays NumPy-only. The two routes describe the same N(100, 15).
    """
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NEW (2) estimator_means() -----------------------------------------------
def estimator_means(n: int = N, n_reps: int = N_REPS) -> dict[str, np.ndarray]:
    """Simulate xbar and the one-observation estimator X1.

    Parameters
    ----------
    n:
        Sample size inside each replication. Default N = 20. xbar uses
        all n draws; X1 uses only the first column.
    n_reps:
        Number of independent samples. Default N_REPS = 8_000. Each
        replication produces one xbar and one X1.

    Returns
    -------
    dict[str, np.ndarray]
        xbar is the length-n_reps list of sample means. one_obs is the
        matching list of first observations. dict[str, np.ndarray] is a
        type hint: string keys, NumPy-array values. Python does not
        enforce it at run time.

    Notes
    -----
    Both estimators are unbiased for mu:

        E[xbar] = mu,     E[X1] = mu.

    Bias is E[theta_hat] - theta, so both biases are 0. The Monte Carlo
    means will sit a few hundredths away from 100 because 8,000 draws
    still have sampling error; that remainder is not systematic bias.

    Mean squared error splits as MSE = Var(theta_hat) + [Bias]^2. With
    Bias = 0, MSE equals variance. This step only checks the means;
    Step 2 compares the variances, which is then also an MSE ranking.
    X1 is unbiased and still a poor estimator: its variance is sigma^2,
    not sigma^2/n.
    """
    rng = np.random.default_rng(SEED)
    # Shape (n_reps, n): 8,000 independent samples of size 20.
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    # axis=1 averages the n columns (one xbar per row). Column 0 is X1,
    # a single iid draw from N(mu, sigma), so Var(X1) = sigma^2.
    return {
        "xbar": draws.mean(axis=1),
        "one_obs": draws[:, 0],
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(estimators: dict[str, np.ndarray]) -> Path:
    """Compare sampling means of xbar and of the first observation.

    Parameters
    ----------
    estimators:
        Dictionary from estimator_means() with keys xbar and one_obs.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Each bar is the Monte Carlo mean of one estimator, an estimate of
    E[theta_hat]. The dashed line is the true mu = 100. Unbiasedness is
    both bars sitting on that line, not a claim about one sample of
    size 20. The figure does not show spread; variance and MSE wait
    for Step 2.
    """
    output_path = DIR_FIGURES / "point_estimation_01_unbiasedness.png"
    labels = ["Sample mean\nxbar, n=20", "One observation\nX1"]
    # float(...) unwraps NumPy scalars so the bar heights are plain floats.
    means = [float(np.mean(estimators["xbar"])),
             float(np.mean(estimators["one_obs"]))]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, means, color=colors, width=0.55)
    # Horizontal reference at the parameter. Unbiased estimators recover
    # this height on average.
    ax.axhline(MU, color="#646464", ls="--", lw=1.3, label="True mu = 100")
    ax.set_ylabel("Mean of the estimator")
    ax.set_title("Both Estimators Recover mu = 100: Unbiasedness")
    ax.set_ylim(90, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    for bar, value in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.6,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 unbiasedness report and write the two-bar figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    estimators = estimator_means()
    mean_xbar = float(np.mean(estimators["xbar"]))
    mean_one = float(np.mean(estimators["one_obs"]))
    figure_path = save_figure(estimators)

    print("================================================================")
    print("LESSON 26 - STEP 1: UNBIASEDNESS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    print(f"True mu                         : {MU:.6f}")
    print(f"Mean of xbar (n = 20)           : {mean_xbar:.6f}")
    # Bias = E[theta_hat] - theta. Near-zero values are Monte Carlo error
    # around a true bias of 0, not evidence of systematic shift.
    print(f"Bias of xbar                    : {mean_xbar - MU:.6f}")
    print(f"Mean of X1                      : {mean_one:.6f}")
    print(f"Bias of X1                      : {mean_one - MU:.6f}")
    print("Both estimators are unbiased")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

