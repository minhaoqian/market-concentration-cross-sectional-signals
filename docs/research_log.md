# Research Log

This log records important research decisions, changes in scope, rejected alternatives, data issues, and next steps.

The purpose is to preserve the evolution of the project and reduce hindsight bias when interpreting later results.

---

## 2 June 2026

### Project setup

- Created a dedicated GitHub repository for the project.
- Chosen working topic: market concentration and cross-sectional equity signals.
- WRDS registration has been approved.
- Decided to structure the work as a reproducible research repository rather than as a single notebook or one-off backtest.
- Decided that licensed WRDS raw data will not be uploaded to the public repository.
- Initial version will prioritise price-based signals before extending to fundamental signals.

### Current working research question

Does rising concentration in the US equity market alter the effectiveness of common cross-sectional equity signals, and do observed signal returns persist after controlling for sector, market-beta, and mega-cap exposures?

### Immediate next steps

1. Review the academic and practitioner literature.
2. Confirm which WRDS datasets are available under the Oxford subscription.
3. Define the point-in-time US equity universe.
4. Specify the primary concentration measure and signal definitions.
5. Write the pre-analysis plan before examining the main empirical results.


---

## 3 June 2026 — Literature Review v0.1

### Work completed

- Added a structured literature review covering canonical cross-sectional signals, market concentration, institutional constraints, neutralisation, and concentration measurement.
- Identified recent work suggesting that concentration can affect pricing, institutional behaviour, aggregate predictability, and the size premium.
- Identified literature showing that sector/factor neutralisation can remove expected-return exposure as well as risk.

### Important design decision

Market concentration will be treated primarily as a **conditioning variable**, not as a direct market-timing or alpha signal.

The project will compare both:

1. signal-level predictability, such as rank information coefficients; and
2. portfolio-level outcomes, including raw and neutralised implementations.

### Preliminary research gap

The current working gap is the intersection between aggregate US equity-market concentration and the effectiveness/exposure structure of multiple familiar cross-sectional signals.

This gap is provisional and will be revised if further literature reveals closely overlapping work.

### Next step

Review the canonical empirical definitions of short-term reversal and low-volatility signals, then draft the pre-analysis plan before examining the main empirical results.

---

## 4 June 2026 — Pre-Analysis Plan v0.1

### Primary signal definitions fixed provisionally

- **Momentum:** cumulative return over months t-12 to t-2 (prior 2–12 months).
- **Short-term reversal:** negative of the immediately preceding one-month return.
- **Low volatility:** negative of realised daily-return volatility over the prior 21 trading days; minimum 15 valid daily returns.
- **Low beta:** negative of a conventional CAPM beta estimated from the prior 252 trading days; minimum 126 valid observations.

### Primary research frequency

- Monthly portfolio formation.
- Signals observed at month-end t.
- Portfolio held during month t+1.

### Primary concentration measures

- Top-10 market-cap share.
- Market-cap HHI.

Top-5 market-cap share is reserved as a robustness measure.

### Primary portfolio design

- Point-in-time US common-stock universe.
- Initial CRSP screen: share codes 10/11 and exchange codes 1/2/3.
- Exclude firms below the 20th percentile of NYSE market capitalisation at each formation date.
- Require absolute month-end price >= $5.
- Form signal quintiles monthly.
- Primary portfolios value-weighted; equal-weighted results reported as robustness.
- Signal-level predictive statistic: next-month Spearman rank IC.

### Important methodological principle

All signal definitions are oriented so that a higher signal value corresponds to higher predicted future return. This lets all long-short portfolios use the same Q5-minus-Q1 convention.

### Items still to lock before Version 1.0

- exact CRSP tables and field units;
- delisting-return combination rule;
- sector-neutralisation implementation;
- beta-neutralisation implementation;
- transaction-cost assumptions;
- HAC/Newey-West lag rule;
- final sample start date if data availability requires revision.

---

## 9 June 2026 — CRSP CIZ schema confirmation

### Daily Stock File confirmed

Reviewed the WRDS Variable Descriptions for **CRSP Stock Version 2 (CIZ) — Daily Stock File**.

Confirmed key CIZ fields include:

- `permno`, `permco`
- `ticker`, `tradingsymbol`, `issuernm`
- `issuertype`, `securitytype`, `securitysubtype`, `sharetype`
- `primaryexch`, `siccd`, `naics`, `icbindustry`
- `dlycaldt`
- `dlyprc`
- `dlycap`
- `dlyret`, `dlyretx`, `dlyreti`
- `dlyvol`
- relevant return / price / capitalization flags
- delisting-related classification fields.

### Important schema revision

The project was initially drafted using legacy CRSP conventions such as SHRCD and EXCHCD. The available WRDS product is CIZ, which exposes newer classification fields.

The production common-stock and exchange filters will therefore be redefined using the official CIZ coding documentation before any main result is run.

This is a data-schema revision made before viewing results.

### Next step

Inspect the Monthly Stock File variable descriptions and then the Delisting Information schema.


---

## 10 June 2026 — Monthly Stock File schema confirmation

Reviewed the CIZ Monthly Stock File variable descriptions.

Confirmed primary fields include:

- `mthcaldt`
- `mthprc`
- `mthcap`
- `mthprevcap`
- `mthret`
- `mthretx`
- `mthretflg`
- `mthdelflg`
- `mthvol`
- `shrout`
- distribution / adjustment metadata.

### Major design implication

The primary monthly pipeline can use:

- `mthret` for momentum, reversal, and next-month realised return;
- `mthprc` for the $5 screen;
- `mthcap` for market-cap weighting and Top-10 / HHI concentration measures.

Market capitalization therefore does not need to be reconstructed from price × shares outstanding in the primary specification unless validation checks show a discrepancy.

### Next step

Inspect the separate Delisting Information schema before locking the production return construction and then run a small test extraction rather than immediately downloading the full sample.


---

## 11 June 2026 — Delisting Information schema confirmation

Reviewed the CRSP CIZ Delisting Information variable descriptions.

Confirmed fields include:

- `permno`
- `delistingdt`
- `deldtprc`
- `deldtprcflg`
- `delactiontype`
- `delstatustype`
- `delreasontype`
- `delpaymenttype`
- `delpermno`
- `delpermco`
- `delret`
- `delretmisstype`
- `delnextdt`
- `delnextprc`
- `delnextprcflg`
- `delamtdt`
- `deldivamt`
- `deldistype`
- `deldlydt`.

### Important implication

CIZ provides an explicit `delret` field for delisting total return. The project will therefore incorporate delisting events rather than relying only on ordinary monthly returns.

The exact monthly-return + delisting-return combination rule remains intentionally unlocked until the official CIZ documentation is checked.

### Next step

Move from schema discovery to a small WRDS test extraction, while also confirming the official CIZ coding and return-construction documentation before freezing Version 1.0 of the analysis plan.


---

## 13 June 2026 — Sample-construction protocol v0.1

### Official CIZ universe mapping locked

The primary common-stock universe now uses the official WRDS CIZ mapping of legacy CRSP share codes 10/11:

- ShareType = NS
- SecurityType = EQTY
- SecuritySubType = COM
- USIncFlg = Y
- IssuerType in {ACOR, CORP}

The primary exchange universe uses:

- PrimaryExch = N — NYSE
- PrimaryExch = A — NYSE MKT / NYSE American
- PrimaryExch = Q — NASDAQ

The earlier legacy SHRCD / EXCHCD wording in analysis_plan.md has been replaced accordingly.

### Duplicate investigation resolved

A filtered 2024 Monthly Stock File test pull contained 47,143 rows and 4,153 unique PERMNO values.

There were 199 rows across 99 duplicated PERMNO-month groups. After distribution fields were excluded, every remaining duplicate was an exact full-row duplicate.

Production rule:

1. remove exact full-row duplicates;
2. assert uniqueness of PERMNO + MthCalDt;
3. halt if any non-identical duplicate key remains.

### Size and price screens

Primary screens remain:

- MthPrc >= $5;
- monthly market cap >= the 20th percentile of NYSE MthCap.

The NYSE breakpoint is calculated point-in-time each month from eligible NYSE common stocks before applying the final retained-universe rule.

### Next unresolved issue

Confirm the exact CIZ delisting-return semantics so that MthRet and DelRet are combined without double counting.


---

## 15 June 2026 — Monthly production pipeline scaffold

Created the first reproducible Python implementation of the monthly data pipeline.

### New files

- `src/clean_monthly.py`
- `src/concentration.py`
- `notebooks/01_monthly_data_audit.ipynb`

### Cleaning logic implemented

- exact full-row deduplication;
- hard failure if non-identical PERMNO-month duplicates remain;
- primary-exchange filter N/A/Q;
- positive market-cap requirement;
- monthly NYSE 20th-percentile market-cap breakpoint;
- $5 price screen;
- explicit audit table of row and security counts at each stage.

### Concentration measures implemented

- Top-5 market-cap share;
- Top-10 market-cap share;
- HHI;
- effective number of firms (1 / HHI);
- aggregate market capitalisation;
- monthly security counts.

### Research discipline

The notebook is an audit / validation notebook. It does not yet estimate factor returns or test the main hypothesis.


---

## 17 June 2026 — Concentration sanity check and PERMCO revision

### Sanity checks passed

Selected year-end concentration estimates were economically plausible and internally consistent. Historical top-company tables also showed sensible point-in-time composition.

### Multi-class share issue discovered

The security-level Top-10 list contained both GOOG and GOOGL in the same month.

These are separate listed share classes of Alphabet Inc. They have separate PERMNO values and different voting rights, but belong to the same economic issuer.

For market-concentration measurement, treating them as separate firms would split Alphabet's economic size across two securities.

### Primary definition revised before hypothesis testing

Primary market concentration is now measured at the PERMCO/company level:

1. aggregate MthCap across all PERMNO share classes belonging to the same PERMCO;
2. calculate company market weights;
3. compute Top-5 share, Top-10 share, and HHI from those company weights.

Security-level PERMNO concentration is retained as a robustness measure.

Signal construction remains at the PERMNO level.

This revision occurred before momentum construction and before any concentration-signal relationship was estimated.


---

## 18 June 2026 — Momentum implementation scaffold

### Primary signal implemented

Added the pre-specified 12–2 momentum signal:

- formation date: month-end t;
- lookback returns: t-12 through t-2;
- month t-1 skipped;
- 11 monthly returns compounded;
- contiguous monthly history required.

### Important timing correction

Signal history and next-month realised returns are sourced from a broader security-level monthly history panel that is cleaned for duplicates and exchange eligibility but is **not** filtered by the formation-date $5 price screen or NYSE-size breakpoint outside month t.

This avoids two biases:

1. losing legitimate lookback returns because a stock failed the investability screen in an earlier month;
2. losing t+1 realised returns because a selected stock failed the formation screen in the following month.

Formation eligibility remains determined by the clean panel at month t.

### New files

- `src/signals.py`
- `notebooks/02_momentum_signal.ipynb`

The momentum notebook stops at construction and sanity checks. No concentration-conditioning test has yet been run.


---

## 1 July 2026 — Momentum signal validated v1 and baseline scaffold

### Manual validation passed

For MARA (PERMNO 14813) at the 2021-05 formation date, the 12–2 momentum signal was manually recomputed from the CRSP monthly returns for 2020-05 through 2021-03.

Manual compounded return:

`105.71119104164512`

This matches the programmatic signal to floating-point precision.

The check also confirmed that CRSP monthly dates are last trading dates rather than necessarily calendar month-ends; month selection for validation should therefore use calendar periods rather than hard-coded month-end dates.

### Baseline evaluation added

New files:

- `src/portfolio.py`
- `notebooks/03_momentum_baseline.ipynb`

The notebook computes:

- monthly Spearman Rank IC;
- value-weighted Q1–Q5 returns;
- value-weighted Q5 minus Q1 spread;
- equal-weighted robustness returns;
- next-month return coverage diagnostics;
- descriptive summary statistics.

Formal HAC/Newey-West t-statistics remain deferred until the lag convention is frozen.

No concentration-conditioning result has yet been estimated.


---

## 2 July 2026 — HAC inference convention locked

Before any concentration-conditioned momentum test, the project fixed the time-series inference convention:

- **Primary:** Newey–West / HAC maximum lag = 6 months
- **Robustness:** Newey–West / HAC maximum lag = 12 months

The lag choice will not be changed in response to whether a coefficient or mean crosses a conventional significance threshold.

New files:

- `src/inference.py`
- `notebooks/04_momentum_inference.ipynb`

The notebook applies the convention to:

- mean monthly Rank IC;
- value-weighted Q5 minus Q1 momentum spread;
- equal-weighted Q5 minus Q1 robustness spread.

No concentration-conditioned inference has yet been run.


---

## 5 July 2026 — Methodology gate before concentration conditioning

A pre-conditioning review identified that market concentration and momentum portfolio eligibility should not use the same denominator universe.

### Revision

Primary concentration will be measured from a broad market-state universe:

- CIZ US ordinary common equities;
- N/A/Q exchanges;
- positive market capitalisation;
- company-level PERMCO aggregation;
- no $5 screen;
- no NYSE 20% size screen.

The stricter $5 and NYSE-size screens remain limited to the momentum formation universe.

### Timing locked

At month-end t:

- concentration is observed at t;
- momentum formation and eligibility are determined at t;
- performance is measured in t+1.

New validation notebook:

- `notebooks/05_market_state_concentration.ipynb`

No concentration-conditioned performance test has been run yet.


---

## 10 July 2026 — Core concentration test specification locked

Primary:
- X = broad-market company-level Top10Share at formation month t;
- Y = value-weighted 12–2 momentum Q5 minus Q1 return realised in t+1;
- beta interpreted per 10 percentage points of Top10Share;
- two-sided HAC6 inference;
- HAC12 robustness.

Secondary / robustness:
- linear time trend;
- HHI;
- equal-weighted spread;
- Rank IC;
- expanding-history concentration regimes using only prior data with 60 months minimum history.

New files:
- src/conditioning.py
- notebooks/06_concentration_conditioning.ipynb


---

## 13 July 2026 — Timing robustness added after core concentration result

Before moving to more complex signal-neutralisation tests, the project adds one targeted timing robustness check.

Primary timing remains:

- concentration measured at formation month-end t;
- momentum portfolio formed at t;
- return realised in t+1.

Robustness timing:

- concentration measured at t-1;
- momentum portfolio still formed at t;
- return realised in t+1.

Purpose:

- remove any concern that the market-state variable is determined at the same month-end close used for portfolio formation;
- verify that the weak concentration result is not an artefact of contemporaneous month-end measurement.

Calendar-month lagging is used rather than exact-date subtraction because CRSP monthly dates are last trading dates.

New notebook:

- `notebooks/07_concentration_timing_robustness.ipynb`


---

## 16 July 2026 — Mega-cap exclusion methodology locked

Before testing composition effects, the project fixes:

- primary exclusion = top 10 PERMCO companies by broad-market market cap at formation month t;
- robustness = top 5 and top 20;
- all share classes of an excluded company are removed;
- momentum signal definition is unchanged;
- quintiles are re-formed after exclusion;
- primary estimand = ExTop10 VW Q5-Q1 minus baseline VW Q5-Q1;
- HAC6 primary / HAC12 robustness.

New files:
- `src/mega_cap.py`
- `notebooks/08_mega_cap_exclusion.ipynb`


---

## 18 July 2026 — Mega-cap mechanism decomposition locked

Before moving to sector or beta neutralisation, the project separates:

1. direct value-weight effect with baseline quintile membership held fixed;
2. re-ranking effect from rebuilding quintiles after mega-cap exclusion.

Primary exclusion remains top 10 PERMCO companies.

The decomposition is exactly additive:
TotalChange = DirectWeightEffect + ReRankingEffect.

Additional diagnostics measure mega-cap weight shares and return contributions inside baseline Q1 and Q5.

New files:
- `src/mega_cap_decomposition.py`
- `notebooks/09_mega_cap_decomposition.ipynb`


---

## 19 July 2026 — Industry-neutral methodology locked

Primary:
- FF49 classification from contemporaneous CRSP SICCD;
- equal-weight monthly industry mean of raw 12-2 momentum;
- minimum 10 valid stocks per industry-month;
- adjusted signal = raw momentum minus industry mean;
- global quintiles re-formed on adjusted signal;
- primary estimand = neutral VW Q5-Q1 minus raw VW Q5-Q1;
- HAC6 primary / HAC12 robustness.

Robustness:
- within-industry percentile signal;
- ICBIndustry classification;
- EW spread;
- Rank IC.

An auditable FF49 SIC-definition file is stored in docs/reference.

New files:
- `src/industry_neutral.py`
- `notebooks/10_industry_neutral_momentum.ipynb`
- `docs/reference/Siccodes49.txt`


---

## 22 July 2026 — Daily beta-input audit scaffold

Before rolling beta estimation, the project validates three daily inputs:
1. CRSP CIZ daily stock returns;
2. CRSP value-weighted daily market total return;
3. Kenneth French daily RF.

The audit checks PERMNO-date uniqueness, missingness, return magnitudes, market/RF date overlap, RF unit conversion, and representative formation-date history availability under the pre-specified 252-day window, 5-day skip, and 126-observation minimum.

New files:
- src/daily_data.py
- notebooks/11_daily_data_audit.ipynb


---

## 23 July 2026 — Daily duplicate resolution and beta methodology lock

The CRSP daily stock extract contained 16,259 rows belonging to 7,837
duplicated PERMNO-date groups. Investigation showed that every duplicated-key
row was an exact full-row duplicate and every group had one unique DlyRet.
There were 8,422 redundant rows beyond the first copy and zero conflicting
daily-return groups. The daily reader now removes exact duplicates only and
fails if any non-identical PERMNO-date duplicate remains.

Ex-ante stock beta methodology was frozen before portfolio results:
- CAPM OLS on daily excess returns;
- CRSP stock total return and CRSP VW market total return;
- Kenneth French daily RF;
- 252 CRSP market trading-day window;
- skip the 5 market trading days immediately before formation;
- minimum 126 valid paired observations;
- fixed CRSP market calendar, not stock-specific observed-day counting;
- no winsorisation, clipping, forward-fill or beta imputation.

Portfolio neutralisation is not yet implemented. Beta estimates must first pass
coverage, distribution and extreme-value diagnostics in
`notebooks/12_beta_estimation.ipynb`.


---

## 25 July 2026 — Ex-ante beta validation passed

The frozen 252/5/126 CAPM beta estimator produced high and stable coverage
across all 312 formation months. Overall valid-beta coverage averaged about
97.9%. Representative-month coverage was approximately 92.3% in 2000-01,
99.0% in 2008-12, 94.6% in 2020-12, and 98.2% in 2025-12. Median valid
observations were 252 in every month.

The overall beta distribution was centred near 1.09 (median) / 1.14 (mean).
A small number of extreme positive and negative estimates were observed,
including estimates below -6 and above 10. These are retained under the
pre-specified no-winsorisation rule; the 252/5/126 specification is not changed
after inspection.

All consistency assertions passed:
- unique PERMNO-month beta keys;
- every non-missing beta satisfies the 126-observation minimum;
- no estimate uses more than 252 market trading days.

The beta estimation gate therefore passes. The next stage keeps original
momentum rankings and quintile membership, separates the beta-coverage effect,
and tests the pre-specified market-overlay beta-neutral construction. Long/short
leg rescaling remains a robustness construction only.


---

## 26 July 2026 — Beta diagnostics closed; project enters final synthesis

Additional diagnostics showed a correlation of approximately 0.05 between
formation-date net momentum beta and next-month market excess return. Sorting
months into market-return quintiles did not reveal a simple monotonic
relationship between ex-ante net beta and subsequent market state.

No additional beta specification is introduced. The beta-neutral chapter is
therefore closed under the pre-specified methodology, and the project moves to
final synthesis rather than further specification expansion.

A working integrated interpretation is now documented in
`docs/final_synthesis.md`.

---

## 28 July 2026 — Beta-neutral diagnostics completed; synthesis stage opened

The beta-neutral portfolio analysis is now complete.

Key findings:
- beta coverage is complete within the realised Q1/Q5 momentum legs, so the beta-coverage effect on the spread is zero;
- average ex-ante Q5-Q1 beta is close to zero but varies materially over time;
- the primary market-overlay hedge lowers average VW momentum performance by roughly 11 bps per month in point estimates;
- the neutralisation effect is statistically imprecise under both HAC6 and HAC12;
- the leg-rescaling robustness construction has the same directional effect;
- the ex-post monthly market beta falls materially after hedging, from roughly -0.38 to roughly -0.16, but is not eliminated;
- correlation between ex-ante net beta and the following holding month's market excess return is about 0.05;
- beta by market-return quintile is non-monotonic, so the ex-ante/ex-post beta gap is not explained by a simple market-state relation.

No further beta specification is added. This avoids post-result specification search.

The project now moves to final synthesis, figures/tables, and research-paper packaging.

---

## 31 July 2026 — Final-review bridge test locked before results

A professor-style final review identified one remaining identification gap:
the mega-cap decomposition establishes a direct portfolio-weight mechanism,
but does not by itself show that the mechanism becomes stronger when aggregate
market concentration is higher.

Before observing bridge-test results, the following specifications are frozen:

1. DirectWeightEffect_t = alpha + beta * Top10Share_t + error_t
2. (Top10Weight_Q5,t - Top10Weight_Q1,t)
   = alpha + gamma * Top10Share_t + error_t

Top10Share is scaled per +10 percentage points. HAC6 is primary and HAC12 is
robustness. A linear time trend with HAC6 is reported as secondary robustness
because concentration is persistent and strongly trending.

No HHI, alternative Top-N threshold, nonlinear transformation, sample split,
or lag search is added in this bridge stage.


---

## 2 August 2026 — Concentration mechanism bridge results

The pre-specified bridge tests distinguish a portfolio-exposure mechanism from
a realised-return effect.

Direct-weight effect:
- coefficient per +10pp Top10Share: +0.001840 per month;
- HAC6 t = 0.772, p = 0.440, 95% CI [-0.002831, 0.006510];
- HAC12 p = 0.316;
- with linear trend, coefficient = +0.002748, p = 0.283.

Thus aggregate concentration does not precisely predict the realised monthly
direct-weight return effect.

Top-10 weight gap (Q5 minus Q1):
- coefficient per +10pp Top10Share: +0.244777;
- HAC6 t = 6.599, p < 1e-10;
- 95% CI [0.172071, 0.317483];
- HAC12 result is essentially unchanged;
- with linear time trend, coefficient remains positive at +0.099303,
  t = 2.512, p = 0.012, 95% CI [0.021837, 0.176770].

Interpretation: higher aggregate concentration is strongly associated with a
larger mega-cap formation-weight imbalance between the winner and loser legs,
even after a linear time trend. However, the realised direct-weight return
effect remains noisy and is not precisely increasing with concentration.
The final paper should distinguish these two statements.

## External benchmark validation locked

Before observing the comparison, the project will validate its realised
momentum series against the Kenneth French US monthly Momentum Factor (Mom).
The project spread is aligned by holding month (formation t -> realised t+1).
Because the portfolio constructions differ, the primary validation criterion is
economically meaningful positive co-movement, not equality of means or a
one-for-one factor beta.


---

## 4 August 2026 — External momentum validation passed

The project momentum implementation was externally validated against the
Kenneth French US monthly Momentum Factor (Mom), aligned by realised holding
month (formation t -> return t+1).

Common sample: 299 monthly observations.

Summary:
- Project VW mean = 0.000746, monthly vol = 0.055643.
- Project EW mean = 0.002457, monthly vol = 0.046319.
- French Mom mean = 0.002021, monthly vol = 0.046342.
- Corr(Project VW, French Mom) = 0.875434.
- Corr(Project EW, French Mom) = 0.916523.

Diagnostic regressions:
- Project VW on French Mom: beta = 1.0511, HAC SE = 0.0742,
  t = 14.18, p < 1e-40, 95% CI [0.9058, 1.1965], R2 = 0.766;
  alpha = -0.001379, p = 0.404.
- Project EW on French Mom: beta = 0.9161, HAC SE = 0.0388,
  t = 23.61, p < 1e-100, 95% CI [0.8400, 0.9921], R2 = 0.840;
  alpha = +0.000606, p = 0.590.

Interpretation: the project's momentum series co-move very strongly with the
established external benchmark despite intentionally different portfolio
construction. The weak project VW mean is therefore not evidence of an obvious
timing or implementation failure. External validation passes.

## CRSP CIZ delisting-return treatment verified from official documentation

The CRSP CIZ cross-reference and database guides state that CIZ MthRet is
constructed from compounded daily returns and that this daily-compounding
treatment also applies to delisting returns. The CIZ field documentation also
notes that monthly return fields can include a delisting return when
appropriate.

Therefore the project's use of CIZ MthRet does not require a separate legacy
DLRET merge to incorporate delisting returns. The final paper should document
this distinction explicitly because legacy CRSP workflows often merge DLRET
separately.
