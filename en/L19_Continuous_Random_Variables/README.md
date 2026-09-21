# Lesson 19 - Continuous Random Variables: Density and Interval Probability

This 50-minute micro-lesson uses one fully synthetic help-desk service-time
clock to introduce a continuous density on $[2, 14]$ minutes. Probability is
area under the curve, not a point height. The final step shows that
$P(X=c)=0$ for every single minute $c$, including the mode.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 5, Section 5.1 (continuous probability functions). Companion
  practice: *Introductory Statistics 2e*, Section 5.1.
- **Prerequisites:** Discrete random variables, PMF, and $E[X]$ from Lessons
  13 through 18.
- **Data notice:** Every service time, density, and interval probability is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Distinguish a continuous density $f(x)$ from a discrete PMF.
2. Read $P(a<X<b)$ as the area between $a$ and $b$ under $f$.
3. Use the CDF difference $F(b)-F(a)$ to compute an interval probability.
4. Explain why $P(X=c)=0$ for a continuous random variable.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: minutes on a clock, not defect counts | Name the support $[2, 14]$. |
| 06-16 | Density versus PMF | Confirm that $f(6)$ is a height, not a probability. |
| 16-24 | Run Step 1 | Read $f(6)=0.166667$ and total area $1.000000$. |
| 24-34 | Interval probability as area | Compute $F(10)-F(4)$. |
| 34-42 | Run Step 2 | Obtain $P(4<X<10)=0.750000$. |
| 42-48 | Run Step 3 and shrink the window | Contrast $0.158854$ with $0.003330$ and $P(X=6)=0$. |
| 48-50 | Concept check and handoff to Lesson 20 | Name the uniform model as a flat density. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same triangular
service-time model with `SEED = 42` and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `continuous_rv_01_density.py` | Triangular density on $[2, 14]$ | $f(2)=0.000000$, $f(6)=0.166667$, $f(14)=0.000000$, mean $=7.333333$, total area $=1.000000$. |
| 2 | `continuous_rv_02_interval_probability.py` | Interval probability as area | $F(4)=0.083333$, $F(10)=0.833333$, $P(4<X<10)=P(4\le X\le 10)=0.750000$. |
| 3 | `continuous_rv_03_point_mass_limit.py` | $P(X=c)=0$ from a continuous CDF | $P(\|X-6\|<0.50)=0.158854$, $P(\|X-6\|<0.10)=0.033021$, $P(\|X-6\|<0.01)=0.003330$, $F(6)=0.333333$, jump $=0.000000$, $P(X=6)=0.000000$. |

The Step 3 result is a limit, not a named family yet. A continuous clock can
assign probability to intervals, not to a single minute. Lesson 20 uses a
flat uniform density and a Monte Carlo check of $P(X>16)$.

## Synthetic Service-Time Model

Support: $X\in[2,14]$ minutes. Shape: triangular with mode $6$. Mean:

\[
E[X]=\frac{a+b+\text{mode}}{3}=\frac{2+14+6}{3}=7.333333.
\]

Peak density $f(6)=2/(14-2)=1/6=0.166667$. That height is not $P(X=6)$.
The 6-minute window from 4 to 10 has probability

\[
P(4<X<10)=F(10)-F(4)=0.833333-0.083333=0.750000.
\]

The same number is obtained with closed endpoints. Shrinking a window about
the mode drives the probability to 0, which is $P(X=6)$.

## Student Study Notebook

The executed notebook
[`notebooks/lesson_19_continuous_random_variables.ipynb`](notebooks/lesson_19_continuous_random_variables.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds the
triangular density in memory, calculates interval area with CDF differences,
and connects shrinking windows and the absence of a CDF jump to zero point
mass. It includes three embedded figures, editable practices with collapsible
answers, and executable assertions for all verified package values plus
$f(8)=0.125000$ and $P(6<X<12)=0.625000$.

The notebook was executed both in place and as the only lesson artifact in an
empty temporary directory. Its saved HTML and Markdown renders and all three
figures were inspected after execution.

## Common Misconceptions

- $f(x)$ is a density height. It is not $P(X=x)$.
- Continuous probability lives on intervals, not on isolated points.
- $P(a<X<b)$ and $P(a\le X\le b)$ match because each endpoint has mass 0.
- The mode is the most likely *region*, not a point with positive mass.
- A CDF with no jump at $c$ is the geometric statement of $P(X=c)=0$.
- The synthetic clock illustrates continuous arithmetic. It is not a claim
  about any real help desk.

## Package Structure

```text
L19_Continuous_Random_Variables/
|-- README.md
|-- src/
|   |-- continuous_rv_01_density.py
|   |-- continuous_rv_02_interval_probability.py
|   `-- continuous_rv_03_point_mass_limit.py
|-- figures/
|   |-- continuous_rv_01_density.png
|   |-- continuous_rv_02_interval_probability.png
|   `-- continuous_rv_03_point_mass_limit.png
|-- notebooks/
|   `-- lesson_19_continuous_random_variables.ipynb
`-- slides/
    |-- lesson_19.tex
    `-- lesson_19.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L19_Continuous_Random_Variables/src/continuous_rv_01_density.py
uv run en/L19_Continuous_Random_Variables/src/continuous_rv_02_interval_probability.py
uv run en/L19_Continuous_Random_Variables/src/continuous_rv_03_point_mass_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L19_Continuous_Random_Variables/notebooks/lesson_19_continuous_random_variables.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_19.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_19.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Continuous densities, interval probability as area, and $P(X=c)=0$ follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Chapter 5, Section
[5.1](https://openstax.org/books/introductory-business-statistics-2e/pages/5-1-continuous-probability-functions).
Companion continuous-function practice is in *Introductory Statistics 2e*,
Section
[5.1](https://openstax.org/books/introductory-statistics-2e/pages/5-1-continuous-probability-functions).
The uniform-density limit is prepared for Lesson 20. OpenStax publishes these
texts under the Creative Commons Attribution-NonCommercial-ShareAlike license.
The synthetic dataset, code, and figures in this package are original course
materials.

