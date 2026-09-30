# Final Synthesis — Working Draft

## Research question

**Does rising concentration in the US equity market distort the measured performance of cross-sectional momentum, and is any distortion primarily a signal-ranking effect or a portfolio-implementation effect?**

This synthesis is intentionally narrower than the original pre-analysis plan. The completed first research version focuses on 12-2 momentum and uses several mechanism tests rather than expanding into many additional signals.

---

## 1. Baseline momentum

Primary signal:

[
MOM_{i,t}=prod_{s=t-12}^{t-2}(1+R_{i,s})-1.
]

The formation universe uses the monthly NYSE 20th-percentile size screen and a $5 price screen. Returns are measured in t+1.

Main descriptive results:

- mean monthly Rank IC: approximately **0.0077**;
- positive Rank IC fraction: approximately **58%**;
- value-weighted Q5-Q1 spread: approximately **+0.075% per month**;
- equal-weighted Q5-Q1 spread: approximately **+0.246% per month**.

Under the pre-specified HAC inference convention, neither the Rank IC nor the value-weighted or equal-weighted spread is statistically distinguishable from zero.

### Interpretation

The sample does not produce a strong unconditional value-weighted momentum premium. This matters because later mechanism tests should be interpreted as explaining variation in a weak baseline rather than decomposing a large unconditional alpha.

---

## 2. Aggregate market concentration

Market concentration is measured on a broader market-state universe and aggregated to the company level using PERMCO before calculating concentration.

Primary measure:
- Top-10 company market-cap share.

Additional measures:
- Top-5 share;
- HHI;
- effective number of firms.

The broad-market Top-10 share rises materially over the sample, reaching roughly 37% by end-2025.

Primary regression:

[
Spread_{t+1}=alpha+eta,Top10Share_t+epsilon_{t+1}.
]

The estimated coefficient is negative in the primary value-weighted specification, but imprecise and not robustly different from zero. Trend-controlled, HHI, equal-weighted, Rank-IC, and lagged-concentration specifications do not produce a stable common sign-and-significance pattern.

### Interpretation

There is no robust evidence that aggregate concentration by itself linearly predicts subsequent momentum effectiveness.

This weakens a simple story of:

> higher market concentration -> lower cross-sectional momentum alpha.

---

## 3. Mega-cap exclusion

To test a more direct composition mechanism, the top 5, 10, and 20 companies by company-level market capitalisation are removed before re-forming momentum portfolios.

Primary Top-10 exclusion:

- baseline VW spread: about **+0.075%/month**;
- ex-Top-10 VW spread: about **+0.184%/month**;
- difference: about **+0.110%/month**.

The difference is positive but statistically imprecise under HAC6/HAC12.

The point estimate grows as more mega-cap firms are excluded, but this monotonic pattern is treated descriptively rather than promoted as a significance-based specification choice.

Equal-weighted momentum and Rank IC change very little.

### Interpretation

The fact that the value-weighted implementation changes while equal-weighted performance and Rank IC remain almost unchanged suggests that mega-caps affect portfolio implementation more than signal ranking.

---

## 4. Mega-cap decomposition

Excluding mega-caps and then re-forming quintiles can mechanically change both weights and quintile membership. To distinguish these channels, the total change is decomposed into:

[
TotalChange = DirectWeightEffect + ReRankingEffect.
]

Using baseline quintile membership and removing Top-10 company securities only within those existing quintiles:

- direct weight effect: about **+0.111%/month**;
- re-ranking effect: approximately **0%/month**;
- total change: about **+0.110%/month**.

Thus, essentially the entire Top-10 exclusion effect comes from direct portfolio weights rather than changes in momentum ordering.

### Interpretation

This is the clearest mechanism result in the project:

> mega-cap concentration can change the realised return of a value-weighted momentum strategy even when the cross-sectional ranking itself is almost unchanged.

---

## 5. Industry neutralisation

Primary neutralisation:
- map contemporaneous SIC to Fama-French 49 industries;
- subtract the equal-weighted industry-month mean momentum;
- re-form global quintiles.

Results:

- raw VW spread: about **+0.075%/month**;
- FF49-neutral VW spread: about **-0.026%/month**;
- change: about **-0.100%/month**, statistically imprecise.

Equal-weighted performance changes little.

Rank IC is almost identical before and after neutralisation:

- raw Rank IC: about **0.00768**;
- FF49-neutral Rank IC: about **0.00763**.

Within-industry percentile and ICB-industry robustness checks tell a similar story.

### Interpretation

There is no evidence that neutralising broad industry common trends improves cross-sectional ranking ability. The signal's weak predictive content is not primarily an industry-classification artifact.

---

## 6. Market-beta neutralisation

Ex-ante stock betas are estimated from daily excess-return CAPM regressions using:

- 252 CRSP market trading days;
- 5-day skip before formation;
- minimum 126 valid paired observations;
- no winsorisation or imputation.

Beta coverage is high and stable, averaging roughly 98%.

For the momentum long-short portfolio:

- Q1 and Q5 portfolio betas are both around one on average;
- average ex-ante net long-short beta is near zero, though it varies substantially over time.

Primary neutralisation keeps the original momentum holdings and within-leg value weights, then hedges the estimated net market beta with a market overlay.

Results:

- beta-eligible raw spread is essentially identical to the original spread;
- beta-neutral spread falls by roughly **11 bps/month** in point estimates;
- the neutralisation effect is not statistically distinguishable from zero under HAC6/HAC12.

A separate long/short leg-rescaling construction produces the same directional conclusion.

The realised monthly market beta of the raw portfolio is materially negative. Ex-ante hedging reduces the magnitude of this realised beta substantially, though it does not eliminate it.

Additional diagnostics show little linear relationship between ex-ante net beta and subsequent market excess return, and no simple monotonic beta pattern across market-return quintiles.

### Interpretation

Market-beta exposure affects the realised time-series behaviour of the value-weighted momentum portfolio, but beta neutralisation does not provide statistically strong evidence of a return improvement or deterioration.

---

# 7. Integrated conclusion

Taken together, the evidence does **not** support a simple claim that rising aggregate market concentration destroys momentum's cross-sectional predictive ability.

Instead, the most coherent interpretation is:

1. the unconditional momentum signal is weak in this sample;
2. aggregate concentration does not robustly predict its subsequent performance;
3. mega-cap exclusion changes value-weighted returns much more than it changes equal-weighted returns or Rank IC;
4. almost all of the mega-cap exclusion effect is attributable to direct weights, not re-ranking;
5. industry neutralisation leaves ranking ability nearly unchanged;
6. beta neutralisation changes realised exposure but does not reveal a statistically robust hidden momentum premium.

The strongest evidence therefore points toward a **portfolio implementation channel**:

> market concentration matters primarily because value-weighted portfolios place large economic weights on a small number of firms, not because concentration systematically destroys the information in the underlying cross-sectional momentum ranking.

This conclusion should be stated cautiously. Several economically meaningful point estimates are statistically imprecise, and the project should not convert weak evidence into a strong causal claim.

---

# 8. Limitations

The final paper should explicitly discuss:

- the sample begins in 2000 and therefore does not cover earlier momentum history;
- the primary signal is momentum only;
- transaction costs are not yet the central focus of the current version;
- market concentration is highly persistent and trending;
- the portfolio analysis is observational rather than causal;
- ex-ante beta estimates are noisy and time-varying;
- value-weighted results can be sensitive to a small number of very large firms;
- statistical power is limited by 312 monthly observations;
- multiple robustness checks are interpreted conservatively to avoid specification mining.

---

# 9. What should not be added now

Unless a clear economic reason emerges, the project should avoid expanding into:

- many alternative momentum windows;
- repeated changes to beta windows or beta clipping;
- arbitrary concentration thresholds chosen after inspecting p-values;
- large families of factor-neutral or residual-momentum specifications;
- dozens of sample splits.

The remaining work should focus on synthesis, transparent robustness, figures, tables, and communication rather than specification expansion.

---

# 10. Final deliverables

Recommended final outputs:

1. one main results table;
2. one mechanism/decomposition table;
3. 4-5 publication-quality figures;
4. an 8-12 page research note;
5. a concise README;
6. a two-line CV bullet;
7. a 60-90 second interview explanation and a deeper 5-minute version.
