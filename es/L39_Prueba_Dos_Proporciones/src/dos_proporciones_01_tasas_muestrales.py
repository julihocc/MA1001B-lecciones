"""
Lección 39 - Paso 1: Dos tasas muestrales de conversión
=======================================================
NUEVO EN ESTE PASO: sample_rates(), pooled_proportion() y save_figure().

La Receta
Una prueba A/B sintética de un aviso de pago registra nA = 400 visitantes
y xA = 72 conversiones en la versión A, frente a nB = 410 visitantes y
xB = 61 conversiones en la versión B. Las muestras son independientes, no
pareadas.

Ejecútalo:
    uv run es/L39_Prueba_Dos_Proporciones/src/dos_proporciones_01_tasas_muestrales.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 400
X_A = 72
N_B = 410
X_B = 61
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) sample_rates() ------------------------------------------------
def sample_rates() -> dict[str, float]:
    """Devuelve tamaños, conteos de conversión y proporciones muestrales."""
    return {
        "n_a": float(N_A),
        "x_a": float(X_A),
        "n_b": float(N_B),
        "x_b": float(X_B),
        "phat_a": X_A / N_A,
        "phat_b": X_B / N_B,
        "diff": X_A / N_A - X_B / N_B,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) pooled_proportion() -------------------------------------------
def pooled_proportion(x_a: int = X_A, n_a: int = N_A, x_b: int = X_B, n_b: int = N_B) -> dict[str, float]:
    """Combina las dos muestras bajo H0: pA = pB."""
    p_pool = (x_a + x_b) / (n_a + n_b)
    return {
        "p_pool": float(p_pool),
        "n_total": float(n_a + n_b),
        "x_total": float(x_a + x_b),
        "np_a": float(n_a * p_pool),
        "nq_a": float(n_a * (1.0 - p_pool)),
        "np_b": float(n_b * p_pool),
        "nq_b": float(n_b * (1.0 - p_pool)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(rates: dict[str, float]) -> Path:
    """Compara las dos tasas de conversión observadas."""
    output_path = DIR_FIGURES / "dos_proporciones_01_tasas_muestrales.png"
    labels = ["Versión A", "Versión B"]
    values = [rates["phat_a"], rates["phat_b"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=["#5B8DEF", "#EC2661"], width=0.55)
    ax.set_ylabel("Tasa de conversión")
    ax.set_title("Prueba A/B sintética: nA = 400, nB = 410")
    ax.set_ylim(0, 0.26)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value, count, n in zip(
        bars, values, [int(rates["x_a"]), int(rates["x_b"])], [int(rates["n_a"]), int(rates["n_b"])]
    ):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{count}/{n}\n{value:.3f}",
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
    rates = sample_rates()
    pooled = pooled_proportion()
    figure_path = save_figure(rates)

    print("================================================================")
    print("LECCIÓN 39 - PASO 1: DOS TASAS MUESTRALES DE CONVERSIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Versión A nA, xA                : {int(rates['n_a'])}, {int(rates['x_a'])}")
    print(f"Versión B nB, xB                : {int(rates['n_b'])}, {int(rates['x_b'])}")
    print(f"Proporción muestral p-sombrero A: {rates['phat_a']:.6f}")
    print(f"Proporción muestral p-sombrero B: {rates['phat_b']:.6f}")
    print(f"Diferencia p-sombrero A menos B : {rates['diff']:.6f}")
    print(f"Proporción combinada bajo H0    : {pooled['p_pool']:.6f}")
    print(f"nA * p-combinada                : {pooled['np_a']:.6f}")
    print(f"nB * p-combinada                : {pooled['np_b']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

