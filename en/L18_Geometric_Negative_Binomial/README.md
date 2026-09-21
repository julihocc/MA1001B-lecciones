# Lesson 18 - Geometric and Negative-Binomial Waiting Times

This 50-minute micro-lesson waits for defectives in a fully synthetic audit.
Each independent trial has success probability $p=0.12$. Students compute
$P(X=1)$ and $E[X]=1/p$ for the geometric waiting time, then wait for $r=3$
successes in the negative-binomial model. The limit is fatigue: if $p$ declines
with trial number, trials are no longer independent.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Section 4.3.
- **Prerequisites:** Bernoulli trials from Lesson 14.
- **Data notice:** Every trial and waiting time is synthetic. The scripts
  contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Define $X$ as the trial number of the first success and compute $P(X=1)=p$.
2. Compute $E[X]=1/p$ for the geometric model.
3. Extend the wait to $r=3$ successes with $E[X]=r/p$.
4. Explain why declining $p$ from fatigue makes the mean wait exceed $1/p$.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: wait for the first defective | Name $p=0.12$. |
| 06-16 | Geometric $P(X=1)=p$ | Confirm $0.120000$. |
| 16-24 | Run Step 1 | Read $E[X]=8.333333$. |
| 24-34 | Negative binomial $r=3$ | Compute $r/p=25$. |
| 34-42 | Run Step 2 | Confirm $E[X]=25.000000$ and $P(X=3)=0.001728$. |
| 42-48 | Run Step 3 with fatigue | Contrast $8.333333$ with simulated $17.162800$. |
| 48-50 | Concept check | Name independence and constant $p$. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same success
probability with `SEED = 42` and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `waiting_times_01_geometric.py` | Geometric waiting time | $P(X=1)=0.120000$, $P(X\le 5)=0.472268$, $E[X]=8.333333$, $\mathrm{Var}(X)=61.111111$. |
| 2 | `waiting_times_02_negative_binomial.py` | Trials until $r=3$ successes | $E[X]=25.000000$, $\mathrm{Var}(X)=183.333333$, $P(X=3)=p^3=0.001728$. |
| 3 | `waiting_times_03_fatigue_dependence.py` | Declining $p$ | $p$ on trial $10$ is $0.091228$; the seed-42 mean censored at 400 trials is $17.162800$, with 165 of 10,000 waits at the cap. |

Here $X$ counts trials until the first success (geometric) or until the $r$-th
success (negative binomial), matching OpenStax. scipy's \texttt{nbinom} counts
failures before $r$ successes; the scripts convert that to a trial count.

The Step 3 result is a limit: trials are not independent if fatigue changes
$p$. Because $p_t=0.12(0.97)^{t-1}$ declines geometrically, the model assigns
positive probability to never seeing a success; the limiting probability is
approximately $0.016100$. Therefore $17.162800$ is a capped simulation summary,
not an uncensored finite expectation.

## Student Study Notebook

The executed notebook
[`notebooks/lesson_18_geometric_negative_binomial.ipynb`](notebooks/lesson_18_geometric_negative_binomial.ipynb)
is a self-contained, Google Colab-compatible study guide. It reconstructs the
geometric and negative-binomial trial-count conventions, then diagnoses the
declining-$p$ fatigue model without reading repository files. It includes three
embedded figures, editable practices with collapsible answers, and executable
assertions for the verified values above, the 165 capped waits, and the
$0.016100$ limiting no-success probability.

The notebook was executed both in place and as the only lesson artifact in an
empty temporary directory. Its saved HTML and Markdown renders and all three
figures were inspected after execution.

## Common Misconceptions

- Geometric $X$ starts at $1$, not $0$, when $X$ is the trial of first success.
- $E[X]=1/p$ is a mean wait, not a probability.
- Negative binomial with $r=1$ is the geometric model.
- scipy \texttt{nbinom} uses failures, not trials, unless converted.
- The synthetic audit illustrates waiting times. It is not a claim about any
  real inspection process.

## Package Structure

```text
L18_Geometric_Negative_Binomial/
|-- README.md
|-- src/
|   |-- waiting_times_01_geometric.py
|   |-- waiting_times_02_negative_binomial.py
|   `-- waiting_times_03_fatigue_dependence.py
|-- figures/
|   |-- waiting_times_01_geometric.png
|   |-- waiting_times_02_negative_binomial.png
|   `-- waiting_times_03_fatigue_dependence.png
|-- notebooks/
|   `-- lesson_18_geometric_negative_binomial.ipynb
`-- slides/
    |-- lesson_18.tex
    `-- lesson_18.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L18_Geometric_Negative_Binomial/src/waiting_times_01_geometric.py
uv run en/L18_Geometric_Negative_Binomial/src/waiting_times_02_negative_binomial.py
uv run en/L18_Geometric_Negative_Binomial/src/waiting_times_03_fatigue_dependence.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L18_Geometric_Negative_Binomial/notebooks/lesson_18_geometric_negative_binomial.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_18.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_18.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The geometric distribution, and the waiting-time interpretation used here for
the negative binomial, follow Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Section
[4.3](https://openstax.org/books/introductory-business-statistics-2e/pages/4-3-geometric-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic audit, code, and
figures in this package are original course materials.

