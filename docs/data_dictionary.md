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


---

# 6. Source: CRSP Stock Version 2 (CIZ) — Monthly Stock File

WRDS product: `crsp_a_stock`  
WRDS library: `crspa`  
WRDS file/query family observed in the interface: `wrds_msfv2_query`  
Coverage observed in WRDS: monthly calendar dates from 1925-12-31 through 2025-12-31.

The Monthly Stock File is the primary backbone for monthly signal formation, portfolio construction, concentration measurement, and next-month realised returns.

## 6.1 Core identifiers and metadata

Confirmed fields visible in the CIZ Monthly Stock File include:

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `permno` | Integer | PERMNO | Primary security identifier |
| `permco` | Integer | PERMCO | Issuer-level identifier |
| `ticker` | Character | Ticker | Human-readable diagnostics only |
| `tradingsymbol` | Character | Trading Symbol | Diagnostics |
| `issuernm` | Character | Issuer Name | Reporting / identity checks |
| `siccd` | Integer | SIC Code | Industry / sector mapping candidate |
| `naics` | Character | NAICS Code | Industry mapping candidate |
| `icbindustry` | Character | ICB Industry Code | Sector-neutralisation candidate |

The same point-in-time identifier rule applies as in the Daily Stock File: `permno` is the primary research key; ticker is not.

## 6.2 Dates and completeness

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `yyyymm` | Integer | YYYYMM - Monthly Calendar Period Key | Convenience month key |
| `mthcaldt` | Date | Monthly Calendar Date | Primary monthly time index |
| `mthcompflg` | Character | Monthly Completeness Flag | Data-quality checks |
| `mthcompsubflg` | Character | Monthly Completeness Sub-Flag | Data-quality checks |

## 6.3 Price, capitalization, returns, and volume

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `mthprc` | Decimal | Monthly Price | Primary month-end price screen |
| `mthprcflg` | Character | Monthly Price Flag | Price-quality check |
| `mthprcdt` | Date | Monthly Price Date | Timing validation |
| `mthdtflg` | Character | Monthly Price Date Flag | Timing / data-quality diagnostics |
| `mthdelflg` | Character | Monthly Delisting Flag | Identify delisting-linked monthly observations |
| `mthcap` | Decimal | Monthly Market Capitalization | **Primary market-cap field** for weighting and concentration |
| `mthprevprc` | Decimal | Monthly Previous Price | Diagnostics / lagged information |
| `mthprevprcflg` | Character | Monthly Previous Price Flag | Diagnostics |
| `mthprevdt` | Date | Monthly Previous Price Date | Timing diagnostics |
| `mthprevdtflg` | Character | Monthly Previous Date Flag | Timing diagnostics |
| `mthprevcap` | Decimal | Monthly Previous Total Capitalization | Candidate lagged weight field / diagnostics |
| `mthret` | Decimal | Monthly Total Return | **Primary monthly return** |
| `mthretx` | Decimal | Monthly Return Without Dividends | Return decomposition / diagnostics |
| `mthretflg` | Character | Monthly Return Flag | Return-quality / missingness checks |
| `mthdiscnt` | Integer | Monthly Distribution Count | Corporate-action diagnostics |
| `mthvol` | Decimal | Monthly Volume | Liquidity diagnostics |

## 6.4 Share information visible in the Monthly Stock File

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `shrstartdt` | Date | Share Information Start Date | Point-in-time validity |
| `shrenddt` | Date | Share Information End Date | Point-in-time validity |
| `shrout` | Integer | Shares Outstanding | Audit / market-cap reconstruction if needed |
| `shrsource` | Character | Share Change Source Type | Share-data diagnostics |
| `shrfactype` | Character | Share Factor Type | Corporate-action diagnostics |
| `shradrflg` | Character | Share ADR Flag | Sample diagnostics / potential ADR exclusion |

The presence of both `mthcap` and `shrout` means market capitalization does not need to be reconstructed manually for the primary specification unless validation checks reveal a reason to do so.

## 6.5 Distribution fields visible in the Monthly Stock File

The monthly schema also exposes distribution-related variables including:

- `disexdt` — Ex-Distribution Date
- `disseqnbr` — Distribution Sequence Number
- `disordinaryflg` — Distribution Ordinary Dividend Flag
- `distype` — Distribution Type
- `disfreqtype` — Distribution Frequency Type
- `dispaymenttype` — Distribution Payment Method Type
- `disdetailtype` — Distribution Detail Type
- `distaxtype` — Distribution Tax Status Type
- `disorigcurtype` — Distribution Original Currency Type
- `disdivamt` — Dividend Amount
- `disfacpr` — Factor To Adjust Price
- `disfacshr` — Factor To Adjust Shares

These fields are useful for corporate-action auditing, but the primary return signal should use `mthret` rather than manually reconstructing total return unless CRSP CIZ documentation requires otherwise.

## 6.6 Primary mapping from research design to monthly fields

The following primary mappings are now supported directly by the CIZ Monthly Stock File:

| Research component | Primary field(s) |
|---|---|
| Momentum | `mthret` |
| Short-term reversal | `mthret` |
| Next-month realised portfolio return | `mthret` |
| $5 price screen | `mthprc` |
| Market-cap weighting | `mthcap` |
| Top-10 concentration | `mthcap` |
| HHI concentration | `mthcap` |
| Delisting diagnostics | `mthdelflg` plus separate Delisting Information table |
| Liquidity diagnostics | `mthvol` |
| Industry / sector mapping candidate | `siccd`, `naics`, `icbindustry` |

## 6.7 Implications for the project design

1. **Momentum and reversal can be built entirely from monthly CIZ returns.**
2. **Market capitalization is directly available as `mthcap`.**
3. **The primary price screen can use `mthprc`.**
4. **The market-cap concentration measures can be computed directly from `mthcap`.**
5. **Shares outstanding are available for validation rather than mandatory reconstruction.**
6. **Monthly completeness, price, and return flags should be inspected before final missing-data rules are locked.**

---

# 7. Current preferred field set for the first monthly extraction

The first test extraction should be deliberately small and include only fields needed to validate the schema and sample logic.

Recommended fields:

- `permno`
- `permco`
- `mthcaldt`
- `ticker`
- `issuernm`
- `primaryexch`
- `securitytype`
- `securitysubtype`
- `sharetype`
- `siccd`
- `naics`
- `icbindustry`
- `mthprc`
- `mthprcflg`
- `mthcap`
- `mthprevcap`
- `mthret`
- `mthretx`
- `mthretflg`
- `mthdelflg`
- `mthvol`
- `shrout`
- `shradrflg`

Do not download the full history yet. The first extraction should use a short date range and be treated as a schema / quality-control test.


---

# 8. Source: CRSP Stock Version 2 (CIZ) — Delisting Information

WRDS product: `crsp_a_stock`  
WRDS library: `crspa`  
WRDS file observed in the interface: `stkdelists`  
Coverage observed in WRDS: delisting dates from 1962-06-24 through 2025-12-30.

This table is used to identify delisting events and recover delisting-related returns that may not be represented by an ordinary month-end continuation return.

## 8.1 Confirmed fields

| Variable | Type | WRDS description | Planned use |
|---|---|---|---|
| `primaryexch` | Character | Primary Exchange | Delisting-event diagnostics |
| `nasdissuno` | Integer | Nasdaq Issue Number | Reference only |
| `siccd` | Integer | SIC Code | Industry reference |
| `permno` | Integer | PERMNO | Primary merge key |
| `delistingdt` | Date | Delisting Date | Event date |
| `deldtprc` | Decimal | Delisting Date Price | Delisting price diagnostics |
| `deldtprcflg` | Character | Delisting Date Price Flag | Data-quality diagnostics |
| `delactiontype` | Character | Delisting Corporate Action Type | Event classification |
| `delstatustype` | Character | Delisting Completion Status Type | Event-status diagnostics |
| `delreasontype` | Character | Delisting Reason Type | Cause-of-delisting classification |
| `delpaymenttype` | Character | Delisting Payment Summary Type | Payment classification |
| `delpermno` | Integer | Delisting PERMNO | Delisting-security reference |
| `delpermco` | Integer | Delisting PERMCO | Delisting-company reference |
| `delret` | Decimal | Delisting Total Return | **Primary delisting-return field** |
| `delretmisstype` | Character | Delisting Return Missing Type | Missing-return classification |
| `delnextdt` | Date | Delisting Next Price Date | Post-delisting price reference |
| `delnextprc` | Decimal | Delisting Next Price | Post-delisting value diagnostics |
| `delnextprcflg` | Character | Delisting Next Price Flag | Data-quality diagnostics |
| `delamtdt` | Date | Delisting Amount Date | Cash/distribution timing |
| `deldivamt` | Decimal | Delisting Dividend Amount | Delisting distribution diagnostics |
| `deldistype` | Character | Delisting Distributions Type | Distribution classification |
| `deldlydt` | Date | Delisting Daily Date | Daily alignment field |

## 8.2 Primary research implication

The presence of `delret` confirms that delisting returns are explicitly available in CIZ.

The production holding-period return logic should therefore account for both:

- the ordinary monthly total return from the Monthly Stock File; and
- the delisting total return from Delisting Information where applicable.

The exact combination rule will be taken from the official CRSP CIZ documentation before implementation. We will **not** automatically copy the legacy SIZ formula without verifying that CIZ uses the same return semantics.

## 8.3 Missing delisting returns

`delretmisstype` must be examined whenever `delret` is missing.

The project will not silently replace missing delisting returns with zero.

Any imputation rule, if needed, must be:

1. justified from CRSP documentation or established literature;
2. specified before the main portfolio results are interpreted;
3. separately tested as a robustness choice where appropriate.

## 8.4 Merge logic — provisional

Primary merge key:

- `permno`

Time alignment:

- use `delistingdt` / relevant monthly date to attach the event to the correct holding period;
- validate against `mthdelflg` in the Monthly Stock File.

The exact merge code will be tested on a small date range before the full sample is downloaded.
