"""
Lección 37 - Paso 3: Los grupos observacionales no son un experimento aleatorizado
=================================================================================
NUEVO EN ESTE PASO: experience_summaries(), association_check() y
save_figure().

La Receta
Partir de t_dos_muestras_02_prueba_welch.py e introducir:
    1. experience_summaries()   un confounder que difiere por turno
    2. association_check()      tiempo de recolección frente a experiencia dentro de grupos
    3. save_figure()            dispersión que bloquea una lectura causal

Welch puede rechazar medias iguales. Eso no es evidencia de que el turno
mismo causó la diferencia. Los asociados no fueron asignados al azar: el
turno A es más experimentado, y la experiencia se asocia con recolecciones
más rápidas.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 30
N_B = 32
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae tiempos de recolección sintéticos independientes y años de experiencia."""
    rng = np.random.default_rng(seed)
    return {
        "times_a": rng.normal(loc=48.0, scale=6.0, size=N_A),
        "times_b": rng.normal(loc=52.5, scale=7.5, size=N_B),
        "experience_a": rng.normal(loc=4.5, scale=1.0, size=N_A),
        "experience_b": rng.normal(loc=2.0, scale=0.8, size=N_B),
    }


# --- NUEVO (1) experience_summaries() ----------------------------------------
def experience_summaries(exp_a: np.ndarray, exp_b: np.ndarray) -> dict[str, float]:
    """Resume años de experiencia, que no fueron asignados al azar."""
    return {
        "mean_exp_a": float(np.mean(exp_a)),
        "mean_exp_b": float(np.mean(exp_b)),
        "s_exp_a": float(np.std(exp_a, ddof=1)),
        "s_exp_b": float(np.std(exp_b, ddof=1)),
        "exp_diff": float(np.mean(exp_a) - np.mean(exp_b)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) association_check() -------------------------------------------
def association_check(samples: dict[str, np.ndarray]) -> dict[str, float]:
    """Correlaciona tiempo de recolección con experiencia dentro de cada turno observacional."""
    r_a = float(np.corrcoef(samples["experience_a"], samples["times_a"])[0, 1])
    r_b = float(np.corrcoef(samples["experience_b"], samples["times_b"])[0, 1])
    welch = stats.ttest_ind(
        samples["times_a"], samples["times_b"], equal_var=False
    )
    return {
        "r_a": r_a,
        "r_b": r_b,
        "welch_p": float(welch.pvalue),
        "randomized": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(samples: dict[str, np.ndarray]) -> Path:
    """Dispersión de tiempo de recolección contra experiencia, coloreada por turno no asignado."""
    output_path = DIR_FIGURES / "t_dos_muestras_03_limite_observacional.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.scatter(
        samples["experience_a"],
        samples["times_a"],
        color="#5B8DEF",
        s=42,
        label="Turno A",
        edgecolors="#1A2E51",
    )
    ax.scatter(
        samples["experience_b"],
        samples["times_b"],
        color="#EC2661",
        s=42,
        label="Turno B",
        edgecolors="#1A2E51",
    )
    ax.set_xlabel("Años de experiencia (no asignados al azar)")
    ax.set_ylabel("Tiempo de recolección (minutos)")
    ax.set_title("Una prueba de Welch significativa no es un experimento aleatorizado")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    samples = build_shift_samples()
    exp = experience_summaries(samples["experience_a"], samples["experience_b"])
    assoc = association_check(samples)
    figure_path = save_figure(samples)

    print("================================================================")
    print("LECCIÓN 37 - PASO 3: LÍMITE OBSERVACIONAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Valor p bilateral de Welch      : {assoc['welch_p']:.6f}")
    print(f"Experiencia media turno A (años): {exp['mean_exp_a']:.6f}")
    print(f"Experiencia media turno B (años): {exp['mean_exp_b']:.6f}")
    print(f"Brecha de experiencia A menos B : {exp['exp_diff']:.6f}")
    print(f"Corr(experiencia, tiempo) turno A: {assoc['r_a']:.6f}")
    print(f"Corr(experiencia, tiempo) turno B: {assoc['r_b']:.6f}")
    print("Asignación aleatoria de asociados: no")
    print("Afirmación causal del valor p de Welch: no justificada")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

