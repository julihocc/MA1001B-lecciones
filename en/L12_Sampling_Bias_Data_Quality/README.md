# Lesson 12 - Sampling Bias, Data Quality, and Nonsampling Error

This 50-minute micro-lesson uses one fully synthetic 8,000-row service-ticket
register to compare a simple random sample with a larger web-only convenience
sample and with a coverage gap that excludes one region. The final step shows
that cleaning incomplete rows does not restore units that were never in the
frame.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Sections 1.2 and 1.4. Companion data-quality discussion: *Principles of Data
  Science*, Sections 2.1 and 8.1.
- **Prerequisites:** Population versus sample from Lesson 01 and sampling
  designs from Lesson 02.
- **Data notice:** Every ticket, region, channel, and complaint flag is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Estimate a population complaint rate from a simple random sample and report
   sampling error.
2. Contrast that error with a larger convenience sample restricted to the Web
   channel.
3. Identify a coverage gap when a region is missing from the frame.
4. Explain why listwise cleaning of a biased frame cannot restore missing units.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: parameter versus sampling error | Name the complaint-rate parameter. |
| 06-16 | The 8,000-row register | Confirm region counts $2400$, $2400$, $2000$, $1200$. |
| 16-24 | Run Step 1 | Read population $0.119875$ and SRS error $0.014875$. |
| 24-34 | Web-only selection | Predict the direction of bias. |
| 34-42 | Run Step 2 | Contrast $n=400$ error $0.014875$ with $n=1{,}200$ error $0.063208$. |
| 42-48 | Run Step 3 and inspect West | See $0$ West tickets after cleaning. |
| 48-50 | Concept check and handoff to Lesson 13 | Name sampling error versus nonsampling error. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
register with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `sampling_bias_01_srs.py` | Complete frame and SRS | $N=8{,}000$; population rate $0.119875$; SRS $n=400$ rate $0.105000$; absolute error $0.014875$. |
| 2 | `sampling_bias_02_convenience_web.py` | Web-only convenience sample | Web rate $0.057323$; convenience $n=1{,}200$ rate $0.056667$; absolute error $0.063208$. Larger sample, more error. |
| 3 | `sampling_bias_03_coverage_gap.py` | Coverage gap, missingness, cleaning | West rate $0.276667$; no-West error $0.027669$; after cleaning, West tickets $=0$ and error $0.026509$. |

The Step 3 result is a limit: deleting incomplete rows can tidy a table without
repairing a frame that never contained West. Lesson 13 moves from sample quality
to a discrete random variable defined on a well-specified sample space.

## Synthetic Ticket Register

| Region | Tickets | Role in the bias story |
|---|---:|---|
| North | $2{,}400$ | In the frame |
| South | $2{,}400$ | In the frame |
| East | $2{,}000$ | In the frame; heavy Web channel |
| West | $1{,}200$ | Highest complaint rate; dropped in the coverage gap |

Verified rates with `SEED = 42`:

| Quantity | Value |
|---|---:|
| Population complaint rate | $0.119875$ |
| Web-channel complaint rate | $0.057323$ |
| Store-channel complaint rate | $0.176555$ |
| West complaint rate | $0.276667$ |
| Non-West complaint rate | $0.092206$ |
| Missing complaint flags | $616$ ($253$ in West) |

## Study Notebook

The executed, self-contained study guide is
[`notebooks/lesson_12_sampling_bias_data_quality.ipynb`](notebooks/lesson_12_sampling_bias_data_quality.ipynb).
It rebuilds the synthetic register in memory with `SEED = 42`, develops the
three lesson steps cumulatively, and embeds three figures. It also includes
canonical values. The notebook has been executed both in place and from an
empty temporary directory; its HTML and Markdown renders and all three figures
were inspected.

## Common Misconceptions

- A larger sample is not automatically a better sample.
- Convenience sampling from an easy channel is not a simple random sample.
- Coverage error is a nonsampling error: the units were never available.
- Listwise deletion removes incomplete rows; it does not impute missing regions.
- The synthetic register illustrates bias. It is not a claim about any real
  service process.

## Package Structure

```text
L12_Sampling_Bias_Data_Quality/
|-- README.md
|-- notebooks/
|   `-- lesson_12_sampling_bias_data_quality.ipynb
|-- src/
|   |-- sampling_bias_01_srs.py
|   |-- sampling_bias_02_convenience_web.py
|   `-- sampling_bias_03_coverage_gap.py
|-- figures/
|   |-- sampling_bias_01_srs.png
|   |-- sampling_bias_02_convenience_web.png
|   `-- sampling_bias_03_coverage_gap.png
`-- slides/
    |-- lesson_12.tex
    `-- lesson_12.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_01_srs.py
uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_02_convenience_web.py
uv run en/L12_Sampling_Bias_Data_Quality/src/sampling_bias_03_coverage_gap.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L12_Sampling_Bias_Data_Quality/notebooks/lesson_12_sampling_bias_data_quality.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_12.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_12.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

Sampling, variation, and study design follow Alexander Holmes, Barbara
Illowsky, and Susan Dean, *Introductory Business Statistics 2e*, Sections
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling)
and
[1.4](https://openstax.org/books/introductory-business-statistics-2e/pages/1-4-experimental-design-and-ethics).
Data-collection and ethics companion pages are *Principles of Data Science*,
Sections
[2.1](https://openstax.org/books/principles-data-science/pages/2-1-overview-of-data-collection-methods)
and
[8.1](https://openstax.org/books/principles-data-science/pages/8-1-ethics-in-data-collection).
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

