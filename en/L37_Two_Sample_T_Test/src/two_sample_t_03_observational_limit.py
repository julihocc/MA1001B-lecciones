"""
Lesson 37 - Step 3: Observational Groups Are Not a Randomized Experiment
========================================================================
THE RECIPE
Start from two_sample_t_02_welch_test.py, then introduce:
    1. experience_summaries()   a confounder that differs by shift
    2. association_check()      pick time versus experience inside groups
    3. save_figure()            scatter that blocks a causal reading

Context:
Welch can reject equal means. That is not evidence that the shift itself
caused the difference. Associates were not randomly assigned: Shift A is
more experienced, and experience tracks faster picks. This script emphasizes
that statistical significance does not imply causation, especially in the
presence of lurking variables (confounders) when using observational data.

How to read this file:
- `experience_summaries`: Quantifies the unassigned baseline differences
  between groups, exposing a confounding element.
- `association_check`: Validates how closely the confounder tracks the
  dependent variable inside the independent groups.
- `save_figure`: Visually confirms that the distribution gap might simply be
  an experience gap, rather than an inherent shift difference.

Run it:
    python two_sample_t_03_observational_limit.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 30
N_B = 32
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """
    Draw independent synthetic pick times and years of experience.

    Parameters
    ----------
    seed : int, optional
        Seed for the random number generator (default is SEED).

    Returns
    -------
    dict[str, np.ndarray]
        A dictionary containing the simulated pick times and experience
        levels for Shift A and Shift B as numpy arrays.
    """
    rng = np.random.default_rng(seed)
    return {
        "times_a": rng.normal(loc=48.0, scale=6.0, size=N_A),
        "times_b": rng.normal(loc=52.5, scale=7.5, size=N_B),
        # Notice the built-in disparity in experience metrics
        "experience_a": rng.normal(loc=4.5, scale=1.0, size=N_A),
        "experience_b": rng.normal(loc=2.0, scale=0.8, size=N_B),
    }


# --- NEW (1) experience_summaries() ------------------------------------------
def experience_summaries(exp_a: np.ndarray, exp_b: np.ndarray) -> dict[str, float]:
    """
    Summarize years of experience, which were not randomly assigned.

    Parameters
    ----------
    exp_a : np.ndarray
        Array containing experience values for Shift A.
    exp_b : np.ndarray
        Array containing experience values for Shift B.

    Returns
    -------
    dict[str, float]
        Dictionary of mean and standard deviation for the experience
        levels, tracking the underlying discrepancy.

    Notes
    -----
    When dealing with observational (non-experimental) data, examining the
    covariates is critical. If covariates differ wildly across groups, they
    may act as confounding variables.
    """
    return {
        "mean_exp_a": float(np.mean(exp_a)),
        "mean_exp_b": float(np.mean(exp_b)),
        "s_exp_a": float(np.std(exp_a, ddof=1)),
        "s_exp_b": float(np.std(exp_b, ddof=1)),
        # Calculates the discrepancy in baseline experience levels
        "exp_diff": float(np.mean(exp_a) - np.mean(exp_b)),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) association_check() ---------------------------------------------
def association_check(samples: dict[str, np.ndarray]) -> dict[str, float]:
    """
    Correlate pick time with experience inside each observational shift.

    Parameters
    ----------
    samples : dict[str, np.ndarray]
        The comprehensive dict of times and experience arrays.

    Returns
    -------
    dict[str, float]
        Dictionary of correlation coefficients and Welch test significance.

    Notes
    -----
    np.corrcoef returns the Pearson product-moment correlation coefficient
    matrix. Position [0, 1] captures the off-diagonal correlation value
    between the two independent arrays.
    """
    # r represents the correlation coefficient showing linear relationship
    r_a = float(np.corrcoef(samples["experience_a"], samples["times_a"])[0, 1])
    r_b = float(np.corrcoef(samples["experience_b"], samples["times_b"])[0, 1])

    # We still check for statistical difference via Welch's test
    welch = stats.ttest_ind(
        samples["times_a"], samples["times_b"], equal_var=False
    )

    return {
        "r_a": r_a,
        "r_b": r_b,
        "welch_p": float(welch.pvalue),
        # Randomized flag is manually set to 0.0 reflecting the observational reality
        "randomized": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(samples: dict[str, np.ndarray]) -> Path:
    """
    Scatter pick time against experience, colored by unassigned shift.

    Parameters
    ----------
    samples : dict[str, np.ndarray]
        The dictionary containing times and experiences.

    Returns
    -------
    Path
        The absolute filepath where the scatter plot was saved.

    Notes
    -----
    Plotting covariates on the X-axis helps visualize whether the outcome
    (Y-axis) difference is actually due to group membership or underlying
    covariate difference.
    """
    output_path = DIR_FIGURES / "two_sample_t_03_observational_limit.png"

    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot Shift A's experience against performance
    ax.scatter(
        samples["experience_a"],
        samples["times_a"],
        color="#5B8DEF",
        s=42,  # marker size
        label="Shift A",
        edgecolors="#1A2E51",
    )
    # Plot Shift B's experience against performance
    ax.scatter(
        samples["experience_b"],
        samples["times_b"],
        color="#EC2661",
        s=42,
        label="Shift B",
        edgecolors="#1A2E51",
    )

    # Emphasize that experience wasn't uniformly randomized
    ax.set_xlabel("Years of experience (not randomly assigned)")
    ax.set_ylabel("Pick time (minutes)")
    ax.set_title("A Significant Welch Test Is Not a Randomized Experiment")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Build data including the confounding variable
    samples = build_shift_samples()
    # Summarize the differences in the confounder
    exp = experience_summaries(samples["experience_a"], samples["experience_b"])
    # Check if the confounder is correlated with the outcome metric
    assoc = association_check(samples)
    # Map the differences visually
    figure_path = save_figure(samples)

    print("================================================================")
    print("LESSON 37 - STEP 3: OBSERVATIONAL LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Welch two-sided p-value         : {assoc['welch_p']:.6f}")
    print(f"Shift A mean experience (years) : {exp['mean_exp_a']:.6f}")
    print(f"Shift B mean experience (years) : {exp['mean_exp_b']:.6f}")
    print(f"Experience gap A minus B        : {exp['exp_diff']:.6f}")
    print(f"Corr(experience, time) Shift A  : {assoc['r_a']:.6f}")
    print(f"Corr(experience, time) Shift B  : {assoc['r_b']:.6f}")
    print("Random assignment of associates : no")
    print("Causal claim from Welch p-value : not justified")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

