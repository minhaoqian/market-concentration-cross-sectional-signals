# Does Market Concentration Distort Cross-Sectional Momentum?

## Mega-Cap Exposure and Portfolio Implementation in US Equities, 2000-2025

**Author:** Minhao Qian  
**Programme:** MSc Mathematical & Computational Finance, University of Oxford  
**Status:** Final research version, October 2026

---

## Abstract

This paper studies whether rising concentration in the US equity market distorts the measured performance of cross-sectional momentum, and whether any distortion reflects weaker stock-ranking information or changes in portfolio implementation. Using CRSP monthly US common-equity data from 2000 through 2025, the analysis constructs a 12-2 momentum signal, evaluates value-weighted and equal-weighted quintile portfolios, measures concentration at the company level, and applies a sequence of mechanism tests involving mega-cap exclusion, industry neutralisation, market-beta neutralisation, and an external benchmark validation against the Kenneth French Momentum Factor.

The unconditional momentum signal is weak in this sample. Mean monthly Rank IC is 0.00768, the value-weighted Q5-Q1 spread averages 0.0746% per month, and the equal-weighted spread averages 0.2457% per month; none is statistically distinguishable from zero under the pre-specified Newey-West inference rule. Aggregate Top-10 market-cap concentration does not robustly predict subsequent momentum returns. By contrast, excluding the ten largest companies raises the value-weighted momentum spread by approximately 0.110 percentage points per month. An exact decomposition localises essentially the entire observed point estimate to direct portfolio weights rather than re-ranking: the direct-weight component is +0.1114 percentage points per month, whereas the re-ranking component is approximately zero.

A final bridge test strengthens the economic interpretation. Higher aggregate Top-10 concentration is strongly associated with a larger Top-10 weight imbalance between the winner and loser legs: a 10-percentage-point increase in aggregate Top-10 share is associated with a 24.5-percentage-point larger Q5-minus-Q1 mega-cap weight gap under the primary specification, and the relation remains positive after a linear time trend. However, the realised direct-weight return effect remains noisy and is not itself precisely increasing with concentration. Industry neutralisation leaves Rank IC almost unchanged, while ex-ante beta hedging materially reduces realised market beta without revealing a statistically robust hidden momentum premium.

The project's momentum implementation is externally validated against the Kenneth French US Momentum Factor. Over 299 common holding months, the project value-weighted spread has a 0.875 correlation with French Mom and the equal-weighted spread has a 0.917 correlation. The combined evidence therefore points toward a portfolio-implementation channel: concentration changes the economic weights attached to momentum rankings more clearly than it changes the informational content of those rankings.

---

# 1. Introduction

US equity-market concentration has increased sharply in recent years. By the end of 2025, the ten largest US-listed companies account for roughly 37% of aggregate market capitalisation in the broad market-state universe used in this study. This development matters for quantitative equity research because many cross-sectional signals are evaluated through value-weighted portfolios. When a small number of companies become exceptionally large, the realised performance of a signal portfolio can become highly sensitive to those companies even if the underlying ranking rule has not changed.

This distinction motivates the central research question:

> **Does rising market concentration weaken the informational content of cross-sectional momentum, or does it primarily change the implementation of a value-weighted momentum portfolio?**

A cross-sectional signal and a portfolio implementation answer different questions. A signal ranks securities. A weighting rule determines how much economic exposure is attached to each rank. In a dispersed market those layers may appear similar. In a concentrated market they can diverge.

The empirical design therefore separates three channels.

1. **Signal quality.** Monthly Spearman Rank IC and the stability of cross-sectional ordering are used to ask whether past-return rankings continue to contain information about next-month returns.
2. **Portfolio implementation.** Value-weighted and equal-weighted returns are compared; mega-cap companies are removed; and the exclusion effect is decomposed into a direct-weight component and a re-ranking component.
3. **Systematic exposure.** Industry-neutral and market-beta-neutral implementations are used to determine whether the raw strategy mainly reflects common industry trends or market exposure rather than cross-sectional momentum.

The paper's contribution is not a claim that concentration causally destroys or creates momentum. The aggregate concentration regressions are statistically weak. The more informative result comes from the portfolio-construction layer. Mega-cap exclusion changes value-weighted momentum returns while leaving ranking diagnostics almost unchanged, and the decomposition shows that virtually all of the observed exclusion point estimate is attributable to direct weights.

A final concentration-mechanism bridge test sharpens this interpretation. Aggregate concentration strongly predicts the **weight imbalance** created by mega-cap firms between the winner and loser portfolios, even after a linear time trend. It does not precisely predict the realised monthly direct-weight return effect. This is economically coherent: concentration determines how much portfolio weight mega-cap firms receive, whereas the return consequence additionally depends on what those firms subsequently earn.

The project also performs two final validation checks. First, the project momentum series co-moves very strongly with the Kenneth French US Momentum Factor despite different portfolio constructions. Second, official CRSP CIZ documentation confirms that the monthly total return field used here compounds daily returns and includes delisting returns when appropriate, so a separate legacy-style DLRET merge is not required.

The resulting conclusion is narrower, and stronger, than a generic factor-decay claim:

> **market concentration appears more relevant to the implementation of value-weighted cross-sectional momentum than to the informational content of the momentum ranking itself.**

---

# 2. Related Literature

## 2.1 Cross-sectional momentum

Jegadeesh and Titman (1993) establish the classic intermediate-horizon momentum result: stocks with strong past returns tend to outperform stocks with weak past returns over subsequent months. The present study follows this broad empirical tradition and uses a pre-specified 12-2 formation rule, skipping the most recent month.

The purpose here is not to re-establish momentum as an anomaly over the full historical CRSP sample. The sample begins in 2000, after the original discovery period, and the primary objective is diagnostic: momentum provides a canonical cross-sectional signal through which to distinguish ranking quality from portfolio implementation.

Daniel and Moskowitz (2016) show that momentum returns can be highly state dependent and can experience large crashes, particularly around market rebounds following stressed states. That literature is relevant to the present sample because weak unconditional momentum need not imply an implementation error or permanent disappearance of the signal. It also motivates the project's separate examination of market-beta exposure.

## 2.2 Industry momentum and neutralisation

Moskowitz and Grinblatt (1999) document a substantial industry component in momentum and show that controlling for industry momentum can reduce individual-stock momentum profitability. This provides the direct motivation for the FF49 industry-neutralisation exercise in this paper.

The empirical question is not whether industry exposure should always be removed. Neutralisation can remove unwanted exposure, but it can also remove economically relevant variation. The appropriate test is therefore comparative: does industry neutralisation improve ranking information or materially change the portfolio result?

## 2.3 Market concentration and portfolio structure

Recent work treats financial-market concentration as an economically meaningful state variable rather than a purely descriptive statistic. Research on market concentration, large-firm valuation, price impact, capital allocation, regulatory constraints, and granular market structure motivates the possibility that a small number of dominant firms can alter portfolio behaviour even without becoming standalone return predictors.

The present study takes a deliberately narrower empirical approach. Concentration is used both as a market-state variable and as a portfolio-composition mechanism. The goal is to determine whether concentration changes the information in momentum ranks, the economic weights assigned to those ranks, or both.

## 2.4 Beta and factor implementation

Factor portfolios can inherit unintended systematic exposures. Frazzini and Pedersen (2014), among others, highlight the economic importance of beta exposure and leverage constraints. In the present setting, market-beta neutralisation is used as an exposure diagnostic rather than as an assumption that a neutral portfolio must be superior.

The paper therefore compares the original momentum spread, a beta-eligible comparator with identical signal membership, and an ex-ante beta-neutral portfolio. This separates sample-coverage effects from the effect of hedging market exposure.

---

# 3. Data and Sample Construction

## 3.1 Monthly CRSP sample

The primary sample uses CRSP monthly US stock data obtained through WRDS and spans January 2000 through December 2025.

The final investable formation panel contains:

- 601,350 security-month observations;
- 7,423 unique PERMNO securities;
- 312 formation months;
- 544,090 valid 12-2 momentum observations.

The formation universe applies the following rules:

- US common equities;
- NYSE, AMEX, or NASDAQ primary listing;
- positive formation-month market capitalisation;
- exclusion of stocks below the monthly NYSE 20th percentile of market capitalisation;
- month-end price of at least $5.

PERMNO is used as the security identifier. PERMCO is used as the economic-company identifier for concentration and mega-cap analysis.

## 3.2 Formation universe versus market-state universe

The project separates the **signal-investment universe** from the **market-state universe**.

The investment universe applies the NYSE size screen and the $5 price screen. The broader market-state universe retains the common-equity, major-exchange, and positive-market-cap requirements but omits those stricter investability filters.

This distinction avoids mechanically defining market concentration using the same screens that determine signal eligibility.

## 3.3 Company-level concentration and multiple share classes

Concentration is measured after aggregating listed share classes to PERMCO.

This matters for companies such as Alphabet, where GOOG and GOOGL are separate listed securities but represent claims on the same economic issuer. Security-level treatment remains appropriate for returns and momentum ranking; company-level aggregation is appropriate for market concentration.

## 3.4 Monthly return treatment and delistings

The analysis uses CRSP CIZ `MthRet` as the monthly total-return field.

CRSP's File Format 2.0 documentation defines `MthRet` as the daily total return compounded for the period and states that it includes delisting returns when appropriate. The CIZ cross-reference guide further explains that the shift to daily-compounded monthly returns also applies to delisting returns.

Accordingly, the study does **not** apply an additional legacy-style merge of a separate DLRET field into `MthRet`. Doing so would risk double-counting delisting information already included in the CIZ monthly return.

## 3.5 Daily beta inputs

Daily beta estimation uses:

- CRSP daily stock total returns;
- CRSP value-weighted daily market total return including dividends;
- Kenneth French daily risk-free rate.

The stock history begins in December 1998 to provide sufficient pre-2000 beta history.

The daily stock extract was separately audited. It contained 16,259 rows belonging to 7,837 duplicated PERMNO-date groups. Every such group was an exact full-row duplicate with identical daily return. Retaining one copy removed 8,422 redundant rows and left zero conflicting return groups.

The daily CRSP market series and French risk-free series align exactly on 6,813 trading dates over the research interval.

---

# 4. Research Design

## 4.1 Momentum signal

At formation month (t), the momentum signal is

[
MOM_{i,t}=prod_{s=t-12}^{t-2}(1+R_{i,s})-1.
]

The signal uses eleven monthly total returns and skips (t-1).

Momentum history is constructed on a broader monthly history panel. Formation-date investability screens are applied at (t), not retroactively to every month in the lookback window. Valid momentum requires contiguous calendar-month history.

## 4.2 Portfolio formation

Each formation month:

1. eligible securities are ranked by momentum;
2. five cross-sectional quintiles are formed;
3. Q5 is the winner portfolio;
4. Q1 is the loser portfolio;
5. the Q5-Q1 spread is realised in calendar month (t+1).

The primary implementation is value weighted using formation-month market capitalisation. Equal-weighted returns are retained as an implementation diagnostic.

Missing next-month returns are never replaced with zero. Weights are renormalised among securities with observed next-month returns.

## 4.3 Rank IC

Monthly Spearman Rank IC is computed between the momentum signal at formation and next-month returns.

Rank IC is particularly useful for the paper's central question because it measures ranking information without imposing the value-weighting scheme that may itself be distorted by mega-cap concentration.

## 4.4 Inference convention

Inference rules were frozen before the main concentration and neutralisation results were interpreted:

- Newey-West HAC lag 6: primary;
- Newey-West HAC lag 12: robustness;
- two-sided tests;
- 95% confidence intervals.

The same convention is maintained throughout to reduce specification selection based on significance.

---

# 5. Baseline Momentum and External Validation

## 5.1 Baseline results

The investable universe contains an average of approximately 1,927 stocks per month and a median of 1,843.

The mean monthly Rank IC is

[
0.00768.
]

Under HAC6:

- t = 0.957;
- p = 0.339;
- 95% CI = [-0.0081, 0.0234].

The primary value-weighted Q5-Q1 spread averages

[
0.0746%	ext{ per month}.
]

Under HAC6:

- t = 0.227;
- p = 0.821;
- 95% CI = [-0.570%, 0.719%] per month.

The equal-weighted spread averages

[
0.2457%	ext{ per month},
]

with HAC6 p = 0.384.

The point estimate is substantially larger under equal weighting, but neither implementation is statistically distinguishable from zero.

## 5.2 Why the weak baseline requires validation

Because momentum is a well-established empirical phenomenon, a weak 2000-2025 baseline raises an important implementation question. A low sample mean could reflect genuine sample-period behaviour, portfolio-construction differences, or a coding/timing error.

The project therefore performs an external benchmark validation against the Kenneth French US monthly Momentum Factor (Mom).

The project spread is aligned by **realised holding month**. A project portfolio formed in month (t) earns its return in (t+1), so its (t+1) return is compared with French Mom in (t+1).

The constructions are intentionally different. French Mom uses six value-weighted portfolios from a 2x3 size-by-prior-return sort, while this project uses a screened investment universe and global quintiles. Equality is neither expected nor required.

## 5.3 External benchmark results

Across 299 common monthly observations:

| Series | Mean monthly | Monthly volatility |
|---|---:|---:|
| Project VW | 0.0746% | 5.564% |
| Project EW | 0.2457% | 4.632% |
| Kenneth French Mom | 0.2021% | 4.634% |

The correlations are:

- Corr(Project VW, French Mom) = **0.8754**;
- Corr(Project EW, French Mom) = **0.9165**;
- Corr(Project VW, Project EW) = 0.8609.

A diagnostic HAC6 regression of the project VW spread on French Mom gives:

- French Mom beta = 1.051;
- HAC SE = 0.074;
- t = 14.18;
- 95% CI = [0.906, 1.196];
- (R^2 = 0.766);
- alpha = -0.138% per month, p = 0.404.

For the project EW spread:

- French Mom beta = 0.916;
- HAC SE = 0.039;
- t = 23.61;
- 95% CI = [0.840, 0.992];
- (R^2 = 0.840);
- alpha = +0.061% per month, p = 0.590.

The project implementation therefore exhibits very strong co-movement with an established external benchmark. The weak value-weighted mean is not evidence of an obvious one-month timing error or a fundamentally broken momentum implementation.

---

# 6. Aggregate Market Concentration

## 6.1 Measures

Company-level concentration is measured using:

- Top-5 market-cap share;
- Top-10 market-cap share;
- HHI;
- effective number of firms, (1/HHI).

Top-10 share declines toward roughly 15% around the mid-2010s before rising sharply. It reaches approximately 37% by end-2025.

## 6.2 Primary conditioning regression

The primary specification is

[
Spread_{t+1}=alpha+eta Top10Share_t+epsilon_{t+1}.
]

Top-10 share is scaled so that the reported coefficient corresponds to a +10-percentage-point change in concentration.

The primary VW coefficient is

[
-0.3275%	ext{ per month per +10pp Top-10 share}.
]

Inference:

- HAC6 t = -0.620;
- p = 0.536;
- 95% CI = [-1.364%, 0.709%].

Adding a linear time trend reduces the coefficient to -0.162% with p = 0.799.

Using HHI produces a similarly imprecise result. Equal-weighted and Rank-IC specifications switch sign, and lagging concentration by one month does not change the overall conclusion.

## 6.3 Interpretation

Aggregate concentration does not robustly predict subsequent momentum effectiveness.

This finding rejects an overly simple narrative in which rising concentration mechanically destroys momentum alpha. It does not, however, rule out a more direct portfolio-composition mechanism.

---

# 7. Mega-Cap Exclusion

## 7.1 Design

Each month, the largest firms are identified at the PERMCO level using the broad market-state universe. All securities belonging to the relevant companies are removed from the formation universe.

The primary specification excludes the Top 10 companies. Top 5 and Top 20 are retained as robustness checks.

## 7.2 Results

| Exclusion | Mean VW spread | Change vs baseline | HAC6 p | HAC12 p |
|---|---:|---:|---:|---:|
| Top 5 | 0.1375% | +0.0629 pp | 0.357 | 0.329 |
| Top 10 | 0.1844% | +0.1099 pp | 0.269 | 0.250 |
| Top 20 | 0.2456% | +0.1711 pp | 0.116 | 0.092 |

For Top-10 exclusion, the approximate HAC6 95% confidence interval for the monthly change is [-0.085%, 0.305%].

The point estimate becomes larger as more mega-cap companies are excluded. This ordering is treated descriptively. Top 20 is not promoted to the primary specification based on its lower p-value.

---

# 8. Mega-Cap Decomposition

## 8.1 Why exclusion alone is insufficient

Removing mega-cap firms and then re-forming quintiles changes two objects at once:

1. portfolio weights;
2. quintile membership.

To identify the mechanism, the Top-10 exclusion effect is decomposed exactly.

A fixed-rank portfolio preserves the original Q1-Q5 membership, removes Top-10 company securities within those original portfolios, and renormalises the remaining value weights.

Define:

[
DirectWeightEffect=FixedRanks-Baseline,
]

[
ReRankingEffect=Reformed-FixedRanks,
]

so that

[
TotalChange=DirectWeightEffect+ReRankingEffect.
]

## 8.2 Results

| Component | Mean monthly effect | HAC6 p | HAC12 p |
|---|---:|---:|---:|
| Direct weight | +0.1114 pp | 0.259 | 0.242 |
| Re-ranking | -0.0016 pp | 0.866 | 0.866 |
| Total | +0.1099 pp | 0.269 | 0.250 |

The approximate HAC6 95% CI for the direct-weight effect is [-0.082%, 0.305%] per month.

The decomposition strongly **localises the observed exclusion point estimate** to the direct-weight channel. It does not, by itself, establish that the population mean direct-weight effect is positive with conventional statistical precision.

This distinction is important. The clean decomposition answers **where the observed monthly-average difference comes from**; the wide confidence interval answers **how precisely its population magnitude is estimated**.

## 8.3 Leg-level exposure

Top-10 companies account on average for:

- 9.95% of Q1 formation weight;
- 17.66% of Q5 formation weight.

Median shares are 8.26% and 15.87%, respectively.

The winner portfolio therefore carries substantially more mega-cap weight than the loser portfolio on average.

---

# 9. Concentration-to-Mechanism Bridge

The decomposition demonstrates that the observed Top-10 exclusion point estimate is a weight effect. A remaining question is whether this weight mechanism is actually stronger when the **aggregate market is more concentrated**.

Two bridge specifications were fixed before observing the results.

## 9.1 Does concentration predict the realised direct-weight return effect?

[
DirectWeightEffect_t=alpha+eta Top10Share_t+epsilon_t.
]

Per +10pp Top-10 market share:

- coefficient = +0.1840 percentage points per month;
- HAC6 SE = 0.2383 percentage points;
- t = 0.772;
- p = 0.440;
- 95% CI = [-0.283%, 0.651%];
- N = 299.

HAC12 p = 0.316.

With a linear time trend, the coefficient is +0.2748 percentage points, p = 0.283.

Thus, aggregate concentration does **not** precisely predict the realised direct-weight return effect.

## 9.2 Does concentration predict the mega-cap weight imbalance?

Define:

[
WeightGap_t=Top10Weight_{Q5,t}-Top10Weight_{Q1,t}.
]

Regressing this weight gap on Top-10 market share gives, per +10pp concentration:

- coefficient = **+24.48 percentage points**;
- HAC6 SE = 3.71 percentage points;
- t = 6.60;
- p < 0.0000000001;
- 95% CI = [17.21 pp, 31.75 pp];
- N = 300;
- (R^2 = 0.297).

HAC12 gives essentially the same result.

After adding a linear time trend:

- coefficient = **+9.93 percentage points**;
- t = 2.51;
- p = 0.012;
- 95% CI = [2.18 pp, 17.68 pp].

## 9.3 Interpretation

This bridge is central to the final interpretation.

Higher aggregate concentration is strongly associated with a larger **portfolio-exposure imbalance**: mega-cap companies take relatively more weight in the winner leg than the loser leg as market concentration rises.

However, the return consequence of that imbalance is noisy. The direct-weight return effect depends not only on the size of the weight imbalance but also on the subsequent realised returns of the mega-cap companies occupying Q5 and Q1.

The evidence therefore supports the following statement:

> **market concentration clearly changes the geometry of value-weighted momentum exposure, but it does not generate a stable one-to-one mapping from concentration to subsequent momentum returns.**

---

# 10. Industry Neutralisation

## 10.1 Method

Securities are mapped to contemporaneous Fama-French 49 industries using SIC codes.

Within each valid industry-month, the equal-weighted industry mean momentum signal is subtracted:

[
MOM^{IN}_{i,t}=MOM_{i,t}-overline{MOM}_{g,t}.
]

Industries require at least ten stocks. Global quintiles are then re-formed on the neutralised signal.

## 10.2 Results

Raw VW spread:

[
+0.0746%	ext{/month}.
]

FF49-neutral VW spread:

[
-0.0255%	ext{/month}.
]

Difference:

[
-0.1001%	ext{/month}.
]

HAC6 p = 0.585. The approximate 95% CI is [-0.459%, 0.259%].

More importantly:

- Raw Rank IC = 0.007680;
- FF49-neutral Rank IC = 0.007625;
- difference = -0.000054;
- HAC6 p = 0.986.

The ranking information is essentially unchanged.

## 10.3 Interpretation

The result does not reproduce a large improvement from industry neutralisation in this sample. Broad industry common trends are therefore not the main explanation for the observed cross-sectional ranking or for the mega-cap implementation effect.

---

# 11. Market-Beta Neutralisation

## 11.1 Ex-ante beta estimation

For each stock and formation month:

[
R_{i,d}-R_{f,d}
=
alpha_{i,t}
+
eta_{i,t}(R_{m,d}-R_{f,d})
+epsilon_{i,d}.
]

The locked specification uses:

- 252 CRSP market trading days;
- skip the five trading days immediately before formation;
- minimum 126 valid paired observations;
- no winsorisation;
- no clipping;
- no beta imputation.

Average valid-beta coverage across the formation universe is approximately 97.9%. Coverage is effectively complete among stocks entering Q1 and Q5.

## 11.2 Primary market-overlay hedge

The primary beta-neutral portfolio preserves the original stock holdings and within-leg value weights.

Let

[
eta_{LS,t}=eta_{Q5,t}-eta_{Q1,t}.
]

Then

[
R^{BN}_{LS,t+1}
=
R^{Eligible}_{LS,t+1}
-
hateta_{LS,t}R^{MKT,excess}_{t+1}.
]

## 11.3 Results

- Original VW spread = +0.0746%/month;
- Beta-eligible spread = +0.0746%/month;
- Beta-neutral spread = -0.0389%/month;
- Neutralisation effect = -0.1135 percentage points/month.

Inference on the neutralisation effect:

- HAC6 t = -0.762;
- p = 0.446;
- approximate 95% CI = [-0.405%, 0.178%];
- HAC12 p = 0.388.

A leg-rescaling robustness construction produces a smaller negative point estimate and similarly weak inference.

## 11.4 Realised market beta

The raw momentum portfolio has ex-post monthly market beta:

[
-0.381.
]

HAC6 p = 0.00044.

After ex-ante neutralisation:

[
-0.158,
]

with p = 0.0405.

Thus, the hedge substantially reduces realised market exposure but does not mechanically eliminate it.

The difference between near-zero average ex-ante net beta and more negative realised time-series beta is not explained by a simple linear relationship between formation beta and next-month market return. Their correlation is only about 0.054, and market-return quintiles do not reveal a monotonic pattern.

## 11.5 Interpretation

Market beta matters for the realised behaviour of the strategy, but beta neutralisation does not reveal a statistically robust hidden momentum premium.

Ex-ante neutrality should also not be confused with ex-post neutrality. The former is constructed from estimated conditional betas; the latter reflects realised covariance over time.

---

# 12. Integrated Interpretation

The study asks three distinct questions.

## 12.1 Does concentration destroy momentum ranking information?

The evidence does not support a strong affirmative answer.

- Mean Rank IC is weak but positive.
- Top-10 concentration does not robustly reduce Rank IC.
- Mega-cap exclusion changes value-weighted returns much more than ranking diagnostics.
- Industry neutralisation leaves Rank IC almost unchanged.
- The project momentum series strongly co-moves with the established French momentum benchmark.

There is no clear evidence that rising concentration systematically destroys the informational content of the 12-2 ranking.

## 12.2 Does concentration change value-weighted implementation?

Yes, descriptively and mechanically.

The Top-10 exclusion point estimate is almost entirely localised to the direct-weight component. More importantly, the final bridge test shows that aggregate concentration strongly predicts the **Q5-minus-Q1 mega-cap weight gap**, including after controlling for a linear trend.

This is the strongest link between aggregate concentration and the portfolio-construction mechanism.

The return consequence remains statistically imprecise because exposure and payoff are separate objects. A larger mega-cap weight imbalance does not guarantee a larger monthly return distortion unless the relevant mega-cap stocks subsequently earn unusually high or low returns.

## 12.3 Are industry or market beta the main hidden explanation?

The evidence suggests no.

Industry neutralisation leaves ranking quality virtually unchanged. Beta neutralisation materially changes market exposure but does not uncover a statistically robust positive momentum premium.

The main empirical distinction therefore remains ranking information versus value-weighted implementation.

---

# 13. What the Evidence Does and Does Not Establish

The paper's strongest result is structural rather than causal.

It **does establish** that:

- the observed Top-10 exclusion point estimate is almost entirely a direct-weight effect rather than a re-ranking effect;
- rising aggregate concentration is strongly associated with a larger mega-cap weight imbalance between Q5 and Q1;
- the project momentum implementation has high external correlation with the Kenneth French momentum benchmark;
- industry neutralisation does not materially alter Rank IC;
- ex-ante market hedging materially reduces realised market beta.

It **does not establish** that:

- a 10-percentage-point rise in concentration causally reduces future momentum returns by a fixed amount;
- the positive mean Top-10 exclusion return effect is estimated with high statistical precision;
- removing mega-cap firms would necessarily improve a live momentum strategy after trading and financing costs;
- the conclusions generalise automatically to other signals.

This distinction keeps the interpretation proportional to the evidence.

---

# 14. Limitations

## 14.1 Sample period

The sample begins in 2000 and does not include the earlier decades in which the original momentum literature was established.

The sample contains 312 formation months and 299 valid momentum-performance months, limiting statistical power for persistent state variables.

## 14.2 Momentum-only scope

This completed research version studies one signal: 12-2 momentum.

The results should not automatically be extrapolated to value, reversal, low volatility, profitability, quality, or other cross-sectional characteristics.

## 14.3 Observational identification

Market concentration is persistent, strongly trending, and not randomly assigned.

The paper therefore identifies empirical associations and portfolio mechanics rather than a clean causal effect of concentration.

The bridge weight-gap result survives a linear trend, which strengthens the mechanism interpretation, but a deterministic trend does not remove all possible common-state confounding.

## 14.4 Statistical precision

Several economically meaningful point estimates are imprecisely estimated:

- the unconditional VW momentum spread;
- the aggregate concentration coefficient;
- the Top-10 exclusion return effect;
- the direct-weight return effect;
- industry-neutralisation return differences;
- beta-neutralisation return differences.

Confidence intervals are therefore reported and interpretation does not rely on statistical-significance thresholds alone.

## 14.5 Transaction and implementation costs

The analysis focuses on gross returns.

A live long-short implementation would face turnover, bid-ask spreads, market impact, shorting costs, borrow availability, financing, and operational constraints. Mega-cap removal could itself change liquidity and turnover.

The paper therefore makes a research-mechanism claim rather than a claim about directly tradable net alpha.

## 14.6 Beta estimation error

Ex-ante beta is estimated, not observed.

Conditional betas can vary over time, and estimation error can leave non-zero realised market exposure even when the constructed ex-ante beta is zero.

## 14.7 Multiple robustness checks

Robustness specifications are treated as dependent diagnostics rather than independent discovery tests.

Primary rules were frozen before results where possible, and smaller p-values in secondary specifications are not used to redefine the research question after the fact.

---

# 15. Conclusion

This paper studies whether rising US equity-market concentration distorts cross-sectional momentum.

The evidence does not support a simple claim that aggregate concentration systematically destroys momentum ranking ability. The baseline momentum signal is weak over 2000-2025, but its implementation is externally validated against the Kenneth French Momentum Factor, and ranking diagnostics remain broadly stable across mega-cap exclusion and industry neutralisation.

The more informative result lies in portfolio implementation.

Removing the ten largest companies raises the value-weighted momentum spread by about 11 basis points per month in point estimates. An exact decomposition localises virtually the entire observed difference to direct portfolio weights rather than re-ranking. The final bridge test then connects this mechanism back to aggregate concentration: as the market becomes more concentrated, the mega-cap weight imbalance between the winner and loser portfolios becomes substantially larger, including after a linear time trend.

At the same time, the realised return effect of that weight channel remains noisy and statistically imprecise. This distinction is economically important. Concentration can clearly change **exposure** without generating a deterministic change in **payoff**.

Industry and market-beta controls do not reveal a robust hidden momentum premium. Beta hedging reduces realised market exposure but does not overturn the return conclusion.

The final conclusion is therefore:

> **market concentration appears more relevant to the portfolio implementation of value-weighted cross-sectional momentum than to the informational content of the momentum ranking itself.**

More broadly, the project illustrates a practical principle for quantitative equity research. When factor performance changes in a concentrated market, researchers should decompose the observation into three separate questions:

1. did the cross-sectional ranking weaken?
2. did the weighting rule concentrate economic exposure?
3. did systematic factor exposures change?

Only after separating those layers should a weaker realised portfolio be described as genuine factor decay.

---

# Appendix A. Core Results

## A.1 Baseline

| Outcome | Mean | HAC6 t | HAC6 p | HAC12 p |
|---|---:|---:|---:|---:|
| Rank IC | 0.007680 | 0.957 | 0.339 | 0.349 |
| VW Q5-Q1 | 0.0746%/mo | 0.227 | 0.821 | 0.807 |
| EW Q5-Q1 | 0.2457%/mo | 0.870 | 0.384 | 0.407 |

## A.2 Aggregate concentration

| Specification | Estimate | HAC6 p |
|---|---:|---:|
| Top10 -> VW spread | -0.3275% per +10pp | 0.536 |
| Top10 + linear trend | -0.1617% per +10pp | 0.799 |
| HHI -> VW spread | -0.6091% per +0.01 | 0.470 |
| Top10 -> EW spread | +0.3260% per +10pp | 0.409 |
| Top10 -> Rank IC | +0.006309 per +10pp | 0.613 |
| Lagged Top10 -> VW spread | -0.3030% per +10pp | 0.582 |

## A.3 Mega-cap exclusion

| Specification | Mean spread | Mean change | HAC6 p | HAC12 p |
|---|---:|---:|---:|---:|
| ExTop5 | 0.1375% | +0.0629 pp | 0.357 | 0.329 |
| ExTop10 | 0.1844% | +0.1099 pp | 0.269 | 0.250 |
| ExTop20 | 0.2456% | +0.1711 pp | 0.116 | 0.092 |

## A.4 Mega-cap decomposition

| Component | Mean effect | HAC6 p | HAC12 p |
|---|---:|---:|---:|
| Direct weight | +0.1114 pp/mo | 0.259 | 0.242 |
| Re-ranking | -0.0016 pp/mo | 0.866 | 0.866 |
| Total | +0.1099 pp/mo | 0.269 | 0.250 |

## A.5 Concentration-mechanism bridge

| Outcome | Coefficient per +10pp Top10 share | HAC6 p | 95% CI |
|---|---:|---:|---:|
| Direct-weight return effect | +0.1840 pp/mo | 0.440 | [-0.283, 0.651] pp |
| Q5-Q1 Top10 weight gap | +24.48 pp | <1e-10 | [17.21, 31.75] pp |
| Q5-Q1 weight gap + time trend | +9.93 pp | 0.012 | [2.18, 17.68] pp |

## A.6 Industry neutralisation

| Outcome | Raw | Neutral | Change | HAC6 p |
|---|---:|---:|---:|---:|
| VW spread | +0.0746% | -0.0255% | -0.1001 pp | 0.585 |
| Rank IC | 0.007680 | 0.007625 | -0.000054 | 0.986 |

## A.7 Beta neutralisation

| Metric | Estimate |
|---|---:|
| Original VW spread | +0.0746%/mo |
| Beta-neutral VW spread | -0.0389%/mo |
| Neutralisation effect | -0.1135 pp/mo |
| HAC6 p | 0.446 |
| HAC12 p | 0.388 |
| Ex-post market beta: raw | -0.381 |
| Ex-post market beta: beta-neutral | -0.158 |

## A.8 External benchmark validation

| Metric | Project VW | Project EW |
|---|---:|---:|
| Correlation with French Mom | 0.875 | 0.917 |
| Regression beta on French Mom | 1.051 | 0.916 |
| Regression beta 95% CI | [0.906, 1.196] | [0.840, 0.992] |
| Regression R2 | 0.766 | 0.840 |
| Alpha p-value | 0.404 | 0.590 |

---

# Appendix B. Reproducibility and Audit Notes

- Raw licensed CRSP data are excluded from the public repository.
- Monthly data are cleaned to unique PERMNO-month observations before analysis.
- Momentum was manually validated on extreme cases using calendar-month periods.
- Market concentration is measured on a broader market-state universe and aggregated to PERMCO.
- Multiple share classes are combined for concentration but remain separate securities for return analysis.
- CRSP CIZ `MthRet` is used directly; official documentation states that it compounds daily total returns and includes delisting returns when appropriate.
- Daily stock data were audited for duplicate PERMNO-date rows before beta estimation.
- Daily CRSP market and French RF align on 6,813 research-period trading dates.
- The 252-day / 5-day skip / 126-observation beta rule was frozen before beta-neutral portfolio results.
- HAC6 primary and HAC12 robustness were fixed before concentration and neutralisation interpretation.
- Top-10 is the primary mega-cap exclusion specification; Top-5 and Top-20 remain robustness checks.
- The concentration-mechanism bridge specifications were frozen before results.
- External French Mom validation is aligned by realised holding month rather than formation-month label.

---

# References

Daniel, K., & Moskowitz, T. J. (2016). Momentum crashes. *Journal of Financial Economics*, 122(2), 221-247.

Ehsani, S., Harvey, C. R., & Li, F. *Is Sector-Neutrality in Factor Investing a Mistake?* Working paper.

Frazzini, A., & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1-25.

Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers: Implications for stock market efficiency. *Journal of Finance*, 48(1), 65-91.

Moskowitz, T. J., & Grinblatt, M. (1999). Do industries explain momentum? *Journal of Finance*, 54(4), 1249-1290.

Neuhann, D., & Sockin, M. (2024). *Financial Market Concentration and Misallocation*. Journal / working-paper version as cited in the project literature notes.

Center for Research in Security Prices (CRSP). *CRSP US Stock & Indexes Database Guide, File Format 2.0 (CIZ)*.

Center for Research in Security Prices (CRSP). *SIZ to CIZ Cross-Reference Guide*.

Kenneth R. French Data Library. *Momentum Factor (Mom)* and daily research factors.
