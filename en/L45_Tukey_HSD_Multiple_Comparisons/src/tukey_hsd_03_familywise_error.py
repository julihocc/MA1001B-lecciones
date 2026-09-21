"""
Lesson 45 - Step 3: Unadjusted Tests Inflate Familywise Error
=============================================================

THE RECIPE
----------
Start from tukey_hsd_02_tukey_hsd.py, then introduce:
    1. simulate_null_experiments()  5000 three-group studies under equal means
    2. familywise_rates()           unadjusted t versus Tukey rejection rates
    3. save_figure()                compare empirical FWER with alpha=0.05

Context:
--------
Why do we need Tukey's HSD? Why not just use unadjusted t-tests? This script
runs a Monte Carlo simulation of the null hypothesis (meaning all groups have
the exact same true population mean). Under the global null, any "significant"
difference we find is a false positive (Type I error). We expect a 5% false
positive rate.
Limit: pairwise t tests without correction inflate familywise error. Under the
global null, at least one unadjusted pair rejects more often than 5 percent.
Tukey keeps that familywise rate near the advertised alpha.

How to read this file:
----------------------
1. `simulate_null_experiments()` repeatedly draws random samples where all means
   are identical. It tracks how often unadjusted t-tests and Tukey HSD incorrectly
   reject the null hypothesis.
2. `familywise_rates()` calculates the percentage of experiments where at least
   one false positive occurred (the Familywise Error Rate, FWER).
3. `save_figure()` creates a bar chart showing the inflated FWER of unadjusted
   tests compared to the protected Tukey HSD.

Run it:
-------
    uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_03_familywise_error.py
"""

from pathlib import Path

# matplotlib for plotting
import matplotlib
# numpy is heavily used here for vectorized array operations (fast simulations)
import numpy as np
# pandas for dataframes
import pandas as pd
# scipy.stats provides distributions for critical values (t and studentized range)
from scipy import stats
# statsmodels provides the Tukey HSD function for a sample check
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Use Agg backend for headless plotting
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CONSTANTS ---
SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = K_GROUPS * N_PER_GROUP
TREATMENTS = ("Standard", "Guided", "Automated")
# NULL_MEAN is the single true population mean for ALL groups (H0 is true)
NULL_MEAN = 48.0
SIGMA = 3.2
ALPHA = 0.05
# N_SIMULATIONS is the number of imaginary experiments we will run
N_SIMULATIONS = 5000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) simulate_null_experiments() -------------------------------------
def simulate_null_experiments(seed: int = SEED) -> pd.DataFrame:
    """
    Simulate 5000 experiments in which all three true means are equal.

    Parameters
    ----------
    seed : int, optional
        Random seed for replicability.

    Returns
    -------
    tuple[pd.DataFrame, object]
        A DataFrame of booleans indicating if each simulation had ANY rejection
        for unadjusted tests and for Tukey tests. Also returns the Tukey result
        object for the very first simulation as an example.

    Notes
    -----
    This function uses vectorized numpy operations to run 5000 experiments
    almost instantly. Doing this with nested for-loops would be very slow.
    """
    rng = np.random.default_rng(seed)

    # data shape: (5000 simulations, 3 groups, 12 observations)
    data = rng.normal(
        NULL_MEAN, SIGMA, size=(N_SIMULATIONS, K_GROUPS, N_PER_GROUP)
    )

    # Calculate means and variances along the observations axis (axis=2)
    means = data.mean(axis=2)
    group_vars = data.var(axis=2, ddof=1)

    # Degrees of freedom for a two-sample t-test
    df_pair = 2 * N_PER_GROUP - 2
    # Critical t-value for two-tailed test at alpha=0.05
    t_crit = float(stats.t.ppf(1.0 - ALPHA / 2.0, df_pair))

    # Indices for pairwise comparisons (0 vs 1, 0 vs 2, 1 vs 2)
    pairs = ((0, 1), (0, 2), (1, 2))

    # Boolean array keeping track of whether ANY pair in a simulation rejected H0
    unadjusted_any = np.zeros(N_SIMULATIONS, dtype=bool)

    # --- Unadjusted t-tests (Vectorized) ---
    for i, j in pairs:
        # Calculate pooled variance for the pair across all 5000 simulations
        pooled = (
            (N_PER_GROUP - 1) * group_vars[:, i]
            + (N_PER_GROUP - 1) * group_vars[:, j]
        ) / df_pair
        # Standard error of the difference
        se_diff = np.sqrt(pooled * (2.0 / N_PER_GROUP))
        # Compute t-statistics
        t_stat = (means[:, i] - means[:, j]) / se_diff

        # logical OR: if this pair rejects, the whole simulation is marked True
        unadjusted_any |= np.abs(t_stat) > t_crit

    # --- Tukey HSD (Vectorized manual computation) ---
    # Calculate sum of squared errors (SSE) and Mean Squared Error (MSE)
    sse = np.sum((data - means[:, :, None]) ** 2, axis=(1, 2))
    mse = sse / (N_TOTAL - K_GROUPS)

    # Critical q-value from Studentized Range distribution
    q_crit = float(
        stats.studentized_range.ppf(1.0 - ALPHA, K_GROUPS, N_TOTAL - K_GROUPS)
    )
    # The Honestly Significant Difference (HSD) threshold
    hsd = q_crit * np.sqrt(mse / N_PER_GROUP)

    # Boolean array for Tukey rejections
    tukey_any = np.zeros(N_SIMULATIONS, dtype=bool)
    for i, j in pairs:
        # Reject if absolute difference exceeds HSD threshold
        tukey_any |= np.abs(means[:, i] - means[:, j]) > hsd

    # Generate labels for a single example run
    labels = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    # Run statsmodels Tukey HSD on the very first simulation (data[0])
    example = pairwise_tukeyhsd(data[0].ravel(), labels, alpha=ALPHA)

    return pd.DataFrame(
        {
            "unadjusted_any_reject": unadjusted_any,
            "tukey_any_reject": tukey_any,
        }
    ), example
# ------------------------------------------------------------------------------


# --- NEW (2) familywise_rates() ----------------------------------------------
def familywise_rates(results: pd.DataFrame) -> dict[str, float]:
    """
    Estimate familywise error rates from the null simulations.

    Parameters
    ----------
    results : pd.DataFrame
        Boolean columns indicating whether a Type I error occurred in each sim.

    Returns
    -------
    dict[str, float]
        Dictionary with the calculated error rates.

    Notes
    -----
    The mean of a boolean array gives the proportion of True values.
    """
    return {
        "unadjusted_fwer": float(results["unadjusted_any_reject"].mean()),
        "tukey_fwer": float(results["tukey_any_reject"].mean()),
        "n_simulations": float(N_SIMULATIONS),
        "target_alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(rates: dict[str, float]) -> Path:
    """
    Compare empirical familywise error with the advertised alpha.

    Parameters
    ----------
    rates : dict[str, float]
        The dictionary returned by familywise_rates().

    Returns
    -------
    Path
        Absolute path to the saved bar chart.

    Notes
    -----
    This plot visually proves that unadjusted tests far exceed the 0.05 limit,
    while Tukey holds the line.
    """
    output_path = DIR_FIGURES / "tukey_hsd_03_familywise_error.png"

    labels = ["Unadjusted\npairwise t", "Tukey HSD", "Advertised\nalpha"]
    values = [
        rates["unadjusted_fwer"],
        rates["tukey_fwer"],
        rates["target_alpha"],
    ]
    colors = ["#EC2661", "#1A2E51", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot bars
    bars = ax.bar(labels, values, color=colors, width=0.62)
    # Draw reference line at the target 0.05 alpha level
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.2)

    ax.set_ylabel("Familywise error rate")
    ax.set_title("Unadjusted Pairwise Tests Inflate Familywise Error")
    ax.set_ylim(0, 0.22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate bars with their exact values
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.4f}",
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
    # 1. Run 5000 simulations under the global null hypothesis
    results, example = simulate_null_experiments()
    # 2. Compute the Familywise Error Rates
    rates = familywise_rates(results)
    # 3. Create a bar plot of the results
    figure_path = save_figure(rates)
    # Count how many rejections happened in the sample run
    example_rejects = int(np.sum(example.reject))

    print("================================================================")
    print("LESSON 45 - STEP 3: FAMILYWISE ERROR LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Simulated null experiments      : {int(rates['n_simulations'])}")
    print(f"True means under H0             : all equal to {NULL_MEAN:.1f}")
    print(f"Advertised alpha                : {rates['target_alpha']:.6f}")
    print(f"Unadjusted pairwise FWER        : {rates['unadjusted_fwer']:.6f}")
    print(f"Tukey HSD FWER                  : {rates['tukey_fwer']:.6f}")
    print(f"Example null Tukey rejections   : {example_rejects}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

