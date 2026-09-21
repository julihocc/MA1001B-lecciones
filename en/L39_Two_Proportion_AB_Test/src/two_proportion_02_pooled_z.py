"""
Lesson 39 - Step 2: Pooled z Test for pA minus pB
=================================================
THE RECIPE
Start from two_proportion_01_sample_rates.py, then introduce:
    1. pooled_standard_error()  SE of phatA - phatB under H0: pA = pB
    2. two_proportion_z_test()  z statistic and two-sided p-value
    3. save_figure()            standard-normal tails for the A/B z

Context:
To determine if the observed difference between version A and B is statistically
significant, we calculate a z-statistic. Because our null hypothesis states that
the proportions are identical (pA = pB), we use the pooled proportion to calculate
the standard error of the difference. We then compare our z-statistic against
a standard normal distribution to obtain a p-value.

How to read this file:
Notice how `pooled_standard_error` uses `p_pool` from both samples, instead of
separate standard errors for each arm. Then, look at `two_proportion_z_test`,
which constructs the test statistic and finds the probability (p-value) of seeing
data this extreme under the null.

Run it:
    python two_proportion_02_pooled_z.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# Use the Agg backend to generate plots without a display server
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Constants ---
# Random seed (kept for consistency with other files)
SEED = 42

# Sample data re-declared (we do not import previous lesson scripts to keep them self-contained)
N_A = 400
X_A = 72
N_B = 410
X_B = 61

# Significance level for the test
ALPHA = 0.05

# Output directory for figures
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def sample_rates() -> dict[str, float]:
    """
    Return sample sizes, conversion counts, and sample proportions.

    Returns:
        dict[str, float]: Unchanged from the previous step.
    """
    return {
        "n_a": float(N_A),
        "x_a": float(X_A),
        "n_b": float(N_B),
        "x_b": float(X_B),
        "phat_a": X_A / N_A,
        "phat_b": X_B / N_B,
        "diff": X_A / N_A - X_B / N_B,
    }


# --- NEW (1) pooled_standard_error() -----------------------------------------
def pooled_standard_error(p_pool: float, n_a: int = N_A, n_b: int = N_B) -> float:
    """
    Standard error of phatA - phatB using the pooled proportion.

    Parameters:
        p_pool (float): The pooled sample proportion from both arms.
        n_a (int): Sample size for group A. Defaults to N_A.
        n_b (int): Sample size for group B. Defaults to N_B.

    Returns:
        float: The pooled standard error.

    Notes:
        Under H0: pA = pB, the variance of (phatA - phatB) is p_pool * (1 - p_pool) * (1/n_a + 1/n_b).
        The standard error is the square root of this variance.
    """
    return float(np.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_a + 1.0 / n_b)))
# ------------------------------------------------------------------------------


# --- NEW (2) two_proportion_z_test() -----------------------------------------
def two_proportion_z_test() -> dict[str, float]:
    """
    Two-sided z test of H0: pA = pB.

    Returns:
        dict[str, float]: A dictionary containing:
            - 'phat_a': Sample proportion for A.
            - 'phat_b': Sample proportion for B.
            - 'p_pool': Pooled proportion.
            - 'se': Pooled standard error.
            - 'z_stat': The computed z-statistic.
            - 'p_value': The two-sided p-value.
            - 'z_critical': The critical z-value for the given ALPHA.

    Notes:
        The z-statistic measures how many standard errors the observed difference
        is away from zero. We use stats.norm.sf (survival function) to get the
        right-tail probability, and multiply by 2 for a two-sided test.
    """
    # 1. Calculate sample proportions
    phat_a = X_A / N_A
    phat_b = X_B / N_B

    # 2. Calculate pooled proportion and standard error
    p_pool = (X_A + X_B) / (N_A + N_B)
    se = pooled_standard_error(p_pool)

    # 3. Calculate z-statistic
    z_stat = (phat_a - phat_b) / se

    # 4. Calculate two-sided p-value using the standard normal survival function
    p_value = float(2.0 * stats.norm.sf(np.abs(z_stat)))

    return {
        "phat_a": phat_a,
        "phat_b": phat_b,
        "p_pool": p_pool,
        "se": se,
        "z_stat": float(z_stat),
        "p_value": p_value,
        "z_critical": float(stats.norm.ppf(1.0 - ALPHA / 2.0)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(z_stat: float, z_critical: float) -> Path:
    """
    Shade both tails of N(0, 1) beyond the observed A/B z.

    Parameters:
        z_stat (float): The observed z-statistic from the experiment.
        z_critical (float): The critical z-value threshold for significance.

    Returns:
        Path: The absolute path where the figure was saved.

    Notes:
        This plot visually demonstrates the p-value as the shaded area in both tails
        of the standard normal distribution beyond our observed test statistic.
    """
    output_path = DIR_FIGURES / "two_proportion_02_pooled_z.png"

    # Create the x-axis for the standard normal distribution
    x = np.linspace(-3.6, 3.6, 600)
    # Calculate the PDF (Probability Density Function) values
    y = stats.norm.pdf(x)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)

    # Shade the rejection regions based on the observed z_stat
    ax.fill_between(x, y, where=(x <= -abs(z_stat)), color="#EC2661", alpha=0.45)
    ax.fill_between(x, y, where=(x >= abs(z_stat)), color="#EC2661", alpha=0.45)

    # Draw vertical lines for observed and critical values
    ax.axvline(z_stat, color="#EC2661", linewidth=1.6,
               label=f"observed z = {z_stat:.2f}")
    ax.axvline(z_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"z* = {z_critical:.2f}")
    ax.axvline(-z_critical, color="#646464", linestyle="--", linewidth=1.2)

    # Formatting
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.set_title("Two-Sided z Test for pA minus pB")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    # Save and close
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Run the test
    test = two_proportion_z_test()
    # Make a decision based on the p-value and our alpha threshold
    decision = "reject H0" if test["p_value"] < ALPHA else "do not reject H0"

    # Save the visualization
    figure_path = save_figure(test["z_stat"], test["z_critical"])

    # Output results identically to the unannotated version
    print("================================================================")
    print("LESSON 39 - STEP 2: POOLED z TEST")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print("Hypotheses                      : H0: pA = pB vs H1: pA != pB")
    print(f"Difference p-hat A minus B      : {test['phat_a'] - test['phat_b']:.6f}")
    print(f"Pooled proportion               : {test['p_pool']:.6f}")
    print(f"Pooled SE                       : {test['se']:.6f}")
    print(f"z statistic                     : {test['z_stat']:.6f}")
    print(f"Two-sided p-value               : {test['p_value']:.6f}")
    print(f"Critical z* (two-sided)         : {test['z_critical']:.6f}")
    print(f"Decision at alpha = 0.05        : {decision}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

