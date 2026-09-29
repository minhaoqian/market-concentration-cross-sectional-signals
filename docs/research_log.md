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