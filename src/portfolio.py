"""Baseline cross-sectional evaluation for pre-specified signals.

This module evaluates a signal before any conditioning on market concentration.

Primary baseline:
- monthly Spearman Rank IC;
- value-weighted quintile returns using formation-month market capitalisation;
- Q5 minus Q1 spread.

Equal-weighted quintile returns are retained as a robustness comparison.

Missing next-month returns are never replaced with zero. Portfolio returns are
computed over observed next-month returns and the observed market-cap coverage
is reported explicitly for every date/quintile so missingness remains visible.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def monthly_rank_ic(
    df: pd.DataFrame,
    signal_col: str = "Momentum_12_2",
    return_col: str = "NextMthRet",
    date_col: str = "MthCalDt",
    min_obs: int = 20,
) -> pd.DataFrame:
    """Calculate monthly Spearman rank IC between signal and next-month return."""
    required = {signal_col, return_col, date_col}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns for Rank IC: {sorted(missing)}")

    rows = []
    for date, g in df.groupby(date_col, sort=True):
        x = g[[signal_col, return_col]].dropna()
        n = len(x)
        ic = np.nan
        if n >= min_obs:
            ic = x[signal_col].corr(x[return_col], method="spearman")
        rows.append({date_col: date, "RankIC": ic, "N_Obs": n})

    return pd.DataFrame(rows).sort_values(date_col).reset_index(drop=True)


def _portfolio_return_one_group(
    g: pd.DataFrame,
    return_col: str,
    weight_col: str,
) -> pd.Series:
    """Return VW/EW returns plus next-return coverage diagnostics."""
    formation_n = len(g)
    observed = g.dropna(subset=[return_col]).copy()
    observed_n = len(observed)

    formation_cap = pd.to_numeric(g[weight_col], errors="coerce").sum(min_count=1)
    observed_cap = pd.to_numeric(
        observed[weight_col], errors="coerce"
    ).sum(min_count=1)

    vw = np.nan
    ew = np.nan

    if observed_n > 0:
        ew = observed[return_col].mean()

        w = pd.to_numeric(observed[weight_col], errors="coerce")
        r = pd.to_numeric(observed[return_col], errors="coerce")
        valid = w.notna() & r.notna() & (w > 0)
        if valid.any() and w[valid].sum() > 0:
            vw = np.average(r[valid], weights=w[valid])

    obs_cap_share = np.nan
    if pd.notna(formation_cap) and formation_cap > 0 and pd.notna(observed_cap):
        obs_cap_share = observed_cap / formation_cap

    return pd.Series(
        {
            "VW_Return": vw,
            "EW_Return": ew,
            "Formation_N": formation_n,
            "ObservedReturn_N": observed_n,
            "ObservedReturn_CountShare": (
                observed_n / formation_n if formation_n > 0 else np.nan
            ),
            "Formation_MarketCap": formation_cap,
            "ObservedReturn_MarketCap": observed_cap,
            "ObservedReturn_CapShare": obs_cap_share,
        }
    )


def quintile_returns(
    df: pd.DataFrame,
    quintile_col: str = "SignalQuintile",
    return_col: str = "NextMthRet",
    weight_col: str = "MthCap",
    date_col: str = "MthCalDt",
) -> pd.DataFrame:
    """Compute monthly value- and equal-weighted returns for signal quintiles."""
    required = {quintile_col, return_col, weight_col, date_col}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns for quintile returns: {sorted(missing)}")

    use = df.dropna(subset=[quintile_col]).copy()
    use[quintile_col] = use[quintile_col].astype(int)

    out = (
        use.groupby([date_col, quintile_col], observed=True, sort=True)
        .apply(
            _portfolio_return_one_group,
            return_col=return_col,
            weight_col=weight_col,
            include_groups=False,
        )
        .reset_index()
    )

    return out


def quintile_return_panel(
    qret: pd.DataFrame,
    return_col: str = "VW_Return",
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
) -> pd.DataFrame:
    """Pivot quintile returns wide and add Q5-Q1 spread."""
    wide = qret.pivot(
        index=date_col,
        columns=quintile_col,
        values=return_col,
    ).sort_index()

    wide = wide.rename(columns={q: f"Q{q}" for q in wide.columns})
    required = {"Q1", "Q5"}
    if not required.issubset(wide.columns):
        raise ValueError("Q1 and Q5 are required to construct the momentum spread.")

    wide["Q5_minus_Q1"] = wide["Q5"] - wide["Q1"]
    return wide.reset_index()


def baseline_summary(
    rank_ic: pd.DataFrame,
    spread_panel: pd.DataFrame,
    spread_col: str = "Q5_minus_Q1",
) -> pd.Series:
    """Descriptive baseline summary without formal HAC inference.

    Formal t-statistics are intentionally deferred until the pre-specified
    Newey-West lag rule is frozen.
    """
    ic = rank_ic["RankIC"].dropna()
    spread = spread_panel[spread_col].dropna()

    return pd.Series(
        {
            "RankIC_months": len(ic),
            "RankIC_mean": ic.mean(),
            "RankIC_median": ic.median(),
            "RankIC_positive_fraction": (ic > 0).mean(),
            "Spread_months": len(spread),
            "Spread_mean_monthly": spread.mean(),
            "Spread_vol_monthly": spread.std(ddof=1),
            "Spread_positive_fraction": (spread > 0).mean(),
            "Spread_annualised_mean": 12 * spread.mean(),
            "Spread_annualised_vol": np.sqrt(12) * spread.std(ddof=1),
        }
    )
