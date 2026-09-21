"""
Lesson 39 - Step 3: Peeking at p-Values Inflates Type I Error
=============================================================
THE RECIPE
Start from two_proportion_02_pooled_z.py, then introduce:
    1. two_proportion_pvalue()  z p-value from interim counts
    2. simulate_peeking()       seed-42 type I rate with four looks
    3. save_figure()            one planned test versus peeking

Context:
In industry A/B testing, it's tempting to check the dashboard repeatedly and
stop the experiment as soon as p < 0.05. This is called "peeking." Under H0
(no true difference), this practice artificially inflates the Type I error
(false-positive rate) well beyond the nominal alpha of 0.05.

How to read this file:
First, review `two_proportion_pvalue` to see a simplified version of our earlier
test logic adapted for incremental counts. Then, study `simulate_peeking`,
which runs thousands of simulated A/B tests. It compares what happens if we
only look at the end versus if we look at 25%, 50%, 75%, and 100% marks,
stopping early if we ever cross the threshold.

Run it:
    python two_proportion_03_peeking_limit.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

# Configure matplotlib for headless generation
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Constants ---
SEED = 42
N_A = 400
N_B = 410

# The true probability of conversion for both groups in our simulation (H0 is true)
P_NULL = 0.16

# Number of simulated experiments to run
N_SIM = 8000

# We will "peek" at the results after 25%, 50%, 75%, and 100% of traffic
LOOK_FRACTIONS = (0.25, 0.50, 0.75, 1.00)

# The significance level we are targeting
ALPHA = 0.05

# Output directory
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) two_proportion_pvalue() -----------------------------------------
def two_proportion_pvalue(x_a: int, n_a: int, x_b: int, n_b: int) -> float:
    """
    Two-sided pooled-z p-value from interim conversion counts.

    Parameters:
        x_a (int): Current conversions in A.
        n_a (int): Current sample size in A.
        x_b (int): Current conversions in B.
        n_b (int): Current sample size in B.

    Returns:
        float: The two-sided p-value.

    Notes:
        This is a lightweight version of the previous test function,
        designed to be called rapidly during simulations. We handle edge
        cases (like n=0 or zero standard error) gracefully.
    """
    # Prevent division by zero if an arm has no samples yet
    if n_a <= 0 or n_b <= 0:
        return 1.0

    # Calculate pooled proportion
    p_pool = (x_a + x_b) / (n_a + n_b)

    # Calculate standard error
    se = np.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_a + 1.0 / n_b))
    if se == 0.0:
        return 1.0

    # Calculate z-statistic and return the p-value
    z_stat = (x_a / n_a - x_b / n_b) / se
    return float(2.0 * stats.norm.sf(np.abs(z_stat)))
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_peeking() ----------------------------------------------
def simulate_peeking(seed: int = SEED) -> dict[str, float]:
    """
    Estimate type I error with one final test versus four peeks.

    Parameters:
        seed (int): Random seed for reproducibility. Defaults to SEED.

    Returns:
        dict[str, float]: A dictionary containing:
            - 'n_sim': Number of simulation runs.
            - 'n_looks': Number of peeks per experiment.
            - 'type_i_once': False positive rate if tested only at the end.
            - 'type_i_peek': False positive rate if testing repeatedly.
            - 'alpha': The nominal significance level.

    Notes:
        The simulation generates Binomial random variables for each visitor,
        assuming H0 is true (both arms have success probability P_NULL).
    """
    # Initialize the random number generator
    rng = np.random.default_rng(seed)

    # Track how often we incorrectly reject H0
    reject_once = 0
    reject_peek = 0

    for _ in range(N_SIM):
        # Generate the full timeline of conversions for both arms
        arm_a = rng.binomial(1, P_NULL, N_A)
        arm_b = rng.binomial(1, P_NULL, N_B)

        peeked = False

        # Check the data at each fraction of the total experiment
        for fraction in LOOK_FRACTIONS:
            # Determine the current sample size for this interim look
            n_a = int(N_A * fraction)
            n_b = int(N_B * fraction)

            # Calculate the p-value using data up to this point
            p_value = two_proportion_pvalue(
                int(arm_a[:n_a].sum()), n_a, int(arm_b[:n_b].sum()), n_b
            )

            # Record the decision for the "one final test" strategy
            if fraction == 1.0 and p_value < ALPHA:
                reject_once += 1

            # If ANY peek results in significance, we record a "peeked" rejection
            if p_value < ALPHA:
                peeked = True

        # If we crossed the threshold at any point, we falsely rejected H0
        if peeked:
            reject_peek += 1

    return {
        "n_sim": float(N_SIM),
        "n_looks": float(len(LOOK_FRACTIONS)),
        "type_i_once": reject_once / N_SIM,
        "type_i_peek": reject_peek / N_SIM,
        "alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(results: dict[str, float]) -> Path:
    """
    Compare the planned type I rate with the peeked type I rate in a plot.

    Parameters:
        results (dict[str, float]): The results dictionary from simulate_peeking().

    Returns:
        Path: The absolute path where the figure was saved.

    Notes:
        This visualizes how continuous monitoring without statistical correction
        dramatically inflates false positives.
    """
    output_path = DIR_FIGURES / "two_proportion_03_peeking_limit.png"

    # Prepare data
    labels = ["One test at nA, nB", "Four peeks, stop if p < 0.05"]
    values = [results["type_i_once"], results["type_i_peek"]]

    # Set up plot
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=["#1A2E51", "#EC2661"], width=0.55)

    # Draw a line indicating the nominal alpha
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.4,
               label="nominal alpha = 0.05")

    # Configure labels and bounds
    ax.set_ylabel("False-positive rate under H0")
    ax.set_title("Peeking Inflates Type I Error")
    ax.set_ylim(0, 0.18)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Annotate the bars with their exact rates
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.005,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Run the simulation
    results = simulate_peeking()
    figure_path = save_figure(results)

    # Output results identically to the unannotated version
    print("================================================================")
    print("LESSON 39 - STEP 3: PEEKING LIMIT")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Simulated experiments           : {int(results['n_sim'])}")
    print(f"Null conversion probability     : {P_NULL:.2f}")
    print(f"Looks per experiment            : {int(results['n_looks'])}")
    print(f"Type I rate, one final test     : {results['type_i_once']:.6f}")
    print(f"Type I rate with peeking        : {results['type_i_peek']:.6f}")
    print(f"Nominal alpha                   : {results['alpha']:.2f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

