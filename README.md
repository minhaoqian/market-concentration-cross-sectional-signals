# Market Concentration and Cross-Sectional Equity Signals

## Project Overview

This repository contains an empirical quantitative-finance study of how rising US equity-market concentration affects the measured performance and exposure structure of a cross-sectional momentum strategy.

The project separates three questions:

1. Does aggregate market concentration predict momentum performance?
2. Do mega-cap weights distort value-weighted momentum portfolios?
3. Do industry and market-beta neutralisation materially change the signal?

## Research Question

Does market concentration distort cross-sectional equity signals through changes in ranking ability, or mainly through portfolio weights and common exposures?

The current empirical version studies 12-2 momentum in depth.

## Main Findings

- Baseline momentum is positive but weak: the value-weighted Q5-Q1 spread is about 0.075% per month and the equal-weighted spread about 0.246% per month.
- Aggregate Top-10 market share and HHI do not robustly predict momentum performance.
- Excluding the Top 10 companies raises the value-weighted momentum spread by roughly 0.110% per month in point estimates.
- A fixed-rank decomposition shows that almost all of this change is a direct portfolio-weight effect, not a re-ranking effect.
- Fama-French 49 industry neutralisation leaves Rank IC essentially unchanged and does not improve momentum performance.
- Ex-ante market-beta neutralisation lowers the value-weighted return point estimate and materially reduces realised market exposure, but the return change is statistically imprecise.

Across the project, economically meaningful point estimates are often accompanied by wide confidence intervals. Conclusions are therefore framed around the structure of the evidence rather than significance hunting.

See docs/empirical_synthesis.md for the integrated interpretation.

## Data and Sample

The primary monthly sample spans 2000-2025 and uses CRSP Stock Version 2 (CIZ) through WRDS.

The investable universe applies US common-equity filters using CIZ classification fields, NYSE/NYSE American/NASDAQ listings, positive market capitalisation, a monthly NYSE 20th-percentile market-cap screen, and a $5 price screen.

Market concentration is measured on a broader market-state universe and aggregated to the PERMCO/company level before Top-N shares and HHI are computed.

Raw licensed WRDS data are intentionally excluded from the public repository.

## Signal

Primary signal: 12-2 momentum. At month-end t, total returns from t-12 through t-2 are compounded, t-1 is skipped, contiguous monthly history is required, quintiles are formed at t, and the portfolio is held during t+1.

Primary portfolios are value weighted. Equal-weighted portfolios and monthly Spearman Rank IC are used as robustness and diagnostic measures.

## Neutralisation and Exposure Tests

The current analysis includes broad market-concentration conditioning, timing robustness, Top-5/Top-10/Top-20 mega-cap exclusion, fixed-rank weight-vs-reranking decomposition, Fama-French 49 industry neutralisation, ICB-industry robustness, rolling daily CAPM beta estimation, ex-ante market-beta hedge overlay, long/short beta-rescaling robustness, and ex-post realised market-beta diagnostics.

## Inference

The inference convention was locked before the relevant results were examined: Newey-West/HAC lag 6 primary, lag 12 robustness, two-sided tests, and 95% confidence intervals.

## Current Status

Empirical analysis is substantially complete. Core data engineering, concentration measurement, momentum construction, baseline inference, mega-cap decomposition, industry neutralisation, and beta-neutralisation have all been implemented and validated.

Remaining work is primarily final result tables and figures, a concise robustness summary, transaction-cost / implementation discussion, the final research note or paper, and CV/interview packaging.

## Reproducibility

Methodological revisions and data issues are recorded in docs/research_log.md. Raw CRSP files are not committed, but the code documents the transformations required for authorised users to reproduce the analysis with their own WRDS access.