# Lesson 28 - Student t Interval when sigma is Unknown

This 50-minute micro-lesson uses the same fully synthetic filling-line sample
as Lesson 27, but now $\sigma$ is unknown. The interval uses $s$ and a $t$
critical value with $\mathrm{df}=n-1$. The final step shows that one extreme
outlier inflates $s$ and the interval.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 8, Section 8.2 (confidence interval when $\sigma$ is unknown).
- **Prerequisites:** The known-sigma z interval from Lesson 27.
- **Data notice:** Every fill volume is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $s$ and the estimated standard error $s/\sqrt{n}$.
2. Obtain $t^{*}$ from the $t$ distribution with $\mathrm{df}=n-1$.
3. Form the 95% $t$ interval $\bar{x}\pm t^{*}\cdot s/\sqrt{n}$.
4. Explain how one extreme outlier inflates $s$ and the interval width.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: $\sigma$ is no longer known | Name $s$ as the scale estimate. |
| 06-16 | Degrees of freedom $n-1$ | Confirm $\mathrm{df}=35$. |
| 16-24 | Run Step 1 | Read $s=8.390375$ and $\widehat{\mathrm{SE}}=1.398396$. |
| 24-34 | $t^{*}$ versus $z^{*}=1.96$ | See $t^{*}=2.030108$. |
| 34-42 | Run Step 2 | Obtain $[499.899604, 505.577392]$. |
| 42-48 | Run Step 3 with a 560 ml fill | See $s$ rise to $12.616189$. |
| 48-50 | Concept check and handoff to Lesson 29 | Name the next target: a proportion. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
fills with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `t_ci_mean_01_sample_sd.py` | $s$ and $s/\sqrt{n}$ | $n=36$, $\mathrm{df}=35$, $\bar{x}=502.738498$, $s=8.390375$, $\widehat{\mathrm{SE}}=1.398396$. |
| 2 | `t_ci_mean_02_t_interval.py` | $t^{*}$ from `scipy.stats.t.ppf` | $t^{*}=2.030108$; margin $=2.838894$; CI $[499.899604, 505.577392]$; covers true $\mu=502$. |
| 3 | `t_ci_mean_03_outlier_inflates_s.py` | One 560 ml outlier inflates $s$ | Contaminated $s=12.616189$; CI $[499.767301, 508.304710]$; width inflation $=2.859620$. |

The Step 3 result is a limit of the $t$ interval: the formula remains
algebraically defined after an outlier, but $s$ is no longer a stable scale
estimate. Lesson 29 leaves means and estimates a population proportion.

The executed [student notebook](notebooks/lesson_28_t_confidence_interval_mean.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Filling-Line Sample

The analyst does not know $\sigma$. The scripts generate $n=36$ iid fills from
$N(502, 10)$ with `SEED = 42`, matching Lesson 27, then estimate scale from
the sample.

\[
\widehat{\mathrm{SE}}=\frac{s}{\sqrt{n}}=\frac{8.390375}{\sqrt{36}}=1.398396,
\]

\[
t^{*}=t_{0.975,35}=2.030108,
\]

\[
\bar{x}\pm t^{*}\cdot\widehat{\mathrm{SE}}=[499.899604, 505.577392].
\]

Replacing the last fill by $560$ ml shifts $\bar{x}$ to $504.036006$ and
inflates $s$ from $8.390375$ to $12.616189$. The interval width grows from
$5.677789$ to $8.537408$.

## Common Misconceptions

- $s$ is not $\sigma$. The extra uncertainty is why $t^{*}>z^{*}$.
- A $t$ interval is not automatically wider than the Lesson 27 z interval:
  this sample has $s<\sigma$, so the $t$ margin can still be smaller.
- One extreme observation can dominate $s$ even when $n=36$.
- The $t$ procedure assumes approximate normality of the population.
- Covering the hidden $\mu$ in this seed-42 sample does not prove robustness
  to outliers.
- The synthetic fills illustrate $t$ arithmetic. They are not a claim about
  any real filling line.

## Package Structure

```text
L28_T_Confidence_Interval_Mean/
|-- README.md
|-- src/
|   |-- t_ci_mean_01_sample_sd.py
|   |-- t_ci_mean_02_t_interval.py
|   `-- t_ci_mean_03_outlier_inflates_s.py
|-- figures/
|   |-- t_ci_mean_01_sample_sd.png
|   |-- t_ci_mean_02_t_interval.png
|   `-- t_ci_mean_03_outlier_inflates_s.png
|-- notebooks/
|   `-- lesson_28_t_confidence_interval_mean.ipynb
`-- slides/
    |-- lesson_28.tex
    `-- lesson_28.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_01_sample_sd.py
uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_02_t_interval.py
uv run en/L28_T_Confidence_Interval_Mean/src/t_ci_mean_03_outlier_inflates_s.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L28_T_Confidence_Interval_Mean/notebooks/lesson_28_t_confidence_interval_mean.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_28.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_28.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The Student $t$ interval for a mean when the population standard deviation is
unknown follows Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 8, Section
[8.2](https://openstax.org/books/introductory-business-statistics-2e/pages/8-2-a-confidence-interval-when-the-population-standard-deviation-is-unknown-and-small-sample-case).
The next target, a population proportion, is prepared for Section
[8.3](https://openstax.org/books/introductory-business-statistics-2e/pages/8-3-a-confidence-interval-for-a-population-proportion)
in Lesson 29. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

