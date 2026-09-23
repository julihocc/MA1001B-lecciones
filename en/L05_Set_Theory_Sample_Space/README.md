# Lesson 05 - Set Theory and Sample Spaces

## Accessibility correction — 23 September 2026

The membership matrix retains its data, categories, and colors, while its
numeric annotations are now black (`#000000`). Against `#EC2661`, the
calculated contrast is 5.02:1 (previously 4.19:1 with white digits); it is
higher on the pale background. I regenerated the figure, the extensive
notebook outputs, and both PDF decks, and visually checked the matrix slide.
The three scripts retain their canonical counts. The compact notebook now
links to the extensive notebook via its public GitHub path, which also works
from Colab; the local copy remains beside it. The new hosted run and weekly
propagation are recorded separately.
The extensive notebook now points to the current 75-page deck. The deck
identifies the worked F solution as part of the companion notebook rather
than promising a separate solution slide; older page counts below are history.

This package provides an extended student guide and a 40-minute class route.
One fully synthetic dispatch experiment connects
Cartesian products, events, union, intersection, complement, disjointness, and
exhaustiveness with readable Python.

- **Track:** English, MA1001B.
- **Class route:** `slides/lesson_05_compact.pdf` (12 slides) and
  `notebooks/lesson_05_compact.ipynb` (11 cells, five code cells).
- **Extended study:** `slides/lesson_05.pdf` and
  `notebooks/lesson_05_set_theory_sample_space.ipynb`.
- **Deck:** `slides/lesson_05.pdf`. There is no
  slide-count ceiling; explanations are divided into student-readable pages.
- **Reference:** OpenStax, *Introductory Business Statistics 2e*, Sections 3.1
  and 3.2.
- **Data:** all 480 dispatches, frequencies, and probabilities are invented
  teaching assumptions. They are not data or estimates from a company.

## Compact route — 40-minute class

The compact slides and notebook were revised for this L05 demo. Open both and
run five code cells; computation takes seconds within the allotted blocks.
The notebook uses only the standard library and eight verified synthetic
frequencies from the seed-42 script. Generating 480 rows and their figures
remains in the extended study material.

| Minutes | Objective and slides/cells | Instructor action and check | Transition |
|---:|---|---|---|
| 00–10 | Model and eight tuples; slides 1–3, cell 1. | Introduce the dispatch, build $S$, and check that it has eight types. | Distinguish records. |
| 10–14 | Synthetic frequencies; slide 4, cell 2. | Compare 480 records with eight types; check that repeating a tuple does not change $|S|$. | Define events. |
| 14–26 | Events and operations; slides 5–7, cell 3. | Ask for predictions of intersection, union, and complement; run and compare types with records. | Compare pairs. |
| 26–33 | Disjointness and exhaustiveness; slides 8–9, cell 4. | Contrast A–B with C–D and check each property separately. | Apply both conditions. |
| 33–40 | Integration and close; slides 10–12, cell 5. | Define F, predict 2/40/1/5, and explain the units; bridge to L06. | End L05. |

This is an instructor timing estimate, not a timed classroom rehearsal.

## Learning outcomes

By the end, a student can:

1. Define the dispatch experiment, represent an outcome, and construct its
   sample space.
2. Distinguish possible outcomes, observed records, cardinalities, and
   frequencies.
3. Represent events as subsets and calculate union, intersection, and the
   complement relative to a stated universe.
4. Justify disjointness and exhaustiveness as separate set properties.
5. Implement and interpret these operations in Python, including the new event
   `F = Express and Delayed`.

Every objective has a worked example, an executable activity, and a check in
the deck and notebook.

## Synthetic dispatch model

One outcome is the ordered tuple

$$
(\text{shift},\ \text{service},\ \text{status}).
$$

The categories are Day/Night, Standard/Express, and On time/Delayed. The
sample space has $2\times2\times2=8$ possible outcome types. A `dispatch_id`
labels a row but is not part of the outcome; repeated rows can share one tuple.

The scripts generate 480 rows with `SEED = 42`. Shift and service probabilities
are unequal, and the delay probability is 0.10 plus 0.08 for Night and 0.12
for Express. The Express increment is deliberately synthetic: it must not be
read as a claim about a real service.

## Incremental source scripts

Each script is standalone and reconstructs the same model. Its calculation and
figure-building functions do not write files; `main()` coordinates execution
and uses `save_figure()` to retain the PNG. The functions separate academic
calculation from presentation and I/O:

| Step | Source | New functions | Verified result |
|:---:|---|---|---|
| 1 | `src/set_theory_01_sample_space.py` | `build_sample_space()`, `simulate_dispatches()`, `build_frequency_figure()` | $|S|=8$; 480 rows; frequencies `196/16/71/25/89/30/38/15`; maximum 196. |
| 2 | `src/set_theory_02_set_operations.py` | `define_events()`, `summarize_set_operations()`, `build_membership_figure()` | Cardinalities `4/4/2/6/4`; observed counts `172/86/45/213/308`. |
| 3 | `src/set_theory_03_disjoint_events.py` | `define_service_events()`, `compare_event_pairs()`, `build_pair_figure()` | A/B `2/6/False/False`; C/D `0/8/True/True`. |

Seaborn handles bar placement, grouped bars, and heatmap rendering after the
code has built explicit semantic tables. It does not replace the calculations:
the count, membership matrix, intersection, union, and universe comparison
remain visible and testable.

## Student deck

`slides/lesson_05.tex` and its compiled PDF follow the route

`intuition -> formal definition -> worked example -> implementation -> interpretation`.

The deck explains the dispatch context before notation, distinguishes the eight
possibilities from 480 observations, works through `4 + 4 - 2 = 6`, defines
relative complement, separates disjointness from exhaustiveness, and closes
with F, counterexamples, simulation assumptions, data structures, graphics, and
validation. Code fragments are included with `\lstinputlisting`; the complete
source remains in `src/`. The deck is student-facing: it contains no instructor
notes or facilitation instructions.

## Reproducible student notebook

[`notebooks/lesson_05_set_theory_sample_space.ipynb`](notebooks/lesson_05_set_theory_sample_space.ipynb)
is an executable companion, not a replacement for the deck. It:

- introduces context, objectives, formulas, and references to PDF revision
  `f38d037` and its verified physical page titles;
- copies the calculation and figure-building functions literally from the
  canonical source, including docstrings and comments, and records each
  source-to-cell mapping in cell metadata;
- introduces imports, constants, and shared state once, then replaces each
  script `main()` with sequential cells;
- displays each returned figure with `display()` and closes it explicitly; the
  notebook writes no PNG and does not use `__file__`, `Agg`, or `DIR_FIGURES`;
- executes the F integration, canonical assertions, and safe rejection checks
  for events outside S and empty pair mappings.

The notebook is self-contained at execution time: it reads no scripts, figures,
data files, network resources, or package-install commands. It can be run in a
clean kernel from the repository or from an isolated directory with the locked
environment.

## Validation record

The package was validated after source revision `f38d037`:

- all three scripts executed and reproduced the table and pair values above;
- all three PNGs were regenerated and visually reviewed;
- the deck compiled twice to 79 pages with no `Overfull \\vbox` warnings;
- the executed notebook passed `nbformat` and AST syntax checks, preserved all
  literal mapped functions, and was executed twice from clean kernels;
- an isolated copy of the notebook executed from a temporary directory;
- notebook checks confirmed exact 480-row reconstruction, canonical frequencies,
  cardinalities, observed counts, pair properties, F values, error contracts,
  and zero open Matplotlib figures;
- HTML export contained the full notebook and three embedded figures.

HTML export was checked structurally for the complete notebook and its three
embedded figures. A full browser visual review of the local HTML remains
subject to the local `file:` URL policy; no Colab validation is claimed.

## Package structure

```text
L05_Set_Theory_Sample_Space/
|-- README.md
|-- notebooks/
|   `-- lesson_05_set_theory_sample_space.ipynb
|-- src/
|   |-- set_theory_01_sample_space.py
|   |-- set_theory_02_set_operations.py
|   `-- set_theory_03_disjoint_events.py
|-- figures/
|   |-- set_theory_01_sample_space.png
|   |-- set_theory_02_set_operations.png
|   `-- set_theory_03_disjoint_events.png
`-- slides/
    |-- lesson_05.tex
    `-- lesson_05.pdf
```

## Running the package

From the repository root:

```bash
uv sync --frozen
uv run en/L05_Set_Theory_Sample_Space/src/set_theory_01_sample_space.py
uv run en/L05_Set_Theory_Sample_Space/src/set_theory_02_set_operations.py
uv run en/L05_Set_Theory_Sample_Space/src/set_theory_03_disjoint_events.py
```

Execute the notebook and retain its outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L05_Set_Theory_Sample_Space/notebooks/lesson_05_set_theory_sample_space.ipynb
```

Compile twice from `slides/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_05.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_05.tex
```

## OpenStax attribution

The conceptual foundation follows Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Chapter 3:
[Section 3.1](https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology)
for experiments, outcomes, sample spaces, events, unions, intersections, and
complements, and
[Section 3.2](https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
for mutually exclusive events. The text is CC BY-NC-SA 4.0. The dispatch case,
simulation, figures, code, results, and F comparison are original course
materials based on synthetic data.

