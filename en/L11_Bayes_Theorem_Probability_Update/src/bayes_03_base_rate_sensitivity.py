"""
Lesson 11 - Step 3: Base-Rate Sensitivity
=========================================
THE RECIPE
Start from bayes_02_posterior.py, then introduce:
    1. posterior_from_prior()   P(D|F) as a function of the defective prior
    2. naive_likelihood_as_posterior()  the base-rate fallacy P(D|F) ~ P(F|D)
    3. save_figure()            contrast prior 0.10 with prior 0.02

If the prior collapses from 0.10 to 0.02, the posterior falls with it even
though the likelihoods stay at 0.80 and 0.10. Ignoring the base rate is the
limit of this lesson.

How to read this file:
You already know Python through OOP. Step 2 applied Bayes' theorem at prior
0.10. This step reuses the same update as a function of the prior. Lesson 01
still covers pathlib, Agg, savefig/close, and if __name__.

New in this step:
    posterior as a function of the prior, likelihoods held fixed
    rare base rate        P(D)=0.02 versus the original P(D)=0.10
    base-rate fallacy     treating P(F|D) as if it were P(D|F)
    sensitivity curve     posterior versus prior on [0.01, 0.40]

main() recomputes P(D|F) at both priors, prints the naive 0.80 shortcut,
and writes the evidence figure.

Run it:
    python bayes_03_base_rate_sensitivity.py
"""

# Path locates figures/ from this file. See Lesson 01 for pathlib, Agg, and
# savefig/close.
from pathlib import Path

import matplotlib

# Same unattended-figure setup as Lesson 01: select Agg before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Reserved course seed; the sensitivity study is arithmetic, not a draw.
SEED = 42
# Likelihoods held fixed so only the base rate moves. P(F|D)=0.80 is still
# not the posterior.
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
P_FLAGGED_GIVEN_CLEAN = 0.10
# Original Lesson 10 / Step 2 prior: 10 defective lots in 100.
PRIOR_ORIGINAL = 0.10
# Rare-event prior: the same inspection, but defectives are now 2 in 100.
PRIOR_RARE = 0.02
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) posterior_from_prior() ------------------------------------------
def posterior_from_prior(prior_defective: float) -> dict[str, float]:
    """Update P(D|F) when only the defective base rate changes.

    Parameters
    ----------
    prior_defective:
        A candidate P(D). Likelihoods stay at the module constants
        P(F|D)=0.80 and P(F|C)=0.10.

    Returns
    -------
    dict[str, float]
        prior, numerator P(F and D), p_flagged from the two-path sum,
        and posterior P(D|F).

    Notes
    -----
    Holding the likelihoods fixed isolates base-rate sensitivity: any
    change in the posterior comes only from the prior. When P(D) is
    small, most flags come from the large clean group, so P(D|F) stays
    well below P(F|D). At prior 0.02: numerator 0.016, P(F)=0.114,
    posterior ≈ 0.140351.
    """
    p_clean = 1.0 - prior_defective
    # Same Bayes numerator as Step 2: P(F|D) P(D).
    numerator = P_FLAGGED_GIVEN_DEFECTIVE * prior_defective
    # False-flag path: P(F|C) P(C). Grows as the prior shrinks because
    # P(C)=1-P(D) then covers almost every lot.
    path_clean = P_FLAGGED_GIVEN_CLEAN * p_clean
    p_flagged = numerator + path_clean
    return {
        "prior": prior_defective,
        "numerator": numerator,
        "p_flagged": p_flagged,
        # Bayes update: posterior = numerator / P(F).
        "posterior": numerator / p_flagged,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) naive_likelihood_as_posterior() ---------------------------------
def naive_likelihood_as_posterior() -> float:
    """Return the mistaken identification of P(D|F) with P(F|D).

    Returns
    -------
    float
        P(F|D)=0.80, unchanged by the prior.

    Notes
    -----
    The base-rate fallacy treats a high detection rate as if it were the
    posterior. Bayes' theorem still divides by P(F), which includes false
    flags. This function returns the naive number so the figure can plot
    it as a horizontal line that does not move when the prior changes.
    """
    return P_FLAGGED_GIVEN_DEFECTIVE
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    original: dict[str, float],
    rare: dict[str, float],
    naive: float,
) -> Path:
    """Save posterior versus prior and the naive likelihood shortcut.

    Parameters
    ----------
    original, rare:
        Dicts from posterior_from_prior() at P(D)=0.10 and P(D)=0.02.
    naive:
        P(F|D) from naive_likelihood_as_posterior(), the fallacy line.

    Returns
    -------
    Path
        Absolute path of the PNG. See Lesson 01 for savefig/close.

    Notes
    -----
    The curve is the Bayes posterior as a function of the prior, with
    likelihoods fixed. Two marked points are the lesson cases. The dashed
    horizontal line is the naive 0.80 that ignores the base rate.
    """
    output_path = DIR_FIGURES / "bayes_03_base_rate_sensitivity.png"
    # 80 equally spaced priors from 1% to 40%. Each is fed through the
    # same Bayes update; only P(D) changes.
    priors = np.linspace(0.01, 0.40, 80)
    posteriors = np.array(
        [posterior_from_prior(p)["posterior"] for p in priors]
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(
        priors,
        posteriors,
        color="#1A2E51",
        lw=2.2,
        label="Bayes posterior P(D | F)",
    )
    # Horizontal line at P(F|D): the base-rate fallacy, independent of P(D).
    ax.axhline(
        naive,
        color="#EC2661",
        linestyle="--",
        lw=1.6,
        label="Naive: treat P(F | D) as the posterior",
    )
    ax.scatter(
        [original["prior"], rare["prior"]],
        [original["posterior"], rare["posterior"]],
        color=["#5B8DEF", "#EC2661"],
        s=70,
        zorder=5,
    )
    ax.annotate(
        f"prior={original['prior']:.2f}\nposterior={original['posterior']:.3f}",
        xy=(original["prior"], original["posterior"]),
        xytext=(0.16, 0.62),
        fontsize=8,
        color="#1A2E51",
        arrowprops=dict(arrowstyle="-|>", color="#1A2E51"),
    )
    ax.annotate(
        f"prior={rare['prior']:.2f}\nposterior={rare['posterior']:.3f}",
        xy=(rare["prior"], rare["posterior"]),
        xytext=(0.08, 0.32),
        fontsize=8,
        color="#EC2661",
        arrowprops=dict(arrowstyle="-|>", color="#EC2661"),
    )
    ax.set_xlabel("Prior P(D)")
    ax.set_ylabel("Posterior P(D | F)")
    ax.set_title("A Rare Defective Rate Collapses the Posterior")
    ax.set_xlim(0.00, 0.42)
    ax.set_ylim(0.00, 0.90)
    ax.grid(linestyle="--", alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Compare the original and rare-prior posteriors with the naive shortcut.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    original = posterior_from_prior(PRIOR_ORIGINAL)
    rare = posterior_from_prior(PRIOR_RARE)
    naive = naive_likelihood_as_posterior()
    figure_path = save_figure(original, rare, naive)

    print("================================================================")
    print("LESSON 11 - STEP 3: BASE-RATE SENSITIVITY")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Likelihood P(F | D)             : {P_FLAGGED_GIVEN_DEFECTIVE:.6f}")
    print(f"Likelihood P(F | C)             : {P_FLAGGED_GIVEN_CLEAN:.6f}")
    print(f"Original prior P(D)             : {original['prior']:.6f}")
    print(f"Original P(F)                   : {original['p_flagged']:.6f}")
    print(f"Original posterior P(D | F)     : {original['posterior']:.6f}")
    print(f"Rare prior P(D)                 : {rare['prior']:.6f}")
    print(f"Rare P(F)                       : {rare['p_flagged']:.6f}")
    print(f"Rare posterior P(D | F)         : {rare['posterior']:.6f}")
    print(f"Naive P(F | D) treated as P(D|F): {naive:.6f}")
    print(
        "Posterior drop (0.10 to 0.02)   : "
        f"{original['posterior'] - rare['posterior']:.6f}"
    )
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Standard script entry point; see Lesson 01 for the if __name__ idiom.
if __name__ == "__main__":
    main()

