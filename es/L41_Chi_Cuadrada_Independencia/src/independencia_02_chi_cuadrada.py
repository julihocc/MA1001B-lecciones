"""
Lección 41 - Paso 2: Prueba ji-cuadrada de independencia
=======================================================
LA RECETA
Parte de independencia_01_tabla_contingencia.py e introduce:
    1. chi_square_statistic()   suma de (O - E)^2 / E sobre las seis celdas
    2. independence_test()      df = (r-1)(c-1), p-valor, V de Cramer
    3. save_figure()            mapa de calor de contribuciones celulares

La misma tabla sintética 2 por 3 de pago se reconstruye desde constantes.
No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
CHANNELS = ("Correo", "Búsqueda", "Redes")
OUTCOMES = ("Convertido", "No convertido")
OBSERVED = np.array([[40, 55, 18], [80, 70, 62]], dtype=float)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def expected_table(observed: np.ndarray) -> np.ndarray:
    """Conteos esperados de independencia E = total fila * total columna / n."""
    n = observed.sum()
    return np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n


# --- NUEVO (1) chi_square_statistic() ----------------------------------------
def chi_square_statistic(observed: np.ndarray, expected: np.ndarray) -> dict[str, np.ndarray | float]:
    """Devuelve contribuciones celulares y el total ji-cuadrada."""
    contributions = (observed - expected) ** 2 / expected
    return {"contributions": contributions, "chi2": float(np.sum(contributions))}
# ------------------------------------------------------------------------------


# --- NUEVO (2) independence_test() -------------------------------------------
def independence_test(observed: np.ndarray) -> dict[str, float]:
    """Prueba ji-cuadrada de independencia más V de Cramer."""
    scipy_chi2, p_value, df, expected = stats.chi2_contingency(observed, correction=False)
    n = observed.sum()
    cramer_v = float(np.sqrt(scipy_chi2 / (n * (min(observed.shape) - 1))))
    return {
        "chi2": float(scipy_chi2),
        "p_value": float(p_value),
        "df": float(df),
        "cramer_v": cramer_v,
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),
        "n": float(n),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(contributions: np.ndarray) -> Path:
    """Mapa de calor de (O - E)^2 / E en la tabla 2 por 3."""
    output_path = DIR_FIGURES / "independencia_02_chi_cuadrada.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    image = ax.imshow(contributions, cmap="Reds", vmin=0, vmax=contributions.max())
    ax.set_xticks(np.arange(len(CHANNELS)), CHANNELS)
    ax.set_yticks(np.arange(len(OUTCOMES)), OUTCOMES)
    ax.set_title("Contribuciones celulares ji-cuadrada, df = 2")
    for i in range(contributions.shape[0]):
        for j in range(contributions.shape[1]):
            ax.text(
                j, i, f"{contributions[i, j]:.2f}",
                ha="center", va="center", color="#1A2E51", fontweight="bold",
            )
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="(O - E)^2 / E")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    expected = expected_table(OBSERVED)
    parts = chi_square_statistic(OBSERVED, expected)
    test = independence_test(OBSERVED)
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(parts["contributions"])

    print("================================================================")
    print("LECCIÓN 41 - PASO 2: INDEPENDENCIA JI-CUADRADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Hipótesis                       : H0: conversión independiente del canal")
    print(f"Estadístico ji-cuadrada         : {test['chi2']:.6f}")
    print(f"Grados de libertad (r-1)(c-1)   : {int(test['df'])}")
    print(f"p-valor de cola derecha         : {test['p_value']:.6f}")
    print(f"chi2* crítica (alpha = 0.05)    : {test['critical']:.6f}")
    print(f"V de Cramer                     : {test['cramer_v']:.6f}")
    print(f"Decisión a alpha = 0.05         : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

