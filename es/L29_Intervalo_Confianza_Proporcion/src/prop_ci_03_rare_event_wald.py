"""
Lección 29 - Paso 3: Los eventos raros hacen engañoso el intervalo de Wald
=========================================================================
La Receta
Partir de prop_ci_02_wald_interval.py e introducir:
    1. rare_event_snapshot()     x = 3 de n = 150 resoluciones en primer contacto
    2. compare_wald_and_wilson() Wald puede ser negativo; Wilson permanece en (0, 1)
    3. save_figure()             contrastar los dos intervalos en el mismo eje

Límite: un evento raro con x pequeña falla la verificación éxito-fracaso.
El intervalo de Wald puede entonces reportar un límite inferior negativo,
que no es una proporción válida. El intervalo de Wilson se muestra solo
como contraste diagnóstico.
"""

from pathlib import Path

import matplotlib
import numpy as np
from statsmodels.stats.proportion import proportion_confint

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 150
X_RARE = 3
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) rare_event_snapshot() -----------------------------------------
def rare_event_snapshot(n: int = N, x: int = X_RARE) -> dict[str, float]:
    """Construye los conteos de evento raro que rompen las condiciones de Wald."""
    phat = x / n
    return {
        "n": float(n),
        "x": float(x),
        "phat": phat,
        "n_phat": n * phat,
        "n_qhat": n * (1.0 - phat),
        "conditions_ok": float(n * phat >= 5 and n * (1.0 - phat) >= 5),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_wald_and_wilson() -------------------------------------
def compare_wald_and_wilson(n: int, x: int) -> dict[str, float]:
    """Calcula intervalos de Wald y Wilson al 95% para la misma instantánea rara."""
    phat = x / n
    se = np.sqrt(phat * (1.0 - phat) / n)
    wald_lower = phat - Z_STAR * se
    wald_upper = phat + Z_STAR * se
    wilson_lower, wilson_upper = proportion_confint(
        x, n, alpha=0.05, method="wilson"
    )
    return {
        "se": float(se),
        "wald_lower": float(wald_lower),
        "wald_upper": float(wald_upper),
        "wald_negative_lower": float(wald_lower < 0.0),
        "wilson_lower": float(wilson_lower),
        "wilson_upper": float(wilson_upper),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    phat: float,
    comparison: dict[str, float],
) -> Path:
    """Contrasta el intervalo de Wald inválido con el diagnóstico de Wilson."""
    output_path = DIR_FIGURES / "prop_ci_03_rare_event_wald.png"
    labels = ["Wald (x rara=3)", "Wilson (diagnóstico)"]
    lowers = [comparison["wald_lower"], comparison["wilson_lower"]]
    uppers = [comparison["wald_upper"], comparison["wilson_upper"]]
    centers = [phat, phat]
    xerr = np.array(
        [
            [phat - lowers[0], phat - lowers[1]],
            [uppers[0] - phat, uppers[1] - phat],
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
    ax.axvline(0.0, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label="Frontera p = 0")
    ax.set_yticks([1.0, 0.0])
    ax.set_yticklabels(labels)
    ax.set_xlabel("Proporción poblacional p")
    ax.set_title("Eventos raros: Wald puede cruzar por debajo de cero")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_ylim(-0.7, 1.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    rare = rare_event_snapshot()
    comparison = compare_wald_and_wilson(N, X_RARE)
    figure_path = save_figure(rare["phat"], comparison)

    print("================================================================")
    print("LECCIÓN 29 - PASO 3: LÍMITE DE WALD CON EVENTO RARO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Éxitos raros x                  : {X_RARE}")
    print(f"Proporción muestral phat        : {rare['phat']:.6f}")
    print(f"n * phat                        : {rare['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {rare['n_qhat']:.6f}")
    print(f"Condiciones satisfechas         : {'Sí' if rare['conditions_ok'] else 'No'}")
    print(f"Error estándar de Wald          : {comparison['se']:.6f}")
    print(f"Límite inferior de Wald         : {comparison['wald_lower']:.6f}")
    print(f"Límite superior de Wald         : {comparison['wald_upper']:.6f}")
    print(
        "El límite inferior de Wald es negativo: "
        f"{'Sí' if comparison['wald_negative_lower'] else 'No'}"
    )
    print(f"Límite inferior de Wilson       : {comparison['wilson_lower']:.6f}")
    print(f"Límite superior de Wilson       : {comparison['wilson_upper']:.6f}")
    print("Límite                          : una x pequeña hace que Wald sea engañoso")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

