# Market Concentration and Cross-Sectional Momentum

**Empirical quantitative-finance research project | US equities, 2000-2025**

> **Final conclusion:** market concentration appears more relevant to the **portfolio implementation** of value-weighted momentum than to the **informational content** of the momentum ranking itself.

## Start here

- [Final report landing page](FINAL_REPORT.md)
- [Final PDF](paper/Minhao_Qian_Market_Concentration_Momentum_Final.pdf)
- [Final Word version](paper/Minhao_Qian_Market_Concentration_Momentum_Final.docx)
- [GitHub-readable full paper](paper/research_note.md)
- [Final numerical results](docs/final_results_registry.md)
- [Research log / methodology locks](docs/research_log.md)
- [Project structure](docs/PROJECT_STRUCTURE.md)

## Headline results

| Result | Estimate |
|---|---:|
| Baseline VW momentum | +0.0746% / month |
| Baseline EW momentum | +0.2457% / month |
| Mean Rank IC | 0.00768 |
| Ex-Top10 improvement | +0.1099 pp / month |
| Direct-weight component | +0.1114 pp / month |
| Re-ranking component | -0.0016 pp / month |
| Concentration -> Q5-Q1 mega-cap weight gap | +24.48 pp per +10pp Top10 share |
| French Mom correlation: project VW | 0.875 |
| French Mom correlation: project EW | 0.917 |

## Research design

The project studies one pre-specified signal: **12-2 price momentum**.

It separates:
1. **signal quality** - Rank IC and cross-sectional ordering;
2. **portfolio implementation** - VW vs EW, mega-cap exclusion, direct-weight decomposition;
3. **systematic exposure** - industry neutralisation and ex-ante market-beta neutralisation.

Primary inference uses Newey-West HAC lag 6, with lag 12 as robustness.

## Repository map

- `paper/` - final research note
- `results/` - publication-facing result tables and figures
- `notebooks/` - sequential empirical workflow, 01 through 16
- `src/` - reusable research code
- `docs/` - methodology, data dictionary, audit trail, literature notes
- `data/` - local-only licensed inputs; raw CRSP data are not committed
- `scripts/` - local project housekeeping / reproducibility helpers

## Reproducibility

Raw CRSP data are licensed and intentionally excluded from GitHub. An authorised WRDS user can reproduce the project by placing the expected source files under `data/raw/` and running the notebooks in numerical order.

The external benchmark data from the Kenneth French Data Library are small public research files and are used only for validation.

## Status

**Research v1: complete.**

The final professor-style review added:
- a concentration-to-weight-mechanism bridge test;
- external validation against Kenneth French Mom;
- explicit verification of CIZ delisting-return treatment;
- tighter separation between mechanical decomposition evidence and statistical precision.
