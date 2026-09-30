"""External validation against the Kenneth French US Momentum Factor (Mom).

Purpose
-------
This is a sanity-check benchmark, not a replacement for the project's own
momentum construction.

Important timing:
The project's spread indexed by formation month t is realised in calendar
month t+1. French Mom is indexed by realised return month. Therefore the
project spread must be shifted to its holding month before alignment.

French Mom construction differs materially from this project:
- six value-weight portfolios from a 2x3 size x prior-return sort;
- NYSE median size breakpoint;
- NYSE 30th/70th prior-return breakpoints;
- factor = 1/2(Small High + Big High) - 1/2(Small Low + Big Low).

The project instead uses a screened investable universe and global momentum
quintiles. The validation therefore focuses on co-movement, not equality.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm


def read_french_monthly_mom(path: str | Path) -> pd.DataFrame:
    """Read Kenneth French monthly Momentum Factor CSV; return decimal returns."""
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", errors="replace") as fh:
        lines = fh.readlines()

    header_row = None
    for i, line in enumerate(lines):
        fields = [x.strip() for x in line.strip().split(",")]
        if "Mom" in fields:
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not locate monthly Momentum Factor header ('Mom').")

    raw = pd.read_csv(path, skiprows=header_row)
    if "Mom" not in raw.columns:
        raise ValueError("Mom column not found after header detection.")

    date_col = raw.columns[0]
    out = raw[[date_col, "Mom"]].copy()
    out = out.rename(columns={date_col: "MonthRaw"})

    month_str = out["MonthRaw"].astype(str).str.strip()
    valid = month_str.str.fullmatch(r"\d{6}")
    out = out.loc[valid].copy()
    out["Month"] = pd.PeriodIndex(
        pd.to_datetime(out["MonthRaw"].astype(str), format="%Y%m"),
        freq="M",
    )

    # Kenneth French factor returns are reported in percent.
    out["FrenchMom"] = pd.to_numeric(out["Mom"], errors="coerce") / 100.0
    out = out[["Month", "FrenchMom"]].dropna().sort_values("Month").reset_index(drop=True)

    if out["Month"].duplicated().any():
        raise ValueError("French monthly Mom series has duplicate months.")

    return out


def align_project_with_french(
    vw: pd.DataFrame,
    ew: pd.DataFrame,
    french: pd.DataFrame,
    date_col: str = "MthCalDt",
    spread_col: str = "Q5_minus_Q1",
    start: str = "2000-02",
    end: str = "2025-12",
) -> pd.DataFrame:
    """Align project realised holding-month spreads with French Mom."""
    v = vw[[date_col, spread_col]].rename(columns={spread_col: "ProjectVW"}).copy()
    e = ew[[date_col, spread_col]].rename(columns={spread_col: "ProjectEW"}).copy()

    for x in (v, e):
        x[date_col] = pd.to_datetime(x[date_col], errors="raise")
        x["Month"] = x[date_col].dt.to_period("M") + 1

    proj = v[["Month", "ProjectVW"]].merge(
        e[["Month", "ProjectEW"]],
        on="Month",
        how="inner",
        validate="one_to_one",
    )

    out = proj.merge(french, on="Month", how="inner", validate="one_to_one")
    lo, hi = pd.Period(start, freq="M"), pd.Period(end, freq="M")
    out = out[out["Month"].between(lo, hi)].copy()

    return out.sort_values("Month").reset_index(drop=True)


def validation_summary(aligned: pd.DataFrame) -> pd.DataFrame:
    """Mean, volatility, and correlation diagnostics."""
    rows = []
    for col in ["ProjectVW", "ProjectEW", "FrenchMom"]:
        s = pd.to_numeric(aligned[col], errors="coerce").dropna()
        rows.append(
            {
                "Series": col,
                "N": len(s),
                "MeanMonthly": s.mean(),
                "StdMonthly": s.std(ddof=1),
                "AnnualisedMean_x12": 12 * s.mean(),
                "AnnualisedVol_sqrt12": np.sqrt(12) * s.std(ddof=1),
            }
        )
    return pd.DataFrame(rows)


def correlation_summary(aligned: pd.DataFrame) -> pd.DataFrame:
    return aligned[["ProjectVW", "ProjectEW", "FrenchMom"]].corr()


def benchmark_regression(
    aligned: pd.DataFrame,
    project_col: str,
    hac_lag: int = 6,
) -> pd.Series:
    """Diagnostic regression of project spread on French Mom."""
    use = aligned[[project_col, "FrenchMom"]].apply(
        pd.to_numeric, errors="coerce"
    ).dropna()

    X = sm.add_constant(use["FrenchMom"].to_numpy(dtype=float))
    y = use[project_col].to_numpy(dtype=float)
    fit = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": hac_lag, "use_correction": True},
    )
    ci = fit.conf_int(alpha=0.05)

    return pd.Series(
        {
            "N": len(use),
            "Alpha": float(fit.params[0]),
            "Alpha_p": float(fit.pvalues[0]),
            "FrenchMomBeta": float(fit.params[1]),
            "Beta_HAC_SE": float(fit.bse[1]),
            "Beta_t": float(fit.tvalues[1]),
            "Beta_p": float(fit.pvalues[1]),
            "Beta_CI95_Low": float(ci[1, 0]),
            "Beta_CI95_High": float(ci[1, 1]),
            "R2": float(fit.rsquared),
        }
    )
