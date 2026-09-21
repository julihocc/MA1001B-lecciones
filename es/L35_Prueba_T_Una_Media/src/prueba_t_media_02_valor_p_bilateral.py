"""
Lección 35 - Paso 2: Valor p bilateral de la t de Student
=========================================================
NUEVO EN ESTE PASO: two_sided_p_value(), critical_t_and_decision() y
save_figure().

La Receta
Partir de prueba_t_media_01_error_estandar_muestral.py e introducir:
    1. two_sided_p_value()     probabilidad de dos colas de t con gl = n - 1
    2. critical_t_and_decision()  t* con alfa = 0.05 y la regla rechazar/retener
    3. save_figure()           sombrear ambas colas de la densidad t

Los mismos n = 40 tiempos de empaque sintéticos se reconstruyen con SEED = 42.
No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 40
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


def t_statistic(times: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """Calcula x-barra, s, EE, grados de libertad y la t de una muestra."""
    n = times.size
    xbar = float(np.mean(times))
    sample_sd = float(np.std(times, ddof=1))
    se = sample_sd / np.sqrt(n)
    t_stat = (xbar - mu0) / se
    return {
        "n": float(n),
        "xbar": xbar,
        "sample_sd": sample_sd,
        "se": float(se),
        "df": float(n - 1),
        "t_stat": float(t_stat),
        "mu0": mu0,
    }


# --- NUEVO (1) two_sided_p_value() -------------------------------------------
def two_sided_p_value(t_stat: float, df: float) -> dict[str, float]:
    """Devuelve el valor p bilateral de la t de Student y de ttest_1samp."""
    p_manual = float(2.0 * stats.t.sf(np.abs(t_stat), df))
    return {"p_value": p_manual}
# ------------------------------------------------------------------------------


# --- NUEVO (2) critical_t_and_decision() -------------------------------------
def critical_t_and_decision(
    t_stat: float,
    df: float,
    p_value: float,
    alpha: float = ALPHA,
) -> dict[str, float | str]:
    """Compara |t| con t* y el valor p con alfa."""
    t_critical = float(stats.t.ppf(1.0 - alpha / 2.0, df))
    reject = bool(p_value < alpha)
    return {
        "alpha": alpha,
        "t_critical": t_critical,
        "decision": "rechazar H0" if reject else "no rechazar H0",
        "reject": float(reject),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(t_stat: float, df: float, t_critical: float) -> Path:
    """Sombrea las colas bilaterales t más allá del estadístico observado."""
    output_path = DIR_FIGURES / "prueba_t_media_02_valor_p_bilateral.png"
    x = np.linspace(-4.5, 4.5, 600)
    y = stats.t.pdf(x, df)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(x, y, where=(x <= -abs(t_stat)), color="#EC2661", alpha=0.45)
    ax.fill_between(x, y, where=(x >= abs(t_stat)), color="#EC2661", alpha=0.45)
    ax.axvline(t_stat, color="#EC2661", linestyle="-", linewidth=1.6,
               label=f"t observada = {t_stat:.2f}")
    ax.axvline(t_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"t* = {t_critical:.2f}")
    ax.axvline(-t_critical, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_xlabel("t")
    ax.set_ylabel("Densidad")
    ax.set_title(f"Prueba t bilateral, gl = {int(df)}")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    times = build_pack_times()
    summary = t_statistic(times)
    p_info = two_sided_p_value(summary["t_stat"], summary["df"])
    scipy_test = stats.ttest_1samp(times, MU0)
    decision = critical_t_and_decision(
        summary["t_stat"], summary["df"], p_info["p_value"]
    )
    figure_path = save_figure(
        summary["t_stat"], summary["df"], float(decision["t_critical"])
    )

    print("================================================================")
    print("LECCIÓN 35 - PASO 2: VALOR P BILATERAL DE T")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {int(summary['n'])}")
    print(f"Hipótesis                       : H0: mu = {MU0:.0f} frente a H1: mu != {MU0:.0f}")
    print(f"Media muestral x-barra          : {summary['xbar']:.6f}")
    print(f"Estadístico t                   : {summary['t_stat']:.6f}")
    print(f"Grados de libertad              : {int(summary['df'])}")
    print(f"Valor p bilateral (manual)      : {p_info['p_value']:.6f}")
    print(f"Valor p bilateral (scipy)       : {float(scipy_test.pvalue):.6f}")
    print(f"Nivel de significancia alfa     : {float(decision['alpha']):.2f}")
    print(f"t* crítica (bilateral)          : {float(decision['t_critical']):.6f}")
    print(f"Decisión con alfa = 0.05        : {decision['decision']}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

