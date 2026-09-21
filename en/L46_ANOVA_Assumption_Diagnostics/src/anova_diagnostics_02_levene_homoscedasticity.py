"""
Lesson 46 - Step 2: Equal Variances and Residual versus Fitted
==============================================================

THE RECIPE
----------
Start from anova_diagnostics_01_residual_normality.py, then introduce:
    1. levene_test()        scipy.stats.levene for the three methods
    2. residual_vs_fitted() group standard deviations and fitted values
    3. save_figure()        residual versus fitted scatter

Context:
--------
ANOVA also assumes that the variance (spread) of data in each group is
roughly equal. This is known as "homoscedasticity" or equal variances.
If one group's data is much more spread out than the others, ANOVA can
produce misleading results.

The same 36 cycle times are rebuilt from seed 42. No earlier lesson script is
imported. Homoscedasticity means the within-method spreads are comparable;
independence is a design claim, not a plot statistic.

How to read this file:
----------------------
1. `build_cycle_times` and `anova_residuals`: Same as Step 1.
2. `levene_test`: A statistical test specifically designed to check if variances
   are equal across multiple groups.
3. `residual_vs_fitted`: Calculates the standard deviation of each group to
   see the spread mathematically.
4. `save_figure`: Plots a scatter plot of residuals vs. fitted means. A random
   scatter with roughly equal vertical spread indicates equal variances.

Run it:
-------
    uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_02_levene_homoscedasticity.py
"""

# Path manipulation for output directories
from pathlib import Path

# matplotlib for plotting; backend set to "Agg" for background saving
import matplotlib
import numpy as np
import pandas as pd
# stats module provides Levene's test for equal variances
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Consistent seed ensures we look at the exact same data as Step 1
SEED = 42
N_PER_GROUP = 12
TREATMENTS = ("Standard", "Guided", "Automated")
TRUE_MEANS = {"Standard": 50.0, "Guided": 48.0, "Automated": 43.0}
SIGMA = 3.2
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """
    Rebuild the three synthetic cycle-time samples from seed 42.

    Parameters
    ----------
    seed : int, optional
        The random seed. Defaults to SEED.

    Returns
    -------
    pd.DataFrame
        DataFrame with "method" and "cycle_time_seconds" columns.
    """
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)


def anova_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Form residuals and fitted group means.

    Parameters
    ----------
    sample : pd.DataFrame
        Input data containing the categorical method and numeric cycle time.

    Returns
    -------
    pd.DataFrame
        DataFrame updated with "fitted" (group means) and "residual" values.
    """
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    out = sample.copy()
    out["fitted"] = fitted
    out["residual"] = out["cycle_time_seconds"] - fitted
    return out


# --- NEW (1) levene_test() ---------------------------------------------------
def levene_test(sample: pd.DataFrame) -> dict[str, float]:
    """
    Test equal variances of cycle time across packing methods.

    Parameters
    ----------
    sample : pd.DataFrame
        The complete dataset with "method" and "cycle_time_seconds".

    Returns
    -------
    dict[str, float]
        A dictionary containing the Levene test statistic and the p-value.

    Notes
    -----
    Levene's test checks the null hypothesis that all input samples are from
    populations with equal variances. A p-value > 0.05 indicates we do not
    reject this assumption.
    """
    # Extract data arrays for each treatment group separately
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]

    # Unpack the list of arrays directly into the stats.levene function
    statistic, p_value = stats.levene(*groups)
    return {"levene_stat": float(statistic), "levene_p": float(p_value)}
# ------------------------------------------------------------------------------


# --- NEW (2) residual_vs_fitted() --------------------------------------------
def residual_vs_fitted(diagnosed: pd.DataFrame) -> dict[str, float]:
    """
    Report group standard deviations used in the equal-variance check.

    Parameters
    ----------
    diagnosed : pd.DataFrame
        The DataFrame with group assignment and calculated residuals/fitted values.

    Returns
    -------
    dict[str, float]
        Dictionary with standard deviation computed for each group, plus the
        overall mean of all residuals (which should be extremely close to 0).
    """
    out: dict[str, float] = {}
    for name in TREATMENTS:
        values = diagnosed.loc[
            diagnosed["method"] == name, "cycle_time_seconds"
        ]
        # ddof=1 means we use sample standard deviation (N-1 degrees of freedom)
        out[f"sd_{name.lower()}"] = float(values.std(ddof=1))

    out["residual_mean"] = float(diagnosed["residual"].mean())
    return out
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(diagnosed: pd.DataFrame) -> Path:
    """
    Save residual versus fitted values for the balanced experiment.

    Parameters
    ----------
    diagnosed : pd.DataFrame
        DataFrame including "method", "fitted", and "residual" columns.

    Returns
    -------
    Path
        Absolute path to the saved PNG image.

    Notes
    -----
    A residual vs. fitted plot displays the predicted group means on the x-axis
    and the residuals on the y-axis. If the equal variances assumption holds,
    the vertical spread of points should be similar across all x-axis clusters.
    """
    output_path = DIR_FIGURES / "anova_diagnostics_02_levene_homoscedasticity.png"
    # Specific colors for different categorical methods
    colors = {"Standard": "#1A2E51", "Guided": "#5B8DEF", "Automated": "#EC2661"}

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot each group separately to assign it a distinct color and legend label
    for name in TREATMENTS:
        block = diagnosed.loc[diagnosed["method"] == name]
        ax.scatter(
            block["fitted"],
            block["residual"],
            color=colors[name],
            s=42,       # dot size
            alpha=0.9,  # transparency
            label=name,
        )

    # Draw a dashed reference line at residual = 0
    ax.axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)

    # Configure axes and title
    ax.set_xlabel("Fitted group mean (seconds)")
    ax.set_ylabel("Residual (seconds)")
    ax.set_title("Residuals versus Fitted: Comparable Spread")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Rebuild the sample and find residuals
    sample = build_cycle_times()
    diagnosed = anova_residuals(sample)

    # 2. Run Levene's test for equal variances
    levene = levene_test(sample)

    # 3. Calculate standard deviations for each group
    spreads = residual_vs_fitted(diagnosed)

    # 4. Generate the diagnostic plot
    figure_path = save_figure(diagnosed)

    print("================================================================")
    print("LESSON 46 - STEP 2: LEVENE AND EQUAL SPREAD")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"SD Standard                     : {spreads['sd_standard']:.6f}")
    print(f"SD Guided                       : {spreads['sd_guided']:.6f}")
    print(f"SD Automated                    : {spreads['sd_automated']:.6f}")
    print(f"Levene statistic                : {levene['levene_stat']:.6f}")
    print(f"Levene p-value                  : {levene['levene_p']:.6f}")
    print("Independence                    : design assumption, not a plot")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

