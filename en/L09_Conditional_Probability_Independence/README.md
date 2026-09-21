# Lesson 09: Conditional Probability and Independence

This 50-minute micro-lesson uses one fully synthetic order-operations scenario
to reduce a sample space, test whether two events are independent, and expose
the dependence created by sampling without replacement.

## Learning Outcomes

By the end of the lesson, students can:

1. interpret and calculate (P(A\mid B)) using the condition as the denominator;
2. explain why (P(A\mid B)) and (P(B\mid A)) answer different questions;
3. test independence using a conditional or product equality;
4. update a sequential probability when sampling without replacement.

## Prerequisites

- events, intersections, and sample spaces from Lesson 05;
- contingency-table probabilities and multiplication rules from Lesson 08;
- basic pandas filtering, NumPy arrays, and matplotlib charts.

## 50-Minute Facilitation Route

| Time | Activity | Evidence |
|---:|---|---|
| 0-6 min | Revisit the synthetic 400-order table and pose a conditional question. | Students identify the restricted denominator. |
| 6-15 min | Derive conditional probability as a reduced sample space. | (P(L\mid M)=48/120=0.40). |
| 15-23 min | Run Step 1 and reverse the condition. | (P(L\mid M)=0.40), while (P(M\mid L)=0.60). |
| 23-32 min | Define and test independence. | Conditional and product equalities are evaluated. |
| 32-39 min | Run Step 2 and interpret the association carefully. | Both equalities fail; no causal claim is made. |
| 39-47 min | Run Step 3 for two selections without replacement. | Exact 0.133333 and simulated 0.132938 replace the naive 0.160000. |
| 47-50 min | Concept check and bridge to L10. | Students state why branches are needed for longer sequences. |

The concept check may lead directly into another lesson in the same class
session. It is not a mandatory end-of-session activity.

## Synthetic Operations Scenario

All orders, routing processes, delivery outcomes, and inspection selections are
synthetic. They do not describe a real organization, partner, or operating
process.

| Routing process | Late | On time | Row total |
|---|---:|---:|---:|
| Manual review | 48 | 72 | 120 |
| Automated | 32 | 248 | 280 |
| Column total | 80 | 320 | 400 |

Let (M) be manual review and (L) be late delivery. Conditioning on manual
review reduces the denominator from 400 orders to 120:

\[
P(L\mid M)=\frac{P(L\cap M)}{P(M)}=\frac{48}{120}=0.40.
\]

Reversing the condition changes the reference group:

\[
P(M\mid L)=\frac{48}{80}=0.60.
\]

The two values differ because their denominators answer different questions.

## Testing Independence

Events (M) and (L) are independent if any equivalent equality holds, such
as

\[
P(L\mid M)=P(L)
\]

or

\[
P(M\cap L)=P(M)P(L).
\]

Here, (0.40\ne0.20) and (0.12\ne0.06), so the events are not independent in
the synthetic table. This is evidence of association only; the table does not
show that manual review causes late delivery.

## The Without-Replacement Limit

In a small synthetic inspection batch, four of ten orders are flagged. If two
orders are selected without replacement, then

\[
P(\text{both flagged})=\frac{4}{10}\frac{3}{9}=\frac{2}{15}
=0.133333\ldots
\]

The naive independent calculation ((4/10)^2=0.160000) fails because the first
selection changes both the numerator and denominator for the second. The
seed-42 simulation of 500,000 selections produced 0.132938. Tracking longer
sequences motivates the tree diagrams and sample-space decomposition in L10.

## Study Notebook

The student guide
[`notebooks/lesson_09_conditional_probability_independence.ipynb`](notebooks/lesson_09_conditional_probability_independence.ipynb)
integrates the three steps into one cumulative state. It rebuilds the 400-order
synthetic register in memory, preserves the documented function contracts from
`src/`, embeds three editable figures, and concludes with executable
assertions, safe practice, and collapsible answers. Its seed-42 simulation uses
500,000 selections and verifies the exact without-replacement calculation.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Scripts and Verified Results

Every script is standalone, uses seed 42, accepts no command-line arguments,
imports no earlier step, and writes only its corresponding PNG. These values
came from two matching executions in the locked `uv` environment.

| Step | Script | Verified result |
|:---:|---|---|
| 1 | `conditional_01_reduced_sample_space.py` | (P(L\mid M)=0.400000), (P(L\mid\text{Automated})=0.114286), and (P(M\mid L)=0.600000). |
| 2 | `conditional_02_independence_tests.py` | (P(L)=0.200000\ne0.400000); (P(M\cap L)=0.120000\ne0.060000=P(M)P(L)); independent is `False`. |
| 3 | `conditional_03_without_replacement_limit.py` | Naive 0.160000; exact 0.133333; seed-42 simulation 0.132938 from 500,000 trials. |

## Common Misconceptions

- The condition after the vertical bar determines the denominator.
- (P(A\mid B)) and (P(B\mid A)) are generally different.
- Independence must be checked; it should not be inferred from event names.
- Mutually exclusive events with positive probabilities are not independent.
- A difference in conditional rates is an association, not proof of causation.
- Without replacement, the first selection changes later probabilities.

## Package Structure

```text
L09_Conditional_Probability_Independence/
|-- README.md
|-- notebooks/
|   `-- lesson_09_conditional_probability_independence.ipynb
|-- src/
|   |-- conditional_01_reduced_sample_space.py
|   |-- conditional_02_independence_tests.py
|   `-- conditional_03_without_replacement_limit.py
|-- figures/
|   |-- conditional_01_rates.png
|   |-- conditional_02_independence.png
|   `-- conditional_03_sequence.png
`-- slides/
    |-- lesson_09.tex
    `-- lesson_09.pdf
```

## Execution

Run from the repository root:

```powershell
uv sync --frozen
uv run en/L09_Conditional_Probability_Independence/src/conditional_01_reduced_sample_space.py
uv run en/L09_Conditional_Probability_Independence/src/conditional_02_independence_tests.py
uv run en/L09_Conditional_Probability_Independence/src/conditional_03_without_replacement_limit.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L09_Conditional_Probability_Independence/notebooks/lesson_09_conditional_probability_independence.ipynb
```

Compile twice from the `slides/` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error lesson_09.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_09.tex
```

## OpenStax Attribution

The definition of conditional probability as a reduced sample space follows
OpenStax, *Introductory Business Statistics 2e*, Chapter 3, Section 3.1.
Equivalent independence criteria and the dependence created by sampling
without replacement follow Section 3.2. The general multiplication rule is
consistent with Section 3.3.

- Section 3.1: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Section 3.2: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events>
- Section 3.3: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-3-two-basic-rules-of-probability>
- Authors: Alexander Holmes, Barbara Illowsky, and Susan Dean.
- License: CC BY-NC-SA 4.0.

