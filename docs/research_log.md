# Research Log

This log records important research decisions, changes in scope, rejected alternatives, data issues, and next steps.

The purpose is to preserve the evolution of the project and reduce hindsight bias when interpreting later results.

---

## 29 September 2026

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

## 29 September 2026 — Literature Review v0.1

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

## 29 September 2026 — Pre-Analysis Plan v0.1

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

## 29 September 2026 — CRSP CIZ schema confirmation

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

## 29 September 2026 — Monthly Stock File schema confirmation

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

## 29 September 2026 — Delisting Information schema confirmation

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

## 29 September 2026 — Sample-construction protocol v0.1

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

## 29 September 2026 — Monthly production pipeline scaffold

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
