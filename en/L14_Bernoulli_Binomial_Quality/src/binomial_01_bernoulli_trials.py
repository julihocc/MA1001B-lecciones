"""
Lesson 14 - Step 1: Bernoulli Trials
====================================
NEW IN THIS STEP: bernoulli_trial(), binomial_assumptions(), and save_figure().

THE RECIPE
Build the first complete program in this order:
    1. bernoulli_trial()         two-point masses p and q = 1 - p
    2. binomial_assumptions()    n, constant p, q, and the mean np
    3. save_figure()             bar chart of one Bernoulli inspection

Context:
A fully synthetic inspection of one unit is a Bernoulli trial with success
probability p = 0.08 (the unit is defective). Repeating that trial n = 20
times, independently and with the same p, produces a binomial count X.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script adds the Bernoulli trial
and the four ingredients of a binomial count.

    dict[str, float]     a type hint: string keys, float values
    float | int          a type hint: the value may be either type
    ax.bar / ax.text     two-bar probability chart with numeric labels

main() reports p, q, n, and np for one synthetic inspection lot and writes
the two-point evidence figure. No earlier lesson script is imported.

Run it:
    python binomial_01_bernoulli_trials.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy is imported so Steps 2-3 can add array
# work without changing the import block. The aliases are the same ones
# used from Lesson 01 onward.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. This Step 1 script does not draw random
# numbers, but the seed is reserved so later steps stay aligned.
SEED = 42
# n: a fixed number of independent inspections in one lot. That fixed n is
# the first binomial assumption.
N_TRIALS = 20
# p: P(defective) on one inspection. In a Bernoulli trial the event of
# interest is called "success" even when it is a quality failure.
P_DEFECT = 0.08
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) bernoulli_trial() -----------------------------------------------
def bernoulli_trial() -> dict[str, float]:
    """Return the two-point distribution for one inspection.

    Returns
    -------
    dict[str, float]
        p_defect is P(success) = p. p_clean is P(failure) = q = 1 - p.
        The two values sum to 1 because a Bernoulli trial has exactly two
        outcomes.

    Notes
    -----
    A Bernoulli trial is one yes/no experiment. Here "yes" means the
    inspected unit is defective. There is no third outcome, and p does not
    change from one isolated inspection to the next. Repeating this trial
    n times under the binomial assumptions produces the count X in Step 2.
    """
    return {
        "p_defect": P_DEFECT,
        "p_clean": 1.0 - P_DEFECT,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) binomial_assumptions() ------------------------------------------
def binomial_assumptions() -> dict[str, float | int]:
    """Return the binomial ingredients n, p, mean np, and q = 1 - p.

    Returns
    -------
    dict[str, float | int]
        n is the fixed number of trials (an int). p is the constant success
        chance. q = 1 - p is the failure chance. mean_np is the expected
        defect count n * p, a mean, not a probability.

    Notes
    -----
    Four assumptions turn n Bernoulli trials into X ~ Binomial(n, p):
        1. n is fixed in advance (here 20 inspections per lot).
        2. each trial has two outcomes (defective / clean).
        3. p is the same on every trial.
        4. trials are independent.
    Step 3 will break assumption 3 by mixing two different p values.
    The annotation float | int means a value may be either type; Python
    does not enforce it at run time.
    """
    return {
        "n": N_TRIALS,
        "p": P_DEFECT,
        "q": 1.0 - P_DEFECT,
        "mean_np": N_TRIALS * P_DEFECT,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(trial: dict[str, float]) -> Path:
    """Save the Bernoulli two-point mass function.

    Parameters
    ----------
    trial:
        The dict from bernoulli_trial(), with p_clean and p_defect.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    A Bernoulli PMF has mass at only two points. The left bar is q = 0.92
    (clean / failure). The right bar is p = 0.08 (defective / success).
    Those two heights are the entire distribution of one inspection.
    """
    output_path = DIR_FIGURES / "binomial_01_bernoulli_trials.png"
    # A newline in each label stacks "failure"/"success" under the outcome name.
    labels = ["Clean\n(failure)", "Defective\n(success)"]
    values = [trial["p_clean"], trial["p_defect"]]
    colors = ["#1A2E51", "#EC2661"]

    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Probability")
    ax.set_title("One Bernoulli Inspection: p = 0.08")
    # 1.05 leaves room above p_clean = 0.92 for the numeric label.
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each BarContainer patch with its probability so the label
    # can sit at the center of the bar, slightly above the top.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 Bernoulli report and write the two-point figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    trial = bernoulli_trial()
    assumptions = binomial_assumptions()
    figure_path = save_figure(trial)

    print("================================================================")
    print("LESSON 14 - STEP 1: BERNOULLI TRIALS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"P(defective) on one trial       : {trial['p_defect']:.6f}")
    print(f"P(clean) on one trial           : {trial['p_clean']:.6f}")
    print(f"Number of trials n              : {assumptions['n']}")
    print(f"Constant p across trials        : {assumptions['p']:.6f}")
    print(f"q = 1 - p                       : {assumptions['q']:.6f}")
    # np = 20 * 0.08 = 1.6 expected defectives in the lot, not a chance.
    print(f"Target mean np                  : {assumptions['mean_np']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

