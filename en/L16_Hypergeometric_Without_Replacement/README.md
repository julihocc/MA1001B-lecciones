# Lesson 16 - Hypergeometric Distribution: Sampling Without Replacement

This 50-minute micro-lesson inspects a fully synthetic lot of $N=80$ units
that contains $K=6$ defectives. A draw of $n=10$ units is taken without
replacement, so $X$ is hypergeometric. Students compute $P(X=0)$ and
$E[X]=nK/N$, then compare the binomial approximation with $p=K/N$.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Section 4.1.
- **Prerequisites:** Binomial trials from Lessons 14--15.
- **Data notice:** Every lot, defective count, and draw is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Identify $N$, $K$, and $n$ in a without-replacement draw.
2. Compute $P(X=0)$ from the hypergeometric PMF.
3. Compute $E[X]=nK/N$.
4. Explain why the binomial overstates $P(X=0)$ when $n/N$ is not small.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: without replacement | Name $N=80$, $K=6$, $n=10$. |
| 06-16 | Sampling fraction $n/N$ | Obtain $0.125$, not small. |
| 16-24 | Run Step 1 | Read $P(X=0)=0.436326$. |
| 24-34 | Mean $nK/N$ | Compute $10\times 6/80=0.75$. |
| 34-42 | Run Step 2 | Confirm $E[X]=0.750000$. |
| 42-48 | Run Step 3 | Contrast binomial $P(X=0)=0.458582$. |
| 48-50 | Concept check and handoff to Lesson 17 | Name rare events and Poisson. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
lot with `SEED = 42` reserved and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `hypergeometric_01_without_replacement.py` | Hypergeometric $P(X=0)$ | $N=80$, $K=6$, $n=10$, $n/N=0.125000$, $P(X=0)=0.436326$. |
| 2 | `hypergeometric_02_expectation.py` | $E[X]=nK/N$ | $E[X]=0.750000$, matching \texttt{scipy.stats.hypergeom.mean}. |
| 3 | `hypergeometric_03_binomial_approximation.py` | Binomial with $p=K/N$ | $p=0.075000$; binomial $P(X=0)=0.458582$; overstatement $0.022257$. |

The Step 3 result is a limit: the binomial overstates $P(X=0)$ when $n/N$ is
not small, because drawing without replacement depletes defectives. Lesson 17
models rare events with a Poisson rate.

## Student Study Notebook

The self-contained notebook
[`notebooks/lesson_16_hypergeometric_without_replacement.ipynb`](notebooks/lesson_16_hypergeometric_without_replacement.ipynb)
turns the three script milestones into one cumulative student workflow. It
keeps one synthetic finite lot in memory, embeds three figures, includes
assertions for the exact PMF, moments, approximation error, and smaller-draw
comparison. It does not read repository files or require network access.

The notebook was executed both in place and after being copied by itself into
an empty temporary directory. Its saved HTML and Markdown renders and all
three extracted figures were visually inspected.

## Common Misconceptions

- Hypergeometric trials are not independent: each draw changes the remaining
  lot.
- $E[X]=nK/N$ can match a binomial mean even when $P(X=0)$ does not.
- The binomial approximation needs a small sampling fraction $n/N$.
- The synthetic lot illustrates without-replacement sampling. It is not a claim
  about any real warehouse.

## Package Structure

```text
L16_Hypergeometric_Without_Replacement/
|-- README.md
|-- src/
|   |-- hypergeometric_01_without_replacement.py
|   |-- hypergeometric_02_expectation.py
|   `-- hypergeometric_03_binomial_approximation.py
|-- figures/
|   |-- hypergeometric_01_without_replacement.png
|   |-- hypergeometric_02_expectation.png
|   `-- hypergeometric_03_binomial_approximation.png
|-- notebooks/
|   `-- lesson_16_hypergeometric_without_replacement.ipynb
`-- slides/
    |-- lesson_16.tex
    `-- lesson_16.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L16_Hypergeometric_Without_Replacement/src/hypergeometric_01_without_replacement.py
uv run en/L16_Hypergeometric_Without_Replacement/src/hypergeometric_02_expectation.py
uv run en/L16_Hypergeometric_Without_Replacement/src/hypergeometric_03_binomial_approximation.py
```

Execute and save the student notebook from the repository root:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L16_Hypergeometric_Without_Replacement/notebooks/lesson_16_hypergeometric_without_replacement.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_16.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_16.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The hypergeometric distribution follows Alexander Holmes, Barbara Illowsky, and
Susan Dean, *Introductory Business Statistics 2e*, Section
[4.1](https://openstax.org/books/introductory-business-statistics-2e/pages/4-1-hypergeometric-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic lot, code, and
figures in this package are original course materials.

