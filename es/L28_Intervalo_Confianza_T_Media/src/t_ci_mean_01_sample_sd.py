"""
Lección 28 - Paso 1: Desviación estándar muestral cuando sigma es desconocida
=============================================================================
NUEVO EN ESTE PASO: generate_fill_sample(), sample_sd_metrics() y
save_figure().

La Receta
Se observa la misma línea de llenado completamente sintética, pero ahora la
desviación estándar poblacional es desconocida. Una muestra de n = 36
botellas con semilla 42 produce xbar y s. El error estándar estimado es
s / sqrt(n), y la distribución muestral de (xbar - mu) / (s / sqrt(n)) es
t de Student con gl = n - 1.

Ejecútalo:
    uv run es/L28_Intervalo_Confianza_T_Media/src/t_ci_mean_01_sample_sd.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
SIGMA_TRUE = 10.0
MU_TRUE = 502.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) generate_fill_sample() ----------------------------------------
def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid. El analista observa la muestra, no sigma."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)
# ------------------------------------------------------------------------------


# --- NUEVO (2) sample_sd_metrics() -------------------------------------------
def sample_sd_metrics(sample: np.ndarray) -> dict[str, float]:
    """Retorna xbar, s, EE estimado y grados de libertad."""
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    se_hat = s / np.sqrt(N)
    return {
        "n": float(N),
        "df": float(N - 1),
        "xbar": xbar,
        "s": s,
        "se_hat": float(se_hat),
        "hidden_sigma": SIGMA_TRUE,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Guarda un histograma con xbar y la banda de EE estimado a partir de s."""
    output_path = DIR_FIGURES / "t_ci_mean_01_sample_sd.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")
    ax.axvline(
        metrics["xbar"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Media muestral = {metrics['xbar']:.2f} ml",
    )
    ax.axvspan(
        metrics["xbar"] - metrics["se_hat"],
        metrics["xbar"] + metrics["se_hat"],
        color="#5B8DEF",
        alpha=0.22,
        label=f"s / sqrt(n) = {metrics['se_hat']:.4f} ml",
    )
    ax.set_xlabel("Volumen de llenado (ml)")
    ax.set_ylabel("Conteo de botellas")
    ax.set_title("Sigma desconocida: error estándar estimado a partir de s")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_fill_sample()
    metrics = sample_sd_metrics(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LECCIÓN 28 - PASO 1: DESVIACIÓN ESTÁNDAR MUESTRAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Grados de libertad n-1          : {int(metrics['df'])}")
    print(f"Sigma oculta (ml)               : {metrics['hidden_sigma']:.6f}")
    print(f"Media muestral xbar (ml)        : {metrics['xbar']:.6f}")
    print(f"Desv. estándar muestral s       : {metrics['s']:.6f}")
    print(f"EE estimado s/sqrt(n)           : {metrics['se_hat']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

