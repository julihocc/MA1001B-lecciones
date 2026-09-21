"""
Lesson 32 - Step 3: Two-Variance F Is Sensitive to Non-Normality
================================================================
THE RECIPE
Start from f_two_var_02_f_test.py, then introduce:
    1. type_i_normal()          F-test Type I rate under equal normal variances
    2. type_i_heavy_tails()     same equal-variance H0, but t(3) samples
    3. save_figure()            contrast the two empirical Type I rates

Limit: when both stations have the same variance but heavy tails, the F
test rejects H0 far more often than alpha = 0.05. The two-variance F
procedure is sensitive to non-normality.

How to read this file:
You already know Python through OOP. Steps 1-2 formed F = s1^2 / s2^2
and read P(F >= f_stat) with scipy.stats.f.sf. Lesson 01 covers pathlib
and unattended savefig. This step keeps that same F test and asks how
often it rejects a true H0 under two different population shapes.

    F = s1^2 / s2^2              same ratio as Step 2, now 5000 times
    np.var(..., axis=1, ddof=1)  sample variance of each replication row
    stats.f.sf(F, df1, df2)      vectorized upper-tail p-values
    np.mean(p < alpha)           empirical Type I rate
    rng.normal(0, sigma, ...)    equal-variance normal samples (H0 true)
    rng.standard_t(3, ...)       equal-variance t(3) samples (H0 still true)

H0 is true in both experiments: the two groups share one variance. The
F(df1, df2) tail is calibrated for independent normal data. Heavy t(3)
tails inflate the rejection rate, so a small p-value is no longer a
reliable two-variance signal.

main() prints the two Type I rates next to nominal alpha = 0.05.

Run it:
    python f_two_var_03_nonnormal_sensitivity.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.f.sf is the same upper-tail reader as Step 2, now applied to
# thousands of F ratios at once. dfn = n1-1, dfd = n2-1.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Seed 42 now drives the two Monte Carlo experiments. The Step 1-2
# station samples are not reused; this script studies Type I error.
SEED = 42
N1 = 25
N2 = 25
# Number of independent two-sample replications in each experiment.
N_REPS = 5000
ALPHA = 0.05
# Common sd for the equal-variance normal experiment. Scale cancels in
# F = s1^2 / s2^2 when both groups share it, so the value 6 is a label.
EQUAL_SIGMA = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def f_reject_rate(samples_a: np.ndarray, samples_b: np.ndarray) -> float:
    """Share of replications with upper-tail p-value below alpha.

    Parameters
    ----------
    samples_a:
        Array of shape (n_reps, n1). Each row is one Station A sample.
    samples_b:
        Array of shape (n_reps, n2). Each row is one Station B sample.

    Returns
    -------
    float
        Fraction of rows with stats.f.sf(F, n1-1, n2-1) < ALPHA. When
        H0 is true, this is an empirical Type I rate.

    Notes
    -----
    axis=1 takes the sample variance of each row, not of the whole
    matrix. F = s1^2 / s2^2 is then a length-n_reps vector. stats.f.sf
    is vectorized: one call returns every upper-tail p-value. The Step 2
    scalar test is the same arithmetic applied once.
    """
    # ddof=1 on each row: the same sample-variance convention as Step 1.
    s1_sq = np.var(samples_a, axis=1, ddof=1)
    s2_sq = np.var(samples_b, axis=1, ddof=1)
    f_stats = s1_sq / s2_sq
    # Survival function of F(24, 24) at every observed ratio.
    p_values = stats.f.sf(f_stats, N1 - 1, N2 - 1)
    return float(np.mean(p_values < ALPHA))


# --- NEW (1) type_i_normal() -------------------------------------------------
def type_i_normal(n_reps: int = N_REPS) -> dict[str, float]:
    """Type I rate when both stations are normal with equal sigma.

    Parameters
    ----------
    n_reps:
        Number of independent two-sample replications. Default 5000.

    Returns
    -------
    dict[str, float]
        n_reps and type_i, the fraction of replications that reject H0.

    Notes
    -----
    Both groups are Normal(0, 6) so H0: sigma1^2 = sigma2^2 is true.
    Independent normal samples are the setting where F ~ F(df1, df2)
    under H0, so the Type I rate should sit near alpha = 0.05. The
    shared mean 0 is irrelevant: F compares variances, not means.
    """
    rng = np.random.default_rng(SEED)
    a = rng.normal(0.0, EQUAL_SIGMA, size=(n_reps, N1))
    b = rng.normal(0.0, EQUAL_SIGMA, size=(n_reps, N2))
    return {"n_reps": float(n_reps), "type_i": f_reject_rate(a, b)}
# ------------------------------------------------------------------------------


# --- NEW (2) type_i_heavy_tails() --------------------------------------------
def type_i_heavy_tails(n_reps: int = N_REPS) -> dict[str, float]:
    """Type I rate when both stations are t(3) with equal scale.

    Parameters
    ----------
    n_reps:
        Number of independent two-sample replications. Default 5000.

    Returns
    -------
    dict[str, float]
        n_reps and type_i, the fraction of replications that reject H0.

    Notes
    -----
    rng.standard_t(3, ...) draws Student's t with 3 degrees of freedom.
    Both groups share that same law, so the population variances are
    still equal and H0 remains true. t(3) has heavier tails than a
    normal, and the F(df1, df2) calibration assumes normality, so the
    test rejects too often. Equal variances are not enough.
    """
    rng = np.random.default_rng(SEED)
    # t(3) on both sides: equal variances, non-normal shape.
    a = rng.standard_t(3, size=(n_reps, N1))
    b = rng.standard_t(3, size=(n_reps, N2))
    return {"n_reps": float(n_reps), "type_i": f_reject_rate(a, b)}
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(normal_rate: float, heavy_rate: float) -> Path:
    """Contrast nominal alpha with Type I rates under two populations.

    Parameters
    ----------
    normal_rate:
        Empirical Type I rate from type_i_normal().
    heavy_rate:
        Empirical Type I rate from type_i_heavy_tails().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The dashed line is the nominal alpha = 0.05 that the F test is
    supposed to keep when H0 is true. The navy bar (normal) should sit
    near that line. The magenta bar (t(3)) sits well above it: the
    two-variance F procedure is sensitive to non-normality.
    """
    output_path = DIR_FIGURES / "f_two_var_03_nonnormal_sensitivity.png"
    labels = ["Equal-variance\nnormal", "Equal-variance\nt(3) tails"]
    values = [normal_rate, heavy_rate]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(ALPHA, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label=f"Nominal alpha = {ALPHA:.2f}")
    ax.set_ylabel("Empirical Type I rate")
    ax.set_title("Two-Variance F Is Sensitive to Non-Normality")
    ax.set_ylim(0, max(0.25, heavy_rate + 0.05))
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 Type I report and write the contrast figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    normal = type_i_normal()
    heavy = type_i_heavy_tails()
    figure_path = save_figure(normal["type_i"], heavy["type_i"])

    print("================================================================")
    print("LESSON 32 - STEP 3: NON-NORMAL SENSITIVITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Replications                    : {N_REPS}")
    print(f"n1, n2                          : {N1}, {N2}")
    print(f"Nominal alpha                   : {ALPHA:.6f}")
    # Calibrated case: H0 true and both groups normal. Near 0.05.
    print(f"Type I rate (normal, equal var) : {normal['type_i']:.6f}")
    # Same H0, t(3) tails: F rejects too often. Limit of this lesson.
    print(f"Type I rate (t(3), equal var)   : {heavy['type_i']:.6f}")
    print("Limit                          : two-variance F is sensitive to non-normality")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

