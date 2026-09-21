# Lesson 24 - Central Limit Theorem

This 50-minute micro-lesson uses one fully synthetic delay clock modeled as
an exponential population with mean $10$ minutes. The population is
right-skewed (skewness $2$). Sample means of size $n=4$ remain skewed;
sample means of size $n=40$ are closer to normal. The final step shows that
small $n$ plus skew makes the normal tail a poor approximation.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 7, Sections 7.1--7.2 (CLT for sample means and using the CLT).
  Companion practice: *Introductory Statistics 2e*, Sections 7.1--7.2.
- **Prerequisites:** Sampling distribution of $\bar x$ and
  $\mathrm{SE}=\sigma/\sqrt{n}$ from Lesson 23.
- **Data notice:** Every delay time and sample mean is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Recognize a right-skewed population that is not itself normal.
2. Compare histograms of $\bar x$ for $n=4$ and $n=40$.
3. Use the CLT statement: for large $n$, $\bar x$ is approximately normal.
4. Explain why a two-SE tail is unreliable when $n$ is small and skew is
   large.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: delays, not a bell | Name mean $=$ sd $=10$ and skewness $2$. |
| 06-16 | Run Step 1 | Read median $6.931472$ versus mean $10$. |
| 16-24 | What should $\bar x$ look like? | Predict less skew for larger $n$. |
| 24-34 | Run Step 2 | Contrast skew $1.049897$ with $0.332572$. |
| 34-42 | Two-SE tail on a Gamma mean | Compare exact versus $N(\mu,\mathrm{SE})$. |
| 42-48 | Run Step 3 | Contrast $0.042380$ with $0.022750$ at $n=4$. |
| 48-50 | Concept check and handoff to Lesson 25 | Name $\hat p$ as another sample statistic. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
exponential delay population with `SEED = 42` and adds the next concept
without importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `clt_01_skewed_population.py` | Exponential delay population | Mean $=$ sd $=10.000000$, median $=6.931472$, skewness $=2.000000$, $P(X>20)=0.135335$. |
| 2 | `clt_02_means_n4_n40.py` | 5{,}000 means, $n=4$ vs $n=40$ | $n=4$: empirical SE $5.076401$, skew $1.049897$. $n=40$: empirical SE $1.574371$, skew $0.332572$. |
| 3 | `clt_03_small_n_skew_limit.py` | Exact Gamma tail versus CLT normal | $n=4$: exact $P(\bar x>20)=0.042380$ versus normal $0.022750$. $n=40$: exact $0.030560$ versus normal $0.022750$. |

The Step 3 result is a limit. The CLT is a large-sample approximation, not a
promise at $n=4$ on a skewness-$2$ clock. Lesson 25 applies the same sampling
logic to a sample proportion $\hat p$.

## Student Study Notebook

The executed [student notebook](notebooks/lesson_24_central_limit_theorem.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Delay Population

$X\sim\mathrm{Exponential}(\text{mean}=10)$. Then $E[X]=\sigma=10$ and
skewness $=2$. For iid samples,
\[
E[\bar x]=10,\qquad
\mathrm{SE}(\bar x)=\frac{10}{\sqrt{n}},
\]
and $\bar x$ is exactly $\mathrm{Gamma}(\text{shape}=n,\text{scale}=10/n)$.
The CLT replaces that Gamma law by $N(10,10/\sqrt{n})$. At $n=4$ the two-SE
tail $P(\bar x>20)$ is $0.042380$, almost double the normal value
$0.022750$.

## Common Misconceptions

- The CLT is about $\bar x$, not about the original observations becoming
  normal.
- $n=4$ is not ``large'' on a skewness-$2$ delay clock.
- Matching means and SEs does not make the tails match.
- A normal two-SE tail of $0.022750$ can be about half the true tail.
- Larger $n$ reduces skew of $\bar x$ at rate $2/\sqrt{n}$ for this
  exponential family.
- The synthetic delays illustrate the CLT. They are not a claim about any
  real queue.

## Package Structure

```text
L24_Central_Limit_Theorem/
|-- README.md
|-- src/
|   |-- clt_01_skewed_population.py
|   |-- clt_02_means_n4_n40.py
|   `-- clt_03_small_n_skew_limit.py
|-- figures/
|   |-- clt_01_skewed_population.png
|   |-- clt_02_means_n4_n40.png
|   `-- clt_03_small_n_skew_limit.png
|-- notebooks/
|   `-- lesson_24_central_limit_theorem.ipynb
`-- slides/
    |-- lesson_24.tex
    `-- lesson_24.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L24_Central_Limit_Theorem/src/clt_01_skewed_population.py
uv run en/L24_Central_Limit_Theorem/src/clt_02_means_n4_n40.py
uv run en/L24_Central_Limit_Theorem/src/clt_03_small_n_skew_limit.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L24_Central_Limit_Theorem/notebooks/lesson_24_central_limit_theorem.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_24.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_24.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The central limit theorem for sample means and the large-sample normal
approximation follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 7, Sections
[7.1](https://openstax.org/books/introductory-business-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar)
and
[7.2](https://openstax.org/books/introductory-business-statistics-2e/pages/7-2-using-the-central-limit-theorem).
Companion CLT practice is in *Introductory Statistics 2e*, Sections
[7.1](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar)
and
[7.2](https://openstax.org/books/introductory-statistics-2e/pages/7-2-using-the-central-limit-theorem).
The small-$n$ limit prepares the sampling distribution of a proportion in
Lesson 25. OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

