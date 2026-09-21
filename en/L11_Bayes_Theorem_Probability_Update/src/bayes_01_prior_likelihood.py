"""
Lesson 11 - Step 1: Prior and Likelihoods
=========================================
NEW IN THIS STEP: prior_probability(), likelihoods(), and save_figure().

Context:
The Lesson 10 100-lot inspection tree continues here. The prior is the
defective rate before seeing the flag: P(D)=0.10. The likelihoods are the
flag rates given each status: P(F|D)=0.80 and P(F|C)=0.10. Bayes' theorem
will combine these pieces in Step 2.

How to read this file:
You already know Python through OOP: functions, classes, lists, dictionaries,
loops, and conditionals. Lesson 01 introduced pathlib, the Agg backend,
unattended savefig/close, and the if __name__ entry point. Those plumbing
idioms return here with a short pointer, not a second treatise.

New in this step:
    prior                 P(D) before the inspection flag is observed
    likelihood            P(F|D) and P(F|C): flag rates given each status
    complement likelihoods  1 - P(F|status), the cleared-given-status rates
    bar chart of pieces   prior next to the two flag likelihoods, not mixed

main() stores the prior and likelihoods from the Lesson 10 tree, prints each
piece, and writes the evidence figure.

Run it:
    python bayes_01_prior_likelihood.py
"""

# Path locates figures/ from this file. See Lesson 01 for pathlib, Agg, and
# savefig/close.
from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Course-wide seed, reserved so later steps stay aligned. This script has
# no random draws: every probability is a constant from the Lesson 10 tree.
SEED = 42
# Prior P(D)=0.10: the first-stage defective rate BEFORE the flag is
# observed. From the 100-lot tree: 10 defective / 100 lots.
P_DEFECTIVE = 0.10
# Complement of the prior: P(C)=1-P(D)=0.90. The two first-stage
# probabilities must sum to 1.
P_CLEAN = 0.90
# Likelihood P(F|D)=0.80: among defective lots, the chance the inspection
# flags them. From the tree: 8 flagged / 10 defective. This is NOT P(D|F).
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
# Likelihood P(F|C)=0.10: false-flag rate among clean lots. From the tree:
# 9 flagged / 90 clean.
P_FLAGGED_GIVEN_CLEAN = 0.10
# figures/ next to this package, independent of the shell's working directory.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) prior_probability() ---------------------------------------------
def prior_probability() -> dict[str, float]:
    """Return the first-stage prior before the inspection flag is observed.

    Returns
    -------
    dict[str, float]
        p_defective is P(D), the belief that a lot is defective before
        seeing the flag. p_clean is P(C) = 1 - P(D).

    Notes
    -----
    A prior is a probability assigned before the new evidence. The
    inspection flag is that evidence; it has not been used yet. The
    annotation `-> dict[str, float]` is a type hint: string keys, float
    values. Python does not enforce it at run time.
    """
    return {
        "p_defective": P_DEFECTIVE,
        "p_clean": P_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) likelihoods() ---------------------------------------------------
def likelihoods() -> dict[str, float]:
    """Return the flag likelihoods given defective and given clean.

    Returns
    -------
    dict[str, float]
        p_flagged_given_defective is P(F|D), p_flagged_given_clean is
        P(F|C), and the two cleared rates are the complements
        1 - P(F|status).

    Notes
    -----
    A likelihood is a probability of the observed flag given a status,
    written P(flag | status). It is not the posterior P(status | flag).
    P(F|D)=0.80 looks large, but that number still conditions on the lot
    already being defective.
    """
    return {
        "p_flagged_given_defective": P_FLAGGED_GIVEN_DEFECTIVE,
        "p_flagged_given_clean": P_FLAGGED_GIVEN_CLEAN,
        # Complements: miss rate among defectives, and clear rate among
        # clean lots. Each pair (flagged, cleared) given a status sums to 1.
        "p_cleared_given_defective": 1.0 - P_FLAGGED_GIVEN_DEFECTIVE,
        "p_cleared_given_clean": 1.0 - P_FLAGGED_GIVEN_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(prior: dict[str, float], like: dict[str, float]) -> Path:
    """Save a comparison of the prior and the two flag likelihoods.

    Parameters
    ----------
    prior:
        Dict from prior_probability() with P(D) and P(C).
    like:
        Dict from likelihoods() with P(F|D) and P(F|C).

    Returns
    -------
    Path
        Absolute path of the PNG. Side effect: writes that file. Never
        calls plt.show(); see Lesson 01 for savefig/close.

    Notes
    -----
    The three bars are different kinds of probability sitting on one axis
    so they are not confused: a prior P(D), then two likelihoods that
    condition on status. Bayes' theorem in Step 2 will combine them
    rather than treat any one bar as the posterior.
    """
    output_path = DIR_FIGURES / "bayes_01_prior_likelihood.png"
    # Two-line tick labels: the probability name on the second line.
    labels = [
        "Prior\nP(D)",
        "Likelihood\nP(F | D)",
        "Likelihood\nP(F | C)",
    ]
    values = np.array(
        [
            prior["p_defective"],
            like["p_flagged_given_defective"],
            like["p_flagged_given_clean"],
        ]
    )
    colors = ["#1A2E51", "#EC2661", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probability")
    ax.set_title("Prior Defective Rate and Flag Likelihoods")
    # Headroom above 1.00 so the 0.80 and 0.10 labels are not clipped.
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        # Center the label on the bar: left edge plus half the width.
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Print the prior and likelihoods, then save the comparison figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    prior = prior_probability()
    like = likelihoods()
    figure_path = save_figure(prior, like)

    print("================================================================")
    print("LESSON 11 - STEP 1: PRIOR AND LIKELIHOODS")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"P(defective) prior              : {prior['p_defective']:.6f}")
    print(f"P(clean) prior                  : {prior['p_clean']:.6f}")
    print(
        "P(flagged | defective)          : "
        f"{like['p_flagged_given_defective']:.6f}"
    )
    print(
        "P(flagged | clean)              : "
        f"{like['p_flagged_given_clean']:.6f}"
    )
    print(
        "P(cleared | defective)          : "
        f"{like['p_cleared_given_defective']:.6f}"
    )
    print(
        "P(cleared | clean)              : "
        f"{like['p_cleared_given_clean']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()

