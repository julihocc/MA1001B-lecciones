"""
Lección 11 - Paso 3: Sensibilidad a la tasa base
================================================
NUEVO EN ESTE PASO: posterior_from_prior(), naive_likelihood_as_posterior() y
save_figure().

CAMBIOS RESPECTO A bayes_02_posterior.py
La Receta
---------
Introduce estos cambios en este orden:
    1. posterior_from_prior()   P(D|F) como función de la priori de defectuosos
    2. naive_likelihood_as_posterior()  la falacia de tasa base P(D|F) ~ P(F|D)
    3. save_figure()            contrasta priori 0.10 con priori 0.02

Si la priori cae de 0.10 a 0.02, la posterior cae con ella aunque las
verosimilitudes se mantengan en 0.80 y 0.10. Ignorar la tasa base es el
límite de esta lección.

Ejecútalo:
    uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_03_sensibilidad_tasa_base.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEED = 42
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
P_FLAGGED_GIVEN_CLEAN = 0.10
PRIOR_ORIGINAL = 0.10
PRIOR_RARE = 0.02
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) posterior_from_prior() ----------------------------------------
def posterior_from_prior(prior_defective: float) -> dict[str, float]:
    """Actualiza P(D|F) cuando solo cambia la tasa base de defectuosos."""
    p_clean = 1.0 - prior_defective
    numerator = P_FLAGGED_GIVEN_DEFECTIVE * prior_defective
    path_clean = P_FLAGGED_GIVEN_CLEAN * p_clean
    p_flagged = numerator + path_clean
    return {
        "prior": prior_defective,
        "numerator": numerator,
        "p_flagged": p_flagged,
        "posterior": numerator / p_flagged,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) naive_likelihood_as_posterior() -------------------------------
def naive_likelihood_as_posterior() -> float:
    """Devuelve la identificación errónea de P(D|F) con P(F|D)."""
    return P_FLAGGED_GIVEN_DEFECTIVE
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    original: dict[str, float],
    rare: dict[str, float],
    naive: float,
) -> Path:
    """Guarda la posterior versus la priori y el atajo ingenuo de verosimilitud."""
    output_path = DIR_FIGURES / "bayes_03_sensibilidad_tasa_base.png"
    priors = np.linspace(0.01, 0.40, 80)
    posteriors = np.array(
        [posterior_from_prior(p)["posterior"] for p in priors]
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(
        priors,
        posteriors,
        color="#1A2E51",
        lw=2.2,
        label="Posterior de Bayes P(D | F)",
    )
    ax.axhline(
        naive,
        color="#EC2661",
        linestyle="--",
        lw=1.6,
        label="Ingenuo: tratar P(F | D) como posterior",
    )
    ax.scatter(
        [original["prior"], rare["prior"]],
        [original["posterior"], rare["posterior"]],
        color=["#5B8DEF", "#EC2661"],
        s=70,
        zorder=5,
    )
    ax.annotate(
        f"priori={original['prior']:.2f}\nposterior={original['posterior']:.3f}",
        xy=(original["prior"], original["posterior"]),
        xytext=(0.16, 0.62),
        fontsize=8,
        color="#1A2E51",
        arrowprops=dict(arrowstyle="-|>", color="#1A2E51"),
    )
    ax.annotate(
        f"priori={rare['prior']:.2f}\nposterior={rare['posterior']:.3f}",
        xy=(rare["prior"], rare["posterior"]),
        xytext=(0.08, 0.32),
        fontsize=8,
        color="#EC2661",
        arrowprops=dict(arrowstyle="-|>", color="#EC2661"),
    )
    ax.set_xlabel("Priori P(D)")
    ax.set_ylabel("Posterior P(D | F)")
    ax.set_title("Una tasa rara de defectuosos colapsa la posterior")
    ax.set_xlim(0.00, 0.42)
    ax.set_ylim(0.00, 0.90)
    ax.grid(linestyle="--", alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    original = posterior_from_prior(PRIOR_ORIGINAL)
    rare = posterior_from_prior(PRIOR_RARE)
    naive = naive_likelihood_as_posterior()
    figure_path = save_figure(original, rare, naive)

    print("================================================================")
    print("LECCIÓN 11 - PASO 3: SENSIBILIDAD A LA TASA BASE")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Verosimilitud P(F | D)          : {P_FLAGGED_GIVEN_DEFECTIVE:.6f}")
    print(f"Verosimilitud P(F | C)          : {P_FLAGGED_GIVEN_CLEAN:.6f}")
    print(f"Priori original P(D)            : {original['prior']:.6f}")
    print(f"P(F) original                   : {original['p_flagged']:.6f}")
    print(f"Posterior original P(D | F)     : {original['posterior']:.6f}")
    print(f"Priori rara P(D)                : {rare['prior']:.6f}")
    print(f"P(F) rara                       : {rare['p_flagged']:.6f}")
    print(f"Posterior rara P(D | F)         : {rare['posterior']:.6f}")
    print(f"Ingenuo: P(F | D) como P(D|F)   : {naive:.6f}")
    print(
        "Caída de posterior (0.10 a 0.02): "
        f"{original['posterior'] - rare['posterior']:.6f}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

