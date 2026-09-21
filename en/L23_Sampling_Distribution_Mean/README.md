# Lesson 23 - Sampling Distribution of the Mean

This 50-minute micro-lesson uses one fully synthetic cycle-time population
modeled as $\mathrm{Normal}(\mu=80,\sigma=12)$ minutes. The sampling
distribution of $\bar x$ has mean $\mu$ and standard error
$\sigma/\sqrt{n}$. Sample sizes $n=9$ and $n=36$ are compared, then 5{,}000
seed-42 samples recover those standard errors. The final step shows that the
SE formula assumes iid draws from the defined population.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 7, Section 7.1 (the central limit theorem for sample means).
  Companion practice: *Introductory Statistics 2e*, Section 7.1.
- **Prerequisites:** Normal $z$ cuts and process yield from Lessons 21 and
  22.
- **Data notice:** Every cycle time and sample mean is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State that $E[\bar x]=\mu$ and $\mathrm{SE}(\bar x)=\sigma/\sqrt{n}$.
2. Compare the sampling distributions for $n=9$ and $n=36$.
3. Check the SE formula with a seeded simulation of sample means.
4. Explain why clustered, non-iid copies inflate the observed SE.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: one unit versus a sample mean | Name $\mu=80$ and $\sigma=12$. |
| 06-16 | SE formula $\sigma/\sqrt{n}$ | Compute $12/3=4$ and $12/6=2$. |
| 16-24 | Run Step 1 | Confirm SE ratio $2.000000$. |
| 24-34 | Simulate many samples of $\bar x$ | Predict empirical SE near 4 and 2. |
| 34-42 | Run Step 2 | Read $3.997160$ and $2.028859$. |
| 42-48 | Run Step 3 with clustered copies | Contrast $2.028859$ with $4.992583$. |
| 48-50 | Concept check and handoff to Lesson 24 | Name the CLT for a skewed population. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
$\mathrm{Normal}(80,12)$ population with `SEED = 42` and adds the next concept
without importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `sampling_mean_01_standard_error.py` | $\mathrm{SE}=\sigma/\sqrt{n}$ | SE$(n=9)=4.000000$, SE$(n=36)=2.000000$, ratio $=2.000000$. |
| 2 | `sampling_mean_02_n9_vs_n36.py` | 5{,}000 iid samples, seed 42 | $n=9$: mean of means $80.036617$, empirical SE $3.997160$. $n=36$: mean of means $79.994341$, empirical SE $2.028859$. |
| 3 | `sampling_mean_03_iid_limit.py` | Clustered copies break iid | Formula SE for 6 clusters $=4.898979$, clustered empirical SE $=4.992583$, inflation ratio $=2.460784$. |

The Step 3 result is a limit. Thirty-six copied observations from six
clusters are not 36 iid draws. Lesson 24 keeps iid sampling but starts from
a right-skewed population and invokes the central limit theorem.

## Student Study Notebook

The executed [student notebook](notebooks/lesson_23_sampling_distribution_mean.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Cycle-Time Population

Population: $X\sim N(80,12^2)$. For iid samples,

\[
E[\bar x]=80,\qquad
\mathrm{SE}(\bar x)=\frac{12}{\sqrt{n}}.
\]

So $\mathrm{SE}(9)=4$ and $\mathrm{SE}(36)=2$. A seed-42 experiment of
5{,}000 samples recovers $3.997160$ and $2.028859$. If each sample of 36 is
six cluster values copied six times, the observed SE rises to $4.992583$,
near $12/\sqrt{6}=4.898979$.

## Common Misconceptions

- $\sigma$ describes one observation. $\sigma/\sqrt{n}$ describes $\bar x$.
- Larger $n$ shrinks SE. It does not change the population $\sigma$.
- A simulation SE such as $2.028859$ checks the formula; it does not replace
  $2$.
- Repeating the same cluster six times does not create six new iid draws.
- The SE formula assumes iid sampling from the defined population.
- The synthetic cycle times illustrate sampling arithmetic. They are not a
  claim about any real line.

## Package Structure

```text
L23_Sampling_Distribution_Mean/
|-- README.md
|-- src/
|   |-- sampling_mean_01_standard_error.py
|   |-- sampling_mean_02_n9_vs_n36.py
|   `-- sampling_mean_03_iid_limit.py
|-- figures/
|   |-- sampling_mean_01_standard_error.png
|   |-- sampling_mean_02_n9_vs_n36.png
|   `-- sampling_mean_03_iid_limit.png
|-- notebooks/
|   `-- lesson_23_sampling_distribution_mean.ipynb
`-- slides/
    |-- lesson_23.tex
    `-- lesson_23.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L23_Sampling_Distribution_Mean/src/sampling_mean_01_standard_error.py
uv run en/L23_Sampling_Distribution_Mean/src/sampling_mean_02_n9_vs_n36.py
uv run en/L23_Sampling_Distribution_Mean/src/sampling_mean_03_iid_limit.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L23_Sampling_Distribution_Mean/notebooks/lesson_23_sampling_distribution_mean.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_23.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_23.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The sampling distribution of $\bar x$ and $\mathrm{SE}=\sigma/\sqrt{n}$
follow Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory
Business Statistics 2e*, Chapter 7, Section
[7.1](https://openstax.org/books/introductory-business-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar).
Companion sampling-distribution practice is in *Introductory Statistics 2e*,
Section
[7.1](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar).
The iid limit prepares the central limit theorem for a skewed population in
Lesson 24. OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

