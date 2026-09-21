"""
Lesson 05 - Step 3: Disjoint and Exhaustive Events
==================================================
NEW IN THIS STEP: define_service_events(), compare_event_pairs(), and
build_pair_figure().

The Recipe
    1. define_service_events() creates Standard and Express events
    2. compare_event_pairs()   tests overlap and sample-space coverage
    3. build_pair_figure()     contrasts two event relationships

The script is standalone. It rebuilds the common universe and synthetic rows;
its new calculation compares (A, B) = (Night, Delayed) with
(C, D) = (Standard, Express).
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
    """Rebuild the eight possible shift-service-status outcomes."""
    return tuple(product(SHIFTS, SERVICES, STATUSES))


def simulate_dispatches(seed: int = SEED) -> pd.DataFrame:
    """Rebuild the same fully synthetic 480 dispatch records as Steps 1-2."""
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


def define_events(
    sample_space: SampleSpace,
) -> tuple[set[Outcome], set[Outcome]]:
    """Rebuild Step 2 events: A is Night and B is Delayed."""
    event_a = {outcome for outcome in sample_space if outcome[0] == "Night"}
    event_b = {outcome for outcome in sample_space if outcome[2] == "Delayed"}
    return event_a, event_b


# --- NEW (1) define_service_events() -----------------------------------------
def define_service_events(
    sample_space: SampleSpace,
) -> tuple[set[Outcome], set[Outcome]]:
    """Define C as Standard service and D as Express service.

    Every outcome has exactly one service, so C and D cannot overlap and
    together cover every member of S. That is a partition: mutually exclusive
    and exhaustive at once. A and B from Step 2 do not form a partition.
    """
    event_c = {outcome for outcome in sample_space if outcome[1] == "Standard"}
    event_d = {outcome for outcome in sample_space if outcome[1] == "Express"}
    return event_c, event_d


# --- NEW (2) compare_event_pairs() -------------------------------------------
def compare_event_pairs(
    sample_space: SampleSpace,
    pairs: dict[str, tuple[set[Outcome], set[Outcome]]],
) -> pd.DataFrame:
    """Compare intersection, union, disjointness, and exhaustiveness.

    Parameters
    ----------
    sample_space : tuple
        Ordered S, converted to a set for equality and membership checks.
    pairs : dict
        Mapping from a pair name to (first event, second event).

    Returns
    -------
    pandas.DataFrame
        One row per pair with intersection_size, union_size, disjoint, and
        exhaustive columns.

    Raises
    ------
    ValueError
        If no pairs are supplied or an event contains a result outside S.

    Notes
    -----
    Disjoint means the intersection is empty. Exhaustive means the union
    equals S. These are independent checks; equal cardinalities alone do not
    prove set equality.
    """
    if not pairs:
        raise ValueError("At least one event pair is required.")
    universe = set(sample_space)
    rows = []
    for pair_name, (first, second) in pairs.items():
        if not first <= universe or not second <= universe:
            raise ValueError("Events must be subsets of the sample space.")
        # Compute each operation once and reuse it for both properties.
        intersection = first & second
        union = first | second
        rows.append(
            {
                "pair": pair_name,
                "intersection_size": len(intersection),
                "union_size": len(union),
                "disjoint": not intersection,
                "exhaustive": union == universe,
            }
        )
    return pd.DataFrame(rows).set_index("pair")


# --- NEW (3) build_pair_figure() ---------------------------------------------
def build_pair_figure(
    comparison: pd.DataFrame,
    sample_space_size: int,
) -> plt.Figure:
    """Represent overlap and coverage for the event pairs received.

    The input table contains exact cardinalities. ``melt`` reshapes those
    columns for Seaborn; it does not calculate new mathematical quantities.
    The dashed line is the size of the received universe, not a hard-coded 8.
    """
    sizes = comparison[["intersection_size", "union_size"]].rename(
        columns={
            "intersection_size": "Intersection",
            "union_size": "Union",
        }
    )
    sizes = sizes.rename_axis("pair").reset_index().melt(
        id_vars="pair", var_name="measure", value_name="outcomes"
    )
    sizes["pair"] = sizes["pair"].str.replace(" / ", "\n", regex=False)

    figure, axis = plt.subplots(figsize=(9.2, 5.2), layout="constrained")
    sns.barplot(
        data=sizes,
        x="pair",
        y="outcomes",
        hue="measure",
        hue_order=["Intersection", "Union"],
        estimator="sum",
        errorbar=None,
        palette={"Intersection": "#EC2661", "Union": "#1A2E51"},
        ax=axis,
    )
    # Zero intersection means disjointness; reaching |S| means coverage.
    axis.axhline(
        sample_space_size,
        color="#0039A6",
        linestyle="--",
        label="Entire sample space",
    )
    axis.set(
        title="Disjointness and Exhaustiveness Answer Different Questions",
        xlabel="",
        ylabel="Number of possible outcomes",
        ylim=(0, sample_space_size + 2),
    )
    for bars in axis.containers:
        axis.bar_label(bars, fmt="%.0f", padding=3)
    axis.legend(
        title=None, loc="upper left", bbox_to_anchor=(1, 1), frameon=False
    )
    return figure


def main() -> None:
    """Compare two event pairs, report their properties, and save the figure."""
    sample_space = build_sample_space()
    dispatches = simulate_dispatches()
    event_a, event_b = define_events(sample_space)
    event_c, event_d = define_service_events(sample_space)
    comparison = compare_event_pairs(
        sample_space,
        {
            "A: Night / B: Delayed": (event_a, event_b),
            "C: Standard / D: Express": (event_c, event_d),
        },
    )
    from set_theory_01_sample_space import save_figure

    figure = build_pair_figure(comparison, len(sample_space))
    figure_path = save_figure(
        figure, DIR_FIGURES / "set_theory_03_disjoint_events.png"
    )

    print("================================================================")
    print("LESSON 05 - STEP 3: DISJOINT EVENTS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Sample-space outcomes |S|       : {len(sample_space)}")
    print(f"Synthetic dispatch records      : {len(dispatches)}")
    for pair_name, row in comparison.iterrows():
        print(f"Pair                            : {pair_name}")
        print(f"  Intersection size             : {int(row['intersection_size'])}")
        print(f"  Union size                    : {int(row['union_size'])}")
        print(f"  Mutually exclusive            : {bool(row['disjoint'])}")
        print(f"  Exhaustive                    : {bool(row['exhaustive'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()
