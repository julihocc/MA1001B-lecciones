"""
Lección 32 - Paso 2: Razón F y probabilidad de cola superior
============================================================
NUEVO EN ESTE PASO: f_ratio(), f_upper_tail() y save_figure().

La Receta
Partir de f_dos_var_01_varianzas_muestrales.py e introducir:
    1. f_ratio()            F = s1^2 / s2^2
    2. f_upper_tail()       p = scipy.stats.f.sf(F, df1, df2)
    3. save_figure()        sombrear la cola F más allá de la razón observada

H0: sigma1^2 = sigma2^2 frente a H1: sigma1^2 > sigma2^2. Las mismas dos
muestras de estación se reconstruyen con SEED = 42. No se importa ningún
script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N1 = 25
N2 = 25
MU = 40.0
SIGMA1 = 8.0
SIGMA2 = 5.0
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_two_stations(seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """Extrae muestras normales independientes de dos estaciones de empaque."""
    rng = np.random.default_rng(seed)
    station_a = rng.normal(loc=MU, scale=SIGMA1, size=N1)
    station_b = rng.normal(loc=MU, scale=SIGMA2, size=N2)
    return station_a, station_b


# --- NUEVO (1) f_ratio() -----------------------------------------------------
def f_ratio(station_a: np.ndarray, station_b: np.ndarray) -> dict[str, float]:
    """Calcula F = s1^2 / s2^2 con gl de numerador y denominador."""
    s1_sq = float(np.var(station_a, ddof=1))
    s2_sq = float(np.var(station_b, ddof=1))
    return {
        "s1_sq": s1_sq,
        "s2_sq": s2_sq,
        "f_stat": s1_sq / s2_sq,
        "df1": float(N1 - 1),
        "df2": float(N2 - 1),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) f_upper_tail() ------------------------------------------------
def f_upper_tail(f_stat: float, df1: float, df2: float) -> dict[str, float]:
    """Devuelve el valor p de cola superior con scipy.stats.f.sf y el F crítico."""
    p_value = float(stats.f.sf(f_stat, df1, df2))
    f_crit = float(stats.f.ppf(1.0 - ALPHA, df1, df2))
    return {
        "p_value": p_value,
        "alpha": ALPHA,
        "f_crit": f_crit,
        "reject_h0": float(p_value < ALPHA),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(ratio: dict[str, float], tail: dict[str, float]) -> Path:
    """Sombrea la densidad F a la derecha de la razón observada."""
    output_path = DIR_FIGURES / "f_dos_var_02_prueba_f.png"
    df1, df2 = ratio["df1"], ratio["df2"]
    x = np.linspace(0.02, max(6.0, ratio["f_stat"] + 1.5), 400)
    y = stats.f.pdf(x, df1, df2)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(
        x[x >= ratio["f_stat"]],
        y[x >= ratio["f_stat"]],
        color="#EC2661",
        alpha=0.55,
        label=f"P(F >= {ratio['f_stat']:.2f}) = {tail['p_value']:.4f}",
    )
    ax.axvline(ratio["f_stat"], color="#EC2661", linewidth=2.0)
    ax.axvline(tail["f_crit"], color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"F crítico = {tail['f_crit']:.2f}")
    ax.set_xlabel("Estadístico F")
    ax.set_ylabel("Densidad")
    ax.set_title("Distribución F: cola superior para dos varianzas")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    station_a, station_b = generate_two_stations()
    ratio = f_ratio(station_a, station_b)
    tail = f_upper_tail(ratio["f_stat"], ratio["df1"], ratio["df2"])
    figure_path = save_figure(ratio, tail)

    print("================================================================")
    print("LECCIÓN 32 - PASO 2: RAZÓN F Y COLA SUPERIOR")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print("H0                             : sigma1^2 = sigma2^2")
    print("H1                             : sigma1^2 > sigma2^2")
    print(f"s1^2                            : {ratio['s1_sq']:.6f}")
    print(f"s2^2                            : {ratio['s2_sq']:.6f}")
    print(f"F = s1^2 / s2^2                 : {ratio['f_stat']:.6f}")
    print(f"gl1, gl2                        : {int(ratio['df1'])}, {int(ratio['df2'])}")
    print(f"F crítico (alfa=0.05)           : {tail['f_crit']:.6f}")
    print(f"Valor p de cola superior (f.sf) : {tail['p_value']:.6f}")
    print(f"Rechazar H0 con alfa=0.05       : {'sí' if tail['reject_h0'] else 'no'}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

