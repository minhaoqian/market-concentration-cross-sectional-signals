# Does Market Concentration Distort Cross-Sectional Equity Signals?

## Project Overview

This repository contains an empirical quantitative-finance research project on whether rising US equity-market concentration distorts the measured performance of cross-sectional momentum strategies.

The first research version deliberately focuses on **12-2 price momentum** rather than testing many signals at once. The objective is to distinguish several possible mechanisms:

1. aggregate market concentration;
2. mega-cap portfolio-weight concentration;
3. industry common-trend exposure;
4. market-beta exposure.

The project is built as a reproducible research workflow rather than a single backtest.

## Main Research Question

> **Does market concentration distort the measured performance of cross-sectional momentum, and if so, is the effect driven by signal ranking or by portfolio implementation?**

## Data

Primary data come from CRSP through WRDS:

- monthly US common-equity data, 2000-2025;
- daily stock returns, 1998-2025;
- CRSP value-weighted daily market return;
- Kenneth French daily risk-free rate.

Licensed raw WRDS data are **not** uploaded to this public repository.

## Primary Sample

At monthly formation date t:

- US common equities on NYSE / AMEX / NASDAQ;
- positive market capitalisation;
- exclude stocks below the monthly NYSE 20th percentile of market capitalisation;
- require month-end price >= $5;
- form portfolios at t and measure realised return in t+1.

Momentum is defined as cumulative return from t-12 through t-2.

A broader market-state universe is used for market-concentration measurement so that concentration itself is not mechanically conditioned on the stricter signal-investment screens.

## Research Design

### Baseline momentum
- 12-2 momentum;
- monthly Spearman Rank IC;
- value-weighted quintiles, Q5-Q1;
- equal-weighted robustness;
- Newey-West HAC lag 6 primary, lag 12 robustness.

### Aggregate concentration
Company-level concentration is constructed after aggregating multiple share classes to PERMCO:
- Top-5 share;
- Top-10 share;
- HHI;
- effective number of firms.

Primary test:
- momentum spread on contemporaneous Top-10 market share, with holding return realised in t+1.

### Mega-cap mechanism
- exclude top 5 / 10 / 20 companies by market capitalisation;
- distinguish total change from:
  - direct portfolio-weight effect;
  - re-ranking effect.

### Industry neutralisation
Primary:
- Fama-French 49 industry mapping from contemporaneous SIC;
- demean raw momentum within industry-month before re-forming global quintiles.

Robustness:
- within-industry percentile rank;
- CRSP ICB industry neutralisation.

### Market-beta neutralisation
Ex-ante CAPM beta:
- CRSP daily stock excess returns;
- CRSP value-weighted market excess return;
- 252 market trading-day window;
- skip the 5 trading days immediately before formation;
- minimum 126 paired observations;
- no beta winsorisation or imputation.

Primary construction:
- preserve original momentum holdings and within-leg value weights;
- hedge the portfolio's estimated net market beta with a market overlay.

## Main Findings So Far

The empirical evidence points toward a portfolio-implementation mechanism rather than a breakdown in momentum ranking ability.

- Baseline value-weighted momentum is positive but weak and statistically imprecise.
- Aggregate market concentration does not show a robust linear relationship with subsequent momentum performance.
- Removing mega-cap firms raises the value-weighted momentum spread in point estimates, while equal-weighted performance and Rank IC change very little.
- A decomposition shows that almost all of the mega-cap exclusion effect comes from **direct portfolio weights**, not re-ranking.
- Industry neutralisation leaves Rank IC almost unchanged and does not improve momentum performance.
- Beta neutralisation reduces realised market exposure and lowers the momentum spread in point estimates, but the return effect remains statistically imprecise.

The current interpretation is therefore:

> rising market concentration appears more relevant to how a value-weighted momentum portfolio is implemented than to whether the underlying cross-sectional ranking contains information.

This conclusion remains subject to final synthesis, figure production, and reporting of limitations.

## Repository Structure

```text
docs/        Research design, sample construction, methodology logs, synthesis
notebooks/   Sequential empirical analysis
src/         Reusable Python research code
data/        Local-only raw/interim/processed data
paper/       Final research note / report
```

## Current Status

Core empirical analysis is approximately **75-80% complete**.

Completed:
- monthly sample construction;
- concentration measures;
- momentum signal validation;
- baseline portfolio and inference;
- concentration conditioning;
- timing robustness;
- mega-cap exclusion and decomposition;
- industry neutralisation;
- daily beta data audit;
- rolling beta estimation;
- primary beta-neutral momentum analysis.

Remaining:
- final synthesis;
- a small set of final robustness checks only if economically justified;
- publication-quality tables and figures;
- final README / research note / CV and interview summary.

## Reproducibility

Every final result should be traceable from licensed source data through documented transformations and code. Methodology changes are recorded in `docs/research_log.md` to reduce hindsight bias and specification search.
