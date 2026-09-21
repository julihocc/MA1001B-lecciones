"""
Lección 41 - Paso 3: Una asociación significativa no es una afirmación causal
============================================================================
LA RECETA
Parte de independencia_02_chi_cuadrada.py e introduce:
    1. device_strata()          tablas de escritorio y móvil que suman a 2x3
    2. stratified_tests()       p-valores de independencia dentro de cada dispositivo
    3. save_figure()            tasas de conversión por canal, conjunto vs estratos

La tabla combinada puede rechazar independencia. Tras estratificar por
dispositivo, un confusor que no se asignó al azar, la asociación de canal
desaparece. Un ji-cuadrada significativo no es una afirmación causal.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
CHANNELS = ("Correo", "Búsqueda", "Redes")
DESKTOP = np.array([[30, 50, 8], [20, 30, 10]], dtype=float)
MOBILE = np.array([[10, 5, 10], [60, 40, 52]], dtype=float)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) device_strata() -----------------------------------------------
def device_strata() -> dict[str, np.ndarray]:
    """Devuelve tablas de dispositivo cuya suma es el registro 2 por 3 original."""
    combined = DESKTOP + MOBILE
    return {"desktop": DESKTOP.copy(), "mobile": MOBILE.copy(), "combined": combined}
# ------------------------------------------------------------------------------


# --- NUEVO (2) stratified_tests() --------------------------------------------
def stratified_tests(tables: dict[str, np.ndarray]) -> dict[str, float]:
    """p-valores ji-cuadrada en conjunto y dentro de cada estrato de dispositivo."""
    results = {}
    for name, table in tables.items():
        chi2, p_value, df, _ = stats.chi2_contingency(table, correction=False)
        results[f"{name}_chi2"] = float(chi2)
        results[f"{name}_p"] = float(p_value)
        results[f"{name}_df"] = float(df)
        rates = table[0] / table.sum(axis=0)
        results[f"{name}_rate_email"] = float(rates[0])
        results[f"{name}_rate_search"] = float(rates[1])
        results[f"{name}_rate_social"] = float(rates[2])
    return results
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(results: dict[str, float]) -> Path:
    """Tasas de conversión por canal en conjunto y dentro de estratos."""
    output_path = DIR_FIGURES / "independencia_03_limite_no_causalidad.png"
    x = np.arange(len(CHANNELS))
    width = 0.25
    overall = [
        results["combined_rate_email"],
        results["combined_rate_search"],
        results["combined_rate_social"],
    ]
    desktop = [
        results["desktop_rate_email"],
        results["desktop_rate_search"],
        results["desktop_rate_social"],
    ]
    mobile = [
        results["mobile_rate_email"],
        results["mobile_rate_search"],
        results["mobile_rate_social"],
    ]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - width, overall, width, color="#EC2661", label="Conjunto")
    ax.bar(x, desktop, width, color="#1A2E51", label="Escritorio")
    ax.bar(x + width, mobile, width, color="#5B8DEF", label="Móvil")
    ax.set_xticks(x, CHANNELS)
    ax.set_ylabel("Tasa de conversión")
    ax.set_title("La asociación de canal desaparece dentro de estratos de dispositivo")
    ax.set_ylim(0, 0.85)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    tables = device_strata()
    results = stratified_tests(tables)
    figure_path = save_figure(results)

    print("================================================================")
    print("LECCIÓN 41 - PASO 3: LÍMITE DE NO CAUSALIDAD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"p-valor ji-cuadrada conjunto    : {results['combined_p']:.6f}")
    print(f"p-valor ji-cuadrada escritorio  : {results['desktop_p']:.6f}")
    print(f"p-valor ji-cuadrada móvil       : {results['mobile_p']:.6f}")
    print(f"Conversión conjunto Búsqueda    : {results['combined_rate_search']:.6f}")
    print(f"Conversión conjunto Redes       : {results['combined_rate_social']:.6f}")
    print(f"Conversión escritorio Búsqueda  : {results['desktop_rate_search']:.6f}")
    print(f"Conversión móvil Redes          : {results['mobile_rate_social']:.6f}")
    print("Asignación aleatoria del canal  : no")
    print("Afirmación causal desde chi2    : no justificada")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

