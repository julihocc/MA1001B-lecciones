"""
Lesson 11 - Step 2: Bayes Formula and the Posterior
===================================================
THE RECIPE
Start from bayes_01_prior_likelihood.py, then introduce:
    1. bayes_numerator()     P(F|D) P(D), the defective-and-flagged path
    2. bayes_denominator()   law of total probability for P(F)
    3. posterior()           P(D|F) = numerator / denominator

The same 100-lot tree is rebuilt from the same constants. No earlier lesson
script is imported. The posterior equals 8/17 from the frequency tree.

How to read this file:
You already know Python through OOP. Step 1 stored the prior and flag
likelihoods. Those helpers are copied here so the script stays self-contained;
comments concentrate on the NEW bands. Lesson 01 remains the reference for
pathlib, Agg, savefig/close, and if __name__.

New in this step:
    Bayes numerator       P(F and D) = P(F|D) P(D)
    law of total probability  P(F) = sum of the two flagged paths
    posterior / Bayes update  P(D|F) = numerator / P(F)
    frequency check       8/17 from the Lesson 10 tree

main() multiplies the defective-and-flagged path, adds the two flagged
paths to get P(F), divides to obtain P(D|F), and matches 8/17.

Run it:
    python bayes_02_posterior.py
"""

# Path locates figures/ from this file. See Lesson 01 for pathlib, Agg, and
# savefig/close.
from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Reserved course seed; the update itself is arithmetic on constants.
SEED = 42
# Prior P(D) and P(C), copied from Step 1: belief before the flag.
P_DEFECTIVE = 0.10
P_CLEAN = 0.90
# Likelihoods, copied from Step 1: P(F|D) and P(F|C). They are not the
# posterior; Bayes' theorem will invert the conditioning.
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
P_FLAGGED_GIVEN_CLEAN = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def prior_probability() -> dict[str, float]:
    """Return the first-stage prior before the inspection flag is observed.

    Copied from Step 1 so this file stays standalone. P(D)=0.10 is the
    belief that a lot is defective before seeing the flag.
    """
    return {
        "p_defective": P_DEFECTIVE,
        "p_clean": P_CLEAN,
    }


def likelihoods() -> dict[str, float]:
    """Return the flag likelihoods given defective and given clean.

    Copied from Step 1 with only the two flag rates: Bayes' theorem for
    P(D|F) uses P(F|D) and P(F|C), not the cleared complements.
    """
    return {
        "p_flagged_given_defective": P_FLAGGED_GIVEN_DEFECTIVE,
        "p_flagged_given_clean": P_FLAGGED_GIVEN_CLEAN,
    }


# --- NEW (1) bayes_numerator() -----------------------------------------------
def bayes_numerator(prior: dict[str, float], like: dict[str, float]) -> float:
    """Return P(F and D) = P(F|D) P(D).

    Parameters
    ----------
    prior:
        Step 1 dict; prior['p_defective'] is P(D).
    like:
        Step 1 dict; like['p_flagged_given_defective'] is P(F|D).

    Returns
    -------
    float
        The joint probability of the defective-and-flagged path. On this
        tree: 0.80 * 0.10 = 0.08.

    Notes
    -----
    This product is the numerator of Bayes' theorem for P(D|F). It is also
    the Lesson 10 path probability: multiply along the defective then
    flagged branches.
    """
    return like["p_flagged_given_defective"] * prior["p_defective"]
# ------------------------------------------------------------------------------


# --- NEW (2) bayes_denominator() ---------------------------------------------
def bayes_denominator(prior: dict[str, float], like: dict[str, float]) -> dict[str, float]:
    """Return P(F) by adding the two mutually exclusive flagged paths.

    Parameters
    ----------
    prior, like:
        The same Step 1 dictionaries used by bayes_numerator().

    Returns
    -------
    dict[str, float]
        defective_and_flagged is P(F and D), clean_and_flagged is
        P(F and C), and p_flagged is their sum P(F).

    Notes
    -----
    Law of total probability: P(F) = P(F|D)P(D) + P(F|C)P(C). The first
    term is the Bayes numerator; the second is the false-flag path. On
    this tree: 0.08 + 0.09 = 0.17. The paths are mutually exclusive
    because a lot cannot be both defective and clean.
    """
    path_defective = like["p_flagged_given_defective"] * prior["p_defective"]
    path_clean = like["p_flagged_given_clean"] * prior["p_clean"]
    return {
        "defective_and_flagged": path_defective,
        "clean_and_flagged": path_clean,
        "p_flagged": path_defective + path_clean,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) posterior() -----------------------------------------------------
def posterior(numerator: float, p_flagged: float) -> float:
    """Return P(D|F) from Bayes' theorem.

    Parameters
    ----------
    numerator:
        P(F and D) from bayes_numerator().
    p_flagged:
        P(F) from the denominator, the total probability of a flag.

    Returns
    -------
    float
        The posterior P(D|F): the updated probability that a lot is
        defective AFTER the flag is observed.

    Notes
    -----
    Bayes update: posterior = (likelihood * prior) / evidence, here
    0.08 / 0.17 = 8/17 ≈ 0.470588. The posterior is larger than the
    prior 0.10, so the flag is informative, but it is far from the
    likelihood 0.80.
    """
    return numerator / p_flagged
# ------------------------------------------------------------------------------


def save_figure(paths: dict[str, float], posterior_value: float) -> Path:
    """Save the two flagged paths and the resulting posterior.

    Parameters
    ----------
    paths:
        Dict from bayes_denominator() with the two flagged-path joints
        and P(F).
    posterior_value:
        P(D|F) from posterior().

    Returns
    -------
    Path
        Absolute path of the PNG. See Lesson 01 for savefig/close.

    Notes
    -----
    Four bars on one axis: numerator, false-flag path, their sum P(F),
    and the posterior. The posterior is a ratio, not a fourth path, so
    it can sit above P(F) even though it is built from those paths.
    """
    output_path = DIR_FIGURES / "bayes_02_posterior.png"
    labels = [
        "P(D and F)\nnumerator",
        "P(C and F)",
        "P(F)\ndenominator",
        "P(D | F)\nposterior",
    ]
    values = np.array(
        [
            paths["defective_and_flagged"],
            paths["clean_and_flagged"],
            paths["p_flagged"],
            posterior_value,
        ]
    )
    colors = ["#EC2661", "#5B8DEF", "#1A2E51", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probability")
    ax.set_title("Bayes: Posterior = Flagged-and-Defective Path / P(F)")
    # Headroom above 0.47 so the posterior label is not clipped.
    ax.set_ylim(0, 0.55)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.015,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path


def main() -> None:
    """Apply Bayes' theorem and match the posterior to the 8/17 tree ratio.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    prior = prior_probability()
    like = likelihoods()
    # Numerator of the Bayes update: likelihood times prior.
    numerator = bayes_numerator(prior, like)
    # Denominator: P(F) from the two mutually exclusive flagged paths.
    paths = bayes_denominator(prior, like)
    posterior_value = posterior(numerator, paths["p_flagged"])
    # Same ratio as counts on the Lesson 10 tree: 8 flagged-defective
    # lots out of 17 flagged lots.
    frequency_check = 8 / 17
    figure_path = save_figure(paths, posterior_value)

    print("================================================================")
    print("LESSON 11 - STEP 2: BAYES POSTERIOR")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Prior P(D)                      : {prior['p_defective']:.6f}")
    print(
        "Likelihood P(F | D)             : "
        f"{like['p_flagged_given_defective']:.6f}"
    )
    print(
        "Likelihood P(F | C)             : "
        f"{like['p_flagged_given_clean']:.6f}"
    )
    print(f"Numerator P(D and F)            : {numerator:.6f}")
    print(f"Path P(C and F)                 : {paths['clean_and_flagged']:.6f}")
    print(f"Denominator P(F)                : {paths['p_flagged']:.6f}")
    print(f"Posterior P(D | F)              : {posterior_value:.6f}")
    print(f"Frequency check 8/17            : {frequency_check:.6f}")
    # isclose, not ==: 0.08 and 0.17 are binary floats, so the quotient
    # may not match 8/17 bit for bit even when the math is the same.
    print(f"Matches 8/17                    : {np.isclose(posterior_value, frequency_check)}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()

