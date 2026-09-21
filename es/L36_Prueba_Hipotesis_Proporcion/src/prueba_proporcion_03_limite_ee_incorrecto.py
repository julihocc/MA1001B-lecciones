"""
Lección 36 - Paso 3: Usar phat en el EE es el estadístico de prueba incorrecto
==============================================================================
NUEVO EN ESTE PASO: se_using_phat(), compare_statistics() y save_figure().

La Receta
Partir de prueba_proporcion_02_z_valor_p.py e introducir:
    1. se_using_phat()         el EE de Wald que no pertenece a esta prueba
    2. compare_statistics()    z correcto frente al z incorrecto
    3. save_figure()           comparación lado a lado de z y valor p

Una prueba de hipótesis de H0: p = p0 debe usar p0 en el error estándar.
Reemplazar p0 por phat es un EE de intervalo de confianza, no el estadístico
de prueba, y puede invertir la decisión con alfa = 0.05.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 200
X_LATE = 28
P0 = 0.10
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def sample_proportion(x: int = X_LATE, n: int = N) -> dict[str, float]:
    """Devuelve el conteo observado de banderas de retraso y la proporción muestral."""
    return {"n": float(n), "x": float(x), "phat": x / n, "p0": P0}


def se_under_h0(n: int = N, p0: float = P0) -> float:
    """Error estándar de phat cuando H0: p = p0 es verdadera."""
    return float(np.sqrt(p0 * (1.0 - p0) / n))


# --- NUEVO (1) se_using_phat() -----------------------------------------------
def se_using_phat(phat: float, n: int = N) -> float:
    """Error estándar de Wald que usa phat en lugar de p0."""
    return float(np.sqrt(phat * (1.0 - phat) / n))
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_statistics() ------------------------------------------
def compare_statistics(phat: float, p0: float, se0: float, se_hat: float) -> dict[str, float]:
    """Contrasta la prueba z basada en H0 con la z incorrecta basada en phat."""
    z_correct = (phat - p0) / se0
    z_wrong = (phat - p0) / se_hat
    p_correct = float(stats.norm.sf(z_correct))
    p_wrong = float(stats.norm.sf(z_wrong))
    return {
        "z_correct": float(z_correct),
        "z_wrong": float(z_wrong),
        "p_correct": p_correct,
        "p_wrong": p_wrong,
        "reject_correct": float(p_correct < ALPHA),
        "reject_wrong": float(p_wrong < ALPHA),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(se0: float, se_hat: float, comparison: dict[str, float]) -> Path:
    """Compara errores estándar, valores z y valores p correctos e incorrectos."""
    output_path = DIR_FIGURES / "prueba_proporcion_03_limite_ee_incorrecto.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6))

    se_labels = ["EE usa p0\n(prueba correcta)", "EE usa phat\n(prueba incorrecta)"]
    se_vals = [se0, se_hat]
    axes[0].bar(se_labels, se_vals, color=["#1A2E51", "#EC2661"], width=0.55)
    axes[0].set_ylabel("Error estándar")
    axes[0].set_title("¿Qué número pertenece al EE?")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for i, value in enumerate(se_vals):
        axes[0].text(i, value + 0.0004, f"{value:.4f}", ha="center", fontweight="bold")

    p_labels = ["valor p con p0", "valor p con phat"]
    p_vals = [comparison["p_correct"], comparison["p_wrong"]]
    axes[1].bar(p_labels, p_vals, color=["#1A2E51", "#EC2661"], width=0.55)
    axes[1].axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.3,
                    label="alfa = 0.05")
    axes[1].set_ylabel("Valor p de cola derecha")
    axes[1].set_title("Un EE incorrecto puede invertir la decisión")
    axes[1].set_ylim(0, 0.09)
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for i, value in enumerate(p_vals):
        axes[1].text(i, value + 0.002, f"{value:.4f}", ha="center", fontweight="bold")

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    summary = sample_proportion()
    se0 = se_under_h0()
    se_hat = se_using_phat(summary["phat"])
    comparison = compare_statistics(summary["phat"], summary["p0"], se0, se_hat)
    figure_path = save_figure(se0, se_hat, comparison)

    print("================================================================")
    print("LECCIÓN 36 - PASO 3: LÍMITE DEL EE INCORRECTO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Proporción muestral phat        : {summary['phat']:.6f}")
    print(f"EE correcto usando p0           : {se0:.6f}")
    print(f"EE incorrecto usando phat       : {se_hat:.6f}")
    print(f"z correcto (p0 en EE)           : {comparison['z_correct']:.6f}")
    print(f"z incorrecto (phat en EE)       : {comparison['z_wrong']:.6f}")
    print(f"Valor p correcto de cola derecha: {comparison['p_correct']:.6f}")
    print(f"Valor p incorrecto de cola der. : {comparison['p_wrong']:.6f}")
    print(
        "Decisión con EE correcto         : "
        f"{'rechazar H0' if comparison['reject_correct'] else 'no rechazar H0'}"
    )
    print(
        "Decisión con EE incorrecto       : "
        f"{'rechazar H0' if comparison['reject_wrong'] else 'no rechazar H0'}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

