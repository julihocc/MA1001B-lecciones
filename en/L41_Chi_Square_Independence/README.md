# Lesson 41 - Chi-Square Test of Independence

This 50-minute micro-lesson uses one fully synthetic $2\times 3$ checkout
table, $n=325$, to test whether conversion is independent of acquisition
channel. Expected counts use the independence formula, $df=(2-1)(3-1)=2$,
and Cramer's V summarizes association strength. The final step shows that a
significant association is not a causal claim: the pattern vanishes inside
device strata.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 11, Section 11.4 (test of independence).
- **Prerequisites:** Chi-square goodness of fit from Lesson 40.
- **Data notice:** Every visitor count is synthetic. The scripts contain no
  real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Form expected counts $E=(\text{row total}\times\text{column total})/n$.
2. Compute $\chi^2$ for a two-way table with $df=(r-1)(c-1)$.
3. Report a right-tailed p-value and Cramer's V.
4. Explain why a significant association is not a causal claim.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: conversion by channel | Sketch the $2\times 3$ table. |
| 06-16 | Margins and expected counts | Compute $E_{11}=113\times120/325$. |
| 16-24 | Run Step 1 | Read expected $41.723$, $43.462$, $27.815$ on the converted row. |
| 24-34 | $\chi^2$ and $df=2$ | Name independence as $H_0$. |
| 34-42 | Run Step 2 | Obtain $\chi^2=10.114985$, $p=0.006361$, $V=0.176417$. |
| 42-48 | Run Step 3 | Contrast combined $p=0.006361$ with desktop $p=0.368546$. |
| 48-50 | Concept check and handoff to Lesson 42 | Name the next tool: chi-square homogeneity. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
synthetic checkout table without importing another lesson script. These
values came from two matching executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `independence_01_contingency_table.py` | $2\times 3$ table and $E_{ij}$ | $n=325$; observed converted $40,55,18$; not converted $80,70,62$; minimum $E=27.815385$. |
| 2 | `independence_02_chi_square.py` | Independence $\chi^2$, $df=2$, Cramer's V | $\chi^2=10.114985$, $p=0.006361$, $\chi^{2*}=5.991465$, $V=0.176417$, reject $H_0$. |
| 3 | `independence_03_no_causation_limit.py` | Confounding by device | Combined $p=0.006361$; desktop $p=0.368546$; mobile $p=0.761939$. Association is not a causal claim. |

The Step 3 result is a limit, not a new chi-square variant. Channel was not
randomly assigned. Lesson 42 keeps the same arithmetic but changes the
sampling story to independent samples.

## Synthetic Checkout Table

| Outcome | Email | Search | Social | Total |
|---|---:|---:|---:|---:|
| Converted | 40 | 55 | 18 | 113 |
| Not converted | 80 | 70 | 62 | 212 |
| Total | 120 | 125 | 80 | 325 |

\[
\chi^2=10.114985,\qquad df=2,\qquad p=0.006361,\qquad V=0.176417.
\]

Inside desktop visitors the p-value is $0.368546$; inside mobile visitors it
is $0.761939$. The combined association is compatible with a device mix, not
with a causal channel effect.

## Common Misconceptions

- Independence $H_0$ is about one sample cross-classified, not about two
  experiments.
- $df=(r-1)(c-1)$, not $n-1$.
- Cramer's V is a strength summary; it is not a p-value.
- Rejecting independence does not identify which cell caused the result, and
  it does not identify a cause in the world.
- The synthetic checkout table illustrates independence. It is not a claim
  about any real acquisition channel.

## Package Structure

```text
L41_Chi_Square_Independence/
|-- README.md
|-- src/
|   |-- independence_01_contingency_table.py
|   |-- independence_02_chi_square.py
|   `-- independence_03_no_causation_limit.py
|-- figures/
|   |-- independence_01_contingency_table.png
|   |-- independence_02_chi_square.png
|   `-- independence_03_no_causation_limit.png
|-- notebooks/
|   `-- lesson_41_chi_square_independence.ipynb
`-- slides/
    |-- lesson_41.tex
    `-- lesson_41.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L41_Chi_Square_Independence/src/independence_01_contingency_table.py
uv run en/L41_Chi_Square_Independence/src/independence_02_chi_square.py
uv run en/L41_Chi_Square_Independence/src/independence_03_no_causation_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L41_Chi_Square_Independence/notebooks/lesson_41_chi_square_independence.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_41.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_41.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The chi-square test of independence, expected counts from the product of
margins, $df=(r-1)(c-1)$, and the warning that association is not causation
follow Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory
Business Statistics 2e*, Chapter 11, Section
[11.4](https://openstax.org/books/introductory-business-statistics-2e/pages/11-4-test-of-independence).
Companion independence practice is in *Introductory Statistics 2e*, Section
[11.3](https://openstax.org/books/introductory-statistics-2e/pages/11-3-test-of-independence).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

