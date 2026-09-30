"""Mega-cap exclusion tests for momentum portfolio composition.

Pre-specified hierarchy:
- Primary: exclude the 10 largest PERMCO companies each formation month.
- Robustness: exclude top 5 and top 20.
- Mega-cap ranks are defined from the broad market-state universe.
- Signal values are not recomputed; only formation eligibility changes.
- Baseline and exclusion portfolios use the same momentum definition and
  formation-date investability screens.

Primary comparison:
    Delta_t = Spread_ExTop10_t - Spread_Baseline_t

Inference on Delta_t uses the already-fixed HAC6 primary / HAC12 robustness
convention.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.inference import primary_and_robustness_hac


def largest_permco_by_month(
    market_state: pd.DataFrame,
    n: int,
    date_col: str = "MthCalDt",
    permco_col: str = "PERMCO",
    cap_col: str = "MthCap",
) -> pd.DataFrame:
    """Return top-n PERMCO companies by aggregate market cap each month."""
    if n <= 0:
        raise ValueError("n must be positive.")

    required = {date_col, permco_col, cap_col}
    missing = required.difference(market_state.columns)
    if missing:
        raise ValueError(f"Missing market-state columns: {sorted(missing)}")

    x = market_state[[date_col, permco_col, cap_col]].copy()
    x[date_col] = pd.to_datetime(x[date_col], errors="raise")
    x[cap_col] = pd.to_numeric(x[cap_col], errors="coerce")
    x = x.dropna(subset=[permco_col, cap_col])
    x = x[x[cap_col] > 0]

    company = (
        x.groupby([date_col, permco_col], as_index=False)[cap_col]
        .sum()
        .rename(columns={cap_col: "CompanyMarketCap"})
    )

    ranked = company.sort_values(
        [date_col, "CompanyMarketCap"], ascending=[True, False]
    ).copy()
    ranked["MegaCapRank"] = ranked.groupby(date_col).cumcount() + 1

    return ranked[ranked["MegaCapRank"] <= n].reset_index(drop=True)


def exclude_top_permco(
    formation: pd.DataFrame,
    market_state: pd.DataFrame,
    n: int,
    date_col: str = "MthCalDt",
    permco_col: str = "PERMCO",
) -> pd.DataFrame:
    """Remove every security belonging to the top-n PERMCO companies at month t."""
    required = {date_col, permco_col}
    missing = required.difference(formation.columns)
    if missing:
        raise ValueError(f"Missing formation columns: {sorted(missing)}")

    top = largest_permco_by_month(
        market_state=market_state,
        n=n,
        date_col=date_col,
        permco_col=permco_col,
    )[[date_col, permco_col]].copy()
    top["IsMegaCapExcluded"] = True

    out = formation.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="raise")

    out = out.merge(
        top,
        on=[date_col, permco_col],
        how="left",
        validate="many_to_one",
    )

    out = out[out["IsMegaCapExcluded"].isna()].drop(
        columns=["IsMegaCapExcluded"]
    )
    return out.reset_index(drop=True)


def compare_spreads(
    baseline: pd.DataFrame,
    alternative: pd.DataFrame,
    date_col: str = "MthCalDt",
    spread_col: str = "Q5_minus_Q1",
    alt_label: str = "ExTop10",
) -> pd.DataFrame:
    """Align baseline and alternative spreads and calculate monthly delta."""
    left = baseline[[date_col, spread_col]].copy()
    right = alternative[[date_col, spread_col]].copy()

    left = left.rename(columns={spread_col: "BaselineSpread"})
    right = right.rename(columns={spread_col: f"{alt_label}Spread"})

    out = left.merge(
        right, on=date_col, how="inner", validate="one_to_one"
    ).sort_values(date_col).reset_index(drop=True)

    out[f"Delta_{alt_label}_Minus_Baseline"] = (
        out[f"{alt_label}Spread"] - out["BaselineSpread"]
    )
    return out


def delta_hac_summary(
    comparison: pd.DataFrame,
    alt_label: str = "ExTop10",
) -> pd.DataFrame:
    """HAC mean inference for the exclusion-minus-baseline spread difference."""
    col = f"Delta_{alt_label}_Minus_Baseline"
    if col not in comparison.columns:
        raise ValueError(f"{col} not found in comparison table.")
    return primary_and_robustness_hac(comparison[col])
