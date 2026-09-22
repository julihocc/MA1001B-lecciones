# Lesson 07: Counting Techniques II

## Repeated Categories and Allocations

This lesson extends counting from distinct objects to repeated
categories. One fully synthetic service-network scenario connects repeated
permutations, multinomial allocations, and combinations with repetition. The
final step exposes the central limit of counting: possible occupancy profiles
are not automatically equally likely.

## Learning Outcomes

By the end of the lesson, students can:

1. count distinct sequences when category labels repeat;
2. interpret a multinomial coefficient as an allocation of labeled objects to
   labeled categories with fixed sizes;
3. use stars and bars to count nonnegative allocations of identical units;
4. explain why counting possible profiles does not determine their
   probabilities.

## Prerequisites

- finite sample spaces and events from Lesson 05;
- the product rule, factorial notation, permutations, and combinations from
  Lesson 06;
- basic Python functions, tuples, loops, and bar charts.

## Current 40-Minute Class Route

The teacher uses [the compact notebook](notebooks/lesson_07_compact.ipynb) and
[compact slides](slides/lesson_07_compact.pdf) together. The notebook includes
executable enumeration and seeded simulation; the slides carry the visible
derivations and questions. This estimate fits within the 100-minute S02 class.

| Time | Compact focus | Check and transition |
|---:|---|---|
| 00-04 | Define labeled requests and repeated queue labels. | Name one outcome before selecting a rule. |
| 04-12 | Repeated permutations: $8!/(3!3!2!)=560$. | Check by enumeration; reinterpret the same coefficient. |
| 12-21 | Multinomial allocation: 560, including the 210-210-140 split for R01. | Identify labeled requests and category sizes. |
| 21-36 | Stars and bars: 165 profiles; compare exact routing probabilities with seed-42 simulation. | Explain why profiles are not equally likely. |
| 36-40 | Concept check and bridge to L08. | State what extra model information probability needs. |

## Earlier 50-Minute Reference Route

The following timing records the original package and is retained only as
historical context.

| Time | Activity | Evidence |
|---:|---|---|
| 0-5 min | Define one outcome before selecting a formula. | Students distinguish labeled requests from repeated queue labels. |
| 5-15 min | Derive repeated permutations. | Duplicate rearrangements are divided out. |
| 15-24 min | Run Step 1 and inspect its chart. | Formula and exhaustive enumeration both return 560. |
| 24-34 min | Reframe the same coefficient as a multinomial allocation. | Step 2 returns 560 allocations and the 210-210-140 split for R01. |
| 34-43 min | Count occupancy profiles with stars and bars. | Step 3 returns 165 nonnegative four-center profiles. |
| 43-48 min | Compare counting with routing probabilities. | Exact and simulated probabilities reject the equal-profile assumption. |
| 48-50 min | Concept check and bridge to L08. | Students state why probability needs more than a count. |

The concept check may connect directly to another lesson in the same class
session. It is not a mandatory end-of-session activity.

## Synthetic Service-Network Scenario

All requests, queues, service centers, and routing mechanisms are synthetic.
No real organization, partner, or operational claim is represented.

Eight labeled service requests first enter three labeled queues with fixed
sizes: three Priority, three Standard, and two Audit. The final step considers
eight units or requests across four labeled service centers.

### Repeated permutations

If a sequence contains category counts \(n_1,\ldots,n_k\), its distinct
rearrangements are

\[
\frac{n!}{n_1!n_2!\cdots n_k!}.
\]

For the 3-3-2 queue pattern,

\[
\frac{8!}{3!3!2!}=560.
\]

The naive count \(8!=40{,}320\) treats identical category labels as distinct.
It overcounts every unique sequence by \(3!3!2!=72\).

### Multinomial allocations

The same coefficient counts allocations of eight labeled requests to three
labeled queues of sizes 3, 3, and 2. Exhaustive enumeration produces 560
allocations. Across them, request R01 appears in Priority 210 times, Standard
210 times, and Audit 140 times. These counts reflect the fixed queue sizes:
\(3/8\), \(3/8\), and \(2/8\) of the 560 allocations.

### Combinations with repetition

Stars and bars counts ways to distribute \(m\) identical units among \(r\)
labeled categories:

\[
\binom{m+r-1}{r-1}.
\]

For eight units across four centers, the scripts verify

\[
\binom{8+4-1}{4-1}=\binom{11}{3}=165
\]

nonnegative ordered occupancy profiles.

## Scripts and Verified Results

Each script is standalone, accepts no command-line arguments, imports no other
lesson step, and writes only its corresponding PNG. The results below came
from repeated execution in the locked `uv` environment.

| Step | Script | Verified result |
|:---:|---|---|
| 1 | `allocations_01_repeated_permutations.py` | Formula and enumeration both return 560; the naive count is 40,320 and the duplicate factor is 72. |
| 2 | `allocations_02_multinomial_categories.py` | Formula and enumeration both return 560 allocations; R01 appears 210, 210, and 140 times across Priority, Standard, and Audit. |
| 3 | `allocations_03_star_bars_probability_limit.py` | Formula and enumeration both return 165 profiles. With 500,000 simulations and seed 42, selected profile estimates are 0.005288, 0.013000, and 0.025894. |

For independent uniform routing to four centers, the exact probabilities of
the ordered profiles are:

| Profile | Incorrect equal-profile value | Exact probability | Seed-42 simulation |
|---|---:|---:|---:|
| `(5, 1, 1, 1)` | 0.00606061 | 0.00512695 | 0.00528800 |
| `(4, 2, 1, 1)` | 0.00606061 | 0.01281738 | 0.01300000 |
| `(3, 2, 2, 1)` | 0.00606061 | 0.02563477 | 0.02589400 |

The false value \(1/165\) assumes that all occupancy profiles are equally
likely. Random routing instead weights each profile by the number of labeled
request sequences that produce it. Counting profiles alone therefore cannot
justify a probability assignment.

## Study Notebook

The compact notebook and slides above are teacher presentation material. The
following extensive notebook remains the student study guide; the original
scripts, figures, and extensive slides are retained.

The student guide
[`notebooks/lesson_07_counting_techniques_ii.ipynb`](notebooks/lesson_07_counting_techniques_ii.ipynb)
integrates the three steps into one cumulative state. It constructs all finite
collections in memory, preserves the documented function contracts from
`src/`, embeds three editable figures, and concludes with executable
assertions, safe practice, and collapsible answers. Its seed-42 simulation uses
500,000 draws and includes an exact reconstruction check.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Common Misconceptions

- Dividing by \(n!\) is not a general correction. Divide only by factorials of
  exchangeable repeated categories.
- A repeated-label sequence and an allocation of labeled requests are different
  descriptions that can share the same multinomial coefficient.
- Stars and bars requires identical units and labeled categories; changing
  either condition changes the sample space.
- An ordered profile such as `(5, 1, 1, 1)` names which center receives each
  count. Permuting its entries creates other ordered profiles.
- Counting 165 possible profiles does not prove that each has probability
  \(1/165\).
- Monte Carlo agreement supports the stated routing model; it does not prove
  that any real service network routes requests uniformly.

## Package Structure

```text
L07_Counting_Techniques_II/
|-- README.md
|-- notebooks/
|   |-- lesson_07_counting_techniques_ii.ipynb
|   `-- lesson_07_compact.ipynb
|-- src/
|   |-- allocations_01_repeated_permutations.py
|   |-- allocations_02_multinomial_categories.py
|   `-- allocations_03_star_bars_probability_limit.py
|-- figures/
|   |-- allocations_01_repeated_permutations.png
|   |-- allocations_02_multinomial_categories.png
|   `-- allocations_03_star_bars_probability_limit.png
`-- slides/
    |-- lesson_07.tex
    |-- lesson_07.pdf
    |-- lesson_07_compact.tex
    `-- lesson_07_compact.pdf
```

## Execution

Run from the repository root:

```powershell
uv sync --frozen
uv run en/L07_Counting_Techniques_II/src/allocations_01_repeated_permutations.py
uv run en/L07_Counting_Techniques_II/src/allocations_02_multinomial_categories.py
uv run en/L07_Counting_Techniques_II/src/allocations_03_star_bars_probability_limit.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L07_Counting_Techniques_II/notebooks/lesson_07_counting_techniques_ii.ipynb
```

Compile twice from the `slides/` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error lesson_07.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_07.tex
```

## Attribution and Scope

The probability foundation follows OpenStax, *Introductory Business Statistics
2e*, Chapter 3, Section 3.1: sample spaces, equally likely outcomes,
theoretical probability by counting, and long-run relative frequency. The
repeated-permutation, multinomial, and stars-and-bars formulas are a
course-developed combinatorial extension aligned with the MA1001B curriculum;
they are not attributed as definitions from that OpenStax section.

- OpenStax section: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Authors: Alexander Holmes, Barbara Illowsky, and Susan Dean.
- License notice used by the course source: CC BY-NC-SA 4.0.

