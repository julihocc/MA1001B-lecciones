# Lesson 35 - t Test for a Mean with Unknown Variance

This 50-minute micro-lesson uses one fully synthetic pack-out register to
replace a known-sigma z test with Student's t. The sample standard deviation
s enters the standard error, the reference curve has df = n - 1, and the
decision uses a two-sided p-value. The final step shows that n = 8 plus
right skew makes that p-value fragile.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 9, Sections 9.3 (which distribution) and 9.4 (full hypothesis-test
  examples). Companion: *Introductory Statistics 2e*, Section 9.4.
- **Prerequisites:** Hypothesis-testing language from Lesson 33 and the
  known-sigma z test from Lesson 34.
- **Data notice:** Every pack time is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State $H_0:\mu=50$ versus $H_1:\mu\neq 50$ when $\sigma$ is unknown.
2. Compute $t=(\bar{x}-\mu_0)/(s/\sqrt{n})$ and identify $df=n-1$.
3. Obtain a two-sided p-value from Student t and decide at $\alpha=0.05$.
4. Explain why a small, skewed sample makes the t p-value an unstable input.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: sigma is no longer given | Write $H_0$ and $H_1$ for a 50-minute claim. |
| 06-16 | Sample mean, s, and SE | Contrast $s/\sqrt{n}$ with a known-sigma SE. |
| 16-24 | Run Step 1 | Read $\bar{x}=52.229590$, $s=4.955099$, $t=2.845789$. |
| 24-34 | Two-sided t tail | Shade both tails and name $df=39$. |
| 34-42 | Run Step 2 | Obtain $p=0.007026$ and reject $H_0$. |
| 42-48 | Run Step 3 | Contrast $p=0.767485$ with $p=0.081584$ after dropping one delay. |
| 48-50 | Concept check and handoff to Lesson 36 | Name the next tool: a test for a proportion. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
register with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `t_test_mean_01_sample_standard_error.py` | Sample s, SE, t statistic, $df=n-1$ | $n=40$, $\bar{x}=52.229590$, $s=4.955099$, $SE=0.783470$, $df=39$, $t=2.845789$. |
| 2 | `t_test_mean_02_two_sided_pvalue.py` | Two-sided p-value and $t^*$ | Manual and scipy $p=0.007026$; $t^*=2.022691$; reject $H_0$ at $\alpha=0.05$. |
| 3 | `t_test_mean_03_small_n_skew_limit.py` | Small n plus skew | $n=8$: skewness $=1.935033$, Shapiro-Wilk $p=0.001286$, $t=0.307397$, two-sided $p=0.767485$. Drop the 83.174379-minute delay and $p$ falls to $0.081584$. The $n=40$ p-value stays between $0.001481$ and $0.013087$. |

The Step 3 result is a limit, not a new test. With $n=8$ and a long right tail,
one observation moves the p-value by an order of magnitude. Lesson 36 leaves
means and tests a business proportion.

## Synthetic Pack-Out Register

The hypothesized service standard is $\mu_0=50$ minutes. The $n=40$ sample is
drawn from a Normal$(52,6)$ generator so that the unknown-sigma story continues
the known-sigma setting of Lesson 34.

\[
t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}=\frac{52.229590-50}{0.783470}=2.845789,
\]

\[
p=2P(T_{39}\ge 2.845789)=0.007026.
\]

Because $|t|>t^*=2.022691$ and $p<\alpha=0.05$, the two-sided test rejects
$H_0:\mu=50$. The $n=8$ follow-up is a different draw: seven typical packs plus
one long delay. That sample is right-skewed, fails a Shapiro-Wilk check, and
does not support the same stable decision.

## Common Misconceptions

- Unknown $\sigma$ is not a license to keep using $z$ with $s$ in place of
  $\sigma$ without changing the reference curve.
- A two-sided p-value counts both tails, even when $\bar{x}$ sits on one side.
- Failing to reject $H_0$ in the $n=8$ sample is not proof that $\mu=50$.
- A single long delay can inflate $s$, shrink $|t|$, and move $p$ sharply.
- The synthetic pack times illustrate the t procedure. They are not a claim
  about any real fulfillment line.

## Package Structure

```text
L35_T_Test_One_Mean/
|-- README.md
|-- src/
|   |-- t_test_mean_01_sample_standard_error.py
|   |-- t_test_mean_02_two_sided_pvalue.py
|   `-- t_test_mean_03_small_n_skew_limit.py
|-- figures/
|   |-- t_test_mean_01_sample_standard_error.png
|   |-- t_test_mean_02_two_sided_pvalue.png
|   `-- t_test_mean_03_small_n_skew_limit.png
|-- notebooks/
|   `-- lesson_35_t_test_one_mean.ipynb
`-- slides/
    |-- lesson_35.tex
    `-- lesson_35.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L35_T_Test_One_Mean/src/t_test_mean_01_sample_standard_error.py
uv run en/L35_T_Test_One_Mean/src/t_test_mean_02_two_sided_pvalue.py
uv run en/L35_T_Test_One_Mean/src/t_test_mean_03_small_n_skew_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L35_T_Test_One_Mean/notebooks/lesson_35_t_test_one_mean.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_35.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_35.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The one-sample t test when $\sigma$ is unknown, the $t$ statistic, degrees of
freedom $n-1$, and two-sided decisions follow Alexander Holmes, Barbara
Illowsky, and Susan Dean, *Introductory Business Statistics 2e*, Chapter 9,
Sections
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-probability-distribution-needed-for-hypothesis-testing)
and
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
Companion one-mean t practice is in *Introductory Statistics 2e*, Section
[9.4](https://openstax.org/books/introductory-statistics-2e/pages/9-4-full-hypothesis-test-examples).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

