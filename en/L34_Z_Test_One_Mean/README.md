# Lesson 34 - Z Test for a Mean with Known Variance

This 50-minute micro-lesson runs a one-sided z test on a fully synthetic
delivery-time sample. With $n=40$ and known $\sigma=6$, the statistic is
$z=(\bar{x}-80)/(\sigma/\sqrt{n})$ and the $p$-value is the standard-normal
upper tail. The final step shows that a known $\sigma$ is rarely true in
operations data.

- **Target duration:** 50 minutes.
- **Canonical reference:** OpenStax, *Introductory Business Statistics 2e*,
  Chapter 9, Sections 9.3 and 9.4 (distribution needed for testing; full
  hypothesis-test examples).
- **Prerequisites:** Testing language from Lesson 33 and the known-sigma z
  interval from Lesson 27.
- **Data notice:** Every delivery time is synthetic. The scripts contain no
  real company, customer, or partner data.

## Learning Outcomes

By the end of the lesson, a student can:

1. Compute $z=(\bar{x}-\mu_{0})/(\sigma/\sqrt{n})$ when $\sigma$ is known.
2. Obtain the upper-tail $p$-value from the standard normal.
3. Decide at $\alpha=0.05$ by comparing $p$ with $\alpha$.
4. Explain why a known-$\sigma$ z test is rarely the right operations tool.

## 50-Minute Facilitation Route

| Time | Classroom movement | Observable student work |
|---:|---|---|
| 00-06 | Opening: $H_{0}:\mu=80$ vs $H_{1}:\mu>80$ | Write the z formula. |
| 06-16 | Known $\sigma=6$, $n=40$ | Confirm $\mathrm{SE}=0.948683$. |
| 16-24 | Run Step 1 | Read $\bar{x}=82.229590$ and $z=2.350194$. |
| 24-34 | Upper-tail $p$-value | Shade $P(Z\ge z)$. |
| 34-42 | Run Step 2 | Obtain $p=0.009382$ and reject $H_{0}$. |
| 42-48 | Run Step 3 with $s$ in place of $\sigma$ | See $p$ drop to $0.002215$. |
| 48-50 | Concept check and handoff to Lesson 35 | Name the one-sample $t$ test. |

The slide deck contains eight core slides plus one suggested-answers appendix.
or skipped when the same class session continues directly into another lesson.

## Incremental Scripts and Verified Results

The three programs are self-contained. Each program rebuilds the same synthetic
deliveries with `SEED = 42` and adds the next concept without importing another
lesson script. These values came from two matching executions in the locked
`uv` environment.

| Step | Script | New concept | Verified result |
|:---:|---|---|---|
| 1 | `z_test_mean_01_z_statistic.py` | $z$ statistic with known $\sigma$ | $n=40$, $\sigma=6$, $\bar{x}=82.229590$, $\mathrm{SE}=0.948683$, $z=2.350194$. |
| 2 | `z_test_mean_02_p_value.py` | Upper-tail $p$-value and decision | $p=0.009382<\alpha=0.05$; reject $H_{0}$. |
| 3 | `z_test_mean_03_known_sigma_limit.py` | $s$ is not $\sigma$ | $s=4.955099$; invalid z-with-$s$ gives $z=2.845789$ and $p=0.002215$. |

The Step 3 result is a limit: operations data almost never arrive with a known
population $\sigma$. Keeping a z reference curve after replacing $\sigma$ by
$s$ is the wrong test. Lesson 35 uses $t$ with $\mathrm{df}=n-1$.

## Synthetic Delivery Sample

The analyst treats $\sigma=6$ minutes as known and tests $H_{0}:\mu=80$ versus
$H_{1}:\mu>80$. The scripts generate $n=40$ iid $N(82,6)$ times only so that
the hidden mean can be checked.

\[
z=\frac{82.229590-80}{6/\sqrt{40}}=\frac{2.229590}{0.948683}=2.350194,
\]

\[
p=P(Z\ge 2.350194)=0.009382.
\]

The sample standard deviation from the same 40 times is $s=4.955099\neq 6$.

## Common Misconceptions

- The $p$-value is not the probability that $H_{0}$ is true.
- A small $p$-value is evidence against $H_{0}$, not a proof of the exact
  alternative value.
- $s$ is a statistic. It does not license the z reference curve.
- Known $\sigma$ is a modeling assumption, not a typical operations fact.
- The synthetic deliveries illustrate z arithmetic. They are not a claim
  about any real last-mile process.

## Package Structure

```text
L34_Z_Test_One_Mean/
|-- README.md
|-- src/
|   |-- z_test_mean_01_z_statistic.py
|   |-- z_test_mean_02_p_value.py
|   `-- z_test_mean_03_known_sigma_limit.py
|-- figures/
|   |-- z_test_mean_01_z_statistic.png
|   |-- z_test_mean_02_p_value.png
|   `-- z_test_mean_03_known_sigma_limit.png
|-- notebooks/
|   `-- lesson_34_z_test_one_mean.ipynb
`-- slides/
    |-- lesson_34.tex
    `-- lesson_34.pdf
```

## Running the Lesson

From the repository root:

```bash
uv sync --frozen
uv run en/L34_Z_Test_One_Mean/src/z_test_mean_01_z_statistic.py
uv run en/L34_Z_Test_One_Mean/src/z_test_mean_02_p_value.py
uv run en/L34_Z_Test_One_Mean/src/z_test_mean_03_known_sigma_limit.py
uv run jupyter nbconvert --execute --to notebook --inplace en/L34_Z_Test_One_Mean/notebooks/lesson_34_z_test_one_mean.ipynb
```

The executed student notebook is self-contained and Google Colab-compatible.
It integrates the three lesson steps in one cumulative in-memory state,
embeds three editable figures, and requires no repository files, downloads, or
external datasets.

Compile the slides from the `slides/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error lesson_34.tex
pdflatex -interaction=nonstopmode -halt-on-error lesson_34.tex
```

The compiled PDF contains the eight-slide core and the suggested-answers
appendix. It is a canonical lesson artifact and is stored through Git LFS.

## OpenStax Attribution

The z test for a mean with known variance, the test statistic, and the
$p$-value decision follow Alexander Holmes, Barbara Illowsky, and Susan Dean,
*Introductory Business Statistics 2e*, Chapter 9, Sections
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-distribution-needed-for-hypothesis-testing)
and
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
The unknown-$\sigma$ $t$ test is the natural continuation in Lesson 35.
OpenStax publishes this text under the Creative Commons
Attribution-NonCommercial-ShareAlike license. The synthetic dataset, code, and
figures in this package are original course materials.

