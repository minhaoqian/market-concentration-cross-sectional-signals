"""Time-series inference helpers for monthly signal-performance series.

Pre-specified convention:
- Primary HAC/Newey-West lag: 6 months
- Robustness HAC/Newey-West lag: 12 months

The purpose is to avoid choosing an inference window after inspecting whether a
particular lag makes a result significant.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


PRIMARY_HAC_LAG = 6
ROBUSTNESS_HAC_LAG = 12


def hac_mean_test(series: pd.Series, maxlags: int) -> pd.Series:
    """Estimate a constant-only regression with HAC standard errors.

    Returns the sample mean, HAC standard error, t-statistic, two-sided p-value,
    and a 95% confidence interval.
    """
    x = pd.to_numeric(series, errors="coerce").dropna()

    if len(x) <= maxlags + 2:
        raise ValueError(
            f"Not enough observations ({len(x)}) for HAC maxlags={maxlags}."
        )

    y = x.to_numpy(dtype=float)
    X = np.ones((len(y), 1))

    fit = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": maxlags, "use_correction": True},
    )

    mean = float(fit.params[0])
    se = float(fit.bse[0])
    t = float(fit.tvalues[0])
    p = float(fit.pvalues[0])
    ci_low, ci_high = map(float, fit.conf_int(alpha=0.05)[0])

    return pd.Series(
        {
            "N": len(x),
            "Mean": mean,
            "HAC_Lag": maxlags,
            "HAC_SE": se,
            "T_Stat": t,
            "P_Value": p,
            "CI95_Low": ci_low,
            "CI95_High": ci_high,
        }
    )


def primary_and_robustness_hac(series: pd.Series) -> pd.DataFrame:
    """Run the pre-specified 6-month primary and 12-month robustness tests."""
    primary = hac_mean_test(series, PRIMARY_HAC_LAG)
    robustness = hac_mean_test(series, ROBUSTNESS_HAC_LAG)

    out = pd.DataFrame(
        [primary, robustness],
        index=["Primary_HAC6", "Robustness_HAC12"],
    )
    return out
