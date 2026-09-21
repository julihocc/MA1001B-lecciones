"""
Lesson 05 - Step 1: Outcomes and the Sample Space
=================================================
NEW IN THIS STEP: build_sample_space(), simulate_dispatches(), and
build_frequency_figure().

The Recipe
    1. build_sample_space()   enumerates possibilities without frequencies
    2. simulate_dispatches()  produces observations with unequal probabilities
    3. build_frequency_figure() contrasts possibilities with frequencies

List every possible outcome of one synthetic dispatch experiment, simulate a
seeded collection of dispatch records, and verify which possible outcomes
appear. Possible does not mean equally likely.

Run it:
    uv run en/L05_Set_Theory_Sample_Space/src/set_theory_01_sample_space.py
"""

from itertools import product
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Agg saves figures without opening windows; choose it before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# One outcome keeps the order (shift, service, status). These aliases make
# contracts readable without introducing a class for three categorical fields.
Outcome = tuple[str, str, str]
SampleSpace = tuple[Outcome, ...]

SEED = 42
OBSERVATION_COUNT = 480
SHIFTS = ("Day", "Night")
SERVICES = ("Standard", "Express")
STATUSES = ("On time", "Delayed")

# Parameters of the synthetic example; they are not company estimates.
# Each probability corresponds to the category at the same position.
SHIFT_PROBABILITIES = (0.65, 0.35)
SERVICE_PROBABILITIES = (0.70, 0.30)
BASE_DELAY_PROBABILITY = 0.10
NIGHT_DELAY_INCREMENT = 0.08
EXPRESS_DELAY_INCREMENT = 0.12

# Resolve from this file so execution works from any current directory.
# The directory is created only when a figure is saved.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"


# --- NEW (1) build_sample_space() --------------------------------------------
def build_sample_space() -> SampleSpace:
    """Enumerate possible outcomes independently of observations.

    Returns
    -------
    tuple[tuple[str, str, str], ...]
        Eight ordered outcomes (shift, service, status). The model admits every
        combination: 2 x 2 x 2 = 8. This describes possibilities, not their
        probabilities or the number of dispatches.
    """
    # product is equivalent to three nested loops; status changes fastest.
    # tuple materializes the iterator so tables and figures keep one stable
    # order. Each inner tuple can be used as a set member.
    return tuple(product(SHIFTS, SERVICES, STATUSES))


# --- NEW (2) simulate_dispatches() -------------------------------------------
def simulate_dispatches(seed: int = SEED) -> pd.DataFrame:
    """Generate 480 synthetic dispatches without reading or writing files.

    Parameters
    ----------
    seed : int
        Non-negative integer for NumPy's local generator. The same seed,
        parameters, and environment rebuild the same rows in the same order.

    Returns
    -------
    pandas.DataFrame
        Columns dispatch_id, shift, service, status, and outcome. Each row is
        an observation; outcome is its (shift, service, status) tuple.
        Identifiers distinguish rows but do not add possibilities to S.

    Assumptions
    -----------
    Shift and service are independently sampled in this model. Delay depends
    on both. These parameters are didactic choices that create unequal
    frequencies, not conclusions about real operations.

    Raises
    ------
    ValueError
        NumPy rejects a negative seed. The constructed delay probabilities
        must remain in the interval [0, 1].
    """
    # The generator lives inside the function: other code cannot consume its
    # sequence before the simulation. It is not restarted between draws.
    rng = np.random.default_rng(seed)

    # Each array has one entry per dispatch. p follows category order; 0.35 is
    # a probability, not an exact quota of 35 percent of the rows.
    shifts = rng.choice(
        SHIFTS, size=OBSERVATION_COUNT, p=SHIFT_PROBABILITIES
    )
    services = rng.choice(
        SERVICES, size=OBSERVATION_COUNT, p=SERVICE_PROBABILITIES
    )

    # Comparisons produce arrays aligned by dispatch. True contributes 1 and
    # False contributes 0: the four rates are 0.10, 0.18, 0.22, and 0.30.
    delay_probability = (
        BASE_DELAY_PROBABILITY
        + NIGHT_DELAY_INCREMENT * (shifts == "Night")
        + EXPRESS_DELAY_INCREMENT * (services == "Express")
    )
    if np.any((delay_probability < 0) | (delay_probability > 1)):
        raise ValueError("Each delay probability must be between 0 and 1.")

    # For U uniform on [0, 1), P(U < p) = p. np.where turns each decision
    # into its categorical label.
    uniform_draws = rng.random(OBSERVATION_COUNT)
    statuses = np.where(
        uniform_draws < delay_probability, "Delayed", "On time"
    )

    # Columns share positions: row i joins the ith draws. The starting ID only
    # labels rows; it is not part of the mathematical outcome.
    dispatches = pd.DataFrame(
        {
            "dispatch_id": np.arange(500_001, 500_001 + OBSERVATION_COUNT),
            "shift": shifts,
            "service": services,
            "status": statuses,
        }
    )
    # zip groups the three categories by row; list materializes tuples for
    # pandas. Repeating an outcome increases its frequency, not |S|.
    dispatches["outcome"] = list(zip(shifts, services, statuses))
    return dispatches


def save_figure(figure: plt.Figure, path: Path) -> Path:
    """Save a figure as PNG and release its resources, even if saving fails.

    The caller constructs the figure and supplies its destination. This
    function creates only the required directory; write errors propagate
    rather than reporting a save that did not happen.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, dpi=170)
    finally:
        # Closing prevents hidden figures from accumulating across runs.
        plt.close(figure)
    return path


def outcome_label(outcome: Outcome) -> str:
    """Convert one outcome tuple to readable text for a figure or table.

    Formatting is a presentation concern; the underlying tuple remains the
    hashable mathematical object used by the set operations.
    """
    return " | ".join(outcome)


# --- NEW (3) build_frequency_figure() ----------------------------------------
def build_frequency_figure(
    sample_space: SampleSpace,
    dispatches: pd.DataFrame,
) -> plt.Figure:
    """Represent the frequency of every possible outcome, including zeros.

    The function receives the ordered S and a DataFrame with an outcome column.
    It returns a Figure without changing inputs or writing files; the caller
    decides whether to display, save, or close it. Bars count dispatches, not
    probabilities.
    """
    # value_counts counts repeated observed tuples. Iterating through S keeps
    # possibilities that were absent; get(..., 0) gives them a zero frequency.
    counts = dispatches["outcome"].value_counts()
    frequencies = pd.DataFrame(
        {
            "outcome": [outcome_label(item) for item in sample_space],
            "frequency": [int(counts.get(item, 0)) for item in sample_space],
        }
    )

    # Seaborn receives semantic columns and places the bars and labels. The
    # data already contain one count per row, so sum represents it directly;
    # errorbar=None avoids inferential intervals that this example did not fit.
    figure, axis = plt.subplots(figsize=(10.2, 5.2), layout="constrained")
    sns.barplot(
        data=frequencies,
        x="frequency",
        y="outcome",
        order=frequencies["outcome"].tolist(),
        estimator="sum",
        errorbar=None,
        color="#EC2661",
        ax=axis,
    )
    axis.set(
        title="Possible Outcomes and Observed Frequencies",
        xlabel="Observed synthetic dispatches",
        ylabel="",
    )
    # bar_label resolves bar coordinates, including zero-valued bars.
    axis.bar_label(axis.containers[0], fmt="%.0f", padding=3)
    axis.margins(x=0.18)
    return figure


def main() -> None:
    """Coordinate calculation, visualization, saving, and reporting."""
    sample_space = build_sample_space()
    dispatches = simulate_dispatches()
    figure = build_frequency_figure(sample_space, dispatches)
    figure_path = save_figure(
        figure, DIR_FIGURES / "set_theory_01_sample_space.png"
    )

    observed_outcomes = set(dispatches["outcome"])
    # Calculate the aggregation once and reuse it in the report.
    counts = dispatches["outcome"].value_counts()
    most_frequent_outcome = counts.index[0]
    most_frequent_count = int(counts.iloc[0])

    # Keep possible outcomes and observations at separate conceptual levels.
    print("================================================================")
    print("LESSON 05 - STEP 1: SAMPLE SPACE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Possible outcomes in S          : {len(sample_space)}")
    print(f"Synthetic dispatch records      : {len(dispatches)}")
    print(f"Distinct outcomes observed      : {len(observed_outcomes)}")
    print("Most frequent observed outcome  : "
          f"{outcome_label(most_frequent_outcome)}")
    print(f"Records with that outcome       : {most_frequent_count}")
    print("Equal-likelihood assumption     : Not made")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Importing permits reviewing functions without running the example or
# creating a PNG as a side effect.
if __name__ == "__main__":
    main()

