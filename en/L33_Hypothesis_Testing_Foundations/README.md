# Lesson 33 - Hypothesis Testing: H0, H1, Type I and Type II Errors

This 50-minute micro-lesson sets the language of a one-sided test
$H_{0}:\mu=50$ versus $H_{1}:\mu>50$ at $\alpha=0.05$. A seed-42 simulation
recovers a Type I rate near $\alpha$. Power is then measured at $\mu=53$.
The final step shows that failing to reject $H_{0}$ is not proof that $H_{0}$
is true.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 9, Sections 9.1 and 9.2 (hypotheses; Type I and Type II errors).
- **Prerequisites:** Sampling distribution of the mean and the known-sigma z
  interval from Lessons 23 and 27.
- **Data notice:** Every cycle time is synthetic. The scripts contain no real
  company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. State $H_{0}$ and $H_{1}$ for a one-sided mean test.
2. Convert $\alpha$ into a rejection cutoff for $\bar{x}$.
3. Interpret a Type I error as rejecting a true $H_{0}$.
4. Explain why failing to reject $H_{0}$ is not proof that $H_{0}$ is true.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: $H_{0}:\mu=50$ vs $H_{1}:\mu>50$ | Write both hypotheses. |
| 06-16 | $\alpha=0.05$ as a tail area | Confirm $z^{*}=1.644854$. |
| 16-24 | Run Step 1 | Read cutoff $\bar{x}=52.193138$. |
| 24-34 | Type I definition | Name a false rejection. |
| 34-42 | Run Step 2 | Simulated Type I rate $0.053100$. |
| 42-48 | Run Step 3 power and a nearby miss | Power $0.724100$; nearby $\bar{x}=51.590798$ does not reject. |
| 48-50 | Concept check and handoff to Lesson 34 | Name the one-sample z test. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the testing setup
with `SEED = 42` and adds the next concept without importing another lesson
script. These values came from two matching executions in the locked `uv`
environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `ht_foundations_01_hypotheses_alpha.py` | $H_{0}$, $H_{1}$, $\alpha$, cutoff | $n=36$, $\sigma=8$, $\mathrm{SE}=1.333333$, $z^{*}=1.644854$, cutoff $=52.193138$. |
| 2 | `ht_foundations_02_type_i_rate.py` | Simulated Type I rate | 531 rejections in 10{,}000 $H_{0}$ samples; rate $=0.053100$. |
| 3 | `ht_foundations_03_type_ii_not_proof.py` | Power and non-proof | Power at $\mu=53$ is $0.724100$; Type II $=0.275900$; $\mu=51$ sample $\bar{x}=51.590798$ does not reject. |

The Step 3 result is a limit: a non-rejection can occur when $H_{0}$ is false.
Absence of evidence against $H_{0}$ is not proof of $H_{0}$.

## Synthetic One-Sided Test

Known $\sigma=8$, $n=36$, $\mathrm{SE}=8/\sqrt{36}=1.333333$.

\[
\bar{x}_{\text{crit}}=50+1.644854\times 1.333333=52.193138.
\]

Reject $H_{0}$ when $\bar{x}\ge 52.193138$. Under $\mu=50$ the simulated
false-rejection rate is $0.053100$. Under $\mu=53$ the test detects the shift
in $0.724100$ of 10{,}000 samples, so it still misses $0.275900$ of them.

## Common Misconceptions

- $\alpha$ is chosen before seeing the sample, not after.
- A Type I error is not ``the test is wrong''; it is a false rejection when
  $H_{0}$ is true.
- Power is not 1 just because $H_{1}$ is true.
- Failing to reject $H_{0}$ is not the same as proving $\mu=50$.
- The synthetic cycles illustrate error rates. They are not a claim about any
  real packing target.

## Package Structure

```text
L33_Hypothesis_Testing_Foundations/
|-- README.md
|-- src/
|   |-- ht_foundations_01_hypotheses_alpha.py
|   |-- ht_foundations_02_type_i_rate.py
|   `-- ht_foundations_03_type_ii_not_proof.py
|-- figures/
|   |-- ht_foundations_01_hypotheses_alpha.png
|   |-- ht_foundations_02_type_i_rate.png
|   `-- ht_foundations_03_type_ii_not_proof.png
|-- notebooks/
|   `-- lesson_33_hypothesis_testing_foundations.ipynb
`-- slides/
    |-- lesson_33.tex
    `-- lesson_33.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_01_hypotheses_alpha.py
uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_02_type_i_rate.py
uv run en/L33_Hypothesis_Testing_Foundations/src/ht_foundations_03_type_ii_not_proof.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L33_Hypothesis_Testing_Foundations/notebooks/lesson_33_hypothesis_testing_foundations.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_33.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_33.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Null and alternative hypotheses, Type I and Type II errors, and the role of
$\alpha$ follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 9, Sections
[9.1](https://openstax.org/books/introductory-business-statistics-2e/pages/9-1-null-and-alternative-hypotheses)
and
[9.2](https://openstax.org/books/introductory-business-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors).
The one-sample z test with known variance is prepared for Sections
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-distribution-needed-for-hypothesis-testing)
and
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples)
in Lesson 34. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

