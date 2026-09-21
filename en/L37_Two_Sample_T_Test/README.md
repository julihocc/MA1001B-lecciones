# Lesson 37 - Two Independent Means (Two-Sample t)

This 50-minute micro-lesson uses two fully synthetic warehouse shifts,
$n_A=30$ and $n_B=32$, to compare independent means with a Welch $t$ test.
Each group keeps its own $s$. The final step shows that a significant
two-sample $t$ is not a randomized experiment: associates were not assigned
to shifts, and experience differs by group.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 10, Section 10.1 (comparing two independent population means).
- **Prerequisites:** One-sample $t$ from Lesson 35 and the one-proportion $z$
  test from Lesson 36.
- **Data notice:** Every pick time and experience value is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Distinguish two independent samples from paired observations.
2. Compute a Welch $t$ statistic without pooling the two variances.
3. Read Satterthwaite degrees of freedom and a two-sided p-value.
4. Explain why an observational grouping is not a randomized treatment.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: two shifts, two independent samples | Sketch $H_0:\mu_A=\mu_B$. |
| 06-16 | Group means and sample $s$ | Contrast $n$, $\bar{x}$, and $s$ by shift. |
| 16-24 | Run Step 1 | Read $\bar{x}_A=48.100885$ and $\bar{x}_B=52.826941$. |
| 24-34 | Welch SE, not a pooled $s_p$ | Write $\sqrt{s_A^2/n_A+s_B^2/n_B}$. |
| 34-42 | Run Step 2 | Obtain $t=-3.363436$, $p=0.001382$, reject $H_0$. |
| 42-48 | Run Step 3 | Contrast experience $4.484559$ versus $1.801265$ years. |
| 48-50 | Concept check and handoff to Lesson 38 | Name the next tool: paired before-after $t$. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
shifts with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `two_sample_t_01_group_summaries.py` | Independent group summaries | $n_A=30$, $n_B=32$; $\bar{x}_A=48.100885$, $\bar{x}_B=52.826941$; $s_A=4.660494$, $s_B=6.325509$; difference $-4.726057$. |
| 2 | `two_sample_t_02_welch_test.py` | Welch $t$, Satterthwaite df, two-sided $p$ | $SE=1.405128$, $t=-3.363436$, $df=56.900423$, $p=0.001382$ (manual and scipy), $t^*=2.002541$, reject $H_0$. |
| 3 | `two_sample_t_03_observational_limit.py` | Observational confounder | Mean experience $4.484559$ versus $1.801265$ years. Associates were not randomly assigned, so the Welch $p$-value is not a causal claim. |

The Step 3 result is a limit, not a new test. Welch answers whether the two
observed means are compatible with a common $\mu$. It does not answer whether
the shift caused the difference. Lesson 38 studies paired before-after data.

## Synthetic Shift Register

Welch does not pool the variances:

\[
t=\frac{\bar{x}_A-\bar{x}_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}
=\frac{-4.726057}{1.405128}=-3.363436,
\]

with Satterthwaite $df=56.900423$. The two-sided p-value is $0.001382$, so
$H_0:\mu_A=\mu_B$ is rejected at $\alpha=0.05$. Shift A is also more
experienced by $2.683295$ years. That imbalance was not created by random
assignment.

## Common Misconceptions

- Two columns of times are not automatically paired; pairing requires a match.
- Welch does not require $s_A=s_B$ or $n_A=n_B$.
- Equal-variance pooling is a different model from the stated Welch procedure.
- A small p-value compares means. It does not identify a cause.
- The synthetic shifts illustrate two-sample $t$. They are not a claim about
  any real warehouse.

## Package Structure

```text
L37_Two_Sample_T_Test/
|-- README.md
|-- src/
|   |-- two_sample_t_01_group_summaries.py
|   |-- two_sample_t_02_welch_test.py
|   `-- two_sample_t_03_observational_limit.py
|-- figures/
|   |-- two_sample_t_01_group_summaries.png
|   |-- two_sample_t_02_welch_test.png
|   `-- two_sample_t_03_observational_limit.png
|-- notebooks/
|   `-- lesson_37_two_sample_t_test.ipynb
`-- slides/
    |-- lesson_37.tex
    `-- lesson_37.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L37_Two_Sample_T_Test/src/two_sample_t_01_group_summaries.py
uv run en/L37_Two_Sample_T_Test/src/two_sample_t_02_welch_test.py
uv run en/L37_Two_Sample_T_Test/src/two_sample_t_03_observational_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L37_Two_Sample_T_Test/notebooks/lesson_37_two_sample_t_test.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_37.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_37.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The two-sample $t$ test for independent means, the unpooled (Welch) standard
error, and the distinction between independent groups and matched pairs follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Chapter 10, Section
[10.1](https://openstax.org/books/introductory-business-statistics-2e/pages/10-1-comparing-two-independent-population-means).
Companion independent-mean practice is in *Introductory Statistics 2e*,
Section
[10.1](https://openstax.org/books/introductory-statistics-2e/pages/10-1-two-population-means-with-unknown-standard-deviations).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

