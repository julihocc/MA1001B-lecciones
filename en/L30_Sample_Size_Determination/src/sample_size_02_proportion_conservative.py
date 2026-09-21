"""
Lesson 30 - Step 2: Conservative Sample Size for a Proportion
=============================================================
THE RECIPE
Start from sample_size_01_mean_margin.py, then introduce:
    1. proportion_sample_size()  n = z*^2 p(1-p) / E^2
    2. conservative_p()          p = 0.5 maximizes p(1-p)
    3. save_figure()             compare p = 0.5 with other planning values

A 95% interval for a first-contact rate is planned with E = 0.03. Using
p = 0.5 is the conservative choice when the true p is unknown.

How to read this file:
You already know Python through OOP. Step 1 planned n = (z* s / E)^2 for
a mean. Lesson 01 covers pathlib and unattended savefig; they are rebuilt
here only so the script stays self-contained. This step replaces the mean
formula with the proportion sample-size formula.

    n = z*^2 * p * (1-p) / E^2   rearrange E = z* sqrt(p(1-p)/n) for n
    p * (1-p)                    Bernoulli variance; largest at p = 0.5
    np.ceil(raw)                 same round-up rule as Step 1
    ax.bar of planning p         required n across p; magenta at 0.5

main() reports n at p = 0.5 and at the Lesson 29 guess p = 0.18, then
saves the comparison figure. No earlier lesson script is imported.

Run it:
    python sample_size_02_proportion_conservative.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Reserved seed. This script still does not draw random numbers; n is a
# planning formula, not a simulation.
SEED = 42
# Same 95% z* as Step 1. The critical value does not change just because
# the parameter is now a proportion.
Z_STAR = 1.96
# Target margin of error for the first-contact rate: 3 percentage points.
E_PROP = 0.03
# Conservative planning value. p(1-p) = 0.25 is the maximum of that
# parabola on [0, 1], so this p produces the largest n.
P_CONSERVATIVE = 0.5
# A sharper guess, reused from the Lesson 29 first-contact example. It
# is not used as the recommended plan when p is unknown.
P_GUESSED = 0.18
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) proportion_sample_size() ----------------------------------------
def proportion_sample_size(
    z_star: float,
    p_plan: float,
    margin: float,
) -> dict[str, float]:
    """Return raw and rounded-up n = z*^2 p(1-p) / E^2.

    Parameters
    ----------
    z_star:
        Normal critical value for the planned confidence level. The
        lesson uses 1.96 for 95%.
    p_plan:
        Planning value of the population proportion. Not the eventual
        sample proportion.
    margin:
        Target margin of error E on the proportion scale. Here E = 0.03.

    Returns
    -------
    dict[str, float]
        p_plan echoes the input. pq is p(1-p). raw_n is the unrounded
        formula value. n_required is that value rounded up with ceil.

    Notes
    -----
    A 95% proportion interval has half-width
    E = z* sqrt(p(1-p) / n). Squaring both sides and solving for n
    gives n = z*^2 p(1-p) / E^2. The mean formula from Step 1 used a
    planning s; this one uses the Bernoulli variance p(1-p) instead.
    """
    # n = z*^2 * p * (1-p) / E^2. z_star ** 2 is the squared critical
    # value. p_plan * (1.0 - p_plan) is p(1-p). margin ** 2 is E^2 in
    # the denominator. For z*=1.96, p=0.5, E=0.03:
    # 3.8416 * 0.25 / 0.0009 = 1067.111...
    raw = (z_star ** 2) * p_plan * (1.0 - p_plan) / (margin ** 2)
    return {
        "p_plan": p_plan,
        "pq": p_plan * (1.0 - p_plan),
        "raw_n": float(raw),
        # Same ceil-then-int round-up as Step 1's round_up_n(); inlined
        # here so this file does not import that step.
        "n_required": int(np.ceil(raw)),
    }
# ------------------------------------------------------------------------------


# --- NEW (2) conservative_p() ------------------------------------------------
def conservative_p() -> dict[str, float]:
    """Show that p = 0.5 yields the largest p(1-p) and therefore the largest n.

    Returns
    -------
    dict[str, float]
        guessed_p / guessed_n use P_GUESSED = 0.18. conservative_p /
        conservative_n use p = 0.5. extra_observations is how many
        more rows the conservative plan requires.

    Notes
    -----
    f(p) = p(1-p) = p - p^2 is a downward parabola. Its vertex is at
    p = 0.5, where f(0.5) = 0.25. Any other planning p, including 0.18
    and 0.70, gives a smaller product and a smaller n. Using p = 0.5
    when the true p is unknown is therefore the conservative choice:
    the resulting n is large enough for every p.
    """
    guessed = proportion_sample_size(Z_STAR, P_GUESSED, E_PROP)
    conservative = proportion_sample_size(Z_STAR, P_CONSERVATIVE, E_PROP)
    return {
        "guessed_p": P_GUESSED,
        "guessed_n": float(guessed["n_required"]),
        "conservative_p": P_CONSERVATIVE,
        "conservative_n": float(conservative["n_required"]),
        # 1068 - 631 = 437 extra observations if we refuse to guess p.
        "extra_observations": float(
            conservative["n_required"] - guessed["n_required"]
        ),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure() -> Path:
    """Compare required n across planning values of p.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The five bars reuse n = z*^2 p(1-p) / E^2 at E = 0.03. The curve
    p(1-p) is symmetric about 0.5, so p = 0.30 and p = 0.70 are not
    equally far from 0.5 in n: 0.70 is the mirror of 0.30. Magenta
    marks the conservative peak at p = 0.5.
    """
    output_path = DIR_FIGURES / "sample_size_02_proportion_conservative.png"
    # Include the Lesson 29 guess 0.18 and the conservative 0.50.
    p_values = np.array([0.10, 0.18, 0.30, 0.50, 0.70])
    # Vector form of n = z*^2 p(1-p) / E^2, then ceil. p_values *
    # (1.0 - p_values) is the Bernoulli variance at each planning p.
    ns = np.ceil((Z_STAR ** 2) * p_values * (1.0 - p_values) / (E_PROP ** 2))
    # abs(p - 0.5) < 1e-9 is a float-safe test for p == 0.5.
    colors = ["#EC2661" if abs(p - 0.5) < 1e-9 else "#5B8DEF" for p in p_values]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar([f"{p:.2f}" for p in p_values], ns, color=colors, width=0.62)
    ax.set_xlabel("Planning value of p")
    ax.set_ylabel("Required sample size n")
    ax.set_title("Proportion Sample Size: p = 0.5 Is Conservative")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, ns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 15,
            f"{int(value)}",
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
    """Run the Step 2 conservative-p report and write the p-versus-n figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    conservative = proportion_sample_size(Z_STAR, P_CONSERVATIVE, E_PROP)
    guessed = proportion_sample_size(Z_STAR, P_GUESSED, E_PROP)
    contrast = conservative_p()
    figure_path = save_figure()

    print("================================================================")
    print("LESSON 30 - STEP 2: CONSERVATIVE PROPORTION SAMPLE SIZE")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed (reserved)          : {SEED}")
    print(f"Textbook z-star                 : {Z_STAR:.6f}")
    print(f"Target margin E                 : {E_PROP:.6f}")
    print(f"Conservative p                  : {conservative['p_plan']:.6f}")
    # p(1-p) at 0.5 is exactly 0.25, the peak of that product.
    print(f"Conservative p(1-p)             : {conservative['pq']:.6f}")
    print(f"Conservative raw n              : {conservative['raw_n']:.6f}")
    print(f"Conservative rounded-up n       : {conservative['n_required']}")
    print(f"Guessed p from Lesson 29        : {guessed['p_plan']:.6f}")
    print(f"Guessed rounded-up n            : {guessed['n_required']}")
    print(f"Extra observations at p=0.5     : {int(contrast['extra_observations'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

