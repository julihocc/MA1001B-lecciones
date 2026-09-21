"""
Lesson 32 - Step 1: Sample Variances from Two Independent Groups
================================================================
NEW IN THIS STEP: generate_two_stations(), sample_variances(), and
save_figure().

THE RECIPE
Build the first complete program in this order:
    1. generate_two_stations()  independent Normal(40, 8) and Normal(40, 5)
    2. sample_variances()       s1^2, s2^2 with divisor n-1, plus df1, df2
    3. save_figure()            side-by-side boxplots of the two samples

Context:
Two fully synthetic packing stations are sampled independently. Station A
has n1 = 25 cycles and Station B has n2 = 25 cycles. Each sample variance
estimates that station's population variance.

How to read this file:
You already know Python through object-oriented programming: functions,
classes, lists, dictionaries, loops, and conditionals. Lesson 01 introduced
pathlib.Path, the Agg backend, and unattended fig.savefig; those idioms are
reused here without being re-taught. This script draws two independent
normal samples and reports their sample variances. The F ratio
F = s1^2 / s2^2 and scipy.stats.f wait until Step 2.

    np.random.default_rng(SEED)  seeded Generator; 42 is course-wide
    rng.normal(loc, scale, size) draws from Normal(mean, sd); scale is sd
    np.var(x, ddof=1)            sample variance s^2, divisor n-1 not n
    df = n - 1                   degrees of freedom for one sample variance
    hidden sigma^2               generating variance; the analyst does not
                                 observe it

main() rebuilds the two stations, prints s1^2, s2^2, and (df1, df2), and
writes the boxplot figure. No earlier lesson script is imported.

Run it:
    python f_two_var_01_sample_variances.py
"""

# Path construction is the Lesson 01 idiom: locate figures/ from __file__,
# not from the shell's current working directory. See L01 for pathlib.
from pathlib import Path

# matplotlib draws the PNG. numpy builds the station samples and sample
# variances. The aliases are the same ones used from Lesson 01 onward.
import matplotlib
import numpy as np

# Agg renders to a file and never opens a window. Select it before pyplot,
# exactly as in Lesson 01.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 42 is the course-wide default. The same integer rebuilds the same two
# station samples in Steps 2 and 3 of this lesson.
SEED = 42
# Sample sizes. Equal n is convenient, not required: F allows n1 != n2.
N1 = 25
N2 = 25
# Shared mean of the two synthetic packing clocks. F compares variances,
# not means, so a common mu keeps the contrast on spread.
MU = 40.0
# Station A population sd. scale= in rng.normal, not the variance.
SIGMA1 = 8.0
# Station B population sd. Smaller than SIGMA1, so s1^2 will tend to
# exceed s2^2. The analyst does not see these values.
SIGMA2 = 5.0
# Same figures/ path as Lesson 01: this file's folder -> lesson folder ->
# figures/. mkdir is a no-op when the folder already exists.
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figures"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NEW (1) generate_two_stations() -----------------------------------------
def generate_two_stations(seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """Draw independent normal samples from two packing stations.

    Parameters
    ----------
    seed:
        Integer forwarded to NumPy's generator so Steps 2 and 3 rebuild
        the same two samples. Default is the module-level SEED = 42.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        station_a has n1 = 25 draws from Normal(40, 8). station_b has
        n2 = 25 draws from Normal(40, 5). The two arrays are independent
        because they come from successive calls on one Generator.

    Notes
    -----
    loc is the mean and scale is the standard deviation, not the
    variance. Station A therefore has hidden sigma1^2 = 64 and Station B
    has hidden sigma2^2 = 25. Independence of the two samples is an
    assumption of the two-variance F procedure in Step 2.
    """
    # default_rng(seed) returns a Generator. Do not mix this with the
    # older np.random.seed() global state.
    rng = np.random.default_rng(seed)
    station_a = rng.normal(loc=MU, scale=SIGMA1, size=N1)
    station_b = rng.normal(loc=MU, scale=SIGMA2, size=N2)
    return station_a, station_b
# ------------------------------------------------------------------------------


# --- NEW (2) sample_variances() ----------------------------------------------
def sample_variances(
    station_a: np.ndarray,
    station_b: np.ndarray,
) -> dict[str, float]:
    """Return s1^2, s2^2, and the two degrees of freedom.

    Parameters
    ----------
    station_a:
        n1 cycle times from generate_two_stations().
    station_b:
        n2 cycle times from generate_two_stations().

    Returns
    -------
    dict[str, float]
        n1, n2, df1 = n1-1, df2 = n2-1, the two sample variances s1_sq
        and s2_sq, and the hidden population variances used to generate
        the data. All values are plain Python floats for printing.

    Notes
    -----
    np.var(..., ddof=1) is the sample variance with divisor n-1. NumPy's
    default ddof=0 would divide by n and is the wrong convention here.
    Each sample variance carries its own degrees of freedom: df1 = 24
    and df2 = 24. The F ratio F = s1^2 / s2^2 is not formed in this
    step; scipy.stats.f is unused until Step 2.
    """
    # ddof=1: divisor n-1. float(...) strips the NumPy scalar wrapper.
    s1_sq = float(np.var(station_a, ddof=1))
    s2_sq = float(np.var(station_b, ddof=1))
    return {
        "n1": float(N1),
        "n2": float(N2),
        "df1": float(N1 - 1),
        "df2": float(N2 - 1),
        "s1_sq": s1_sq,
        "s2_sq": s2_sq,
        # Generating variances. Printed for teaching; not an estimate.
        "hidden_sigma1_sq": SIGMA1 ** 2,
        "hidden_sigma2_sq": SIGMA2 ** 2,
    }
# ------------------------------------------------------------------------------


# --- NEW (3) save_figure() ---------------------------------------------------
def save_figure(
    station_a: np.ndarray,
    station_b: np.ndarray,
    metrics: dict[str, float],
) -> Path:
    """Save side-by-side boxplots of the two station samples.

    Parameters
    ----------
    station_a:
        n1 cycle times plotted as the left box.
    station_b:
        n2 cycle times plotted as the right box.
    metrics:
        Dict from sample_variances(); s1_sq and s2_sq go in the title.

    Returns
    -------
    Path
        Absolute path of the PNG. The function writes that file and does
        not open a window. Lesson 01 explains pathlib and savefig.

    Notes
    -----
    Boxplots display spread, which is what the two-variance comparison
    is about. The means can look similar (both clocks have mu = 40) while
    the boxes differ in width. F in Step 2 compares the sample variances,
    not the sample means.
    """
    output_path = DIR_FIGURES / "f_two_var_01_sample_variances.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    box = ax.boxplot(
        [station_a, station_b],
        tick_labels=["Station A", "Station B"],
        patch_artist=True,
        widths=0.45,
    )
    box["boxes"][0].set_facecolor("#EC2661")
    box["boxes"][1].set_facecolor("#5B8DEF")
    for median in box["medians"]:
        median.set_color("#1A2E51")
        median.set_linewidth(2)
    ax.set_ylabel("Cycle time (minutes)")
    ax.set_title(
        f"sA^2 = {metrics['s1_sq']:.2f}   |   sB^2 = {metrics['s2_sq']:.2f}"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    # tight_layout, savefig, and close follow the Lesson 01 unattended
    # pattern. Never call plt.show().
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    """Run the Step 1 two-variance report and write the boxplot figure.

    Returns
    -------
    None
        Results go to stdout and to the PNG. Nothing is returned.
    """
    station_a, station_b = generate_two_stations()
    metrics = sample_variances(station_a, station_b)
    figure_path = save_figure(station_a, station_b, metrics)

    print("================================================================")
    print("LESSON 32 - STEP 1: TWO SAMPLE VARIANCES")
    print("================================================================")
    print("Synthetic data notice           : No real company data are used")
    print(f"Random seed                     : {SEED}")
    print(f"Station A n1                    : {N1}")
    print(f"Station B n2                    : {N2}")
    print(f"df1 = n1-1                      : {int(metrics['df1'])}")
    print(f"df2 = n2-1                      : {int(metrics['df2'])}")
    # Sample variances with ddof=1. F = s1^2 / s2^2 is formed in Step 2.
    print(f"Station A s1^2                  : {metrics['s1_sq']:.6f}")
    print(f"Station B s2^2                  : {metrics['s2_sq']:.6f}")
    print(f"Hidden sigma1^2                 : {metrics['hidden_sigma1_sq']:.6f}")
    print(f"Hidden sigma2^2                 : {metrics['hidden_sigma2_sq']:.6f}")
    print(f"Figure saved to                 : {figure_path}")
    print("================================================================")


# Lesson 01 explains this entry-point idiom. Keep it so the file runs as a
# standalone program and does not execute main() on import.
if __name__ == "__main__":
    main()

