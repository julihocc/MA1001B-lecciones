"""
Lección 15 - Paso 1: Dos políticas de inspección
================================================
NUEVO EN ESTE PASO: policy_a(), policy_b() y save_figure().

La Receta
Un escritorio de calidad completamente sintético compara dos políticas
binomiales que comparten la misma media de defectuosos: la Política A
inspecciona n = 50 unidades con p = 0.04, y la Política B inspecciona
n = 20 unidades con p = 0.10. Ambas tienen np = 2.

Ejecútalo:
    uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_01_dos_politicas.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POLICY_A = {"name": "A", "n": 50, "p": 0.04}
POLICY_B = {"name": "B", "n": 20, "p": 0.10}
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) policy_a() ----------------------------------------------------
def policy_a() -> dict[str, float | int | str]:
    """Devuelve la Política A: muestra más grande, menor chance de defecto."""
    n = POLICY_A["n"]
    p = POLICY_A["p"]
    return {"name": "A", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}
# ------------------------------------------------------------------------------


# --- NUEVO (2) policy_b() ----------------------------------------------------
def policy_b() -> dict[str, float | int | str]:
    """Devuelve la Política B: muestra más pequeña, mayor chance de defecto."""
    n = POLICY_B["n"]
    p = POLICY_B["p"]
    return {"name": "B", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    a: dict[str, float | int | str],
    b: dict[str, float | int | str],
) -> Path:
    """Guarda n, p y la media de las dos políticas."""
    output_path = DIR_FIGURES / "riesgo_binomial_01_dos_politicas.png"
    labels = ["n", "10 p", "media np"]
    a_vals = [float(a["n"]), 10.0 * float(a["p"]), float(a["mean"])]
    b_vals = [float(b["n"]), 10.0 * float(b["p"]), float(b["mean"])]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - width / 2, a_vals, width, color="#1A2E51", label="Política A")
    ax.bar(x + width / 2, b_vals, width, color="#EC2661", label="Política B")
    ax.set_xticks(x)
    ax.set_xticklabels(["n (unidades)", "10 x p", "media np"])
    ax.set_ylabel("Valor")
    ax.set_title("Misma media np = 2; distintos n y p")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    a = policy_a()
    b = policy_b()
    figure_path = save_figure(a, b)

    print("================================================================")
    print("LECCIÓN 15 - PASO 1: DOS POLÍTICAS")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Política A n                     : {a['n']}")
    print(f"Política A p                     : {a['p']:.6f}")
    print(f"Política A media np              : {a['mean']:.6f}")
    print(f"Política A varianza              : {a['variance']:.6f}")
    print(f"Política B n                     : {b['n']}")
    print(f"Política B p                     : {b['p']:.6f}")
    print(f"Política B media np              : {b['mean']:.6f}")
    print(f"Política B varianza              : {b['variance']:.6f}")
    print(f"Medias iguales                   : {np.isclose(a['mean'], b['mean'])}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

