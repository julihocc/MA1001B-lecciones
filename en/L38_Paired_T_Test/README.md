# Lesson 38 - Paired Samples (Before-After t)

This 50-minute micro-lesson uses 25 fully synthetic packing stations measured
before and after a layout change. The observational unit is the station, so
the test is a one-sample $t$ on $d=\text{before}-\text{after}$. The final
step shows that an unpaired two-sample $t$ on the same columns ignores the
matching and can reverse the $\alpha=0.05$ decision.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 10, Section 10.6 (matched or paired samples).
- **Prerequisites:** One-sample $t$ from Lesson 35 and two independent means
  from Lesson 37.
- **Data notice:** Every handle time is synthetic. The scripts contain no
  real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Form paired differences from before-after measurements on the same units.
2. Run a one-sample $t$ test of $H_0:\mu_d=0$ with $df=n-1$.
3. Contrast the paired standard error with an unpaired two-sample SE.
4. Explain why unpaired analysis of paired data ignores the matching.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: the same 25 stations twice | Sketch $d_i=\text{before}_i-\text{after}_i$. |
| 06-16 | Mean difference and $s_d$ | Contrast $s_d$ with $s_{\text{before}}$ and $s_{\text{after}}$. |
| 16-24 | Run Step 1 | Read $\bar{d}=2.720813$, $s_d=1.525772$, $r=0.973356$. |
| 24-34 | Paired $t$ as one-sample $t$ on $d$ | Write $t=\bar{d}/(s_d/\sqrt{n})$. |
| 34-42 | Run Step 2 | Obtain $t=8.916186$, $p=4.395592\times10^{-9}$, reject $H_0$. |
| 42-48 | Run Step 3 | Contrast paired $p=4.395592\times10^{-9}$ with unpaired $p=0.147291$. |
| 48-50 | Concept check and handoff to Lesson 39 | Name the next tool: two proportions in an A/B test. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same 25
pairs with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `paired_t_01_differences.py` | Matched differences | $n=25$; $\bar{x}_{\text{before}}=54.716880$, $\bar{x}_{\text{after}}=51.996067$; $\bar{d}=2.720813$; $s_d=1.525772$; $r=0.973356$. |
| 2 | `paired_t_02_paired_test.py` | One-sample $t$ on $d$ | $SE=0.305154$, $t=8.916186$, $df=24$, $p=4.395592\times10^{-9}$, $t^*=2.063899$, reject $H_0$. |
| 3 | `paired_t_03_unpaired_limit.py` | Unpaired analysis ignores matching | Unpaired $SE=1.847143$, $t=1.472985$, $p=0.147291$, do not reject $H_0$. |

The Step 3 result is a limit, not a second legitimate test of the layout
change. The pairing is the design. Lesson 39 compares two independent
proportions in an A/B test.

## Synthetic Station Register

\[
t=\frac{\bar{d}-0}{s_d/\sqrt{n}}=\frac{2.720813}{0.305154}=8.916186,
\qquad df=24,
\]

\[
p=2P(T_{24}\ge 8.916186)=4.395592\times10^{-9}.
\]

The before-after correlation is $0.973356$. That matching shrinks the SE from
the unpaired $1.847143$ to the paired $0.305154$. Dropping the pairing
inflates $p$ from $4.395592\times10^{-9}$ to $0.147291$ and flips the
$\alpha=0.05$ decision.

## Common Misconceptions

- Two columns of times are paired only when each row is the same unit.
- The paired test does not compare $\bar{x}_{\text{before}}$ to
  $\bar{x}_{\text{after}}$ with a two-sample SE.
- A large $s_{\text{before}}$ does not block a paired finding if $s_d$ is small.
- Unpaired analysis of paired data is not a robustness check; it is the wrong
  sampling model.
- The synthetic stations illustrate paired $t$. They are not a claim about any
  real layout change.

## Package Structure

```text
L38_Paired_T_Test/
|-- README.md
|-- src/
|   |-- paired_t_01_differences.py
|   |-- paired_t_02_paired_test.py
|   `-- paired_t_03_unpaired_limit.py
|-- figures/
|   |-- paired_t_01_differences.png
|   |-- paired_t_02_paired_test.png
|   `-- paired_t_03_unpaired_limit.png
|-- notebooks/
|   `-- lesson_38_paired_t_test.ipynb
`-- slides/
    |-- lesson_38.tex
    `-- lesson_38.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L38_Paired_T_Test/src/paired_t_01_differences.py
uv run en/L38_Paired_T_Test/src/paired_t_02_paired_test.py
uv run en/L38_Paired_T_Test/src/paired_t_03_unpaired_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L38_Paired_T_Test/notebooks/lesson_38_paired_t_test.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_38.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_38.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Matched-pair hypothesis tests, the reduction to a one-sample $t$ on the
differences, and the contrast with independent samples follow Alexander
Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business Statistics
2e*, Chapter 10, Section
[10.6](https://openstax.org/books/introductory-business-statistics-2e/pages/10-6-matched-or-paired-samples).
Companion paired-sample practice is in *Introductory Statistics 2e*, Section
[10.4](https://openstax.org/books/introductory-statistics-2e/pages/10-4-matched-or-paired-samples).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

