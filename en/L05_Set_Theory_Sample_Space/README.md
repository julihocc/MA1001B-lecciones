# Lesson 05 — Set Theory and Sample Spaces

## Current version — 24 September 2026

The eight-slide **compact presentation** explains theory through a die:
sample space, events, intersection, union, complement, disjointness, and
exhaustiveness. It stands on its own. The 16-cell **compact notebook** (five
code cells) independently develops a coded example with 480 synthetic
dispatches. It distinguishes eight possible outcome types from observed
frequencies and performs operations on dispatch IDs. Explain the change
of universe when switching resources.

- Instructor: [presentation](instructor/lesson_05_compact.pdf),
  [LaTeX source](instructor/lesson_05_compact.tex), and
  [worked notebook](instructor/lesson_05_compact.ipynb).
- Student self-study: [extended PDF](student/lesson_05.pdf),
  [LaTeX source](student/lesson_05.tex), and
  [extended notebook](student/lesson_05_set_theory_sample_space.ipynb).
- Earlier compact versions: `antecedentes/pre-autonomia-2026-09-24/`.
- Reference: OpenStax, *Introductory Business Statistics 2e*, 3.1–3.2.
- Data: all dispatch records are synthetic.

### Estimated 40-minute compact route

| Minutes | Goal and resource | Instructor action and check | Transition |
|---:|---|---|---|
| 00–10 | Concepts and die universe; deck pp. 1–2. | Define experiment, outcome, sample space, and event; check that an event is a subset of S. | Set operations. |
| 10–18 | Operations; deck pp. 3–6. | Find intersection, union without duplicates, and complement; check cardinalities. | Event properties. |
| 18–23 | Disjointness and exhaustiveness; deck pp. 7–8. | Check empty intersection and union equal to S separately. | Change universe. |
| 23–28 | Eight types; notebook section 1, code cell 3. | Run Cartesian product and check `|S|=8`. | Observed records. |
| 28–34 | Simulation; notebook section 2, code cell 6. | Run 480 dispatches with seed 42; distinguish type and record units. | Operations on IDs. |
| 34–38 | Events and properties; notebook sections 3–4, code cells 9 and 12. | Check 45 in A∩B, 213 in A∪B, and C,D disjoint and exhaustive. | Final query. |
| 38–40 | Query F; notebook section 5, code cell 15. | Check 40 delayed express dispatches and interpret the answer. | Close L05. |

This is an instructor estimate, not a timed classroom rehearsal. Local runs
with locked dependencies and visual review are recorded separately. The dated
notes below describe earlier stages and may mention historical paths, counts,
or publication states; the current resources are linked above.

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

`student/lesson_05.tex` and its compiled PDF follow the route

`intuition -> formal definition -> worked example -> implementation -> interpretation`.

The deck explains the dispatch context before notation, distinguishes the eight
possibilities from 480 observations, works through `4 + 4 - 2 = 6`, defines
relative complement, separates disjointness from exhaustiveness, and closes
with F, counterexamples, simulation assumptions, data structures, graphics, and
validation. Code fragments are included with `\lstinputlisting`; the complete
source remains in `src/`. The deck is student-facing: it contains no instructor
notes or facilitation instructions.

## Reproducible student notebook

[`student/lesson_05_set_theory_sample_space.ipynb`](student/lesson_05_set_theory_sample_space.ipynb)
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

## Current package structure

```text
L05_Set_Theory_Sample_Space/
├── instructor/   compact presentation (.tex and .pdf), compact notebook
├── student/      extended presentation (.tex and .pdf), extended notebook
├── antecedentes/ earlier compact versions
├── src/         three shared incremental scripts
├── figures/     three shared figures
└── README.md
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
  en/L05_Set_Theory_Sample_Space/student/lesson_05_set_theory_sample_space.ipynb
```

Compile twice from `student/`:

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

