# Lesson 26 - Point Estimation: Unbiasedness, Efficiency, Consistency

This 50-minute micro-lesson uses one fully synthetic cost clock modeled as
$\mathrm{Normal}(\mu=100,\sigma=15)$. Two estimators of $\mu$ are compared:
the sample mean $\bar x$ and the one-observation estimator $X_1$. Both are
unbiased. $\bar x$ is more efficient, and raising $n$ from 20 to 200 shrinks
its spread (consistency). The final step shows that unbiasedness does not
imply small variance in a small sample.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 8 introduction (point estimates and estimator properties).
  Companion practice: *Introductory Statistics 2e*, Chapter 8 introduction.
- **Prerequisites:** Sampling distributions of $\bar x$ and $\hat p$ from
  Lessons 23 through 25.
- **Data notice:** Every cost and sample mean is synthetic. The scripts
  contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Define unbiasedness as $E[\hat\theta]=\theta$.
2. Compare efficiency through $\mathrm{Var}(\bar x)$ versus $\mathrm{Var}(X_1)$.
3. Recognize consistency as spread shrinking when $n$ grows.
4. Explain why an unbiased estimator can still be too noisy at small $n$.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: estimate $\mu=100$ from a sample | Name two candidate estimators. |
| 06-16 | Unbiasedness as ``correct on average'' | Predict both means near 100. |
| 16-24 | Run Step 1 | Read biases $-0.042690$ and $-0.083926$. |
| 24-34 | Efficiency: smaller variance wins | Compute $225/20=11.25$. |
| 34-42 | Run Step 2 | Contrast SD $3.352961$ with $1.052019$. |
| 42-48 | Run Step 3 at $n=5$ | Obtain $P(|\bar x-\mu|>10)=0.137875$. |
| 48-50 | Concept check and handoff to Lesson 27 | Name a $z$ interval around $\bar x$. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
$N(100,15)$ cost population with `SEED = 42` and adds the next concept
without importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `point_estimation_01_unbiasedness.py` | Unbiasedness of $\bar x$ and $X_1$ | Mean of $\bar x=99.957310$ (bias $-0.042690$); mean of $X_1=99.916074$ (bias $-0.083926$). |
| 2 | `point_estimation_02_efficiency_consistency.py` | Efficiency and consistency | $\mathrm{Var}(X_1)=227.612313$ versus $\mathrm{Var}(\bar x_{20})=11.242349$, ratio $20.245975$. SD of $\bar x_{200}=1.052019$ versus formula $1.060660$. |
| 3 | `point_estimation_03_small_sample_variance.py` | Small-sample noise | $n=5$: mean $100.066209$, SD $6.737762$, $P(|\bar x-\mu|>10)=0.137875$. $n=200$: the same event has probability $0.000000$. |

The Step 3 result is a limit. Being unbiased is not the same as being
precise in one small sample. Lesson 27 wraps $\bar x$ in a $z$ confidence
interval when $\sigma$ is known.

The executed [student notebook](notebooks/lesson_26_point_estimation_properties.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Cost Population

Population: $X\sim N(100,15^2)$. Estimators:

\[
E[\bar x]=\mu,\qquad \mathrm{Var}(\bar x)=\frac{15^2}{n},
\qquad
E[X_1]=\mu,\qquad \mathrm{Var}(X_1)=225.
\]

At $n=20$, $\mathrm{Var}(\bar x)=11.25$, so $\bar x$ is about 20 times more
efficient than $X_1$. At $n=5$, $\bar x$ remains unbiased but
$P(|\bar x-100|>10)=0.137875$. At $n=200$ that event is not observed in
8{,}000 seed-42 replications.

## Common Misconceptions

- Unbiasedness is a long-run average property. It is not a guarantee for
  one sample.
- $X_1$ is unbiased and still a poor estimator because its variance is
  $\sigma^2$, not $\sigma^2/n$.
- Efficiency compares variances of unbiased estimators at the same $n$.
- Consistency is about $n\to\infty$, not about a single $n=5$ draw.
- A $13.8\%$ chance of missing $\mu$ by more than 10 can be unacceptable
  even when the estimator is unbiased.
- The synthetic costs illustrate estimator properties. They are not a
  claim about any real cost process.

## Package Structure

```text
L26_Point_Estimation_Properties/
|-- README.md
|-- src/
|   |-- point_estimation_01_unbiasedness.py
|   |-- point_estimation_02_efficiency_consistency.py
|   `-- point_estimation_03_small_sample_variance.py
|-- figures/
|   |-- point_estimation_01_unbiasedness.png
|   |-- point_estimation_02_efficiency_consistency.png
|   `-- point_estimation_03_small_sample_variance.png
|-- notebooks/
|   `-- lesson_26_point_estimation_properties.ipynb
`-- slides/
    |-- lesson_26.tex
    `-- lesson_26.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L26_Point_Estimation_Properties/src/point_estimation_01_unbiasedness.py
uv run en/L26_Point_Estimation_Properties/src/point_estimation_02_efficiency_consistency.py
uv run en/L26_Point_Estimation_Properties/src/point_estimation_03_small_sample_variance.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L26_Point_Estimation_Properties/notebooks/lesson_26_point_estimation_properties.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_26.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_26.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Point estimates, unbiasedness, and the role of sample size in shrinking
estimator spread follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 8,
[Introduction](https://openstax.org/books/introductory-business-statistics-2e/pages/8-introduction).
Companion estimation setup is in *Introductory Statistics 2e*, Chapter 8,
[Introduction](https://openstax.org/books/introductory-statistics-2e/pages/8-introduction).
The small-sample variance limit prepares $z$ confidence intervals for a mean
in Lesson 27. OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

