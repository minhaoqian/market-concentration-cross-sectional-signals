#!/usr/bin/env python3
"""Safely organise local presentation outputs without touching research code/data.

Default mode is dry-run. Use --apply to move recognised final-report / result
files found in the repository root into canonical folders.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import shutil

REPORT_NAMES = {
    "Minhao_Qian_Market_Concentration_Momentum_Final.docx",
    "Minhao_Qian_Market_Concentration_Momentum_Final.pdf",
    "Minhao_Qian_Market_Concentration_Momentum_Research_Note.docx",
    "Minhao_Qian_Market_Concentration_Momentum_Research_Note.pdf",
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="actually move files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]

    for rel in ["data/raw","data/interim","data/processed","paper/final","results/tables","results/figures"]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    moves = []
    for p in root.iterdir():
        if not p.is_file():
            continue
        if p.name in REPORT_NAMES:
            moves.append((p, root / "paper/final" / p.name))
        elif p.name.startswith("table") and p.suffix.lower() == ".csv":
            moves.append((p, root / "results/tables" / p.name))
        elif p.name.startswith("figure") and p.suffix.lower() in {".png",".svg",".pdf"}:
            moves.append((p, root / "results/figures" / p.name))

    for src, dst in moves:
        print(f"{'[MOVE]' if args.apply else '[DRY ]'} {src.name} -> {dst.relative_to(root)}")
        if args.apply:
            if dst.exists():
                raise FileExistsError(f"Destination already exists: {dst}")
            shutil.move(str(src), str(dst))

    if not moves:
        print("No recognised root-level presentation files need moving.")

    print("\nInput check:")
    for rel in [
        "data/raw/monthly_stock_common_equity_2000_2025_prod_v1.csv.gz",
        "data/raw/daily_stock_naq_1998_2025_prod_v1.csv.gz",
        "data/raw/daily_crsp_vw_market_1998_2025_v1.csv.gz",
        "data/raw/F-F_Research_Data_Factors_daily.csv",
        "data/raw/F-F_Momentum_Factor.csv",
    ]:
        print(f"{'OK ' if (root / rel).exists() else '---'} {rel}")

if __name__ == "__main__":
    main()
