# Source Module Guide

| Module | Role |
|---|---|
| `clean_monthly.py` | Monthly cleaning, investable universe, history panel, market-state panel |
| `signals.py` | 12-2 momentum construction and quintile assignment |
| `portfolio.py` | Rank IC and VW/EW portfolio returns |
| `inference.py` | HAC mean inference |
| `concentration.py` | PERMCO company-level Top-N, HHI, effective firms |
| `conditioning.py` | Concentration-performance regressions and regimes |
| `mega_cap.py` | Top-N company identification and exclusion |
| `mega_cap_decomposition.py` | Fixed-rank direct-weight / re-ranking decomposition |
| `industry_neutral.py` | FF49 and ICB industry neutralisation |
| `daily_data.py` | Daily stock, market, and RF alignment/audit |
| `beta.py` | Rolling ex-ante CAPM beta estimation |
| `beta_neutral.py` | Market-overlay and leg-rescaling beta neutralisation |
| `concentration_mechanism_bridge.py` | Final concentration-to-weight-mechanism bridge tests |
| `external_validation.py` | Kenneth French Mom external validation |

The modules are deliberately small and research-specific rather than combined into a single monolithic script.
