# Sample Construction

## Status

**Version 0.1 — defined before the main empirical results are generated.**

This document records the rules used to transform raw CRSP CIZ observations into the monthly US common-equity research panel.

The guiding principle is that every exclusion must be economically or data-structurally justified and fixed before inspecting the main strategy results.

---

# 1. Source Data

Primary source:

- CRSP Stock Version 2 (CIZ)
- Monthly Stock File
- Daily Stock File
- Delisting Information

The monthly panel is the backbone of the research sample. Daily data are used for volatility and beta estimation.

Raw licensed WRDS files remain local and are not committed to the public repository.

---

# 2. Primary Security Identifier

Use **PERMNO** as the primary security-level identifier.

Reasons:

- PERMNO is designed to remain stable through ticker and name changes.
- ticker is retained only for human-readable diagnostics.
- PERMCO may be used for issuer-level diagnostics where a company has multiple traded securities.

The primary monthly key is therefore:

**PERMNO + MthCalDt**

The production monthly panel must contain at most one observation per key.

---

# 3. CIZ Common-Stock Filter

The primary common-stock universe follows the official WRDS CIZ-to-SIZ mapping for legacy CRSP share codes 10 and 11.

Retain observations satisfying:

- ShareType = NS
- SecurityType = EQTY
- SecuritySubType = COM
- USIncFlg = Y
- IssuerType in {ACOR, CORP}

This maps to the traditional US ordinary-common-stock universe represented by legacy share codes 10 and 11.

This filter deliberately excludes, among other categories:

- ETFs
- closed-end funds
- ADR-type shares
- REIT share-code categories outside the legacy 10/11 mapping
- non-US incorporated issuers
- other non-common security structures

Any future expansion beyond this universe must be reported as a robustness or exploratory specification.

---

# 4. Exchange Filter

The primary sample is restricted to the three traditional major US exchanges used in the legacy CRSP EXCHCD 1/2/3 universe.

Retain:

- PrimaryExch = N — NYSE
- PrimaryExch = A — NYSE MKT / NYSE American
- PrimaryExch = Q — NASDAQ

Exclude from the primary sample:

- R — Arca
- B — Cboe BZX
- I — IEX
- X — Other

These excluded exchanges may be revisited only as a robustness extension.

---

# 5. Exact Duplicate Handling

A 2024 test extraction using the common-stock CIZ filter produced:

- 47,143 rows
- 4,153 unique PERMNO values
- 199 rows belonging to duplicated PERMNO-month keys
- 99 duplicated PERMNO-month groups
- 98 groups containing two rows
- 1 group containing three rows

After distribution fields were removed from the query, **all duplicated rows were exact full-row duplicates**.

Therefore the production monthly pipeline will:

1. remove exact full-row duplicates;
2. verify that PERMNO + MthCalDt is unique afterwards;
3. halt with an error if any non-identical duplicate PERMNO-month key remains.

The pipeline must never silently keep the first row of a non-identical duplicated key.

This rule is intentionally stricter than an unconditional drop_duplicates on the key.

---

# 6. Valid Monthly Observation Requirements

Before signal construction, a monthly observation must have:

- valid PERMNO;
- valid MthCalDt;
- valid MthPrc where a price screen is required;
- valid MthCap where market-cap weighting or concentration measurement is required.

Return availability is handled signal-by-signal rather than by dropping every row with a missing MthRet immediately.

Reason:

A missing monthly return can arise from entry, exit, delisting, or other data states that must be diagnosed before exclusion.

MthRetFlg and MthDelFlg will therefore be retained during cleaning.

---

# 7. Price Screen

Primary analysis requires:

**MthPrc >= $5**

The screen is applied at the portfolio-formation month-end.

Purpose:

- reduce microstructure effects;
- reduce dominance by very low-priced securities;
- improve investability of the research universe.

The $5 threshold is a pre-specified implementation choice, not a result-driven threshold.

Robustness analysis will include removing the price screen.

---

# 8. NYSE Market-Capitalisation Breakpoint

The primary analysis excludes very small firms using a monthly NYSE market-cap breakpoint.

For each month t:

1. begin with securities passing the CIZ common-stock filter and N/A/Q exchange filter;
2. require valid positive MthCap;
3. identify NYSE securities using PrimaryExch = N;
4. calculate the 20th percentile of NYSE MthCap;
5. retain securities with MthCap at or above that monthly breakpoint;
6. also apply the $5 price screen.

The breakpoint is therefore time-varying and determined only from information available at the formation date.

Primary threshold:

**20th percentile of NYSE market capitalisation**

Planned robustness checks:

- 10th percentile;
- 30th percentile;
- no market-cap breakpoint;
- a separate large-cap-only universe.

---

# 9. Market Capitalisation

Primary market-cap variable:

**MthCap**

Uses:

- portfolio value weights;
- NYSE size breakpoint;
- Top-10 market-cap concentration;
- HHI concentration;
- size diagnostics.

MthPrevCap is retained for timing and weighting validation.

ShrOut and MthPrc may be used to audit MthCap but are not the primary market-cap construction.

Any WRDS/CRSP unit scaling used in reporting will be documented after validation against the CIZ data guide.

---

# 10. Monthly Returns

Primary monthly return field:

**MthRet**

Uses:

- momentum formation;
- short-term reversal;
- next-month realised stock return;
- portfolio return aggregation.

MthRetx is retained for diagnostics and return decomposition but is not the primary total-return measure.

Missing MthRet values will not automatically be replaced by zero.

---

# 11. Delisting Treatment

CRSP CIZ provides:

- MthDelFlg in the Monthly Stock File;
- DelRet in the Delisting Information table;
- additional delisting classification and missingness fields.

The project will explicitly account for delistings.

Important CIZ-specific rule:

The final return-construction logic must follow the official CIZ semantics because CIZ period returns can incorporate delisting returns where appropriate.

Therefore the project will not automatically apply the legacy SIZ formula:

(1 + RET) × (1 + DLRET) - 1

without first verifying whether that would double-count a return already included in MthRet.

Before the production pipeline is frozen:

1. inspect official CIZ return documentation;
2. inspect MthDelFlg coding;
3. compare affected observations with the separate Delisting Information table;
4. define a single non-double-counting rule;
5. document any missing-delisting-return treatment.

No missing DelRet value will be silently set to zero.

---

# 12. Monthly Panel Construction Order

The intended production order is:

1. load raw Monthly Stock File;
2. remove exact full-row duplicates;
3. assert no non-identical PERMNO-month duplicates remain;
4. apply CIZ common-stock filter;
5. apply PrimaryExch in {N, A, Q};
6. retain required data-quality flags and metadata;
7. require valid positive MthCap for size/concentration calculations;
8. compute the monthly NYSE 20% market-cap breakpoint;
9. apply market-cap breakpoint;
10. apply MthPrc >= $5 screen;
11. attach / validate delisting information;
12. construct signal-specific history requirements;
13. lag formation information appropriately;
14. calculate next-month realised outcomes.

The order will be implemented consistently through the full sample.

---

# 13. Daily Panel Construction

The Daily Stock File will use the same economic security universe where practical.

Daily fields required for the primary project include:

- PERMNO
- DlyCalDt
- DlyRet
- DlyPrc
- DlyCap
- relevant return and price flags
- point-in-time classification fields required for matching

The daily data will feed:

- 21-trading-day realised volatility;
- 252-trading-day rolling market beta.

Daily signal estimates will be attached to the monthly formation date without using observations after that date.

---

# 14. Data-Quality Assertions

The Python pipeline should stop rather than silently continue if any of the following fails:

- duplicated non-identical PERMNO-month rows remain;
- dates fail to parse;
- market-cap weights are constructed from non-positive MthCap;
- a future-dated observation enters a formation-period signal;
- portfolio ranks are calculated before the relevant lag is applied;
- concentration weights fail basic sum checks;
- a merge unexpectedly multiplies row counts.

These checks will be coded as explicit assertions where practical.

---

# 15. 2024 Test-Pull Evidence

The second 2024 Monthly Stock File test pull was deliberately restricted using the official CIZ US common-stock filter and excluded distribution fields.

Observed sample characteristics:

- 47,143 rows before exact deduplication;
- 4,153 unique securities by PERMNO;
- all retained observations matched EQTY / COM / NS under the query filter;
- all remaining duplicate PERMNO-month observations were exact row duplicates.

This test supports the production approach above but does not constitute an empirical result about factor performance.

---

# 16. Items Still to Freeze Before Version 1.0

1. exact CIZ delisting-return combination rule;
2. MthRetFlg admissibility rules;
3. MthPrcFlg admissibility rules;
4. MthCap unit validation;
5. final monthly sample end date;
6. daily-data missing-observation rules for volatility;
7. beta market-return and risk-free-rate series;
8. sector classification used for neutralisation.

Once these are resolved, this document will be promoted to Version 1.0 before the main results are produced.
