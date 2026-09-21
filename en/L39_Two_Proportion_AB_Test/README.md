# Lesson 39 - Two Proportions in A/B Tests

This 50-minute micro-lesson uses one fully synthetic checkout A/B test with
$n_A=400$, $x_A=72$, $n_B=410$, and $x_B=61$. A pooled $z$ statistic tests
$H_0:p_A=p_B$. The final step shows that peeking at p-values at four interim
looks inflates the type I error above $\alpha=0.05$.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 10, Section 10.4 (comparing two independent population
  proportions).
- **Prerequisites:** One-proportion $z$ from Lesson 36 and two independent
  means from Lesson 37.
- **Data notice:** Every visitor and conversion flag is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute two sample conversion rates and their difference.
2. Form the pooled proportion and the SE of $\hat{p}_A-\hat{p}_B$ under $H_0$.
3. Run a two-sided $z$ test for two independent proportions.
4. Explain why peeking at p-values mid-experiment inflates type I error.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: two independent conversion rates | Write $H_0:p_A=p_B$. |
| 06-16 | Sample rates and pooled $\hat{p}$ | Confirm $72/400=0.18$ and $61/410$. |
| 16-24 | Run Step 1 | Read $\hat{p}_A=0.180000$, $\hat{p}_B=0.148780$, $p_{\text{pool}}=0.164198$. |
| 24-34 | Pooled SE and $z$ | Write $\sqrt{\hat{p}(1-\hat{p})(1/n_A+1/n_B)}$. |
| 34-42 | Run Step 2 | Obtain $z=1.199141$, $p=0.230473$, do not reject $H_0$. |
| 42-48 | Run Step 3 | Contrast type I $0.047250$ with peeked type I $0.124250$. |
| 48-50 | Concept check and handoff to Lesson 40 | Name the next tool: chi-square goodness of fit. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
synthetic A/B counts (and, in Step 3, the same seed-42 simulation) without
importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `two_proportion_01_sample_rates.py` | Two rates and pooled $\hat{p}$ | $\hat{p}_A=0.180000$, $\hat{p}_B=0.148780$, difference $0.031220$, $p_{\text{pool}}=0.164198$. |
| 2 | `two_proportion_02_pooled_z.py` | Pooled $z$ for $p_A-p_B$ | $SE=0.026035$, $z=1.199141$, $p=0.230473$, $z^*=1.959964$, do not reject $H_0$. |
| 3 | `two_proportion_03_peeking_limit.py` | Peeking inflates type I error | 8000 null experiments; one final test type I $=0.047250$; four peeks type I $=0.124250$. |

The Step 3 result is a limit, not a sequential-design recipe. A planned
$\alpha=0.05$ test uses one look at the final $n_A$ and $n_B$. Lesson 40
moves from two proportions to a chi-square fit of more than two categories.

## Synthetic A/B Register

\[
\hat{p}_A=\frac{72}{400}=0.18,\qquad
\hat{p}_B=\frac{61}{410}=0.148780,
\]

\[
\hat{p}=\frac{72+61}{810}=0.164198,\qquad
z=\frac{0.180000-0.148780}{0.026035}=1.199141.
\]

The two-sided p-value is $0.230473$, so the test does not reject
$H_0:p_A=p_B$ at $\alpha=0.05$. Under a shared null rate of $0.16$, four
interim looks raise the false-positive rate from $0.047250$ to $0.124250$.

## Common Misconceptions

- Two conversion rates are independent samples, not paired visitors.
- The test SE uses the pooled $\hat{p}$ under $H_0:p_A=p_B$, not two Wald SEs
  added after the fact without pooling.
- A non-significant A/B result is not proof that the versions are identical.
- Checking $p$ after every dashboard refresh is not the same experiment as
  one planned test.
- The synthetic checkout flags illustrate two-proportion $z$. They are not a
  claim about any real product change.

## Package Structure

```text
L39_Two_Proportion_AB_Test/
|-- README.md
|-- src/
|   |-- two_proportion_01_sample_rates.py
|   |-- two_proportion_02_pooled_z.py
|   `-- two_proportion_03_peeking_limit.py
|-- figures/
|   |-- two_proportion_01_sample_rates.png
|   |-- two_proportion_02_pooled_z.png
|   `-- two_proportion_03_peeking_limit.png
|-- notebooks/
|   `-- lesson_39_two_proportion_ab_test.ipynb
`-- slides/
    |-- lesson_39.tex
    `-- lesson_39.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L39_Two_Proportion_AB_Test/src/two_proportion_01_sample_rates.py
uv run en/L39_Two_Proportion_AB_Test/src/two_proportion_02_pooled_z.py
uv run en/L39_Two_Proportion_AB_Test/src/two_proportion_03_peeking_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L39_Two_Proportion_AB_Test/notebooks/lesson_39_two_proportion_ab_test.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_39.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_39.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The two-proportion $z$ test, the pooled estimated proportion, and independent
samples for $p_A-p_B$ follow Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Chapter 10, Section
[10.4](https://openstax.org/books/introductory-business-statistics-2e/pages/10-4-comparing-two-independent-population-proportions).
Companion two-proportion practice is in *Introductory Statistics 2e*, Section
[10.3](https://openstax.org/books/introductory-statistics-2e/pages/10-3-comparing-two-independent-population-proportions).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

