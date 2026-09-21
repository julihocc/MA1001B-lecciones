"""
Lección 38 - Paso 2: t de una muestra sobre las diferencias
===========================================================
NUEVO EN ESTE PASO: paired_standard_error(), paired_t_test() y save_figure().

La Receta
Partir de t_pareada_01_diferencias.py e introducir:
    1. paired_standard_error()  EE de la diferencia media, s_d / sqrt(n)
    2. paired_t_test()          t con gl = n - 1 y el valor p bilateral
    3. save_figure()            histograma de d con el 0 hipotético

Las mismas 25 estaciones emparejadas se reconstruyen con SEED = 42. La
prueba pareada es una t de una muestra aplicada a d = antes - después. No se
importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PAIRS = 25
MU0 = 0.0
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pairs(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae 25 tiempos de manejo emparejados antes-después en minutos."""
    rng = np.random.default_rng(seed)
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    return {"before": before, "after": after, "diff": before - after}


# --- NUEVO (1) paired_standard_error() ---------------------------------------
def paired_standard_error(diff: np.ndarray) -> float:
    """Error estándar de la diferencia media."""
    return float(np.std(diff, ddof=1) / np.sqrt(diff.size))
# ------------------------------------------------------------------------------


# --- NUEVO (2) paired_t_test() -----------------------------------------------
def paired_t_test(diff: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """Prueba t de una muestra de H0: diferencia media = 0."""
    n = diff.size
    dbar = float(np.mean(diff))
    s_d = float(np.std(diff, ddof=1))
    se = paired_standard_error(diff)
    t_stat = (dbar - mu0) / se
    df = n - 1
    p_value = float(2.0 * stats.t.sf(np.abs(t_stat), df))
    scipy_test = stats.ttest_1samp(diff, mu0)
    return {
        "n": float(n),
        "dbar": dbar,
        "s_d": s_d,
        "se": se,
        "t_stat": float(t_stat),
        "df": float(df),
        "p_value": p_value,
        "scipy_p": float(scipy_test.pvalue),
        "t_critical": float(stats.t.ppf(1.0 - ALPHA / 2.0, df)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(diff: np.ndarray, dbar: float) -> Path:
    """Histograma de diferencias emparejadas con H0 en cero."""
    output_path = DIR_FIGURES / "t_pareada_02_prueba_pareada.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(diff, bins=8, color="#5B8DEF", edgecolor="#1A2E51", alpha=0.9)
    ax.axvline(MU0, color="#646464", linestyle="--", linewidth=1.6,
               label="H0: media d = 0")
    ax.axvline(dbar, color="#EC2661", linewidth=1.8,
               label=f"media d = {dbar:.2f}")
    ax.set_xlabel("Diferencia d = antes - después (minutos)")
    ax.set_ylabel("Frecuencia")
    ax.set_title("La t pareada es una t de una muestra sobre las diferencias")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    pairs = build_pairs()
    test = paired_t_test(pairs["diff"])
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(pairs["diff"], test["dbar"])

    print("================================================================")
    print("LECCIÓN 38 - PASO 2: PRUEBA T PAREADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print("Hipótesis                       : H0: mu_d = 0 frente a H1: mu_d != 0")
    print(f"Media de la diferencia d-barra  : {test['dbar']:.6f}")
    print(f"EE de la diferencia media       : {test['se']:.6f}")
    print(f"Estadístico t                   : {test['t_stat']:.6f}")
    print(f"Grados de libertad n-1          : {int(test['df'])}")
    print(f"Valor p bilateral (manual)      : {test['p_value']:.6e}")
    print(f"Valor p bilateral (scipy)       : {test['scipy_p']:.6e}")
    print(f"t* crítica (bilateral)          : {test['t_critical']:.6f}")
    print(f"Decisión con alfa = 0.05        : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

