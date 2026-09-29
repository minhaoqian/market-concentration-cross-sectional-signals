# Data Dictionary

## Status

**Version 0.1 — CRSP CIZ Daily Stock File schema confirmed from WRDS Variable Descriptions.**

This document records the exact source variables used or considered in the project. Variable names follow the CRSP Stock Version 2 (CIZ) interface currently available through WRDS.

Raw licensed WRDS data will not be committed to this public repository.

---

# 1. Source: CRSP Stock Version 2 (CIZ) — Daily Stock File

WRDS product: `crsp_a_stock`  
WRDS library: `crspa`  
WRDS file/query family observed in the interface: `wrds_dsfv2_query`

The Daily Stock File has coverage beginning in 1925 and is suitable for the project's daily-return-based signal construction.

## 1.1 Core identifiers

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `permno` | Integer | PERMNO | Primary security identifier / merge key |
| `permco` | Integer | PERMCO | Issuer-level identifier; useful when one company has multiple securities |
| `ticker` | Character | Ticker | Human-readable diagnostics only |
| `tradingsymbol` | Character | Trading Symbol | Diagnostics / identity checks |
| `cusip` | Character | CUSIP | Reference only; not primary key |
| `cusip9` | Character | CUSIP9 | Reference only |
| `issuernm` | Character | Issuer Name | Diagnostics and reporting |

**Primary identifier rule:** use `permno` for security-level time-series construction. Do not use ticker as the research key because tickers can change through time.

---

## 1.2 Security classification and sample construction

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `issuertype` | Character | Issuer Type | Security-type diagnostics |
| `securitytype` | Character | Security Type | Sample filtering / diagnostics |
| `securitysubtype` | Character | Security Sub-Type | Sample filtering / diagnostics |
| `sharetype` | Character | Share Type | Sample filtering / diagnostics |
| `securityactiveflg` | Character | Security Active Flag | Diagnostics only; do not use current-status information to create survivorship bias |
| `primaryexch` | Character | Primary Exchange | Exchange classification |
| `conditionaltype` | Character | Conditional Type | Trading-status / data-quality diagnostics |
| `exchangetier` | Character | Exchange Tier | Exchange diagnostics |
| `tradingstatusflg` | Character | Trading Status Flag | Data-quality / tradability diagnostics |
| `siccd` | Integer | SIC Code | Sector / industry mapping candidate |
| `naics` | Character | NAICS Code | Industry mapping candidate |
| `icbindustry` | Character | ICB Industry Code | Sector-neutralisation candidate |

### Important CIZ note

The initial pre-analysis plan used legacy CRSP conventions `SHRCD` and `EXCHCD`. In CIZ, security classification is exposed through newer fields such as `issuertype`, `securitytype`, `securitysubtype`, `sharetype`, and `primaryexch`.

Therefore the final common-stock / exchange filter must be defined from the official CIZ coding documentation before the production sample is built.

This is a **schema-driven revision**, not a result-driven change.

---

## 1.3 Dates

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `yyyymmdd` | Integer | YYYYMMDD - Daily Calendar Period Key | Date key / convenience |
| `dlycaldt` | Date | Daily Calendar Date | Primary daily time index |
| `secinfostartdt` | Date | Security Information Start Date | Point-in-time metadata validity |
| `secinfoenddt` | Date | Security Information End Date | Point-in-time metadata validity |
| `securitybegdt` | Date | Begin Date of Stock Data | Coverage diagnostics |
| `securityenddt` | Date | End Date of Stock Data | Coverage diagnostics |

---

## 1.4 Prices, returns, and market capitalisation

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `dlyprc` | Decimal | Daily Price | Price screens / diagnostics |
| `dlycap` | Decimal | Daily Capitalization | Market-cap weighting and concentration measurement candidate |
| `dlyprevprc` | Decimal | Daily Previous Price | Diagnostics |
| `dlyprevcap` | Decimal | Daily Previous Capitalization | Lagged-cap diagnostics / weighting candidate |
| `dlyret` | Decimal | Daily Total Return | **Primary daily return** for realised volatility and beta |
| `dlyretx` | Decimal | Daily Price Return | Price-return decomposition / diagnostics |
| `dlyreti` | Decimal | Daily Income Return | Income-return decomposition / diagnostics |
| `dlyvol` | Decimal | Daily Volume | Liquidity diagnostics |
| `dlyclose` | Decimal | Daily Close | Diagnostics / alternative price field |
| `dlylow` | Decimal | Daily Low | Not required for primary analysis |
| `dlyhigh` | Decimal | Daily High | Not required for primary analysis |
| `dlybid` | Decimal | Daily Bid | Potential microstructure robustness work |
| `dlyask` | Decimal | Daily Ask | Potential microstructure robustness work |

### Primary use

- **Low-volatility signal:** `dlyret`
- **Low-beta signal:** `dlyret`
- **Market-cap weighting / concentration:** likely `dlycap` or the corresponding monthly capitalization field once monthly schema is confirmed
- **$5 price screen:** likely monthly price field; `dlyprc` may be used for diagnostics

---

## 1.5 Return and capitalization flags

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `dlyprcflg` | Character | Daily Price Flag | Price data-quality checks |
| `dlycapflg` | Character | Daily Capitalization Flag | Capitalisation data-quality checks |
| `dlyprevprcflg` | Character | Daily Previous Price Flag | Diagnostics |
| `dlyprevcapflg` | Character | Daily Previous Capitalization Flag | Diagnostics |
| `dlyretmissflg` | Character | Daily Return Missing Flag | Missing-return handling |
| `dlyretdurflg` | Character | Daily Return Duration Flag | Return-period diagnostics |
| `dlydistretflg` | Character | Daily Distribution Return Impact Flag | Corporate-action / return diagnostics |

These flags should be inspected before deciding which observations are admissible for volatility and beta estimation.

---

## 1.6 Dividend / adjustment fields visible in the schema

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `dlyorddivamt` | Decimal | Daily Ordinary Dividend Amount | Diagnostics |
| `dlynonorddivamt` | Decimal | Daily Non-Ordinary Dividend Amount | Diagnostics |
| `dlyfacprc` | Decimal | Daily Factor To Adjust Price | Corporate-action diagnostics |

The primary signal calculations should normally use `dlyret` rather than reconstructing total return manually from price and dividend fields unless CRSP documentation indicates otherwise.

---

## 1.7 Delisting-related fields visible in the Daily Stock File

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `dlydelflg` | Character | Daily Delisting Flag | Identify delisting-linked observations |
| `delactiontype` | Character | Delisting Corporate Action Type | Delisting classification |
| `delstatustype` | Character | Delisting Completion Status Type | Delisting diagnostics |
| `delreasontype` | Character | Delisting Reason Type | Delisting diagnostics |
| `delpaymenttype` | Character | Delisting Payment Summary Type | Delisting diagnostics |

A separate **Delisting Information** table is available and will be documented separately. The production return-combination rule must follow the CIZ documentation rather than automatically copying the legacy SIZ `RET/DLRET` workflow.

---

# 2. Monthly Stock File — to be confirmed

The Monthly Stock File is the backbone of the primary monthly portfolio construction and will be documented after its CIZ Variable Descriptions are inspected.

Expected roles:

- monthly total return for momentum and reversal;
- month-end price for the price screen;
- month-end capitalization for market-cap weighting;
- monthly security classification where appropriate;
- monthly delisting handling;
- next-month realised portfolio return.

Do **not** assume legacy field names such as `ret`, `prc`, `shrout`, `shrcd`, or `exchcd` exist in the CIZ schema.

---

# 3. Other CRSP CIZ sources to document

## Delisting Information

Purpose:
- identify delisting events;
- ensure delisting-related returns are incorporated correctly;
- reduce delisting bias.

## Names

Purpose:
- point-in-time security identity;
- security classification;
- exchange / industry metadata if required.

## Share Outstanding

Purpose:
- audit or reconstruct market capitalisation if needed;
- validate capitalization fields.

## Daily / Monthly Stock Market Indexes

Purpose:
- broad market benchmark;
- market return series for beta estimation if chosen;
- benchmark diagnostics.

---

# 4. Data-timing rules

1. Information dated after portfolio formation may not be used to form the portfolio.
2. Security metadata must be matched using its valid point-in-time date range.
3. Market capitalisation used for weighting must be known at or before the formation date.
4. Ticker and issuer name are display fields, not stable research identifiers.
5. Missing-return and special-status flags must be handled explicitly rather than silently dropped.
6. Any CIZ-to-legacy mapping used from external examples must be checked against official CRSP documentation first.

---

# 5. Next schema checks

Before this dictionary becomes Version 1.0, inspect and document:

1. Monthly Stock File;
2. Delisting Information;
3. Names;
4. Share Outstanding;
5. Daily / Monthly Stock Market Indexes;
6. official CIZ code values for common-stock and exchange filters.
