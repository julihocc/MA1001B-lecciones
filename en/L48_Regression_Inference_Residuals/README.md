# Lesson 48 - Regression Inference, Residual Diagnostics, and Decisions

This 50-minute micro-lesson uses one fully synthetic mail-center sample: 39
ordinary overtime weeks plus one emergency weekend at $(48,\ 42)$. Students
test $H_0:\beta_1=0$, read a residual plot, and then see that the significant
slope vanishes when the influential point is removed.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 13.2 and 13.6 (significance of the linear association and
  prediction from a regression equation).
- **Prerequisites:** Least squares and $R^2$ from Lesson 47.
- **Data notice:** Every week, overtime hour, and unit count is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $SE(b_1)$, the $t$ statistic, and a two-sided $p$-value for
   $H_0:\beta_1=0$.
2. Draw residual versus fitted values and locate an unusual week.
3. Refit the line after deleting the influential point.
4. Explain why one point can create a significant slope that is not a decision
   about ordinary operations.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: 39 ordinary weeks plus one emergency weekend | Mark $(48,\ 42)$ on a sketch. |
| 06-16 | $SE(b_1)$ and $t=b_1/SE(b_1)$ | State $H_0:\beta_1=0$. |
| 16-24 | Run Step 1 | Read $t=5.991932$, $p=5.839701\times10^{-7}$. |
| 24-34 | Residual versus fitted | Find the largest residual. |
| 34-42 | Run Step 2 | Obtain emergency residual $8.570594$. |
| 42-48 | Run Step 3 and the influence limit | Contrast $p=0.291492$ after deletion. |
| 48-50 | Concept check | Refuse to treat the $n=40$ slope as ordinary-week policy. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
40-week sample with `SEED = 42` and adds the next concept without importing
another lesson script. These values came from two matching executions in the
locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `regression_inference_01_slope_se_t.py` | $SE(b_1)$ and $t$ test of $H_0:\beta_1=0$ | $n=40$; $b_1=0.434381$; $SE=0.072494$; $t=5.991932$; $p=5.839701\times10^{-7}$; reject $H_0$. |
| 2 | `regression_inference_02_residual_plot.py` | Residual versus fitted | Residual mean $0.000000$; SD $3.140288$; emergency residual $8.570594$ (largest). |
| 3 | `regression_inference_03_influential_point.py` | Slope vanishes without the point | Without the weekend: $n=39$, $b_1=0.088445$, $t=1.070131$, $p=0.291492$, $R^2=0.030022$; do not reject $H_0$. |

The Step 3 result is the limit. The emergency weekend is not a typical overtime
week. A significant $n=40$ slope is not a decision about ordinary operations.

## Synthetic Inference Table

All 40 weeks:

\[
t=\frac{0.434381}{0.072494}=5.991932,\qquad df=38,\qquad p=5.839701\times10^{-7}.
\]

After deleting the emergency weekend:

\[
t=\frac{0.088445}{0.082649}=1.070131,\qquad p=0.291492.
\]

$R^2$ falls from $0.485814$ to $0.030022$. The association was the point.

## Common Misconceptions

- A small $p$-value is not robust to one high-leverage week.
- Residual mean 0 is a least-squares identity, not a diagnostic pass.
- Deleting a point is a sensitivity check, not a license to drop inconvenient
  data in operations.
- The synthetic mail center illustrates influence. It is not a claim about any
  real warehouse.

## Package Structure

```text
L48_Regression_Inference_Residuals/
|-- README.md
|-- src/
|   |-- regression_inference_01_slope_se_t.py
|   |-- regression_inference_02_residual_plot.py
|   `-- regression_inference_03_influential_point.py
|-- figures/
|   |-- regression_inference_01_slope_se_t.png
|   |-- regression_inference_02_residual_plot.png
|   `-- regression_inference_03_influential_point.png
|-- notebooks/
|   `-- lesson_48_regression_inference_residuals.ipynb
`-- slides/
    |-- lesson_48.tex
    `-- lesson_48.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L48_Regression_Inference_Residuals/src/regression_inference_01_slope_se_t.py
uv run en/L48_Regression_Inference_Residuals/src/regression_inference_02_residual_plot.py
uv run en/L48_Regression_Inference_Residuals/src/regression_inference_03_influential_point.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L48_Regression_Inference_Residuals/notebooks/lesson_48_regression_inference_residuals.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_48.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_48.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Testing the significance of a linear association, residual thinking, and
prediction from a fitted line follow Alexander Holmes, Barbara Illowsky, and
Susan Dean, *Introductory Business Statistics 2e*, Sections
[13.2](https://openstax.org/books/introductory-business-statistics-2e/pages/13-2-testing-the-significance-of-the-correlation-coefficient)
and
[13.6](https://openstax.org/books/introductory-business-statistics-2e/pages/13-6-predicting-with-a-regression-equation).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

