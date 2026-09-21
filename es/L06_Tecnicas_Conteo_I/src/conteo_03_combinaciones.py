"""
Lección 06 - Paso 3: Combinaciones y subconjuntos no ordenados
=============================================================
NUEVO EN ESTE PASO: combinaciones_subconjunto(), simular_comites() y
guardar_grafica_comparativa().

La Receta
CAMBIOS RESPECTO A conteo_02_permutaciones.py
Introdúcelos en este orden:
    1. combinaciones_subconjunto()      calcula selecciones cuando el orden no importa
    2. simular_comites()                enumera los paneles únicos de tres personas
    3. guardar_grafica_comparativa()    compara conteos ordenados y no ordenados

Ejecútalo:
    uv run es/L06_Tecnicas_Conteo_I/src/conteo_03_combinaciones.py
"""

from itertools import combinations
import math
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURAS = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) combinaciones_subconjunto() ------------------------------------
def combinaciones_subconjunto(n: int, k: int) -> int:
    """Calcula C(n, k) = binom(n, k) donde el orden no importa."""
    return math.comb(n, k)
# ------------------------------------------------------------------------------


# --- NUEVO (2) simular_comites() ----------------------------------------------
def simular_comites(elementos: list[str], k: int) -> list[tuple[str, ...]]:
    """Genera todos los subconjuntos únicos de tamaño k."""
    return list(combinations(elementos, k))
# ------------------------------------------------------------------------------


# --- NUEVO (3) guardar_grafica_comparativa() ----------------------------------
def guardar_grafica_comparativa(n_fijo: int) -> None:
    """Compara P(n, k) contra C(n, k) y muestra el factor de reducción k!."""
    ks = list(range(1, n_fijo + 1))
    perms = [math.perm(n_fijo, k) for k in ks]
    combs = [math.comb(n_fijo, k) for k in ks]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ks, perms, marker="o", color="#0039A6", label="Permutaciones P(n, k)", linewidth=2)
    ax.plot(ks, combs, marker="s", color="#EC2661", label="Combinaciones C(n, k)", linewidth=2)
    ax.set_title(f"Permutaciones vs combinaciones para n = {n_fijo}", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Tamaño del subconjunto k", fontsize=10)
    ax.set_ylabel("Cardinalidad", fontsize=10)
    ax.set_xticks(ks)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    ruta_salida = DIR_FIGURAS / "conteo_03_combinaciones.png"
    plt.savefig(ruta_salida, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    analistas = ["Analista_A", "Analista_B", "Analista_C", "Analista_D", "Analista_E", "Analista_F"]
    n = len(analistas)
    k = 3

    total_perms = math.perm(n, k)
    total_combs = combinaciones_subconjunto(n, k)

    comites = simular_comites(analistas, k)
    total_exhaustivo = len(comites)

    guardar_grafica_comparativa(n)

    print("================================================================")
    print("LECCIÓN 06 - PASO 3: COMBINACIONES (EL ORDEN NO IMPORTA)")
    print("================================================================")
    print("Aviso de datos sintéticos      : No se usan datos reales de empresa")
    print(f"Pool disponible n = {n}, tamaño del panel k = {k}")
    print(f"Total de permutaciones P({n}, {k}) : {total_perms}")
    print(f"Total de combinaciones C({n}, {k}) : {total_combs}")
    print(f"Combinaciones generadas realmente : {total_exhaustivo}")
    print(f"Factor de reducción (k!)          : {total_perms // total_combs} (debe ser {math.factorial(k)})")
    print(f"Coincidencia exacta               : {total_combs == total_exhaustivo}")
    print("Primeros 3 paneles:")
    for panel in comites[:3]:
        print(f"   {panel}")
    print(f"Figura guardada en               : {DIR_FIGURAS / 'conteo_03_combinaciones.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

