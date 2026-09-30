"""Cross-sectional signal construction.

Primary momentum follows the pre-analysis definition:
cumulative total return from month t-12 through t-2, formed at month-end t.

Signal construction uses the broader monthly history panel, while portfolio
eligibility is imposed only at the formation date using the cleaned panel.
This avoids accidentally dropping lookback returns or next-month outcomes
because a stock failed a size/price screen outside the formation month.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


KEY = ["PERMNO", "MthCalDt"]


def _validate_history(history: pd.DataFrame) -> pd.DataFrame:
    required = {"PERMNO", "MthCalDt", "MthRet"}
    missing = required.difference(history.columns)
    if missing:
        raise ValueError(f"Missing required history columns: {sorted(missing)}")

    out = history.copy()
    out["MthCalDt"] = pd.to_datetime(out["MthCalDt"], errors="raise")
    out["MthRet"] = pd.to_numeric(out["MthRet"], errors="coerce")

    if out.duplicated(KEY).any():
        raise ValueError("History is not unique on PERMNO + MthCalDt.")

    # CRSP total returns below -100% are not economically valid.
    invalid = out["MthRet"].dropna() < -1
    if invalid.any():
        raise ValueError("Observed MthRet below -100%; inspect source data.")

    out = out.sort_values(KEY).reset_index(drop=True)
    out["MonthId"] = out["MthCalDt"].dt.year * 12 + out["MthCalDt"].dt.month
    return out


def construct_momentum_12_2(history: pd.DataFrame) -> pd.DataFrame:
    """Construct prior 2-12 month momentum and next-month realised return.

    At formation month t:

        MOM_12_2(t) = product(1 + R_s) - 1, s = t-12,...,t-2

    This uses 11 monthly returns and skips month t-1.

    A momentum value is accepted only when the security has a contiguous
    monthly record from t-12 through t. This makes the row-based rolling window
    correspond to actual calendar months rather than merely the previous
    observations.

    The next-month outcome is retained only when the next observed row is
    exactly calendar month t+1.
    """
    out = _validate_history(history)

    g = out.groupby("PERMNO", sort=False)

    # Efficient 11-month compounded return from t-12 through t-2.
    shifted_ret = g["MthRet"].shift(2)
    shifted_log = np.log1p(shifted_ret)

    rolling_log = (
        shifted_log.groupby(out["PERMNO"], sort=False)
        .rolling(window=11, min_periods=11)
        .sum()
        .reset_index(level=0, drop=True)
    )

    out["Momentum_12_2"] = np.expm1(rolling_log)

    # Ensure the observations really correspond to t-12,...,t (no month gaps).
    month_lag_2 = g["MonthId"].shift(2)
    month_lag_12 = g["MonthId"].shift(12)
    contiguous_history = (
        (out["MonthId"] - month_lag_2 == 2)
        & (out["MonthId"] - month_lag_12 == 12)
    )
    out.loc[~contiguous_history, "Momentum_12_2"] = np.nan

    # Realised return in calendar month t+1, regardless of whether the stock
    # passes the t+1 formation screen.
    out["NextMthRet"] = g["MthRet"].shift(-1)
    next_month_id = g["MonthId"].shift(-1)
    out.loc[next_month_id != out["MonthId"] + 1, "NextMthRet"] = np.nan

    return out[
        ["PERMNO", "MthCalDt", "Momentum_12_2", "NextMthRet"]
    ].copy()


def attach_momentum_to_formation_universe(
    formation_panel: pd.DataFrame,
    history: pd.DataFrame,
) -> pd.DataFrame:
    """Attach momentum and next-month return to eligible formation-month stocks."""
    required = {"PERMNO", "MthCalDt"}
    missing = required.difference(formation_panel.columns)
    if missing:
        raise ValueError(
            f"Missing formation-panel columns: {sorted(missing)}"
        )

    formation = formation_panel.copy()
    formation["MthCalDt"] = pd.to_datetime(
        formation["MthCalDt"], errors="raise"
    )

    if formation.duplicated(KEY).any():
        raise ValueError(
            "Formation panel is not unique on PERMNO + MthCalDt."
        )

    signal = construct_momentum_12_2(history)

    merged = formation.merge(
        signal,
        on=KEY,
        how="left",
        validate="one_to_one",
    )

    return merged


def assign_signal_quintiles(
    df: pd.DataFrame,
    signal_col: str = "Momentum_12_2",
    date_col: str = "MthCalDt",
) -> pd.DataFrame:
    """Assign monthly cross-sectional quintiles, Q1=lowest and Q5=highest."""
    out = df.copy()

    def _qcut(s: pd.Series) -> pd.Series:
        valid = s.dropna()
        result = pd.Series(pd.NA, index=s.index, dtype="Int64")
        if valid.nunique() < 5:
            return result

        # Rank first so ties do not make qcut fail unpredictably.
        ranks = valid.rank(method="first")
        result.loc[valid.index] = (
            pd.qcut(ranks, 5, labels=[1, 2, 3, 4, 5]).astype("Int64")
        )
        return result

    out["SignalQuintile"] = out.groupby(date_col)[signal_col].transform(_qcut)
    return out
