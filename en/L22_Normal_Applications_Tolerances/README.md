# Lesson 22 - Normal Applications: Tolerances and Operating Intervals

This 50-minute micro-lesson uses one fully synthetic filling process modeled
as $\mathrm{Normal}(\mu=50,\sigma=4)$ grams. The specification interval is
$[44,56]$. Yield is the in-spec probability. A mean shift to $52$ drops
yield. The final step shows that high spec compliance is not the same as a
centered process.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 6, Section 6.2 (using the normal distribution). Companion practice:
  *Introductory Statistics 2e*, Section 6.2.
- **Prerequisites:** $z$-scores and standard normal areas from Lesson 21.
- **Data notice:** Every fill weight, specification limit, and yield is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Convert specification limits into $z$ cuts.
2. Compute process yield as $P(\mathrm{LSL}<X<\mathrm{USL})$.
3. Quantify how a mean shift changes yield.
4. Explain why a high-yield process need not be centered on the target.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: spec $[44,56]$ around target $50$ | Sketch LSL, target, USL. |
| 06-16 | $z$ cuts for a centered process | Compute $z=\pm 1.5$. |
| 16-24 | Run Step 1 | Read yield $0.866386$. |
| 24-34 | Mean shift to $52$ | Recompute $z$ cuts $-2$ and $1$. |
| 34-42 | Run Step 2 | Obtain yield $0.818595$ and drop $0.047791$. |
| 42-48 | Run Step 3: tight off-center process | Contrast yield $0.977218$ with a mean of $52$. |
| 48-50 | Concept check and handoff to Lesson 23 | Name the sampling distribution of $\bar x$. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the synthetic
filling process with `SEED = 42` and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `normal_tolerances_01_spec_yield.py` | Spec $z$ cuts and in-spec yield | $z=\pm 1.500000$, each tail $0.066807$, yield $0.866386$. |
| 2 | `normal_tolerances_02_mean_shift.py` | Mean shift $\mu=52$ | New $z$ cuts $-2.000000$ and $1.000000$, yield $0.818595$, drop $0.047791$. |
| 3 | `normal_tolerances_03_centered_vs_compliant.py` | Tight off-center process | $\mu=52$, $\sigma=2$, $z$ cuts $-4.000000$ and $2.000000$, yield $0.977218$. |

The Step 3 result is a limit. A process can pass the spec at a high rate and
still sit off the target. Lesson 23 moves from one unit to the sampling
distribution of the sample mean.

## Student Study Notebook

The executed [student notebook](notebooks/lesson_22_normal_applications_tolerances.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Filling Process

Centered model: $X\sim N(50,4^2)$. Specification $[44,56]$:

\[
z_{\mathrm{LSL}}=\frac{44-50}{4}=-1.5,\qquad
z_{\mathrm{USL}}=\frac{56-50}{4}=1.5,
\]
\[
P(44<X<56)=0.866386.
\]

After a $+2$ gram shift, $X\sim N(52,4^2)$ and yield falls to $0.818595$.
A tighter off-center clock $N(52,2^2)$ raises yield to $0.977218$ while
remaining $2$ grams above the target.

## Common Misconceptions

- Yield is an interval probability, not a density height at the target.
- The spec does not move when the process mean moves; the $z$ cuts do.
- A smaller $\sigma$ can raise yield even when the mean is off target.
- High spec compliance is not evidence that the process is centered.
- Equal tail probabilities $0.066807$ appear only when the process is
  centered inside a symmetric spec.
- The synthetic fills illustrate tolerance arithmetic. They are not a
  claim about any real filling line.

## Package Structure

```text
L22_Normal_Applications_Tolerances/
|-- README.md
|-- src/
|   |-- normal_tolerances_01_spec_yield.py
|   |-- normal_tolerances_02_mean_shift.py
|   `-- normal_tolerances_03_centered_vs_compliant.py
|-- figures/
|   |-- normal_tolerances_01_spec_yield.png
|   |-- normal_tolerances_02_mean_shift.png
|   `-- normal_tolerances_03_centered_vs_compliant.png
|-- notebooks/
|   `-- lesson_22_normal_applications_tolerances.ipynb
`-- slides/
    |-- lesson_22.tex
    `-- lesson_22.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L22_Normal_Applications_Tolerances/src/normal_tolerances_01_spec_yield.py
uv run en/L22_Normal_Applications_Tolerances/src/normal_tolerances_02_mean_shift.py
uv run en/L22_Normal_Applications_Tolerances/src/normal_tolerances_03_centered_vs_compliant.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L22_Normal_Applications_Tolerances/notebooks/lesson_22_normal_applications_tolerances.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_22.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_22.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Normal probabilities between specification limits, $z$ cuts, and operating
intervals follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 6, Section
[6.2](https://openstax.org/books/introductory-business-statistics-2e/pages/6-2-using-the-normal-distribution).
Companion applications practice is in *Introductory Statistics 2e*, Section
[6.2](https://openstax.org/books/introductory-statistics-2e/pages/6-2-using-the-normal-distribution).
The yield-versus-centering limit prepares sampling distributions of the mean
in Lesson 23. OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

