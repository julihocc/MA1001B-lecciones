"""
Lección 10 - Paso 1: Árbol de frecuencias y descomposición del espacio muestral
===============================================================================
NUEVO EN ESTE PASO: lot_status_counts(), inspection_joint_counts() y
save_figure().

Contexto:
Un registro sintético de lotes entrantes tiene 100 lotes: 10 defectuosos y 90
limpios. Cada lote se inspecciona una vez. Entre los defectuosos, 8 se marcan
y 2 se omiten. Entre los limpios, 9 se marcan y 81 se liberan. Un diagrama de
árbol descompone este experimento de dos etapas en caminos terminales
mutuamente excluyentes.

Ejecútalo:
    uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_01_arbol_frecuencias.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


SEED = 42
N_LOTS = 100
N_DEFECTIVE = 10
N_CLEAN = 90
N_FLAGGED_DEFECTIVE = 8
N_MISSED_DEFECTIVE = 2
N_FLAGGED_CLEAN = 9
N_CLEARED_CLEAN = 81
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) lot_status_counts() -------------------------------------------
def lot_status_counts() -> dict[str, int]:
    """Devuelve las frecuencias de la primera etapa en el registro sintético."""
    return {
        "defective": N_DEFECTIVE,
        "clean": N_CLEAN,
        "total": N_LOTS,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) inspection_joint_counts() -------------------------------------
def inspection_joint_counts() -> dict[str, int]:
    """Devuelve las cuatro frecuencias de caminos terminales mutuamente excluyentes."""
    return {
        "defective_flagged": N_FLAGGED_DEFECTIVE,
        "defective_missed": N_MISSED_DEFECTIVE,
        "clean_flagged": N_FLAGGED_CLEAN,
        "clean_cleared": N_CLEARED_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(joints: dict[str, int]) -> Path:
    """Guarda un árbol de frecuencias del experimento de inspección de dos etapas."""
    output_path = DIR_FIGURES / "diagramas_arbol_01_arbol_frecuencias.png"
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Árbol de frecuencias: 100 lotes sintéticos")

    def box(x, y, text, color):
        patch = FancyBboxPatch(
            (x - 1.15, y - 0.38),
            2.30,
            0.76,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            facecolor=color,
            edgecolor="#1A2E51",
            linewidth=1.1,
        )
        ax.add_patch(patch)
        ax.text(x, y, text, ha="center", va="center", fontsize=9, color="#1A2E51")

    box(1.4, 3.0, "Inicio\n100 lotes", "#F4F6F9")
    box(4.6, 4.6, "Defectuoso\n10", "#F8D5DE")
    box(4.6, 1.4, "Limpio\n90", "#D6E4F0")
    box(8.3, 5.3, "Marcado\n8", "#EC2661")
    box(8.3, 3.9, "Omitido\n2", "#F4A6B8")
    box(8.3, 2.1, "Marcado\n9", "#5B8DEF")
    box(8.3, 0.7, "Liberado\n81", "#A9C4EA")

    ax.annotate("", xy=(3.4, 4.4), xytext=(2.55, 3.35),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(3.4, 1.6), xytext=(2.55, 2.65),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 5.2), xytext=(5.75, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 4.0), xytext=(5.75, 4.4),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 2.0), xytext=(5.75, 1.6),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))
    ax.annotate("", xy=(7.1, 0.8), xytext=(5.75, 1.2),
                arrowprops=dict(arrowstyle="-|>", color="#1A2E51", lw=1.4))

    ax.text(3.15, 4.15, "10/100", fontsize=8, color="#646464")
    ax.text(3.15, 1.85, "90/100", fontsize=8, color="#646464")
    ax.text(6.35, 5.45, "8/10", fontsize=8, color="#646464")
    ax.text(6.35, 3.55, "2/10", fontsize=8, color="#646464")
    ax.text(6.35, 2.35, "9/90", fontsize=8, color="#646464")
    ax.text(6.35, 0.45, "81/90", fontsize=8, color="#646464")

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    status = lot_status_counts()
    joints = inspection_joint_counts()
    path_sum = sum(joints.values())
    flagged = joints["defective_flagged"] + joints["clean_flagged"]
    figure_path = save_figure(joints)

    print("================================================================")
    print("LECCIÓN 10 - PASO 1: ÁRBOL DE FRECUENCIAS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Total de lotes                  : {status['total']}")
    print(f"Lotes defectuosos               : {status['defective']}")
    print(f"Lotes limpios                   : {status['clean']}")
    print(f"Defectuoso y marcado            : {joints['defective_flagged']}")
    print(f"Defectuoso y omitido            : {joints['defective_missed']}")
    print(f"Limpio y marcado                : {joints['clean_flagged']}")
    print(f"Limpio y liberado               : {joints['clean_cleared']}")
    print(f"Suma de caminos terminales      : {path_sum}")
    print(f"Lotes marcados                  : {flagged}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

