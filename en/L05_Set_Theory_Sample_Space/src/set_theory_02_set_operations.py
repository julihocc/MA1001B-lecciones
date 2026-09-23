"""
Lesson 05 - Step 2: Union, Intersection, and Complement
=========================================================
NEW IN THIS STEP: define_events(), summarize_set_operations(), and
build_membership_figure().

The Recipe
    1. define_events()             creates two subsets of the sample space
    2. summarize_set_operations()  calculates union, intersection, complement
    3. build_membership_figure()   displays outcome membership explicitly

The script is standalone by design. It rebuilds S and the same 480 synthetic
records so a student can run this step without importing Step 1.
"""

from itertools import product
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

# Agg saves figures without opening windows; choose it before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


Outcome = tuple[str, str, str]
SampleSpace = tuple[Outcome, ...]

SEED = 42
OBSERVATION_COUNT = 480
SHIFTS = ("Day", "Night")
SERVICES = ("Standard", "Express")
STATUSES = ("On time", "Delayed")
SHIFT_PROBABILITIES = (0.65, 0.35)
SERVICE_PROBABILITIES = (0.70, 0.30)
BASE_DELAY_PROBABILITY = 0.10
NIGHT_DELAY_INCREMENT = 0.08
EXPRESS_DELAY_INCREMENT = 0.12
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"


def build_sample_space() -> SampleSpace:
    """Rebuild Step 1's eight shift-service-status outcomes."""
    return tuple(product(SHIFTS, SERVICES, STATUSES))


def simulate_dispatches(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the fully synthetic dispatch records from Step 1.

    The same seed, category probabilities, delay model, and outcome tuples
    reproduce the same 480 rows. The function has no file or network input.
    """
    rng = np.random.default_rng(seed)
    shifts = rng.choice(
        SHIFTS, size=OBSERVATION_COUNT, p=SHIFT_PROBABILITIES
    )
    services = rng.choice(
        SERVICES, size=OBSERVATION_COUNT, p=SERVICE_PROBABILITIES
    )
    delay_probability = (
        BASE_DELAY_PROBABILITY
        + NIGHT_DELAY_INCREMENT * (shifts == "Night")
        + EXPRESS_DELAY_INCREMENT * (services == "Express")
    )
    if np.any((delay_probability < 0) | (delay_probability > 1)):
        raise ValueError("Each delay probability must be between 0 and 1.")
    statuses = np.where(
        rng.random(OBSERVATION_COUNT) < delay_probability,
        "Delayed",
        "On time",
    )
    dispatches = pd.DataFrame(
        {
            "dispatch_id": np.arange(500_001, 500_001 + OBSERVATION_COUNT),
            "shift": shifts,
            "service": services,
            "status": statuses,
        }
    )
    dispatches["outcome"] = list(zip(shifts, services, statuses))
    return dispatches


def outcome_label(outcome: Outcome) -> str:
    """Format one outcome tuple for the membership table rows."""
    return " | ".join(outcome)


# --- NEW (1) define_events() -------------------------------------------------
def define_events(
    sample_space: SampleSpace,
) -> tuple[set[Outcome], set[Outcome]]:
    """Define A as Night and B as Delayed.

    The returned objects are events: sets of possible outcome tuples, not lists
    of observed rows. Position 0 is shift and position 2 is status. Because
    tuples are hashable, they can be members of Python sets.
    """
    event_a = {outcome for outcome in sample_space if outcome[0] == "Night"}
    event_b = {outcome for outcome in sample_space if outcome[2] == "Delayed"}
    return event_a, event_b


# --- NEW (2) summarize_set_operations() --------------------------------------
def summarize_set_operations(
    sample_space: SampleSpace,
    event_a: set[Outcome],
    event_b: set[Outcome],
) -> dict[str, set[Outcome]]:
    """Return A, B, their intersection, union, and A's relative complement.

    The complement is relative to the received sample space:
    ``A complement = set(sample_space) - A``. The operations count possible
    outcome types; they do not count repeated observations in the DataFrame.

    Raises
    ------
    ValueError
        If either event contains a tuple outside the supplied universe.
    """
    universe = set(sample_space)
    if not event_a <= universe or not event_b <= universe:
        raise ValueError("Events must be subsets of the sample space.")
    # & is intersection, | is union, and - is relative difference.
    return {
        "A": event_a,
        "B": event_b,
        "A intersection B": event_a & event_b,
        "A union B": event_a | event_b,
        "A complement": universe - event_a,
    }


# --- NEW (3) build_membership_figure() ---------------------------------------
def build_membership_figure(
    sample_space: SampleSpace,
    operations: dict[str, set[Outcome]],
) -> plt.Figure:
    """Build a 0/1 membership heatmap for each set operation.

    Each row is one possible outcome and each column is a named set. The
    returned Figure is not saved or closed here; separating construction from
    I/O makes the same calculation usable in a notebook.
    """
    column_order = ["A", "B", "A intersection B", "A union B", "A complement"]
    # int(True) is 1 and int(False) is 0: membership becomes an explicit table.
    membership = pd.DataFrame(
        {
            name: [int(outcome in operations[name]) for outcome in sample_space]
            for name in column_order
        },
        index=[outcome_label(outcome) for outcome in sample_space],
    )

    figure, axis = plt.subplots(figsize=(10.2, 5.4), layout="constrained")
    # The two colors encode 0/1. Annotated digits keep the figure readable
    # without asking the reader to infer membership from color alone.
    sns.heatmap(
        membership,
        cmap=["#EEF1F7", "#EC2661"],
        cbar=False,
        linewidths=1.0,
        linecolor="white",
        annot=True,
        fmt="d",
        annot_kws={"fontsize": 10, "color": "#000000"},
        ax=axis,
    )
    axis.set(
        title="Membership Defines Each Set Operation",
        xlabel="Event or set operation",
        ylabel="Outcome in the sample space",
    )
    axis.tick_params(axis="x", labelrotation=0, labelsize=9)
    axis.tick_params(axis="y", labelrotation=0, labelsize=9)
    return figure


def main() -> None:
    """Define A/B, print theoretical and observed counts, and save the figure."""
    sample_space = build_sample_space()
    dispatches = simulate_dispatches()
    event_a, event_b = define_events(sample_space)
    operations = summarize_set_operations(sample_space, event_a, event_b)

    # Importing the shared writer here keeps this standalone script executable
    # from the repository root while separating plotting from filesystem I/O.
    from set_theory_01_sample_space import save_figure

    figure = build_membership_figure(sample_space, operations)
    figure_path = save_figure(
        figure, DIR_FIGURES / "set_theory_02_set_operations.png"
    )

    # These masks have one boolean per observed row. They are not event sets.
    record_a = dispatches["shift"].eq("Night")
    record_b = dispatches["status"].eq("Delayed")
    print("================================================================")
    print("LESSON 05 - STEP 2: SET OPERATIONS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample-space outcomes |S|       : {len(sample_space)}")
    for name in ["A", "B", "A intersection B", "A union B", "A complement"]:
        print(f"Outcome count |{name}|".ljust(32) + f": {len(operations[name])}")
    print(f"Observed records in A           : {int(record_a.sum())}")
    print(f"Observed records in B           : {int(record_b.sum())}")
    print(f"Observed records in A and B     : {int((record_a & record_b).sum())}")
    print(f"Observed records in A or B      : {int((record_a | record_b).sum())}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()
