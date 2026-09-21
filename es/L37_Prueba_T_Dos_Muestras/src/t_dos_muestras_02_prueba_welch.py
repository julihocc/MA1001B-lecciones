"""
Lección 37 - Paso 2: Prueba t de Welch de dos muestras
======================================================
NUEVO EN ESTE PASO: welch_standard_error(), welch_t_test() y save_figure().

La Receta
Partir de t_dos_muestras_01_resumenes_grupos.py e introducir:
    1. welch_standard_error()   EE que no agrupa las dos varianzas
    2. welch_t_test()           estadístico t, gl de Satterthwaite, p bilateral
    3. save_figure()            densidad t con el estadístico de Welch observado

Los mismos turnos sintéticos nA = 30 y nB = 32 se reconstruyen con SEED = 42.
Welch es el procedimiento declarado porque los tamaños de muestra y los
valores s muestrales difieren. No se importa ningún script anterior de la
lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 30
N_B = 32
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae tiempos de recolección sintéticos independientes y años de experiencia."""
    rng = np.random.default_rng(seed)
    return {
        "times_a": rng.normal(loc=48.0, scale=6.0, size=N_A),
        "times_b": rng.normal(loc=52.5, scale=7.5, size=N_B),
        "experience_a": rng.normal(loc=4.5, scale=1.0, size=N_A),
        "experience_b": rng.normal(loc=2.0, scale=0.8, size=N_B),
    }


# --- NUEVO (1) welch_standard_error() ----------------------------------------
def welch_standard_error(s_a: float, n_a: int, s_b: float, n_b: int) -> float:
    """Devuelve sqrt(sA^2/nA + sB^2/nB) sin agrupar las varianzas."""
    return float(np.sqrt(s_a**2 / n_a + s_b**2 / n_b))
# ------------------------------------------------------------------------------


# --- NUEVO (2) welch_t_test() ------------------------------------------------
def welch_t_test(times_a: np.ndarray, times_b: np.ndarray) -> dict[str, float]:
    """t de Welch, gl de Satterthwaite y valor p bilateral."""
    mean_a = float(np.mean(times_a))
    mean_b = float(np.mean(times_b))
    s_a = float(np.std(times_a, ddof=1))
    s_b = float(np.std(times_b, ddof=1))
    n_a = times_a.size
    n_b = times_b.size
    se = welch_standard_error(s_a, n_a, s_b, n_b)
    t_stat = (mean_a - mean_b) / se
    df_num = (s_a**2 / n_a + s_b**2 / n_b) ** 2
    df_den = (s_a**2 / n_a) ** 2 / (n_a - 1) + (s_b**2 / n_b) ** 2 / (n_b - 1)
    df_welch = df_num / df_den
    p_value = float(2.0 * stats.t.sf(np.abs(t_stat), df_welch))
    scipy_test = stats.ttest_ind(times_a, times_b, equal_var=False)
    return {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "s_a": s_a,
        "s_b": s_b,
        "se": se,
        "t_stat": float(t_stat),
        "df_welch": float(df_welch),
        "p_value": p_value,
        "scipy_p": float(scipy_test.pvalue),
        "scipy_t": float(scipy_test.statistic),
        "t_critical": float(stats.t.ppf(1.0 - ALPHA / 2.0, df_welch)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(t_stat: float, df_welch: float, t_critical: float) -> Path:
    """Sombrea ambas colas de la curva de referencia t de Welch."""
    output_path = DIR_FIGURES / "t_dos_muestras_02_prueba_welch.png"
    x = np.linspace(-4.8, 4.8, 600)
    y = stats.t.pdf(x, df_welch)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(x, y, where=(x <= -abs(t_stat)), color="#EC2661", alpha=0.45)
    ax.fill_between(x, y, where=(x >= abs(t_stat)), color="#EC2661", alpha=0.45)
    ax.axvline(t_stat, color="#EC2661", linewidth=1.6,
               label=f"t observada = {t_stat:.2f}")
    ax.axvline(-t_critical, color="#646464", linestyle="--", linewidth=1.2)
    ax.axvline(t_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"t* = {t_critical:.2f}")
    ax.set_xlabel("t")
    ax.set_ylabel("Densidad")
    ax.set_title(f"t de Welch de dos muestras, gl = {df_welch:.1f}")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    samples = build_shift_samples()
    test = welch_t_test(samples["times_a"], samples["times_b"])
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(test["t_stat"], test["df_welch"], test["t_critical"])

    print("================================================================")
    print("LECCIÓN 37 - PASO 2: PRUEBA T DE WELCH DE DOS MUESTRAS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print("Hipótesis                       : H0: muA = muB frente a H1: muA != muB")
    print(f"Diferencia de medias A menos B  : {test['mean_a'] - test['mean_b']:.6f}")
    print(f"EE de Welch                     : {test['se']:.6f}")
    print(f"Estadístico t de Welch          : {test['t_stat']:.6f}")
    print(f"gl de Satterthwaite             : {test['df_welch']:.6f}")
    print(f"Valor p bilateral (manual)      : {test['p_value']:.6f}")
    print(f"Valor p bilateral (scipy)       : {test['scipy_p']:.6f}")
    print(f"t* crítica (bilateral)          : {test['t_critical']:.6f}")
    print(f"Decisión con alfa = 0.05        : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

