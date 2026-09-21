"""
Lección 42 - Paso 2: Prueba ji-cuadrada de homogeneidad
======================================================
LA RECETA
Parte de homogeneidad_01_tres_muestras.py e introduce:
    1. expected_under_homogeneity()  E = total de fila * total de columna / n
    2. homogeneity_test()            la misma aritmética chi2 que independencia
    3. save_figure()                 contribuciones celulares de tres sitios

H0 afirma que los tres sitios muestreados de forma independiente comparten
una mezcla de canal. El estadístico coincide con independencia; la historia
de muestreo no. No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SITES = ("Norte", "Centro", "Sur")
CATEGORIES = ("Teléfono", "Chat", "Correo")
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) expected_under_homogeneity() ----------------------------------
def expected_under_homogeneity(observed: np.ndarray) -> np.ndarray:
    """Conteos esperados cuando muestras independientes comparten una mezcla."""
    n = observed.sum()
    return np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n
# ------------------------------------------------------------------------------


# --- NUEVO (2) homogeneity_test() --------------------------------------------
def homogeneity_test(observed: np.ndarray) -> dict[str, float]:
    """Prueba de homogeneidad ji-cuadrada con df = (filas - 1)(columnas - 1)."""
    chi2, p_value, df, expected = stats.chi2_contingency(observed, correction=False)
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "df": float(df),
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),
        "min_expected": float(np.min(expected)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(observed: np.ndarray, expected: np.ndarray) -> Path:
    """Mapa de calor de contribuciones celulares de homogeneidad."""
    output_path = DIR_FIGURES / "homogeneidad_02_chi_cuadrada.png"
    contributions = (observed - expected) ** 2 / expected
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    image = ax.imshow(contributions, cmap="Reds", vmin=0, vmax=contributions.max())
    ax.set_xticks(np.arange(len(CATEGORIES)), CATEGORIES)
    ax.set_yticks(np.arange(len(SITES)), SITES)
    ax.set_title("Contribuciones celulares de homogeneidad, df = 4")
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
    expected = expected_under_homogeneity(OBSERVED)
    test = homogeneity_test(OBSERVED)
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(OBSERVED, expected)

    print("================================================================")
    print("LECCIÓN 42 - PASO 2: HOMOGENEIDAD JI-CUADRADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Hipótesis                       : H0: los tres sitios comparten una mezcla")
    print(
        "Esperados Norte                 : "
        + ", ".join(f"{value:.3f}" for value in expected[0])
    )
    print(
        "Esperados Centro                : "
        + ", ".join(f"{value:.3f}" for value in expected[1])
    )
    print(
        "Esperados Sur                   : "
        + ", ".join(f"{value:.3f}" for value in expected[2])
    )
    print(f"Conteo esperado mínimo          : {test['min_expected']:.6f}")
    print(f"Estadístico ji-cuadrada         : {test['chi2']:.6f}")
    print(f"Grados de libertad (r-1)(c-1)   : {int(test['df'])}")
    print(f"p-valor de cola derecha         : {test['p_value']:.6f}")
    print(f"chi2* crítica (alpha = 0.05)    : {test['critical']:.6f}")
    print(f"Decisión a alpha = 0.05         : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

