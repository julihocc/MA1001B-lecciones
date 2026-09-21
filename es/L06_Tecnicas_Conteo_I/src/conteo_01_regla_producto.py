"""
Lección 06 - Paso 1: Regla del producto y espacio de configuraciones
====================================================================
NUEVO EN ESTE PASO: regla_producto(), generar_espacio_muestral() y
guardar_grafica().

La Receta
Enumera una configuración sintética de revisión de operaciones a través de
tres centros de cumplimiento, cuatro etapas de flujo de trabajo y dos tipos
de evidencia. Verifica que la regla del producto y la enumeración exhaustiva
producen ambas 24 resultados.

Ejecútalo:
    uv run es/L06_Tecnicas_Conteo_I/src/conteo_01_regla_producto.py
"""

from itertools import product
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURAS = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) regla_producto() -----------------------------------------------
def regla_producto(etapas: list[int]) -> int:
    """Calcula el tamaño del producto cartesiano de conjuntos finitos independientes."""
    total = 1
    for n in etapas:
        total *= n
    return total
# ------------------------------------------------------------------------------


# --- NUEVO (2) generar_espacio_muestral() -------------------------------------
def generar_espacio_muestral(
    centros: list[str], etapas: list[str], tipos_evidencia: list[str]
) -> list[tuple[str, str, str]]:
    """Genera exhaustivamente todas las ternas de configuración del espacio muestral."""
    return list(product(centros, etapas, tipos_evidencia))
# ------------------------------------------------------------------------------


# --- NUEVO (3) guardar_grafica() ----------------------------------------------
def guardar_grafica(conteo_por_centro: dict[str, int]) -> None:
    """Genera y guarda la distribución de configuraciones sin abrir una ventana."""
    fig, ax = plt.subplots(figsize=(7, 4))
    barras = ax.bar(
        list(conteo_por_centro.keys()),
        list(conteo_por_centro.values()),
        color="#1A2E51",
        edgecolor="#EC2661",
        linewidth=1.5,
    )
    ax.set_title(
        "Configuraciones de revisión por centro de cumplimiento",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Centro de cumplimiento", fontsize=11)
    ax.set_ylabel("Combinaciones de etapa y evidencia", fontsize=11)
    ax.set_ylim(0, 12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for barra in barras:
        altura = barra.get_height()
        ax.annotate(
            f"{altura}",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    ruta_salida = DIR_FIGURAS / "conteo_01_regla_producto.png"
    plt.savefig(ruta_salida, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    centros = ["Centro_A", "Centro_B", "Centro_C"]
    etapas_flujo = ["Recepción", "Picking", "Empaque", "Despacho"]
    tipos_evidencia = ["Registro", "Observación"]

    etapas = [len(centros), len(etapas_flujo), len(tipos_evidencia)]
    total_teorico = regla_producto(etapas)

    espacio_muestral = generar_espacio_muestral(centros, etapas_flujo, tipos_evidencia)
    total_exhaustivo = len(espacio_muestral)

    conteo_por_centro = {
        centro: sum(1 for item in espacio_muestral if item[0] == centro)
        for centro in centros
    }
    guardar_grafica(conteo_por_centro)

    print("================================================================")
    print("LECCIÓN 06 - PASO 1: REGLA DEL PRODUCTO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(
        "Etapas                          : "
        f"Centros ({len(centros)}) x Flujo ({len(etapas_flujo)}) "
        f"x Evidencia ({len(tipos_evidencia)})"
    )
    print(f"Total teórico por regla del producto : {total_teorico}")
    print(f"Total por enumeración exhaustiva     : {total_exhaustivo}")
    print(f"Coincidencia exacta                  : {total_teorico == total_exhaustivo}")
    print("Primeras 3 configuraciones :")
    for terna in espacio_muestral[:3]:
        print(f"   {terna}")
    print(f"Figura guardada en               : {DIR_FIGURAS / 'conteo_01_regla_producto.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

