"""
Lección 30 - Paso 1: Tamaño de muestra para un margen de error de la media
==========================================================================
NUEVO EN ESTE PASO: mean_sample_size(), round_up_n() y save_figure().

La Receta
Un estudio de operaciones completamente sintético quiere un intervalo al
95% para el tiempo medio de atención con margen de error E = 2 minutos. Un
valor de planificación s = 10 minutos se trata como la escala. La fórmula
de tamaño de muestra para la media es n = (z* s / E)^2, luego se redondea
hacia arriba al siguiente entero.

Ejecútalo:
    uv run es/L30_Determinacion_Tamano_Muestra/src/sample_size_01_mean_margin.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
Z_STAR = 1.96
S_PLAN = 10.0
E_MEAN = 2.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) mean_sample_size() --------------------------------------------
def mean_sample_size(z_star: float, s: float, margin: float) -> dict[str, float]:
    """Retorna el n crudo = (z* s / E)^2 antes del redondeo entero."""
    raw = (z_star * s / margin) ** 2
    return {
        "z_star": z_star,
        "s": s,
        "margin": margin,
        "raw_n": float(raw),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) round_up_n() --------------------------------------------------
def round_up_n(raw_n: float) -> int:
    """Redondea un tamaño de muestra crudo hacia arriba a la siguiente observación entera."""
    return int(np.ceil(raw_n))
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(raw_n: float, n_required: int) -> Path:
    """Guarda n versus margen de error para una media, con z* y s fijos."""
    output_path = DIR_FIGURES / "sample_size_01_mean_margin.png"
    margins = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
    ns = np.ceil((Z_STAR * S_PLAN / margins) ** 2)
    colors = ["#5B8DEF" if m != E_MEAN else "#EC2661" for m in margins]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar([str(m) for m in margins], ns, color=colors, width=0.62)
    ax.set_xlabel("Margen de error objetivo E (minutos)")
    ax.set_ylabel("Tamaño de muestra requerido n")
    ax.set_title("Tamaño de muestra para la media n = (z* s / E)^2, redondeado hacia arriba")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, ns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2,
            f"{int(value)}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    plan = mean_sample_size(Z_STAR, S_PLAN, E_MEAN)
    n_required = round_up_n(plan["raw_n"])
    figure_path = save_figure(plan["raw_n"], n_required)

    print("================================================================")
    print("LECCIÓN 30 - PASO 1: TAMAÑO DE MUESTRA PARA UNA MEDIA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"z-estrella de libro             : {plan['z_star']:.6f}")
    print(f"s de planificación (minutos)    : {plan['s']:.6f}")
    print(f"Margen objetivo E (minutos)     : {plan['margin']:.6f}")
    print(f"n crudo = (z s / E)^2           : {plan['raw_n']:.6f}")
    print(f"n redondeado hacia arriba       : {n_required}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

