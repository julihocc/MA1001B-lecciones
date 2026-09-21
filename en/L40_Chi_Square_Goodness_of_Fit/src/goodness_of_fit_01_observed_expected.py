"""
Lesson 40 - Step 1: Observed Counts versus Hypothesized Shares
==============================================================
NEW IN THIS STEP: hypothesized_shares(), expected_counts(), and save_figure().

THE RECIPE
----------
1. Define the categories and their hypothesized shares (probabilities).
2. Record the observed counts for each category from the sample.
3. Calculate the expected counts by multiplying the total sample size (n) by the hypothesized shares (p).
4. Verify that all expected counts are at least 5 to satisfy the condition for the Chi-Square test.
5. Visualize the differences between observed and expected counts.

Context:
A fully synthetic support desk claims that incoming tickets follow the mix
40 percent phone, 30 percent chat, 20 percent email, and 10 percent app.
A sample of n = 200 tickets is counted. Expected counts are n times the
hypothesized shares.

How to read this file:
- For a student who knows Python OOP, think of `hypothesized_shares()` and `expected_counts()` as methods that extract properties of our statistical model.
- The expected counts are the theoretical frequencies we would see if the null hypothesis (the claimed ticket mix) were perfectly true.
- The differences between the `observed` counts (the real data) and the `expected` counts (the theoretical model) form the basis of the Chi-Square Goodness-of-Fit test.

Run it:
    uv run goodness_of_fit_01_observed_expected.py
"""

from pathlib import Path

# Use the Agg backend for matplotlib, so it generates figures without needing an active display server.
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# SEED: Fixed seed for reproducibility, though not strictly used in this deterministic step.
SEED = 42
# N: Total sample size (number of tickets observed)
N = 200
# CATEGORIES: The different types of tickets
CATEGORIES = ("Phone", "Chat", "Email", "App")
# HYPOTHESIZED: The claimed shares (probabilities) under the null hypothesis (H0)
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
# OBSERVED: The actual ticket counts observed in the sample
OBSERVED = np.array([100, 50, 30, 20], dtype=float)

# DIR_FIGURES: Path object pointing to the sibling 'figures' directory where plots are saved.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
# Ensure the directory exists before attempting to save files into it.
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) hypothesized_shares() -------------------------------------------
def hypothesized_shares() -> dict[str, np.ndarray | float]:
    """
    Return the claimed ticket-mix probabilities.

    Parameters
    ----------
    None

    Returns
    -------
    dict[str, np.ndarray | float]
        A dictionary containing:
        - "categories": An array of the ticket categories.
        - "p": The array of hypothesized probabilities (shares).
        - "n": The total sample size as a float.

    Notes
    -----
    These shares represent the null hypothesis (H0). If H0 is true, the true
    population proportions match these exact probabilities.
    """
    return {
        "categories": np.array(CATEGORIES),
        "p": HYPOTHESIZED.copy(),
        "n": float(N),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) expected_counts() -----------------------------------------------
def expected_counts(n: int = N, p: np.ndarray = HYPOTHESIZED) -> dict[str, np.ndarray | float]:
    """
    Convert hypothesized shares into expected counts E = n p.

    Parameters
    ----------
    n : int, optional
        The total number of observations in the sample (default is N=200).
    p : np.ndarray, optional
        The hypothesized proportions for each category (default is HYPOTHESIZED).

    Returns
    -------
    dict[str, np.ndarray | float]
        A dictionary containing:
        - "observed": A copy of the OBSERVED counts array.
        - "expected": The computed expected counts array.
        - "min_expected": The minimum expected count value.
        - "all_expected_ge_5": A float (1.0 or 0.0) indicating if all expected counts >= 5.

    Notes
    -----
    The expected count for a category is calculated as E = n * p.
    For the Chi-Square approximation to be valid, a common rule of thumb is
    that all expected counts should be at least 5.
    """
    # Calculate the expected counts E_i = n * p_i
    expected = n * p
    return {
        "observed": OBSERVED.copy(),
        "expected": expected,
        "min_expected": float(np.min(expected)),
        "all_expected_ge_5": float(np.all(expected >= 5.0)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(observed: np.ndarray, expected: np.ndarray) -> Path:
    """
    Compare observed ticket counts with expected counts under H0.

    Parameters
    ----------
    observed : np.ndarray
        The actual counts observed in the sample data.
    expected : np.ndarray
        The theoretical counts expected if the null hypothesis is true.

    Returns
    -------
    Path
        The absolute path to the saved PNG figure.

    Notes
    -----
    This side-by-side bar chart visually contrasts the real data against the
    model. Large discrepancies suggest the null hypothesis may be false.
    """
    # Define the output file path for the generated figure
    output_path = DIR_FIGURES / "goodness_of_fit_01_observed_expected.png"

    # Generate x positions for the grouped bars
    x = np.arange(len(CATEGORIES))
    width = 0.36

    # Initialize the matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(8.4, 4.6))

    # Plot the observed counts (shifted slightly left)
    ax.bar(x - width / 2, observed, width, color="#EC2661", label="Observed")
    # Plot the expected counts (shifted slightly right)
    ax.bar(x + width / 2, expected, width, color="#1A2E51", label="Expected under H0")

    # Format the axes and labels
    ax.set_xticks(x, CATEGORIES)
    ax.set_ylabel("Ticket count")
    ax.set_title("n = 200 Tickets versus Hypothesized Mix")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Optimize layout and save the figure to disk
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)

    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    # Fetch the claimed proportions and sample size
    shares = hypothesized_shares()
    # Compute the expected counts and check validity conditions
    counts = expected_counts()
    # Generate the visual comparison
    figure_path = save_figure(counts["observed"], counts["expected"])

    # Output the required console log format exactly
    print("================================================================")
    print("LESSON 40 - STEP 1: OBSERVED VERSUS EXPECTED")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Sample size n                   : {int(shares['n'])}")
    print("Hypothesized shares             : 0.40, 0.30, 0.20, 0.10")
    print("Observed counts                 : 100, 50, 30, 20")
    print(
        "Expected counts                 : "
        + ", ".join(f"{value:.1f}" for value in counts["expected"])
    )
    print(f"Minimum expected count          : {counts['min_expected']:.6f}")
    print(
        "All expected counts >= 5        : "
        f"{'yes' if counts['all_expected_ge_5'] else 'no'}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

