"""
Lección 06 - Paso 2: Permutaciones y asignaciones ordenadas
==========================================================
NUEVO EN ESTE PASO: permutaciones_lineales(), simular_asignaciones() y
guardar_grafica_crecimiento().

La Receta
CAMBIOS RESPECTO A conteo_01_regla_producto.py
Introdúcelos en este orden:
    1. permutaciones_lineales()        calcula asignaciones ordenadas sin reemplazo
    2. simular_asignaciones()          enumera asignaciones para tres roles distintos
    3. guardar_grafica_crecimiento()   muestra el crecimiento al aumentar los roles

Ejecútalo:
    uv run es/L06_Tecnicas_Conteo_I/src/conteo_02_permutaciones.py
"""

from itertools import permutations
import math
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURAS = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) permutaciones_lineales() ---------------------------------------
def permutaciones_lineales(n: int, k: int) -> int:
    """Calcula P(n, k) = n! / (n - k)! usando el módulo estándar math."""
    return math.perm(n, k)
# ------------------------------------------------------------------------------


# --- NUEVO (2) simular_asignaciones() -----------------------------------------
def simular_asignaciones(elementos: list[str], k: int) -> list[tuple[str, ...]]:
    """Genera todos los arreglos ordenados de k elementos sin reemplazo."""
    return list(permutations(elementos, k))
# ------------------------------------------------------------------------------


# --- NUEVO (3) guardar_grafica_crecimiento() ----------------------------------
def guardar_grafica_crecimiento(n_fijo: int) -> None:
    """Grafica la explosión de permutaciones conforme aumenta el tamaño k."""
    ks = list(range(1, n_fijo + 1))
    valores = [math.perm(n_fijo, k) for k in ks]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ks, valores, marker="o", color="#0039A6", linewidth=2, markersize=7)
    ax.set_title(f"Curva de crecimiento de permutaciones P({n_fijo}, k)", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Tamaño de selección k (roles asignados)", fontsize=11)
    ax.set_ylabel("Total de permutaciones", fontsize=10)
    ax.set_xticks(ks)
    ax.grid(True, linestyle="--", alpha=0.5)

    for k, val in zip(ks, valores):
        ax.annotate(f"{val}", xy=(k, val), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=9)

    plt.tight_layout()
    ruta_salida = DIR_FIGURAS / "conteo_02_permutaciones.png"
    plt.savefig(ruta_salida, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    analistas = ["Analista_A", "Analista_B", "Analista_C", "Analista_D", "Analista_E", "Analista_F"]
    n = len(analistas)
    k = 3

    total_teorico = permutaciones_lineales(n, k)
    asignaciones = simular_asignaciones(analistas, k)
    total_exhaustivo = len(asignaciones)

    guardar_grafica_crecimiento(n)

    print("================================================================")
    print("LECCIÓN 06 - PASO 2: PERMUTACIONES (EL ORDEN IMPORTA)")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Pool disponible n = {n} analistas, roles a asignar k = {k}")
    print(f"Fórmula teórica P({n}, {k})      : {total_teorico}")
    print(f"Permutaciones generadas realmente: {total_exhaustivo}")
    print(f"Coincidencia exacta              : {total_teorico == total_exhaustivo}")
    print("Primeras 3 asignaciones ordenadas (Líder, Validación, Reportes):")
    for terna in asignaciones[:3]:
        print(f"   {terna}")
    print(f"Figura guardada en              : {DIR_FIGURAS / 'conteo_02_permutaciones.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

