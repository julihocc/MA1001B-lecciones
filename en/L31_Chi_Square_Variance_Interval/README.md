# Lesson 31 - Chi-Square and a Confidence Interval for Variance

This 50-minute micro-lesson uses one fully synthetic packing-station sample
of $n=20$ cycle times to estimate $\sigma^{2}$. The interval uses chi-square
critical values with $\mathrm{df}=n-1$. The final step shows that non-normal
data invalidate the procedure: coverage collapses under exponential cycles.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 11, Section 11.2 (test of a single variance), used here to build
  the matching interval for $\sigma^{2}$.
- **Prerequisites:** Sample variance and the idea of a sampling distribution
  from earlier estimation lessons.
- **Data notice:** Every cycle time is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $s^{2}$ with divisor $n-1$.
2. Obtain chi-square critical values with $\mathrm{df}=n-1$.
3. Form the 95% interval $((n-1)s^{2}/\chi^{2}_{U},(n-1)s^{2}/\chi^{2}_{L})$.
4. Explain why non-normal data invalidate the chi-square variance interval.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: variance as a process parameter | Name $s^{2}$ as the point estimate. |
| 06-16 | Degrees of freedom $n-1$ | Confirm $\mathrm{df}=19$. |
| 16-24 | Run Step 1 | Read $s^{2}=6.814885$. |
| 24-34 | Chi-square quantiles | See $8.906516$ and $32.852327$. |
| 34-42 | Run Step 2 | Obtain $[3.941359, 14.537986]$. |
| 42-48 | Run Step 3 coverage check | Contrast $0.949400$ with $0.737200$. |
| 48-50 | Concept check and handoff to Lesson 32 | Name a second variance and $F$. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
cycles with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `chi2_var_01_sample_variance.py` | $s^{2}$ with $\mathrm{df}=19$ | $n=20$, $\bar{x}=11.901204$, $s=2.610533$, $s^{2}=6.814885$. |
| 2 | `chi2_var_02_variance_interval.py` | Chi-square 95% interval for $\sigma^{2}$ | $\chi^{2}_{L}=8.906516$, $\chi^{2}_{U}=32.852327$; CI $[3.941359, 14.537986]$; covers hidden $\sigma^{2}=9$. |
| 3 | `chi2_var_03_nonnormal_limit.py` | Coverage under non-normal cycles | Normal coverage $0.949400$; exponential coverage $0.737200$ (5000 reps). |

The Step 3 result is a limit: the formula still runs on skewed data, but it
no longer covers near 95% of the time.

## Synthetic Packing Cycles

The scripts generate $n=20$ iid $N(12,3)$ cycle times so that the hidden
$\sigma^{2}=9$ can be checked.

\[
\frac{(n-1)s^{2}}{\chi^{2}_{0.975,19}}
\le \sigma^{2} \le
\frac{(n-1)s^{2}}{\chi^{2}_{0.025,19}},
\]

\[
[3.941359, 14.537986].
\]

The interval is not symmetric about $s^{2}$. Exponential cycles with true
variance $144$ yield empirical coverage $0.737200$.

## Common Misconceptions

- The chi-square interval for $\sigma^{2}$ is not $\bar{x}\pm z\cdot\mathrm{SE}$.
- Critical values sit in the denominator, so the larger chi-square value
  produces the lower bound.
- Approximate 95% coverage is a property of the method under normality, not
  a guarantee for one sample.
- Skewed cycle times can keep $s^{2}$ defined while destroying coverage.
- The synthetic cycles illustrate chi-square arithmetic. They are not a claim
  about any real packing station.

## Package Structure

```text
L31_Chi_Square_Variance_Interval/
|-- README.md
|-- src/
|   |-- chi2_var_01_sample_variance.py
|   |-- chi2_var_02_variance_interval.py
|   `-- chi2_var_03_nonnormal_limit.py
|-- figures/
|   |-- chi2_var_01_sample_variance.png
|   |-- chi2_var_02_variance_interval.png
|   `-- chi2_var_03_nonnormal_limit.png
|-- notebooks/
|   `-- lesson_31_chi_square_variance_interval.ipynb
`-- slides/
    |-- lesson_31.tex
    `-- lesson_31.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_01_sample_variance.py
uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_02_variance_interval.py
uv run en/L31_Chi_Square_Variance_Interval/src/chi2_var_03_nonnormal_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L31_Chi_Square_Variance_Interval/notebooks/lesson_31_chi_square_variance_interval.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_31.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_31.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The chi-square sampling distribution of $(n-1)s^{2}/\sigma^{2}$ and inference
for a single variance follow Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Chapter 11, Section
[11.2](https://openstax.org/books/introductory-business-statistics-2e/pages/11-2-test-of-a-single-variance).
Comparing two variances with the $F$ distribution is prepared for Section
[12.1](https://openstax.org/books/introductory-business-statistics-2e/pages/12-1-test-of-two-variances)
in Lesson 32. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

