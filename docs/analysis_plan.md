# Pre-Analysis Plan

## Status

**Version 0.1 — written before examining the project's main empirical results.**

This document fixes the primary empirical design as far as possible before the backtest is run. Any later change must be recorded in research_log.md with a reason and labelled as a pre-specified revision, robustness extension, or exploratory analysis.

The purpose is to reduce specification search, hindsight bias, and accidental data mining.

---

# 1. Research Question

## Primary question

> **Does rising concentration in the US equity market alter the effectiveness of common cross-sectional equity signals, and do observed signal returns persist after controlling for sector, market-beta, and mega-cap exposures?**

## Sub-questions

1. Does the cross-sectional predictive ability of each signal vary with aggregate market concentration?
2. Does long-short portfolio performance vary with concentration?
3. Are apparent changes in signal performance explained by sector, beta, or mega-cap exposure?
4. Do raw and neutralised implementations behave differently?
5. Are results robust to alternative signal definitions, concentration measures, portfolio breakpoints, transaction-cost assumptions, and sample periods?

---

# 2. Unit of Analysis and Frequency

## Security level

US-listed common equities.

## Portfolio formation frequency

**Monthly.** At the end of each month t:

1. construct the eligible point-in-time universe using information available by month-end t;
2. calculate each signal using only data dated t or earlier;
3. calculate market concentration at t;
4. form portfolios;
5. measure realised return during month t+1.

This one-period lag is mandatory. No variable observed during t+1 may be used to construct the portfolio held during t+1.

---

# 3. Security Universe

## Primary universe

Subject to confirmation of the exact WRDS/CRSP variable names and Oxford entitlements, the primary universe will consist of:

- CRSP ordinary common shares;
- share codes SHRCD = 10 or 11;
- securities listed on NYSE, AMEX, or NASDAQ;
- exchange codes EXCHCD = 1, 2, or 3;
- observations with a valid month-end price and market capitalisation;
- observations satisfying the minimum history requirements of the relevant signal.

Permanent identifiers such as PERMNO will be used rather than ticker symbols wherever possible.

## Primary liquidity / microcap screen

Exclude stocks below the **20th percentile of NYSE market capitalisation** at each monthly formation date.

Rationale: the NYSE breakpoint reduces the risk that results are dominated by extremely small securities while remaining point-in-time and time-varying.

## Price screen

Require an absolute month-end price of at least **$5** in the primary analysis.

This is a pragmatic liquidity / microstructure screen, not an economic hypothesis.

## Robustness universes

1. no $5 price screen;
2. NYSE market-cap breakpoint at 10%;
3. NYSE market-cap breakpoint at 30%;
4. large-cap-only universe;
5. universe excluding the largest 10 stocks at each formation date.

Any additional universe added after viewing results must be labelled exploratory.

---

# 4. Return Construction

## Stock return

Use CRSP total returns, including distributions, where available.

## Delisting returns

Where CRSP delisting returns are available, incorporate them into realised holding-period returns. The exact combination rule will be documented in sample_construction.md after the relevant CRSP tables and fields are confirmed.

## Market capitalisation

At month-end:

ME(i,t) = |Price(i,t)| × SharesOutstanding(i,t)

The exact CRSP unit conversion will be checked against WRDS metadata before implementation. Portfolio weights must use information dated no later than the formation date.

---

# 5. Primary Signals

The four primary signals are deliberately price-based. All are oriented so that **higher signal values correspond to the side expected to earn higher future returns**.

## 5.1 Momentum

### Economic idea

Intermediate-horizon past winners tend to continue outperforming past losers, while the most recent month is skipped to reduce contamination from very-short-term reversal and microstructure effects.

### Primary definition

For stock i at the end of month t:

**MOM(i,t) = cumulative total return from month t-12 through month t-2.**

Equivalently, compound monthly returns over t-12, ..., t-2.

This is the standard prior 2–12 month convention used in the Kenneth French momentum portfolios.

### Direction

Higher value = stronger momentum.

### Portfolio interpretation

- Long: high momentum
- Short: low momentum

### Robustness definitions

1. a shorter 6–1 style momentum window;
2. a closely related 12–1 date convention;
3. cross-sectionally winsorised momentum.

The primary result remains prior 2–12 month momentum.

## 5.2 Short-Term Reversal

### Economic idea

Very recent winners tend, on average, to underperform very recent losers over the following short horizon.

### Primary definition

**REV(i,t) = -R(i,t)**, where R(i,t) is the stock's total return during the immediately preceding month.

The negative sign makes a prior-month loser receive a high reversal signal and a prior-month winner receive a low reversal signal.

### Direction

Higher value = stronger predicted positive reversal.

### Portfolio interpretation

- Long: prior-month losers
- Short: prior-month winners

### Robustness definitions

1. previous-week / very-short-horizon reversal using daily data;
2. prior-month return residualised by market return;
3. excluding observations associated with extreme corporate-action-related returns.

The main specification remains negative prior-one-month return.

## 5.3 Low Volatility

### Economic idea

Stocks with lower recent realised volatility have often earned unexpectedly strong risk-adjusted returns relative to high-volatility stocks.

### Primary definition

At the end of month t, calculate the standard deviation of daily stock returns over the **previous 21 trading days**.

VOL(i,t) = standard deviation of daily returns over the previous 21 trading days.

Define **LOWVOL(i,t) = -VOL(i,t)** so higher signal values represent lower volatility.

Annualisation is not needed for ranking. If volatility levels are displayed, daily volatility may be multiplied by sqrt(252).

### Minimum observations

Require at least **15 valid daily returns** in the 21-trading-day window.

### Portfolio interpretation

- Long: low-volatility stocks
- Short: high-volatility stocks

### Why total volatility is primary

The project already studies beta separately and later applies exposure controls. Total realised volatility therefore provides a transparent, model-light primary signal.

### Robustness definitions

1. 63-trading-day realised volatility;
2. 126-trading-day realised volatility;
3. idiosyncratic volatility estimated from daily residuals relative to a factor model.

Idiosyncratic volatility is a robustness extension rather than the primary signal.

## 5.4 Low Beta

### Economic idea

Low-beta stocks have historically exhibited stronger risk-adjusted returns than predicted by the standard CAPM relation in a substantial literature.

### Primary beta estimator

At each month-end t, estimate a conventional rolling market-model beta from daily returns over the previous **252 trading days**:

R(i,d) - Rf(d) = alpha(i) + beta(i,t) × [Rm(d) - Rf(d)] + epsilon(i,d).

Define **LOWBETA(i,t) = -beta(i,t)** so higher signal values correspond to lower estimated beta.

### Minimum observations

Require at least **126 valid overlapping daily observations** during the 252-trading-day window.

### Market and risk-free series

Use a broad US equity-market return and a consistent daily risk-free rate from an authoritative WRDS/Fama-French source.

### Portfolio interpretation

- Long: low-beta stocks
- Short: high-beta stocks

### Why not use the Frazzini–Pedersen estimator as primary

Frazzini and Pedersen use a specialised estimator combining a longer-window correlation estimate with a shorter-window volatility estimate. A conventional rolling regression beta is easier to interpret and makes fewer specialised assumptions for the primary specification.

### Robustness definitions

1. Frazzini–Pedersen-style beta estimator;
2. 504-trading-day rolling CAPM beta;
3. shrinkage beta toward one / the cross-sectional mean.

---

# 6. Cross-Sectional Standardisation

At each monthly formation date, signals will be ranked within the eligible cross-section.

The primary analysis will use ranks and quantile assignments rather than raw signal magnitudes because the signals have different units and raw-score weighting can be dominated by extreme observations.

No future-period information may be used in ranking.

---

# 7. Primary Portfolio Construction

## Quantiles

Primary portfolios use **quintiles**.

- Q1 = bottom 20% of signal rank;
- Q5 = top 20% of signal rank.

Because all signals are oriented so that higher values mean higher predicted future return:

**Long-short return = Return(Q5) - Return(Q1).**

## Weighting

Primary: **value-weighted** within each signal portfolio using lagged month-end market capitalisation.

Secondary robustness: **equal-weighted**.

Value weighting reduces mechanical microcap dominance and is closer to an institutional implementation; equal weighting shows whether results rely on smaller firms.

## Rebalancing and holding period

- Rebalance monthly.
- Hold for one month.

---

# 8. Signal-Level Predictive Metric

The primary signal-level statistic is the monthly **Spearman rank information coefficient (Rank IC)**:

IC(t) = SpearmanCorr(signal(i,t), return(i,t+1)).

For each signal report:

- mean IC;
- median IC;
- standard deviation of IC;
- fraction of positive IC months;
- t-statistic of mean IC with an appropriate time-series standard error.

This separates genuine cross-sectional ranking ability from portfolio-construction effects.

---

# 9. Market Concentration Measures

Concentration is measured from the point-in-time market-cap distribution.

## 9.1 Primary measure: Top-10 market-cap share

TOP10(t) = sum of market-cap weights of the 10 largest eligible stocks.

This is intuitive and directly measures mega-cap dominance.

## 9.2 Co-primary measure: HHI

HHI(t) = sum over i of w(i,t)^2, where w(i,t) is stock i's share of aggregate market capitalisation.

HHI uses the whole weight distribution.

## 9.3 Secondary measure

Top-5 market-cap share.

## Interpretation rule

Concentration is a **conditioning variable**, not a direct alpha or market-timing signal.

---

# 10. Concentration Conditioning Tests

## 10.1 Continuous specification — primary

For a monthly signal-performance outcome Y(t):

Y(t) = a + b × Concentration(t) + error(t).

Y(t) may be Rank IC, long-short return, turnover, or an exposure measure.

The sign and statistical significance of b are empirical results; no direction is assumed.

## 10.2 Regime summaries — secondary

For interpretation, concentration may also be split using historical distribution-based terciles:

- Low concentration;
- Medium concentration;
- High concentration.

The continuous test is primary because thresholding discards information.

No cutoff may be chosen after visually searching for the strongest result.

---

# 11. Exposure Diagnostics

For each signal portfolio measure at least:

- market beta;
- sector weights;
- largest-stock exposure;
- top-10 stock exposure;
- portfolio concentration;
- average and median market capitalisation;
- turnover.

This allows us to distinguish a true change in cross-sectional ranking from a change caused by portfolio composition or common exposures.

---

# 12. Neutralisation Tests

Neutralisation is part of the research question, not just data cleaning.

## 12.1 Raw signal

Baseline with no sector or beta neutralisation beyond the universe screens.

## 12.2 Sector-neutral implementation

Compare stocks within sectors or remove sector-level signal means before ranking. The exact implementation will be locked before the primary neutralised result is run.

## 12.3 Beta-neutral portfolio

Construct the long-short portfolio so ex-ante market beta is approximately zero, or hedge the signal portfolio with the market portfolio. The exact primary technique will be locked before the main test.

## 12.4 Mega-cap control

Primary diagnostic: explicitly measure top-10 exposure.

Primary robustness treatment: rerun the analysis excluding the 10 largest stocks at each point in time.

This is preferable to permanently excluding a modern named list of mega-cap firms.

## Interpretation

If neutralisation reduces return, this will not automatically be treated as failure. It may be removing unwanted risk, genuine expected-return exposure, or both.

---

# 13. Transaction Costs and Turnover

Calculate one-way turnover from monthly changes in portfolio weights.

A fixed transaction-cost assumption is not yet locked. Before inspecting net profitability, specify a base cost level plus at least one lower- and one higher-cost scenario.

Net return = gross return - estimated transaction cost.

The exact two-sided turnover convention will be documented before cost-adjusted results are interpreted.

---

# 14. Statistical Inference

## Time-series mean returns and IC

Use heteroskedasticity- and autocorrelation-consistent standard errors where appropriate. The primary Newey-West/HAC lag is fixed at **6 months**, with **12 months** reported as a robustness specification. This convention is fixed before concentration-conditioned results are estimated.

## Cross-sectional regressions

If Fama-MacBeth regressions are added, the regression specification, characteristic scaling, controls, and standard-error treatment will be pre-specified first.

## Multiple testing

The four signals and multiple concentration measures create a multiple-testing problem.

Results will therefore be separated into:

- primary hypotheses;
- robustness tests;
- exploratory tests.

No isolated p-value will be treated as decisive evidence without considering the wider family of tests.

---

# 15. Primary Outcomes

For each signal report:

## Predictive ability

- mean monthly Rank IC;
- IC t-statistic;
- proportion of positive IC months.

## Portfolio performance

- annualised mean return;
- annualised volatility;
- Sharpe ratio;
- maximum drawdown;
- turnover;
- transaction-cost-adjusted return.

## Exposure

- market beta;
- sector concentration;
- top-10 exposure;
- average market capitalisation.

## Concentration sensitivity

- continuous concentration coefficient;
- low/medium/high concentration summary;
- raw versus neutralised comparison.

---

# 16. Robustness Tests

## Signal robustness

- alternative momentum window;
- alternative reversal horizon;
- 3- and 6-month volatility windows;
- idiosyncratic volatility;
- alternative beta window / estimator.

## Portfolio robustness

- deciles instead of quintiles;
- equal weighting;
- alternative microcap screens;
- mega-cap exclusion.

## Concentration robustness

- Top-5 share;
- Top-10 share;
- HHI;
- alternative regime thresholds.

## Time robustness

- pre-/post-GFC;
- pre-/post-COVID;
- recent mega-cap concentration period;
- rolling-window estimates.

Subperiods are robustness analyses, not breakpoints to be selected for dramatic results.

## Falsification / placebo ideas

- permute signal ranks within month;
- randomly assign concentration states in a way that preserves the relevant time-series structure where feasible;
- test whether relationships survive removal of the largest securities.

The exact placebo design will be fixed before implementation.

---

# 17. Sample Period

The preferred research sample is **2000–2026** if all required fields are consistently available.

This period is long enough to contain multiple market environments while remaining focused on the modern US equity market.

If required daily-history fields or data quality make a 2000 start infeasible, the start date may be moved forward **before main results are examined**, with the reason recorded in research_log.md.

The end month will be the latest complete month available when the production dataset is frozen.

---

# 18. Data Freeze and Reproducibility

When the first production dataset is downloaded:

1. record download date;
2. record WRDS library and table names;
3. record variable names;
4. record query logic;
5. record sample date range;
6. save an immutable local raw copy;
7. never overwrite the raw copy;
8. never upload licensed WRDS raw data to the public GitHub repository.

Public GitHub will contain code where licensing permits, documentation, aggregate tables, figures, research logs, and the final report.

---

# 19. Decision Rules for Changes

A primary definition may change only if:

1. a required data field is unavailable;
2. the definition is found to be inconsistent with the cited literature;
3. implementation would create a mechanical error or look-ahead bias;
4. a genuine data-quality issue makes the specification infeasible.

A weak, insignificant, or economically unattractive result is **not** a valid reason to redefine the primary specification.

---

# 20. Next Actions Before Version 1.0

1. confirm CRSP daily and monthly access in WRDS;
2. confirm access to market and risk-free factor data;
3. create data_dictionary.md;
4. create sample_construction.md;
5. verify exact CRSP variable units and delisting-return handling;
6. lock the sector-neutralisation implementation;
7. lock the beta-neutralisation implementation;
8. set transaction-cost scenarios;
9. define the Newey-West lag rule;
10. freeze this plan as Version 1.0.

Only after these steps should the main empirical results be generated.

---

## Concentration-conditioning hierarchy

Primary hypothesis test:
- outcome: value-weighted 12–2 momentum Q5 minus Q1 next-month return;
- concentration: company-level Top-10 market-cap share from the broad market-state universe at formation month-end t;
- model: VW momentum spread on Top10Share;
- Top10Share coefficient reported per 10 percentage points;
- two-sided HAC6 inference;
- HAC12 robustness.

Pre-specified robustness / secondary analyses:
- linear time trend;
- HHI;
- equal-weighted spread;
- monthly Rank IC;
- Low/Medium/High concentration states using expanding historical tertiles.

Regime thresholds at month t use only concentration observations through t-1 and require at least 60 months of prior history.


---

## Mega-cap composition test

This stage is locked before results are viewed.

### Primary

- rank companies monthly by broad-market PERMCO market capitalisation;
- exclude all securities belonging to the top 10 PERMCO companies from the momentum formation universe;
- keep the 12–2 momentum signal definition unchanged;
- recompute quintiles after exclusion;
- compare value-weighted Q5 minus Q1 with the baseline.

Primary estimand:

```text
Delta_t = Spread_ExTop10_t - Spread_Baseline_t
```

Inference:
- HAC6 primary;
- HAC12 robustness.

### Pre-specified robustness

- exclude top 5 PERMCO companies;
- exclude top 20 PERMCO companies;
- compare equal-weighted spread;
- compare Rank IC.

Top-N membership is always determined from the broad market-state universe at formation month t.


---

## Mega-cap mechanism decomposition

Before sector or beta neutralisation, the Top-10 exclusion result is decomposed into two components.

### Fixed-rank counterfactual

Hold baseline momentum quintile membership fixed, remove securities belonging to the top-10 PERMCO companies, and re-normalise value weights inside each original quintile.

This isolates the direct portfolio-weight effect.

### Re-formed counterfactual

Remove the same top-10 PERMCO companies before portfolio formation and recompute quintile membership.

### Exact decomposition

```text
TotalChange = ReformedSpread - BaselineSpread
DirectWeightEffect = FixedRanksSpread - BaselineSpread
ReRankingEffect = ReformedSpread - FixedRanksSpread

TotalChange = DirectWeightEffect + ReRankingEffect
```

HAC6 is primary and HAC12 is robustness for each component mean.

Additional diagnostics report top-10 formation-weight share and realised-return contribution inside the baseline Q1 and Q5 legs.


---

## Industry-neutral momentum test

This stage is fixed before results are inspected.

### Primary industry definition

Fama-French 49 industries, mapped from contemporaneous CRSP `SICCD`.

The repository stores an auditable copy of the published SIC-range definition file at:

`docs/reference/Siccodes49.txt`

### Primary neutral signal

For stock i in industry g at formation month t:

```text
IndustryMeanMomentum(g,t) = equal-weight mean of raw 12-2 momentum in industry g
IndustryNeutralMomentum(i,t) = RawMomentum(i,t) - IndustryMeanMomentum(g,t)
```

Industry-months require at least 10 valid momentum observations.

Global Q1-Q5 portfolios are then re-formed using the adjusted signal.

### Primary estimand

```text
Delta_t = VW_Spread_IndustryNeutral_t - VW_Spread_Raw_t
```

Inference:
- HAC6 primary;
- HAC12 robustness.

### Pre-specified robustness

- within-industry percentile-rank signal;
- CRSP ICBIndustry broad classification;
- equal-weighted spread;
- Rank IC.

Mega-cap exclusion is not combined with industry neutralisation at this stage.
