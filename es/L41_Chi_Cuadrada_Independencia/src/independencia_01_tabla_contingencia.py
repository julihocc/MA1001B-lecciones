"""
Lección 41 - Paso 1: Una tabla de contingencia 2 por 3
======================================================
NUEVO EN ESTE PASO: observed_table(), expected_table() y save_figure().

La Receta
Un registro de pago sintético clasifica n = 325 visitantes por conversión
(sí o no) y por canal de adquisición (correo, búsqueda, redes). Bajo
independencia, los conteos esperados de celda son total de fila por total
de columna sobre n.

Ejecútalo:
    uv run es/L41_Chi_Cuadrada_Independencia/src/independencia_01_tabla_contingencia.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
CHANNELS = ("Correo", "Búsqueda", "Redes")
OUTCOMES = ("Convertido", "No convertido")
OBSERVED = np.array([[40, 55, 18], [80, 70, 62]], dtype=float)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) observed_table() ----------------------------------------------
def observed_table() -> dict[str, np.ndarray | float]:
    """Devuelve la tabla 2 por 3 observada y sus márgenes."""
    row_totals = OBSERVED.sum(axis=1)
    col_totals = OBSERVED.sum(axis=0)
    return {
        "observed": OBSERVED.copy(),
        "row_totals": row_totals,
        "col_totals": col_totals,
        "n": float(OBSERVED.sum()),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) expected_table() ----------------------------------------------
def expected_table(observed: np.ndarray) -> dict[str, np.ndarray | float]:
    """Conteos esperados de independencia E = total fila * total columna / n."""
    n = observed.sum()
    expected = np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n
    return {
        "expected": expected,
        "min_expected": float(np.min(expected)),
        "all_expected_ge_5": float(np.all(expected >= 5.0)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(observed: np.ndarray) -> Path:
    """Barras agrupadas de conteos de conversión por canal de adquisición."""
    output_path = DIR_FIGURES / "independencia_01_tabla_contingencia.png"
    x = np.arange(len(CHANNELS))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - width / 2, observed[0], width, color="#EC2661", label="Convertido")
    ax.bar(x + width / 2, observed[1], width, color="#1A2E51", label="No convertido")
    ax.set_xticks(x, CHANNELS)
    ax.set_ylabel("Conteo de visitantes")
    ax.set_title("Tabla sintética 2 por 3 de pago, n = 325")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    observed = observed_table()
    expected = expected_table(observed["observed"])
    figure_path = save_figure(observed["observed"])

    print("================================================================")
    print("LECCIÓN 41 - PASO 1: TABLA DE CONTINGENCIA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {int(observed['n'])}")
    print("Observados convertidos          : 40, 55, 18")
    print("Observados no convertidos       : 80, 70, 62")
    print(
        "Totales de fila                 : "
        + ", ".join(f"{value:.0f}" for value in observed["row_totals"])
    )
    print(
        "Totales de columna              : "
        + ", ".join(f"{value:.0f}" for value in observed["col_totals"])
    )
    print(
        "Esperados convertidos           : "
        + ", ".join(f"{value:.3f}" for value in expected["expected"][0])
    )
    print(
        "Esperados no convertidos        : "
        + ", ".join(f"{value:.3f}" for value in expected["expected"][1])
    )
    print(f"Conteo esperado mínimo          : {expected['min_expected']:.6f}")
    print(
        "Todos los esperados >= 5        : "
        f"{'sí' if expected['all_expected_ge_5'] else 'no'}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

