"""Mega-cap weight-contribution decomposition.

Purpose
-------
Separate the effect of removing mega-cap companies from:
1) the direct value-weight effect within the *existing* baseline quintiles; and
2) the additional effect of re-forming quintile membership after exclusion.

Definitions
-----------
Baseline:
    Original momentum quintiles and value-weighted returns.

Fixed-rank exclusion:
    Keep the baseline Q1-Q5 membership unchanged, remove securities belonging
    to the top-N PERMCO companies at formation month t, then re-normalise
    formation-month market-cap weights among the remaining securities in each
    quintile.

Re-formed exclusion:
    Remove top-N PERMCO companies from the formation universe first, then
    recompute quintiles and value-weighted returns.

Thus for each month:

    TotalChange = Reformed - Baseline
                = (FixedRanks - Baseline)
                + (Reformed - FixedRanks)

The first term is the direct weight/composition effect.
The second is the re-ranking / boundary effect.

Return calculations mirror src.portfolio.py:
- missing next-month returns are never replaced with zero;
- value weights are normalised over securities with observed next-month returns.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.mega_cap import largest_permco_by_month
from src.inference import primary_and_robustness_hac


def _topn_membership_table(
    market_state: pd.DataFrame,
    n: int,
    date_col: str = "MthCalDt",
    permco_col: str = "PERMCO",
) -> pd.DataFrame:
    top = largest_permco_by_month(
        market_state=market_state,
        n=n,
        date_col=date_col,
        permco_col=permco_col,
    )[[date_col, permco_col]].copy()
    top["IsTopN"] = True
    return top


def fixed_rank_value_weighted_returns(
    baseline_members: pd.DataFrame,
    market_state: pd.DataFrame,
    n: int = 10,
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
    permco_col: str = "PERMCO",
    weight_col: str = "MthCap",
    return_col: str = "NextMthRet",
) -> pd.DataFrame:
    """Value-weighted quintile returns after removing top-N firms without re-ranking."""
    required = {
        date_col, quintile_col, permco_col, weight_col, return_col
    }
    missing = required.difference(baseline_members.columns)
    if missing:
        raise ValueError(f"Missing baseline columns: {sorted(missing)}")

    top = _topn_membership_table(
        market_state, n=n, date_col=date_col, permco_col=permco_col
    )

    x = baseline_members.dropna(subset=[quintile_col]).copy()
    x[date_col] = pd.to_datetime(x[date_col], errors="raise")
    x = x.merge(
        top,
        on=[date_col, permco_col],
        how="left",
        validate="many_to_one",
    )
    x["IsTopN"] = x["IsTopN"].fillna(False).astype(bool)

    # Remove top-N companies but keep baseline quintile labels fixed.
    kept = x[~x["IsTopN"]].copy()

    rows = []
    for (date, q), g in kept.groupby([date_col, quintile_col], observed=True, sort=True):
        observed = g.dropna(subset=[return_col]).copy()

        vw = np.nan
        if not observed.empty:
            w = pd.to_numeric(observed[weight_col], errors="coerce")
            r = pd.to_numeric(observed[return_col], errors="coerce")
            valid = w.notna() & r.notna() & (w > 0)
            if valid.any() and w[valid].sum() > 0:
                vw = float(np.average(r[valid], weights=w[valid]))

        rows.append(
            {
                date_col: date,
                quintile_col: int(q),
                "VW_Return_FixedRanks": vw,
                "ObservedReturn_N": len(observed),
            }
        )

    return pd.DataFrame(rows).sort_values([date_col, quintile_col]).reset_index(drop=True)


def fixed_rank_spread(
    fixed_qret: pd.DataFrame,
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
) -> pd.DataFrame:
    """Pivot fixed-rank quintile returns and construct Q5-Q1."""
    wide = fixed_qret.pivot(
        index=date_col,
        columns=quintile_col,
        values="VW_Return_FixedRanks",
    ).sort_index()
    wide = wide.rename(columns={q: f"Q{q}" for q in wide.columns})

    if not {"Q1", "Q5"}.issubset(wide.columns):
        raise ValueError("Q1 and Q5 required for fixed-rank spread.")

    wide["Q5_minus_Q1"] = wide["Q5"] - wide["Q1"]
    return wide.reset_index()


def decomposition_table(
    baseline_spread: pd.DataFrame,
    fixed_spread: pd.DataFrame,
    reformed_spread: pd.DataFrame,
    date_col: str = "MthCalDt",
    spread_col: str = "Q5_minus_Q1",
) -> pd.DataFrame:
    """Create an exactly additive direct-weight / re-ranking decomposition."""
    b = baseline_spread[[date_col, spread_col]].rename(
        columns={spread_col: "BaselineSpread"}
    )
    f = fixed_spread[[date_col, spread_col]].rename(
        columns={spread_col: "FixedRanksSpread"}
    )
    r = reformed_spread[[date_col, spread_col]].rename(
        columns={spread_col: "ReformedSpread"}
    )

    out = (
        b.merge(f, on=date_col, how="inner", validate="one_to_one")
        .merge(r, on=date_col, how="inner", validate="one_to_one")
        .sort_values(date_col)
        .reset_index(drop=True)
    )

    out["DirectWeightEffect"] = out["FixedRanksSpread"] - out["BaselineSpread"]
    out["ReRankingEffect"] = out["ReformedSpread"] - out["FixedRanksSpread"]
    out["TotalChange"] = out["ReformedSpread"] - out["BaselineSpread"]
    out["AdditivityError"] = (
        out["DirectWeightEffect"] + out["ReRankingEffect"] - out["TotalChange"]
    )

    if out["AdditivityError"].abs().dropna().max() > 1e-12:
        raise AssertionError("Decomposition is not numerically additive.")

    return out


def mega_cap_leg_diagnostics(
    baseline_members: pd.DataFrame,
    market_state: pd.DataFrame,
    n: int = 10,
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
    permco_col: str = "PERMCO",
    weight_col: str = "MthCap",
    return_col: str = "NextMthRet",
) -> pd.DataFrame:
    """Measure top-N weight share and return contribution inside baseline quintiles.

    FormationWeightShare:
        top-N formation-month market cap / total formation-month market cap
        within that baseline quintile.

    ObservedWeightShare:
        same concept but among securities with observed next-month returns.

    ReturnContribution:
        contribution of top-N securities to the baseline quintile's realised
        value-weighted return, using the same observed-return normalisation as
        the baseline portfolio.
    """
    top = _topn_membership_table(
        market_state, n=n, date_col=date_col, permco_col=permco_col
    )

    x = baseline_members.dropna(subset=[quintile_col]).copy()
    x[date_col] = pd.to_datetime(x[date_col], errors="raise")
    x = x.merge(
        top,
        on=[date_col, permco_col],
        how="left",
        validate="many_to_one",
    )
    x["IsTopN"] = x["IsTopN"].fillna(False).astype(bool)

    rows = []
    for (date, q), g in x.groupby([date_col, quintile_col], observed=True, sort=True):
        w_form = pd.to_numeric(g[weight_col], errors="coerce")
        form_valid = w_form.notna() & (w_form > 0)
        total_form = w_form[form_valid].sum()
        mega_form = w_form[form_valid & g["IsTopN"]].sum()
        form_share = mega_form / total_form if total_form > 0 else np.nan

        obs = g.dropna(subset=[return_col]).copy()
        w_obs = pd.to_numeric(obs[weight_col], errors="coerce")
        r_obs = pd.to_numeric(obs[return_col], errors="coerce")
        obs_valid = w_obs.notna() & r_obs.notna() & (w_obs > 0)

        total_obs = w_obs[obs_valid].sum()
        mega_mask = obs_valid & obs["IsTopN"]

        obs_share = (
            w_obs[mega_mask].sum() / total_obs if total_obs > 0 else np.nan
        )

        contribution = np.nan
        baseline_return = np.nan
        if total_obs > 0:
            norm_w = w_obs[obs_valid] / total_obs
            baseline_return = float((norm_w * r_obs[obs_valid]).sum())

            mega_index = obs.index[mega_mask]
            if len(mega_index) == 0:
                contribution = 0.0
            else:
                contribution = float(
                    (
                        (w_obs.loc[mega_index] / total_obs)
                        * r_obs.loc[mega_index]
                    ).sum()
                )

        rows.append(
            {
                date_col: date,
                quintile_col: int(q),
                "FormationWeightShare": form_share,
                "ObservedWeightShare": obs_share,
                "ReturnContribution": contribution,
                "BaselineLegReturn": baseline_return,
                "TopN_SecurityCount": int(g["IsTopN"].sum()),
            }
        )

    return pd.DataFrame(rows).sort_values([date_col, quintile_col]).reset_index(drop=True)


def component_hac_summary(decomp: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """HAC6/HAC12 mean inference for all three decomposition components."""
    return {
        col: primary_and_robustness_hac(decomp[col])
        for col in ["DirectWeightEffect", "ReRankingEffect", "TotalChange"]
    }
