"""Beta-neutral portfolio construction for the existing momentum strategy.

Primary construction (locked before results):
1. Keep the original 12-2 momentum rankings and baseline quintile membership.
2. Restrict both comparator and neutral portfolio to stocks with valid ex-ante beta.
3. Preserve within-leg formation-month value weights.
4. Compute ex-ante Q5 and Q1 portfolio betas from those weights.
5. Hedge the net beta with the CRSP value-weighted market excess return.

Primary estimand:
    BetaNeutral - BetaEligibleRaw

A separate coverage effect:
    BetaEligibleRaw - OriginalRaw

is reported so missing-beta exclusions are not confused with neutralisation.

Robustness:
    Rescale long/short legs to zero beta at constant 200% gross exposure,
    only when both leg betas are strictly positive.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def compound_monthly_market_excess(market_rf: pd.DataFrame) -> pd.DataFrame:
    """Compound daily market and RF returns separately to calendar months."""
    required = {"Date", "MarketRet", "RF"}
    missing = required.difference(market_rf.columns)
    if missing:
        raise ValueError(f"Missing market/RF columns: {sorted(missing)}")

    x = market_rf[list(required)].copy()
    x["Date"] = pd.to_datetime(x["Date"], errors="raise")
    x["Month"] = x["Date"].dt.to_period("M")

    def _compound(s: pd.Series) -> float:
        s = pd.to_numeric(s, errors="coerce").dropna()
        if s.empty:
            return np.nan
        return float(np.prod(1.0 + s.to_numpy(dtype=float)) - 1.0)

    out = (
        x.groupby("Month", sort=True)
        .agg(
            MarketRetMonthly=("MarketRet", _compound),
            RFMonthly=("RF", _compound),
            TradingDays=("Date", "size"),
        )
        .reset_index()
    )
    out["MarketExcessMonthly"] = out["MarketRetMonthly"] - out["RFMonthly"]
    return out


def _vw_return(g: pd.DataFrame, return_col: str, weight_col: str) -> float:
    """Value-weighted realised return over observed returns only."""
    r = pd.to_numeric(g[return_col], errors="coerce")
    w = pd.to_numeric(g[weight_col], errors="coerce")
    valid = r.notna() & w.notna() & (w > 0)
    if not valid.any() or w[valid].sum() <= 0:
        return np.nan
    return float(np.average(r[valid], weights=w[valid]))


def _vw_beta(g: pd.DataFrame, beta_col: str, weight_col: str) -> float:
    """Formation-date value-weighted ex-ante beta."""
    b = pd.to_numeric(g[beta_col], errors="coerce")
    w = pd.to_numeric(g[weight_col], errors="coerce")
    valid = b.notna() & w.notna() & (w > 0)
    if not valid.any() or w[valid].sum() <= 0:
        return np.nan
    return float(np.average(b[valid], weights=w[valid]))


def build_beta_neutral_momentum(
    formation_signal: pd.DataFrame,
    beta: pd.DataFrame,
    market_rf: pd.DataFrame,
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
    return_col: str = "NextMthRet",
    weight_col: str = "MthCap",
    beta_col: str = "Beta",
) -> pd.DataFrame:
    """Construct original, beta-eligible, and beta-neutral monthly spreads."""
    required = {
        "PERMNO", date_col, quintile_col, return_col, weight_col
    }
    missing = required.difference(formation_signal.columns)
    if missing:
        raise ValueError(f"Missing formation/signal columns: {sorted(missing)}")

    b_required = {"PERMNO", date_col, beta_col}
    b_missing = b_required.difference(beta.columns)
    if b_missing:
        raise ValueError(f"Missing beta columns: {sorted(b_missing)}")

    f = formation_signal.copy()
    f[date_col] = pd.to_datetime(f[date_col], errors="raise")

    if f.duplicated(["PERMNO", date_col]).any():
        raise ValueError("Formation-signal panel is not unique on PERMNO-month.")

    b = beta[["PERMNO", date_col, beta_col]].copy()
    b[date_col] = pd.to_datetime(b[date_col], errors="raise")
    if b.duplicated(["PERMNO", date_col]).any():
        raise ValueError("Beta panel is not unique on PERMNO-month.")

    x = f.merge(
        b,
        on=["PERMNO", date_col],
        how="left",
        validate="one_to_one",
    )

    # Keep original signal quintile assignment; do not re-rank after beta exclusions.
    x = x[x[quintile_col].isin([1, 5])].copy()
    x[quintile_col] = x[quintile_col].astype(int)

    rows = []
    for date, g in x.groupby(date_col, sort=True):
        q1 = g[g[quintile_col].eq(1)]
        q5 = g[g[quintile_col].eq(5)]

        raw_q1 = _vw_return(q1, return_col, weight_col)
        raw_q5 = _vw_return(q5, return_col, weight_col)

        q1e = q1[q1[beta_col].notna()].copy()
        q5e = q5[q5[beta_col].notna()].copy()

        elig_q1 = _vw_return(q1e, return_col, weight_col)
        elig_q5 = _vw_return(q5e, return_col, weight_col)

        beta_q1 = _vw_beta(q1e, beta_col, weight_col)
        beta_q5 = _vw_beta(q5e, beta_col, weight_col)
        beta_ls = (
            beta_q5 - beta_q1
            if pd.notna(beta_q5) and pd.notna(beta_q1)
            else np.nan
        )

        # Coverage diagnostics are formation-date quantities.
        def _cap_share(eligible: pd.DataFrame, full: pd.DataFrame) -> float:
            full_cap = pd.to_numeric(full[weight_col], errors="coerce")
            elig_cap = pd.to_numeric(eligible[weight_col], errors="coerce")
            full_cap = full_cap[full_cap > 0].sum()
            elig_cap = elig_cap[elig_cap > 0].sum()
            return float(elig_cap / full_cap) if full_cap > 0 else np.nan

        rows.append(
            {
                date_col: date,
                "Original_Q1": raw_q1,
                "Original_Q5": raw_q5,
                "OriginalSpread": (
                    raw_q5 - raw_q1
                    if pd.notna(raw_q5) and pd.notna(raw_q1)
                    else np.nan
                ),
                "Eligible_Q1": elig_q1,
                "Eligible_Q5": elig_q5,
                "EligibleSpread": (
                    elig_q5 - elig_q1
                    if pd.notna(elig_q5) and pd.notna(elig_q1)
                    else np.nan
                ),
                "Beta_Q1": beta_q1,
                "Beta_Q5": beta_q5,
                "Beta_LS": beta_ls,
                "Q1_FormationN": len(q1),
                "Q5_FormationN": len(q5),
                "Q1_BetaEligibleN": len(q1e),
                "Q5_BetaEligibleN": len(q5e),
                "Q1_BetaEligibleCountShare": len(q1e) / len(q1) if len(q1) else np.nan,
                "Q5_BetaEligibleCountShare": len(q5e) / len(q5) if len(q5) else np.nan,
                "Q1_BetaEligibleCapShare": _cap_share(q1e, q1),
                "Q5_BetaEligibleCapShare": _cap_share(q5e, q5),
            }
        )

    out = pd.DataFrame(rows).sort_values(date_col).reset_index(drop=True)

    monthly_market = compound_monthly_market_excess(market_rf)
    out["HoldingMonth"] = out[date_col].dt.to_period("M") + 1
    out = out.merge(
        monthly_market.rename(columns={"Month": "HoldingMonth"}),
        on="HoldingMonth",
        how="left",
        validate="many_to_one",
    )

    out["BetaNeutralSpread"] = (
        out["EligibleSpread"]
        - out["Beta_LS"] * out["MarketExcessMonthly"]
    )

    out["CoverageEffect"] = out["EligibleSpread"] - out["OriginalSpread"]
    out["NeutralisationEffect"] = (
        out["BetaNeutralSpread"] - out["EligibleSpread"]
    )
    out["TotalVsOriginal"] = (
        out["BetaNeutralSpread"] - out["OriginalSpread"]
    )

    # Mechanical ex-ante beta after the market overlay.
    out["ExAnteBetaAfterHedge"] = out["Beta_LS"] - out["Beta_LS"]

    # Pre-specified long/short rescaling robustness.
    valid_scale = (out["Beta_Q5"] > 0) & (out["Beta_Q1"] > 0)
    denom = out["Beta_Q5"] + out["Beta_Q1"]
    out["ScaleLong"] = np.nan
    out["ScaleShort"] = np.nan

    out.loc[valid_scale, "ScaleLong"] = (
        2.0 * out.loc[valid_scale, "Beta_Q1"]
        / denom.loc[valid_scale]
    )
    out.loc[valid_scale, "ScaleShort"] = (
        2.0 * out.loc[valid_scale, "Beta_Q5"]
        / denom.loc[valid_scale]
    )
    out["ScaledNeutralSpread"] = np.nan
    out.loc[valid_scale, "ScaledNeutralSpread"] = (
        out.loc[valid_scale, "ScaleLong"] * out.loc[valid_scale, "Eligible_Q5"]
        - out.loc[valid_scale, "ScaleShort"] * out.loc[valid_scale, "Eligible_Q1"]
    )
    out["ScaledNeutralisationEffect"] = (
        out["ScaledNeutralSpread"] - out["EligibleSpread"]
    )

    return out


def ex_post_market_beta(
    panel: pd.DataFrame,
    return_col: str,
    market_col: str = "MarketExcessMonthly",
    hac_lag: int = 6,
) -> pd.Series:
    """Estimate realised monthly market beta with HAC standard errors."""
    x = panel[[return_col, market_col]].apply(
        pd.to_numeric, errors="coerce"
    ).dropna()

    if len(x) <= hac_lag + 2:
        raise ValueError("Not enough monthly observations for ex-post beta regression.")

    X = sm.add_constant(x[market_col].to_numpy(dtype=float))
    y = x[return_col].to_numpy(dtype=float)
    fit = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": hac_lag, "use_correction": True},
    )

    return pd.Series(
        {
            "N": len(x),
            "Alpha": float(fit.params[0]),
            "MarketBeta": float(fit.params[1]),
            "Beta_HAC_SE": float(fit.bse[1]),
            "Beta_T": float(fit.tvalues[1]),
            "Beta_P": float(fit.pvalues[1]),
        }
    )
