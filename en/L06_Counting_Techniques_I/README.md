# Lesson 06 - Counting Techniques I

This lesson uses one fully synthetic operations-review program
to count finite sample spaces. Students apply the product rule, distinguish
permutations from combinations, verify formulas through exhaustive Python
enumeration, and diagnose an overcounting error when restrictions interact.

- **Current class route:** 40 minutes with the compact notebook and slides.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 3, especially Section 3.1 for sample spaces and events.
- **Prerequisites:** Sample spaces, events, complements, and disjoint sets from
  Lesson 05, plus factorial notation.
- **Data notice:** Every facility, analyst, role, and restriction is synthetic.
  No real company, partner, employee, or operational data are used.
- **Scope note:** This older package retains four cumulative conceptual steps
  because the fourth exposes the required overcounting limit.

## Learning Outcomes

By the end of the lesson, a student can:

1. Apply the product rule to a sequence of finite choice stages.
2. Calculate permutations when assigned positions create distinct outcomes.
3. Calculate combinations when a selected subset has no internal roles.
4. Verify a counting formula through exhaustive enumeration.
5. Explain why selecting mandatory categories first can count the same final
   group more than once.

## Current 40-Minute Class Route

The teacher uses [the compact notebook](notebooks/lesson_06_compact.ipynb) and
[compact slides](slides/lesson_06_compact.pdf) together. The notebook is
self-contained and retains executable checks; the slides supply the visible
derivations and questions. The schedule is an estimate for this lesson within
the 100-minute S02 class.

| Time | Compact focus | Check and transition |
|---:|---|---|
| 00-03 | Define an outcome and the synthetic review setting. | Ask what one complete configuration contains. |
| 03-10 | Product rule: $3\times4\times2=24$. | Enumerate, then change from stages to distinct roles. |
| 10-18 | Permutations: $P(6,3)=120$. | Explain why role order matters; remove the roles. |
| 18-25 | Combinations: $\binom{6}{3}=20$. | Explain the $3!$ reduction; add restrictions. |
| 25-36 | Restricted groups: reject 420 against the 126-group universe, then derive 99. | Identify duplicate groups and disjoint exclusions. |
| 36-40 | Select a counting rule and bridge to L07. | State the outcome, order, and restrictions before choosing a formula. |

## Earlier 50-Minute Reference Route

The following timing documents the original package; it is retained as
historical context and is not the current S02 exposure route.

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-08 | Connect sample-space size with the product rule and run Step 1 | Verify $3\times4\times2=24$ by enumeration. |
| 08-20 | Assign three distinct roles and run Step 2 | Calculate $P(6,3)=120$ and explain why order matters. |
| 20-31 | Remove the role labels and run Step 3 | Calculate $\binom{6}{3}=20$ and explain the $3!$ reduction. |
| 31-44 | Add category and conflict restrictions and run Step 4 | Reject 420 as larger than the 126-element universe and derive 99. |
| 44-50 | Concept check and transition | Select a counting method and state how the same group could be overcounted. |

The extensive slide deck contains eight core slides plus one suggested-answers
appendix.
The concept check can lead into Lesson 07 during the same 100-minute class. It
does not imply that the full class session ends here.

## Synthetic Operations-Review Program

The four steps use related decisions in one synthetic review program:

- Step 1 configures a review across three fulfillment centers, four workflow
  stages, and two evidence types.
- Step 2 assigns three distinct roles from six process analysts.
- Step 3 forms an unranked three-person peer panel from the same six analysts.
- Step 4 forms a four-person review group from five operations analysts and
  four data specialists under a category rule and one stated conflict.

The scripts enumerate finite sets exactly. They use no stochastic simulation,
so a random seed is unnecessary and every run is deterministic by construction.

## Counting Rules

### Product rule

If a configuration requires one choice from each successive stage with
$n_1,n_2,\ldots,n_m$ available options, the total number of configurations is

$$
N=\prod_{i=1}^{m}n_i.
$$

The stages describe components of one outcome. The rule does not require the
options to have equal probabilities.

### Permutations

When $k$ distinct positions are filled without replacement from $n$ available
elements, order changes the outcome:

$$
P(n,k)=\frac{n!}{(n-k)!}.
$$

### Combinations

When only the selected subset matters, its internal ordering does not create a
new outcome:

$$
\binom{n}{k}=\frac{n!}{k!(n-k)!}=\frac{P(n,k)}{k!}.
$$

## Incremental Scripts and Verified Results

Each script is standalone, uses no command-line arguments or cross-imports, and
writes only its corresponding PNG. The values below come from repeated direct
execution in the locked `uv` environment.

| Step | Script | Added idea | Verified result |
|:---:|---|---|---|
| 1 | `counting_01_product_rule.py` | Product rule and exhaustive sample space | $3\times4\times2=24$ configurations, matching all 24 enumerated tuples. Each center contributes 8. |
| 2 | `counting_02_permutations.py` | Ordered role assignments without replacement | $P(6,3)=120$, matching 120 generated assignments. |
| 3 | `counting_03_combinations.py` | Unranked subset selection | $\binom{6}{3}=20$, matching 20 generated panels. The reduction from 120 is $3!=6$. |
| 4 | `counting_04_restrictions.py` | Overcounting trap and complement decomposition | The full universe has $\binom{9}{4}=126$ groups. The naive expression gives 420. Removing 6 single-discipline groups and 21 conflict groups leaves 99, matching exhaustive enumeration. |

The Step 4 naive expression is

$$
5\times4\times\binom{7}{2}=420.
$$

It first designates one member from each discipline and then fills the remaining
two positions. A final group with several members from a discipline can arise
from several different designated pairs, so the expression counts that group
more than once. The complement calculation begins from the 126 unique groups:

$$
126-5-1-21=99.
$$

The five all-operations groups and one all-data group are disjoint from the 21
groups containing the conflict pair, so this subtraction does not introduce a
second overlap.

## Study Notebook

The compact notebook and slides above are teacher presentation material. The
following extensive notebook remains the student study guide; the original
scripts, figures, and extensive slides are retained.

The student guide
[`notebooks/lesson_06_counting_techniques_i.ipynb`](notebooks/lesson_06_counting_techniques_i.ipynb)
integrates the four conceptual steps into one cumulative deterministic state.
It enumerates every finite collection in memory, preserves the documented
function contracts from `src/`, embeds four editable figures, and concludes
with executable assertions, safe practice, and collapsible answers.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Common Misconceptions

- The product rule counts complete configurations, not the sum of choices
  offered at separate stages.
- Permutations and combinations answer different questions. The presence of
  people or objects does not determine which formula applies.
- Reordering members creates a new permutation only when positions or sequence
  change the outcome.
- Exhaustive enumeration verifies a formula for the stated finite example. It
  does not replace the reasoning needed to select the formula.
- A computed count larger than the entire sample space proves that some
  outcomes were counted repeatedly.
- Subtracting invalid cases requires checking whether the excluded categories
  overlap.
- The synthetic results make no claim about any real review program.

## Package Structure

```text
L06_Counting_Techniques_I/
|-- README.md
|-- notebooks/
|   |-- lesson_06_counting_techniques_i.ipynb
|   `-- lesson_06_compact.ipynb
|-- src/
|   |-- counting_01_product_rule.py
|   |-- counting_02_permutations.py
|   |-- counting_03_combinations.py
|   `-- counting_04_restrictions.py
|-- figures/
|   |-- counting_01_product_rule.png
|   |-- counting_02_permutations.png
|   |-- counting_03_combinations.png
|   `-- counting_04_restrictions.png
`-- slides/
    |-- lesson_06.tex
    |-- lesson_06.pdf
    |-- lesson_06_compact.tex
    `-- lesson_06_compact.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L06_Counting_Techniques_I/src/counting_01_product_rule.py
uv run en/L06_Counting_Techniques_I/src/counting_02_permutations.py
uv run en/L06_Counting_Techniques_I/src/counting_03_combinations.py
uv run en/L06_Counting_Techniques_I/src/counting_04_restrictions.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L06_Counting_Techniques_I/notebooks/lesson_06_counting_techniques_i.ipynb
```

Compile twice from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_06.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_06.tex
```

The retained PDF contains the eight-slide core and the suggested-answers
appendix. The repository stores it through Git LFS.

## OpenStax Attribution

The probability framing follows Alexander Holmes, Barbara Illowsky, and Susan
Dean, *Introductory Business Statistics 2e*, Chapter 3, Section
[3.1](https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology),
which defines experiments, outcomes, sample spaces, and events. The complement
reasoning builds on the event operations introduced there. The cited text is
licensed under CC BY-NC-SA 4.0. The counting formulas, synthetic operations
example, Python verification, figures, and overcounting comparison are original
course scaffolding.

## 2026-09-25 · compact code guidance

Every code cell in the compact instructor notebook now carries explanatory comments beside the relevant operation. The executable Python and saved outputs were preserved; a fresh run reproduced the saved outputs. Student materials were not changed.

| Notebook | Code cells | SHA-256 |
|---|---:|---|
| [lesson_06_compact.ipynb](notebooks/lesson_06_compact.ipynb) | 4 | 529AB5214F7C0D9B4F0C5ABBA6CA9F23F16AE3E98065D4AED29C5ED7066847F5 |
