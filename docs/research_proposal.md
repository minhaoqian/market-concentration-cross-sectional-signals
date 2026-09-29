# Research Proposal

## Working Title

**Does Market Concentration Distort Cross-Sectional Equity Signals?**

## 1. Motivation

US equity-market returns can become concentrated in a relatively small number of very large firms. When this happens, measured performance of systematic equity signals may partly reflect exposure to dominant stocks, sectors, or common market risk rather than broad cross-sectional predictability.

This project will investigate whether the behaviour of common cross-sectional signals changes as market concentration rises, and whether any apparent signal performance remains after controlling for exposures that may mechanically arise in a concentrated market.

The project is deliberately framed as an empirical question rather than as an assumption that concentration must weaken or strengthen factor performance.

## 2. Main Research Question

**Does rising concentration in the US equity market alter the effectiveness of common cross-sectional equity signals, and do observed signal returns persist after controlling for sector, market-beta, and mega-cap exposures?**

## 3. Sub-Questions

1. Does cross-sectional signal performance differ between high- and low-concentration market environments?
2. Are changes visible in both portfolio returns and cross-sectional predictive measures such as information coefficients?
3. To what extent are measured signal returns associated with mega-cap, sector, or market-beta exposure?
4. Do sector-neutral or beta-neutral implementations behave more consistently across concentration regimes?
5. Are any findings robust to alternative definitions of concentration, signal construction, portfolio formation, transaction costs, and sample periods?

## 4. Initial Hypotheses

These hypotheses are provisional and should be finalised before examining the main results.

### H1
Cross-sectional signal performance differs materially between high- and low-concentration market environments.

### H2
A non-trivial portion of observed signal performance during highly concentrated periods is associated with mega-cap, sector, or market-beta exposure.

### H3
Neutralised implementations may reduce exposure-driven variation in performance, although they may also reduce raw returns.

The hypotheses are testable statements, not conclusions. Null or contradictory findings are valid research outcomes.

## 5. Initial Signal Set

The first version of the project will prioritise price-based signals to keep the initial data pipeline transparent:

- Momentum
- Short-term reversal
- Low volatility
- Beta

Fundamental signals such as value or quality may be added only after the price-based research pipeline is validated.

## 6. Candidate Concentration Measures

Primary and secondary measures will be pre-specified before the main empirical tests. Candidates include:

- Top-10 market-cap share
- Top-5 market-cap share
- Herfindahl-Hirschman Index (HHI) based on market-cap weights

The analysis should avoid choosing a concentration measure solely because it produces the strongest result.

## 7. Proposed Empirical Workflow

1. Define a point-in-time US equity universe.
2. Construct clean return, market-cap, and exposure data.
3. Build each cross-sectional signal using only information available at portfolio-formation time.
4. Form baseline portfolios and calculate cross-sectional predictive statistics.
5. Measure market concentration through time.
6. Compare signal behaviour across concentration states and continuously through interaction/regression tests.
7. Apply sector, beta, and selected mega-cap controls.
8. Incorporate realistic transaction-cost assumptions.
9. Conduct robustness and falsification tests.
10. Document limitations and alternative explanations.

## 8. Data Requirements

The preferred source is WRDS, depending on available Oxford subscriptions.

Potential required fields include:

- Permanent security identifier
- Date
- Security type / exchange information
- Price
- Returns
- Shares outstanding
- Delisting returns where available
- Market-cap inputs
- Industry / sector classification
- Benchmark or market return
- Additional reference fields required for sample construction

A separate data dictionary and sample-construction document will record exact field definitions once database entitlements are confirmed.

## 9. Key Research Risks

The design must explicitly address:

- Survivorship bias
- Look-ahead bias
- Delisting bias
- Corporate-action handling
- Ticker and identifier changes
- Missing and stale observations
- Microcap and illiquidity effects
- Transaction costs and turnover
- Multiple testing
- Specification search / data mining
- Regime definition sensitivity
- Structural change over time

## 10. Contribution

The intended contribution is not to claim that equity factors or market concentration are new topics. The project instead asks whether concentration changes how familiar cross-sectional signals should be interpreted, especially once common exposure channels are controlled for.

The final contribution statement will be refined after a systematic literature review establishes what has already been studied and which part of the question remains genuinely open.

## 11. Next Steps

1. Conduct a structured literature review.
2. Confirm WRDS database entitlements and exact usable datasets.
3. Finalise the security universe and sample period.
4. Finalise the primary concentration measure.
5. Finalise signal definitions before viewing main results.
6. Write a pre-analysis plan.
