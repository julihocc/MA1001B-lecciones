# Lesson 17 - Poisson Model for Rare Events

This 50-minute micro-lesson models the number of fully synthetic stoppage
events $X$ on one shift with mean rate $\lambda=3.2$. Students compute
$P(X=0)$ and $P(X\ge 6)$, simulate $10{,}000$ shifts with seed $42$, and then
replace a constant rate with a clustered mixture whose variance exceeds
$\lambda$.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Section 4.4.
- **Prerequisites:** Discrete PMFs from Lesson 13 and binomial counts from
  Lessons 14--15.
- **Data notice:** Every shift and event count is synthetic. The scripts
  contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State the Poisson mean $\lambda$ and the equal-mean-and-variance property.
2. Compute $P(X=0)$ and $P(X\ge 6)$ for $\lambda=3.2$.
3. Compare those probabilities with a seed-$42$ simulation of $10{,}000$ shifts.
4. Explain why clustered events produce overdispersion: $\mathrm{Var}(X)>\lambda$.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: rare events per shift | Name $\lambda=3.2$. |
| 06-16 | Poisson mean equals variance | Write $\mathrm{Var}(X)=\lambda$. |
| 16-24 | Run Step 1 | Read $P(X=0)=0.040762$ and $P(X\ge 6)=0.105408$. |
| 24-34 | Simulate $10{,}000$ shifts | Predict the empirical rate. |
| 34-42 | Run Step 2 | Compare $0.040000$ and $0.109000$ with the exact values. |
| 42-48 | Run Step 3 clustered mixture | See simulated variance $6.811382>\lambda$. |
| 48-50 | Concept check and handoff to Lesson 18 | Name waiting times. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same Poisson
rate with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `poisson_01_pmf.py` | Poisson PMF and tails | $\lambda=3.200000$, $P(X=0)=0.040762$, $P(X\ge 6)=0.105408$. |
| 2 | `poisson_02_simulate_shifts.py` | $10{,}000$ seed-$42$ shifts | Simulated $P(X=0)=0.040000$, $P(X\ge 6)=0.109000$, mean $3.209300$, variance $3.256094$. |
| 3 | `poisson_03_overdispersion.py` | Clustered mixture | $70\%$ $\lambda=2.0$ and $30\%$ $\lambda=6.0$; theoretical variance $6.560000$; simulated variance $6.811382$. |

The Step 3 result is a limit: if events cluster, variance exceeds $\lambda$.
Lesson 18 models waiting times until the first or $r$-th success.

## Student Study Notebook

The self-contained notebook
[`notebooks/lesson_17_poisson_rare_events.ipynb`](notebooks/lesson_17_poisson_rare_events.ipynb)
turns the three script milestones into one cumulative student workflow. It
keeps the exact Poisson model and seed-42 simulations in memory, embeds three
finishes with assertions for rate scaling, exact tails, simulation identity,
mixture moments, and overdispersion. It does not read repository files or
require network access.

The notebook was executed both in place and after being copied by itself into
an empty temporary directory. Its saved HTML and Markdown renders and all
three extracted figures were visually inspected.

## Common Misconceptions

- Poisson $X$ is a count, not a waiting time.
- $\mathrm{Var}(X)=\lambda$ is an assumption, not a data fact.
- A simulation estimate can be close to the exact PMF without replacing it.
- A mixture of rates with the same mean is not Poisson.
- The synthetic shifts illustrate rare-event arithmetic. They are not a claim
  about any real operations desk.

## Package Structure

```text
L17_Poisson_Rare_Events/
|-- README.md
|-- src/
|   |-- poisson_01_pmf.py
|   |-- poisson_02_simulate_shifts.py
|   `-- poisson_03_overdispersion.py
|-- figures/
|   |-- poisson_01_pmf.png
|   |-- poisson_02_simulate_shifts.png
|   `-- poisson_03_overdispersion.png
|-- notebooks/
|   `-- lesson_17_poisson_rare_events.ipynb
`-- slides/
    |-- lesson_17.tex
    `-- lesson_17.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L17_Poisson_Rare_Events/src/poisson_01_pmf.py
uv run en/L17_Poisson_Rare_Events/src/poisson_02_simulate_shifts.py
uv run en/L17_Poisson_Rare_Events/src/poisson_03_overdispersion.py
```

Execute and save the student notebook from the repository root:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L17_Poisson_Rare_Events/notebooks/lesson_17_poisson_rare_events.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_17.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_17.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The Poisson distribution follows Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Section
[4.4](https://openstax.org/books/introductory-business-statistics-2e/pages/4-4-poisson-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic shifts, code, and
figures in this package are original course materials.

