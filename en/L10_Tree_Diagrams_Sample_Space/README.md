# Lesson 10 - Tree Diagrams and Sample-Space Decomposition

This 50-minute micro-lesson uses one fully synthetic incoming-lot register to
draw a two-stage tree, multiply along branches, and add mutually exclusive
paths. The final step shows that a time-ordered tree does not display the
reversed conditional, which Lesson 11 names as Bayes' theorem.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 3, Section 3.4 (contingency tables and probability trees). Companion
  practice: *Introductory Statistics 2e*, Section 3.5.
- **Prerequisites:** Conditional probability and independence from Lesson 09,
  plus the multiplication rule from Lesson 08.
- **Data notice:** Every lot, inspection flag, and path count is synthetic. The
  scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Decompose a two-stage experiment into a tree of mutually exclusive paths.
2. Label branches with frequencies or probabilities.
3. Multiply along a path to obtain a joint probability and add disjoint paths.
4. Explain why $P(B\mid A)$ can be a single branch while $P(A\mid B)$ requires
   combining paths.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: two stages, status then inspection | Sketch the four terminal paths. |
| 06-16 | Frequency tree and sample-space size | Confirm the four counts sum to 100. |
| 16-24 | Run Step 1 | Read 8, 2, 9, and 81 from the tree. |
| 24-34 | Probability labels and path multiplication | Compute $0.10\times0.80=0.08$. |
| 34-42 | Run Step 2 and add the flagged paths | Obtain $P(\text{flagged})=0.17$. |
| 42-48 | Run Step 3 and reverse the condition | Contrast $0.800000$ with $0.470588$. |
| 48-50 | Concept check and handoff to Lesson 11 | Name the inversion that Bayes will organize. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
register with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `tree_diagrams_01_frequency_tree.py` | Frequency tree, mutually exclusive terminal paths | $100$ lots; $10$ defective and $90$ clean; terminal counts $8$, $2$, $9$, $81$; flagged total $17$. |
| 2 | `tree_diagrams_02_probability_branches.py` | Branch probabilities, path multiplication, addition of disjoint paths | $P(D)=0.100000$, $P(F\mid D)=0.800000$, $P(D\cap F)=0.080000$, $P(F)=0.170000$, four-path sum $=1.000000$. |
| 3 | `tree_diagrams_03_reverse_conditional.py` | Reverse conditional from combined paths | $P(F\mid D)=0.800000$ versus $P(D\mid F)=0.470588=8/17$. Seed-42 simulation of $100{,}000$ lots: $0.469551$. |

The Step 3 result is a limit, not a named theorem yet. The tree is drawn in
time order, so $P(F\mid D)$ is a downward branch while $P(D\mid F)$ is not.
Lesson 11 organizes that inversion as Bayes' theorem using *Principles of Data
Science*, Section 3.4.

## Synthetic Inspection Register

| Lot status | Flagged | Not flagged | Row total |
|---|---:|---:|---:|
| Defective | 8 | 2 | 10 |
| Clean | 9 | 81 | 90 |
| Column total | 17 | 83 | 100 |

First-stage branches: $P(D)=10/100=0.10$ and $P(C)=90/100=0.90$. Second-stage
branches: $P(F\mid D)=8/10=0.80$ and $P(F\mid C)=9/90=0.10$. The flagged
probability is the sum of two mutually exclusive paths:

\[
P(F)=P(D)P(F\mid D)+P(C)P(F\mid C)=0.08+0.09=0.17.
\]

The reversed question uses the same two paths as numerator and denominator:

\[
P(D\mid F)=\frac{P(D\cap F)}{P(F)}=\frac{8}{17}=0.470588\ldots
\]

## Study Notebook

The student guide
[`notebooks/lesson_10_tree_diagrams_sample_space.ipynb`](notebooks/lesson_10_tree_diagrams_sample_space.ipynb)
integrates the three steps into one cumulative state. It builds the complete
100-lot synthetic register from constants, embeds a frequency tree and two
editable probability figures, and concludes with executable assertions, safe
practice, and collapsible answers. Its seed-42 check simulates 100,000 lots and
retains the exact $8/17$ benchmark.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Common Misconceptions

- A tree is a decomposition of one experiment, not a second data source.
- Branch labels on a stage are conditional on reaching that node.
- Joint path probabilities are products; mutually exclusive path totals are sums.
- $P(F\mid D)$ and $P(D\mid F)$ answer different questions and need not match.
- A simulation estimate can be close to the exact path ratio without replacing it.
- The synthetic register illustrates tree arithmetic. It is not a claim about any
  real inspection process.

## Package Structure

```text
L10_Tree_Diagrams_Sample_Space/
|-- README.md
|-- notebooks/
|   `-- lesson_10_tree_diagrams_sample_space.ipynb
|-- src/
|   |-- tree_diagrams_01_frequency_tree.py
|   |-- tree_diagrams_02_probability_branches.py
|   `-- tree_diagrams_03_reverse_conditional.py
|-- figures/
|   |-- tree_diagrams_01_frequency_tree.png
|   |-- tree_diagrams_02_path_probabilities.png
|   `-- tree_diagrams_03_reverse_conditional.png
`-- slides/
    |-- lesson_10.tex
    `-- lesson_10.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L10_Tree_Diagrams_Sample_Space/src/tree_diagrams_01_frequency_tree.py
uv run en/L10_Tree_Diagrams_Sample_Space/src/tree_diagrams_02_probability_branches.py
uv run en/L10_Tree_Diagrams_Sample_Space/src/tree_diagrams_03_reverse_conditional.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L10_Tree_Diagrams_Sample_Space/notebooks/lesson_10_tree_diagrams_sample_space.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_10.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_10.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Tree diagrams, branch labels, path multiplication, and sample-space
decomposition follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 3, Section
[3.4](https://openstax.org/books/introductory-business-statistics-2e/pages/3-4-contingency-tables-and-probability-trees).
Companion tree-and-Venn practice is in *Introductory Statistics 2e*, Section
[3.5](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams).
The reversed-conditional limit is prepared for *Principles of Data Science*,
Section 3.4, in Lesson 11. OpenStax publishes these texts under the Creative
Commons Attribution-NonCommercial-ShareAlike license. The synthetic dataset,
code, and figures in this package are original course materials.

