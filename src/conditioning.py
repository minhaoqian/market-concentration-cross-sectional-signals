"""Concentration-conditioning tests for the validated momentum baseline.

Primary specification:

    VW_MomentumSpread_t = alpha + beta * Top10Share_t + error_t

The spread indexed by formation month t is realised in calendar month t+1.
Top10Share_t is measured at formation month-end t from the broad market-state
universe.

For interpretability, one regressor unit equals a 10-percentage-point change
in Top-10 concentration.

Inference:
- primary HAC/Newey-West lag = 6 months;
- robustness HAC/Newey-West lag = 12 months.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from src.inference import PRIMARY_HAC_LAG


def merge_performance_and_concentration(
    performance: pd.DataFrame,
    concentration: pd.DataFrame,
    date_col: str = "MthCalDt",
) -> pd.DataFrame:
    left = performance.copy()
    right = concentration.copy()

    left[date_col] = pd.to_datetime(left[date_col], errors="raise")
    right[date_col] = pd.to_datetime(right[date_col], errors="raise")

    if left[date_col].duplicated().any():
        raise ValueError("Performance series has duplicate formation months.")
    if right[date_col].duplicated().any():
        raise ValueError("Concentration series has duplicate months.")

    merged = left.merge(
        right, on=date_col, how="inner", validate="one_to_one"
    ).sort_values(date_col).reset_index(drop=True)

    if merged.empty:
        raise ValueError("No overlapping months after merge.")
    return merged


def hac_regression(
    df: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    maxlags: int = PRIMARY_HAC_LAG,
    add_time_trend: bool = False,
) -> tuple[pd.DataFrame, object]:
    required = {y_col, *x_cols}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing regression columns: {sorted(missing)}")

    use = df.copy()
    x_cols = list(x_cols)

    if add_time_trend:
        use["TimeTrend"] = np.arange(len(use), dtype=float)
        x_cols.append("TimeTrend")

    use = use[[y_col, *x_cols]].dropna().copy()

    X = sm.add_constant(use[x_cols], has_constant="add")
    fit = sm.OLS(use[y_col].astype(float), X.astype(float)).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": maxlags, "use_correction": True},
    )

    ci = fit.conf_int(alpha=0.05)
    rows = []
    for name in fit.params.index:
        rows.append(
            {
                "Term": name,
                "Estimate": float(fit.params[name]),
                "HAC_SE": float(fit.bse[name]),
                "T_Stat": float(fit.tvalues[name]),
                "P_Value": float(fit.pvalues[name]),
                "CI95_Low": float(ci.loc[name, 0]),
                "CI95_High": float(ci.loc[name, 1]),
                "N": int(fit.nobs),
                "HAC_Lag": int(maxlags),
                "R2": float(fit.rsquared),
            }
        )

    return pd.DataFrame(rows).set_index("Term"), fit


def primary_top10_spec(
    df: pd.DataFrame,
    outcome_col: str = "Q5_minus_Q1",
    top10_col: str = "Top10Share",
    maxlags: int = PRIMARY_HAC_LAG,
    add_time_trend: bool = False,
) -> tuple[pd.DataFrame, object]:
    use = df.copy()
    use["Top10Share_10pp"] = pd.to_numeric(
        use[top10_col], errors="coerce"
    ) / 0.10

    return hac_regression(
        use,
        y_col=outcome_col,
        x_cols=["Top10Share_10pp"],
        maxlags=maxlags,
        add_time_trend=add_time_trend,
    )


def hhi_spec(
    df: pd.DataFrame,
    outcome_col: str = "Q5_minus_Q1",
    hhi_col: str = "HHI",
    maxlags: int = PRIMARY_HAC_LAG,
    add_time_trend: bool = False,
) -> tuple[pd.DataFrame, object]:
    use = df.copy()
    use["HHI_0p01"] = pd.to_numeric(use[hhi_col], errors="coerce") / 0.01

    return hac_regression(
        use,
        y_col=outcome_col,
        x_cols=["HHI_0p01"],
        maxlags=maxlags,
        add_time_trend=add_time_trend,
    )


def expanding_concentration_regimes(
    concentration: pd.DataFrame,
    value_col: str = "Top10Share",
    date_col: str = "MthCalDt",
    min_history: int = 60,
) -> pd.DataFrame:
    """Classify Low/Medium/High using prior-history expanding tertiles.

    Thresholds at month t use only observations available through t-1.
    The first min_history months remain unclassified.
    """
    x = concentration[[date_col, value_col]].copy()
    x[date_col] = pd.to_datetime(x[date_col], errors="raise")
    x = x.sort_values(date_col).reset_index(drop=True)

    lows, highs, regimes = [], [], []
    values = pd.to_numeric(x[value_col], errors="coerce")

    for i, current in enumerate(values):
        if i < min_history or pd.isna(current):
            lows.append(np.nan)
            highs.append(np.nan)
            regimes.append(pd.NA)
            continue

        hist = values.iloc[:i].dropna()
        q33 = float(hist.quantile(1 / 3))
        q67 = float(hist.quantile(2 / 3))
        lows.append(q33)
        highs.append(q67)

        if current < q33:
            regimes.append("Low")
        elif current > q67:
            regimes.append("High")
        else:
            regimes.append("Medium")

    x["Prior_Q33"] = lows
    x["Prior_Q67"] = highs
    x["ConcentrationRegime"] = pd.Categorical(
        regimes, categories=["Low", "Medium", "High"], ordered=True
    )
    return x


def regime_descriptives(
    merged: pd.DataFrame,
    regime_col: str = "ConcentrationRegime",
    columns: tuple[str, ...] = ("Q5_minus_Q1", "RankIC"),
) -> pd.DataFrame:
    keep = [c for c in columns if c in merged.columns]
    if not keep:
        raise ValueError("No requested descriptive columns are present.")

    return (
        merged.dropna(subset=[regime_col])
        .groupby(regime_col, observed=True)[keep]
        .agg(["count", "mean", "median"])
    )
