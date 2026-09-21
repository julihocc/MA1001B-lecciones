# Lesson 43 - Experimental Design: Factors and Randomization

This 50-minute micro-lesson uses one fully synthetic packing line to define a
three-level factor, randomly assign 36 stations, and contrast that experiment
with self-selected groups. The final step shows that an observational factor
is not a randomized treatment.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 12 introduction and Section 12.2 (one-way ANOVA setup: factor,
  response, and independent samples).
- **Prerequisites:** Two-sample comparisons from Lessons 37-39 and the idea
  that association is not causation from Lesson 41.
- **Data notice:** Every station, experience value, packing method, and cycle
  time is synthetic. The scripts contain no real company, customer, or partner
  data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Name the experimental factor, its levels, the experimental units, and the
   response.
2. Explain why random assignment balances pretreatment covariates in
   expectation.
3. Compare group means after a randomized assignment of 36 units.
4. State why self-selected groups mix the factor with who chose the level.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: three packing methods, 36 stations | Name factor, units, and response. |
| 06-16 | Random assignment of 12 stations per method | Confirm the assignment is balanced. |
| 16-24 | Run Step 1 | Read counts $12$, $12$, $12$ and experience gap $1.047694$. |
| 24-34 | Cycle times after randomization | Compare the three randomized means. |
| 34-42 | Run Step 2 | Obtain Auto-Standard gap $-8.019206$ versus true effect $-7$. |
| 42-48 | Run Step 3 and the self-selection limit | Contrast experience gaps $1.047694$ and $5.216727$. |
| 48-50 | Concept check and handoff to Lesson 44 | Ask whether a significant $F$ can name the pair. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
stations with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `experimental_design_01_factor_randomization.py` | Three-level factor and random assignment of 36 units | $n=12$ per method; mean experience $4.618485$, $5.943166$, $5.666180$ years; Auto-Standard experience gap $1.047694$. |
| 2 | `experimental_design_02_randomized_outcomes.py` | Cycle times after randomization | Means $51.871576$, $50.039332$, $43.852371$ seconds; randomized Auto-Standard gap $-8.019206$; true Automated effect $-7$. |
| 3 | `experimental_design_03_self_selection_limit.py` | Self-selected groups confound method with experience | Self-selected experience $2.678106$, $5.654891$, $7.894834$ years; observational experience gap $5.216727$; observational $Y$ gap $-14.809630$. |

The Step 3 result is a design limit. Operators with more experience choose
Automated, so the observational gap mixes the method with who selected it.
Lesson 44 analyzes the randomized three-group response with one-way ANOVA.

## Synthetic Packing-Line Experiment

True additive effects on cycle time, in seconds, are $0$ (Standard), $-2$
(Guided), and $-7$ (Automated). Random assignment does not use operator
experience to choose a method. Self-selection assigns the lowest experience
tertile to Standard, the middle tertile to Guided, and the highest tertile to
Automated.

Randomized Auto-Standard gap:

\[
\bar y_{\text{Automated}}-\bar y_{\text{Standard}}=-8.019206.
\]

Observational Auto-Standard gap:

\[
\bar y_{\text{self-selected Automated}}-\bar y_{\text{self-selected Standard}}=-14.809630.
\]

The observational comparison overstates the method effect because experience
is no longer a balanced covariate.

## Common Misconceptions

- A factor level observed in operations is not automatically a treatment.
- Random assignment balances covariates in expectation; it does not make every
  sample mean identical.
- A large observational gap can be the wrong causal number even when $n$ is
  balanced.
- The synthetic packing line illustrates design. It is not a claim about any
  real warehouse.

## Package Structure

```text
L43_Experimental_Design_Principles/
|-- README.md
|-- src/
|   |-- experimental_design_01_factor_randomization.py
|   |-- experimental_design_02_randomized_outcomes.py
|   `-- experimental_design_03_self_selection_limit.py
|-- figures/
|   |-- experimental_design_01_factor_randomization.png
|   |-- experimental_design_02_randomized_outcomes.png
|   `-- experimental_design_03_self_selection_limit.png
|-- notebooks/
|   `-- lesson_43_experimental_design_principles.ipynb
`-- slides/
    |-- lesson_43.tex
    `-- lesson_43.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L43_Experimental_Design_Principles/src/experimental_design_01_factor_randomization.py
uv run en/L43_Experimental_Design_Principles/src/experimental_design_02_randomized_outcomes.py
uv run en/L43_Experimental_Design_Principles/src/experimental_design_03_self_selection_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L43_Experimental_Design_Principles/notebooks/lesson_43_experimental_design_principles.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_43.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_43.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Experimental factors, independent samples, and the setup for comparing more
than two means follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 12,
[Introduction](https://openstax.org/books/introductory-business-statistics-2e/pages/12-introduction)
and Section
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

