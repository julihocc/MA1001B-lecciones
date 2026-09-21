"""
Lesson 18 - Step 3: Fatigue Makes Trials Dependent
==================================================
THE RECIPE
Start from waiting_times_02_negative_binomial.py, then introduce:
    1. fatigue_success_probability()  p declines with trial number
    2. simulate_waiting_times()       seed-42 waiting times under fatigue
    3. save_figure()                  geometric mean versus fatigued mean

If inspector fatigue lowers p on later trials, the trials are no longer
independent with constant p. Waiting times then exceed 1/p.

How to read this file:
You already know Python through OOP. Steps 1-2 built the geometric wait
for the first success and the negative-binomial wait for r = 3, both
under independent trials with constant p. Lesson 01 covers pathlib and
unattended savefig. This step keeps the opening p = 0.12 but lets p
decline with the trial number.

    p * 0.97**(t-1)      declining success chance on trial t
    default_rng(seed)    NumPy Generator for the fatigued waits
    still_open mask      vectorized first-success search
    stats.geom.rvs       constant-p Monte Carlo of the geometric mean

main() prints p on trials 1 and 10, the fatigued simulated mean, and the
constant-p simulated mean. The fatigued wait exceeds 1/p because later
trials are less likely to succeed.

Run it:
    python waiting_times_03_fatigue_dependence.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.geom.rvs draws constant-p geometric waiting times for the
# comparison mean. The fatigued waits use NumPy's Generator instead.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P_SUCCESS = 0.12
# Multiplicative decay of p, not a stopping probability: each later trial
# has 97% of the previous trial's success chance.
FATIGUE_RATIO = 0.97
N_SIMULATIONS = 10_000
# Hard cap so a path whose p has decayed toward 0 cannot loop forever.
MAX_TRIALS = 400
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def geometric_parameters() -> dict[str, float]:
    """Return p and E[X] = 1/p for trials until the first success.

    Rebuilt from Step 1 so this file does not import that script. The
    closed form 1/p is the constant-p benchmark that fatigue will exceed.
    """
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
    }


# --- NEW (1) fatigue_success_probability() -----------------------------------
def fatigue_success_probability(trial_number: np.ndarray) -> np.ndarray:
    """Return a declining success probability p * 0.97^(t-1).

    Parameters
    ----------
    trial_number:
        Inspection index t = 1, 2, 3, ... as an array. t = 1 is the first
        trial, so the exponent is 0 and the returned chance is p.

    Returns
    -------
    np.ndarray
        Success probability on each requested trial. Values fall as t
        grows because FATIGUE_RATIO = 0.97 is less than 1.

    Notes
    -----
    The geometric model needs the same p on every independent trial.
    Here p_t = 0.12 * 0.97^(t-1), so trial 1 still has p = 0.12 but
    trial 10 has p = 0.12 * 0.97^9 ≈ 0.091. Later inspections are less
    likely to catch a defective, and the trials are no longer i.i.d.
    A mean wait of 1/p is then the wrong formula.
    """
    return P_SUCCESS * (FATIGUE_RATIO ** (trial_number - 1))
# ------------------------------------------------------------------------------


# --- NEW (2) simulate_waiting_times() ----------------------------------------
def simulate_waiting_times(
    n_simulations: int = N_SIMULATIONS,
    seed: int = SEED,
) -> np.ndarray:
    """Simulate waiting times when p declines with each trial.

    Parameters
    ----------
    n_simulations:
        Number of independent synthetic audits. Default 10_000.
    seed:
        Seed for np.random.default_rng. Default SEED = 42.

    Returns
    -------
    np.ndarray
        Length n_simulations. Entry i is the trial of first success in
        audit i, or MAX_TRIALS if no success occurred by the cap.

    Notes
    -----
    All audits run in parallel. On trial t every still-open audit draws
    an independent Uniform(0, 1) and succeeds if that draw is less than
    p_t. The first success records t and closes that audit. Because p_t
    falls with t, typical waits are longer than the constant-p mean 1/p.

    rng.random is called with the full length n_simulations on every
    trial, including audits already closed. That keeps the random stream
    independent of which audits finished early.
    """
    rng = np.random.default_rng(seed)
    # Start every wait at the cap; a first success overwrites this value.
    waits = np.full(n_simulations, MAX_TRIALS, dtype=int)
    still_open = np.ones(n_simulations, dtype=bool)
    for trial in range(1, MAX_TRIALS + 1):
        # Wrap the scalar trial in an array so the Step-3 helper, which
        # is written for arrays, can return p_t as a one-element result.
        p_t = float(fatigue_success_probability(np.array([trial]))[0])
        # Bernoulli(p_t) vector: True where that audit succeeds on trial t.
        success = rng.random(n_simulations) < p_t
        newly_done = still_open & success
        waits[newly_done] = trial
        still_open[newly_done] = False
        if not np.any(still_open):
            break
    return waits
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(geometric_mean: float, fatigued_mean: float) -> Path:
    """Contrast the constant-p mean with the fatigued mean.

    Parameters
    ----------
    geometric_mean:
        Closed-form E[X] = 1/p from geometric_parameters().
    fatigued_mean:
        Sample mean of the seed-42 fatigued waiting times.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Left bar: the geometric formula 1/p, valid only for independent
    trials with constant p. Right bar: the simulated mean when p declines.
    The gap is the visual of the constant-p / independence limit.
    """
    output_path = DIR_FIGURES / "waiting_times_03_fatigue_dependence.png"
    labels = ["Geometric\nE[X] = 1/p", "Fatigue\nsimulated mean"]
    values = [geometric_mean, fatigued_mean]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Mean waiting time (trials)")
    ax.set_title("Declining p Makes the Wait Longer Than 1/p")
    ax.set_ylim(0, 22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # zip pairs each bar with its mean so the label sits centered above it.
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.25,
            f"{value:.3f}",
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
    """Run the Step 3 fatigue comparison and write the two-bar figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    geom = geometric_parameters()
    p_trial_1 = float(fatigue_success_probability(np.array([1]))[0])
    p_trial_10 = float(fatigue_success_probability(np.array([10]))[0])
    waits = simulate_waiting_times()
    fatigued_mean = float(np.mean(waits))
    # Constant-p Monte Carlo from scipy.stats.geom, same n and seed
    # integer as the fatigued run but a different RNG family, so the two
    # simulated means are not paired draws.
    geometric_draws = stats.geom.rvs(p=P_SUCCESS, size=N_SIMULATIONS, random_state=SEED)
    figure_path = save_figure(geom["mean"], fatigued_mean)

    print("================================================================")
    print("LESSON 18 - STEP 3: FATIGUE DEPENDENCE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Simulated waiting times         : {N_SIMULATIONS:,}")
    print(f"Geometric E[X] = 1/p            : {geom['mean']:.6f}")
    print(f"Fatigue p on trial 1            : {p_trial_1:.6f}")
    print(f"Fatigue p on trial 10           : {p_trial_10:.6f}")
    print(f"Fatigued simulated mean         : {fatigued_mean:.6f}")
    print(f"Constant-p simulated mean       : {float(np.mean(geometric_draws)):.6f}")
    print(f"Fatigue mean exceeds 1/p        : {fatigued_mean > geom['mean']}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

