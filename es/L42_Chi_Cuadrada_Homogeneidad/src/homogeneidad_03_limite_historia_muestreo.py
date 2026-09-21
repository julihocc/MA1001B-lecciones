"""
Lección 42 - Paso 3: El mismo estadístico, distinta historia de muestreo
=======================================================================
LA RECETA
Parte de homogeneidad_02_chi_cuadrada.py e introduce:
    1. two_sampling_stories()   diseños de homogeneidad frente a independencia
    2. shared_statistic()       chi2 idéntica a partir de los mismos números
    3. save_figure()            contraste de los dos planes usando la chi2 compartida

Homogeneidad: tres muestras independientes de sitio, totales de fila fijos
por diseño. Independencia: una muestra de 310 tickets clasificada después
por sitio y canal. La aritmética es la misma. La pregunta no.
"""

from pathlib import Path

import matplotlib
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) two_sampling_stories() ----------------------------------------
def two_sampling_stories() -> dict[str, str]:
    """Describe los dos diseños que pueden producir la misma tabla."""
    return {
        "homogeneity": (
            "Tres muestras planeadas. Norte n=120, Centro n=100, Sur n=90 "
            "se eligieron primero. El canal es la respuesta."
        ),
        "independence": (
            "Una muestra de n=310 tickets. Sitio y canal son dos "
            "clasificaciones posteriores de los mismos tickets."
        ),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) shared_statistic() --------------------------------------------
def shared_statistic(observed: np.ndarray) -> dict[str, float]:
    """El número ji-cuadrada no codifica la historia de muestreo."""
    chi2, p_value, df, _ = stats.chi2_contingency(observed, correction=False)
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "df": float(df),
        "n": float(observed.sum()),
        "row_totals_fixed_by_design": 1.0,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(chi2: float, df: float) -> Path:
    """Diagrama de dos historias de muestreo que comparten un valor ji-cuadrada."""
    output_path = DIR_FIGURES / "homogeneidad_03_limite_historia_muestreo.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("La misma ji-cuadrada, dos historias distintas de muestreo")

    def box(x, y, w, h, text, color):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=color,
            edgecolor="#1A2E51",
            linewidth=1.1,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=8.5, color="#1A2E51", wrap=True)

    box(0.4, 3.4, 4.2, 2.0, "Homogeneidad\n3 muestras planeadas de sitio\nTotales de fila fijos", "#D6E4F0")
    box(5.4, 3.4, 4.2, 2.0, "Independencia\n1 muestra de 310 tickets\nEl sitio es una clasificación", "#F8D5DE")
    box(
        2.4,
        0.5,
        5.2,
        1.8,
        f"Aritmética compartida\nchi2 = {chi2:.6f}, df = {int(df)}\nLa pregunta no se comparte",
        "#F4F6F9",
    )
    ax.annotate("", xy=(5.0, 2.3), xytext=(2.5, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(5.0, 2.3), xytext=(7.5, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    stories = two_sampling_stories()
    stats_out = shared_statistic(OBSERVED)
    figure_path = save_figure(stats_out["chi2"], stats_out["df"])

    print("================================================================")
    print("LECCIÓN 42 - PASO 3: LÍMITE DE HISTORIA DE MUESTREO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Estadístico ji-cuadrada compartido: {stats_out['chi2']:.6f}")
    print(f"Grados de libertad compartidos  : {int(stats_out['df'])}")
    print(f"p-valor compartido              : {stats_out['p_value']:.6f}")
    print(f"Historia de homogeneidad        : {stories['homogeneity']}")
    print(f"Historia de independencia       : {stories['independence']}")
    print("¿Preguntan la misma H0?         : no")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

