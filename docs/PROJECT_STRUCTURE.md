# Project Structure

The repository is intentionally organised as a reproducible research pipeline. Historical notebooks and methodology logs are retained rather than deleted because they document how the final result was reached.

```text
market-concentration-cross-sectional-signals/
├── README.md
├── FINAL_REPORT.md
├── requirements.txt
├── data/
│   ├── README.md
│   ├── raw/          # local only, gitignored
│   ├── interim/      # local only, gitignored
│   └── processed/    # local only, gitignored
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   ├── analysis_plan.md
│   ├── data_dictionary.md
│   ├── literature_review.md
│   ├── sample_construction.md
│   ├── research_log.md
│   ├── final_results_registry.md
│   └── reference/
├── notebooks/
│   ├── README.md
│   └── 01_... through 16_...
├── paper/
│   ├── README.md
│   ├── research_note.md
│   └── final/        # recommended location for final PDF/DOCX locally
├── results/
│   ├── README.md
│   ├── tables/
│   └── figures/
├── scripts/
│   └── organize_local_repo.py
└── src/
    ├── README.md
    └── reusable Python modules
```

## What is canonical?

For final interpretation, use:
1. `paper/research_note.md` - canonical paper text;
2. `docs/final_results_registry.md` - canonical numeric registry;
3. `docs/research_log.md` - methodology and pre-specification audit trail;
4. notebooks 14-16 - final reporting, bridge, and external validation.

Earlier planning files are retained for provenance. They are not the final source of numerical claims.

## Why the notebooks are not collapsed

The numbered notebooks document the sequence of the research:
- data audit;
- signal construction;
- baseline inference;
- concentration;
- timing;
- mega-cap mechanism;
- industry neutralisation;
- daily beta infrastructure;
- beta neutralisation;
- final synthesis and external validation.

Keeping them in numerical order makes the project easier to audit and discuss in interviews.

## Local files

Licensed CRSP files stay under `data/raw/` and are never committed.

Final binary deliverables should be stored locally under:

```text
paper/final/
    Minhao_Qian_Market_Concentration_Momentum_Final.docx
    Minhao_Qian_Market_Concentration_Momentum_Final.pdf
```

Publication-facing CSVs and images belong under `results/tables/` and `results/figures/`.
