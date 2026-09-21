"""
Lección 29 - Paso 2: Intervalo de confianza de Wald para una proporción
======================================================================
La Receta
Partir de prop_ci_01_sample_proportion.py e introducir:
    1. success_failure_check()   n phat y n(1-phat) versus el umbral 5
    2. wald_interval()           phat +/- 1.96 * sqrt(phat(1-phat)/n)
    3. save_figure()             dibujar el intervalo de Wald al 95% para p

Se reconstruye la misma instantánea x = 27, n = 150 a partir de constantes.
No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 150
X_SUCCESS = 27
Z_STAR = 1.96
CUTOFF = 5.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) success_failure_check() ---------------------------------------
def success_failure_check(n: int, x: int) -> dict[str, float]:
    """Verifica las condiciones np y n(1-p) usando phat en lugar de p."""
    phat = x / n
    n_phat = n * phat
    n_qhat = n * (1.0 - phat)
    return {
        "phat": phat,
        "n_phat": n_phat,
        "n_qhat": n_qhat,
        "cutoff": CUTOFF,
        "conditions_ok": float(n_phat >= CUTOFF and n_qhat >= CUTOFF),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) wald_interval() -----------------------------------------------
def wald_interval(n: int, x: int, z_star: float = Z_STAR) -> dict[str, float]:
    """Construye el intervalo de Wald de libro phat +/- z* EE_hat."""
    phat = x / n
    se = np.sqrt(phat * (1.0 - phat) / n)
    margin = z_star * se
    lower = phat - margin
    upper = phat + margin
    return {
        "se": float(se),
        "margin": float(margin),
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(phat: float, interval: dict[str, float]) -> Path:
    """Guarda el intervalo de Wald alrededor de la proporción muestral."""
    output_path = DIR_FIGURES / "prop_ci_02_wald_interval.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        [phat],
        [1],
        xerr=[[phat - interval["lower"]], [interval["upper"] - phat]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.set_yticks([1])
    ax.set_yticklabels(["Intervalo de Wald al 95%"])
    ax.set_xlabel("Proporción poblacional p")
    ax.set_title("Intervalo de Wald: phat +/- 1.96 * sqrt(phat(1-phat)/n)")
    ax.set_xlim(0.0, 0.40)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        phat,
        1.18,
        f"[{interval['lower']:.4f}, {interval['upper']:.4f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    check = success_failure_check(N, X_SUCCESS)
    interval = wald_interval(N, X_SUCCESS)
    figure_path = save_figure(check["phat"], interval)

    print("================================================================")
    print("LECCIÓN 29 - PASO 2: INTERVALO DE CONFIANZA DE WALD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Éxitos x                        : {X_SUCCESS}")
    print(f"Proporción muestral phat        : {check['phat']:.6f}")
    print(f"n * phat                        : {check['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {check['n_qhat']:.6f}")
    print(f"Umbral de la verificación       : {check['cutoff']:.1f}")
    print(f"Condiciones satisfechas         : {'Sí' if check['conditions_ok'] else 'No'}")
    print(f"z-estrella de libro             : {Z_STAR:.6f}")
    print(f"Error estándar                  : {interval['se']:.6f}")
    print(f"Margen de error                 : {interval['margin']:.6f}")
    print(f"Límite inferior                 : {interval['lower']:.6f}")
    print(f"Límite superior                 : {interval['upper']:.6f}")
    print(f"Anchura del intervalo           : {interval['width']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

