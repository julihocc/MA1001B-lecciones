# Lesson 44 - One-Way ANOVA: SS, MS, F

This 50-minute micro-lesson uses one fully synthetic packing experiment with
three methods and $n=12$ stations each. Students build the ANOVA table by
hand, match `scipy.stats.f_oneway`, and then see that a significant $F$ does
not name which pair differs.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 12.2 and 12.3 (one-way ANOVA, the $F$ distribution, and the $F$
  ratio).
- **Prerequisites:** Experimental factors and random assignment from Lesson 43,
  plus the two-sample $t$ idea from Lesson 37.
- **Data notice:** Every station, packing method, and cycle time is synthetic.
  The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Read $n$, $\bar y_i$, and $s_i$ for three independent samples.
2. Decompose $SST=SSB+SSE$ and form $MSB$, $MSE$, and $F=MSB/MSE$.
3. Compare the observed $F$ with an $F(2,33)$ critical value and a $p$-value.
4. Explain why a rejected equal-means hypothesis still does not identify a pair.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: three methods, 12 stations each | Sketch the three samples. |
| 06-16 | Group means and standard deviations | Confirm $n=12$ in each method. |
| 16-24 | Run Step 1 | Read means $49.547060$, $48.331227$, $43.830670$. |
| 24-34 | SST, SSB, SSE on the board | Check $SSB+SSE=SST$. |
| 34-42 | Run Step 2 | Obtain $F=14.823283$ from $MSB/MSE$. |
| 42-48 | Run Step 3 and the pair-limit | Contrast $p=2.550793\times10^{-5}$ with the unlabeled gaps. |
| 48-50 | Concept check and handoff to Lesson 45 | Name Tukey as the pairwise follow-up. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
cycle times with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `one_way_anova_01_group_summaries.py` | Three-group $n$, means, and $s$ | Grand mean $47.236319$; means $49.547060$, $48.331227$, $43.830670$; $s=3.067311$, $2.353358$, $2.660249$. |
| 2 | `one_way_anova_02_ss_ms_table.py` | $SST$, $SSB$, $SSE$, $MS$, manual $F$ | $SST=459.901248$, $SSB=217.641499$, $SSE=242.259749$, $MSB=108.820749$, $MSE=7.341205$, $F=14.823283$; $df=2,33,35$. |
| 3 | `one_way_anova_03_f_test_limit.py` | `f_oneway` $p$-value; $F$ does not name a pair | scipy $F=14.823283$, $p=2.550793\times10^{-5}$, $F_{0.05}(2,33)=3.284918$; gaps $1.215833$, $5.716390$, $4.500557$. |

The Step 3 result is a limit, not a pairwise procedure. The omnibus $F$ rejects
equal means, but Standard versus Guided is a much smaller gap than either
comparison with Automated. Lesson 45 answers the pairwise question with Tukey
HSD.

## Synthetic ANOVA Table

\[
H_0:\ \mu_{\text{Standard}}=\mu_{\text{Guided}}=\mu_{\text{Automated}},
\qquad
H_1:\ \text{at least one mean differs.}
\]

| Source | SS | df | MS | F |
|---|---:|---:|---:|---:|
| Between (factor) | 217.641499 | 2 | 108.820749 | 14.823283 |
| Error (within) | 242.259749 | 33 | 7.341205 |  |
| Total | 459.901248 | 35 |  |  |

The reconstruction identity is $SSB+SSE=SST=459.901248$. The observed $F$
exceeds $3.284918$, so $H_0$ is rejected at $\alpha=0.05$.

## Common Misconceptions

- A large $F$ is evidence against equal means, not a ranking of the three
  methods.
- $MSB$ is not a variance of the original observations; it is $SSB/(k-1)$.
- Matching `f_oneway` is a check of the table, not a second experiment.
- The synthetic packing line illustrates ANOVA arithmetic. It is not a claim
  about any real warehouse.

## Package Structure

```text
L44_One_Way_ANOVA/
|-- README.md
|-- src/
|   |-- one_way_anova_01_group_summaries.py
|   |-- one_way_anova_02_ss_ms_table.py
|   `-- one_way_anova_03_f_test_limit.py
|-- figures/
|   |-- one_way_anova_01_group_summaries.png
|   |-- one_way_anova_02_ss_ms_table.png
|   `-- one_way_anova_03_f_test_limit.png
|-- notebooks/
|   `-- lesson_44_one_way_anova.ipynb
`-- slides/
    |-- lesson_44.tex
    `-- lesson_44.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L44_One_Way_ANOVA/src/one_way_anova_01_group_summaries.py
uv run en/L44_One_Way_ANOVA/src/one_way_anova_02_ss_ms_table.py
uv run en/L44_One_Way_ANOVA/src/one_way_anova_03_f_test_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L44_One_Way_ANOVA/notebooks/lesson_44_one_way_anova.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_44.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_44.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

One-way ANOVA, the $F$ ratio, and the between/within decomposition follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Sections
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
and
[12.3](https://openstax.org/books/introductory-business-statistics-2e/pages/12-3-the-f-distribution-and-the-f-ratio).
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

