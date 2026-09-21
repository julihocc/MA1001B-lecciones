# Lesson 32 - F Distribution and Comparing Two Variances

This 50-minute micro-lesson compares two fully synthetic packing stations
through the ratio $F=s_{1}^{2}/s_{2}^{2}$. The upper-tail probability comes
from `scipy.stats.f.sf`. The final step shows that the two-variance $F$ test
is sensitive to non-normality: equal-variance $t(3)$ samples inflate the Type
I rate.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 12, Section 12.1 (test of two variances).
- **Prerequisites:** A single-variance chi-square interval from Lesson 31.
- **Data notice:** Every cycle time is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute two independent sample variances $s_{1}^{2}$ and $s_{2}^{2}$.
2. Form $F=s_{1}^{2}/s_{2}^{2}$ with $\mathrm{df}_{1}=n_{1}-1$ and
   $\mathrm{df}_{2}=n_{2}-1$.
3. Read the upper-tail $p$-value from the $F$ distribution.
4. Explain why the two-variance $F$ test is sensitive to non-normality.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: two independent stations | Name two sample variances. |
| 06-16 | Degrees of freedom pair | Confirm $(24,24)$. |
| 16-24 | Run Step 1 | Read $s_{1}^{2}=44.205731$ and $s_{2}^{2}=12.024693$. |
| 24-34 | $F$ ratio | Compute $3.676246$. |
| 34-42 | Run Step 2 | Obtain $p=0.001125$ and reject $H_{0}$. |
| 42-48 | Run Step 3 Type I check | Contrast $0.052200$ with $0.202400$. |
| 48-50 | Concept check and handoff to Lesson 33 | Name hypotheses and error types. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the station
samples with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `f_two_var_01_sample_variances.py` | Two sample variances | $n_{1}=n_{2}=25$; $s_{1}^{2}=44.205731$; $s_{2}^{2}=12.024693$. |
| 2 | `f_two_var_02_f_test.py` | $F$ and `f.sf` | $F=3.676246$; $F_{0.05}=1.983760$; $p=0.001125$; reject $H_{0}$. |
| 3 | `f_two_var_03_nonnormal_sensitivity.py` | Type I under heavy tails | Normal Type I $=0.052200$; $t(3)$ Type I $=0.202400$ (5000 reps). |

The Step 3 result is a limit: equal variances plus heavy tails make the $F$
test reject far too often.

## Synthetic Two-Station Sample

Station A is generated from $N(40,8)$ and Station B from $N(40,5)$, each with
$n=25$. The test is $H_{0}:\sigma_{1}^{2}=\sigma_{2}^{2}$ versus
$H_{1}:\sigma_{1}^{2}>\sigma_{2}^{2}$.

\[
F=\frac{s_{1}^{2}}{s_{2}^{2}}=\frac{44.205731}{12.024693}=3.676246,
\]

\[
p=P(F_{24,24}\ge 3.676246)=0.001125.
\]

Under equal variances, 5000 normal replications reject at rate $0.052200$,
near $\alpha=0.05$. Equal-variance $t(3)$ replications reject at $0.202400$.

## Common Misconceptions

- $F$ compares variances, not means.
- The two samples must be independent.
- A small $p$-value is not a statement about which station is faster.
- The $F$ test is not robust to heavy tails the way some mean tests are.
- The synthetic stations illustrate $F$ arithmetic. They are not a claim
  about any real packing line.

## Package Structure

```text
L32_F_Distribution_Two_Variances/
|-- README.md
|-- src/
|   |-- f_two_var_01_sample_variances.py
|   |-- f_two_var_02_f_test.py
|   `-- f_two_var_03_nonnormal_sensitivity.py
|-- figures/
|   |-- f_two_var_01_sample_variances.png
|   |-- f_two_var_02_f_test.png
|   `-- f_two_var_03_nonnormal_sensitivity.png
|-- notebooks/
|   `-- lesson_32_f_distribution_two_variances.ipynb
`-- slides/
    |-- lesson_32.tex
    `-- lesson_32.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L32_F_Distribution_Two_Variances/src/f_two_var_01_sample_variances.py
uv run en/L32_F_Distribution_Two_Variances/src/f_two_var_02_f_test.py
uv run en/L32_F_Distribution_Two_Variances/src/f_two_var_03_nonnormal_sensitivity.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L32_F_Distribution_Two_Variances/notebooks/lesson_32_f_distribution_two_variances.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_32.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_32.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The $F$ test of two variances follows Alexander Holmes, Barbara Illowsky, and
Susan Dean, *Introductory Business Statistics 2e*, Chapter 12, Section
[12.1](https://openstax.org/books/introductory-business-statistics-2e/pages/12-1-test-of-two-variances).
Hypothesis-testing language ($H_{0}$, $H_{1}$, Type I and Type II errors) is
prepared for Chapter 9, Sections
[9.1](https://openstax.org/books/introductory-business-statistics-2e/pages/9-1-null-and-alternative-hypotheses)
and
[9.2](https://openstax.org/books/introductory-business-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors)
in Lesson 33. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

