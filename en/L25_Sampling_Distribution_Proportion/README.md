# Lesson 25 - Sampling Distribution of a Proportion

This 50-minute micro-lesson uses one fully synthetic late-delivery indicator
with population proportion $p=0.18$. Samples of $n=120$ tickets have
$\mathrm{SE}(\hat p)=\sqrt{p(1-p)/n}$. A seed-42 simulation of 5{,}000
samples recovers that SE. The final step shows that $np<5$ makes the
normal approximation to $\hat p$ fail.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 7, Section 7.3 (the central limit theorem for proportions).
  Companion practice: *Introductory Statistics 2e*, Section 7.3.
- **Prerequisites:** Sampling distribution of $\bar x$ and the CLT from
  Lessons 23 and 24.
- **Data notice:** Every late-delivery flag and sample proportion is
  synthetic. The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Write $E[\hat p]=p$ and $\mathrm{SE}(\hat p)=\sqrt{p(1-p)/n}$.
2. Check the $np$ and $n(1-p)$ conditions for a normal approximation.
3. Recover the SE formula from a seeded binomial simulation.
4. Explain why $np<5$ makes the bell model of $\hat p$ the wrong tool.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: a 0-1 late-delivery flag | Name $p=0.18$ and $n=120$. |
| 06-16 | SE formula and $np$ counts | Compute $np=21.6$ and $n(1-p)=98.4$. |
| 16-24 | Run Step 1 | Read SE $=0.035071$. |
| 24-34 | Simulate many $\hat p$ | Predict mean near $0.18$. |
| 34-42 | Run Step 2 | Obtain empirical SE $0.035079$. |
| 42-48 | Run Step 3 with $n=20$ | Contrast $np=3.6$ and $P(\hat p=0)=0.018892$. |
| 48-50 | Concept check and handoff to Lesson 26 | Name unbiasedness of $\hat p$ as an estimator. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same
$p=0.18$ indicator with `SEED = 42` and adds the next concept without
importing another lesson script. These values came from two matching
executions in the locked `uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `sampling_proportion_01_se_phat.py` | $\mathrm{SE}(\hat p)$ and $np$ checks | $np=21.600000$, $n(1-p)=98.400000$, SE $=0.035071$. |
| 2 | `sampling_proportion_02_simulation.py` | 5{,}000 samples of $n=120$ | Mean of $\hat p=0.179663$, empirical SE $=0.035079$, simulated $P(\hat p>0.22)=0.119800$ versus normal $0.127032$. |
| 3 | `sampling_proportion_03_np_condition_limit.py` | $n=20$, $np=3.6<5$ | Exact $P(\hat p=0)=0.018892$, simulated $0.016600$, normal mass near 0 $=0.035594$, skewness $=0.430019$. |

The Step 3 result is a limit. The normal curve for $\hat p$ needs both $np$
and $n(1-p)$ at least 5. Lesson 26 treats $\bar x$ and a one-observation
estimator as competing point estimators.

The executed [student notebook](notebooks/lesson_25_sampling_distribution_proportion.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Late-Delivery Indicator

Population proportion $p=0.18$. For iid tickets,

\[
E[\hat p]=0.18,\qquad
\mathrm{SE}(\hat p)=\sqrt{\frac{0.18\times 0.82}{120}}=0.035071.
\]

The counts $np=21.6$ and $n(1-p)=98.4$ both exceed 5. A seed-42 experiment
of 5{,}000 samples recovers empirical SE $0.035079$. For $n=20$,
$np=3.6<5$ and $P(\hat p=0)=0.018892$, a point mass the bell cannot
represent.

## Common Misconceptions

- $\hat p$ is a sample statistic. $p$ is the population parameter.
- $\sqrt{p(1-p)/n}$ uses the population $p$, not a single observed $\hat p$,
  when the sampling distribution is the object of study.
- $np\ge 5$ and $n(1-p)\ge 5$ are conditions for the normal picture, not
  for the existence of $\hat p$.
- $P(\hat p=0)$ can be material when $n$ is small. A continuous bell has no
  such point mass.
- A close simulation SE such as $0.035079$ checks $0.035071$. It does not
  replace the formula.
- The synthetic flags illustrate sampling arithmetic. They are not a claim
  about any real delivery process.

## Package Structure

```text
L25_Sampling_Distribution_Proportion/
|-- README.md
|-- src/
|   |-- sampling_proportion_01_se_phat.py
|   |-- sampling_proportion_02_simulation.py
|   `-- sampling_proportion_03_np_condition_limit.py
|-- figures/
|   |-- sampling_proportion_01_se_phat.png
|   |-- sampling_proportion_02_simulation.png
|   `-- sampling_proportion_03_np_condition_limit.png
|-- notebooks/
|   `-- lesson_25_sampling_distribution_proportion.ipynb
`-- slides/
    |-- lesson_25.tex
    `-- lesson_25.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L25_Sampling_Distribution_Proportion/src/sampling_proportion_01_se_phat.py
uv run en/L25_Sampling_Distribution_Proportion/src/sampling_proportion_02_simulation.py
uv run en/L25_Sampling_Distribution_Proportion/src/sampling_proportion_03_np_condition_limit.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L25_Sampling_Distribution_Proportion/notebooks/lesson_25_sampling_distribution_proportion.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_25.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_25.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The sampling distribution of $\hat p$ and $\mathrm{SE}=\sqrt{p(1-p)/n}$
follow Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory
Business Statistics 2e*, Chapter 7, Section
[7.3](https://openstax.org/books/introductory-business-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions).
Companion proportion practice is in *Introductory Statistics 2e*, Section
[7.3](https://openstax.org/books/introductory-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions).
The $np$ limit prepares point-estimator properties in Lesson 26. OpenStax
publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

