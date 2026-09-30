"""Clean the CRSP CIZ monthly production extract.

This module turns the raw WRDS Monthly Stock File export into the primary
monthly research panel defined in docs/sample_construction.md.

Important:
- Raw WRDS data stay local and are not committed to GitHub.
- The code fails loudly if a non-identical PERMNO-month duplicate remains.
- Filters are applied using only contemporaneously available information.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd


KEY = ["PERMNO", "MthCalDt"]
COMMON_STOCK_FILTER = {
    "USIncFlg": "Y",
    "SecurityType": "EQTY",
    "SecuritySubType": "COM",
    "ShareType": "NS",
}
ISSUER_TYPES = {"ACOR", "CORP"}
PRIMARY_EXCHANGES = {"N", "A", "Q"}


@dataclass(frozen=True)
class CleaningConfig:
    min_price: float = 5.0
    nyse_size_percentile: float = 0.20
    require_positive_market_cap: bool = True


def _read_raw(path: str | Path) -> pd.DataFrame:
    """Read a CSV or CSV.GZ production extract."""
    path = Path(path)
    df = pd.read_csv(path, low_memory=False)

    required = {
        "PERMNO",
        "MthCalDt",
        "PrimaryExch",
        "USIncFlg",
        "IssuerType",
        "SecurityType",
        "SecuritySubType",
        "ShareType",
        "MthPrc",
        "MthCap",
        "MthRet",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["MthCalDt"] = pd.to_datetime(df["MthCalDt"], errors="raise")
    return df


def _deduplicate_exact_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Remove only exact full-row duplicates and assert key uniqueness afterwards."""
    before = len(df)
    duplicated_key_rows_before = int(df.duplicated(KEY, keep=False).sum())

    out = df.drop_duplicates().copy()

    remaining = out[out.duplicated(KEY, keep=False)].copy()
    if not remaining.empty:
        sample = remaining.sort_values(KEY).head(20)
        raise ValueError(
            "Non-identical PERMNO-month duplicates remain after exact-row "
            "deduplication. Investigate before continuing.\n"
            f"Example rows:\n{sample.to_string(index=False)}"
        )

    stats = {
        "rows_before_dedup": before,
        "exact_duplicate_rows_removed": before - len(out),
        "duplicated_key_rows_before_dedup": duplicated_key_rows_before,
        "rows_after_dedup": len(out),
    }
    return out, stats


def _assert_common_stock_query(df: pd.DataFrame) -> None:
    """Verify that the WRDS production query used the intended CIZ common-stock filter."""
    for column, expected in COMMON_STOCK_FILTER.items():
        observed = set(df[column].dropna().astype(str).unique())
        if observed - {expected}:
            raise ValueError(
                f"{column} contains values outside the production filter: "
                f"{sorted(observed)}"
            )

    issuer = set(df["IssuerType"].dropna().astype(str).unique())
    if issuer - ISSUER_TYPES:
        raise ValueError(
            "IssuerType contains values outside {ACOR, CORP}: "
            f"{sorted(issuer)}"
        )


def _apply_exchange_filter(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["PrimaryExch"].isin(PRIMARY_EXCHANGES)].copy()


def _apply_market_cap_requirement(
    df: pd.DataFrame, require_positive: bool
) -> pd.DataFrame:
    out = df.copy()
    out["MthCap"] = pd.to_numeric(out["MthCap"], errors="coerce")

    if require_positive:
        out = out[out["MthCap"].notna() & (out["MthCap"] > 0)].copy()
    return out


def _attach_nyse_breakpoint(
    df: pd.DataFrame, percentile: float
) -> pd.DataFrame:
    """Attach a point-in-time NYSE market-cap percentile breakpoint to each month."""
    if not 0 < percentile < 1:
        raise ValueError("nyse_size_percentile must lie strictly between 0 and 1.")

    nyse = df[df["PrimaryExch"].eq("N")]
    breakpoints = (
        nyse.groupby("MthCalDt", observed=True)["MthCap"]
        .quantile(percentile)
        .rename("NYSE_Size_Breakpoint")
    )

    out = df.merge(
        breakpoints,
        left_on="MthCalDt",
        right_index=True,
        how="left",
        validate="many_to_one",
    )

    if out["NYSE_Size_Breakpoint"].isna().any():
        bad_dates = (
            out.loc[out["NYSE_Size_Breakpoint"].isna(), "MthCalDt"]
            .drop_duplicates()
            .dt.strftime("%Y-%m-%d")
            .tolist()
        )
        raise ValueError(f"Missing NYSE breakpoint for dates: {bad_dates[:10]}")

    return out


def _apply_size_and_price_screens(
    df: pd.DataFrame, config: CleaningConfig
) -> pd.DataFrame:
    out = df[df["MthCap"] >= df["NYSE_Size_Breakpoint"]].copy()

    out["MthPrc"] = pd.to_numeric(out["MthPrc"], errors="coerce")
    out = out[out["MthPrc"].notna() & (out["MthPrc"].abs() >= config.min_price)].copy()

    return out


def _assert_clean_panel(df: pd.DataFrame) -> None:
    if df.duplicated(KEY).any():
        raise AssertionError("Clean panel is not unique on PERMNO + MthCalDt.")

    if (df["MthCap"] <= 0).any():
        raise AssertionError("Non-positive MthCap remains in the clean panel.")

    if df["MthCalDt"].isna().any():
        raise AssertionError("Missing MthCalDt remains in the clean panel.")



def build_monthly_history_panel(raw_path: str | Path) -> pd.DataFrame:
    """Build the security-level monthly history used for signal lookbacks/outcomes.

    This panel deliberately stops *before* the formation-date size and price
    screens. A stock's signal history and next-month realised return should not
    disappear merely because it failed the investability screen in an earlier
    or later month.

    Applied here:
    - exact-row deduplication;
    - validation of the WRDS CIZ common-stock query;
    - primary exchange filter N/A/Q.

    Not applied here:
    - NYSE size breakpoint;
    - $5 price screen.

    Those are formation-date eligibility rules and belong in the clean panel.
    """
    raw = _read_raw(raw_path)
    _assert_common_stock_query(raw)
    deduped, _ = _deduplicate_exact_rows(raw)
    history = _apply_exchange_filter(deduped)

    if history.duplicated(KEY).any():
        raise AssertionError(
            "History panel is not unique on PERMNO + MthCalDt."
        )

    return history.sort_values(KEY).reset_index(drop=True)


def build_clean_monthly_panel(
    raw_path: str | Path,
    config: CleaningConfig = CleaningConfig(),
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Build the primary monthly research panel.

    Returns
    -------
    clean : pd.DataFrame
        Final monthly panel after the pre-specified filters.
    audit : pd.DataFrame
        Stage-by-stage row and security counts.
    """
    raw = _read_raw(raw_path)
    _assert_common_stock_query(raw)

    rows = []

    def record(stage: str, frame: pd.DataFrame) -> None:
        rows.append(
            {
                "stage": stage,
                "rows": len(frame),
                "unique_permno": frame["PERMNO"].nunique(dropna=True),
                "months": frame["MthCalDt"].nunique(dropna=True),
            }
        )

    record("raw", raw)

    deduped, dedup_stats = _deduplicate_exact_rows(raw)
    record("exact_deduplicated", deduped)

    exchange = _apply_exchange_filter(deduped)
    record("primary_exchanges_N_A_Q", exchange)

    cap_valid = _apply_market_cap_requirement(
        exchange, config.require_positive_market_cap
    )
    record("valid_positive_market_cap", cap_valid)

    with_breakpoint = _attach_nyse_breakpoint(
        cap_valid, config.nyse_size_percentile
    )

    clean = _apply_size_and_price_screens(with_breakpoint, config)
    record(
        f"nyse_p{int(config.nyse_size_percentile * 100)}_and_price_ge_{config.min_price:g}",
        clean,
    )

    _assert_clean_panel(clean)

    audit = pd.DataFrame(rows)
    for name, value in dedup_stats.items():
        audit[name] = np.nan
        audit.loc[audit["stage"].eq("exact_deduplicated"), name] = value

    return clean.sort_values(KEY).reset_index(drop=True), audit


def save_clean_outputs(
    clean: pd.DataFrame,
    audit: pd.DataFrame,
    output_path: str | Path,
    audit_path: str | Path | None = None,
) -> None:
    """Save local processed outputs.

    The repository .gitignore excludes data/processed, so these files remain local.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_path, index=False)

    if audit_path is not None:
        audit_path = Path(audit_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit.to_csv(audit_path, index=False)


if __name__ == "__main__":
    RAW = Path("data/raw/monthly_stock_common_equity_2000_2025_prod_v1.csv.gz")
    OUT = Path("data/processed/monthly_clean_v1.csv.gz")
    AUDIT = Path("results/tables/monthly_cleaning_audit_v1.csv")

    panel, audit_table = build_clean_monthly_panel(RAW)
    print(audit_table.to_string(index=False))
    save_clean_outputs(panel, audit_table, OUT, AUDIT)
