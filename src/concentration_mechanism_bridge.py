"""Bridge tests linking aggregate concentration to the mega-cap weight mechanism.

These specifications are locked before seeing the bridge-test results.

Primary questions
-----------------
1. Does the monthly direct-weight component of Top-10 exclusion become larger
   when aggregate Top-10 market concentration is higher?
2. Does the Top-10 formation-weight gap between the momentum winner and loser
   legs become larger when aggregate Top-10 concentration is higher?

Primary regressor:
    Top10Share_t, scaled per +10 percentage points.

Inference:
    HAC/Newey-West lag 6 primary; lag 12 robustness.

Secondary robustness:
    Add a deterministic linear time trend because Top10Share is highly
    persistent and strongly trending over the sample.

No HHI, alternative Top-N, sample splits, nonlinear terms, or lag search is
introduced in this bridge stage.
"""

from __future__ import annotations

import pandas as pd

from src.conditioning import merge_performance_and_concentration, primary_top10_spec


def build_weight_gap(
    leg_diagnostics: pd.DataFrame,
    date_col: str = "MthCalDt",
    quintile_col: str = "SignalQuintile",
    weight_col: str = "FormationWeightShare",
) -> pd.DataFrame:
    """Construct Q5 minus Q1 Top-10 formation-weight share by month."""
    required = {date_col, quintile_col, weight_col}
    missing = required.difference(leg_diagnostics.columns)
    if missing:
        raise ValueError(f"Missing leg-diagnostic columns: {sorted(missing)}")

    x = leg_diagnostics[
        leg_diagnostics[quintile_col].isin([1, 5])
    ][[date_col, quintile_col, weight_col]].copy()

    x[date_col] = pd.to_datetime(x[date_col], errors="raise")
    x[quintile_col] = x[quintile_col].astype(int)

    if x.duplicated([date_col, quintile_col]).any():
        raise ValueError("Leg diagnostics are not unique by month and quintile.")

    wide = x.pivot(index=date_col, columns=quintile_col, values=weight_col)
    if not {1, 5}.issubset(wide.columns):
        raise ValueError("Both Q1 and Q5 are required to construct weight gap.")

    out = wide[[1, 5]].rename(
        columns={1: "Top10Weight_Q1", 5: "Top10Weight_Q5"}
    ).reset_index()
    out["Top10WeightGap_Q5MinusQ1"] = (
        out["Top10Weight_Q5"] - out["Top10Weight_Q1"]
    )
    return out.sort_values(date_col).reset_index(drop=True)


def run_bridge_regressions(
    decomposition: pd.DataFrame,
    weight_gap: pd.DataFrame,
    concentration: pd.DataFrame,
    date_col: str = "MthCalDt",
) -> dict[str, pd.DataFrame]:
    """Run frozen bridge specifications for HAC6/HAC12 and trend robustness."""
    direct = decomposition[[date_col, "DirectWeightEffect"]].copy()
    direct = merge_performance_and_concentration(direct, concentration, date_col)

    gap = weight_gap[[date_col, "Top10WeightGap_Q5MinusQ1"]].copy()
    gap = merge_performance_and_concentration(gap, concentration, date_col)

    results = {}

    for label, df, outcome in [
        ("DirectWeightEffect", direct, "DirectWeightEffect"),
        ("WeightGap", gap, "Top10WeightGap_Q5MinusQ1"),
    ]:
        for lag in [6, 12]:
            reg, _ = primary_top10_spec(
                df,
                outcome_col=outcome,
                maxlags=lag,
                add_time_trend=False,
            )
            results[f"{label}_HAC{lag}"] = reg

        reg_trend, _ = primary_top10_spec(
            df,
            outcome_col=outcome,
            maxlags=6,
            add_time_trend=True,
        )
        results[f"{label}_Trend_HAC6"] = reg_trend

    return results


def bridge_summary(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Collect the Top10 coefficient from each bridge regression."""
    rows = []
    for name, reg in results.items():
        s = reg.loc["Top10Share_10pp"]
        rows.append(
            {
                "Specification": name,
                "Estimate_per_10pp": float(s["Estimate"]),
                "HAC_SE": float(s["HAC_SE"]),
                "T_Stat": float(s["T_Stat"]),
                "P_Value": float(s["P_Value"]),
                "CI95_Low": float(s["CI95_Low"]),
                "CI95_High": float(s["CI95_High"]),
                "N": int(s["N"]),
                "R2": float(s["R2"]),
            }
        )
    return pd.DataFrame(rows)
