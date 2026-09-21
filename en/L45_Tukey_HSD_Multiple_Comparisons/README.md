# Lesson 45 - Tukey HSD Multiple Comparisons

This 50-minute micro-lesson uses the same fully synthetic packing experiment
with three methods and $n=12$ stations each. Students first run unadjusted
pairwise $t$ tests, then Tukey HSD, and finally see that uncorrected pairwise
tests inflate familywise error.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 12.2--12.3, continued as post-hoc pairwise practice after a
  significant one-way $F$.
- **Prerequisites:** The ANOVA table and the unlabeled-pair limit from
  Lesson 44.
- **Data notice:** Every station, packing method, and cycle time is synthetic.
  The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Run all three pairwise $t$ tests after a significant ANOVA $F$.
2. Read Tukey HSD mean differences, adjusted $p$-values, and simultaneous CIs.
3. Identify which packing-method pairs differ at familywise $\alpha=0.05$.
4. Explain why unadjusted pairwise tests inflate familywise error.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: $F$ was significant, three pairs remain | List the three pairs. |
| 06-16 | Unadjusted $t$ tests | Compute three $p$-values. |
| 16-24 | Run Step 1 | Read $p=0.287762$, $0.000071$, $0.000233$. |
| 24-34 | Tukey simultaneous intervals | Check which CIs contain 0. |
| 34-42 | Run Step 2 | Retain Guided vs Standard; reject the other two. |
| 42-48 | Run Step 3 and the FWER limit | Contrast $0.127800$ with Tukey $0.049000$. |
| 48-50 | Concept check and handoff to Lesson 46 | Ask what equal-variance ANOVA still assumes. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
cycle times with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `tukey_hsd_01_pairwise_unadjusted.py` | Three unadjusted pairwise $t$ tests | Standard-Guided $p=0.287762$ (retain); Standard-Automated $p=0.000071$ (reject); Guided-Automated $p=0.000233$ (reject). |
| 2 | `tukey_hsd_02_tukey_hsd.py` | Tukey HSD with `pairwise_tukeyhsd` | Guided vs Standard $p_{\text{adj}}=0.521330$, CI $(-1.498394,3.930061)$ retains; the two Automated pairs reject. |
| 3 | `tukey_hsd_03_familywise_error.py` | Familywise error under the global null | 5000 null experiments: unadjusted FWER $0.127800$; Tukey FWER $0.049000$; advertised $\alpha=0.05$. |

The Step 3 result is the limit. Three unadjusted $\alpha=0.05$ tests do not
keep the probability of any false pair at 5 percent. Lesson 46 checks the
ANOVA assumptions that both $F$ and Tukey still rely on.

## Synthetic Tukey Decisions

Tukey HSD at familywise $\alpha=0.05$:

| Pair | Mean difference | Adjusted $p$ | Simultaneous 95% CI | Reject? |
|---|---:|---:|---|---|
| Automated vs Guided | 4.500557 | 0.000789 | $(1.786329,\ 7.214784)$ | Yes |
| Automated vs Standard | 5.716390 | 0.000033 | $(3.002163,\ 8.430617)$ | Yes |
| Guided vs Standard | 1.215833 | 0.521330 | $(-1.498394,\ 3.930061)$ | No |

Automated is slower than neither competitor once the comparison is a method
contrast: it is faster. Guided and Standard are not distinguished.

## Common Misconceptions

- A significant ANOVA $F$ does not license three ordinary $t$ tests at 0.05.
- Familywise error is the chance of at least one false pair, not the per-test
  alpha.
- A Tukey interval that contains 0 is a retain decision, not proof of equality.
- The synthetic packing line illustrates multiple comparisons. It is not a
  claim about any real warehouse.

## Package Structure

```text
L45_Tukey_HSD_Multiple_Comparisons/
|-- README.md
|-- src/
|   |-- tukey_hsd_01_pairwise_unadjusted.py
|   |-- tukey_hsd_02_tukey_hsd.py
|   `-- tukey_hsd_03_familywise_error.py
|-- figures/
|   |-- tukey_hsd_01_pairwise_unadjusted.png
|   |-- tukey_hsd_02_tukey_hsd.png
|   `-- tukey_hsd_03_familywise_error.png
|-- notebooks/
|   `-- lesson_45_tukey_hsd_multiple_comparisons.ipynb
`-- slides/
    |-- lesson_45.tex
    `-- lesson_45.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_01_pairwise_unadjusted.py
uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_02_tukey_hsd.py
uv run en/L45_Tukey_HSD_Multiple_Comparisons/src/tukey_hsd_03_familywise_error.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L45_Tukey_HSD_Multiple_Comparisons/notebooks/lesson_45_tukey_hsd_multiple_comparisons.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_45.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_45.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

One-way ANOVA and the need for a follow-up after a significant $F$ follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Sections
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
and
[12.3](https://openstax.org/books/introductory-business-statistics-2e/pages/12-3-the-f-distribution-and-the-f-ratio).
Tukey HSD is the post-hoc multiple-comparison practice used with those
sections. OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

