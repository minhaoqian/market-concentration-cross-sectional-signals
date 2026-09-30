# Final Reporting Plan

## Objective

The final report should be a complete empirical research note rather than a collection of notebook outputs. It should explain the research question, data, methodology, empirical results, mechanism tests, robustness, limitations, and economic interpretation in a single coherent narrative.

Target length: approximately **8-12 pages of main text**, excluding appendix material.

---

# 1. Proposed report structure

## 1. Introduction

The introduction should motivate the rise in US equity-market concentration and explain why it may matter for cross-sectional equity strategies.

The central question is:

> Does market concentration distort the measured performance of cross-sectional momentum, and if so, does the distortion arise because the underlying ranking becomes less informative or because value-weighted portfolio implementation becomes increasingly dominated by mega-cap firms?

The introduction should distinguish three ideas from the outset:

1. **signal quality** — whether past-return rankings predict future cross-sectional returns;
2. **portfolio implementation** — how value weighting maps those rankings into realised portfolio returns;
3. **systematic exposure** — whether apparent momentum returns reflect industry or market-beta exposure.

The introduction should preview the main finding cautiously: the strongest evidence points toward a portfolio-weight implementation channel rather than a collapse in cross-sectional ranking ability.

## 2. Data and sample construction

This section should document:

- CRSP / WRDS monthly common-equity data, 2000-2025;
- CRSP daily stock data, 1998-2025;
- CRSP value-weighted market total return;
- Kenneth French daily risk-free rate;
- NYSE / AMEX / NASDAQ restriction;
- positive market capitalisation;
- monthly NYSE 20th-percentile size screen;
- $5 price screen;
- PERMNO as security identifier;
- PERMCO aggregation for company-level concentration;
- exact-duplicate treatment;
- missing-return treatment;
- formation month t and realised return t+1.

The report should explicitly separate:

- **broad market-state universe** for concentration measurement;
- **signal-investment universe** for momentum portfolio construction.

This distinction is important because using the stricter investable universe to measure concentration could mechanically condition the market-state variable on the portfolio eligibility rules.

## 3. Momentum signal and baseline

Define 12-2 momentum:

[
MOM_{i,t}=prod_{s=t-12}^{t-2}(1+R_{i,s})-1.
]

Explain:

- 11 monthly returns;
- skip t-1;
- require contiguous history;
- next-month outcome must correspond to calendar t+1;
- quintiles re-formed monthly;
- Q5 is long, Q1 is short;
- value-weighted implementation is primary;
- equal-weighted and Rank IC are robustness / diagnostic measures.

Inference:

- Newey-West HAC lag 6 primary;
- lag 12 robustness;
- two-sided tests;
- 95% confidence intervals.

## 4. Market concentration

Define company-level:

- Top-5 market share;
- Top-10 market share;
- HHI;
- effective number of firms.

Explain PERMCO aggregation and why multiple share classes such as Alphabet must be combined for market-concentration measurement.

Primary specification:

[
Spread_{t+1}=alpha+eta Top10Share_t+epsilon_{t+1}.
]

Report:

- raw Top-10 trend;
- primary HAC regression;
- linear time-trend robustness;
- HHI robustness;
- lagged concentration timing robustness;
- descriptive expanding concentration regimes.

Do not interpret regime ordering as causal or monotonic evidence.

## 5. Mega-cap composition mechanism

Explain why aggregate concentration regressions may miss a direct implementation mechanism.

Primary experiment:

- identify top-10 PERMCO companies each month using the broad market-state universe;
- remove all securities belonging to those companies;
- re-form momentum quintiles;
- compare the new VW spread with baseline.

Robustness:
- top 5;
- top 20;
- EW spread;
- Rank IC.

Do not promote top-20 merely because its p-value is smaller.

## 6. Mega-cap decomposition

This should be a central section of the paper.

Define:

[
TotalChange = Reformed-Baseline
]

[
DirectWeightEffect = FixedRanks-Baseline
]

[
ReRankingEffect = Reformed-FixedRanks.
]

Explain that the fixed-rank portfolio preserves original Q1/Q5 membership and removes mega-cap securities only within those existing quintiles.

The decomposition identifies whether mega-cap exclusion works through:

- economic portfolio weights;
- signal ordering / quintile-boundary changes.

This is the strongest mechanism result and should receive a dedicated table and figure.

## 7. Industry neutralisation

Primary:

- map contemporaneous SIC to FF49;
- subtract equal-weight industry-month mean momentum;
- require at least 10 stocks in an industry-month;
- re-form global quintiles.

Robustness:
- within-industry percentile rank;
- ICBIndustry demean.

Report both portfolio returns and Rank IC. Emphasise that near-identical raw and neutralised Rank IC provides direct evidence about ranking quality.

## 8. Market-beta neutralisation

Explain ex-ante CAPM beta estimation:

[
R_{i,d}-R_{f,d}
=
alpha_{i,t}
+
eta_{i,t}(R_{m,d}-R_{f,d})
+
epsilon_{i,d}.
]

Specification:
- 252 CRSP market trading days;
- skip most recent 5 market trading days;
- minimum 126 valid paired observations;
- no winsorisation;
- no imputation.

Primary beta-neutral construction:

[
R^{BN}_{LS,t+1}
=
R^{Eligible}_{LS,t+1}
-
hateta_{LS,t}R^{MKT,excess}_{t+1}.
]

Distinguish:
- beta coverage effect;
- neutralisation effect.

Report:
- Q1 / Q5 ex-ante beta;
- net long-short beta;
- raw vs beta-neutral spread;
- HAC inference on the neutralisation effect;
- ex-post realised market beta before / after hedging;
- leg-rescaling robustness.

Explain clearly that ex-ante neutrality does not guarantee zero ex-post beta.

## 9. Integrated interpretation

The synthesis should separate evidence into three questions.

### Did concentration destroy momentum ranking ability?
Evidence:
- Rank IC weak but positive;
- little Rank-IC change after mega-cap exclusion;
- little Rank-IC change after industry neutralisation.

Conclusion:
No strong evidence of systematic ranking deterioration.

### Does concentration affect value-weighted implementation?
Evidence:
- ex-mega-cap VW spread rises;
- EW spread changes little;
- decomposition attributes almost the entire change to direct weights.

Conclusion:
This is the strongest supported mechanism.

### Are systematic exposures the main explanation?
Evidence:
- industry neutralisation does not improve performance;
- beta neutralisation changes realised exposure but return effects are imprecise.

Conclusion:
Industry and market beta do not reveal a large hidden momentum premium.

## 10. Limitations

Must include:

- 2000-2025 sample only;
- momentum-only first research version;
- 312 monthly observations limit time-series power;
- concentration is highly persistent and trending;
- observational design, not causal identification;
- no full transaction-cost implementation yet;
- ex-ante beta estimates are noisy and time-varying;
- some economically meaningful estimates have wide confidence intervals;
- robustness specifications must not be interpreted as independent tests;
- value-weighted portfolios can be dominated by a small number of firms.

## 11. Conclusion

The conclusion should be modest.

Recommended core message:

> The evidence does not indicate that rising US market concentration systematically destroys the information in cross-sectional momentum rankings. Instead, mega-cap concentration appears primarily to alter the realised performance of value-weighted implementations through portfolio weights. Industry and market-beta controls do not reveal a robust hidden momentum premium. The distinction between signal quality and portfolio construction is therefore central when evaluating cross-sectional strategies in an increasingly concentrated equity market.

---

# 2. Required final tables

## Table 1 — Sample and baseline

Include:
- sample dates;
- formation rows;
- unique PERMNO;
- valid momentum observations;
- average / median monthly investable-stock count;
- Rank IC mean;
- VW Q5-Q1 mean;
- EW Q5-Q1 mean;
- HAC6 t / p / CI;
- HAC12 p.

## Table 2 — Aggregate concentration tests

Rows:
- Top10 -> VW spread;
- Top10 + linear trend;
- HHI -> VW spread;
- Top10 -> EW spread;
- Top10 -> Rank IC;
- lagged Top10 -> VW spread.

Columns:
- coefficient scaling;
- estimate;
- HAC SE;
- t;
- p;
- 95% CI;
- N.

## Table 3 — Mega-cap exclusion and decomposition

Panel A:
- baseline;
- ex-Top5;
- ex-Top10;
- ex-Top20;
- exclusion-minus-baseline effect;
- HAC6 / HAC12.

Panel B:
- DirectWeightEffect;
- ReRankingEffect;
- TotalChange;
- HAC6 / HAC12.

Panel C:
- Q1 Top10 weight share;
- Q5 Top10 weight share;
- return contribution difference.

## Table 4 — Neutralisation results

Rows:
- raw VW momentum;
- FF49-neutral VW;
- FF49 change;
- raw Rank IC;
- FF49-neutral Rank IC;
- beta-eligible raw;
- beta-neutral;
- beta neutralisation effect;
- leg-rescaled robustness.

Also report:
- ex-post market beta raw;
- ex-post market beta beta-neutral.

---

# 3. Required final figures

## Figure 1 — US market concentration, 2000-2025
Top-10 share over time. Optionally include HHI / effective number as a second panel or appendix figure.

## Figure 2 — Cumulative momentum spread
Cumulative wealth path of:
- baseline VW Q5-Q1;
- equal-weight Q5-Q1.

This is descriptive, not a claim of tradable wealth after costs.

## Figure 3 — Mega-cap exclusion comparison
Cumulative or rolling comparison:
- baseline VW;
- ex-Top10 VW.

The caption should make clear that statistical inference is performed on monthly differences, not visual separation.

## Figure 4 — Mega-cap mechanism decomposition
Bar chart of:
- DirectWeightEffect;
- ReRankingEffect;
- TotalChange.

This is likely the most important mechanism figure.

## Figure 5 — Beta exposure before and after neutralisation
Time series or summary showing:
- ex-ante Beta_LS;
- zero line;
and/or a concise bar/table visual of ex-post market beta raw vs beta-neutral.

---

# 4. Appendix material

Recommended appendix:
- data-field definitions;
- exact WRDS query logic;
- daily duplicate audit;
- momentum extreme-value validation;
- concentration market-state vs investable-universe comparison;
- timing robustness;
- FF49 mapping coverage;
- beta coverage / beta distribution;
- additional Top5 / Top20 / ICB / percentile robustness.

---

# 5. Evidence still needed before final prose is frozen

The final report should be written from generated tables rather than remembered screenshots.

Run the dedicated final-results notebook and provide its outputs. Specifically needed:

1. final consolidated baseline table;
2. final concentration regression table;
3. final mega-cap exclusion / decomposition table;
4. final industry-neutral table;
5. final beta-neutral table;
6. generated final figures.

Once these outputs are available, exact numbers in the report can be frozen without relying on manually transcribed intermediate results.
