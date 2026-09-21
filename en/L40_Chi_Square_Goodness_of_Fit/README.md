# Lesson 40 - Chi-Square Goodness of Fit

This 50-minute micro-lesson uses one fully synthetic support-ticket mix to
test hypothesized shares $0.40$, $0.30$, $0.20$, and $0.10$. Expected counts
are $np$, the statistic is $\chi^2=\sum(O-E)^2/E$, and $df=3$. The final
step shows that an expected count below 5 makes the chi-square approximation
a poor decision tool.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 11, Section 11.3 (goodness-of-fit test).
- **Prerequisites:** One- and two-proportion $z$ tests from Lessons 36 and
  39.
- **Data notice:** Every ticket count is synthetic. The scripts contain no
  real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Convert hypothesized category shares into expected counts $E=np$.
2. Compute $\chi^2=\sum(O-E)^2/E$ with $df=k-1$.
3. Read a right-tailed p-value and decide at $\alpha=0.05$.
4. Explain why an expected count below 5 weakens the approximation.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: a claimed four-channel mix | Write $H_0:$ shares $=(0.40,0.30,0.20,0.10)$. |
| 06-16 | Observed versus $E=np$ | Confirm expected $80$, $60$, $40$, $20$. |
| 16-24 | Run Step 1 | Read minimum $E=20$ and the $E\ge 5$ check. |
| 24-34 | Cell contributions and $df=3$ | Compute $(100-80)^2/80=5$. |
| 34-42 | Run Step 2 | Obtain $\chi^2=9.166667$, $p=0.027155$, reject $H_0$. |
| 42-48 | Run Step 3 | See $E=4$ and $E=2$; one ticket moves a cell term from $2.000$ to $0.500$. |
| 48-50 | Concept check and handoff to Lesson 41 | Name the next tool: chi-square test of independence. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
synthetic ticket mix without importing another lesson script. These values
came from two matching executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `goodness_of_fit_01_observed_expected.py` | Observed versus $E=np$ | $n=200$; observed $100,50,30,20$; expected $80,60,40,20$; all $E\ge 5$. |
| 2 | `goodness_of_fit_02_chi_square.py` | $\chi^2$, $df=3$, right-tailed $p$ | Contributions $5.000000$, $1.666667$, $2.500000$, $0.000000$; $\chi^2=9.166667$; $p=0.027155$; $\chi^{2*}=7.814728$; reject $H_0$. |
| 3 | `goodness_of_fit_03_small_expected_limit.py` | $E<5$ limit | $n=20$; observed $14,4,2,0$; expected $8,6,4,2$; two cells with $E<5$. App contribution $2.000000$ if $O=0$ versus $0.500000$ if $O=1$. |

The Step 3 result is a limit, not a second GOF claim. The $n=20$ table has
expected counts $4$ and $2$, so the chi-square p-value is not a stable
decision input. Lesson 41 uses a two-way table instead of a hypothesized mix.

## Synthetic Ticket Mix

\[
\chi^2=\frac{(100-80)^2}{80}+\frac{(50-60)^2}{60}+\frac{(30-40)^2}{40}+\frac{(20-20)^2}{20}
=9.166667,
\]

with $df=4-1=3$ and $p=0.027155$. The $n=200$ table meets $E\ge 5$. The
$n=20$ follow-up does not: Email has $E=4$ and App has $E=2$, with an
observed App count of $0$.

## Common Misconceptions

- Expected counts are $np$ under $H_0$, not the observed sample shares.
- Goodness of fit is right-tailed: large $\chi^2$ is evidence against $H_0$.
- $df=k-1$ for $k$ categories with probabilities fully specified.
- One cell with $E<5$ is already a warning, even if software still prints $p$.
- The synthetic tickets illustrate GOF. They are not a claim about any real
  support desk.

## Package Structure

```text
L40_Chi_Square_Goodness_of_Fit/
|-- README.md
|-- src/
|   |-- goodness_of_fit_01_observed_expected.py
|   |-- goodness_of_fit_02_chi_square.py
|   `-- goodness_of_fit_03_small_expected_limit.py
|-- figures/
|   |-- goodness_of_fit_01_observed_expected.png
|   |-- goodness_of_fit_02_chi_square.png
|   `-- goodness_of_fit_03_small_expected_limit.png
|-- notebooks/
|   `-- lesson_40_chi_square_goodness_of_fit.ipynb
`-- slides/
    |-- lesson_40.tex
    `-- lesson_40.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L40_Chi_Square_Goodness_of_Fit/src/goodness_of_fit_01_observed_expected.py
uv run en/L40_Chi_Square_Goodness_of_Fit/src/goodness_of_fit_02_chi_square.py
uv run en/L40_Chi_Square_Goodness_of_Fit/src/goodness_of_fit_03_small_expected_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L40_Chi_Square_Goodness_of_Fit/notebooks/lesson_40_chi_square_goodness_of_fit.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_40.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_40.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The chi-square goodness-of-fit statistic, $df=k-1$, the expected-count
guideline, and the right-tailed decision follow Alexander Holmes, Barbara
Illowsky, and Susan Dean, *Introductory Business Statistics 2e*, Chapter 11,
Section
[11.3](https://openstax.org/books/introductory-business-statistics-2e/pages/11-3-goodness-of-fit-test).
Companion GOF practice is in *Introductory Statistics 2e*, Section
[11.2](https://openstax.org/books/introductory-statistics-2e/pages/11-2-goodness-of-fit-test).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

