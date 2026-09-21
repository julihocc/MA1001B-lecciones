# Lesson 36 - Hypothesis Test for a Business Proportion

This 50-minute micro-lesson uses one fully synthetic inspection register to
test $H_0:p=0.10$ with $n=200$ lots and $x=28$ late flags. The $z$ statistic
uses $p_0$ in the standard error. The final step shows that substituting
$\hat{p}$ into that standard error is the wrong test statistic and can flip
the $\alpha=0.05$ decision.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 9, Section 9.4 (full hypothesis-test examples, including a single
  proportion). Companion: *Introductory Statistics 2e*, Section 9.4.
- **Prerequisites:** Hypothesis-testing language from Lesson 33 and the
  one-mean $t$ test from Lesson 35.
- **Data notice:** Every lot and late flag is synthetic. The scripts contain
  no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State $H_0:p=p_0$ versus a one-sided $H_1$ for a business proportion.
2. Check $np_0>5$ and $n(1-p_0)>5$ before using a normal $z$ test.
3. Compute $z=(\hat{p}-p_0)/\sqrt{p_0(1-p_0)/n}$ and a right-tailed p-value.
4. Explain why the test standard error must use $p_0$, not $\hat{p}$.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: a 10 percent late-flag claim | Write $H_0:p=0.10$ and $H_1:p>0.10$. |
| 06-16 | Sample proportion and conditions | Confirm $28/200=0.14$ and $np_0=20$. |
| 16-24 | Run Step 1 | Read $\hat{p}=0.140000$, $np_0=20$, $n(1-p_0)=180$. |
| 24-34 | SE under $H_0$ and the $z$ formula | Write $\sqrt{0.10\times0.90/200}$. |
| 34-42 | Run Step 2 | Obtain $z=1.885618$, $p=0.029673$, reject $H_0$. |
| 42-48 | Run Step 3 | Contrast $p=0.029673$ with the wrong $p=0.051521$. |
| 48-50 | Concept check and handoff to Lesson 37 | Name the next tool: two independent means. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
counts and adds the next concept without importing another lesson script.
These values came from two matching executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `proportion_test_01_sample_and_conditions.py` | $\hat{p}$, $np_0$ and $n(1-p_0)$ | $n=200$, $x=28$, $\hat{p}=0.140000$, $p_0=0.100000$, $np_0=20$, $n(1-p_0)=180$, conditions met. |
| 2 | `proportion_test_02_z_pvalue.py` | $z$ with $p_0$ in the SE, right-tailed $p$ | $SE=0.021213$, $z=1.885618$, $p=0.029673$, $z^*=1.644854$, reject $H_0$ at $\alpha=0.05$. |
| 3 | `proportion_test_03_wrong_se_limit.py` | $\hat{p}$ in the SE is the wrong statistic | Wrong $SE=0.024536$, wrong $z=1.630278$, wrong $p=0.051521$; decision flips to do not reject $H_0$. |

The Step 3 result is a limit, not a second legitimate test. A confidence
interval for $p$ may use $\hat{p}$ in the standard error; a test of
$H_0:p=p_0$ may not. Lesson 37 moves from one sample to two independent means.

## Synthetic Inspection Register

\[
\hat{p}=\frac{28}{200}=0.14,\qquad
SE_0=\sqrt{\frac{0.10\times0.90}{200}}=0.021213,
\]

\[
z=\frac{0.14-0.10}{0.021213}=1.885618,\qquad
p=P(Z\ge 1.885618)=0.029673.
\]

The right-tailed test rejects $H_0:p=0.10$ at $\alpha=0.05$. Replacing $p_0$
with $\hat{p}$ inflates the standard error to $0.024536$ and produces
$z=1.630278$ with $p=0.051521$, which fails to reject. That second calculation
is not the hypothesis-test statistic.

## Common Misconceptions

- $\hat{p}$ estimates $p$, but the test of $H_0:p=p_0$ standardizes with $p_0$.
- The Wald interval SE and the test SE are not interchangeable.
- $np_0$ and $n(1-p_0)$ are checked under $H_0$, not with $\hat{p}$.
- Failing to reject after using the wrong SE is not a second analysis of the
  same hypothesis; it is a different, incorrect statistic.
- The synthetic late flags illustrate the $z$ procedure. They are not a claim
  about any real inspection process.

## Package Structure

```text
L36_Hypothesis_Test_Proportion/
|-- README.md
|-- src/
|   |-- proportion_test_01_sample_and_conditions.py
|   |-- proportion_test_02_z_pvalue.py
|   `-- proportion_test_03_wrong_se_limit.py
|-- figures/
|   |-- proportion_test_01_sample_and_conditions.png
|   |-- proportion_test_02_z_pvalue.png
|   `-- proportion_test_03_wrong_se_limit.png
|-- notebooks/
|   `-- lesson_36_hypothesis_test_proportion.ipynb
`-- slides/
    |-- lesson_36.tex
    `-- lesson_36.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L36_Hypothesis_Test_Proportion/src/proportion_test_01_sample_and_conditions.py
uv run en/L36_Hypothesis_Test_Proportion/src/proportion_test_02_z_pvalue.py
uv run en/L36_Hypothesis_Test_Proportion/src/proportion_test_03_wrong_se_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L36_Hypothesis_Test_Proportion/notebooks/lesson_36_hypothesis_test_proportion.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_36.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_36.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The one-proportion $z$ test, the $np_0$ and $n(1-p_0)$ conditions, and the
requirement that the standard error use $p_0$ follow Alexander Holmes,
Barbara Illowsky, and Susan Dean, *Introductory Business Statistics 2e*,
Chapter 9, Sections
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-probability-distribution-needed-for-hypothesis-testing)
and
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
Companion proportion-test practice is in *Introductory Statistics 2e*, Section
[9.4](https://openstax.org/books/introductory-statistics-2e/pages/9-4-full-hypothesis-test-examples).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

