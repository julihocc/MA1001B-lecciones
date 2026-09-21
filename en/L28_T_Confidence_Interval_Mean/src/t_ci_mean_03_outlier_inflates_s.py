"""
Lesson 28 - Step 3: One Extreme Outlier Inflates s and the Interval
===================================================================
THE RECIPE
Start from t_ci_mean_02_t_interval.py, then introduce:
    1. contaminate_one_fill()     replace one observation by an extreme outlier
    2. compare_clean_vs_outlier() t intervals before and after the outlier
    3. save_figure()              show how s and the interval width inflate

Limit: a single extreme fill inflates s, so the t interval becomes much
wider. The t procedure is valid under approximate normality; one outlier
is enough to distort the estimated scale.

How to read this file:
You already know Python through OOP. Steps 1-2 computed s, df = n-1, t*
from scipy.stats.t.ppf, and xbar +/- t* * s/sqrt(n). Lesson 01 covers
pathlib and unattended savefig. This script copies those t calculations
and comments only the NEW bands.

    contaminate last fill     one 560 ml value replaces sample[-1]
    s after the outlier       ddof=1 still, but one residual dominates
    df stays n-1              n is unchanged, so t* from t.ppf is the same
    wider interval            se_hat = s/sqrt(n) grows with s, not with t*
    approximate normality     the t interval assumes the fills are roughly Normal

main() reprints the clean t interval, then the contaminated s, endpoints,
and width inflation.

Run it:
    uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_03_outlier_inflates_s.py
"""

# Same Lesson 01 path idiom: figures/ next to this package, not cwd.
from pathlib import Path

import matplotlib
import numpy as np
# stats.t.ppf is reused from Step 2: t* = t.ppf(1 - alpha/2, df) with
# df = n-1. The outlier does not change n, so it does not change t*.
from scipy import stats

# Agg before pyplot, as in Lesson 01: draw to a file, never a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Identical filling-line constants to Steps 1-2. SEED rebuilds the same
# clean sample before the last fill is replaced.
SEED = 42
N = 36
SIGMA_TRUE = 10.0
MU_TRUE = 502.0
# Extreme milliliters written over sample[-1]. About six hidden-sigma
# units above MU_TRUE, so it inflates s far more than it shifts xbar.
OUTLIER_VALUE = 560.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills. The analyst observes the sample, not sigma.

    Rebuilt from Step 1 so this file does not import that script.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


def t_interval_from_sample(sample: np.ndarray) -> dict[str, float]:
    """Compute s, t*, and the 95% t interval from one sample.

    Parameters
    ----------
    sample:
        Either the clean fills or the contaminated copy. n is taken
        from sample.size so both calls share one function.

    Returns
    -------
    dict[str, float]
        n, df, xbar, s, se_hat, t_star, lower, upper, and width.

    Notes
    -----
    Same arithmetic as Step 2, applied twice. df = n-1 still parameterizes
    scipy.stats.t. t* = stats.t.ppf(1 - alpha/2, df) therefore matches
    Step 2 for both the clean and the dirty sample: n does not change,
    so the critical value does not change.

    What does change is s. ddof=1 keeps the sample divisor n-1, but one
    huge residual (560 - xbar)^2 dominates the sum of squares, so s and
    se_hat = s/sqrt(n) jump. The interval xbar +/- t* * se_hat widens
    because the estimated scale inflated, not because t* moved.
    """
    n = sample.size
    # t degrees of freedom: one df spent on xbar. Equal to 35 for both
    # samples because contamination does not add or drop a bottle.
    df = n - 1
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    se_hat = s / np.sqrt(n)
    # Same two-sided 0.975 quantile of t_df as Step 2.
    t_star = float(stats.t.ppf(1.0 - (1.0 - CONFIDENCE) / 2.0, df))
    margin = t_star * se_hat
    return {
        "n": float(n),
        "df": float(df),
        "xbar": xbar,
        "s": s,
        "se_hat": float(se_hat),
        "t_star": t_star,
        "lower": xbar - margin,
        "upper": xbar + margin,
        "width": 2.0 * margin,
    }


# --- NEW (1) contaminate_one_fill() ------------------------------------------
def contaminate_one_fill(sample: np.ndarray) -> np.ndarray:
    """Replace the last observation with one extreme 560 ml fill.

    Parameters
    ----------
    sample:
        Clean fills from generate_fill_sample(). Not modified in place.

    Returns
    -------
    np.ndarray
        A copy whose last entry is OUTLIER_VALUE. Length remains n, so
        df = n-1 and t* stay exactly the Step 2 values.

    Notes
    -----
    np.array(..., copy=True) builds a new buffer. Writing 560 into the
    last slot of that copy leaves the original sample available for the
    clean t interval. Replacing one point is enough to break the Normal
    scale estimate that the t procedure relies on.
    """
    contaminated = np.array(sample, copy=True)
    contaminated[-1] = OUTLIER_VALUE
    return contaminated
# ------------------------------------------------------------------------------


# --- NEW (2) compare_clean_vs_outlier() --------------------------------------
def compare_clean_vs_outlier(
    clean: dict[str, float],
    dirty: dict[str, float],
) -> dict[str, float]:
    """Measure how one outlier inflates s and the t-interval width.

    Parameters
    ----------
    clean, dirty:
        Dictionaries from t_interval_from_sample() on the original
        sample and on the contaminated copy.

    Returns
    -------
    dict[str, float]
        s_inflation (dirty s minus clean s), width_inflation (dirty
        width minus clean width), and xbar_shift.

    Notes
    -----
    The mean moves by only (560 - last fill) / n, a 1/n shift. s moves
    much more because squared residuals feed the sample variance. The
    t interval inherits that scale jump through se_hat. Matching t*
    values on the two rows of the figure are the point: df did not
    change, the estimated scale did.
    """
    return {
        "s_inflation": dirty["s"] - clean["s"],
        "width_inflation": dirty["width"] - clean["width"],
        "xbar_shift": dirty["xbar"] - clean["xbar"],
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    clean: dict[str, float],
    dirty: dict[str, float],
) -> Path:
    """Contrast the clean t interval with the outlier-inflated interval.

    Parameters
    ----------
    clean, dirty:
        t-interval summaries before and after replacing one fill.

    Returns
    -------
    Path
        Absolute path of the PNG. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Two error bars share the hidden-mu reference line. xerr is 2 x 2:
    row 0 is the left-arm lengths (xbar - lower), row 1 is the right-arm
    lengths (upper - xbar). The dirty interval is wider because s grew,
    even though both intervals use the same t* from stats.t.ppf.
    """
    output_path = DIR_FIGURES / "t_ci_mean_03_outlier_inflates_s.png"
    labels = ["Clean sample\nt interval", "One 560 ml outlier\nt interval"]
    centers = [clean["xbar"], dirty["xbar"]]
    # Shape (2, n_series): first row subtracts from the center, second
    # row adds to the center. errorbar then draws asymmetric caps.
    xerr = np.array(
        [
            [clean["xbar"] - clean["lower"], dirty["xbar"] - dirty["lower"]],
            [clean["upper"] - clean["xbar"], dirty["upper"] - dirty["xbar"]],
        ]
    )
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        centers,
        [1.0, 0.0],
        xerr=xerr,
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=2.8,
        capsize=8,
        markersize=8,
    )
    ax.axvline(MU_TRUE, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"True mu = {MU_TRUE:.1f}")
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(labels)
    ax.set_xlabel("Fill volume (ml)")
    ax.set_title("One Extreme Outlier Inflates s and the t Interval")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_ylim(-0.7, 1.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 3 outlier comparison and write the two-interval figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    clean = t_interval_from_sample(sample)
    dirty_sample = contaminate_one_fill(sample)
    dirty = t_interval_from_sample(dirty_sample)
    comparison = compare_clean_vs_outlier(clean, dirty)
    figure_path = save_figure(clean, dirty)

    print("================================================================")
    print("LESSON 28 - STEP 3: OUTLIER INFLATES S")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    print(f"Outlier replacement (ml)        : {OUTLIER_VALUE:.6f}")
    print(f"Clean xbar (ml)                 : {clean['xbar']:.6f}")
    print(f"Clean s (ml)                    : {clean['s']:.6f}")
    # Same stats.t.ppf(0.975, 35) as Step 2; contamination does not
    # change df, so t* is reused rather than recomputed from a new n.
    print(f"Clean t-star                    : {clean['t_star']:.6f}")
    print(f"Clean lower bound               : {clean['lower']:.6f}")
    print(f"Clean upper bound               : {clean['upper']:.6f}")
    print(f"Clean width                     : {clean['width']:.6f}")
    print(f"Outlier xbar (ml)               : {dirty['xbar']:.6f}")
    print(f"Outlier s (ml)                  : {dirty['s']:.6f}")
    print(f"Outlier lower bound             : {dirty['lower']:.6f}")
    print(f"Outlier upper bound             : {dirty['upper']:.6f}")
    print(f"Outlier width                   : {dirty['width']:.6f}")
    print(f"s inflation                     : {comparison['s_inflation']:.6f}")
    print(f"xbar shift                      : {comparison['xbar_shift']:.6f}")
    print(f"Width inflation                 : {comparison['width_inflation']:.6f}")
    print("Limit                          : one outlier inflates s and the CI")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

