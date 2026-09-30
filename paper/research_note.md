# Does Market Concentration Distort Cross-Sectional Equity Signals?
## Momentum, Mega-Cap Exposure, and Portfolio Implementation in US Equities, 2000–2025

### Abstract

This paper studies whether rising concentration in the US equity market distorts the measured performance of cross-sectional momentum strategies, and whether any distortion reflects deterioration in signal quality or changes in portfolio implementation. Using CRSP monthly US common-equity data from 2000 through 2025, the analysis constructs a standard 12–2 momentum signal, evaluates value-weighted and equal-weighted quintile portfolios, measures market concentration at the company level, and then applies a sequence of mechanism tests involving mega-cap exclusion, industry neutralisation, and market-beta neutralisation.

The unconditional momentum signal is weak in this sample. Mean monthly Rank IC is 0.00768, while the value-weighted Q5–Q1 spread averages 0.0746% per month and is statistically indistinguishable from zero under the pre-specified Newey-West inference rule. Aggregate market concentration, measured by Top-10 market-cap share or HHI, does not robustly predict subsequent momentum performance. By contrast, excluding the ten largest companies raises the value-weighted momentum spread by approximately 0.110 percentage points per month. A decomposition shows that essentially the entire effect is due to direct portfolio weights rather than re-ranking: the direct weight effect is +0.111 percentage points per month, while the re-ranking effect is approximately zero.

Industry neutralisation leaves Rank IC almost unchanged, and market-beta neutralisation materially reduces realised market exposure but does not reveal a statistically robust hidden momentum premium. The combined evidence therefore points toward a portfolio-implementation channel: rising market concentration matters more for how a value-weighted cross-sectional strategy is implemented than for whether the underlying momentum ranking contains information.

---

## 1. Introduction

US equity-market concentration has increased substantially in recent years. A relatively small number of very large companies now account for an unusually large fraction of total listed-market capitalisation. This change raises an important question for quantitative equity research: when the market becomes more concentrated, do traditional cross-sectional signals become less informative, or do their realised portfolio returns simply become more sensitive to a handful of dominant firms?

That distinction matters. A cross-sectional signal can remain informative at the security-ranking level while a value-weighted implementation becomes economically dominated by a small number of mega-cap companies. In that case, weaker realised long-short returns need not indicate that the underlying signal has disappeared. Instead, the mapping from signal ranks to portfolio weights may have changed.

This project focuses on momentum because it provides a clean setting in which to separate these channels. The central question is:

> **Does rising US equity-market concentration distort the measured performance of cross-sectional momentum, and if so, is the effect driven by signal ranking or by portfolio implementation?**

The empirical design deliberately distinguishes three layers.

First, **signal quality** is measured using cross-sectional Rank IC and quintile ordering. If market concentration genuinely destroys momentum information, one would expect the relation between past-return ranks and future-return ranks to deteriorate.

Second, **portfolio implementation** is studied through value-weighted versus equal-weighted returns and direct mega-cap exclusion. If concentration mainly affects portfolio construction, value-weighted returns should change more than equal-weighted returns or Rank IC.

Third, **systematic exposures** are examined through industry neutralisation and ex-ante market-beta neutralisation. These tests evaluate whether apparent momentum performance is largely an artifact of industry common trends or time-varying market exposure.

The results do not support a simple story in which higher aggregate market concentration systematically destroys momentum. The baseline momentum signal is already weak in this 2000–2025 sample, and aggregate concentration measures do not robustly predict subsequent momentum performance. However, mega-cap exclusion materially changes value-weighted momentum returns while leaving Rank IC and equal-weighted results almost unchanged. A direct decomposition shows that this effect is almost entirely attributable to portfolio weights rather than re-ranking.

The strongest empirical conclusion is therefore not that concentration changes the informational content of momentum, but that concentration changes the economic implementation of a value-weighted momentum portfolio.

---

## 2. Data

### 2.1 Monthly equity data

The primary sample is built from CRSP monthly US equity data obtained through WRDS. The research window is January 2000 through December 2025.

The monthly production sample contains:

- 601,350 formation-date observations;
- 7,423 unique PERMNO securities;
- 312 formation months.

The investable sample is restricted to US common equities listed on NYSE, AMEX, or NASDAQ, with positive market capitalisation. At each monthly formation date, stocks below the 20th percentile of NYSE market capitalisation are excluded. A $5 minimum month-end price screen is also imposed.

These screens are applied only at the formation date. Historical returns used to construct momentum, and next-month returns used to evaluate portfolio performance, are obtained from a broader monthly history panel so that a stock does not lose valid lookback or outcome data merely because it fails a formation screen in another month.

### 2.2 Market-state universe

Market concentration is not measured on the stricter signal-investment universe. Instead, a broader market-state universe is used. This universe applies the US common-equity and major-exchange restrictions and requires positive market capitalisation, but it does not apply the $5 price screen or the monthly NYSE 20th-percentile size screen.

This distinction is important. If the same investability restrictions were used to measure market concentration, the market-state variable would be mechanically conditioned on the portfolio construction rule. Measuring concentration on a broader state universe reduces this concern.

### 2.3 Company-level aggregation

Market concentration is measured at the economic-company level rather than the listed-security level. Multiple share classes belonging to the same PERMCO are aggregated before calculating Top-N concentration and HHI.

This matters for firms such as Alphabet, where GOOG and GOOGL are distinct securities but represent claims on the same economic company. Treating those share classes as separate firms would mechanically overstate the number of large companies and understate true company-level concentration.

### 2.4 Daily data for beta estimation

Daily beta estimation uses:

- CRSP daily stock total returns;
- CRSP value-weighted market return including dividends;
- Kenneth French daily risk-free rate.

The daily stock extract covers December 1998 through December 2025. The daily market and risk-free series align exactly on 6,813 trading dates.

The daily stock file initially contains exact duplicate observations. A dedicated audit identifies 16,259 rows belonging to 7,837 duplicated PERMNO-date groups. Every duplicated-key group has identical values across all downloaded fields, including identical daily returns. There are 8,422 redundant rows beyond the first copy and zero conflicting daily-return groups. Exact duplicates are therefore removed before beta estimation.

---

## 3. Momentum Signal and Portfolio Construction

### 3.1 Signal definition

The primary signal is standard 12–2 momentum:

[
MOM_{i,t}
=
prod_{s=t-12}^{t-2}(1+R_{i,s})-1.
]

The construction uses eleven monthly total returns, from month (t-12) through month (t-2), and skips month (t-1).

A signal is accepted only when the relevant monthly history is contiguous in calendar time. This prevents a rolling row window from accidentally spanning missing months.

Across the full sample, 544,090 valid momentum observations are formed.

### 3.2 Portfolio formation

At each formation month (t):

1. stocks are ranked by momentum;
2. five cross-sectional quintiles are formed;
3. Q5 contains the strongest past winners;
4. Q1 contains the weakest momentum stocks;
5. performance is measured using realised return in calendar month (t+1).

The primary portfolio is value weighted using formation-month market capitalisation. Equal-weighted portfolios are retained as a robustness comparison.

Missing next-month returns are never replaced with zero. Portfolio returns are computed over stocks with observed next-month returns, with value weights renormalised over the observed-return subset.

### 3.3 Cross-sectional diagnostic

In addition to portfolio returns, monthly Spearman Rank IC is calculated between momentum and next-month return. Rank IC is useful because it isolates cross-sectional ranking information from portfolio weighting.

---

## 4. Inference

All primary monthly time-series mean tests use the same pre-specified inference rule:

- Newey-West HAC lag 6 months: primary;
- Newey-West HAC lag 12 months: robustness;
- two-sided tests;
- 95% confidence intervals.

This rule was fixed before the concentration and neutralisation results were examined. The purpose is to reduce the risk of choosing a standard-error specification after seeing which one produces statistical significance.

---

## 5. Baseline Momentum Results

The average monthly number of investable stocks is 1,927, with a median of 1,843.

### 5.1 Rank IC

The mean monthly Rank IC is:

[
0.00768.
]

There are 299 months with valid Rank IC.

Under HAC6:

- mean: 0.00768;
- HAC standard error: 0.00803;
- t-statistic: 0.957;
- p-value: 0.339;
- 95% CI: ([-0.00806, 0.02341]).

Under HAC12, the p-value is 0.349.

The point estimate is positive but statistically imprecise.

### 5.2 Value-weighted spread

The value-weighted Q5–Q1 spread averages:

[
0.000746
]

per month, or approximately:

[
0.0746%
]

per month.

Under HAC6:

- HAC standard error: 0.00329;
- t-statistic: 0.227;
- p-value: 0.821;
- 95% CI: ([-0.5703%, 0.7194%]) per month.

Under HAC12, the p-value is 0.807.

### 5.3 Equal-weighted spread

The equal-weighted Q5–Q1 spread averages:

[
0.002457,
]

or approximately:

[
0.2457%
]

per month.

Under HAC6:

- t-statistic: 0.870;
- p-value: 0.384.

Under HAC12:

- p-value: 0.407.

### 5.4 Baseline interpretation

The equal-weighted spread is more than three times the value-weighted spread in point estimates, but neither is statistically distinguishable from zero under the fixed inference rule.

This is important for the interpretation of later tests. The paper is not explaining the disappearance of a large unconditional momentum premium. Instead, it is examining how concentration and systematic exposures alter an already weak value-weighted implementation.

---

## 6. Market Concentration

### 6.1 Concentration measures

Company-level concentration is measured using:

- Top-5 market-cap share;
- Top-10 market-cap share;
- Herfindahl-Hirschman Index (HHI);
- effective number of firms, (1/HHI).

The Top-10 company share declines from roughly 19–20% in the early 2000s to around 15% in the mid-2010s, then rises sharply after 2018. By end-2025, the Top-10 share is approximately 37%.

This change is economically large and motivates the central question of the paper.

### 6.2 Primary concentration regression

The primary specification is:

[
Spread_{t+1}
=
alpha
+
eta Top10Share_t
+
epsilon_{t+1}.
]

Top-10 share is scaled so that the coefficient corresponds to a 10-percentage-point increase in concentration.

The estimated coefficient is:

[
-0.003275.
]

Thus, a 10-percentage-point increase in Top-10 market share is associated with a point estimate of approximately:

[
-0.3275%
]

in the subsequent monthly value-weighted momentum spread.

However, the estimate is imprecise:

- HAC SE: 0.005286;
- t-statistic: -0.620;
- p-value: 0.536;
- 95% CI: ([-1.3636%, 0.7086%]).

### 6.3 Time-trend robustness

Adding a linear time trend reduces the Top-10 coefficient in magnitude:

[
-0.001617.
]

The p-value rises to 0.799.

This indicates that the negative primary coefficient is not robust to controlling for the strong secular time trend in concentration.

### 6.4 HHI robustness

Using HHI instead of Top-10 share produces:

[
-0.006091
]

per 0.01 increase in HHI, with:

- t-statistic: -0.723;
- p-value: 0.470.

Again, the estimate is negative but statistically imprecise.

### 6.5 Equal-weighted and Rank-IC outcomes

When the outcome is the equal-weighted spread, the Top-10 coefficient changes sign:

[
+0.003260,
]

with p-value 0.409.

When the outcome is Rank IC, the coefficient is:

[
+0.006309,
]

with p-value 0.613.

The lack of a common sign across value-weighted, equal-weighted, and Rank-IC outcomes weakens a simple interpretation in which higher concentration uniformly reduces momentum effectiveness.

### 6.6 Lagged concentration

Using concentration from the prior month gives a value-weighted coefficient of:

[
-0.003030,
]

with p-value 0.582.

The timing robustness therefore does not materially change the conclusion.

### 6.7 Concentration interpretation

The aggregate regressions do not provide robust evidence that market concentration linearly predicts subsequent momentum performance.

This does not imply that concentration is irrelevant. Rather, it suggests that the mechanism may operate through portfolio composition and weights rather than through a smooth aggregate state variable.

---

## 7. Mega-Cap Exclusion

### 7.1 Motivation

A value-weighted portfolio can be heavily influenced by a small number of firms even if the cross-sectional signal itself remains unchanged. To test this mechanism directly, the largest firms are removed from the formation universe before momentum quintiles are re-formed.

Mega-cap firms are identified at the PERMCO company level using the broad market-state universe.

### 7.2 Excluding the top five companies

Excluding the top five companies increases the mean value-weighted spread to:

[
0.001375,
]

or 0.1375% per month.

Relative to baseline, the difference is:

[
+0.000629,
]

or approximately +0.0629 percentage points per month.

HAC6 p-value: 0.357.

### 7.3 Excluding the top ten companies

The primary mega-cap test excludes the ten largest companies.

The resulting mean spread is:

[
0.001844,
]

or approximately:

[
0.1844%
]

per month.

The difference from baseline is:

[
+0.001099,
]

or approximately:

[
+0.1099
]

percentage points per month.

Inference:

- HAC6 t-statistic: 1.105;
- HAC6 p-value: 0.269;
- HAC12 p-value: 0.250.

The point estimate is economically meaningful but statistically imprecise.

### 7.4 Excluding the top twenty companies

Excluding the top twenty companies increases the spread further to:

[
0.002456,
]

or 0.2456% per month.

The difference from baseline is:

[
+0.001711,
]

or +0.1711 percentage points per month.

Inference:

- HAC6 t-statistic: 1.574;
- HAC6 p-value: 0.116;
- HAC12 p-value: 0.092.

The increasingly positive point estimates from Top-5 to Top-20 exclusion are economically suggestive, but this ordering is treated as descriptive rather than used to promote Top-20 as a new primary specification after observing the p-values.

### 7.5 Interpretation

Mega-cap exclusion changes the value-weighted implementation materially. The next question is whether this happens because the exclusion changes momentum rankings and quintile boundaries, or because the removed firms carry large portfolio weights.

---

## 8. Mega-Cap Decomposition

### 8.1 Decomposition design

The total effect of mega-cap exclusion is decomposed into two parts.

First, construct a **fixed-rank exclusion** portfolio:

- preserve the original baseline quintile membership;
- remove securities belonging to the Top-10 companies within those original quintiles;
- renormalise the remaining value weights.

Second, compare that portfolio with the fully re-formed ex-Top10 portfolio.

The identity is:

[
TotalChange
=
DirectWeightEffect
+
ReRankingEffect.
]

where:

[
DirectWeightEffect
=
FixedRanks-Baseline,
]

and:

[
ReRankingEffect
=
Reformed-FixedRanks.
]

### 8.2 Direct weight effect

The mean direct weight effect is:

[
+0.001114,
]

or approximately:

[
+0.1114
]

percentage points per month.

Inference:

- HAC6 t-statistic: 1.129;
- HAC6 p-value: 0.259;
- HAC12 p-value: 0.242.

### 8.3 Re-ranking effect

The mean re-ranking effect is:

[
-0.000016,
]

or approximately:

[
-0.0016
]

percentage points per month.

Inference:

- HAC6 t-statistic: -0.169;
- HAC6 p-value: 0.866;
- HAC12 p-value: 0.866.

This effect is economically negligible.

### 8.4 Total effect

The total ex-Top10 change is:

[
+0.001099,
]

matching the exclusion experiment.

Inference:

- HAC6 t-statistic: 1.105;
- HAC6 p-value: 0.269;
- HAC12 p-value: 0.250.

### 8.5 Leg-level mega-cap weights

Within the original baseline quintiles, Top-10 companies account on average for:

- Q1 formation weight share: 9.95%;
- Q5 formation weight share: 17.66%.

The corresponding median weight shares are:

- Q1: 8.26%;
- Q5: 15.87%.

Thus, mega-cap firms receive substantially more weight in the winner portfolio than in the loser portfolio on average.

Their mean return contribution is:

- Q1: 0.1537 percentage points per month;
- Q5: 0.2195 percentage points per month.

The difference is economically meaningful but highly variable over time.

### 8.6 Decomposition interpretation

This is the clearest mechanism result in the paper.

Almost the entire Top-10 exclusion effect comes from direct changes in value weights:

[
0.1114%quad 	ext{direct weight effect}
]

versus approximately:

[
-0.0016%quad 	ext{re-ranking effect}.
]

The implication is that mega-cap concentration changes the realised performance of a value-weighted momentum portfolio without materially changing the underlying signal ordering.

This distinction is central to the paper's thesis.

---

## 9. Industry Neutralisation

### 9.1 Methodology

Stocks are mapped to contemporaneous Fama-French 49 industries using SIC codes.

For each industry-month, the equal-weighted mean raw momentum signal is calculated. The industry-neutral signal is:

[
MOM^{IN}_{i,t}
=
MOM_{i,t}
-
overline{MOM}_{g,t}.
]

Industries require at least ten valid stocks in the month.

Global quintiles are then re-formed using the neutralised signal.

### 9.2 Value-weighted result

The raw value-weighted spread is:

[
+0.000746.
]

The FF49-neutral spread is:

[
-0.000255.
]

The difference is:

[
-0.001001,
]

or approximately:

[
-0.1001
]

percentage points per month.

Inference:

- HAC6 t-statistic: -0.547;
- HAC6 p-value: 0.585;
- HAC12 p-value: 0.594.

### 9.3 Rank IC

Raw Rank IC:

[
0.007680.
]

Industry-neutral Rank IC:

[
0.007625.
]

Difference:

[
-0.000054.
]

Inference:

- HAC6 t-statistic: -0.017;
- HAC6 p-value: 0.986;
- HAC12 p-value: 0.986.

### 9.4 Interpretation

The near-identical Rank IC before and after industry neutralisation is particularly informative.

If the raw momentum ranking were primarily driven by industry common trends, removing those trends should materially alter cross-sectional predictive ability. Instead, the Rank IC is virtually unchanged.

Industry common trends therefore do not appear to be the main explanation for the weak raw momentum signal or for the mega-cap implementation effect.

---

## 10. Ex-Ante Market-Beta Neutralisation

### 10.1 Beta estimation

At each formation month, stock beta is estimated using the daily excess-return CAPM:

[
R_{i,d}-R_{f,d}
=
alpha_{i,t}
+
eta_{i,t}(R_{m,d}-R_{f,d})
+
epsilon_{i,d}.
]

The estimation window is defined on the CRSP market trading calendar:

- 252 trading days;
- skip the five market trading days immediately before formation;
- minimum 126 valid paired observations.

No beta winsorisation, clipping, forward filling, or imputation is used.

Overall valid-beta coverage averages approximately 97.9% across the formation universe.

### 10.2 Beta-eligible comparator

The beta-neutral portfolio is not compared with a different stock sample.

Instead:

1. stocks without valid beta are removed;
2. original quintile membership is preserved;
3. within-leg value weights are renormalised;
4. this beta-eligible raw portfolio becomes the direct comparator.

In the final momentum Q1/Q5 portfolios, beta coverage is effectively complete, so the beta-eligible raw spread is numerically identical to the original spread.

### 10.3 Market-overlay construction

Let:

[
eta_{LS,t}
=
eta_{Q5,t}
-
eta_{Q1,t}.
]

The primary beta-neutral spread is:

[
R^{BN}_{LS,t+1}
=
R^{Eligible}_{LS,t+1}
-
hateta_{LS,t}
R^{MKT,excess}_{t+1}.
]

This preserves the original momentum holdings and internal stock weights and changes only the portfolio's market exposure.

### 10.4 Return effect

Original value-weighted spread:

[
+0.000746.
]

Beta-neutral spread:

[
-0.000389.
]

Neutralisation effect:

[
-0.001135,
]

or approximately:

[
-0.1135
]

percentage points per month.

Inference:

- HAC6 t-statistic: -0.762;
- HAC6 p-value: 0.446;
- HAC12 p-value: 0.388.

Thus, beta neutralisation lowers the average momentum spread in point estimates, but the effect is statistically imprecise.

### 10.5 Leg-rescaling robustness

A separate robustness construction rescales the long and short legs to achieve zero ex-ante beta while holding total gross exposure at 200%.

The mean neutralisation effect under this construction is:

[
-0.000578,
]

or -0.0578 percentage points per month.

Inference:

- HAC6 p-value: 0.703;
- HAC12 p-value: 0.657.

The direction is consistent with the primary market-overlay construction.

### 10.6 Ex-post realised market beta

The raw momentum portfolio has a realised monthly market beta of:

[
-0.3813.
]

Under HAC6:

- t-statistic: -3.515;
- p-value: 0.00044.

After ex-ante beta neutralisation, realised market beta becomes:

[
-0.1580.
]

Under HAC6:

- t-statistic: -2.049;
- p-value: 0.0405.

Thus, ex-ante hedging materially reduces the magnitude of realised market exposure, though it does not eliminate it.

This is not internally inconsistent. Ex-ante beta neutrality is a construction property based on estimated conditional beta. Ex-post time-series beta reflects realised covariance with the market and can remain non-zero because betas are noisy and time varying.

Additional diagnostics show only a 0.054 correlation between ex-ante net beta and subsequent market excess return, with no simple monotonic relationship across market-return quintiles.

### 10.7 Interpretation

Market beta matters for the realised time-series behaviour of the strategy, but neutralisation does not reveal a statistically robust hidden momentum premium.

The evidence therefore does not support the view that the weak value-weighted momentum result is primarily an artifact of uncompensated market exposure.

---

## 11. Integrated Results

The paper asks three distinct questions.

### 11.1 Does concentration destroy momentum ranking ability?

The evidence is weak.

- Mean Rank IC is positive but small.
- Rank IC does not show a robust negative relationship with Top-10 concentration.
- Removing mega-cap companies leaves Rank IC largely unchanged.
- Industry neutralisation leaves Rank IC almost exactly unchanged.

There is therefore no strong evidence that rising concentration systematically destroys the information contained in the cross-sectional momentum ranking.

### 11.2 Does concentration affect value-weighted implementation?

The evidence is considerably stronger.

- Excluding the Top-10 companies raises the VW spread by about 11 basis points per month.
- Equal-weighted performance changes much less.
- The decomposition assigns almost the entire effect to direct portfolio weights.
- Re-ranking contributes essentially zero.

This is the central mechanism result.

### 11.3 Are systematic exposures the main explanation?

The evidence is again weak.

- Industry neutralisation does not improve signal ranking.
- Beta neutralisation materially reduces realised market beta.
- However, the return effect of beta neutralisation is not statistically precise.
- No robust hidden premium emerges after either industry or market-beta control.

---

## 12. Economic Interpretation

The most coherent interpretation is that market concentration matters through the mapping from cross-sectional ranks to economic portfolio weights.

A cross-sectional signal answers the question:

> which stocks rank high or low?

A value-weighted portfolio answers a different question:

> how much capital is assigned to each ranked stock?

When mega-cap firms become exceptionally large, the second mapping can change dramatically even if the first does not.

This distinction explains why a value-weighted strategy can behave differently in a concentrated market without requiring the underlying rank signal to disappear.

The result is particularly relevant for empirical asset-pricing and systematic-equity research. A decline in value-weighted long-short performance should not automatically be interpreted as evidence that the signal has become less informative. Researchers should separately examine ranking quality, portfolio weighting, and systematic exposures.

---

## 13. Statistical Interpretation

Several economically meaningful point estimates in this paper are statistically imprecise.

This includes:

- the baseline value-weighted momentum premium;
- the aggregate concentration coefficient;
- the mega-cap exclusion effect;
- the direct weight decomposition effect;
- industry-neutralisation return changes;
- beta-neutralisation return changes.

The appropriate conclusion is therefore not that these mechanisms are definitively established in a causal sense.

Instead, the evidence supports a hierarchy:

1. **strongest descriptive mechanism evidence:** mega-cap weight concentration;
2. **weak evidence:** aggregate concentration forecasting momentum;
3. **little evidence:** industry-neutralisation improving ranking;
4. **meaningful exposure change but weak return evidence:** beta neutralisation.

The distinction between economic magnitude and statistical precision is maintained throughout.

---

## 14. Limitations

### 14.1 Sample length

The sample spans 2000–2025. This period is economically rich but still provides only 312 monthly formation observations and 299 valid momentum-performance months. Time-series inference therefore has limited power.

### 14.2 Momentum-only first research version

The original project concept considered several price-based signals. The completed first version deliberately narrows the empirical scope to momentum in order to avoid uncontrolled specification expansion.

Results should not automatically be generalised to reversal, low volatility, beta, profitability, or value signals.

### 14.3 Observational design

The study is observational. Market concentration is not randomly assigned and is strongly persistent over time.

The regressions therefore identify conditional empirical relationships, not causal effects of concentration.

### 14.4 Persistent concentration trend

Top-10 market share has a strong secular trend. The project includes a linear-trend robustness check, but this does not fully solve all identification problems associated with persistent macro-financial state variables.

### 14.5 Transaction costs

The present version focuses on gross portfolio returns and mechanisms rather than a full trading-cost model.

A live strategy would face turnover, bid-ask spreads, market impact, shorting costs, financing, and implementation constraints.

### 14.6 Long-short cumulative-return charts

Cumulative charts in the reporting notebook should be interpreted as descriptive indices of repeated monthly spread returns, not as a fully specified self-financing live-trading wealth process. A final publication version should state the assumed capital convention explicitly or use cumulative arithmetic spread as the main visual.

### 14.7 Beta estimation error

Ex-ante beta is estimated rather than observed. Even with a 252-day window, beta estimates can be noisy, particularly for securities with limited daily history.

The project therefore treats beta neutralisation as an exposure-control exercise rather than a perfect hedge.

### 14.8 Multiple robustness tests

Robustness specifications are not independent hypothesis tests. The project avoids selecting a preferred specification based on which p-value appears most favourable.

For example, the smaller HAC12 p-value for the Top-20 exclusion is not used to redefine the primary mega-cap test.

---

## 15. Conclusion

This paper asks whether rising US equity-market concentration distorts cross-sectional momentum.

The answer is nuanced.

There is no robust evidence that aggregate market concentration systematically reduces momentum's cross-sectional ranking ability. The baseline Rank IC is weak, but neither concentration conditioning nor industry neutralisation reveals a clear deterioration in the information content of the signal.

The more informative result comes from portfolio implementation. Removing mega-cap companies raises the value-weighted momentum spread, and an exact decomposition shows that almost the entire change comes from direct portfolio weights rather than re-ranking. This suggests that concentration can materially alter the realised behaviour of a value-weighted strategy even when the underlying signal ranking remains largely unchanged.

Industry and market-beta controls do not reveal a robust hidden momentum premium. Beta neutralisation materially reduces realised market exposure but produces a statistically imprecise decline in average momentum returns.

The central conclusion is therefore:

> **market concentration appears more relevant to the implementation of value-weighted cross-sectional momentum than to the informational content of the momentum ranking itself.**

More broadly, the results highlight a practical research lesson. In a concentrated market, observed strategy performance should be decomposed into signal quality, portfolio weighting, and systematic exposure before concluding that a factor has strengthened or weakened.

---

## Appendix A. Core Numerical Results

### A.1 Baseline

| Outcome | Mean | HAC6 t | HAC6 p | HAC12 p |
|---|---:|---:|---:|---:|
| Rank IC | 0.007680 | 0.957 | 0.339 | 0.349 |
| VW Q5-Q1 | 0.0746%/mo | 0.227 | 0.821 | 0.807 |
| EW Q5-Q1 | 0.2457%/mo | 0.870 | 0.384 | 0.407 |

### A.2 Concentration regressions

| Specification | Estimate | HAC6 t | p |
|---|---:|---:|---:|
| Top10 -> VW spread | -0.3275% per +10pp | -0.620 | 0.536 |
| Top10 + trend | -0.1617% per +10pp | -0.254 | 0.799 |
| HHI -> VW spread | -0.6091% per +0.01 | -0.723 | 0.470 |
| Top10 -> EW spread | +0.3260% per +10pp | 0.826 | 0.409 |
| Top10 -> Rank IC | +0.006309 per +10pp | 0.506 | 0.613 |
| Lagged Top10 -> VW spread | -0.3030% per +10pp | -0.551 | 0.582 |

### A.3 Mega-cap exclusion

| Specification | Mean spread | Mean change | HAC6 p | HAC12 p |
|---|---:|---:|---:|---:|
| ExTop5 | 0.1375% | +0.0629% | 0.357 | 0.329 |
| ExTop10 | 0.1844% | +0.1099% | 0.269 | 0.250 |
| ExTop20 | 0.2456% | +0.1711% | 0.116 | 0.092 |

### A.4 Mega-cap decomposition

| Component | Mean effect | HAC6 p | HAC12 p |
|---|---:|---:|---:|
| Direct weight | +0.1114%/mo | 0.259 | 0.242 |
| Re-ranking | -0.0016%/mo | 0.866 | 0.866 |
| Total | +0.1099%/mo | 0.269 | 0.250 |

### A.5 Industry neutralisation

| Outcome | Raw | Neutral | Change | HAC6 p |
|---|---:|---:|---:|---:|
| VW spread | +0.0746% | -0.0255% | -0.1001% | 0.585 |
| Rank IC | 0.007680 | 0.007625 | -0.000054 | 0.986 |

### A.6 Beta neutralisation

| Metric | Estimate |
|---|---:|
| Original VW spread | +0.0746%/mo |
| Beta-neutral VW spread | -0.0389%/mo |
| Neutralisation effect | -0.1135%/mo |
| HAC6 p | 0.446 |
| HAC12 p | 0.388 |
| Ex-post beta, raw | -0.381 |
| Ex-post beta, beta-neutral | -0.158 |

