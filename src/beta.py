"""Ex-ante CAPM beta estimation for monthly portfolio formation.

Methodology locked before observing beta-neutral portfolio results:
- daily CRSP stock total returns;
- CRSP value-weighted market return including dividends;
- Kenneth French daily risk-free rate;
- excess-return CAPM OLS;
- 252 CRSP market trading-day window;
- skip the 5 market trading days immediately before formation;
- require at least 126 valid paired observations;
- no beta winsorisation or imputation.

The window is defined on the CRSP market calendar, not on each stock's own
observed-return sequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BetaConfig:
    lookback_days: int = 252
    skip_days: int = 5
    min_obs: int = 126


def _prepare_market_calendar(market_rf: pd.DataFrame) -> pd.DataFrame:
    required = {"Date", "MarketRet", "RF", "MarketExcessRet"}
    missing = required.difference(market_rf.columns)
    if missing:
        raise ValueError(f"Missing market/RF columns: {sorted(missing)}")

    cal = market_rf[list(required)].copy()
    cal["Date"] = pd.to_datetime(cal["Date"], errors="raise")
    cal = cal.sort_values("Date").reset_index(drop=True)

    if cal["Date"].duplicated().any():
        raise ValueError("Market calendar is not unique on Date.")

    cal["MarketIdx"] = np.arange(len(cal), dtype=np.int64)
    return cal


def _attach_daily_excess_returns(
    daily_stock: pd.DataFrame,
    market_calendar: pd.DataFrame,
) -> pd.DataFrame:
    required = {"PERMNO", "DlyCalDt", "DlyRet"}
    missing = required.difference(daily_stock.columns)
    if missing:
        raise ValueError(f"Missing daily-stock columns: {sorted(missing)}")

    stock = daily_stock[["PERMNO", "DlyCalDt", "DlyRet"]].copy()
    stock["DlyCalDt"] = pd.to_datetime(stock["DlyCalDt"], errors="raise")

    if stock.duplicated(["PERMNO", "DlyCalDt"]).any():
        raise ValueError("Daily stock input is not unique on PERMNO-date.")

    joined = stock.merge(
        market_calendar[["Date", "MarketIdx", "RF", "MarketExcessRet"]],
        left_on="DlyCalDt",
        right_on="Date",
        how="inner",
        validate="many_to_one",
    )

    joined["DlyRet"] = pd.to_numeric(joined["DlyRet"], errors="coerce")
    joined["StockExcessRet"] = joined["DlyRet"] - joined["RF"]

    valid = (
        joined["StockExcessRet"].notna()
        & joined["MarketExcessRet"].notna()
    )
    out = joined.loc[
        valid,
        ["PERMNO", "MarketIdx", "MarketExcessRet", "StockExcessRet"]
    ].copy()

    return out.sort_values(["PERMNO", "MarketIdx"]).reset_index(drop=True)


def _formation_window_bounds(
    formation: pd.DataFrame,
    market_calendar: pd.DataFrame,
    config: BetaConfig,
) -> pd.DataFrame:
    required = {"PERMNO", "MthCalDt"}
    missing = required.difference(formation.columns)
    if missing:
        raise ValueError(f"Missing formation columns: {sorted(missing)}")

    out = formation[["PERMNO", "MthCalDt"]].copy()
    out["MthCalDt"] = pd.to_datetime(out["MthCalDt"], errors="raise")

    market_dates = market_calendar["Date"].to_numpy(dtype="datetime64[ns]")
    formation_dates = out["MthCalDt"].to_numpy(dtype="datetime64[ns]")

    # Most recent market trading day strictly before formation.
    prev_market_idx = np.searchsorted(
        market_dates, formation_dates, side="left"
    ) - 1

    # Skip the five immediately preceding market trading days.
    end_idx = prev_market_idx - config.skip_days
    start_idx = end_idx - config.lookback_days + 1

    out["WindowStartIdx"] = start_idx
    out["WindowEndIdx"] = end_idx
    out["WindowAvailable"] = start_idx >= 0
    return out


def estimate_monthly_capm_beta(
    formation: pd.DataFrame,
    daily_stock: pd.DataFrame,
    market_rf: pd.DataFrame,
    config: BetaConfig = BetaConfig(),
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Estimate one ex-ante CAPM beta per PERMNO-formation month.

    Uses cumulative sufficient statistics within each PERMNO so the fixed
    market-calendar window can be evaluated without repeatedly scanning the
    full daily panel.

    Returns
    -------
    beta : DataFrame
        PERMNO, MthCalDt, Beta, BetaNObs, window diagnostics.
    audit : DataFrame
        Monthly coverage summary.
    """
    if config.lookback_days <= 1:
        raise ValueError("lookback_days must exceed 1.")
    if config.skip_days < 0:
        raise ValueError("skip_days must be non-negative.")
    if config.min_obs < 2 or config.min_obs > config.lookback_days:
        raise ValueError("min_obs must lie between 2 and lookback_days.")

    cal = _prepare_market_calendar(market_rf)
    windows = _formation_window_bounds(formation, cal, config)
    daily = _attach_daily_excess_returns(daily_stock, cal)

    rows = []

    daily_groups = {
        int(k): g for k, g in daily.groupby("PERMNO", sort=False)
    }

    for permno, fgrp in windows.groupby("PERMNO", sort=False):
        g = daily_groups.get(int(permno))

        if g is None or g.empty:
            tmp = fgrp.copy()
            tmp["Beta"] = np.nan
            tmp["BetaNObs"] = 0
            tmp["BetaDenom"] = np.nan
            rows.append(tmp)
            continue

        idx = g["MarketIdx"].to_numpy(dtype=np.int64)
        x = g["MarketExcessRet"].to_numpy(dtype=float)
        y = g["StockExcessRet"].to_numpy(dtype=float)

        # Prefix sums; element j stores sum through j-1.
        c_n = np.arange(len(g) + 1, dtype=np.int64)
        c_x = np.concatenate(([0.0], np.cumsum(x)))
        c_y = np.concatenate(([0.0], np.cumsum(y)))
        c_xy = np.concatenate(([0.0], np.cumsum(x * y)))
        c_x2 = np.concatenate(([0.0], np.cumsum(x * x)))

        lo_idx = fgrp["WindowStartIdx"].to_numpy(dtype=np.int64)
        hi_idx = fgrp["WindowEndIdx"].to_numpy(dtype=np.int64)

        left = np.searchsorted(idx, lo_idx, side="left")
        right = np.searchsorted(idx, hi_idx, side="right")

        n = c_n[right] - c_n[left]
        sx = c_x[right] - c_x[left]
        sy = c_y[right] - c_y[left]
        sxy = c_xy[right] - c_xy[left]
        sx2 = c_x2[right] - c_x2[left]

        denom = sx2 - (sx * sx / np.where(n > 0, n, 1))
        numer = sxy - (sx * sy / np.where(n > 0, n, 1))

        beta = np.full(len(fgrp), np.nan, dtype=float)
        ok = (
            fgrp["WindowAvailable"].to_numpy(dtype=bool)
            & (n >= config.min_obs)
            & np.isfinite(denom)
            & (denom > 0)
        )
        beta[ok] = numer[ok] / denom[ok]

        tmp = fgrp.copy()
        tmp["Beta"] = beta
        tmp["BetaNObs"] = n
        tmp["BetaDenom"] = denom
        rows.append(tmp)

    beta = pd.concat(rows, ignore_index=True).sort_values(
        ["MthCalDt", "PERMNO"]
    ).reset_index(drop=True)

    audit = (
        beta.groupby("MthCalDt", sort=True)
        .agg(
            FormationN=("PERMNO", "size"),
            ValidBetaN=("Beta", lambda s: int(s.notna().sum())),
            MeanObs=("BetaNObs", "mean"),
            MedianObs=("BetaNObs", "median"),
        )
        .reset_index()
    )
    audit["ValidBetaPct"] = audit["ValidBetaN"] / audit["FormationN"]

    return beta, audit


def beta_distribution(beta: pd.DataFrame) -> pd.Series:
    """Descriptive diagnostics for valid ex-ante beta estimates."""
    s = pd.to_numeric(beta["Beta"], errors="coerce").dropna()
    if s.empty:
        return pd.Series(dtype=float)

    return s.describe(
        percentiles=[0.01, 0.05, 0.50, 0.95, 0.99]
    )
