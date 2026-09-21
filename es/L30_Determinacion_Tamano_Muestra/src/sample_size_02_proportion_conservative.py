"""
Lección 30 - Paso 2: Tamaño de muestra conservador para una proporción
=====================================================================
La Receta
Partir de sample_size_01_mean_margin.py e introducir:
    1. proportion_sample_size()  n = z*^2 p(1-p) / E^2
    2. conservative_p()          p = 0.5 maximiza p(1-p)
    3. save_figure()             comparar p = 0.5 con otros valores de planificación

Se planifica un intervalo al 95% para una tasa de primer contacto con
E = 0.03. Usar p = 0.5 es la elección conservadora cuando la p verdadera
es desconocida.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
Z_STAR = 1.96
E_PROP = 0.03
P_CONSERVATIVE = 0.5
P_GUESSED = 0.18
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) proportion_sample_size() --------------------------------------
def proportion_sample_size(
    z_star: float,
    p_plan: float,
    margin: float,
) -> dict[str, float]:
    """Retorna n crudo y redondeado hacia arriba n = z*^2 p(1-p) / E^2."""
    raw = (z_star ** 2) * p_plan * (1.0 - p_plan) / (margin ** 2)
    return {
        "p_plan": p_plan,
        "pq": p_plan * (1.0 - p_plan),
        "raw_n": float(raw),
        "n_required": int(np.ceil(raw)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) conservative_p() ----------------------------------------------
def conservative_p() -> dict[str, float]:
    """Muestra que p = 0.5 produce el mayor p(1-p) y por tanto el mayor n."""
    guessed = proportion_sample_size(Z_STAR, P_GUESSED, E_PROP)
    conservative = proportion_sample_size(Z_STAR, P_CONSERVATIVE, E_PROP)
    return {
        "guessed_p": P_GUESSED,
        "guessed_n": float(guessed["n_required"]),
        "conservative_p": P_CONSERVATIVE,
        "conservative_n": float(conservative["n_required"]),
        "extra_observations": float(
            conservative["n_required"] - guessed["n_required"]
        ),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure() -> Path:
    """Compara el n requerido a través de valores de planificación de p."""
    output_path = DIR_FIGURES / "sample_size_02_proportion_conservative.png"
    p_values = np.array([0.10, 0.18, 0.30, 0.50, 0.70])
    ns = np.ceil((Z_STAR ** 2) * p_values * (1.0 - p_values) / (E_PROP ** 2))
    colors = ["#EC2661" if abs(p - 0.5) < 1e-9 else "#5B8DEF" for p in p_values]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar([f"{p:.2f}" for p in p_values], ns, color=colors, width=0.62)
    ax.set_xlabel("Valor de planificación de p")
    ax.set_ylabel("Tamaño de muestra requerido n")
    ax.set_title("Tamaño de muestra para una proporción: p = 0.5 es conservador")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, ns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 15,
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
    conservative = proportion_sample_size(Z_STAR, P_CONSERVATIVE, E_PROP)
    guessed = proportion_sample_size(Z_STAR, P_GUESSED, E_PROP)
    contrast = conservative_p()
    figure_path = save_figure()

    print("================================================================")
    print("LECCIÓN 30 - PASO 2: TAMAÑO DE MUESTRA CONSERVADOR PARA UNA PROPORCIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"z-estrella de libro             : {Z_STAR:.6f}")
    print(f"Margen objetivo E               : {E_PROP:.6f}")
    print(f"p conservadora                  : {conservative['p_plan']:.6f}")
    print(f"p(1-p) conservadora             : {conservative['pq']:.6f}")
    print(f"n crudo conservador             : {conservative['raw_n']:.6f}")
    print(f"n redondeado conservador        : {conservative['n_required']}")
    print(f"p supuesta de la Lección 29     : {guessed['p_plan']:.6f}")
    print(f"n redondeado supuesto           : {guessed['n_required']}")
    print(f"Observaciones extra con p=0.5   : {int(contrast['extra_observations'])}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

