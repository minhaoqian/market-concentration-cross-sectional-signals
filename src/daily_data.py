"""Daily-data preparation and alignment for rolling beta estimation.

Inputs:
1. CRSP CIZ Daily Stock File.
2. CRSP Daily Stock Market Indexes.
3. Fama-French daily factors.

This module validates and aligns inputs only. It does not estimate beta.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


STOCK_REQUIRED = {"PERMNO", "DlyCalDt", "DlyRet"}
MARKET_REQUIRED = {"dlycaldt", "vwretd"}


def read_daily_stock(path: str | Path) -> pd.DataFrame:
    """Read CRSP CIZ daily stock data and remove only redundant exact rows."""
    df = pd.read_csv(path, low_memory=False)
    missing = STOCK_REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing daily-stock columns: {sorted(missing)}")

    out = df.copy()
    out["DlyCalDt"] = pd.to_datetime(out["DlyCalDt"], errors="raise")
    out["DlyRet"] = pd.to_numeric(out["DlyRet"], errors="coerce")

    if "PrimaryExch" in out.columns:
        bad = set(out["PrimaryExch"].dropna().astype(str).unique()) - {"N", "A", "Q"}
        if bad:
            raise ValueError(f"Unexpected exchange codes: {sorted(bad)}")

    # The production extract was audited before analysis: all duplicate
    # PERMNO-date rows were exact full-row duplicates and had identical DlyRet.
    # Retain one copy only, then fail loudly if any non-identical key duplicate
    # remains in a future extract.
    out = out.drop_duplicates().copy()

    if out.duplicated(["PERMNO", "DlyCalDt"]).any():
        sample = out.loc[
            out.duplicated(["PERMNO", "DlyCalDt"], keep=False)
        ].sort_values(["PERMNO", "DlyCalDt"]).head(20)
        raise ValueError(
            "Non-identical PERMNO-date duplicates remain after exact-row "
            "deduplication. Investigate before beta estimation.\n"
            f"{sample.to_string(index=False)}"
        )

    return out.sort_values(["PERMNO", "DlyCalDt"]).reset_index(drop=True)


def read_daily_market(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    missing = MARKET_REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing daily-market columns: {sorted(missing)}")

    out = df[["dlycaldt", "vwretd"]].copy()
    out = out.rename(columns={"dlycaldt": "Date", "vwretd": "MarketRet"})
    out["Date"] = pd.to_datetime(out["Date"], errors="raise")
    out["MarketRet"] = pd.to_numeric(out["MarketRet"], errors="coerce")

    if out["Date"].duplicated().any():
        raise ValueError("Daily market series has duplicate dates.")

    return out.sort_values("Date").reset_index(drop=True)


def read_fama_french_daily_rf(path: str | Path) -> pd.DataFrame:
    """Read Kenneth French daily factors and return RF in decimal units.

    Kenneth French CSV downloads include explanatory text before the actual
    comma-separated header, so the header row must be detected explicitly.
    """
    path = Path(path)

    with path.open("r", encoding="utf-8-sig", errors="replace") as fh:
        lines = fh.readlines()

    header_row = None
    for i, line in enumerate(lines):
        fields = [x.strip() for x in line.strip().split(",")]
        if "Mkt-RF" in fields and "RF" in fields:
            header_row = i
            break

    if header_row is None:
        raise ValueError(
            "Could not locate the Fama-French daily factor header "
            "(expected columns including Mkt-RF and RF)."
        )

    raw = pd.read_csv(path, skiprows=header_row)

    if "RF" not in raw.columns:
        raise ValueError("RF column not found in Fama-French daily file.")

    date_col = raw.columns[0]
    out = raw[[date_col, "RF"]].copy()
    out = out.rename(columns={date_col: "Date"})

    date_str = out["Date"].astype(str).str.strip()
    valid = date_str.str.fullmatch(r"\d{8}")
    out = out.loc[valid].copy()
    out["Date"] = pd.to_datetime(
        out["Date"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="raise",
    )

    # Kenneth French factor returns are reported in percent.
    out["RF"] = pd.to_numeric(out["RF"], errors="coerce") / 100.0

    if out["Date"].duplicated().any():
        raise ValueError("Fama-French RF series has duplicate dates.")

    return out.sort_values("Date").reset_index(drop=True)

def audit_daily_stock(df: pd.DataFrame) -> pd.Series:
    duplicated_key_rows = int(
        df.duplicated(["PERMNO", "DlyCalDt"], keep=False).sum()
    )
    exact_dupes = int(df.duplicated().sum())

    return pd.Series(
        {
            "rows": len(df),
            "unique_permno": df["PERMNO"].nunique(dropna=True),
            "trading_dates": df["DlyCalDt"].nunique(dropna=True),
            "start_date": df["DlyCalDt"].min(),
            "end_date": df["DlyCalDt"].max(),
            "missing_dlyret": int(df["DlyRet"].isna().sum()),
            "missing_dlyret_pct": 100 * df["DlyRet"].isna().mean(),
            "duplicate_permno_date_rows": duplicated_key_rows,
            "exact_duplicate_rows": exact_dupes,
            "min_return": df["DlyRet"].min(skipna=True),
            "max_return": df["DlyRet"].max(skipna=True),
        }
    )


def align_market_and_rf(
    market: pd.DataFrame,
    rf: pd.DataFrame,
    start: str = "1998-12-01",
    end: str = "2025-12-31",
) -> Tuple[pd.DataFrame, pd.Series]:
    m = market[market["Date"].between(pd.Timestamp(start), pd.Timestamp(end))].copy()
    r = rf[rf["Date"].between(pd.Timestamp(start), pd.Timestamp(end))].copy()

    aligned = m.merge(r, on="Date", how="inner", validate="one_to_one")
    aligned["MarketExcessRet"] = aligned["MarketRet"] - aligned["RF"]

    market_dates = set(m["Date"])
    rf_dates = set(r["Date"])

    audit = pd.Series(
        {
            "market_dates": len(market_dates),
            "rf_dates": len(rf_dates),
            "common_dates": len(aligned),
            "market_only_dates": len(market_dates - rf_dates),
            "rf_only_dates": len(rf_dates - market_dates),
            "start_common": aligned["Date"].min(),
            "end_common": aligned["Date"].max(),
            "missing_market_return": int(aligned["MarketRet"].isna().sum()),
            "missing_rf": int(aligned["RF"].isna().sum()),
            "rf_mean_daily": aligned["RF"].mean(),
            "rf_min_daily": aligned["RF"].min(),
            "rf_max_daily": aligned["RF"].max(),
            "market_return_mean_daily": aligned["MarketRet"].mean(),
            "market_return_min_daily": aligned["MarketRet"].min(),
            "market_return_max_daily": aligned["MarketRet"].max(),
        }
    )

    return aligned.sort_values("Date").reset_index(drop=True), audit


def formation_history_availability(
    formation_panel: pd.DataFrame,
    daily_stock: pd.DataFrame,
    lookback_days: int = 252,
    skip_days: int = 5,
    min_obs: int = 126,
) -> pd.DataFrame:
    """Diagnostic count of usable daily observations before formation dates."""
    formation = formation_panel[["PERMNO", "MthCalDt"]].copy()
    formation["MthCalDt"] = pd.to_datetime(formation["MthCalDt"], errors="raise")

    stock = daily_stock[["PERMNO", "DlyCalDt", "DlyRet"]].copy()
    stock = stock.sort_values(["PERMNO", "DlyCalDt"])

    rows = []
    grouped = {k: g for k, g in stock.groupby("PERMNO", sort=False)}

    for row in formation.itertuples(index=False):
        hist = grouped.get(row.PERMNO)
        if hist is None:
            valid_n = 0
        else:
            hist = hist[hist["DlyCalDt"] < row.MthCalDt]
            if len(hist) > skip_days:
                hist = hist.iloc[:-skip_days]
            else:
                hist = hist.iloc[0:0]
            hist = hist.tail(lookback_days)
            valid_n = int(hist["DlyRet"].notna().sum())

        rows.append(
            {
                "PERMNO": row.PERMNO,
                "MthCalDt": row.MthCalDt,
                "ValidDailyObs": valid_n,
                "MeetsMinObs": valid_n >= min_obs,
            }
        )

    return pd.DataFrame(rows)
