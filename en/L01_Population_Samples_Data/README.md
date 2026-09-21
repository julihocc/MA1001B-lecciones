# Lesson 01 - Population, Samples, and Data Types

This 50-minute micro-lesson introduces the language that connects business
questions to statistical evidence. Students work with one fully synthetic
operations register to distinguish a population from a sample, a parameter from
a statistic, and categorical data from quantitative data.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 1, Sections 1.1 and 1.2.
- **Prerequisites:** Basic algebra, Python expressions, and tabular data.
- **Data notice:** Every record in this lesson is synthetic. The scripts and
  notebook contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Define a target population and identify a sample drawn from it.
2. Match a population parameter with its sample statistic.
3. Classify variables as categorical, quantitative discrete, or quantitative
   continuous based on their analytical meaning.
4. Explain why a larger convenience sample can remain biased.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-05 | Opening question: What exactly do we want to learn about all orders? | State a target population and variable. |
| 05-15 | Population, sample, parameter, and statistic | Label each element in a business question. |
| 15-25 | Run Step 1 and compare the two distributions | Interpret $N$, $n$, $\mu$, and $\bar{x}$. |
| 25-35 | Classify variables and run Step 2 | Justify each type from meaning, not storage format. |
| 35-45 | Run Step 3 and examine selection bias | Compare sample size with estimation error. |
| 45-50 | Concept checkpoint and handoff | Defend one classification and one sampling claim before the session continues. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Student Study Notebook

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cc/MA1001B-lecciones/main/en/L01_Population_Samples_Data/notebooks/lesson_01_population_samples_data.ipynb)

[`lesson_01_population_samples_data.ipynb`](notebooks/lesson_01_population_samples_data.ipynb)
is the student-facing entry point for independent study. It adapts the three
standalone scripts into one incremental, top-to-bottom workflow with embedded
figures, executable checks, editable practice cells, and collapsible suggested
answers. Its function contracts and inline annotations preserve the
student-facing code documentation from `src/`, while explicitly explaining the
few notebook-specific substitutions for script entry points and file output. It
generates the synthetic population in memory and does not import the lesson
scripts, read the retained PNG files, or require an external dataset.

The notebook is stored with its verified outputs. A fresh Google Colab runtime
already provides its only dependencies: NumPy, pandas, Matplotlib, and IPython.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
population with `SEED = 42` and adds the next concept without importing another
lesson script.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `data_foundations_01_population_sample.py` | Population, random sample, parameter, statistic | $N=12{,}000$, $n=200$, $\mu=45.26$ min, $\bar{x}=46.11$ min, absolute error $=0.85$ min. |
| 2 | `data_foundations_02_data_types.py` | Analytical variable types | `order_id` acts as an identifier; `channel` and `region` are categorical; `items_per_order` is discrete; time and value are continuous. |
| 3 | `data_foundations_03_sampling_bias.py` | Selection bias as the limiting case | Random sample: $n=200$, error $0.85$ min. Convenience sample: $n=1{,}000$, error $6.24$ min. |

The Step 3 result demonstrates a limit, not a universal numerical rule. A large
sample can still produce a poor estimate when the selection process excludes
important parts of the population. Lesson 02 develops probability sampling
designs in detail.

## Variable Dictionary

| Variable | Analytical role | Reason |
|---|---|---|
| `order_id` | Identifier with a categorical role | Arithmetic on the code has no business meaning. |
| `channel` | Categorical | Values name order channels. |
| `region` | Categorical | Values name operating regions. |
| `items_per_order` | Quantitative discrete | The value counts individual items. |
| `processing_time_minutes` | Quantitative continuous | The value measures elapsed time. |
| `order_value_mxn` | Quantitative continuous | The value measures monetary magnitude. |

## Common Misconceptions

- A population means the full set defined by the question, not necessarily every
  person or transaction in existence.
- A parameter describes a population. A statistic comes from a sample and may
  vary across samples.
- Numeric storage does not guarantee a quantitative analytical role. An order ID
  remains a label.
- A larger sample reduces random sampling variation under suitable sampling, but
  size alone does not repair selection bias.
- The synthetic example illustrates statistical concepts. It provides no claim
  about any real organization or operating process.

## Package Structure

```text
L01_Population_Samples_Data/
|-- README.md
|-- src/
|   |-- data_foundations_01_population_sample.py
|   |-- data_foundations_02_data_types.py
|   `-- data_foundations_03_sampling_bias.py
|-- figures/
|   |-- data_foundations_01_population_sample.png
|   |-- data_foundations_02_data_types.png
|   `-- data_foundations_03_sampling_bias.png
|-- notebooks/
|   `-- lesson_01_population_samples_data.ipynb
`-- slides/
    |-- lesson_01.tex
    `-- lesson_01.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L01_Population_Samples_Data/src/data_foundations_01_population_sample.py
uv run en/L01_Population_Samples_Data/src/data_foundations_02_data_types.py
uv run en/L01_Population_Samples_Data/src/data_foundations_03_sampling_bias.py
```

To re-execute the notebook locally:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L01_Population_Samples_Data/notebooks/lesson_01_population_samples_data.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_01.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Concept definitions and the curricular sequence follow Alexander Holmes,
Barbara Illowsky, and Susan Dean, *Introductory Business Statistics 2e*,
Chapter 1, Sections
[1.1](https://openstax.org/books/introductory-business-statistics-2e/pages/1-1-definitions-of-statistics-probability-and-key-terms)
and
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling).
OpenStax publishes the text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

