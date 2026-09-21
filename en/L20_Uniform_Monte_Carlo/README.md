# Lesson 20 - Continuous Uniform Distribution and Monte Carlo

This 50-minute micro-lesson uses one fully synthetic ticket-processing clock
modeled as $\mathrm{Uniform}(8,20)$ minutes. The exact tail $P(X>16)$ equals
length over $12$. A seed-42 Monte Carlo of $100{,}000$ draws recovers that
tail. The final step shows that a flat model fails when density piles at
one end.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 5, Section 5.2 (the uniform distribution). Companion practice:
  *Introductory Statistics 2e*, Section 5.2.
- **Prerequisites:** Continuous density and interval probability from Lesson
  19.
- **Data notice:** Every processing time, density, and Monte Carlo draw is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Write the flat density $f(x)=1/(b-a)$ on a closed interval.
2. Compute $P(X>c)$ as remaining length divided by $b-a$.
3. Check an exact uniform probability with a seeded Monte Carlo sample.
4. Explain why a piled density makes the uniform tail the wrong number.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: a flat clock on $[8,20]$ | Sketch a rectangle of height $1/12$. |
| 06-16 | Length ratio as probability | Compute $(20-16)/12=1/3$. |
| 16-24 | Run Step 1 | Read height $0.083333$ and $P(X>16)=0.333333$. |
| 24-34 | Monte Carlo idea: simulate, then count | Predict a tail near $1/3$. |
| 34-42 | Run Step 2 | Obtain Monte Carlo tail $0.333290$. |
| 42-48 | Run Step 3 and pile the density | Contrast $0.333333$ with $0.555556$. |
| 48-50 | Concept check and handoff to Lesson 21 | Name $z$ as a standardized clock. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
$\mathrm{Uniform}(8,20)$ model with `SEED = 42` and adds the next concept
without importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `uniform_mc_01_exact_uniform.py` | Flat density, length ratio, exact tail | Height $1/12=0.083333$, mean $=14.000000$, $P(X>16)=0.333333$. |
| 2 | `uniform_mc_02_monte_carlo.py` | Seed-42 Monte Carlo of $100{,}000$ draws | Simulated tail $0.333290$, absolute error $0.000043$, simulated mean $14.007499$. |
| 3 | `uniform_mc_03_piled_density_limit.py` | Right-triangular pile on the same support | Piled $P(X>16)=0.555556$, piled mean $=16.000000$, piled height at $20$ is $0.166667$. |

The Step 3 result is a limit. Uniform is the right model only when the
density is actually flat. Lesson 21 standardizes a bell-shaped clock with
$z=(x-\mu)/\sigma$.

## Synthetic Processing-Time Model

Support: $X\sim\mathrm{Uniform}(8,20)$ minutes. Density height:

\[
f(x)=\frac{1}{20-8}=\frac{1}{12}=0.083333,\qquad 8\le x\le 20.
\]

Mean $(a+b)/2=14$. Tail by length:

\[
P(X>16)=\frac{20-16}{12}=\frac{1}{3}=0.333333.
\]

A seed-42 sample of $100{,}000$ draws estimates that tail as $0.333290$.
If the true clock is right-triangular and piles at $20$ minutes, the same
cut has probability $0.555556$, not $1/3$.

## Student Study Notebook

The executed notebook
[`notebooks/lesson_20_uniform_monte_carlo.ipynb`](notebooks/lesson_20_uniform_monte_carlo.ipynb)
is a self-contained, Google Colab-compatible study guide. It builds the flat
uniform model in memory, reproduces the seed-42 Monte Carlo sample, and then
compares the rectangle with a right-triangular density on the same support. It
includes three embedded figures, editable practices with collapsible answers,
and executable assertions for the verified package values, a 1,000-draw
practice, and left-side probability comparisons.

The notebook was executed both in place and as the only lesson artifact in an
empty temporary directory. Its saved HTML and Markdown renders and all three
figures were inspected after execution.

## Common Misconceptions

- A uniform density is flat. It is not “any shape on a bounded interval.”
- $P(X>16)$ is remaining length over $b-a$, not a density height.
- Monte Carlo recovers the exact tail; it does not replace the formula.
- A close simulation error such as $0.000043$ is expected with $100{,}000$
  draws. It is not evidence that the exact value is wrong.
- If tickets cluster near one endpoint, the uniform tail is the wrong number.
- The synthetic clock illustrates uniform arithmetic. It is not a claim
  about any real ticket desk.

## Package Structure

```text
L20_Uniform_Monte_Carlo/
|-- README.md
|-- src/
|   |-- uniform_mc_01_exact_uniform.py
|   |-- uniform_mc_02_monte_carlo.py
|   `-- uniform_mc_03_piled_density_limit.py
|-- figures/
|   |-- uniform_mc_01_exact_uniform.png
|   |-- uniform_mc_02_monte_carlo.png
|   `-- uniform_mc_03_piled_density_limit.png
|-- notebooks/
|   `-- lesson_20_uniform_monte_carlo.ipynb
`-- slides/
    |-- lesson_20.tex
    `-- lesson_20.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L20_Uniform_Monte_Carlo/src/uniform_mc_01_exact_uniform.py
uv run en/L20_Uniform_Monte_Carlo/src/uniform_mc_02_monte_carlo.py
uv run en/L20_Uniform_Monte_Carlo/src/uniform_mc_03_piled_density_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L20_Uniform_Monte_Carlo/notebooks/lesson_20_uniform_monte_carlo.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_20.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_20.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The continuous uniform density, length-ratio probability, and mean
$(a+b)/2$ follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 5, Section
[5.2](https://openstax.org/books/introductory-business-statistics-2e/pages/5-2-the-uniform-distribution).
Companion uniform practice is in *Introductory Statistics 2e*, Section
[5.2](https://openstax.org/books/introductory-statistics-2e/pages/5-2-the-uniform-distribution).
The piled-density limit prepares the need for other continuous families,
including the normal model in Lesson 21. OpenStax publishes these texts
under the Creative Commons Attribution-NonCommercial-ShareAlike license.
The synthetic dataset, code, and figures in this package are original
course materials.

