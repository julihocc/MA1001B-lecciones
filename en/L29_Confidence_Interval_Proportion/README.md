# Lesson 29 - Confidence Interval for a Population Proportion

This 50-minute micro-lesson uses one fully synthetic service snapshot to
estimate a first-contact resolution rate. The Wald 95% interval is built after
checking $n\hat{p}$ and $n(1-\hat{p})$. The final step shows that a rare event
with small $x$ can push the Wald lower bound below 0.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 8, Section 8.3 (confidence interval for a population proportion).
- **Prerequisites:** The z interval for a mean from Lesson 27 and the idea of
  a sampling distribution of $\hat{p}$ from Lesson 25.
- **Data notice:** Every ticket count is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $\hat{p}=x/n$ from a binary snapshot.
2. Check $n\hat{p}\ge 5$ and $n(1-\hat{p})\ge 5$ before using the normal
   approximation.
3. Form the 95% Wald interval $\hat{p}\pm 1.96\sqrt{\hat{p}(1-\hat{p})/n}$.
4. Explain why a rare event with small $x$ makes the Wald interval misleading.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: binary first-contact flag | Write $\hat{p}=x/n$. |
| 06-16 | Success-failure products | Confirm $27$ and $123$ both exceed 5. |
| 16-24 | Run Step 1 | Read $\hat{p}=0.180000$. |
| 24-34 | Standard error of $\hat{p}$ | Compute $0.031369$. |
| 34-42 | Run Step 2 | Obtain $[0.118517, 0.241483]$. |
| 42-48 | Run Step 3 with $x=3$ | See Wald lower bound $-0.002405$. |
| 48-50 | Concept check and handoff to Lesson 30 | Name sample-size planning next. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the snapshot from
constants with `SEED = 42` reserved and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `prop_ci_01_sample_proportion.py` | $\hat{p}=x/n$ and the two products | $x=27$, $n=150$, $\hat{p}=0.180000$, $n\hat{p}=27$, $n(1-\hat{p})=123$. |
| 2 | `prop_ci_02_wald_interval.py` | Wald 95% interval after the check | Conditions satisfied; SE $=0.031369$; CI $[0.118517, 0.241483]$. |
| 3 | `prop_ci_03_rare_event_wald.py` | Rare $x=3$ breaks Wald | $n\hat{p}=3$; Wald $[-0.002405, 0.042405]$; Wilson diagnostic $[0.006825, 0.057147]$. |

The Step 3 result is a limit: a proportion cannot be negative, yet Wald reports
a negative bound when $x$ is small. The Wilson interval is a diagnostic
contrast, not the lesson's main procedure.

The executed [student notebook](notebooks/lesson_29_confidence_interval_proportion.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files. The
notebook computes Wilson directly from its score formula to reproduce the
script's diagnostic without a notebook-only `statsmodels` dependency.

## Synthetic First-Contact Snapshot

Main example: $x=27$ first-contact resolutions in $n=150$ tickets.

\[
\hat{p}=\frac{27}{150}=0.180000,\qquad
\mathrm{SE}=\sqrt{\frac{0.18\times 0.82}{150}}=0.031369,
\]

\[
\hat{p}\pm 1.96\cdot\mathrm{SE}=[0.118517, 0.241483].
\]

Rare-event contrast: $x=3$, $n=150$, $\hat{p}=0.020000$, $n\hat{p}=3<5$.
The Wald lower bound is $-0.002405$.

## Common Misconceptions

- $\hat{p}$ is a statistic. The interval estimates the population $p$.
- The cutoff 5 is a guideline for the normal approximation, not a law of
  nature.
- A Wald interval can leave $[0,1]$ when $x$ is small.
- Wilson is shown only to diagnose that failure; it is not required for the
  lesson outcome.
- $n\hat{p}=27$ uses $\hat{p}$, not the unknown $p$.
- The synthetic tickets illustrate interval arithmetic. They are not a claim
  about any real service desk.

## Package Structure

```text
L29_Confidence_Interval_Proportion/
|-- README.md
|-- src/
|   |-- prop_ci_01_sample_proportion.py
|   |-- prop_ci_02_wald_interval.py
|   `-- prop_ci_03_rare_event_wald.py
|-- figures/
|   |-- prop_ci_01_sample_proportion.png
|   |-- prop_ci_02_wald_interval.png
|   `-- prop_ci_03_rare_event_wald.png
|-- notebooks/
|   `-- lesson_29_confidence_interval_proportion.ipynb
`-- slides/
    |-- lesson_29.tex
    `-- lesson_29.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_01_sample_proportion.py
uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_02_wald_interval.py
uv run en/L29_Confidence_Interval_Proportion/src/prop_ci_03_rare_event_wald.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L29_Confidence_Interval_Proportion/notebooks/lesson_29_confidence_interval_proportion.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_29.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_29.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The Wald interval for a population proportion and the success-failure check
follow Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory
Business Statistics 2e*, Chapter 8, Section
[8.3](https://openstax.org/books/introductory-business-statistics-2e/pages/8-3-a-confidence-interval-for-a-population-proportion).
Sample-size planning for a chosen margin of error is prepared for Section
[8.4](https://openstax.org/books/introductory-business-statistics-2e/pages/8-4-calculating-the-sample-size-n-continuous-and-binary-random-variables)
in Lesson 30. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

