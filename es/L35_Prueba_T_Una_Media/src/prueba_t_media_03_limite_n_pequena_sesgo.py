"""
Lección 35 - Paso 3: n pequeña más sesgo hace frágil el valor p de t
====================================================================
NUEVO EN ESTE PASO: skewed_small_sample(), leave_one_out_pvalues() y
save_figure().

La Receta
Partir de prueba_t_media_02_valor_p_bilateral.py e introducir:
    1. skewed_small_sample()     n = 8 tiempos de empaque sesgados a la derecha
    2. leave_one_out_pvalues()   cómo una observación mueve el valor p
    3. save_figure()             p de la muestra completa frente a p dejando uno fuera

La muestra n = 40 aproximadamente simétrica se reconstruye solo como contraste
de robustez. El límite es el sorteo apresurado n = 8: un retraso largo infla
s y el valor p bilateral deja de ser un insumo de decisión estable.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 40
N_SMALL = 8
MU0 = 50.0
PROCESS_MEAN = 52.0
PROCESS_SD = 6.0
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pack_times(seed: int = SEED) -> np.ndarray:
    """Extrae n = 40 tiempos de ciclo de empaque sintéticos en minutos."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=PROCESS_MEAN, scale=PROCESS_SD, size=N)


# --- NUEVO (1) skewed_small_sample() -----------------------------------------
def skewed_small_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n = 8 tiempos: siete empaques típicos más un retraso largo."""
    rng = np.random.default_rng(seed)
    bulk = rng.normal(loc=48.0, scale=3.5, size=N_SMALL - 1)
    tail = rng.lognormal(mean=4.5, sigma=0.25, size=1)
    return np.concatenate([bulk, tail])
# ------------------------------------------------------------------------------


# --- NUEVO (2) leave_one_out_pvalues() ---------------------------------------
def leave_one_out_pvalues(times: np.ndarray, mu0: float = MU0) -> dict[str, object]:
    """Calcula la prueba t de la muestra completa y cada valor p dejando uno fuera."""
    full = stats.ttest_1samp(times, mu0)
    loo_p = []
    for i in range(times.size):
        reduced = np.delete(times, i)
        loo_p.append(float(stats.ttest_1samp(reduced, mu0).pvalue))
    loo = np.array(loo_p)
    return {
        "xbar": float(np.mean(times)),
        "sample_sd": float(np.std(times, ddof=1)),
        "skewness": float(stats.skew(times)),
        "t_stat": float(full.statistic),
        "p_value": float(full.pvalue),
        "shapiro_p": float(stats.shapiro(times).pvalue),
        "loo_pvalues": loo,
        "min_loo_p": float(np.min(loo)),
        "max_loo_p": float(np.max(loo)),
        "dropped_index": int(np.argmax(times)),
        "dropped_value": float(np.max(times)),
        "p_without_max": float(loo[int(np.argmax(times))]),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(times: np.ndarray, results: dict[str, object]) -> Path:
    """Contrasta el histograma n = 8 con los valores p dejando uno fuera."""
    output_path = DIR_FIGURES / "prueba_t_media_03_limite_n_pequena_sesgo.png"
    loo = np.asarray(results["loo_pvalues"], dtype=float)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6))

    axes[0].hist(times, bins=6, color="#F4A6B8", edgecolor="#1A2E51")
    axes[0].axvline(MU0, color="#646464", linestyle="--", linewidth=1.5,
                    label="media H0 = 50")
    axes[0].axvline(float(results["xbar"]), color="#EC2661", linewidth=1.6,
                    label=f"x-barra = {float(results['xbar']):.1f}")
    axes[0].set_xlabel("Tiempo de ciclo (minutos)")
    axes[0].set_ylabel("Frecuencia")
    axes[0].set_title("n = 8, tiempos de empaque sesgados a la derecha")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    colors = ["#EC2661" if i == int(results["dropped_index"]) else "#1A2E51"
              for i in range(len(loo))]
    axes[1].bar(np.arange(1, len(loo) + 1), loo, color=colors, width=0.7)
    axes[1].axhline(float(results["p_value"]), color="#5B8DEF", linestyle="-",
                    linewidth=1.6, label=f"p completa = {float(results['p_value']):.3f}")
    axes[1].axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.2,
                    label="alfa = 0.05")
    axes[1].set_xlabel("Observación omitida")
    axes[1].set_ylabel("Valor p bilateral")
    axes[1].set_title("Valores p dejando uno fuera")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    large = build_pack_times()
    large_test = stats.ttest_1samp(large, MU0)
    large_loo = [
        float(stats.ttest_1samp(np.delete(large, i), MU0).pvalue)
        for i in range(large.size)
    ]
    small = skewed_small_sample()
    results = leave_one_out_pvalues(small)
    figure_path = save_figure(small, results)

    print("================================================================")
    print("LECCIÓN 35 - PASO 3: LÍMITE DE n PEQUEÑA MÁS SESGO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Valor p bilateral n = 40        : {float(large_test.pvalue):.6f}")
    print(f"p mínima dejando uno fuera n=40 : {min(large_loo):.6f}")
    print(f"p máxima dejando uno fuera n=40 : {max(large_loo):.6f}")
    print(f"Tamaño de muestra n = 8         : {N_SMALL}")
    print(f"Media muestral n = 8            : {float(results['xbar']):.6f}")
    print(f"s muestral n = 8                : {float(results['sample_sd']):.6f}")
    print(f"Sesgo n = 8                     : {float(results['skewness']):.6f}")
    print(f"Valor p Shapiro-Wilk n = 8      : {float(results['shapiro_p']):.6f}")
    print(f"Estadístico t n = 8             : {float(results['t_stat']):.6f}")
    print(f"Valor p bilateral n = 8         : {float(results['p_value']):.6f}")
    print(f"Retraso más largo (minutos)     : {float(results['dropped_value']):.6f}")
    print(f"Valor p sin el más largo        : {float(results['p_without_max']):.6f}")
    print(f"p mínima dejando uno fuera      : {float(results['min_loo_p']):.6f}")
    print(f"p máxima dejando uno fuera      : {float(results['max_loo_p']):.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

