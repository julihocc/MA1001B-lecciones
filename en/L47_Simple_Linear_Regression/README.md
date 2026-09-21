# Lesson 47 - Simple Linear Regression: Least Squares and R-squared

This 50-minute micro-lesson uses one fully synthetic 40-week mail-center
sample. Students scatter coaching hours against units packed per labor hour,
fit the least-squares line $y=12+0.45x$ plus noise, and then see that a high
$R^2$ is not a causal lever.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 13.3 and 13.4 (linear equations and the regression equation).
- **Prerequisites:** Scatterplots and correlation from earlier numerical
  summaries, plus the observational-versus-randomized contrast from Lesson 43.
- **Data notice:** Every week, coaching hour, and productivity value is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Read a scatter of one numerical predictor and one numerical response.
2. Compute the least-squares slope and intercept from $S_{xx}$ and $S_{xy}$.
3. Decompose $SST=SSR+SSE$ and form $R^2=1-SSE/SST$.
4. Explain why a high $R^2$ does not license a causal coaching policy.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: 40 weeks, $x$ coaching hours, $y$ units per hour | Sketch the scatter. |
| 06-16 | Cloud of points, no line yet | Read $n=40$ and $r=0.910813$. |
| 16-24 | Run Step 1 | Confirm the $x$ range $9.402$ to $39.220$. |
| 24-34 | Normal equations on the board | Compare manual slope with scipy. |
| 34-42 | Run Step 2 | Obtain $b_1=0.405936$, $b_0=13.136554$. |
| 42-48 | Run Step 3 and the $R^2$ limit | Read $R^2=0.829580$; refuse the causal lever. |
| 48-50 | Concept check and handoff to Lesson 48 | Ask for $SE(b_1)$ and residual plots. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
40-week sample with `SEED = 42` and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `simple_regression_01_scatter.py` | Scatter of $x$ and $y$ | $n=40$; $\bar x=25.075277$; $\bar y=23.315500$; $r=0.910813$. |
| 2 | `simple_regression_02_least_squares.py` | Least-squares slope and intercept | $b_1=0.405936$, $b_0=13.136554$; true slope $0.45$; $SSE=113.102672$. |
| 3 | `simple_regression_03_r_squared_limit.py` | $R^2$ is not a causal lever | $SST=663.669939$, $SSR=550.567267$, $R^2=0.829580$; fitted +10h gain $4.059355$. |

The Step 3 result is a limit. $R^2=0.829580$ says the line tracks these 40
observed weeks. Coaching hours were not randomly assigned, so the slope is not
a policy button. Lesson 48 adds $SE(b_1)$, a $t$ test, residual plots, and an
influential point.

## Synthetic Least-Squares Fit

True line: $y=12+0.45x+\varepsilon$. Fitted line:

\[
\hat y=13.136554+0.405936\,x.
\]

Variation identity:

\[
SST=SSR+SSE=550.567267+113.102672=663.669939,
\]

\[
R^2=1-\frac{SSE}{SST}=0.829580.
\]

A 10-hour increase in coaching has fitted gain $4.059355$ units per hour on
this scatter. That arithmetic is not a randomized treatment effect.

## Common Misconceptions

- The least-squares line is the unique minimizer of squared vertical gaps, not
  a proof of cause.
- $R^2$ close to 1 can still come from a confounded observational sample.
- Matching scipy `linregress` is a check of the normal equations, not a second
  data set.
- The synthetic mail center illustrates regression arithmetic. It is not a
  claim about any real warehouse.

## Package Structure

```text
L47_Simple_Linear_Regression/
|-- README.md
|-- src/
|   |-- simple_regression_01_scatter.py
|   |-- simple_regression_02_least_squares.py
|   `-- simple_regression_03_r_squared_limit.py
|-- figures/
|   |-- simple_regression_01_scatter.png
|   |-- simple_regression_02_least_squares.png
|   `-- simple_regression_03_r_squared_limit.png
|-- notebooks/
|   `-- lesson_47_simple_linear_regression.ipynb
`-- slides/
    |-- lesson_47.tex
    `-- lesson_47.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L47_Simple_Linear_Regression/src/simple_regression_01_scatter.py
uv run en/L47_Simple_Linear_Regression/src/simple_regression_02_least_squares.py
uv run en/L47_Simple_Linear_Regression/src/simple_regression_03_r_squared_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L47_Simple_Linear_Regression/notebooks/lesson_47_simple_linear_regression.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_47.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_47.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Linear equations, the least-squares regression line, and $R^2$ follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Sections
[13.3](https://openstax.org/books/introductory-business-statistics-2e/pages/13-3-linear-equations)
and
[13.4](https://openstax.org/books/introductory-business-statistics-2e/pages/13-4-the-regression-equation).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

