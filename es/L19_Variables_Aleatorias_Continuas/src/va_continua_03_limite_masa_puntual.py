"""
Lección 19 - Paso 3: Un punto continuo no carga probabilidad
===========================================================
NUEVO EN ESTE PASO: shrinking_windows(), cdf_has_no_jump() y save_figure().

La Receta
CAMBIOS RESPECTO A va_continua_02_probabilidad_intervalo.py
Introdúcelos en este orden:
    1. shrinking_windows()      P(|X - c| < h) colapsa hacia 0
    2. cdf_has_no_jump()        F es continua, de modo que P(X = c) = 0
    3. save_figure()            grafica la FDA sin salto en la moda

El mismo modelo triangular de tiempo de servicio se reconstruye. El límite es
que P(X = c) = 0 para cada minuto individual c, incluso la moda.

Ejecútalo:
    uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_03_limite_masa_puntual.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
A = 2.0
B = 14.0
MODE = 6.0
WINDOWS = (0.50, 0.10, 0.01)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def service_time_model():
    """Devuelve el modelo triangular del tiempo de servicio sintético en [2, 14]."""
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)


# --- NUEVO (1) shrinking_windows() -------------------------------------------
def shrinking_windows(model, center: float) -> dict[str, float]:
    """Calcula P(|X - center| < h) para ventanas sucesivamente más pequeñas."""
    results: dict[str, float] = {}
    for half_width in WINDOWS:
        left = center - half_width
        right = center + half_width
        results[f"h_{half_width:.2f}"] = float(
            model.cdf(right) - model.cdf(left)
        )
    return results
# ------------------------------------------------------------------------------


# --- NUEVO (2) cdf_has_no_jump() ---------------------------------------------
def cdf_has_no_jump(model, center: float) -> dict[str, float]:
    """Muestra que F no tiene salto en la moda, de modo que un punto tiene masa 0."""
    f_center = float(model.cdf(center))
    f_left = float(model.cdf(center - 1e-9))
    return {
        "F_at_mode": f_center,
        "F_just_left": f_left,
        "jump": f_center - f_left,
        "P_X_equals_mode": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model, windows: dict[str, float]) -> Path:
    """Grafica la FDA continua y las probabilidades de ventanas que se encogen."""
    output_path = DIR_FIGURES / "va_continua_03_limite_masa_puntual.png"
    x = np.linspace(A, B, 400)
    y = model.cdf(x)
    labels = ["h = 0.50", "h = 0.10", "h = 0.01"]
    values = [windows["h_0.50"], windows["h_0.10"], windows["h_0.01"]]

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))

    axes[0].plot(x, y, color="#1A2E51", lw=2.2)
    axes[0].axvline(MODE, color="#EC2661", ls="--", lw=1.3)
    axes[0].plot(MODE, model.cdf(MODE), "o", color="#EC2661")
    axes[0].set_xlabel("Tiempo de servicio (minutos)")
    axes[0].set_ylabel("F(x) = P(X <= x)")
    axes[0].set_title("La FDA no tiene salto en x = 6")
    axes[0].set_xlim(A, B)
    axes[0].set_ylim(0, 1.05)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    bars = axes[1].bar(labels, values, color=["#1A2E51", "#5B8DEF", "#EC2661"],
                       width=0.62)
    axes[1].set_ylabel("P(|X - 6| < h)")
    axes[1].set_title("Las ventanas que se encogen colapsan a 0")
    axes[1].set_ylim(0, 0.18)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4f}",
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
    model = service_time_model()
    windows = shrinking_windows(model, MODE)
    jump = cdf_has_no_jump(model, MODE)
    figure_path = save_figure(model, windows)

    print("================================================================")
    print("LECCIÓN 19 - PASO 3: LÍMITE DE MASA PUNTUAL")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Centro c                         : {MODE:.1f}")
    print(f"P(|X - 6| < 0.50)                : {windows['h_0.50']:.6f}")
    print(f"P(|X - 6| < 0.10)                : {windows['h_0.10']:.6f}")
    print(f"P(|X - 6| < 0.01)                : {windows['h_0.01']:.6f}")
    print(f"F(6)                             : {jump['F_at_mode']:.6f}")
    print(f"F(6-)                            : {jump['F_just_left']:.6f}")
    print(f"Salto F(6) - F(6-)               : {jump['jump']:.6f}")
    print(f"P(X = 6)                         : {jump['P_X_equals_mode']:.6f}")
    print("Límite: un punto continuo carga probabilidad 0")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

