# Lesson 04 - Anomaly Detection and Boxplots

This 50-minute micro-lesson uses one fully synthetic business-operations sample
to compare three ways of locating unusually distant processing times. Students
check the empirical rule under its shape condition, apply Chebyshev's inequality
without a shape assumption, and use boxplot fences to flag records for further
investigation.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 2, Sections 2.1, 2.2, and 2.7.
- **Prerequisites:** Descriptive statistics from Lesson 03, including the mean,
  sample standard deviation, quartiles, and interquartile range.
- **Data notice:** Every order record is synthetic. No real company, customer,
  facility, partner, or operational data are used.

## Learning Outcomes

By the end of the lesson, a student can:

1. State the distribution condition required by the empirical rule.
2. Apply Chebyshev's inequality for data with any distribution shape.
3. Calculate lower and upper 1.5-IQR fences from Q1 and Q3.
4. Read a boxplot and identify potential outliers reproducibly.
5. Explain why a statistical flag starts an investigation rather than proving
   a cause, error, or business anomaly.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-05 | Revisit center, spread, and distance from the mean | Name the unit and summaries required for a distance rule. |
| 05-17 | Establish the empirical rule and run Step 1 | Compare observed coverage with 68%, 95%, and more than 99%. |
| 17-29 | Add queue delays and run Step 2 | Calculate the two Chebyshev lower bounds and compare them with observation. |
| 29-43 | Introduce boxplot fences and run Step 3 | Reproduce Q1, Q3, IQR, both fences, and the number of flags. |
| 43-50 | Concept check and investigation discussion | Separate a reproducible flag from a conclusion about its cause. |

The slide deck contains eight core slides plus one suggested-answers appendix.
The concept check can connect directly to another micro-lesson in the same
100-minute class. It does not imply that the full class session ends here.

## Synthetic Order Data

All three scripts rebuild the same 600 synthetic order records with `SEED = 42`.
Step 1 starts with bell-shaped processing times. Step 2 adds positive queue
delays to a seeded subset and produces a right tail. Step 3 replaces four times
with known synthetic extremes so the class can compare known construction with
the values selected by a general statistical rule.

| Field | Role |
|---|---|
| `order_id` | Numeric identifier. It labels an order but is not a quantitative measurement. |
| `processing_time_minutes` | Quantitative continuous measurement analyzed in every step. |
| `has_queue_delay` | Categorical indicator added in Step 2. |
| `known_injected_extreme` | Construction label added in Step 3 for validation only. |
| `flagged_by_iqr_rule` | Reproducible statistical flag added in Step 3. |

The construction label is available because the data are synthetic. Real
operational data rarely provide a known answer before investigation.

## Three Rules and Their Conditions

### Empirical rule

For a bell-shaped, symmetric distribution, approximately 68% of observations
fall within one standard deviation of the mean, approximately 95% fall within
two, and more than 99% fall within three. These percentages are approximations,
and the shape condition matters.

### Chebyshev's inequality

For any distribution and $k>1$, the proportion within $k$ standard deviations
of the mean is at least

$$
1-\frac{1}{k^2}.
$$

The lower bounds are 75% for $k=2$ and 88.89% for $k=3$. The observed
proportion may be much larger because the inequality supplies a minimum
guarantee rather than a prediction.

### Boxplot potential-outlier fences

With $\mathrm{IQR}=Q_3-Q_1$, the usual fences are

$$
Q_1-1.5(\mathrm{IQR})
\quad\text{and}\quad
Q_3+1.5(\mathrm{IQR}).
$$

Values beyond either fence are potential outliers. The rule describes their
position relative to the middle half of the data. It does not determine why the
values occurred.

## Incremental Scripts and Verified Results

Each script is standalone, uses no command-line arguments, and writes only its
corresponding PNG. The values below come from repeated direct execution in the
locked `uv` environment.

| Step | Script | Added idea | Verified result |
|:---:|---|---|---|
| 1 | `anomaly_detection_01_empirical_rule.py` | Empirical-rule coverage for a bell-shaped sample | $n=600$, mean $=44.87$ min, sample $s=4.87$ min. Observed coverage is 69.17%, 94.83%, and 99.50% within one, two, and three $s$. |
| 2 | `anomaly_detection_02_chebyshev.py` | Shape-free lower bounds after adding a right tail | 59 orders receive a queue delay. Mean $=45.79$ min, sample $s=5.84$ min, and skewness $=0.74$. Observed coverage is 95.33% within $2s$ against a 75.00% lower bound and 98.67% within $3s$ against 88.89%. |
| 3 | `anomaly_detection_03_boxplot_flags.py` | 1.5-IQR fences and investigation candidates | Q1 $=42.19$, Q3 $=48.89$, IQR $=6.71$, lower fence $=32.13$, and upper fence $=58.96$ min. The rule flags 24 orders, including all 4 injected extremes and 20 other observations. |

The 20 other flags are not automatically false positives. They are values that
meet the same positional rule without carrying the known construction label.
Their causes remain unknown and require record, process, and context checks.

## Study Notebook

The student guide
[`notebooks/lesson_04_anomaly_detection_boxplots.ipynb`](notebooks/lesson_04_anomaly_detection_boxplots.ipynb)
integrates the three steps into one cumulative state. It builds all 600
synthetic orders in memory, preserves the seeded row identities, embeds three
editable figures, and concludes with executable assertions, safe practice, and
collapsible answers.

The notebook is self-contained: it downloads no data, reads no repository
files, requires no network access, and does not import the package scripts or
retained images. It can therefore be uploaded directly to Google Colab, opened
in VS Code with a Colab kernel, or executed in the locked project environment.
Its figures are embedded cell outputs; the PNGs under `figures/` remain the
retained evidence produced by the standalone scripts.

## Investigation Workflow

1. Verify the record, unit, timestamp, and transformation history.
2. Compare the flagged value with operational context and related records.
3. Determine whether it reflects a valid rare event, process change, data
   problem, or another explanation.
4. Document the evidence and decide whether to retain, correct, exclude, or
   model the observation separately.

The statistical rule makes screening reproducible. The investigation supports
the eventual decision.

## Common Misconceptions

- The empirical rule does not apply to every distribution. It requires an
  approximately bell-shaped and symmetric pattern.
- Chebyshev's percentages are lower bounds, not expected percentages and not
  exact coverage predictions.
- A value outside three standard deviations is not automatically an error.
- A boxplot flag identifies a potential outlier. It does not establish the
  cause or business importance of that value.
- The 1.5 multiplier is a conventional screening rule rather than a universal
  scientific law.
- A larger dataset does not remove the need to inspect data quality and
  operational context.
- The synthetic results make no claim about any real operating process.

## Package Structure

```text
L04_Anomaly_Detection_Boxplots/
|-- README.md
|-- notebooks/
|   `-- lesson_04_anomaly_detection_boxplots.ipynb
|-- src/
|   |-- anomaly_detection_01_empirical_rule.py
|   |-- anomaly_detection_02_chebyshev.py
|   `-- anomaly_detection_03_boxplot_flags.py
|-- figures/
|   |-- anomaly_detection_01_empirical_rule.png
|   |-- anomaly_detection_02_chebyshev.png
|   `-- anomaly_detection_03_boxplot_flags.png
`-- slides/
    |-- lesson_04.tex
    `-- lesson_04.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_01_empirical_rule.py
uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_02_chebyshev.py
uv run en/L04_Anomaly_Detection_Boxplots/src/anomaly_detection_03_boxplot_flags.py
```

Execute the notebook and save all cell outputs:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  en/L04_Anomaly_Detection_Boxplots/notebooks/lesson_04_anomaly_detection_boxplots.ipynb
```

Compile twice from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_04.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_04.tex
```

The retained PDF contains the eight-slide core and the suggested-answers
appendix. The repository stores it through Git LFS.

## OpenStax Attribution

The definitions and teaching sequence follow Alexander Holmes, Barbara
Illowsky, and Susan Dean, *Introductory Business Statistics 2e*, Chapter 2:
Section [2.1](https://openstax.org/books/introductory-business-statistics-2e/pages/2-1-stem-and-leaf-graphs-line-graphs-and-bar-graphs)
for the need to investigate unusual observations with background information,
Section [2.2](https://openstax.org/books/introductory-business-statistics-2e/pages/2-2-measures-of-the-location-of-the-data)
for boxplots and the 1.5-IQR potential-outlier fences, and Section
[2.7](https://openstax.org/books/introductory-business-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
for Chebyshev's inequality and the empirical rule. The cited text is licensed
under CC BY-NC-SA 4.0. The synthetic data, code, figures, and investigation
workflow are original course materials.

