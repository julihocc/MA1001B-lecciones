# MA1001B lessons

Public, reusable lessons for MA1001B (Statistical Modeling for Decision Making).
The repository contains academic lesson material in English and Spanish:
slides, source code, figures, notebooks, and student-facing documentation.
It has no student records, private course operations, or instructor-only notes.

## Use

```text
uv sync --frozen
uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_01_poblacion_muestra.py
```

Compile a deck from its `slides` or `diapositivas` directory with your local
LaTeX installation. PDFs and notebooks are tracked with Git LFS.

The original course repository includes this repository at `02-lecciones` as a
Git submodule.

## W08 L08 package

The bilingual L08 package is indexed in [Spanish](es/L08_Reglas_Probabilidad_Tablas_Contingencia/README.md) and [English](en/L08_Probability_Rules_Contingency_Tables/README.md). Each route separates independent student study from compact instructor exposition.

## 2026-09-25 · compact code guidance

Every code cell in the compact instructor notebook now carries explanatory comments beside the relevant operation. The executable Python and saved outputs were preserved; a fresh run reproduced the saved outputs. Student materials were not changed.

| Notebook | Code cells | SHA-256 |
|---|---:|---|
| [leccion_05_compacta.ipynb](es/L05_Teoria_Conjuntos_Espacio_Muestral/docente/leccion_05_compacta.ipynb) | 5 | 0604523AB80CB50BCAC3656F4D767524C7B5E4A0B6A307777B98E8E91C1D8BDE |
| [lesson_05_compact.ipynb](en/L05_Set_Theory_Sample_Space/instructor/lesson_05_compact.ipynb) | 5 | 265D251948104735BDE3C9F58275A8666BA767839D96F6A01A04E46E69861F3F |
| [leccion_06_compacta.ipynb](es/L06_Tecnicas_Conteo_I/notebooks/leccion_06_compacta.ipynb) | 4 | B3B02A61A870DE9D519C18A4B01AD6B2545F2FBA5F9DABDD157BD1E45F3AA06E |
| [lesson_06_compact.ipynb](en/L06_Counting_Techniques_I/notebooks/lesson_06_compact.ipynb) | 4 | 529AB5214F7C0D9B4F0C5ABBA6CA9F23F16AE3E98065D4AED29C5ED7066847F5 |
| [leccion_07_compacta.ipynb](es/L07_Tecnicas_Conteo_II/notebooks/leccion_07_compacta.ipynb) | 3 | FC3FDA7F9A2AF21723C4EEBB26978FEB9BAE261AFE6971273A9FC9FF91855FCB |
| [lesson_07_compact.ipynb](en/L07_Counting_Techniques_II/notebooks/lesson_07_compact.ipynb) | 3 | A7356E4B38603247843673E6DD2EF72742CF22EE3F62548B6DC8F91721396FB6 |
| [leccion_08_compacta.ipynb](es/L08_Reglas_Probabilidad_Tablas_Contingencia/docente/leccion_08_compacta.ipynb) | 3 | 08F1E33C50E9CFA8D82F5703A3AC8B2C56EDA38EF003FF86E0330ED7A47ED27D |
| [lesson_08_compact.ipynb](en/L08_Probability_Rules_Contingency_Tables/instructor/lesson_08_compact.ipynb) | 3 | C9ED1566A0C5A45912772F7693C3B26A3C469892D1E0BD0BCD33D70E55B5E7AE |
