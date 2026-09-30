# Final Results Registry

This file freezes the numerical results used in the final research paper.

## Sample
- Sample: 2000-01-31 to 2025-12-31
- Formation rows: 601,350
- Unique PERMNO: 7,423
- Formation months: 312
- Valid momentum observations: 544,090
- Average monthly investable stocks: 1,927.40
- Median monthly investable stocks: 1,843

## Baseline momentum
- Mean Rank IC: 0.00767956
- Mean VW Q5-Q1: 0.000745766
- Mean EW Q5-Q1: 0.00245703
- VW HAC6 p: 0.820681
- EW HAC6 p: 0.384066
- Rank IC HAC6 p: 0.338769

## Aggregate concentration
- Top10 -> VW coefficient per +10pp: -0.003275; p=0.535566
- Top10 + trend: -0.001617; p=0.799224
- HHI coefficient per +0.01: -0.006091; p=0.469980
- Top10 -> EW: +0.003260; p=0.408711
- Top10 -> Rank IC: +0.006309; p=0.612525
- Lagged Top10 -> VW: -0.003030; p=0.581771

## Mega-cap exclusion
- ExTop5 mean spread: 0.001375; delta=0.000629; HAC6 p=0.356599
- ExTop10 mean spread: 0.001844; delta=0.001099; HAC6 p=0.269173
- ExTop20 mean spread: 0.002456; delta=0.001711; HAC6 p=0.115508

## Mega-cap decomposition
- DirectWeightEffect: 0.001114; HAC6 p=0.259073
- ReRankingEffect: -0.000016; HAC6 p=0.865577
- TotalChange: 0.001099; HAC6 p=0.269173
- Q1 Top10 mean formation weight share: 0.099454
- Q5 Top10 mean formation weight share: 0.176585
- Q1 mean return contribution: 0.0015374
- Q5 mean return contribution: 0.00219508

## Concentration-to-mechanism bridge
### DirectWeightEffect on Top10Share
- Coefficient per +10pp: 0.001840
- HAC6 SE: 0.002383
- t: 0.771983
- p: 0.440124
- 95% CI: [-0.002831, 0.006510]
- N: 299
- With linear trend: coefficient 0.002748; p=0.282749

### Q5-minus-Q1 Top10 formation-weight gap on Top10Share
- Coefficient per +10pp: 0.244777
- HAC6 SE: 0.037095
- t: 6.598576
- p: 4.15e-11
- 95% CI: [0.172071, 0.317483]
- N: 300
- R2: 0.296890
- With linear trend: coefficient 0.099303; p=0.011990; 95% CI [0.021837, 0.176770]

## Industry neutralisation
- Raw VW: 0.000746
- FF49-neutral VW: -0.000255
- Delta: -0.001001
- HAC6 p: 0.584513
- Raw Rank IC: 0.007680
- Neutral Rank IC: 0.007625
- Delta Rank IC: -0.000054
- HAC6 p: 0.986204

## Beta neutralisation
- Original VW: 0.000746
- Beta-eligible VW: 0.000746
- Beta-neutral VW: -0.000389
- Neutralisation effect: -0.001135
- HAC6 p: 0.446078
- HAC12 p: 0.388316
- Leg-rescaled effect: -0.000578; HAC6 p=0.702503
- Ex-post market beta raw: -0.381325; p=0.000439
- Ex-post market beta beta-neutral: -0.157987; p=0.040509

## External validation against Kenneth French Mom
Common sample: 299 holding months.
- Project VW mean: 0.000746; monthly vol 0.055643
- Project EW mean: 0.002457; monthly vol 0.046319
- French Mom mean: 0.002021; monthly vol 0.046342
- Corr(Project VW, French Mom): 0.875434
- Corr(Project EW, French Mom): 0.916523
- VW benchmark beta: 1.051139; 95% CI [0.905802, 1.196475]; R2 0.766385; alpha p=0.404096
- EW benchmark beta: 0.916074; 95% CI [0.840013, 0.992135]; R2 0.840014; alpha p=0.590216

## CRSP CIZ delisting-return treatment
Official CIZ documentation states that MthRet is daily total return compounded for the period and includes delisting returns when appropriate. No separate legacy-style DLRET merge is applied to MthRet.
