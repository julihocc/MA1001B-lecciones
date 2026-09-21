# Lesson 02 - Probability Sampling Designs

This 50-minute micro-lesson develops the sampling-design detail intentionally
reserved from Lesson 01. Students use one fully synthetic business-operations
population to implement simple random, proportional stratified, and one-stage
cluster sampling and to identify the selection unit in each design.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 1, Section 1.2.
- **Prerequisites:** Lesson 01 concepts; basic Python functions, indexing, and
  grouped data.
- **Data notice:** Every record is synthetic. No real company, customer,
  facility, or partner data are used.

## Learning Outcomes

By the end of the lesson, a student can:

1. Explain the role of a sampling frame in a probability sample.
2. Draw a simple random sample without replacement and calculate an order's
   inclusion probability.
3. Allocate and draw a proportional stratified sample across all regions.
4. Distinguish selecting individual orders from selecting whole facility
   clusters.
5. Explain why one seeded comparison does not establish a universal ranking of
   sampling designs.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-05 | Reconnect population, sample, and selection bias to a sampling frame | Identify the frame and the unit that could be selected. |
| 05-15 | Define simple random sampling and run Step 1 | Calculate the equal inclusion chance and inspect sample composition. |
| 15-30 | Partition the frame by region and run Step 2 | Verify proportional allocation and explain why every region appears. |
| 30-43 | Select whole facilities and run Step 3 | Identify the first-stage unit and compare sample sizes and errors. |
| 43-50 | Concept check and transition | Defend a design choice without claiming one method is always best. |

The slide deck contains eight core slides plus one suggested-answers appendix.
The concept check can lead directly into another lesson during a 100-minute

## Synthetic Population and Sampling Frame

The frame contains 12,000 synthetic orders: 500 orders from each of 24
facilities. Six facilities belong to each of four regions. Processing time
depends on region, facility, order size, and random noise, so orders within a
facility share a cluster effect.

| Field | Role in the design |
|---|---|
| `order_id` | Identifies an individual population unit. |
| `facility_id` | Identifies the cluster that contains an order. |
| `region` | Defines the four strata. |
| `items_per_order` | Contributes to synthetic processing time. |
| `processing_time_minutes` | Quantitative variable whose population mean is estimated. |

## Student Study Notebook

[`lesson_02_probability_sampling_designs.ipynb`](notebooks/lesson_02_probability_sampling_designs.ipynb)
is the self-contained entry point for independent study. It converts the three
standalone scripts into one cumulative in-memory analysis, preserves the
seed-42 population and sampling designs, embeds three editable figures, and
includes executable assertions, safe practice cells, and collapsible answers.

The notebook generates its synthetic population entirely in memory. It does
not import the lesson scripts, read the retained PNG files, access the network,
or require any external dataset. Its saved outputs reproduce the canonical
population, SRS, stratified, and cluster results below.

## Incremental Scripts and Verified Results

Each script is standalone and rebuilds the same population with `SEED = 42`.
The numerical results below were copied from direct execution in the locked
`uv` environment.

| Step | Script | Design and selection unit | Verified result |
|:---:|---|---|---|
| 1 | `sampling_designs_01_simple_random.py` | SRS; select 240 individual orders from the complete order frame | $N=12{,}000$, $n=240$, inclusion chance $=2.00\%$, $\mu=47.67$ min, $\bar{x}=47.17$ min, absolute error $=0.50$ min. |
| 2 | `sampling_designs_02_stratified.py` | Proportional stratified; select orders independently within every region | Allocation: 60 orders per region. Stratified mean $=47.95$ min and absolute error $=0.28$ min. |
| 3 | `sampling_designs_03_cluster.py` | One-stage cluster; select 4 facilities and include all their orders | Facilities F02, F11, F16, and F18; $n=2{,}000$ orders; inclusion chance $=16.67\%$; mean $=48.76$ min; error $=1.09$ min. |

The SRS selected 63 North, 68 Central, 51 West, and 58 Southeast
orders. Stratification fixed the allocation at 60 per region. The selected
facility clusters represented Central, North, and West but not Southeast.

These errors describe one deterministic teaching example, not a theorem that
stratified sampling always has the smallest error or cluster sampling always has
the largest. Precision depends on the population structure, allocation,
estimator, and realized random sample. Cluster sampling may still be operationally
attractive when visiting a few groups is cheaper than reaching scattered units.

## Design Comparison

| Design | Randomized selection | Coverage in this lesson | Practical requirement |
|---|---|---|---|
| Simple random | 240 orders from the full frame | Every order has the same 2.00% inclusion chance | A complete list of orders |
| Proportional stratified | 60 orders within each region | Every region contributes observations | Region labels for every order |
| One-stage cluster | 4 facilities, then every order in each selected facility | Four facilities and three regions appear | A facility list and access to all units in selected facilities |

## Common Misconceptions

- Probability sampling requires a known random selection mechanism; it does not
  mean that the realized sample will exactly match every population percentage.
- In proportional stratified sampling, each stratum contributes observations.
  The strata are not the sampled units; orders are sampled within them.
- In one-stage cluster sampling, the first randomized units are clusters. Every
  order in a selected facility enters the sample in this implementation.
- A sample of 2,000 clustered orders does not necessarily carry as much
  independent information as 2,000 orders scattered across the full frame.
- Lower error in one seeded run does not prove that a design is universally
  superior.
- The synthetic results make no claim about any real operating network.

## Package Structure

```text
L02_Probability_Sampling_Designs/
|-- README.md
|-- src/
|   |-- sampling_designs_01_simple_random.py
|   |-- sampling_designs_02_stratified.py
|   `-- sampling_designs_03_cluster.py
|-- figures/
|   |-- sampling_designs_01_simple_random.png
|   |-- sampling_designs_02_stratified.png
|   `-- sampling_designs_03_cluster.png
|-- notebooks/
|   `-- lesson_02_probability_sampling_designs.ipynb
`-- slides/
    |-- lesson_02.tex
    `-- lesson_02.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_01_simple_random.py
uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_02_stratified.py
uv run en/L02_Probability_Sampling_Designs/src/sampling_designs_03_cluster.py
```

Re-execute the student notebook locally with the locked environment:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace en/L02_Probability_Sampling_Designs/notebooks/lesson_02_probability_sampling_designs.ipynb
```

Compile twice from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_02.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_02.tex
```

The retained PDF contains the eight-slide core and the suggested-answers
appendix. It is stored through Git LFS.

## OpenStax Attribution

The definitions and curricular sequence for simple random, stratified, and
cluster sampling follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 1, Section
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling).
The cited text is licensed under CC BY-NC-SA 4.0. The synthetic population,
code, figures, and seeded comparison in this package are original course
materials.

