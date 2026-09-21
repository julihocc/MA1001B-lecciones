"""
Lesson 27 - Step 2: Z Confidence Interval with Known Sigma
==========================================================
THE RECIPE
Start from z_ci_mean_01_sample_standard_error.py, then introduce:
    1. z_critical()             z* = 1.96 for a 95 percent interval
    2. z_confidence_interval()  xbar +/- z* * sigma / sqrt(n)
    3. save_figure()            draw the interval around the sample mean

The same n = 36 synthetic fills are rebuilt with SEED = 42. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 drew the n = 36 fills and
computed SE = sigma / sqrt(n). Lesson 01 covers pathlib and unattended
savefig; they are rebuilt here only so the script stays self-contained.
Lesson 21 used scipy.stats.norm.cdf; this step uses the inverse, ppf.

    z* = 1.96                     textbook two-sided 95% critical value
    alpha = 1 - confidence        two-tail probability; 0.05 for 95%
    stats.norm.ppf(1 - alpha/2)   standard-normal quantile at 0.975
    xbar +/- z* * SE              the z interval when sigma is known
    ax.errorbar                   draw the interval around xbar

main() prints textbook z* = 1.96, the scipy.stats.norm.ppf confirmation,
the margin 3.266667, and the interval [499.471831, 506.005165]. Coverage
of the hidden mu is a check in this seed-42 sample, not a probability
about this one realized interval.

Run it:
    uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_02_z_interval.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.norm.ppf is the standard-normal quantile function (inverse CDF).
# Lesson 21 used cdf to read P(Z <= z); ppf asks which z has that tail.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical filling-line constants to Step 1. The seed is used again so
# xbar matches the Step 1 sample.
SEED = 42
N = 36
SIGMA = 10.0
MU_TRUE = 502.0
# Two-sided 95% interval. alpha = 1 - 0.95 = 0.05 is split across two tails.
CONFIDENCE = 0.95
# Textbook z* for 95%. The interval below uses this 1.96, not the longer
# scipy quantile, so the printed bounds match the OpenStax formula.
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills from N(mu_true, sigma). The analyst does not know mu.

    Rebuilt from Step 1 so this file does not import that script. The
    same seed and N(502, 10) law reproduce the same 36 fills.

    Parameters
    ----------
    seed:
        Generator seed. Default SEED = 42.

    Returns
    -------
    np.ndarray
        Length-n vector of synthetic fill volumes in millilitres.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


def sampling_metrics(sample: np.ndarray) -> dict[str, float]:
    """Return the sample mean and the known-sigma standard error.

    Rebuilt from Step 1. SE = sigma / sqrt(n) still uses the known
    process sigma, not the sample standard deviation.

    Parameters
    ----------
    sample:
        The n = 36 fills from generate_fill_sample().

    Returns
    -------
    dict[str, float]
        n, sigma, xbar, and se = 10 / sqrt(36) = 1.666667.
    """
    xbar = float(np.mean(sample))
    se = SIGMA / np.sqrt(N)
    return {
        "n": float(N),
        "sigma": SIGMA,
        "xbar": xbar,
        "se": float(se),
    }


# --- NEW (1) z_critical() ----------------------------------------------------
def z_critical(confidence: float = CONFIDENCE) -> dict[str, float]:
    """Return the textbook z* = 1.96 and the scipy.stats.norm confirmation.

    Parameters
    ----------
    confidence:
        Two-sided confidence level. Default 0.95.

    Returns
    -------
    dict[str, float]
        confidence, alpha = 1 - confidence, z_star = 1.96, and scipy_z
        from stats.norm.ppf. The interval in this lesson uses z_star.

    Notes
    -----
    For a two-sided 95% interval the remaining 5% is split equally, so
    each tail has probability alpha/2 = 0.025. z* is the standard-normal
    quantile that leaves 0.025 on the right:
        z* = z_{1 - alpha/2} = z_{0.975}.
    scipy.stats.norm.ppf is the inverse of the N(0, 1) CDF: ppf(p) is
    the z with P(Z <= z) = p. So
        stats.norm.ppf(1.0 - alpha / 2.0)
    is ppf(0.975) ≈ 1.959964, which textbooks round to 1.96. The
    interval below uses the rounded Z_STAR so the arithmetic matches
    OpenStax; scipy_z is printed only as a check.
    """
    alpha = 1.0 - confidence
    # Inverse CDF of N(0, 1) at 0.975: the two-sided 95% critical value.
    scipy_z = float(stats.norm.ppf(1.0 - alpha / 2.0))
    return {
        "confidence": confidence,
        "alpha": alpha,
        "z_star": Z_STAR,
        "scipy_z": scipy_z,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) z_confidence_interval() -----------------------------------------
def z_confidence_interval(
    metrics: dict[str, float],
    z_star: float,
) -> dict[str, float]:
    """Build xbar +/- z* * SE when sigma is treated as known.

    Parameters
    ----------
    metrics:
        Dictionary from sampling_metrics() with xbar and se.
    z_star:
        Critical value. This lesson passes the textbook 1.96.

    Returns
    -------
    dict[str, float]
        margin is z* * SE. lower and upper are the interval endpoints.
        width is upper - lower = 2 * margin. covers_true_mu is 1.0 if
        the hidden mu sits inside, else 0.0 (stored as a float so the
        dict stays dict[str, float]).

    Notes
    -----
    The known-sigma z interval is
        xbar +/- z* * sigma / sqrt(n)
    which is the same as xbar +/- z* * SE. For these numbers:
        margin = 1.96 * 1.666667 = 3.266667 ml.
    After the data are seen, the interval either covers mu or it does
    not; 95% is a property of the procedure, not a probability about
    this one realized interval. The interval estimates mu, not the
    fill of the next bottle.
    """
    # Half-width: z* * (sigma / sqrt(n)).
    margin = z_star * metrics["se"]
    # CI formula: [xbar - z* * SE, xbar + z* * SE].
    lower = metrics["xbar"] - margin
    upper = metrics["xbar"] + margin
    return {
        "margin": float(margin),
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
        "covers_true_mu": float(lower <= MU_TRUE <= upper),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    metrics: dict[str, float],
    interval: dict[str, float],
) -> Path:
    """Save a one-sample z interval around the observed mean.

    Parameters
    ----------
    metrics:
        Dictionary from sampling_metrics() with the centre xbar.
    interval:
        Dictionary from z_confidence_interval() with lower and upper.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    errorbar draws a point at xbar and a horizontal bar from lower to
    upper. The dashed line is the hidden mu; it is a teaching overlay,
    not something the analyst observes. The interval is a range for mu,
    not for one bottle.
    """
    output_path = DIR_FIGURES / "z_ci_mean_02_z_interval.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # xerr is [[left error], [right error]]: distances from xbar to the
    # two endpoints, not the endpoints themselves.
    ax.errorbar(
        [metrics["xbar"]],
        [1],
        xerr=[[metrics["xbar"] - interval["lower"]],
              [interval["upper"] - metrics["xbar"]]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.axvline(MU_TRUE, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"True mu = {MU_TRUE:.1f} ml (hidden)")
    ax.set_yticks([1])
    ax.set_yticklabels(["95% z interval"])
    ax.set_xlabel("Fill volume (ml)")
    ax.set_title("Z Interval: xbar +/- 1.96 * sigma / sqrt(n)")
    ax.set_xlim(interval["lower"] - 4, interval["upper"] + 4)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        metrics["xbar"],
        1.18,
        f"[{interval['lower']:.2f}, {interval['upper']:.2f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 2 z-interval report and write the interval figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    metrics = sampling_metrics(sample)
    critical = z_critical()
    # Use textbook z* = 1.96, not scipy's longer quantile.
    interval = z_confidence_interval(metrics, critical["z_star"])
    figure_path = save_figure(metrics, interval)

    print("================================================================")
    print("LESSON 27 - STEP 2: Z CONFIDENCE INTERVAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Known sigma (ml)                : {SIGMA:.6f}")
    print(f"Sample mean xbar (ml)           : {metrics['xbar']:.6f}")
    print(f"Standard error                  : {metrics['se']:.6f}")
    print(f"Confidence level                : {critical['confidence']:.2f}")
    print(f"Textbook z-star                 : {critical['z_star']:.6f}")
    print(f"scipy.stats.norm.ppf z-star     : {critical['scipy_z']:.6f}")
    print(f"Margin of error (ml)            : {interval['margin']:.6f}")
    print(f"Lower bound (ml)                : {interval['lower']:.6f}")
    print(f"Upper bound (ml)                : {interval['upper']:.6f}")
    print(f"Interval width (ml)             : {interval['width']:.6f}")
    print(f"Covers true mu                  : {bool(interval['covers_true_mu'])}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

