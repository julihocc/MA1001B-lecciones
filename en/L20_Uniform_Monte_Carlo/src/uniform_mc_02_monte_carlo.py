"""
Lesson 20 - Step 2: Monte Carlo Check of the Uniform Tail
=========================================================
THE RECIPE
Start from uniform_mc_01_exact_uniform.py, then introduce:
    1. draw_processing_times()  100,000 Uniform(8, 20) draws, seed 42
    2. monte_carlo_tail()       simulated P(X > 16) and sample mean
    3. save_figure()            histogram versus the exact flat density

The same Uniform(8, 20) model is rebuilt. No earlier lesson script is
imported.

How to read this file:
You already know Python through OOP. Step 1 built the exact Uniform(8, 20)
clock: height 1/12, mean 14, tail P(X > 16) = 1/3. Lesson 01 covers
pathlib and unattended savefig; they are rebuilt here only so the script
stays self-contained. This step checks that exact tail by simulation.

    np.random.default_rng(SEED)  seeded Generator; 42 is course-wide
    rng.uniform(a, b, size)      NumPy draw from Uniform(a, b)
    model.rvs(..., random_state=rng)  SciPy equivalent of rng.uniform
    draws > CUT                  boolean mask, True where the time exceeds 16
    np.mean(draws > CUT)         Monte Carlo estimate of P(X > 16)
    ax.hist(..., density=True)   histogram scaled to area 1, overlay pdf

Monte Carlo here means: draw a large seeded sample, count the fraction
of draws in the event, and compare that fraction with the exact 1/3.
It is a numerical check, not a new probability model.

main() prints the exact tail, the Monte Carlo tail, the absolute error,
and both means, then saves the histogram overlay.

Run it:
    python uniform_mc_02_monte_carlo.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.uniform is reused from Step 1: frozen Uniform(loc, loc + scale).
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Seed 42 now actually drives the Generator. The same integer rebuilds
# the same 100,000 draws on every run.
SEED = 42
A = 8.0
B = 20.0
CUT = 16.0
# Monte Carlo sample size. The underscore is a readability separator;
# Python treats 100_000 as 100000. Larger n shrinks the simulation error.
N_DRAWS = 100_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def uniform_model():
    """Return the continuous uniform model on [8, 20] minutes.

    Rebuilt from Step 1 so this file does not import the earlier script.
    SciPy uses loc=a and scale=b-a, so loc=8 and scale=12 is Uniform(8, 20).
    The density is the constant 1/12 on that interval.
    """
    return stats.uniform(loc=A, scale=B - A)


# --- NEW (1) draw_processing_times() -----------------------------------------
def draw_processing_times(model, n_draws: int = N_DRAWS) -> np.ndarray:
    """Draw n_draws processing times from Uniform(8, 20) with seed 42.

    Parameters
    ----------
    model:
        Frozen Uniform(8, 20) from uniform_model().
    n_draws:
        How many independent times to simulate. Default N_DRAWS = 100_000.

    Returns
    -------
    np.ndarray
        Length n_draws. Each entry is a synthetic processing time in
        minutes, drawn from Uniform(8, 20).

    Notes
    -----
    np.random.default_rng(SEED) builds a Generator. Passing that Generator
    as random_state pins SciPy's sampler to the same stream.

        model.rvs(size=n_draws, random_state=rng)

    is the SciPy form of a Uniform(a, b) sample. The NumPy form of the
    same idea is

        rng.uniform(A, B, size=n_draws)

    which draws from [A, B) with the endpoint parameterisation, not
    SciPy's loc/scale. Both are continuous-uniform draws; this lesson
    uses model.rvs so the sample and the exact pdf share one model
    object. Do not mix this Generator with the older np.random.seed()
    global state.
    """
    # One Generator, seeded at 42, owns every draw in this function.
    rng = np.random.default_rng(SEED)
    # rvs = "random variates". random_state=rng is the Generator, not
    # the integer 42 by itself; wrapping it keeps the stream explicit.
    # Equivalent NumPy call: rng.uniform(A, B, size=n_draws).
    return model.rvs(size=n_draws, random_state=rng)
# ------------------------------------------------------------------------------


# --- NEW (2) monte_carlo_tail() ----------------------------------------------
def monte_carlo_tail(draws: np.ndarray, exact_tail: float) -> dict[str, float]:
    """Estimate the tail and mean, and report the Monte Carlo error.

    Parameters
    ----------
    draws:
        The Uniform(8, 20) sample from draw_processing_times().
    exact_tail:
        Step 1 value P(X > 16) = 1/3, used only to measure error.

    Returns
    -------
    dict[str, float]
        estimated_tail is the sample proportion of times above 16.
        sample_mean is the arithmetic mean of the draws.
        abs_error is |estimated_tail - exact_tail|.
        n_draws is the sample size, stored as a float for the dict type.

    Notes
    -----
    Monte Carlo estimates a probability by the relative frequency in a
    simulated sample. draws > CUT is a boolean array (True/False).
    np.mean treats True as 1 and False as 0, so the mean of that mask
    is exactly (number of draws > 16) / n. That is the estimator of
    P(X > 16). With 100,000 seeded draws the error should be small,
    not zero: simulation noise is expected.
    """
    # Boolean mean = sample proportion. This is the Monte Carlo tail.
    estimated_tail = float(np.mean(draws > CUT))
    return {
        "estimated_tail": estimated_tail,
        "sample_mean": float(np.mean(draws)),
        "abs_error": abs(estimated_tail - exact_tail),
        "n_draws": float(len(draws)),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(draws: np.ndarray, model) -> Path:
    """Compare the Monte Carlo histogram with the exact flat density.

    Parameters
    ----------
    draws:
        Seed-42 Uniform(8, 20) sample of length N_DRAWS.
    model:
        Frozen Uniform(8, 20) whose pdf is the navy overlay.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    density=True scales the histogram so its area is 1, matching the
    pdf overlay. If Uniform(8, 20) is the right model, the bars should
    hug the flat height 1/12 and the dashed line at 16 should leave
    about one third of the mass to its right.
    """
    output_path = DIR_FIGURES / "uniform_mc_02_monte_carlo.png"
    x = np.linspace(A, B, 200)
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # bins=30 is a display choice, not a statistical parameter. edgecolor
    # outlines each bar so the flat target remains readable.
    ax.hist(
        draws,
        bins=30,
        density=True,
        color="#5B8DEF",
        alpha=0.55,
        edgecolor="#1A2E51",
        label="Seed-42 histogram",
    )
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Exact Uniform(8, 20)")
    ax.axvline(CUT, color="#EC2661", ls="--", lw=1.4, label="x = 16")
    ax.set_xlabel("Processing time (minutes)")
    ax.set_ylabel("Density")
    ax.set_title("100,000 Draws Recover the Flat Uniform Density")
    ax.set_xlim(A, B)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 Monte Carlo check and write the histogram figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    model = uniform_model()
    # Exact tail and mean from Step 1, rebuilt here from the same model.
    exact_tail = float(1.0 - model.cdf(CUT))
    exact_mean = float(model.mean())
    draws = draw_processing_times(model)
    mc = monte_carlo_tail(draws, exact_tail)
    figure_path = save_figure(draws, model)

    print("================================================================")
    print("LESSON 20 - STEP 2: MONTE CARLO")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Monte Carlo draws               : {int(mc['n_draws']):,}")
    print(f"P(X > 16) exact                 : {exact_tail:.6f}")
    print(f"P(X > 16) Monte Carlo           : {mc['estimated_tail']:.6f}")
    print(f"Absolute error                  : {mc['abs_error']:.6f}")
    print(f"Mean exact                      : {exact_mean:.6f}")
    print(f"Mean Monte Carlo                : {mc['sample_mean']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom.
if __name__ == "__main__":
    main()

