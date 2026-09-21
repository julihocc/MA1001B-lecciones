"""
Lección 28 - Paso 3: Un atípico extremo infla s y el intervalo
=============================================================
La Receta
Partir de t_ci_mean_02_t_interval.py e introducir:
    1. contaminate_one_fill()     sustituir una observación por un atípico extremo
    2. compare_clean_vs_outlier() intervalos t antes y después del atípico
    3. save_figure()              mostrar cómo inflan s y la anchura del intervalo

Límite: un solo llenado extremo infla s, de modo que el intervalo t se
vuelve mucho más ancho. El procedimiento t es válido bajo normalidad
aproximada; un atípico basta para distorsionar la escala estimada.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
SIGMA_TRUE = 10.0
MU_TRUE = 502.0
OUTLIER_VALUE = 560.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid. El analista observa la muestra, no sigma."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


def t_interval_from_sample(sample: np.ndarray) -> dict[str, float]:
    """Calcula s, t* y el intervalo t al 95% a partir de una muestra."""
    n = sample.size
    df = n - 1
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    se_hat = s / np.sqrt(n)
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


# --- NUEVO (1) contaminate_one_fill() ----------------------------------------
def contaminate_one_fill(sample: np.ndarray) -> np.ndarray:
    """Sustituye la última observación por un llenado extremo de 560 ml."""
    contaminated = np.array(sample, copy=True)
    contaminated[-1] = OUTLIER_VALUE
    return contaminated
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_clean_vs_outlier() ------------------------------------
def compare_clean_vs_outlier(
    clean: dict[str, float],
    dirty: dict[str, float],
) -> dict[str, float]:
    """Mide cómo un atípico infla s y la anchura del intervalo t."""
    return {
        "s_inflation": dirty["s"] - clean["s"],
        "width_inflation": dirty["width"] - clean["width"],
        "xbar_shift": dirty["xbar"] - clean["xbar"],
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    clean: dict[str, float],
    dirty: dict[str, float],
) -> Path:
    """Contrasta el intervalo t limpio con el intervalo inflado por el atípico."""
    output_path = DIR_FIGURES / "t_ci_mean_03_outlier_inflates_s.png"
    labels = ["Muestra limpia\nintervalo t", "Un atípico de 560 ml\nintervalo t"]
    centers = [clean["xbar"], dirty["xbar"]]
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
               label=f"mu verdadera = {MU_TRUE:.1f}")
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(labels)
    ax.set_xlabel("Volumen de llenado (ml)")
    ax.set_title("Un atípico extremo infla s y el intervalo t")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_ylim(-0.7, 1.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_fill_sample()
    clean = t_interval_from_sample(sample)
    dirty_sample = contaminate_one_fill(sample)
    dirty = t_interval_from_sample(dirty_sample)
    comparison = compare_clean_vs_outlier(clean, dirty)
    figure_path = save_figure(clean, dirty)

    print("================================================================")
    print("LECCIÓN 28 - PASO 3: UN ATÍPICO INFLA S")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Reemplazo atípico (ml)          : {OUTLIER_VALUE:.6f}")
    print(f"xbar limpia (ml)                : {clean['xbar']:.6f}")
    print(f"s limpia (ml)                   : {clean['s']:.6f}")
    print(f"t-estrella limpia               : {clean['t_star']:.6f}")
    print(f"Límite inferior limpio          : {clean['lower']:.6f}")
    print(f"Límite superior limpio          : {clean['upper']:.6f}")
    print(f"Anchura limpia                  : {clean['width']:.6f}")
    print(f"xbar con atípico (ml)           : {dirty['xbar']:.6f}")
    print(f"s con atípico (ml)              : {dirty['s']:.6f}")
    print(f"Límite inferior con atípico     : {dirty['lower']:.6f}")
    print(f"Límite superior con atípico     : {dirty['upper']:.6f}")
    print(f"Anchura con atípico             : {dirty['width']:.6f}")
    print(f"Inflación de s                  : {comparison['s_inflation']:.6f}")
    print(f"Desplazamiento de xbar          : {comparison['xbar_shift']:.6f}")
    print(f"Inflación de la anchura         : {comparison['width_inflation']:.6f}")
    print("Límite                          : un atípico infla s y el IC")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

