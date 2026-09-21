"""
Lesson 46 - Step 3: Equal n Does Not Rescue Strong Heteroscedasticity
=====================================================================

THE RECIPE
----------
Start from anova_diagnostics_02_levene_homoscedasticity.py, then introduce:
    1. build_heterogeneous()  equal n, strongly unequal variances
    2. broken_anova()         Levene plus F when the equal-spread assumption fails
    3. save_figure()          residual fan from the high-variance method

Context:
--------
What happens if the assumption of equal variances is severely violated?
This condition is called "heteroscedasticity." While having equal sample sizes
(n) in all groups makes ANOVA somewhat robust to minor variance differences,
it cannot save you if the differences are extreme.

Limit: equal-n ANOVA is not immune to strong variance inequality. A
significant F can still appear when one group is far noisier than the others,
so the mean comparison is no longer a clean ANOVA story.

How to read this file:
----------------------
1. `build_heterogeneous`: We purposely simulate data where one group ("Automated")
   has a massive standard deviation (12.0) compared to the others (~1.7).
2. `broken_anova`: Runs both Levene's test (which will now flag a failure) and
   the standard ANOVA F-test, highlighting the problem.
3. `save_figure`: Visualizes the failure via a boxplot and a residual plot showing
   a "fan" shape—a classic sign of heteroscedasticity.

Run it:
-------
    uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_03_variance_inequality_limit.py
"""

# Import path handling
from pathlib import Path

# matplotlib for plotting without opening an interactive window
import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PER_GROUP = 12
TREATMENTS = ("Standard", "Guided", "Automated")
# We set two means equal, and one significantly different
HETERO_MEANS = {"Standard": 50.0, "Guided": 50.0, "Automated": 56.0}
# Here is the trick: "Automated" has a severely large sigma (spread)
HETERO_SIGMAS = {"Standard": 1.6, "Guided": 1.8, "Automated": 12.0}
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) build_heterogeneous() -------------------------------------------
def build_heterogeneous(seed: int = SEED) -> pd.DataFrame:
    """
    Build three equal-n samples with a strongly noisier Automated group.

    Parameters
    ----------
    seed : int, optional
        The random generator seed for reproducibility. Defaults to SEED.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the generated cycle times and their corresponding
        fitted means and residuals.

    Notes
    -----
    This directly injects a large standard deviation into the "Automated" group
    during synthetic data creation, breaking the homoscedasticity assumption.
    """
    rng = np.random.default_rng(seed)
    frames = []

    # Generate data using the specific sigma for each group
    for name in TREATMENTS:
        cycle_time = rng.normal(
            HETERO_MEANS[name], HETERO_SIGMAS[name], N_PER_GROUP
        )
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )

    sample = pd.concat(frames, ignore_index=True)

    # Calculate means and residuals inline
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    sample["fitted"] = fitted
    sample["residual"] = sample["cycle_time_seconds"] - fitted
    return sample
# ------------------------------------------------------------------------------


# --- NEW (2) broken_anova() --------------------------------------------------
def broken_anova(sample: pd.DataFrame) -> dict[str, float]:
    """
    Compute Levene and F when variances are strongly unequal.

    Parameters
    ----------
    sample : pd.DataFrame
        The data containing cycle times for the three treatment methods.

    Returns
    -------
    dict[str, float]
        Dictionary of computed statistics, including standard deviations, means,
        Levene's test results, and standard ANOVA F-test results.

    Notes
    -----
    Because variances are radically different, the ANOVA F-test results are
    unreliable even if it reports a small p-value. The Levene test will correctly
    report a tiny p-value, alerting us that the assumption is broken.
    """
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]

    # Levene test checks if variances are equal (null hypothesis)
    levene_stat, levene_p = stats.levene(*groups)

    # One-way ANOVA checks if means are equal (null hypothesis)
    f_stat, f_p = stats.f_oneway(*groups)

    # Calculate group standard deviations to observe the severity of the violation
    sds = [float(np.std(group, ddof=1)) for group in groups]

    return {
        "sd_standard": sds[0],
        "sd_guided": sds[1],
        "sd_automated": sds[2],
        "mean_standard": float(groups[0].mean()),
        "mean_guided": float(groups[1].mean()),
        "mean_automated": float(groups[2].mean()),
        "levene_stat": float(levene_stat),
        "levene_p": float(levene_p),
        "f_stat": float(f_stat),
        "f_p": float(f_p),
        "n_per_group": float(N_PER_GROUP),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: pd.DataFrame) -> Path:
    """
    Show the residual fan created by one high-variance method.

    Parameters
    ----------
    sample : pd.DataFrame
        The data with extreme variance differences between groups.

    Returns
    -------
    Path
        Absolute path to the saved PNG figure.

    Notes
    -----
    Creates a side-by-side plot:
    1. A boxplot to easily see the huge variance difference visually.
    2. A residuals plot to see the characteristic "fan" or "funnel" shape
       caused by heteroscedasticity.
    """
    output_path = (
        DIR_FIGURES / "anova_diagnostics_03_variance_inequality_limit.png"
    )
    colors = {"Standard": "#1A2E51", "Guided": "#5B8DEF", "Automated": "#EC2661"}

    # Create a 1x2 grid of plots
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]

    # Left Plot: Boxplot showing raw distributions
    boxes = axes[0].boxplot(
        groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )
    for patch, name in zip(boxes["boxes"], TREATMENTS):
        patch.set_facecolor(colors[name])
        patch.set_alpha(0.45)
    axes[0].set_xticks([1, 2, 3])
    axes[0].set_xticklabels(TREATMENTS)
    axes[0].set_ylabel("Cycle time (seconds)")
    axes[0].set_title("Equal n, Unequal Spread")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    # Right Plot: Residuals vs. Fitted showing the 'Fan' shape
    for name in TREATMENTS:
        block = sample.loc[sample["method"] == name]
        axes[1].scatter(
            block["fitted"],
            block["residual"],
            color=colors[name],
            s=42,
            alpha=0.9,
            label=name,
        )
    axes[1].axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)
    axes[1].set_xlabel("Fitted group mean (seconds)")
    axes[1].set_ylabel("Residual (seconds)")
    axes[1].set_title("Residual Fan: ANOVA Assumption Broken")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # 1. Create the heavily skewed data
    sample = build_heterogeneous()

    # 2. Run Levene's and the broken ANOVA
    results = broken_anova(sample)

    # 3. Save visualizations of the failure
    figure_path = save_figure(sample)

    print("================================================================")
    print("LESSON 46 - STEP 3: VARIANCE INEQUALITY LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"n per method                    : {int(results['n_per_group'])}")
    print(f"Mean Standard                   : {results['mean_standard']:.6f}")
    print(f"Mean Guided                     : {results['mean_guided']:.6f}")
    print(f"Mean Automated                  : {results['mean_automated']:.6f}")
    print(f"SD Standard                     : {results['sd_standard']:.6f}")
    print(f"SD Guided                       : {results['sd_guided']:.6f}")
    print(f"SD Automated                    : {results['sd_automated']:.6f}")
    print(f"Levene statistic                : {results['levene_stat']:.6f}")
    print(f"Levene p-value                  : {results['levene_p']:.6e}")
    print(f"ANOVA F                         : {results['f_stat']:.6f}")
    print(f"ANOVA p-value                   : {results['f_p']:.6e}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

