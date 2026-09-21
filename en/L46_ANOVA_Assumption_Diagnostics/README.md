# Lesson 46 - ANOVA Assumptions: Normality, Homoscedasticity, Independence

This 50-minute micro-lesson uses the synthetic packing experiment to inspect
ANOVA residuals, run Levene's test, and then break equal-variance with a
second equal-$n$ example. The final step shows that balanced sample sizes do
not rescue strong variance inequality.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 12.2 and 12.4 (ANOVA assumptions and facts about the $F$
  distribution).
- **Prerequisites:** The ANOVA table from Lesson 44 and Tukey HSD from
  Lesson 45.
- **Data notice:** Every station, packing method, and cycle time is synthetic.
  The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Form ANOVA residuals $e_{ij}=y_{ij}-\bar y_i$ and inspect their histogram.
2. Use Levene's test and a residual-versus-fitted plot to check equal spread.
3. State that independence is a design assumption, not a plot statistic.
4. Explain why equal $n$ does not make ANOVA immune to strong heteroscedasticity.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: three ANOVA assumptions | Name normality, equal variance, independence. |
| 06-16 | Residuals $e_{ij}=y_{ij}-\bar y_i$ | Confirm residual mean $0$. |
| 16-24 | Run Step 1 | Read Shapiro $W=0.977891$, $p=0.673807$. |
| 24-34 | Levene and residual versus fitted | Compare the three sample SDs. |
| 34-42 | Run Step 2 | Obtain Levene $p=0.636619$. |
| 42-48 | Run Step 3 and the equal-$n$ limit | Contrast Levene $p=2.455155\times10^{-4}$ with $F=9.678598$. |
| 48-50 | Concept check and handoff to Lesson 47 | Move from group means to a fitted line. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Steps 1--2 rebuild the Lesson 44 packing
sample with `SEED = 42`. Step 3 rebuilds a second equal-$n$ sample whose
Automated group is far noisier. These values came from two matching executions
in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `anova_diagnostics_01_residual_normality.py` | Residual histogram and Shapiro-Wilk | Residual mean $0.000000$, SD $2.630914$; $W=0.977891$, $p=0.673807$. |
| 2 | `anova_diagnostics_02_levene_homoscedasticity.py` | Levene and residual versus fitted | SDs $3.067311$, $2.353358$, $2.660249$; Levene $0.457821$, $p=0.636619$. |
| 3 | `anova_diagnostics_03_variance_inequality_limit.py` | Equal $n$, unequal variances | SDs $1.533655$, $1.323764$, $9.975934$; Levene $p=2.455155\times10^{-4}$; $F=9.678598$, $p=4.924585\times10^{-4}$. |

The Step 3 result is the limit. All three groups still have $n=12$, but
Automated is several times noisier. A significant $F$ is no longer a clean
mean comparison.

## Synthetic Diagnostics

Balanced packing experiment (Steps 1--2):

- Residuals are $y$ minus the method mean, so they sum to 0 inside each group.
- Shapiro-Wilk does not reject normality ($p=0.673807$).
- Levene does not reject equal variances ($p=0.636619$).
- Independence is inherited from the randomized assignment of stations, not
  from a residual plot.

Heteroscedastic equal-$n$ example (Step 3):

- Means $49.773530$, $50.186315$, $59.115014$.
- Automated SD $9.975934$ versus $1.533655$ and $1.323764$.
- Levene rejects; ANOVA $F$ still rejects. Equal $n$ did not repair the
  assumption.

## Common Misconceptions

- A residual histogram cannot prove independence.
- Equal sample sizes do not imply equal variances.
- A significant $F$ under broken homoscedasticity is not a trustworthy
  ranking of means.
- The synthetic packing line illustrates diagnostics. It is not a claim about
  any real warehouse.

## Package Structure

```text
L46_ANOVA_Assumption_Diagnostics/
|-- README.md
|-- src/
|   |-- anova_diagnostics_01_residual_normality.py
|   |-- anova_diagnostics_02_levene_homoscedasticity.py
|   `-- anova_diagnostics_03_variance_inequality_limit.py
|-- figures/
|   |-- anova_diagnostics_01_residual_normality.png
|   |-- anova_diagnostics_02_levene_homoscedasticity.png
|   `-- anova_diagnostics_03_variance_inequality_limit.png
|-- notebooks/
|   `-- lesson_46_anova_assumption_diagnostics.ipynb
`-- slides/
    |-- lesson_46.tex
    `-- lesson_46.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_01_residual_normality.py
uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_02_levene_homoscedasticity.py
uv run en/L46_ANOVA_Assumption_Diagnostics/src/anova_diagnostics_03_variance_inequality_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L46_ANOVA_Assumption_Diagnostics/notebooks/lesson_46_anova_assumption_diagnostics.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_46.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_46.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

ANOVA assumptions (normal populations, independent samples, and equal standard
deviations) follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Sections
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
and
[12.4](https://openstax.org/books/introductory-business-statistics-2e/pages/12-4-facts-about-the-f-distribution).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

