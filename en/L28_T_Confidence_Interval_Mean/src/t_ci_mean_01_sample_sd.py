"""
Lesson 28 - Step 1: Sample Standard Deviation When Sigma Is Unknown
===================================================================
NEW IN THIS STEP: generate_fill_sample(), sample_sd_metrics(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. generate_fill_sample()   n iid fills; the analyst sees the sample, not sigma
    2. sample_sd_metrics()      xbar, s with ddof=1, se_hat = s/sqrt(n), df = n-1
    3. save_figure()            histogram with xbar and the estimated SE band

Context:
The same fully synthetic filling line is observed, but now the population
standard deviation is unknown. A seed-42 sample of n = 36 bottles yields
xbar and s. The estimated standard error is s / sqrt(n), and the sampling
distribution of (xbar - mu) / (s / sqrt(n)) is Student t with df = n - 1.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. Lesson 27 formed a z interval with a
known sigma. This script replaces that known scale by the sample standard
deviation s and names the t degrees of freedom.

    np.std(x, ddof=1)    sample s, divisor n-1 (NumPy defaults to ddof=0)
    s / sqrt(n)          estimated SE of xbar when sigma is unknown
    df = n - 1           t parameter: one df was spent on xbar
    Student t            (xbar - mu) / (s/sqrt(n)) ~ t_{n-1}, not N(0, 1)
    dict[str, float]     a type hint: string keys, float values

main() reports n, df, the hidden sigma used only to generate the fills,
xbar, s, and s/sqrt(n), then writes the histogram. No earlier lesson
script is imported.

Run it:
    uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_01_sample_sd.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the fill sample and computes
# xbar and s. scipy.stats.t arrives in Step 2; this file only prepares s.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. The same seed rebuilds the Lesson 27
# filling-line sample so the only modeling change is that sigma is hidden.
SEED = 42
# Sample size. df = n - 1 = 35 will parameterize the t distribution in
# Step 2; it is not a second sample size.
N = 36
# True process scale used only by the generator. The analyst does not
# receive this number and must estimate scale from the sample.
SIGMA_TRUE = 10.0
# True mean fill, also hidden from the analyst. Lesson 27 estimated it
# with a z interval; Lesson 28 estimates it with a t interval.
MU_TRUE = 502.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) generate_fill_sample() ------------------------------------------
def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Draw n iid fills. The analyst observes the sample, not sigma.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's generator so Steps 2 and 3 rebuild
        the same 36 fills. Default is the module-level SEED = 42.

    Returns
    -------
    np.ndarray
        Length-n vector of milliliters from N(MU_TRUE, SIGMA_TRUE).
        Nothing is read from disk; every value is generated in memory.

    Notes
    -----
    iid means independent and identically distributed: each bottle is
    drawn from the same Normal, and the draws do not affect each other.
    loc= is the mean and scale= is the standard deviation, not the
    variance. The generator uses SIGMA_TRUE, but later functions never
    plug that constant into a standard error: that is the Lesson 27 to
    Lesson 28 change.
    """
    # default_rng(seed) returns a Generator. All draws in this function
    # go through rng so they form one reproducible stream.
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)
# ------------------------------------------------------------------------------


# --- NEW (2) sample_sd_metrics() ---------------------------------------------
def sample_sd_metrics(sample: np.ndarray) -> dict[str, float]:
    """Return xbar, s, estimated SE, and degrees of freedom.

    Parameters
    ----------
    sample:
        The n fill volumes from generate_fill_sample().

    Returns
    -------
    dict[str, float]
        n, df = n-1, xbar, s, se_hat = s/sqrt(n), and hidden_sigma.
        hidden_sigma is printed for the lesson; it is not used to form
        an interval. dict[str, float] is a type hint, not a run-time check.

    Notes
    -----
    Lesson 03 introduced s with divisor n-1. NumPy's np.std defaults to
    ddof=0 (divisor n, a population formula). Passing ddof=1 selects the
    sample formula:

        s^2 = sum_i (x_i - xbar)^2 / (n - 1)

    The n-1 in the divisor is the same n-1 that becomes the t degrees of
    freedom: xbar used one linear constraint on the residuals, so s is
    built from n-1 free pieces of information.

    Lesson 27 used SE = sigma / sqrt(n) with a known sigma. Here the
    estimated SE is s / sqrt(n). Replacing sigma by s is why the pivot
    (xbar - mu) / (s/sqrt(n)) follows Student t_{n-1} rather than N(0, 1).
    Step 2 turns that pivot into a t critical value.
    """
    xbar = float(np.mean(sample))
    # ddof=1: sample s, divisor n-1. Do not omit it; np.std would then
    # divide by n and understate the scale.
    s = float(np.std(sample, ddof=1))
    # Estimated standard error of xbar. The hat on SE marks that s, not
    # the hidden SIGMA_TRUE, sits in the numerator.
    se_hat = s / np.sqrt(N)
    return {
        "n": float(N),
        # df is a t-distribution parameter, not a count of bottles.
        "df": float(N - 1),
        "xbar": xbar,
        "s": s,
        "se_hat": float(se_hat),
        "hidden_sigma": SIGMA_TRUE,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Save a histogram with xbar and the estimated SE band from s.

    Parameters
    ----------
    sample:
        The n fill volumes plotted as the histogram.
    metrics:
        Dictionary from sample_sd_metrics() supplying xbar and se_hat.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    The red line is the sample mean. The blue band is one estimated SE
    on each side of xbar, s/sqrt(n), not a confidence interval. The
    95% t interval in Step 2 is wider: it multiplies se_hat by t* > 1.
    """
    output_path = DIR_FIGURES / "t_ci_mean_01_sample_sd.png"
    # figsize is width x height in inches. Drawing methods live on ax.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")
    ax.axvline(
        metrics["xbar"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Sample mean = {metrics['xbar']:.2f} ml",
    )
    # axvspan shades a horizontal interval. This is the estimated SE
    # band from s, not the t interval of Step 2.
    ax.axvspan(
        metrics["xbar"] - metrics["se_hat"],
        metrics["xbar"] + metrics["se_hat"],
        color="#5B8DEF",
        alpha=0.22,
        label=f"s / sqrt(n) = {metrics['se_hat']:.4f} ml",
    )
    ax.set_xlabel("Fill volume (ml)")
    ax.set_ylabel("Count of bottles")
    ax.set_title("Unknown Sigma: Estimated Standard Error from s")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 sample-sd report and write the histogram.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    sample = generate_fill_sample()
    metrics = sample_sd_metrics(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LESSON 28 - STEP 1: SAMPLE STANDARD DEVIATION")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Sample size n                   : {N}")
    # int(...) drops the .0 from the float stored in the metrics dict.
    # df = 35 is the t parameter used by scipy.stats.t in Step 2.
    print(f"Degrees of freedom n-1          : {int(metrics['df'])}")
    # Printed so students can compare s with the generator; the analyst
    # who only sees the sample does not know this value.
    print(f"Hidden sigma (ml)               : {metrics['hidden_sigma']:.6f}")
    print(f"Sample mean xbar (ml)           : {metrics['xbar']:.6f}")
    print(f"Sample standard deviation s     : {metrics['s']:.6f}")
    print(f"Estimated SE s/sqrt(n)          : {metrics['se_hat']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

