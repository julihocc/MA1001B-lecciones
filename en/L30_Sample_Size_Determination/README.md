# Lesson 30 - Sample Size for Margin of Error and Budget

This 50-minute micro-lesson plans $n$ before data are collected. A mean
margin of error uses $n=(z^{*}s/E)^{2}$. A proportion uses
$n=z^{*2}p(1-p)/E^{2}$, with $p=0.5$ as the conservative planning value.
The final step shows that $E=0.01$ can demand a sample the budget cannot
fund.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 8, Section 8.4 (calculating the sample size $n$).
- **Prerequisites:** z intervals for a mean and a proportion from Lessons
  27 and 29.
- **Data notice:** Every planning value, cost, and budget figure is synthetic.
  The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $n=(z^{*}s/E)^{2}$ for a mean and round up.
2. Compute $n=z^{*2}p(1-p)/E^{2}$ for a proportion.
3. Explain why $p=0.5$ is the conservative planning value.
4. Compare a statistically required $n$ with the $n$ a budget can fund.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: choose $E$ before sampling | Write the mean formula. |
| 06-16 | Plug in $z^{*}=1.96$, $s=10$, $E=2$ | Obtain raw $n=96.040000$. |
| 16-24 | Run Step 1 | Round up to $n=97$. |
| 24-34 | Proportion formula with $p=0.5$ | See $p(1-p)=0.25$. |
| 34-42 | Run Step 2 | Obtain $n=1068$ versus $631$ at $p=0.18$. |
| 42-48 | Run Step 3 with $E=0.01$ | Required $n=9604$; affordable $n=1666$. |
| 48-50 | Concept check and handoff to Lesson 31 | Name variance as the next parameter. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the planning
constants with `SEED = 42` reserved and adds the next concept without
importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `sample_size_01_mean_margin.py` | $n=(z^{*}s/E)^{2}$ | Raw $n=96.040000$; rounded-up $n=97$. |
| 2 | `sample_size_02_proportion_conservative.py` | Conservative $p=0.5$ | $n=1068$ at $p=0.5$; $n=631$ at $p=0.18$; extra $=437$. |
| 3 | `sample_size_03_budget_vs_precision.py` | $E=0.01$ versus budget | Required $n=9604$; affordable $n=1666$; cost $\$115{,}248$; cannot fund. |

The Step 3 result is a limit: shrinking $E$ inflates $n$ with $1/E^{2}$. A
desired margin is not the same as a fundable study.

## Synthetic Planning Values

Mean handling time: $s=10$ minutes, $E=2$ minutes, $z^{*}=1.96$.

\[
n=\left(\frac{1.96\times 10}{2}\right)^{2}=96.040000 \;\to\; 97.
\]

First-contact proportion: $E=0.03$, conservative $p=0.5$.

\[
n=\frac{1.96^{2}\times 0.25}{0.03^{2}}=1067.111111 \;\to\; 1068.
\]

Tight margin $E=0.01$ at $p=0.5$ requires $n=9604$. At $\$12$ per observation
and a $\$20{,}000$ budget, only $1666$ observations are affordable.

## Common Misconceptions

- Sample size is chosen before the data, from a planning $s$ or $p$, not from
  the eventual sample.
- $p=0.5$ is conservative because $p(1-p)$ is then maximized.
- Rounding down understates the sample needed to hit $E$.
- A smaller $E$ is not free: $n$ grows with $1/E^{2}$.
- A budget constraint can make a statistically nice $E$ infeasible.
- The synthetic costs illustrate planning arithmetic. They are not a claim
  about any real study.

## Package Structure

```text
L30_Sample_Size_Determination/
|-- README.md
|-- src/
|   |-- sample_size_01_mean_margin.py
|   |-- sample_size_02_proportion_conservative.py
|   `-- sample_size_03_budget_vs_precision.py
|-- figures/
|   |-- sample_size_01_mean_margin.png
|   |-- sample_size_02_proportion_conservative.png
|   `-- sample_size_03_budget_vs_precision.png
|-- notebooks/
|   `-- lesson_30_sample_size_determination.ipynb
`-- slides/
    |-- lesson_30.tex
    `-- lesson_30.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L30_Sample_Size_Determination/src/sample_size_01_mean_margin.py
uv run en/L30_Sample_Size_Determination/src/sample_size_02_proportion_conservative.py
uv run en/L30_Sample_Size_Determination/src/sample_size_03_budget_vs_precision.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L30_Sample_Size_Determination/notebooks/lesson_30_sample_size_determination.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three planning steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_30.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_30.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Sample-size formulas for a mean and a proportion follow Alexander Holmes,
Barbara Illowsky, and Susan Dean, *Introductory Business Statistics 2e*,
Chapter 8, Section
[8.4](https://openstax.org/books/introductory-business-statistics-2e/pages/8-4-calculating-the-sample-size-n-continuous-and-binary-random-variables).
Intervals for a variance using the chi-square distribution are prepared for
Section
[11.2](https://openstax.org/books/introductory-business-statistics-2e/pages/11-2-test-of-a-single-variance)
in Lesson 31. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

