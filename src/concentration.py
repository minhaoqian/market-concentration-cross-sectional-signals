"""Market-concentration measures for the cleaned monthly equity panel."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED = {"PERMNO", "MthCalDt", "MthCap"}


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

    return out


def calculate_monthly_concentration(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate pre-specified monthly concentration measures.

    Returns one row per month with:
    - Top-5 market-cap share
    - Top-10 market-cap share
    - Herfindahl-Hirschman Index (HHI)
    - effective number of firms = 1 / HHI
    - number of securities
    - aggregate market capitalisation
    """
    panel = _validate_panel(df)

    panel["TotalMarketCap"] = panel.groupby("MthCalDt")["MthCap"].transform("sum")
    panel["MarketWeight"] = panel["MthCap"] / panel["TotalMarketCap"]

    weight_sums = panel.groupby("MthCalDt")["MarketWeight"].sum()
    if not np.allclose(weight_sums.to_numpy(), 1.0, atol=1e-10):
        raise AssertionError("Monthly market weights do not sum to one.")

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
    )
    top10 = (
        ranked[ranked["SizeRank"] <= 10]
        .groupby("MthCalDt")["MarketWeight"]
        .sum()
        .rename("Top10Share")
    )

    summary = summary.merge(top5, on="MthCalDt", how="left", validate="one_to_one")
    summary = summary.merge(top10, on="MthCalDt", how="left", validate="one_to_one")
    summary["EffectiveNumberOfFirms"] = 1.0 / summary["HHI"]

    return summary[
        [
            "MthCalDt",
            "N_Securities",
            "Aggregate_MarketCap",
            "Top5Share",
            "Top10Share",
            "HHI",
            "EffectiveNumberOfFirms",
        ]
    ].sort_values("MthCalDt").reset_index(drop=True)


def largest_stocks_by_month(
    df: pd.DataFrame,
    n: int = 10,
    months: Iterable[pd.Timestamp | str] | None = None,
) -> pd.DataFrame:
    """Diagnostic table of the largest n securities in selected months."""
    if n <= 0:
        raise ValueError("n must be positive.")

    panel = _validate_panel(df)

    if months is not None:
        month_set = {pd.Timestamp(m) for m in months}
        panel = panel[panel["MthCalDt"].isin(month_set)].copy()

    panel["TotalMarketCap"] = panel.groupby("MthCalDt")["MthCap"].transform("sum")
    panel["MarketWeight"] = panel["MthCap"] / panel["TotalMarketCap"]

    cols = ["MthCalDt", "PERMNO", "MthCap", "MarketWeight"]
    for optional in ["Ticker", "IssuerNm", "PrimaryExch"]:
        if optional in panel.columns:
            cols.append(optional)

    return (
        panel.sort_values(["MthCalDt", "MthCap"], ascending=[True, False])
        .groupby("MthCalDt", group_keys=False)
        .head(n)[cols]
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    INPUT = Path("data/processed/monthly_clean_v1.csv.gz")
    OUTPUT = Path("results/tables/monthly_concentration_v1.csv")

    panel = pd.read_csv(INPUT, low_memory=False)
    concentration = calculate_monthly_concentration(panel)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    concentration.to_csv(OUTPUT, index=False)
    print(concentration.tail().to_string(index=False))
