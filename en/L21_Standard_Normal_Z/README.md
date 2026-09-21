# Lesson 21 - Standard Normal Distribution and Z Scores

This 50-minute micro-lesson uses one fully synthetic audit-score clock modeled
as $\mathrm{Normal}(\mu=50,\sigma=8)$. The $z$-score $(x-\mu)/\sigma$ locates
a raw score on the standard normal ruler. $P(X\le 60)$ equals $P(Z\le 1.25)$.
The final step shows that a $z$-score comparison requires similar shape:
on a right-skewed delay clock, $z=-1$ is off the support.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 6, Section 6.1 (the standard normal distribution). Companion
  practice: *Introductory Statistics 2e*, Section 6.1.
- **Prerequisites:** Continuous density and the uniform model from Lessons 19
  and 20.
- **Data notice:** Every audit score, delay time, and $z$ value is synthetic.
  The scripts contain no real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Convert a raw score into $z=(x-\mu)/\sigma$.
2. Read $P(Z\le z)$ from the standard normal curve.
3. Transfer that probability back to $P(X\le x)$ on $N(\mu,\sigma)$.
4. Explain why skew makes a $z$-score percentile the wrong comparison.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: a bell of audit scores | Name $\mu=50$ and $\sigma=8$. |
| 06-16 | Standardize $x=60$ | Compute $z=(60-50)/8=1.25$. |
| 16-24 | Run Step 1 | Confirm $z=1.250000$. |
| 24-34 | Standard normal left tail | Sketch $P(Z\le 1.25)$. |
| 34-42 | Run Step 2 | Read $P(Z\le 1.25)=0.894350$. |
| 42-48 | Run Step 3 on a delay clock | Contrast $0.158655$ with $0.000000$ at $z=-1$. |
| 48-50 | Concept check and handoff to Lesson 22 | Name spec limits as $z$ cuts. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds its synthetic
clock with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `standard_normal_01_z_scores.py` | $z=(x-\mu)/\sigma$ on $N(50,8)$ | $z(60)=1.250000$; $z$ at $\mu\pm\sigma$ equals $\pm 1.000000$. |
| 2 | `standard_normal_02_standard_probabilities.py` | $P(Z\le 1.25)$ via `scipy.stats.norm` | $P(Z\le 1.25)=P(X\le 60)=0.894350$, $P(Z>1.25)=0.105650$. |
| 3 | `standard_normal_03_skew_breaks_z.py` | Skewed delay clock with the same $z$ formula | Exponential delays: mean $=$ sd $=20$. $P(Z\le -1)=0.158655$ on the bell versus $P(X\le 0)=0.000000$ on the delay clock. |

The Step 3 result is a limit. A $z$-score is a location in standard-deviation
units, not a portable percentile across shapes. Lesson 22 uses $z$ cuts as
specification limits and process yield.

## Student Study Notebook

The executed [student notebook](notebooks/lesson_21_standard_normal_z.ipynb)
is a self-contained, Google Colab-compatible study guide. It rebuilds all
three lesson steps in one cumulative in-memory state, embeds three figures,
and includes editable practice cells, collapsible answers, and assertions for
the canonical values. It was also executed from an empty temporary directory
and rendered to HTML and Markdown without reading repository files.

## Synthetic Audit-Score Model

Operating model: $X\sim N(50,8^2)$. The marked score is $x=60$:

\[
z=\frac{60-50}{8}=1.25,\qquad P(Z\le 1.25)=0.894350.
\]

The same probability is $P(X\le 60)$ on the raw clock. A second synthetic
clock records exponential delays with mean $20$ minutes, so $\sigma=20$ and
the support starts at $0$. Then $z=-1$ corresponds to $x=0$, which has
probability $0$, not the bell-curve value $0.158655$.

## Common Misconceptions

- $z$ is a location in $\sigma$ units. It is not itself a probability.
- $P(Z\le 1.25)$ and $P(X\le 60)$ match only after $X$ is standardized.
- Equal $z$ values are comparable only when the shapes are similar.
- On a right-skewed delay clock, $z=-1$ can sit on the boundary of the
  support, so the bell percentile does not transfer.
- `scipy.stats.norm.cdf` replaces a printed $z$ table; it does not change
  the meaning of the area.
- The synthetic scores illustrate $z$ arithmetic. They are not a claim
  about any real audit.

## Package Structure

```text
L21_Standard_Normal_Z/
|-- README.md
|-- src/
|   |-- standard_normal_01_z_scores.py
|   |-- standard_normal_02_standard_probabilities.py
|   `-- standard_normal_03_skew_breaks_z.py
|-- figures/
|   |-- standard_normal_01_z_scores.png
|   |-- standard_normal_02_standard_probabilities.png
|   `-- standard_normal_03_skew_breaks_z.png
|-- notebooks/
|   `-- lesson_21_standard_normal_z.ipynb
`-- slides/
    |-- lesson_21.tex
    `-- lesson_21.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L21_Standard_Normal_Z/src/standard_normal_01_z_scores.py
uv run en/L21_Standard_Normal_Z/src/standard_normal_02_standard_probabilities.py
uv run en/L21_Standard_Normal_Z/src/standard_normal_03_skew_breaks_z.py
```

Execute the student notebook from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  en/L21_Standard_Normal_Z/notebooks/lesson_21_standard_normal_z.ipynb
```

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_21.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_21.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The standard normal curve, $z$-scores, and left-tail probabilities follow
Alexander Holmes, Barbara Illowsky, and Susan Dean, *Introductory Business
Statistics 2e*, Chapter 6, Section
[6.1](https://openstax.org/books/introductory-business-statistics-2e/pages/6-1-the-standard-normal-distribution).
Companion standard-normal practice is in *Introductory Statistics 2e*,
Section
[6.1](https://openstax.org/books/introductory-statistics-2e/pages/6-1-the-standard-normal-distribution).
The skew limit prepares specification-limit applications in Lesson 22.
OpenStax publishes these texts under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code,
and figures in this package are original course materials.

