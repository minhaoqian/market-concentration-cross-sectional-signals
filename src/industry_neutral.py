"""Industry-neutral momentum based on Fama-French 49 industries.

Primary methodology
-------------------
- Industry classification: FF49 mapped from contemporaneous CRSP SICCD.
- Industry mean: equal-weighted monthly mean of raw 12-2 momentum.
- Minimum valid industry size: 10 stocks in a formation month.
- Neutral signal: raw momentum minus contemporaneous industry mean.
- Portfolio quintiles are re-formed on the adjusted signal.

Robustness
----------
- Within-industry percentile-rank signal.
- CRSP ICBIndustry as an alternative broad classification.

The FF49 SIC ranges are parsed from docs/reference/Siccodes49.txt, an auditable
copy of Kenneth French's published industry-definition file.
"""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd


FF49_DEFINITION_PATH = Path("docs/reference/Siccodes49.txt")


def parse_ff49_definitions(path: str | Path = FF49_DEFINITION_PATH) -> pd.DataFrame:
    """Parse the Fama-French 49 SIC-range definition text file."""
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    rows = []

    current_code = None
    current_short = None
    current_name = None

    header_re = re.compile(r"^\s*(\d+)\s+([A-Za-z0-9]+)\s{2,}(.+?)\s*$")
    range_re = re.compile(r"^\s*(\d{4})-(\d{4})\s+(.+?)\s*$")

    for line in text.splitlines():
        h = header_re.match(line)
        if h:
            current_code = int(h.group(1))
            current_short = h.group(2)
            current_name = h.group(3).strip()
            continue

        r = range_re.match(line)
        if r and current_code is not None:
            rows.append(
                {
                    "FF49": current_code,
                    "FF49Short": current_short,
                    "FF49Name": current_name,
                    "SIC_Start": int(r.group(1)),
                    "SIC_End": int(r.group(2)),
                    "RangeDescription": r.group(3).strip(),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty or out["FF49"].nunique() != 49:
        raise ValueError("FF49 definition parsing failed or did not yield 49 industries.")
    return out


def sic_to_ff49(
    sic: pd.Series,
    definitions: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Map SIC codes to FF49 code, short label and name."""
    defs = parse_ff49_definitions() if definitions is None else definitions.copy()

    sic_num = pd.to_numeric(sic, errors="coerce")
    ff_code = pd.Series(pd.NA, index=sic.index, dtype="Int64")
    ff_short = pd.Series(pd.NA, index=sic.index, dtype="string")
    ff_name = pd.Series(pd.NA, index=sic.index, dtype="string")

    for row in defs.itertuples(index=False):
        mask = sic_num.between(row.SIC_Start, row.SIC_End, inclusive="both")
        ff_code.loc[mask] = row.FF49
        ff_short.loc[mask] = row.FF49Short
        ff_name.loc[mask] = row.FF49Name

    return pd.DataFrame(
        {
            "FF49": ff_code,
            "FF49Short": ff_short,
            "FF49Name": ff_name,
        },
        index=sic.index,
    )


def attach_ff49(
    df: pd.DataFrame,
    sic_col: str = "SICCD",
) -> pd.DataFrame:
    """Attach FF49 labels from contemporaneous SICCD."""
    if sic_col not in df.columns:
        raise ValueError(f"{sic_col} not found.")

    out = df.copy()
    mapped = sic_to_ff49(out[sic_col])
    out = pd.concat([out, mapped], axis=1)
    return out


def industry_demeaned_momentum(
    df: pd.DataFrame,
    signal_col: str = "Momentum_12_2",
    date_col: str = "MthCalDt",
    industry_col: str = "FF49",
    min_industry_size: int = 10,
    output_col: str = "Momentum_IndustryNeutral",
) -> pd.DataFrame:
    """Equal-weight industry-demean raw momentum within each month."""
    required = {signal_col, date_col, industry_col}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    out = df.copy()
    valid = out[signal_col].notna() & out[industry_col].notna()

    stats = (
        out.loc[valid]
        .groupby([date_col, industry_col], observed=True)[signal_col]
        .agg(["count", "mean"])
        .rename(columns={"count": "IndustryN", "mean": "IndustryMeanMomentum"})
        .reset_index()
    )

    out = out.merge(
        stats,
        on=[date_col, industry_col],
        how="left",
        validate="many_to_one",
    )

    eligible = out["IndustryN"].ge(min_industry_size)
    out[output_col] = np.where(
        eligible,
        out[signal_col] - out["IndustryMeanMomentum"],
        np.nan,
    )
    return out


def within_industry_percentile_signal(
    df: pd.DataFrame,
    signal_col: str = "Momentum_12_2",
    date_col: str = "MthCalDt",
    industry_col: str = "FF49",
    min_industry_size: int = 10,
    output_col: str = "Momentum_IndustryPctRank",
) -> pd.DataFrame:
    """Robustness signal: within-industry percentile rank each month."""
    out = df.copy()

    counts = (
        out.dropna(subset=[signal_col, industry_col])
        .groupby([date_col, industry_col], observed=True)[signal_col]
        .transform("count")
    )
    out.loc[counts.index, "IndustryN_Rank"] = counts

    def _rank(g: pd.Series) -> pd.Series:
        return g.rank(method="average", pct=True)

    ranks = (
        out.dropna(subset=[signal_col, industry_col])
        .groupby([date_col, industry_col], observed=True)[signal_col]
        .transform(_rank)
    )
    out.loc[ranks.index, output_col] = ranks
    out.loc[out["IndustryN_Rank"].lt(min_industry_size), output_col] = np.nan
    return out


def icb_demeaned_momentum(
    df: pd.DataFrame,
    signal_col: str = "Momentum_12_2",
    date_col: str = "MthCalDt",
    industry_col: str = "ICBIndustry",
    min_industry_size: int = 10,
    output_col: str = "Momentum_ICBNeutral",
) -> pd.DataFrame:
    """Broad-classification robustness using CRSP ICBIndustry."""
    return industry_demeaned_momentum(
        df=df,
        signal_col=signal_col,
        date_col=date_col,
        industry_col=industry_col,
        min_industry_size=min_industry_size,
        output_col=output_col,
    )


def assign_quintiles_from_signal(
    df: pd.DataFrame,
    signal_col: str,
    date_col: str = "MthCalDt",
    output_col: str = "SignalQuintile",
) -> pd.DataFrame:
    """Assign monthly global quintiles from any validated signal column."""
    out = df.copy()

    def _qcut(s: pd.Series) -> pd.Series:
        valid = s.dropna()
        result = pd.Series(pd.NA, index=s.index, dtype="Int64")
        if valid.nunique() < 5:
            return result
        ranks = valid.rank(method="first")
        result.loc[valid.index] = pd.qcut(
            ranks, 5, labels=[1, 2, 3, 4, 5]
        ).astype("Int64")
        return result

    out[output_col] = out.groupby(date_col)[signal_col].transform(_qcut)
    return out
