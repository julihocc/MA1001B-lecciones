"""
Lección 15 - Paso 3: La misma media puede ocultar colas distintas
================================================================
NUEVO EN ESTE PASO: policy_pmf(), overlay_pmfs() y save_figure().

La Receta
CAMBIOS RESPECTO A riesgo_binomial_02_probabilidades_cola.py
Introdúcelos en este orden:
    1. policy_pmf()         FMP binomial completa de una política
    2. overlay_pmfs()       Política A frente a Política B en el mismo eje
    3. save_figure()        ambas FMP con la región x >= 8 marcada

El límite es que igualar np no es igualar el riesgo. La Política A concentra
más masa en conteos extremos aunque ambas medias valgan 2.

Ejecútalo:
    uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_03_misma_media_colas_distintas.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POLICY_A = {"name": "A", "n": 50, "p": 0.04}
POLICY_B = {"name": "B", "n": 20, "p": 0.10}
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def tail_probability(n: int, p: float, threshold: int = 3) -> float:
    """Devuelve P(X >= threshold) para X ~ Binomial(n, p)."""
    return float(stats.binom.sf(threshold - 1, n=n, p=p))


# --- NUEVO (1) policy_pmf() --------------------------------------------------
def policy_pmf(n: int, p: float, max_x: int = 12) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve valores de x y masas binomiales hasta max_x."""
    xs = np.arange(0, max_x + 1)
    return xs, stats.binom.pmf(xs, n=n, p=p)
# ------------------------------------------------------------------------------


# --- NUEVO (2) overlay_pmfs() ------------------------------------------------
def overlay_pmfs() -> dict[str, np.ndarray | float]:
    """Devuelve ambas FMP y ambas probabilidades de cola."""
    xs, pmf_a = policy_pmf(POLICY_A["n"], POLICY_A["p"])
    _, pmf_b = policy_pmf(POLICY_B["n"], POLICY_B["p"])
    return {
        "xs": xs,
        "pmf_a": pmf_a,
        "pmf_b": pmf_b,
        "tail3_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 3),
        "tail3_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 3),
        "tail8_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 8),
        "tail8_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 8),
        "p0_a": float(stats.binom.pmf(0, n=POLICY_A["n"], p=POLICY_A["p"])),
        "p0_b": float(stats.binom.pmf(0, n=POLICY_B["n"], p=POLICY_B["p"])),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(overlay: dict[str, np.ndarray | float]) -> Path:
    """Superpone las dos FMP y sombrea la cola x >= 8."""
    output_path = DIR_FIGURES / "riesgo_binomial_03_misma_media_colas_distintas.png"
    xs = overlay["xs"]
    width = 0.38

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.axvspan(7.5, 12.5, color="#F8D5DE", alpha=0.55, label="x >= 8")
    ax.bar(
        xs - width / 2,
        overlay["pmf_a"],
        width=width,
        color="#1A2E51",
        label="Política A",
    )
    ax.bar(
        xs + width / 2,
        overlay["pmf_b"],
        width=width,
        color="#EC2661",
        label="Política B",
    )
    ax.set_xlabel("Conteo de defectos x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Igualar np oculta una cola lejana más pesada en la Política A")
    ax.set_xticks(xs)
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    overlay = overlay_pmfs()
    figure_path = save_figure(overlay)

    print("================================================================")
    print("LECCIÓN 15 - PASO 3: MISMA MEDIA, COLAS DISTINTAS")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Media compartida np              : {POLICY_A['n'] * POLICY_A['p']:.6f}")
    print(f"Política A P(X = 0)              : {overlay['p0_a']:.6f}")
    print(f"Política B P(X = 0)              : {overlay['p0_b']:.6f}")
    print(f"Política A P(X >= 3)             : {overlay['tail3_a']:.6f}")
    print(f"Política B P(X >= 3)             : {overlay['tail3_b']:.6f}")
    print(f"Política A P(X >= 8)             : {overlay['tail8_a']:.6f}")
    print(f"Política B P(X >= 8)             : {overlay['tail8_b']:.6f}")
    print(
        "Razón de cola lejana A/B          : "
        f"{overlay['tail8_a'] / overlay['tail8_b']:.6f}"
    )
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

