# Lesson 03 - Central Tendency and Dispersion

This 50-minute micro-lesson uses one fully synthetic business-operations sample
to distinguish two questions: where processing times are centered and how much
they vary. Students calculate the mean, median, sample standard deviation, and
interquartile range, then examine how one extreme recorded delay affects each
summary.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 2, Sections 2.2, 2.3, and 2.7.
- **Prerequisites:** Population and sample terminology from Lesson 01, a
  defensible sampling design from Lesson 02, and basic Python functions.
- **Data notice:** Every record is synthetic. No real company, customer,
  facility, or partner data are used.

## Learning Outcomes

By the end of the lesson, a student can:

1. Calculate and interpret the arithmetic mean and median in context.
2. Calculate the sample standard deviation using the $n-1$ denominator.
3. Calculate the first quartile, third quartile, and interquartile range.
4. Pair mean with standard deviation and median with IQR when describing data.
5. Explain why one extreme value affects these summaries differently without
   treating sensitivity as automatic anomaly detection.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-05 | Frame the two descriptive questions: center and spread | Name the measurement, unit, and sample being summarized. |
| 05-17 | Define mean and median and run Step 1 | Calculate both centers and interpret their 0.49-minute difference. |
| 17-31 | Define sample standard deviation, quartiles, and IQR and run Step 2 | Reproduce $s$, Q1, Q3, and IQR in minutes. |
| 31-43 | Change one recorded value and run Step 3 | Compare how the four summaries respond to the same modification. |
| 43-50 | Concept check and transition | Select and defend a center-spread pair, then state what remains for L04. |

The slide deck contains eight core slides plus one suggested-answers appendix.
The concept check can lead into another micro-lesson in the same 100-minute
class. It does not imply that the full class session ends here.

## Synthetic Order Sample

The sample contains 240 synthetic orders. Processing time is generated from the
number of items, a simulated queue time, and measurement noise. The seed remains
42 in every script, and processing times are rounded to hundredths of a minute.

| Field | Role |
|---|---|
| `order_id` | Numeric identifier. It labels an order but is not a measurement. |
| `items_per_order` | Quantitative discrete input to the synthetic process. |
| `processing_time_minutes` | Quantitative continuous variable summarized in this lesson. |

## Student Study Notebook

[`lesson_03_central_tendency_dispersion.ipynb`](notebooks/lesson_03_central_tendency_dispersion.ipynb)
is the self-contained entry point for independent study. It converts the three
standalone scripts into one cumulative in-memory analysis, preserves the
seed-42 order sample, embeds three editable figures, and includes executable
assertions, safe practice cells, and collapsible answers.

The notebook generates every synthetic order entirely in memory. It does not
import the lesson scripts, read the retained PNG files, access the network, or
require any external dataset. Its saved outputs reproduce the canonical center,
spread, and sensitivity results below.

## Definitions Used in the Lesson

For observations $x_1,\ldots,x_n$:

- The **arithmetic mean** is $\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i$.
- The **median** is the middle value after ordering the observations, or the
  average of the two middle values when $n$ is even.
- The **sample standard deviation** is
  $s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}$ and measures spread
  around the mean in the variable's original units.
- The **interquartile range** is $\mathrm{IQR}=Q_3-Q_1$ and spans the middle
  50% of the ordered observations.

## Incremental Scripts and Verified Results

Each script is standalone and rebuilds the same sample with `SEED = 42`. The
values below come from direct execution in the locked `uv` environment.

| Step | Script | Added idea | Verified result |
|:---:|---|---|---|
| 1 | `descriptive_statistics_01_center.py` | Mean and median | $n=240$, mean $=45.19$ min, median $=44.70$ min, difference $=0.49$ min. |
| 2 | `descriptive_statistics_02_spread.py` | Sample standard deviation, quartiles, and IQR | $s=6.38$ min, Q1 $=40.53$ min, Q3 $=49.01$ min, IQR $=8.48$ min. |
| 3 | `descriptive_statistics_03_sensitivity.py` | Sensitivity to one extreme recorded delay | Order 300193 changes from 65.22 to 180.00 min. Mean changes by $+0.48$ min, median by $+0.00$ min, $s$ by $+4.34$ min, and IQR by $+0.00$ min. |

The displayed `+0.00` changes result from rounding to two decimals. The median
and IQR remain unchanged at the displayed precision, while the mean and sample
standard deviation increase. This comparison demonstrates sensitivity only.
Lesson 04 introduces boxplots and formal anomaly-detection rules.

## Choosing a Center-Spread Pair

| Data pattern or purpose | Center | Spread | Reason |
|---|---|---|---|
| Roughly symmetric distribution without influential extremes | Mean | Sample standard deviation | Both use every observation and describe variation around the mean. |
| Skewed distribution or influential extreme values | Median | IQR | Both depend on ordered positions and resist a small number of extremes. |

These are guidelines rather than automatic decisions. Analysts should inspect
the distribution, preserve the unit, and explain why the selected summaries fit
the decision context.

## Common Misconceptions

- The mean and median do not measure spread. Two samples can share a center and
  have very different variability.
- Standard deviation is not the average absolute distance from the mean. It is
  based on squared deviations and returns to the original units after taking a
  square root.
- The sample formula uses $n-1$. Using $n$ calculates a population standard
  deviation for the observed values instead.
- IQR is $Q_3-Q_1$, not the distance from the median to either quartile.
- A robust summary is less sensitive to extremes, not completely unaffected in
  every dataset.
- A large change in a summary does not prove that a value is an error or an
  anomaly. Context and a stated detection rule are still required.
- The synthetic results make no claim about any real operating process.

## Package Structure

```text
L03_Central_Tendency_Dispersion/
|-- README.md
|-- src/
|   |-- descriptive_statistics_01_center.py
|   |-- descriptive_statistics_02_spread.py
|   `-- descriptive_statistics_03_sensitivity.py
|-- figures/
|   |-- descriptive_statistics_01_center.png
|   |-- descriptive_statistics_02_spread.png
|   `-- descriptive_statistics_03_sensitivity.png
|-- notebooks/
|   `-- lesson_03_central_tendency_dispersion.ipynb
`-- slides/
    |-- lesson_03.tex
    `-- lesson_03.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_01_center.py
uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_02_spread.py
uv run en/L03_Central_Tendency_Dispersion/src/descriptive_statistics_03_sensitivity.py
```

Re-execute the student notebook locally with the locked environment:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L03_Central_Tendency_Dispersion/notebooks/lesson_03_central_tendency_dispersion.ipynb
```

Compile twice from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_03.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_03.tex
```

The retained PDF contains the eight-slide core and the suggested-answers
appendix. The repository stores it through Git LFS.

## OpenStax Attribution

The definitions and teaching sequence follow Alexander Holmes, Barbara
Illowsky, and Susan Dean, *Introductory Business Statistics 2e*, Chapter 2:
Section [2.2](https://openstax.org/books/introductory-business-statistics-2e/pages/2-2-measures-of-the-location-of-the-data)
for quartiles and IQR, Section
[2.3](https://openstax.org/books/introductory-business-statistics-2e/pages/2-3-measures-of-the-center-of-the-data)
for mean and median, and Section
[2.7](https://openstax.org/books/introductory-business-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
for sample standard deviation. The cited text is licensed under CC BY-NC-SA
4.0. The synthetic sample, code, figures, and sensitivity comparison are
original course materials.

