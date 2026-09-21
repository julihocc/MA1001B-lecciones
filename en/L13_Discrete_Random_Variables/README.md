# Lesson 13 - Discrete Random Variables: PMF, CDF, Expectation, Variance

This 50-minute micro-lesson specifies a fully synthetic defect count $X$ on
$\{0,1,2,3\}$ with masses $0.50$, $0.30$, $0.15$, and $0.05$. Students plot
the PMF, accumulate it into a CDF, and then compute $E[X]$ and $\mathrm{Var}(X)$
from moments. The limit is that $E[X^2]$ is not $(E[X])^2$.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Statistics 2e*, Sections
  4.1--4.2. *Introductory Business Statistics 2e* Chapter 4 moves quickly to
  named families, so the general PMF/CDF/moment language is taken from IS 2e.
- **Prerequisites:** Sample spaces and probability rules from Lessons 05--10.
- **Data notice:** Every defect count and probability mass is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State the two PMF conditions: nonnegative masses that sum to 1.
2. Build $F(x)=P(X\le x)$ by accumulating the PMF.
3. Compute $E[X]=\sum x\,P(X=x)$ and $E[X^2]=\sum x^2 P(X=x)$.
4. Obtain $\mathrm{Var}(X)=E[X^2]-(E[X])^2$ and reject $E[X^2]=(E[X])^2$.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: $X$ is a defect count | List the four possible values. |
| 06-16 | PMF conditions | Check $0.50+0.30+0.15+0.05=1$. |
| 16-24 | Run Step 1 | Read the four masses from the stem plot. |
| 24-34 | Accumulate to a CDF | Compute $F(1)=0.80$. |
| 34-42 | Run Step 2 | Obtain $P(1<X\le 3)=0.20$. |
| 42-48 | Run Step 3 | Contrast $E[X^2]=1.350000$ with $(E[X])^2=0.562500$. |
| 48-50 | Concept check and handoff to Lesson 14 | Name the Bernoulli/binomial model. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
PMF with `SEED = 42` reserved and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `discrete_rv_01_pmf.py` | Support and PMF | Masses $0.500000$, $0.300000$, $0.150000$, $0.050000$; sum $=1.000000$. |
| 2 | `discrete_rv_02_cdf.py` | CDF and interval probability | $F(0)=0.500000$, $F(1)=0.800000$, $F(2)=0.950000$, $F(3)=1.000000$; $P(1<X\le 3)=0.200000$. |
| 3 | `discrete_rv_03_expectation_variance.py` | $E[X]$, $E[X^2]$, variance | $E[X]=0.750000$, $(E[X])^2=0.562500$, $E[X^2]=1.350000$, $\mathrm{Var}(X)=0.787500$. |

The Step 3 result is a limit: squaring the mean is not the second moment.
Lesson 14 specializes this discrete language to Bernoulli trials and the
binomial model.

## Synthetic Defect-Count Distribution

\[
P(X=x)=\begin{cases}
0.50 & x=0,\\
0.30 & x=1,\\
0.15 & x=2,\\
0.05 & x=3,\\
0 & \text{otherwise.}
\end{cases}
\]

\[
E[X]=0\cdot0.50+1\cdot0.30+2\cdot0.15+3\cdot0.05=0.75,
\]
\[
E[X^2]=0+1\cdot0.30+4\cdot0.15+9\cdot0.05=1.35,
\]
\[
\mathrm{Var}(X)=1.35-0.75^2=0.7875.
\]

## Study Notebook

The executed, self-contained study guide is
[`notebooks/lesson_13_discrete_random_variables.ipynb`](notebooks/lesson_13_discrete_random_variables.ipynb).
It keeps one PMF in memory across the PMF, CDF, and moment steps and embeds
three figures. It also includes editable practice, collapsible suggested
answers, and assertions for the canonical values. The notebook has been
executed both in place and from an empty temporary directory; its HTML and
Markdown renders and all three figures were inspected.

## Common Misconceptions

- A PMF is a list of point masses, not a density on an interval.
- $F(x)$ jumps at the support points; it is a step function.
- $E[X]$ is a weighted sum, not the most likely value (here the mode is $0$).
- $E[X^2]$ is not $(E[X])^2$. The difference is the variance.
- The synthetic PMF illustrates discrete arithmetic. It is not a claim about
  any real inspection process.

## Package Structure

```text
L13_Discrete_Random_Variables/
|-- README.md
|-- notebooks/
|   `-- lesson_13_discrete_random_variables.ipynb
|-- src/
|   |-- discrete_rv_01_pmf.py
|   |-- discrete_rv_02_cdf.py
|   `-- discrete_rv_03_expectation_variance.py
|-- figures/
|   |-- discrete_rv_01_pmf.png
|   |-- discrete_rv_02_cdf.png
|   `-- discrete_rv_03_expectation_variance.png
`-- slides/
    |-- lesson_13.tex
    `-- lesson_13.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L13_Discrete_Random_Variables/src/discrete_rv_01_pmf.py
uv run en/L13_Discrete_Random_Variables/src/discrete_rv_02_cdf.py
uv run en/L13_Discrete_Random_Variables/src/discrete_rv_03_expectation_variance.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L13_Discrete_Random_Variables/notebooks/lesson_13_discrete_random_variables.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_13.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_13.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The PMF, CDF, expected value, and standard deviation of a discrete random
variable follow Barbara Illowsky and Susan Dean, *Introductory Statistics 2e*,
Sections
[4.1](https://openstax.org/books/introductory-statistics-2e/pages/4-1-probability-distribution-function-pdf-for-a-discrete-random-variable)
and
[4.2](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation).
Named families in *Introductory Business Statistics 2e* begin in Chapter
[4](https://openstax.org/books/introductory-business-statistics-2e/pages/4-introduction).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic distribution, code,
and figures in this package are original course materials.

