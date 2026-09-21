# Lesson 42 - Chi-Square Test of Homogeneity

This 50-minute micro-lesson uses three fully synthetic warehouse samples
(North $n=120$, Central $n=100$, South $n=90$) with the same three ticket
categories. Homogeneity tests whether independently sampled sites share one
mix. The final step shows that homogeneity and independence share the
chi-square arithmetic but not the sampling story.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 11, Section 11.5 (test for homogeneity).
- **Prerequisites:** Chi-square independence from Lesson 41.
- **Data notice:** Every ticket count is synthetic. The scripts contain no
  real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Display three independently sampled category mixes with fixed row totals.
2. Compute the homogeneity $\chi^2$ with $df=(r-1)(c-1)$.
3. Decide $H_0$: the sites share one mix at $\alpha=0.05$.
4. Contrast the homogeneity sampling plan with an independence table.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: three planned site samples | Mark the row totals as design, not chance. |
| 06-16 | Within-site shares | Compute North phone share $60/120=0.50$. |
| 16-24 | Run Step 1 | Read shares $0.500000$, $0.350000$, $0.277778$ for phone. |
| 24-34 | Homogeneity expected counts | Write $E=(\text{row total}\times\text{column total})/n$. |
| 34-42 | Run Step 2 | Obtain $\chi^2=17.812605$, $df=4$, $p=0.001343$, reject $H_0$. |
| 42-48 | Run Step 3 | Name the independence story that reuses the same numbers. |
| 48-50 | Concept check and handoff to Lesson 43 | Name experimental design as the next sampling question. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same three
synthetic site samples without importing another lesson script. These values
came from two matching executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `homogeneity_01_three_samples.py` | Three independent mixes | North $60,40,20$; Central $35,40,25$; South $25,30,35$; phone shares $0.500000$, $0.350000$, $0.277778$. |
| 2 | `homogeneity_02_chi_square.py` | Homogeneity $\chi^2$ | $\chi^2=17.812605$, $df=4$, $p=0.001343$, $\chi^{2*}=9.487729$, minimum $E=23.225806$, reject $H_0$. |
| 3 | `homogeneity_03_sampling_story_limit.py` | Same statistic, different $H_0$ | Shared $\chi^2=17.812605$ and $p=0.001343$. Homogeneity fixes site sample sizes; independence classifies one sample two ways. |

The Step 3 result is a limit, not a second computation. The number
$17.812605$ does not say which design produced the table. Lesson 43 turns
from observational site samples to randomized experimental factors.

## Synthetic Three-Site Register

| Site | Phone | Chat | Email | Sample size |
|---|---:|---:|---:|---:|
| North | 60 | 40 | 20 | 120 |
| Central | 35 | 40 | 25 | 100 |
| South | 25 | 30 | 35 | 90 |
| Total | 120 | 110 | 80 | 310 |

\[
\chi^2=17.812605,\qquad df=(3-1)(3-1)=4,\qquad p=0.001343.
\]

The three row totals were chosen by the sampling plan. That is the
homogeneity story. The same cells could have come from one sample of $310$
tickets later classified by site and channel; that would be independence.

## Common Misconceptions

- Homogeneity is not goodness of fit: there is no hypothesized mix in
  advance, only a claim that several populations share one unknown mix.
- Homogeneity is not independence: the row totals are fixed by design.
- The $\chi^2$ formula does not reveal which sampling story was used.
- Rejecting homogeneity says the mixes differ; it does not say which site
  pair differs.
- The synthetic warehouses illustrate homogeneity. They are not a claim
  about any real network of sites.

## Package Structure

```text
L42_Chi_Square_Homogeneity/
|-- README.md
|-- src/
|   |-- homogeneity_01_three_samples.py
|   |-- homogeneity_02_chi_square.py
|   `-- homogeneity_03_sampling_story_limit.py
|-- figures/
|   |-- homogeneity_01_three_samples.png
|   |-- homogeneity_02_chi_square.png
|   `-- homogeneity_03_sampling_story_limit.png
|-- notebooks/
|   `-- lesson_42_chi_square_homogeneity.ipynb
`-- slides/
    |-- lesson_42.tex
    `-- lesson_42.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L42_Chi_Square_Homogeneity/src/homogeneity_01_three_samples.py
uv run en/L42_Chi_Square_Homogeneity/src/homogeneity_02_chi_square.py
uv run en/L42_Chi_Square_Homogeneity/src/homogeneity_03_sampling_story_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L42_Chi_Square_Homogeneity/notebooks/lesson_42_chi_square_homogeneity.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_42.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_42.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The chi-square test of homogeneity, the shared arithmetic with the
independence statistic, and the distinct sampling story of independent
populations follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 11, Section
[11.5](https://openstax.org/books/introductory-business-statistics-2e/pages/11-5-test-for-homogeneity).
Companion homogeneity practice is in *Introductory Statistics 2e*, Section
[11.4](https://openstax.org/books/introductory-statistics-2e/pages/11-4-test-for-homogeneity).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

