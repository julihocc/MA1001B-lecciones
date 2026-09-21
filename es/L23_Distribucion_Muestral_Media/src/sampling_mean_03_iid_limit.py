"""
Lección 23 - Paso 3: El EE supone extracciones iid
==================================================
La Receta
Partir de sampling_mean_02_n9_vs_n36.py e introducir:
    1. simulate_clustered_means()  n = 36 como 6 conglomerados de 6 copias
    2. se_inflation()              EE empírico versus sigma / sqrt(36)
    3. save_figure()               histograma iid versus histograma agrupado

La fórmula EE = sigma / sqrt(n) supone extracciones iid de la población
definida. Las copias agrupadas hacen que la muestra efectiva se acerque a
6, de modo que el EE observado queda cerca de 12 / sqrt(6), no 12 / sqrt(36).
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 80.0
SIGMA = 12.0
N_LARGE = 36
N_CLUSTERS = 6
CLUSTER_SIZE = 6
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def simulate_sample_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps muestras iid de tamaño n y retorna las medias muestrales."""
    rng = np.random.default_rng(SEED)
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    return draws.mean(axis=1)


# --- NUEVO (1) simulate_clustered_means() ------------------------------------
def simulate_clustered_means(n_reps: int = N_REPS) -> np.ndarray:
    """Repite 6 extracciones de conglomerado seis veces y promedia las 36 copias."""
    rng = np.random.default_rng(SEED)
    clusters = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, N_CLUSTERS))
    copies = np.repeat(clusters, CLUSTER_SIZE, axis=1)
    return copies.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NUEVO (2) se_inflation() ------------------------------------------------
def se_inflation(iid_means: np.ndarray, clustered_means: np.ndarray) -> dict[str, float]:
    """Contrasta el EE iid con el EE inflado por conglomerados."""
    iid_se = float(np.std(iid_means, ddof=1))
    clustered_se = float(np.std(clustered_means, ddof=1))
    return {
        "iid_se": iid_se,
        "clustered_se": clustered_se,
        "formula_n36": SIGMA / np.sqrt(N_LARGE),
        "formula_n6": SIGMA / np.sqrt(N_CLUSTERS),
        "inflation": clustered_se / iid_se,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(iid_means: np.ndarray, clustered_means: np.ndarray) -> Path:
    """Compara medias iid n = 36 con medias agrupadas n = 36."""
    output_path = DIR_FIGURES / "sampling_mean_03_iid_limit.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(iid_means, bins=30, density=True, color="#5B8DEF", alpha=0.55,
            edgecolor="#1A2E51", label="iid n = 36")
    ax.hist(clustered_means, bins=30, density=True, color="#EC2661", alpha=0.45,
            edgecolor="#1A2E51", label="6 conglomerados de 6 copias")
    ax.axvline(MU, color="#1A2E51", ls="--", lw=1.2)
    ax.set_xlabel("Media muestral xbar")
    ax.set_ylabel("Densidad")
    ax.set_title("Las copias agrupadas inflan el EE por encima de sigma / sqrt(36)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    iid_means = simulate_sample_means(N_LARGE)
    clustered_means = simulate_clustered_means()
    summary = se_inflation(iid_means, clustered_means)
    figure_path = save_figure(iid_means, clustered_means)

    print("================================================================")
    print("LECCIÓN 23 - PASO 3: LÍMITE IID")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"EE de fórmula n = 36            : {summary['formula_n36']:.6f}")
    print(f"EE empírico iid                 : {summary['iid_se']:.6f}")
    print(f"EE de fórmula n = 6             : {summary['formula_n6']:.6f}")
    print(f"EE empírico agrupado            : {summary['clustered_se']:.6f}")
    print(f"Razón de inflación del EE       : {summary['inflation']:.6f}")
    print("Límite: el EE supone extracciones iid de la población definida")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

