# Lesson 08: Probability Rules and Contingency Tables

This 50-minute micro-lesson uses one fully synthetic order-operations dataset
to read marginal and joint probabilities from a contingency table, apply the
complement and addition rules, and expose the assumption hidden in multiplying
marginal probabilities.

## Learning Outcomes

By the end of the lesson, students can:

1. read cell, row, column, and grand totals from a two-way table;
2. calculate marginal, joint, and complement probabilities;
3. apply the general addition rule without double-counting an intersection;
4. explain why \(P(A)P(B)\) cannot replace \(P(A\cap B)\) unless independence
   has been established.

## Prerequisites

- outcomes, events, unions, intersections, and complements from Lesson 05;
- finite sample-space counting from Lessons 06 and 07;
- basic pandas tables and matplotlib charts.

## 50-Minute Facilitation Route

| Time | Activity | Evidence |
|---:|---|---|
| 0-5 min | Define events from one business question. | \(M\): manual review; \(L\): late delivery. |
| 5-15 min | Read a two-way contingency table. | Students distinguish cells, margins, and the grand total. |
| 15-24 min | Run Step 1. | Marginal and joint probabilities are verified from 400 records. |
| 24-33 min | Derive complement and addition rules. | The overlap is identified before calculating an OR event. |
| 33-41 min | Run Step 2. | The correct union 0.38 replaces the naive sum 0.50. |
| 41-47 min | Run Step 3 and expose the multiplication limit. | The marginal product 0.06 fails to match the observed intersection 0.12. |
| 47-50 min | Concept check and bridge to L09. | Students identify the missing conditional-probability reasoning. |

The concept check may lead directly into another lesson in the same class
session. It is not a mandatory end-of-session activity.

## Synthetic Operations Dataset

All 400 order records, routing processes, and delivery outcomes are synthetic.
They do not describe a real organization, partner, or operating process.

| Routing process | Late | On time | Row total |
|---|---:|---:|---:|
| Manual review | 48 | 72 | 120 |
| Automated | 32 | 248 | 280 |
| Column total | 80 | 320 | 400 |

Let \(M\) be manual review and \(L\) be late delivery. The table gives

\[
P(M)=\frac{120}{400}=0.30,\qquad
P(L)=\frac{80}{400}=0.20,
\]

and

\[
P(M\cap L)=\frac{48}{400}=0.12.
\]

## Complement and Addition Rules

The complement rule gives

\[
P(M^c)=1-P(M)=0.70.
\]

The general addition rule is

\[
P(M\cup L)=P(M)+P(L)-P(M\cap L).
\]

For the synthetic table,

\[
P(M\cup L)=0.30+0.20-0.12=0.38.
\]

The naive sum 0.50 counts the 48 orders in \(M\cap L\) twice. Directly
counting the 152 orders that are manually reviewed, late, or both also gives
\(152/400=0.38\).

## The Multiplication-Rule Limit

The general multiplication rule is

\[
P(M\cap L)=P(M)P(L\mid M).
\]

The table gives \(P(L\mid M)=48/120=0.40\), so

\[
P(M)P(L\mid M)=0.30(0.40)=0.12.
\]

Multiplying the marginal probabilities instead gives

\[
P(M)P(L)=0.30(0.20)=0.06,
\]

which does not match the observed intersection. This lesson uses that mismatch
as a limit; Lesson 09 develops conditional probability and independence.

## Study Notebook

The student guide
[`notebooks/lesson_08_probability_rules_contingency_tables.ipynb`](notebooks/lesson_08_probability_rules_contingency_tables.ipynb)
integrates the three steps into one cumulative state. It constructs the 400
synthetic records in memory, preserves the documented function contracts from
`src/`, embeds three editable figures, and concludes with executable
assertions, safe practice, and collapsible answers.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Scripts and Verified Results

Every script is standalone, uses seed 42 for the deterministic record order,
accepts no command-line arguments, imports no earlier step, and writes only its
corresponding PNG. The results below came from repeated execution in the locked
`uv` environment.

| Step | Script | Verified result |
|:---:|---|---|
| 1 | `probability_rules_01_contingency_table.py` | 400 records; \(P(M)=0.30\), \(P(L)=0.20\), and \(P(M\cap L)=0.12\). |
| 2 | `probability_rules_02_complement_addition.py` | \(P(M^c)=0.70\); naive sum 0.50; corrected and directly counted union 0.38. |
| 3 | `probability_rules_03_multiplication_limit.py` | Observed intersection 0.12; marginal product 0.06; \(P(L\mid M)=0.40\); general product 0.12. |

## Common Misconceptions

- A cell probability uses one joint cell; a marginal probability uses a row or
  column total.
- OR includes the overlap unless the events are mutually exclusive.
- Adding \(P(A)+P(B)\) without subtracting \(P(A\cap B)\) double-counts shared
  outcomes.
- Mutually exclusive and independent do not mean the same thing.
- The shortcut \(P(A\cap B)=P(A)P(B)\) requires independence; it is not the
  general multiplication rule.
- A contingency table describes associations in the synthetic records. It does
  not establish a causal effect of manual review on late delivery.

## Package Structure

```text
L08_Probability_Rules_Contingency_Tables/
|-- README.md
|-- notebooks/
|   `-- lesson_08_probability_rules_contingency_tables.ipynb
|-- src/
|   |-- probability_rules_01_contingency_table.py
|   |-- probability_rules_02_complement_addition.py
|   `-- probability_rules_03_multiplication_limit.py
|-- figures/
|   |-- probability_01_table.png
|   |-- probability_02_addition.png
|   `-- probability_03_limit.png
`-- slides/
    |-- lesson_08.tex
    `-- lesson_08.pdf
```

## Execution

Run from the repository root:

```powershell
uv sync --frozen
uv run en/L08_Probability_Rules_Contingency_Tables/src/probability_rules_01_contingency_table.py
uv run en/L08_Probability_Rules_Contingency_Tables/src/probability_rules_02_complement_addition.py
uv run en/L08_Probability_Rules_Contingency_Tables/src/probability_rules_03_multiplication_limit.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L08_Probability_Rules_Contingency_Tables/notebooks/lesson_08_probability_rules_contingency_tables.ipynb
```

Compile twice from the `slides/` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error lesson_08.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_08.tex
```

## OpenStax Attribution

Definitions of events, union, intersection, complement, and probabilities from
a two-way table follow OpenStax, *Introductory Business Statistics 2e*, Chapter
3, Section 3.1. The general addition and multiplication rules follow Section
3.3.

- Section 3.1: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Section 3.3: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-3-two-basic-rules-of-probability>
- Authors: Alexander Holmes, Barbara Illowsky, and Susan Dean.
- License: CC BY-NC-SA 4.0.

