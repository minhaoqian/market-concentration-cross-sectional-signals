"""Market-concentration measures for the cleaned monthly equity panel.

Primary concentration is measured at the company level (PERMCO), not the
individual security level (PERMNO). This prevents multiple listed share classes
of the same economic company from being counted as separate firms.

Example: Alphabet's Class A shares (GOOGL) and Class C shares (GOOG) are
separate listed securities with different voting rights, but both represent
economic claims on Alphabet Inc. For market-concentration measurement, their
market capitalisations are aggregated to the same PERMCO before Top-N shares
and HHI are calculated.

Security-level concentration remains available as a robustness measure.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED = {"PERMNO", "PERMCO", "MthCalDt", "MthCap"}


def _validate_panel(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["MthCalDt"] = pd.to_datetime(out["MthCalDt"], errors="raise")
    out["MthCap"] = pd.to_numeric(out["MthCap"], errors="coerce")

    if out.duplicated(["PERMNO", "MthCalDt"]).any():
        raise ValueError("Input panel is not unique on PERMNO + MthCalDt.")

    if out["MthCap"].isna().any() or (out["MthCap"] <= 0).any():
        raise ValueError("MthCap must be non-missing and strictly positive.")

    if out["PERMCO"].isna().any():
        raise ValueError("PERMCO is required for company-level concentration.")

    return out


def _company_panel(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate security-level observations to company-month observations."""
    panel = _validate_panel(df)

    # Representative security for diagnostics: the largest share class of each
    # company in each month. This affects labels only, not company market cap.
    reps = (
        panel.sort_values(
            ["MthCalDt", "PERMCO", "MthCap"],
            ascending=[True, True, False],
        )
        .drop_duplicates(["MthCalDt", "PERMCO"])
        [["MthCalDt", "PERMCO", "PERMNO"] + [
            c for c in ["Ticker", "IssuerNm", "PrimaryExch"] if c in panel.columns
        ]]
    )

    company = (
        panel.groupby(["MthCalDt", "PERMCO"], as_index=False)
        .agg(
            CompanyMarketCap=("MthCap", "sum"),
            N_ShareClasses=("PERMNO", "nunique"),
        )
    )

    company = company.merge(
        reps,
        on=["MthCalDt", "PERMCO"],
        how="left",
        validate="one_to_one",
    )

    return company


def calculate_monthly_concentration(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate primary company-level monthly concentration measures.

    Returns one row per month with:
    - Top-5 company market-cap share
    - Top-10 company market-cap share
    - company-level HHI
    - effective number of firms = 1 / HHI
    - number of firms
    - number of listed securities
    - aggregate market capitalisation
    """
    panel = _validate_panel(df)
    company = _company_panel(panel)

    company["TotalMarketCap"] = company.groupby("MthCalDt")[
        "CompanyMarketCap"
    ].transform("sum")
    company["MarketWeight"] = company["CompanyMarketCap"] / company["TotalMarketCap"]

    weight_sums = company.groupby("MthCalDt")["MarketWeight"].sum()
    if not np.allclose(weight_sums.to_numpy(), 1.0, atol=1e-10):
        raise AssertionError("Monthly company weights do not sum to one.")

    ranked = company.sort_values(
        ["MthCalDt", "CompanyMarketCap"], ascending=[True, False]
    ).copy()
    ranked["SizeRank"] = ranked.groupby("MthCalDt").cumcount() + 1

    firm_summary = (
        company.groupby("MthCalDt")
        .agg(
            N_Firms=("PERMCO", "nunique"),
            Aggregate_MarketCap=("CompanyMarketCap", "sum"),
            HHI=("MarketWeight", lambda x: float(np.square(x).sum())),
        )
        .reset_index()
    )

    security_counts = (
        panel.groupby("MthCalDt")["PERMNO"]
        .nunique()
        .rename("N_Securities")
        .reset_index()
    )

    top5 = (
        ranked[ranked["SizeRank"] <= 5]
        .groupby("MthCalDt")["MarketWeight"]
        .sum()
        .rename("Top5Share")
        .reset_index()
    )
    top10 = (
        ranked[ranked["SizeRank"] <= 10]
        .groupby("MthCalDt")["MarketWeight"]
        .sum()
        .rename("Top10Share")
        .reset_index()
    )

    summary = firm_summary.merge(
        security_counts, on="MthCalDt", how="left", validate="one_to_one"
    )
    summary = summary.merge(top5, on="MthCalDt", how="left", validate="one_to_one")
    summary = summary.merge(top10, on="MthCalDt", how="left", validate="one_to_one")
    summary["EffectiveNumberOfFirms"] = 1.0 / summary["HHI"]

    return summary[
        [
            "MthCalDt",
            "N_Firms",
            "N_Securities",
            "Aggregate_MarketCap",
            "Top5Share",
            "Top10Share",
            "HHI",
            "EffectiveNumberOfFirms",
        ]
    ].sort_values("MthCalDt").reset_index(drop=True)


def calculate_security_level_concentration(df: pd.DataFrame) -> pd.DataFrame:
    """Robustness measure using listed securities (PERMNO) as separate units."""
    panel = _validate_panel(df)

    panel["TotalMarketCap"] = panel.groupby("MthCalDt")["MthCap"].transform("sum")
    panel["MarketWeight"] = panel["MthCap"] / panel["TotalMarketCap"]

    ranked = panel.sort_values(
        ["MthCalDt", "MthCap"], ascending=[True, False]
    ).copy()
    ranked["SizeRank"] = ranked.groupby("MthCalDt").cumcount() + 1

    summary = (
        panel.groupby("MthCalDt")
        .agg(
            N_Securities=("PERMNO", "nunique"),
            Aggregate_MarketCap=("MthCap", "sum"),
            HHI=("MarketWeight", lambda x: float(np.square(x).sum())),
        )
        .reset_index()
    )

    top5 = (
        ranked[ranked["SizeRank"] <= 5]
        .groupby("MthCalDt")["MarketWeight"]
        .sum()
        .rename("Top5Share")
        .reset_index()
    )
    top10 = (
        ranked[ranked["SizeRank"] <= 10]
        .groupby("MthCalDt")["MarketWeight"]
        .sum()
        .rename("Top10Share")
        .reset_index()
    )

    summary = summary.merge(top5, on="MthCalDt", how="left", validate="one_to_one")
    summary = summary.merge(top10, on="MthCalDt", how="left", validate="one_to_one")
    summary["EffectiveNumberOfSecurities"] = 1.0 / summary["HHI"]

    return summary.sort_values("MthCalDt").reset_index(drop=True)


def largest_firms_by_month(
    df: pd.DataFrame,
    n: int = 10,
    months: Iterable[pd.Timestamp | str] | None = None,
) -> pd.DataFrame:
    """Diagnostic table of the largest n companies in selected months."""
    if n <= 0:
        raise ValueError("n must be positive.")

    company = _company_panel(df)

    if months is not None:
        month_set = {pd.Timestamp(m) for m in months}
        company = company[company["MthCalDt"].isin(month_set)].copy()

    company["TotalMarketCap"] = company.groupby("MthCalDt")[
        "CompanyMarketCap"
    ].transform("sum")
    company["MarketWeight"] = company["CompanyMarketCap"] / company["TotalMarketCap"]

    cols = [
        "MthCalDt",
        "PERMCO",
        "CompanyMarketCap",
        "MarketWeight",
        "N_ShareClasses",
        "PERMNO",
    ]
    for optional in ["Ticker", "IssuerNm", "PrimaryExch"]:
        if optional in company.columns:
            cols.append(optional)

    return (
        company.sort_values(
            ["MthCalDt", "CompanyMarketCap"], ascending=[True, False]
        )
        .groupby("MthCalDt", group_keys=False)
        .head(n)[cols]
        .reset_index(drop=True)
    )


# Backward-compatible alias for earlier notebook code.
largest_stocks_by_month = largest_firms_by_month


if __name__ == "__main__":
    INPUT = Path("data/processed/monthly_clean_v1.csv.gz")
    OUTPUT = Path("results/tables/monthly_concentration_v1.csv")

    panel = pd.read_csv(INPUT, low_memory=False)
    concentration = calculate_monthly_concentration(panel)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    concentration.to_csv(OUTPUT, index=False)
    print(concentration.tail().to_string(index=False))
