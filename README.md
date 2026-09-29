# Market Concentration and Cross-Sectional Equity Signals

## Project Overview

This repository documents an empirical quantitative-finance research project on whether rising concentration in the US equity market changes the behaviour and measured performance of common cross-sectional equity signals.

The project is designed as a reproducible research workflow rather than a single backtest. It will document the research question, literature review, data construction, empirical design, robustness checks, code, results, and limitations.

## Working Research Question

**Does rising concentration in the US equity market alter the effectiveness of common cross-sectional equity signals, and do observed signal returns persist after controlling for sector, market-beta, and mega-cap exposures?**

## Initial Scope

The first version of the project will focus on price-based signals, with candidate signals including:

- Momentum
- Short-term reversal
- Low volatility
- Beta

Market concentration will be measured using transparent, pre-specified measures such as top-N market-cap share and the Herfindahl-Hirschman Index (HHI).

## Research Principles

The project will explicitly address:

- Survivorship bias
- Look-ahead bias
- Delisting bias
- Corporate-action adjustments
- Data quality and missingness
- Transaction costs
- Multiple testing and specification search
- Out-of-sample robustness

## Data

The preferred institutional data source is WRDS, subject to the University of Oxford subscription entitlements available to the researcher.

Raw licensed WRDS data will **not** be uploaded to this public repository. Code and documentation will instead describe how the research sample is constructed so that authorised users can reproduce the workflow with their own data access.

## Repository Structure

```text
docs/        Research design, literature review, logs, and data documentation
notebooks/   Exploratory and empirical analysis
src/         Reusable Python research code
results/     Tables, figures, and experiment registry
paper/       Final research report
data/        Local data directories; licensed/raw data excluded from Git
```

## Current Status

**Stage 1: Research design**

Current priority: formalise the motivation, research gap, hypotheses, empirical design, sample definition, and required data fields before running the main analysis.

## Reproducibility

Every final table and figure should be traceable from source data through documented transformations and code.

This repository is a research project in progress. Results and conclusions may change as the empirical design is refined and robustness checks are completed.
