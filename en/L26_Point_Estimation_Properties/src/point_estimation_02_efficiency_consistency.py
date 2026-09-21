"""
Lesson 26 - Step 2: Efficiency and Consistency
==============================================
THE RECIPE
Start from point_estimation_01_unbiasedness.py, then introduce:
    1. estimator_spreads()      variance of xbar versus variance of X1
    2. consistency_check()      n = 20 versus n = 200
    3. save_figure()            boxplots of the four sampling distributions

xbar is more efficient than X1 at the same n. Raising n from 20 to 200
shrinks the spread of xbar: consistency.

How to read this file:
You already know Python through OOP. Step 1 showed that xbar and X1 are
both unbiased for mu. Lesson 01 covers pathlib and unattended savefig;
they are rebuilt here only so the script stays self-contained. This step
compares variances (efficiency) and then raises n (consistency).

    Var(X1) = sigma^2            15^2 = 225
    Var(xbar) = sigma^2 / n      225/20 = 11.25
    efficiency ratio             Var(X1)/Var(xbar) is about n = 20
    MSE = Var + Bias^2           both unbiased, so MSE equals variance
    consistency                  Var(xbar) -> 0 as n grows
    np.var(..., ddof=1)          sample variance of the Monte Carlo list

main() prints formula and empirical variances, the efficiency ratio, and
SD(xbar) at n = 20 and n = 200. No earlier lesson script is imported.

Run it:
    python point_estimation_02_efficiency_consistency.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed, same mu and sigma as Step 1. This file rebuilds the
# Normal(100, 15) clock; it does not import Step 1.
SEED = 42
MU = 100.0
SIGMA = 15.0
# Two sample sizes for xbar. Efficiency compares estimators at the same n
# (here N_SMALL). Consistency compares one estimator as n grows.
N_SMALL = 20
N_LARGE = 200
N_REPS = 8_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def draw_samples(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Draw n_reps samples of size n from N(100, 15).

    Parameters
    ----------
    n:
        Columns in the returned matrix: the sample size inside one
        replication.
    n_reps:
        Rows in the returned matrix. Default N_REPS = 8_000.

    Returns
    -------
    np.ndarray
        Shape (n_reps, n). Each row is one iid sample from N(MU, SIGMA).

    Notes
    -----
    np.random.default_rng(SEED) is created inside the call, so two calls
    with the same n rebuild the same matrix. A call with a different n
    is a different array, still starting from seed 42. Rebuilt here so
    this file does not import Step 1.
    """
    rng = np.random.default_rng(SEED)
    return rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))


# --- NEW (1) estimator_spreads() ---------------------------------------------
def estimator_spreads(draws: np.ndarray) -> dict[str, float]:
    """Compare the variance of xbar with the variance of X1.

    Parameters
    ----------
    draws:
        Monte Carlo matrix of shape (n_reps, n) from draw_samples().
        Column 0 is the X1 estimator; the row mean is xbar.

    Returns
    -------
    dict[str, float]
        var_xbar and var_one are Monte Carlo sample variances (ddof=1).
        sd_xbar and sd_one are the matching SDs. efficiency_ratio is
        Var(X1)/Var(xbar). formula_var_xbar is sigma^2/n; formula_var_one
        is sigma^2.

    Notes
    -----
    Efficiency ranks unbiased estimators at a fixed n: the one with
    smaller variance wins. For iid draws from a population with variance
    sigma^2,

        Var(xbar) = sigma^2 / n,     Var(X1) = sigma^2.

    At n = 20 that is 11.25 versus 225, so xbar is about 20 times more
    efficient. Relative efficiency equals that variance ratio.

    Mean squared error is MSE(theta_hat) = Var(theta_hat) + [Bias]^2.
    Step 1 already showed Bias = 0 for both estimators, so MSE(xbar) =
    11.25 and MSE(X1) = 225. Ranking by variance is ranking by MSE.

    ddof=1 divides by n_reps-1, the unbiased sample variance of the
    Monte Carlo sampling distribution, not the variance of one sample
    of costs.
    """
    xbar = draws.mean(axis=1)
    one_obs = draws[:, 0]
    return {
        "var_xbar": float(np.var(xbar, ddof=1)),
        "var_one": float(np.var(one_obs, ddof=1)),
        "sd_xbar": float(np.std(xbar, ddof=1)),
        "sd_one": float(np.std(one_obs, ddof=1)),
        # Larger than 1 means xbar has the smaller variance (and MSE).
        "efficiency_ratio": float(np.var(one_obs, ddof=1) / np.var(xbar, ddof=1)),
        # draws.shape[1] is n, so this is sigma^2 / n.
        "formula_var_xbar": SIGMA**2 / draws.shape[1],
        "formula_var_one": SIGMA**2,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) consistency_check() ---------------------------------------------
def consistency_check() -> dict[str, np.ndarray]:
    """Return xbar samples for n = 20 and n = 200.

    Returns
    -------
    dict[str, np.ndarray]
        n20 and n200 are length-N_REPS arrays of sample means.

    Notes
    -----
    Consistency is a large-n property: theta_hat_n converges in
    probability to theta as n -> infinity. For xbar that follows from
    Var(xbar) = sigma^2/n -> 0 (and Bias stays 0, so MSE -> 0 too).

    n = 200 is not infinity, but SE falls from 15/sqrt(20) = 3.354
    to 15/sqrt(200) = 1.061. The boxplot of xbar should shrink toward
    mu = 100. X1 is not consistent: its variance stays sigma^2 no
    matter how large n is, because it still uses one observation.
    """
    small = draw_samples(N_SMALL).mean(axis=1)
    large = draw_samples(N_LARGE).mean(axis=1)
    return {"n20": small, "n200": large}
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    draws_small: np.ndarray,
    means_large: np.ndarray,
) -> Path:
    """Boxplot X1, xbar n=20, and xbar n=200.

    Parameters
    ----------
    draws_small:
        Monte Carlo matrix at n = 20. Column 0 is X1; the row mean is
        xbar at n = 20.
    means_large:
        Length-N_REPS array of xbar at n = 200 from consistency_check().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Three sampling distributions, all centered at mu (unbiasedness).
    Width is the lesson: X1 is widest (Var = 225), xbar at n = 20 is
    tighter (Var = 11.25), and xbar at n = 200 is tighter still
    (consistency). Box width is a picture of variance and of MSE
    because Bias = 0.
    """
    output_path = DIR_FIGURES / "point_estimation_02_efficiency_consistency.png"
    data = [draws_small[:, 0], draws_small.mean(axis=1), means_large]
    labels = ["X1", "xbar n=20", "xbar n=200"]
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    boxes = ax.boxplot(data, tick_labels=labels, patch_artist=True, widths=0.55)
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.55)
    ax.axhline(MU, color="#646464", ls="--", lw=1.3)
    ax.set_ylabel("Estimator value")
    ax.set_title("xbar Is More Efficient Than X1; Larger n Is More Consistent")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 efficiency and consistency report and write the figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    draws_small = draw_samples(N_SMALL)
    spreads = estimator_spreads(draws_small)
    means = consistency_check()
    figure_path = save_figure(draws_small, means["n200"])
    sd_n200 = float(np.std(means["n200"], ddof=1))

    print("================================================================")
    print("LESSON 26 - STEP 2: EFFICIENCY AND CONSISTENCY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS:,}")
    # Formula Var(X1) = sigma^2 = 225. Empirical value is the Monte Carlo
    # sample variance of 8,000 copies of X1.
    print(f"Var(X1) formula                 : {spreads['formula_var_one']:.6f}")
    print(f"Var(X1) empirical               : {spreads['var_one']:.6f}")
    # Formula Var(xbar) = 225/20 = 11.25. Because Bias = 0, this is also
    # MSE(xbar) at n = 20.
    print(f"Var(xbar n=20) formula          : {spreads['formula_var_xbar']:.6f}")
    print(f"Var(xbar n=20) empirical        : {spreads['var_xbar']:.6f}")
    # Relative efficiency of xbar versus X1: Var(X1)/Var(xbar) ~ n = 20.
    print(f"Efficiency ratio Var(X1)/Var(xbar): {spreads['efficiency_ratio']:.6f}")
    print(f"SD(xbar n=20)                   : {spreads['sd_xbar']:.6f}")
    # Consistency: SD should track sigma/sqrt(n) = 15/sqrt(200) = 1.061.
    print(f"SD(xbar n=200)                  : {sd_n200:.6f}")
    print(f"Formula SE n=200                : {SIGMA / np.sqrt(N_LARGE):.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

