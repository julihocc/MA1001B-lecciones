"""
Lección 11 - Paso 2: Fórmula de Bayes y la posterior
====================================================
NUEVO EN ESTE PASO: bayes_numerator(), bayes_denominator() y posterior().

CAMBIOS RESPECTO A bayes_01_priori_verosimilitud.py
La Receta
---------
Introduce estos cambios en este orden:
    1. bayes_numerator()     P(F|D) P(D), el camino defectuoso y marcado
    2. bayes_denominator()   ley de la probabilidad total para P(F)
    3. posterior()           P(D|F) = numerador / denominador

El mismo árbol de 100 lotes se reconstruye a partir de las mismas constantes.
No se importa ningún script anterior. La posterior iguala 8/17 del árbol de
frecuencias.

Ejecútalo:
    uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_02_posterior.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEED = 42
P_DEFECTIVE = 0.10
P_CLEAN = 0.90
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
P_FLAGGED_GIVEN_CLEAN = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def prior_probability() -> dict[str, float]:
    """Devuelve la priori de la primera etapa antes de observar la marca."""
    return {
        "p_defective": P_DEFECTIVE,
        "p_clean": P_CLEAN,
    }


def likelihoods() -> dict[str, float]:
    """Devuelve las verosimilitudes de marca dado defectuoso y dado limpio."""
    return {
        "p_flagged_given_defective": P_FLAGGED_GIVEN_DEFECTIVE,
        "p_flagged_given_clean": P_FLAGGED_GIVEN_CLEAN,
    }


# --- NUEVO (1) bayes_numerator() ---------------------------------------------
def bayes_numerator(prior: dict[str, float], like: dict[str, float]) -> float:
    """Devuelve P(F y D) = P(F|D) P(D)."""
    return like["p_flagged_given_defective"] * prior["p_defective"]
# ------------------------------------------------------------------------------


# --- NUEVO (2) bayes_denominator() -------------------------------------------
def bayes_denominator(prior: dict[str, float], like: dict[str, float]) -> dict[str, float]:
    """Devuelve P(F) sumando los dos caminos marcados mutuamente excluyentes."""
    path_defective = like["p_flagged_given_defective"] * prior["p_defective"]
    path_clean = like["p_flagged_given_clean"] * prior["p_clean"]
    return {
        "defective_and_flagged": path_defective,
        "clean_and_flagged": path_clean,
        "p_flagged": path_defective + path_clean,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) posterior() ---------------------------------------------------
def posterior(numerator: float, p_flagged: float) -> float:
    """Devuelve P(D|F) a partir del teorema de Bayes."""
    return numerator / p_flagged
# ------------------------------------------------------------------------------


def save_figure(paths: dict[str, float], posterior_value: float) -> Path:
    """Guarda los dos caminos marcados y la posterior resultante."""
    output_path = DIR_FIGURES / "bayes_02_posterior.png"
    labels = [
        "P(D y F)\nnumerador",
        "P(C y F)",
        "P(F)\ndenominador",
        "P(D | F)\nposterior",
    ]
    values = np.array(
        [
            paths["defective_and_flagged"],
            paths["clean_and_flagged"],
            paths["p_flagged"],
            posterior_value,
        ]
    )
    colors = ["#EC2661", "#5B8DEF", "#1A2E51", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probabilidad")
    ax.set_title("Bayes: posterior = camino marcado y defectuoso / P(F)")
    ax.set_ylim(0, 0.55)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.015,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path


def main() -> None:
    prior = prior_probability()
    like = likelihoods()
    numerator = bayes_numerator(prior, like)
    paths = bayes_denominator(prior, like)
    posterior_value = posterior(numerator, paths["p_flagged"])
    frequency_check = 8 / 17
    figure_path = save_figure(paths, posterior_value)

    print("================================================================")
    print("LECCIÓN 11 - PASO 2: POSTERIOR DE BAYES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Priori P(D)                     : {prior['p_defective']:.6f}")
    print(
        "Verosimilitud P(F | D)          : "
        f"{like['p_flagged_given_defective']:.6f}"
    )
    print(
        "Verosimilitud P(F | C)          : "
        f"{like['p_flagged_given_clean']:.6f}"
    )
    print(f"Numerador P(D y F)              : {numerator:.6f}")
    print(f"Camino P(C y F)                 : {paths['clean_and_flagged']:.6f}")
    print(f"Denominador P(F)                : {paths['p_flagged']:.6f}")
    print(f"Posterior P(D | F)              : {posterior_value:.6f}")
    print(f"Comprobación de frecuencia 8/17 : {frequency_check:.6f}")
    print(f"Coincide con 8/17               : {np.isclose(posterior_value, frequency_check)}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

