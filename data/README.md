# Data Directory

Raw CRSP / WRDS files are licensed and are not committed to GitHub.

Expected local raw inputs:

```text
data/raw/
├── monthly_stock_common_equity_2000_2025_prod_v1.csv.gz
├── daily_stock_naq_1998_2025_prod_v1.csv.gz
├── daily_crsp_vw_market_1998_2025_v1.csv.gz
├── F-F_Research_Data_Factors_daily.csv
└── F-F_Momentum_Factor.csv
```

The daily stock filename uses `naq` rather than `common_equity` because the WRDS daily query was exchange-filtered to NYSE/AMEX/NASDAQ and common-equity eligibility is imposed by matching to the monthly formation universe.

`data/interim/` and `data/processed/` are available for local cached outputs and are also gitignored.
