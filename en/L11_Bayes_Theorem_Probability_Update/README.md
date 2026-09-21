# Lesson 11 - Bayes' Theorem and Probability Updating

This 50-minute micro-lesson continues the fully synthetic 100-lot inspection
tree from Lesson 10. Students separate the prior $P(D)$ from the flag
likelihoods, apply Bayes' theorem to obtain $P(D\mid F)=8/17$, and then change
only the base rate to see the posterior collapse.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Principles of Data Science*, Section 3.4
  (Bayes' theorem). Setup and tree arithmetic: *Introductory Business
  Statistics 2e*, Sections 3.2--3.4.
- **Prerequisites:** Tree diagrams and reversed conditionals from Lesson 10.
- **Data notice:** Every lot, inspection flag, and prior is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Identify a prior $P(D)$ and the likelihoods $P(F\mid D)$ and $P(F\mid C)$.
2. Compute a posterior with Bayes' theorem and match it to the path ratio $8/17$.
3. Recalculate the posterior when the prior changes and the likelihoods do not.
4. Explain why treating $P(F\mid D)$ as $P(D\mid F)$ ignores the base rate.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: prior versus likelihood | Label $P(D)=0.10$ and $P(F\mid D)=0.80$. |
| 06-16 | Pieces of Bayes' theorem | Write numerator $P(F\mid D)P(D)$. |
| 16-24 | Run Step 1 | Confirm $0.100000$, $0.800000$, and $0.100000$. |
| 24-34 | Law of total probability for $P(F)$ | Obtain $0.08+0.09=0.17$. |
| 34-42 | Run Step 2 | Match posterior $0.470588$ with $8/17$. |
| 42-48 | Run Step 3 with prior $0.02$ | Contrast $0.470588$ with $0.140351$. |
| 48-50 | Concept check and handoff to Lesson 12 | Name the base-rate fallacy. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
tree with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `bayes_01_prior_likelihood.py` | Prior $P(D)$ and flag likelihoods | $P(D)=0.100000$, $P(C)=0.900000$, $P(F\mid D)=0.800000$, $P(F\mid C)=0.100000$. |
| 2 | `bayes_02_posterior.py` | Bayes formula, $P(F)$, posterior | Numerator $0.080000$, $P(F)=0.170000$, $P(D\mid F)=0.470588=8/17$. |
| 3 | `bayes_03_base_rate_sensitivity.py` | Base-rate sensitivity | Prior $0.02$ yields $P(F)=0.114000$ and $P(D\mid F)=0.140351$. Naive $P(F\mid D)=0.800000$ is not the posterior. |

The Step 3 result is a limit, not a claim that every rare event has a small
posterior. The likelihoods are held fixed so that only the base rate moves.
Lesson 12 turns from updating a probability to the quality of the sample that
produced the counts.

## Bayes Update on the Synthetic Tree

Likelihoods are held at $P(F\mid D)=0.80$ and $P(F\mid C)=0.10$.

\[
P(D\mid F)=\frac{P(F\mid D)P(D)}{P(F\mid D)P(D)+P(F\mid C)P(C)}.
\]

| Prior $P(D)$ | $P(F)$ | Posterior $P(D\mid F)$ |
|---:|---:|---:|
| $0.10$ | $0.170000$ | $0.470588=8/17$ |
| $0.02$ | $0.114000$ | $0.140351$ |

A flagged lot is still more likely to be defective than the prior, but it is
nowhere near $80\%$ defective when the defective rate is rare.

## Study Notebook

The student guide
[`notebooks/lesson_11_bayes_theorem_probability_update.ipynb`](notebooks/lesson_11_bayes_theorem_probability_update.ipynb)
integrates the three steps into one cumulative state. It separates prior and
likelihoods, reconstructs both paths to the evidence, embeds three editable
figures, and concludes with executable assertions, safe practice, and
collapsible answers. A posterior curve makes base-rate sensitivity visible
while preserving the exact 0.10 and 0.02 prior benchmarks.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Common Misconceptions

- $P(F\mid D)$ is a likelihood, not a posterior.
- Bayes' theorem reuses the same two flagged paths already added in Lesson 10.
- A high detection rate does not cancel a low base rate.
- Changing the prior while holding the likelihoods fixed isolates the base-rate
  effect.
- The synthetic tree illustrates updating. It is not a claim about any real
  inspection process.

## Package Structure

```text
L11_Bayes_Theorem_Probability_Update/
|-- README.md
|-- notebooks/
|   `-- lesson_11_bayes_theorem_probability_update.ipynb
|-- src/
|   |-- bayes_01_prior_likelihood.py
|   |-- bayes_02_posterior.py
|   `-- bayes_03_base_rate_sensitivity.py
|-- figures/
|   |-- bayes_01_prior_likelihood.png
|   |-- bayes_02_posterior.png
|   `-- bayes_03_base_rate_sensitivity.png
`-- slides/
    |-- lesson_11.tex
    `-- lesson_11.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L11_Bayes_Theorem_Probability_Update/src/bayes_01_prior_likelihood.py
uv run en/L11_Bayes_Theorem_Probability_Update/src/bayes_02_posterior.py
uv run en/L11_Bayes_Theorem_Probability_Update/src/bayes_03_base_rate_sensitivity.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L11_Bayes_Theorem_Probability_Update/notebooks/lesson_11_bayes_theorem_probability_update.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_11.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_11.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Bayes' theorem, priors, likelihoods, and posterior updating follow *Principles
of Data Science*, Section
[3.4](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory).
The inspection-tree setup uses Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Sections
[3.2](https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
and
[3.4](https://openstax.org/books/introductory-business-statistics-2e/pages/3-4-contingency-tables-and-probability-trees).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

