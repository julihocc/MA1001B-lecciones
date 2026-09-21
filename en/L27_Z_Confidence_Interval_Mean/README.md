# Lesson 27 - Z Confidence Interval for a Mean (sigma known)

This 50-minute micro-lesson uses one fully synthetic filling-line sample to
build a 95% z interval when the population standard deviation is treated as
known. The final step shows that replacing $\sigma$ by $s$ while keeping
$z^{*}=1.96$ is the wrong tool, which Lesson 28 names as the Student $t$
interval.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 8, Section 8.1 (confidence interval when $\sigma$ is known or the
  sample is large).
- **Prerequisites:** Sampling distribution of the mean and the Central Limit
  Theorem from Lessons 23-24, plus point estimation from Lesson 26.
- **Data notice:** Every fill volume is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute the standard error $\sigma/\sqrt{n}$ when $\sigma$ is known.
2. Form the 95% z interval $\bar{x}\pm 1.96\cdot\sigma/\sqrt{n}$.
3. Interpret the interval as a range for the unknown mean, not for one bottle.
4. Explain why an unknown $\sigma$ makes the z interval the wrong procedure.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: known $\sigma$, unknown $\mu$ | Name the point estimate $\bar{x}$. |
| 06-16 | Standard error $\sigma/\sqrt{n}$ | Confirm $10/\sqrt{36}=1.666667$. |
| 16-24 | Run Step 1 | Read $\bar{x}=502.738498$ ml. |
| 24-34 | Margin $1.96\times$ SE | Compute $3.266667$ ml. |
| 34-42 | Run Step 2 | Obtain $[499.471831, 506.005165]$. |
| 42-48 | Run Step 3 and contrast $s$ with $\sigma$ | See $s=8.390375\neq 10$. |
| 48-50 | Concept check and handoff to Lesson 28 | Name $t$ as the unknown-$\sigma$ tool. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
fills with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `z_ci_mean_01_sample_standard_error.py` | Sample mean and known-sigma SE | $n=36$, $\sigma=10$, $\bar{x}=502.738498$, $\mathrm{SE}=1.666667$. |
| 2 | `z_ci_mean_02_z_interval.py` | 95% z interval with $z^{*}=1.96$ | Margin $=3.266667$; CI $[499.471831, 506.005165]$; width $=6.533333$; covers true $\mu=502$. |
| 3 | `z_ci_mean_03_unknown_sigma_limit.py` | $s$ is not $\sigma$; z-with-$s$ is invalid | $s=8.390375$; invalid z-with-$s$ interval $[499.997642, 505.479354]$; width difference $=1.051622$. |

The Step 3 result is a limit, not a $t$ interval yet. The valid z interval
requires a known $\sigma$. Lesson 28 replaces $z^{*}$ by a $t$ critical value
with $\mathrm{df}=n-1$.

The executed [student notebook](notebooks/lesson_27_z_confidence_interval_mean.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Filling-Line Sample

The analyst treats $\sigma=10$ ml as known from long-run process capability
and does not know $\mu$. The scripts generate $n=36$ iid fills from
$N(502, 10)$ only so that coverage of the hidden mean can be checked.

\[
\mathrm{SE}=\frac{\sigma}{\sqrt{n}}=\frac{10}{\sqrt{36}}=1.666667,
\]

\[
\bar{x}\pm 1.96\cdot\mathrm{SE}=502.738498\pm 3.266667=[499.471831, 506.005165].
\]

The sample standard deviation from the same 36 fills is $s=8.390375$, which
is not $\sigma$. Keeping $z^{*}=1.96$ after that substitution produces a
narrower interval that is no longer a z procedure.

## Common Misconceptions

- A 95% interval is not a 95% probability statement about this one sample
  after the data are observed.
- The interval estimates the population mean, not the fill of the next bottle.
- $s$ is a statistic. It does not license the z critical value.
- A shorter interval is not automatically a better interval.
- Covering the hidden $\mu$ in this seed-42 sample does not prove the method
  always covers $\mu$.
- The synthetic fills illustrate z arithmetic. They are not a claim about any
  real filling line.

## Package Structure

```text
L27_Z_Confidence_Interval_Mean/
|-- README.md
|-- src/
|   |-- z_ci_mean_01_sample_standard_error.py
|   |-- z_ci_mean_02_z_interval.py
|   `-- z_ci_mean_03_unknown_sigma_limit.py
|-- figures/
|   |-- z_ci_mean_01_sample_standard_error.png
|   |-- z_ci_mean_02_z_interval.png
|   `-- z_ci_mean_03_unknown_sigma_limit.png
|-- notebooks/
|   `-- lesson_27_z_confidence_interval_mean.ipynb
`-- slides/
    |-- lesson_27.tex
    `-- lesson_27.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_01_sample_standard_error.py
uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_02_z_interval.py
uv run en/L27_Z_Confidence_Interval_Mean/src/z_ci_mean_03_unknown_sigma_limit.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L27_Z_Confidence_Interval_Mean/notebooks/lesson_27_z_confidence_interval_mean.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_27.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_27.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The z interval for a mean when the population standard deviation is known
follows Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory
Business Statistics 2e*, Chapter 8, Section
[8.1](https://openstax.org/books/introductory-business-statistics-2e/pages/8-1-a-confidence-interval-when-the-population-standard-deviation-is-known-or-large-sample-size).
The unknown-$\sigma$ limit is prepared for Section
[8.2](https://openstax.org/books/introductory-business-statistics-2e/pages/8-2-a-confidence-interval-when-the-population-standard-deviation-is-unknown-and-small-sample-case)
in Lesson 28. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

