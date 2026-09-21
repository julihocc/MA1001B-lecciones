"""
Lección 27 - Paso 3: Sigma desconocida hace del intervalo Z la herramienta
equivocada
=========================================================================
La Receta
Partir de z_ci_mean_02_z_interval.py e introducir:
    1. sample_standard_deviation()  s de los mismos n = 36 llenados
    2. compare_known_vs_plug_in()   intervalo z con sigma versus z con s
    3. save_figure()                contrastar los dos intervalos

Límite: los datos de operaciones casi nunca llegan con una sigma
poblacional conocida. Sustituir sigma por s pero conservar z* = 1.96 no
es un intervalo z válido. La Lección 28 sustituye z* por un valor crítico
t con gl = n - 1.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
SIGMA = 10.0
MU_TRUE = 502.0
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid de N(mu_true, sigma). El analista no conoce mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


# --- NUEVO (1) sample_standard_deviation() -----------------------------------
def sample_standard_deviation(sample: np.ndarray) -> dict[str, float]:
    """Estima sigma a partir de la muestra. Esta s no es un parámetro conocido."""
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    return {
        "xbar": xbar,
        "s": s,
        "se_known": SIGMA / np.sqrt(N),
        "se_plug_in": s / np.sqrt(N),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_known_vs_plug_in() ------------------------------------
def compare_known_vs_plug_in(stats_s: dict[str, float]) -> dict[str, float]:
    """Conserva z* = 1.96 pero cambia sigma por s. Ese cambio es el límite pedagógico."""
    known_margin = Z_STAR * stats_s["se_known"]
    plug_margin = Z_STAR * stats_s["se_plug_in"]
    return {
        "known_lower": stats_s["xbar"] - known_margin,
        "known_upper": stats_s["xbar"] + known_margin,
        "known_width": 2.0 * known_margin,
        "plug_lower": stats_s["xbar"] - plug_margin,
        "plug_upper": stats_s["xbar"] + plug_margin,
        "plug_width": 2.0 * plug_margin,
        "width_difference": 2.0 * abs(plug_margin - known_margin),
        "s_minus_sigma": stats_s["s"] - SIGMA,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    stats_s: dict[str, float],
    comparison: dict[str, float],
) -> Path:
    """Contrasta el intervalo z válido con sigma conocida y el z-con-s inválido."""
    output_path = DIR_FIGURES / "z_ci_mean_03_unknown_sigma_limit.png"
    labels = ["Intervalo z válido\n(sigma conocida)", "z-con-s inválido\n(sigma desconocida)"]
    centers = [stats_s["xbar"], stats_s["xbar"]]
    xerr = np.array(
        [
            [
                stats_s["xbar"] - comparison["known_lower"],
                stats_s["xbar"] - comparison["plug_lower"],
            ],
            [
                comparison["known_upper"] - stats_s["xbar"],
                comparison["plug_upper"] - stats_s["xbar"],
            ],
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
    ax.set_title("Sigma desconocida hace del intervalo Z la herramienta equivocada")
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
    stats_s = sample_standard_deviation(sample)
    comparison = compare_known_vs_plug_in(stats_s)
    figure_path = save_figure(stats_s, comparison)

    print("================================================================")
    print("LECCIÓN 27 - PASO 3: LÍMITE DE SIGMA DESCONOCIDA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida (ml)             : {SIGMA:.6f}")
    print(f"Media muestral xbar (ml)        : {stats_s['xbar']:.6f}")
    print(f"Desv. estándar muestral s       : {stats_s['s']:.6f}")
    print(f"s menos sigma                   : {comparison['s_minus_sigma']:.6f}")
    print(f"EE con sigma conocida           : {stats_s['se_known']:.6f}")
    print(f"EE con s plug-in                : {stats_s['se_plug_in']:.6f}")
    print(f"Límite inferior z válido        : {comparison['known_lower']:.6f}")
    print(f"Límite superior z válido        : {comparison['known_upper']:.6f}")
    print(f"Anchura z válida                : {comparison['known_width']:.6f}")
    print(f"Límite inferior z-con-s inválido: {comparison['plug_lower']:.6f}")
    print(f"Límite superior z-con-s inválido: {comparison['plug_upper']:.6f}")
    print(f"Anchura z-con-s inválida        : {comparison['plug_width']:.6f}")
    print(f"Diferencia absoluta de anchura  : {comparison['width_difference']:.6f}")
    print("Límite                          : sigma desconocida necesita t, no z")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

