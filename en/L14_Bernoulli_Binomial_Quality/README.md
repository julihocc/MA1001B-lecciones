# Lesson 14 - Bernoulli Trials and the Binomial Model

This 50-minute micro-lesson models a fully synthetic inspection of $n=20$
units, each defective with chance $p=0.08$. Students start from one Bernoulli
trial, compute $P(X=0)$, $P(X\le 2)$, $np$, and $np(1-p)$, and then break the
constant-$p$ assumption with a two-point mixture of lots.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Section 4.2.
- **Prerequisites:** Discrete random variables from Lesson 13.
- **Data notice:** Every trial, defect flag, and lot type is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State the Bernoulli trial and the four binomial assumptions.
2. Compute $P(X=0)$ and $P(X\le 2)$ for $X\sim\mathrm{Binomial}(20,0.08)$.
3. Report the mean $np$ and the variance $np(1-p)$.
4. Explain why a mixture of lot types with the same average $p$ is not binomial.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: one inspection | Label success as defective, $p=0.08$. |
| 06-16 | Four binomial assumptions | Check $n$, two outcomes, constant $p$, independence. |
| 16-24 | Run Step 1 | Confirm $q=0.920000$ and $np=1.600000$. |
| 24-34 | Binomial PMF and left tail | Compute $P(X=0)=(0.92)^{20}$. |
| 34-42 | Run Step 2 | Read $P(X=0)=0.188693$ and $P(X\le 2)=0.787946$. |
| 42-48 | Run Step 3 with mixed lots | Contrast $0.188693$ with mixture $0.358291$. |
| 48-50 | Concept check and handoff to Lesson 15 | Name the constant-$p$ limit. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
inspection with `SEED = 42` reserved and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `binomial_01_bernoulli_trials.py` | Bernoulli trial and binomial ingredients | $p=0.080000$, $q=0.920000$, $n=20$, $np=1.600000$. |
| 2 | `binomial_02_pmf_cdf.py` | Binomial PMF, CDF, moments | $P(X=0)=0.188693$, $P(X\le 2)=0.787946$, $\mathrm{Var}(X)=1.472000$. |
| 3 | `binomial_03_nonconstant_p.py` | Mixture of $p=0.02$ and $p=0.14$ | Average $p$ still $0.080000$; mixture $P(X=0)=0.358291$; mixture variance $2.840000$. |

The Step 3 result is a limit: matching the average $p$ does not restore the
binomial model. Lesson 15 keeps the binomial model and compares two policies
that share the same mean $np$.

## Study Notebook

The executed, self-contained study guide is
[`notebooks/lesson_14_bernoulli_binomial_quality.ipynb`](notebooks/lesson_14_bernoulli_binomial_quality.ipynb).
It keeps the same $n=20$ inspection state across the Bernoulli, exact-binomial,
and mixed-lot steps and embeds three figures. It also includes editable
values. The notebook has been executed both in place and from an empty
temporary directory; its HTML and Markdown renders and all three figures were
inspected.

## Common Misconceptions

- A Bernoulli trial has two outcomes; the binomial counts successes in $n$ of them.
- $P(X=0)=(1-p)^n$ uses the constant-$p$ assumption on every trial.
- $np$ is a mean, not a probability.
- Lots with $p=0.02$ and $p=0.14$ averaging $0.08$ are not $\mathrm{Binomial}(20,0.08)$.
- The synthetic inspection illustrates the model. It is not a claim about any
  real process.

## Package Structure

```text
L14_Bernoulli_Binomial_Quality/
|-- README.md
|-- notebooks/
|   `-- lesson_14_bernoulli_binomial_quality.ipynb
|-- src/
|   |-- binomial_01_bernoulli_trials.py
|   |-- binomial_02_pmf_cdf.py
|   `-- binomial_03_nonconstant_p.py
|-- figures/
|   |-- binomial_01_bernoulli_trials.png
|   |-- binomial_02_pmf_cdf.png
|   `-- binomial_03_nonconstant_p.png
`-- slides/
    |-- lesson_14.tex
    `-- lesson_14.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L14_Bernoulli_Binomial_Quality/src/binomial_01_bernoulli_trials.py
uv run en/L14_Bernoulli_Binomial_Quality/src/binomial_02_pmf_cdf.py
uv run en/L14_Bernoulli_Binomial_Quality/src/binomial_03_nonconstant_p.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L14_Bernoulli_Binomial_Quality/notebooks/lesson_14_bernoulli_binomial_quality.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_14.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_14.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Bernoulli trials and the binomial probability distribution follow Alexander
Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business Statistics 2e*,
Section
[4.2](https://openstax.org/books/introductory-business-statistics-2e/pages/4-2-binomial-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic inspection, code,
and figures in this package are original course materials.

