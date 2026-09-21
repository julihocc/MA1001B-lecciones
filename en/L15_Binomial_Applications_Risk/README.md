# Lesson 15 - Binomial Applications and Business Risk

This 50-minute micro-lesson compares two fully synthetic inspection policies
that share the same mean number of defectives: Policy A uses $n=50$ and
$p=0.04$, while Policy B uses $n=20$ and $p=0.10$. Both have $np=2$. Students
compute $P(X\ge 3)$ and then look at $P(X=0)$ and the far tail $P(X\ge 8)$.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Section 4.2.
- **Prerequisites:** Bernoulli trials and the binomial model from Lesson 14.
- **Data notice:** Every policy, trial, and defect count is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State two binomial policies that share the same mean $np$.
2. Compute $P(X\ge 3)$ for each policy.
3. Compare $P(X=0)$ and the far tail $P(X\ge 8)$.
4. Explain why matching $np$ does not match tail risk.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: two policies, one mean | Confirm $np=2$ for both. |
| 06-16 | Variance $np(1-p)$ | Obtain $1.920000$ versus $1.800000$. |
| 16-24 | Run Step 1 | Read $n$, $p$, and matching means. |
| 24-34 | $P(X\ge 3)$ | Predict whether the tails match. |
| 34-42 | Run Step 2 | See $P(X\ge 3)\approx 0.323$ but $P(X\ge 8)$ ratio $1.88$. |
| 42-48 | Run Step 3 overlay | Point to the far-tail region $x\ge 8$. |
| 48-50 | Concept check and handoff to Lesson 16 | Name sampling without replacement. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same two
policies with `SEED = 42` reserved and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `binomial_risk_01_two_policies.py` | Two policies, same mean | A: $n=50$, $p=0.040000$, $np=2.000000$, variance $1.920000$. B: $n=20$, $p=0.100000$, $np=2.000000$, variance $1.800000$. |
| 2 | `binomial_risk_02_tail_probabilities.py` | $P(X=0)$, $P(X\ge 3)$, $P(X\ge 8)$ | $P(X\ge 3)$: $0.323286$ versus $0.323073$. $P(X=0)$: $0.129886$ versus $0.121577$. $P(X\ge 8)$: $0.000781$ versus $0.000416$. |
| 3 | `binomial_risk_03_same_mean_different_tails.py` | Far-tail overlay | Far-tail ratio $A/B=1.880028$. Same mean hides a heavier far tail for Policy A. |

The Step 3 result is a limit: matching $np$ is not matching risk. $P(X\ge 3)$
happens to be almost identical, but $P(X\ge 8)$ is not. Lesson 16 replaces
independent trials with sampling without replacement.

## Student Study Notebook

The self-contained notebook
[`notebooks/lesson_15_binomial_applications_risk.ipynb`](notebooks/lesson_15_binomial_applications_risk.ipynb)
turns the three script milestones into one cumulative student workflow. It
rebuilds the two synthetic policies in memory, embeds three figures, includes
assertions for the exact policy, probability, PMF, and practice results. It
does not read repository files or require network access.

The notebook was executed both in place and after being copied by itself into
an empty temporary directory. Its saved HTML and Markdown renders and all
three extracted figures were visually inspected.

## Common Misconceptions

- Equal means do not imply equal distributions.
- $P(X\ge 3)$ can match even when a farther tail does not.
- Larger $n$ with smaller $p$ can put more mass on extreme counts.
- The synthetic policies illustrate tail risk. They are not a claim about any
  real inspection plan.

## Package Structure

```text
L15_Binomial_Applications_Risk/
|-- README.md
|-- src/
|   |-- binomial_risk_01_two_policies.py
|   |-- binomial_risk_02_tail_probabilities.py
|   `-- binomial_risk_03_same_mean_different_tails.py
|-- figures/
|   |-- binomial_risk_01_two_policies.png
|   |-- binomial_risk_02_tail_probabilities.png
|   `-- binomial_risk_03_same_mean_different_tails.png
|-- notebooks/
|   `-- lesson_15_binomial_applications_risk.ipynb
`-- slides/
    |-- lesson_15.tex
    `-- lesson_15.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L15_Binomial_Applications_Risk/src/binomial_risk_01_two_policies.py
uv run en/L15_Binomial_Applications_Risk/src/binomial_risk_02_tail_probabilities.py
uv run en/L15_Binomial_Applications_Risk/src/binomial_risk_03_same_mean_different_tails.py
```

Execute and save the student notebook from the repository root:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L15_Binomial_Applications_Risk/notebooks/lesson_15_binomial_applications_risk.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_15.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_15.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Binomial applications follow Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Section
[4.2](https://openstax.org/books/introductory-business-statistics-2e/pages/4-2-binomial-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic policies, code, and
figures in this package are original course materials.

