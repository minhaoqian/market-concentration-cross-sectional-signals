# Empirical Synthesis

## Research question

This project asks whether rising US equity-market concentration distorts the measured effectiveness of a cross-sectional momentum signal, and whether any distortion is better understood as a change in ranking ability or as a portfolio-implementation effect driven by mega-cap, industry, or market-beta exposures.

The primary signal is 12-2 momentum formed monthly on a point-in-time investable US common-equity universe. Primary portfolios are value weighted; equal-weighted portfolios and Rank IC are used to separate ranking quality from weighting effects.

## 1. Baseline momentum is positive but weak

- Mean monthly Rank IC is approximately 0.0077.
- The value-weighted Q5-Q1 spread averages approximately 0.075% per month.
- The equal-weighted spread averages approximately 0.246% per month.

Under the pre-specified Newey-West convention (HAC lag 6 primary, lag 12 robustness), none of these mean effects is statistically distinguishable from zero.

## 2. Aggregate market concentration does not robustly predict momentum performance

The primary continuous test regresses the value-weighted momentum spread on contemporaneous broad-market Top-10 company share at formation. The estimated slope is negative in the primary specification, but statistically imprecise. The conclusion is unchanged with HAC12, a linear time trend, HHI, equal-weighted momentum, Rank IC, or one-month-lagged concentration. Expanding-tertile regime summaries are also non-monotonic.

## 3. Mega-cap exclusion points to a portfolio-weight mechanism

- Baseline VW spread: approximately 0.075% per month.
- Excluding the Top 10 companies: approximately 0.184% per month.
- Change: approximately +0.110% per month.

Equal-weighted momentum and Rank IC barely change. A fixed-rank decomposition shows a direct weight effect of approximately +0.111% per month, a re-ranking effect of approximately -0.002% per month, and a total change of approximately +0.110% per month. Almost the entire change is therefore attributable to removing mega-cap portfolio-weight influence rather than changing the signal ordering.

## 4. Industry neutralisation does not improve the signal

Primary Fama-French 49 industry neutralisation slightly lowers the value-weighted momentum spread and leaves Rank IC almost unchanged. Within-industry percentile ranks and CRSP ICB-industry neutralisation lead to the same conclusion. The weak raw momentum result does not appear to be mainly a broad industry-common-trend effect.

## 5. Market-beta neutralisation changes exposure more than inference

Ex-ante stock beta is estimated from daily excess returns with a 252-market-trading-day CAPM window, a 5-day skip, and a 126-observation minimum. No winsorisation, clipping, or beta imputation is used.

Beta coverage is high and stable, averaging about 97.9% of the formation universe. Within the realised Q1 and Q5 momentum legs, beta coverage is complete, so the beta-coverage effect on the spread is zero.

- Raw / beta-eligible VW spread: approximately +0.075% per month.
- Beta-neutral spread: approximately -0.039% per month.
- Neutralisation effect: approximately -0.114% per month.

The return change is not statistically distinguishable from zero under HAC6 or HAC12. A separate long/short leg-rescaling robustness construction produces the same directional conclusion and is also statistically imprecise.

The ex-post market beta falls materially from roughly -0.38 for the raw strategy to roughly -0.16 after the ex-ante hedge, but is not eliminated. The correlation between ex-ante net beta and the following holding-month market excess return is only about 0.05, and beta by market-return quintile is non-monotonic.

## Integrated interpretation

The evidence points more strongly to a portfolio-implementation mechanism than to a deterioration in cross-sectional ranking ability.

- Aggregate concentration itself does not robustly predict momentum performance.
- Removing mega-caps improves value-weighted momentum in point estimates.
- That improvement is almost entirely a direct weight effect.
- Equal-weighted performance and Rank IC are much less affected.
- Industry neutralisation leaves ranking ability essentially unchanged.
- Beta neutralisation changes realised returns and reduces market exposure, but the return effect is noisy and statistically imprecise.

Taken together, rising concentration appears more relevant to how a value-weighted cross-sectional signal is implemented than to whether the underlying momentum ranking continues to contain information.

## Limitations

1. The project studies one primary signal in depth rather than claiming a universal result across all cross-sectional signals.
2. The sample contains only about 300 monthly performance observations, which limits time-series power.
3. Beta is estimated, time varying, and imperfectly hedged out of sample.
4. Transaction costs are not yet incorporated into the main reported spreads.
5. The study is descriptive/empirical rather than a causal identification of why market concentration changes over time.
6. Licensed CRSP raw data cannot be included in the public repository.

## Recommended final framing

Rising US equity-market concentration does not appear to systematically destroy momentum's cross-sectional ranking ability. Its more visible effect is on the implementation of value-weighted portfolios: mega-cap securities can materially alter realised long-short returns through their weights, while industry and beta neutralisation do not reveal a hidden, statistically robust momentum premium.