"""
Lesson 28 - Step 2: Student t Interval with Unknown Sigma
=========================================================
THE RECIPE
Start from t_ci_mean_01_sample_sd.py, then introduce:
    1. t_critical()             t* from scipy.stats.t.ppf with df = n - 1
    2. t_confidence_interval()  xbar +/- t* * s / sqrt(n)
    3. save_figure()            draw the t interval and compare t* with 1.96

The same n = 36 synthetic fills are rebuilt with SEED = 42. No earlier
lesson script is imported.

How to read this file:
You already know Python through OOP. Step 1 computed s, s/sqrt(n), and
df = n-1. Lesson 01 covers pathlib and unattended savefig; they are
rebuilt here only so the script stays self-contained. This step reads the
t critical value from scipy.stats.t and forms the 95% interval.

    stats.t                  Student-t family (pdf, cdf, ppf) in scipy.stats
    stats.t.ppf(q, df)       t quantile: value t* with P(T <= t*) = q
    df = n - 1               35 here; the second argument of t.ppf
    t* = t.ppf(1-alpha/2, df) two-sided critical value; 0.975 for 95%
    t* vs z* = 1.96          t tails are heavier, so t* > z* at finite df
    xbar +/- t* * s/sqrt(n)  the t interval when sigma is unknown

main() prints t*, the 1.96 contrast, the margin, and [lower, upper], then
saves the interval figure.

Run it:
    uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_02_t_interval.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# scipy.stats is the distribution library. stats.t is the Student-t
# family: pdf, cdf, and ppf (quantiles) for T ~ t_df. Lesson 27 used
# stats.norm.ppf for z*; this lesson switches the family to t.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical filling-line constants to Step 1. The same seed rebuilds the
# same 36 fills so the only new arithmetic is t* and the interval.
SEED = 42
N = 36
SIGMA_TRUE = 10.0
MU_TRUE = 502.0
# Two-sided coverage. alpha = 1 - 0.95 = 0.05, so each tail holds 0.025
# and the critical quantile is 1 - alpha/2 = 0.975.
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills. The analyst observes the sample, not sigma.

    Rebuilt from Step 1 so this file does not import that script. loc=
    is the hidden mean and scale= is the hidden SIGMA_TRUE. Later
    functions estimate scale from the sample and never plug SIGMA_TRUE
    into the interval.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


def sample_sd_metrics(sample: np.ndarray) -> dict[str, float]:
    """Return xbar, s, estimated SE, and degrees of freedom.

    Same packaging as Step 1. ddof=1 selects the sample s (divisor n-1).
    se_hat = s/sqrt(n) is the estimated standard error of xbar.
    df = n-1 is the t parameter passed to stats.t.ppf in t_critical().
    """
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    se_hat = s / np.sqrt(N)
    return {
        "n": float(N),
        "df": float(N - 1),
        "xbar": xbar,
        "s": s,
        "se_hat": float(se_hat),
    }


# --- NEW (1) t_critical() ----------------------------------------------------
def t_critical(df: float, confidence: float = CONFIDENCE) -> dict[str, float]:
    """Return t* = t.ppf(1 - alpha/2, df) and the z* = 1.96 contrast.

    Parameters
    ----------
    df:
        Degrees of freedom of the t distribution, n-1 = 35 in this
        lesson. scipy.stats.t.ppf expects this as its second argument.
    confidence:
        Two-sided coverage, default 0.95. Then alpha = 0.05.

    Returns
    -------
    dict[str, float]
        confidence, alpha, df, t_star from stats.t.ppf, the textbook
        z_star = 1.96, and t_minus_z = t* - 1.96.

    Notes
    -----
    Let T ~ t_df. The percent-point function ppf is the inverse CDF:
        stats.t.ppf(q, df) = the number t* such that P(T <= t*) = q.

    A two-sided 95% interval leaves alpha/2 = 0.025 in each tail, so
    q = 1 - alpha/2 = 0.975. That is the same 0.975 that Lesson 27
    passed to stats.norm.ppf; only the family changed from Normal to t.

    t* > 1.96 at finite df because a t curve has heavier tails than
    N(0, 1). The extra width pays for using s in place of sigma. As
    df -> infinity, t_df converges to Normal and t* falls toward 1.96.
    With df = 35 the gap is already small, but it is not zero.

    float(...) unwraps SciPy's NumPy scalar into a Python float for
    printing. The df argument must travel with t*: a t quantile without
    its degrees of freedom is incomplete.
    """
    alpha = 1.0 - confidence
    # 1.0 - alpha/2 is 0.975 for 95%. df is the t parameter, not n.
    t_star = float(stats.t.ppf(1.0 - alpha / 2.0, df))
    return {
        "confidence": confidence,
        "alpha": alpha,
        "df": df,
        "t_star": t_star,
        "z_star": 1.96,
        "t_minus_z": t_star - 1.96,
    }
# ------------------------------------------------------------------------------


# --- NEW (2) t_confidence_interval() -----------------------------------------
def t_confidence_interval(
    metrics: dict[str, float],
    t_star: float,
) -> dict[str, float]:
    """Build xbar +/- t* * s / sqrt(n) when sigma is unknown.

    Parameters
    ----------
    metrics:
        Dictionary from sample_sd_metrics() with xbar and se_hat.
    t_star:
        Critical value from t_critical(), stats.t.ppf(0.975, df=35).

    Returns
    -------
    dict[str, float]
        margin, lower, upper, width, and covers_true_mu as 1.0 or 0.0.
        covers_true_mu is a teaching check against the hidden MU_TRUE;
        an analyst who only sees the sample cannot compute it.

    Notes
    -----
    The t interval is the Lesson 27 z formula with two substitutions:
        z* -> t*   (from stats.t.ppf, not 1.96)
        sigma -> s (already inside se_hat = s/sqrt(n))

    Covering mu on this seed-42 sample does not prove the procedure
    always covers. 95% coverage is a long-run property of the random
    interval, not a probability statement about this one realized pair
    of endpoints.
    """
    # Margin of error: t* times the estimated SE, not 1.96 * sigma/sqrt(n).
    margin = t_star * metrics["se_hat"]
    lower = metrics["xbar"] - margin
    upper = metrics["xbar"] + margin
    return {
        "margin": float(margin),
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
        # Stored as 1.0/0.0 so the return type stays dict[str, float].
        "covers_true_mu": float(lower <= MU_TRUE <= upper),
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    metrics: dict[str, float],
    critical: dict[str, float],
    interval: dict[str, float],
) -> Path:
    """Save the t interval and annotate t* versus z*.

    Parameters
    ----------
    metrics:
        xbar and related sample summaries from sample_sd_metrics().
    critical:
        t_star and df from t_critical(); t* is written on the figure.
    interval:
        lower and upper endpoints from t_confidence_interval().

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    ax.errorbar draws a point at xbar and horizontal caps at the t
    endpoints. xerr is a 2 x 1 array: distance from xbar down to lower,
    then from xbar up to upper. The dashed line is the hidden mu, drawn
    only because this is a synthetic lesson.
    """
    output_path = DIR_FIGURES / "t_ci_mean_02_t_interval.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # xerr rows are (left error, right error). One interval, so each
    # row is a one-element list.
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
    ax.set_yticklabels(["95% t interval"])
    ax.set_xlabel("Fill volume (ml)")
    # df = 35 is n-1; it is the argument that was passed to t.ppf.
    ax.set_title("t Interval: xbar +/- t* * s / sqrt(n), df = 35")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        metrics["xbar"],
        1.18,
        f"t* = {critical['t_star']:.3f}  |  "
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
    """Run the Step 2 t-interval report and write the figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    metrics = sample_sd_metrics(sample)
    # metrics["df"] is 35.0; t_critical forwards it to stats.t.ppf.
    critical = t_critical(metrics["df"])
    interval = t_confidence_interval(metrics, critical["t_star"])
    figure_path = save_figure(metrics, critical, interval)

    print("================================================================")
    print("LESSON 28 - STEP 2: STUDENT T INTERVAL")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    # Same n-1 that parameterized stats.t.ppf.
    print(f"Degrees of freedom              : {int(critical['df'])}")
    print(f"Sample mean xbar (ml)           : {metrics['xbar']:.6f}")
    print(f"Sample standard deviation s     : {metrics['s']:.6f}")
    print(f"Estimated SE                    : {metrics['se_hat']:.6f}")
    print(f"Confidence level                : {critical['confidence']:.2f}")
    # t* = stats.t.ppf(0.975, df=35), larger than z* = 1.96.
    print(f"t-star (scipy t.ppf)            : {critical['t_star']:.6f}")
    print(f"z-star contrast                 : {critical['z_star']:.6f}")
    print(f"t-star minus z-star             : {critical['t_minus_z']:.6f}")
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

