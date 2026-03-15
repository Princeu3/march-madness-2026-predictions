# March Machine Learning Mania 2026

Kaggle competition to predict the 2026 NCAA Men's and Women's basketball tournament outcomes.

**Competition:** [March Machine Learning Mania 2026](https://www.kaggle.com/competitions/march-machine-learning-mania-2026)
**Metric:** Brier Score (lower is better)
**OOF CV Score:** 0.1673

---

## Architecture Overview

```mermaid
flowchart TD
    subgraph DATA["Raw Data (Kaggle)"]
        RS[Regular Season Results]
        DET[Detailed Box Scores]
        MASS[Massey Ordinals<br/>197 ranking systems]
        SEEDS[Tournament Seeds]
        COACH[Coach History]
        CONF[Conference Data]
        TOURN[Historical Tournament Results]
    end

    subgraph FEATURES["Feature Engineering"]
        ELO[Elo Ratings<br/>MOV + Home Court + Regression]
        FF[Four Factors<br/>OEff, DEff, EFG%, TOR, etc.]
        MAS_F[Massey Features<br/>Mean, Median, Top 16 Systems]
        GLM[GLM Team Quality<br/>Ridge on Point Differential]
        SOS[Strength of Schedule<br/>Mean Opponent Elo]
        MOM[Momentum<br/>Last 10 Game Win Rate]
        CS[Conference Strength<br/>Mean Conference Elo]
        CF[Coach Features<br/>Tourney Exp + Tenure]
    end

    subgraph MODEL["Ensemble Model"]
        LGB[LightGBM]
        XGB[XGBoost]
        CAT[CatBoost]
        AVG[Simple Average<br/>+ Clip to 0.02-0.98]
    end

    subgraph OUTPUT["Output"]
        SUB[submission.csv<br/>132,133 matchup predictions]
    end

    RS --> ELO & FF & SOS & MOM
    DET --> FF
    MASS --> MAS_F
    SEEDS --> GLM
    COACH --> CF
    CONF --> CS
    RS --> GLM

    ELO & FF & MAS_F & GLM & SOS & MOM & CS & CF --> |Merge per Team-Season| TEAM_FEAT[Unified Feature Table<br/>57 features per team]

    TOURN --> |Build matchup pairs| TRAIN[Training Data<br/>8,296 tournament games]
    TEAM_FEAT --> TRAIN

    TRAIN --> LGB & XGB & CAT
    LGB --> AVG
    XGB --> AVG
    CAT --> AVG
    AVG --> SUB
```

---

## Elo Rating System

```mermaid
flowchart LR
    subgraph INIT["Initialization"]
        START[All teams start at 1500]
    end

    subgraph GAME["Per-Game Update"]
        HCA[Home Court<br/>+100 Elo to home team]
        EXP[Expected Win<br/>1 / 1+10^Δ/400]
        MOV[MOV Multiplier<br/>K × ln margin+1]
        UPD[Update Ratings<br/>Winner ↑ Loser ↓]
    end

    subgraph SEASON["Season Boundary"]
        REG[Regress to Mean<br/>75% carry + 25% × 1500]
    end

    subgraph OUT["Output Features"]
        LAST[Elo_Last]
        MEAN[Elo_Mean]
        MAX[Elo_Max]
        STD[Elo_Std]
        TREND[Elo_Trend<br/>Linear slope]
    end

    START --> HCA --> EXP --> MOV --> UPD
    UPD -->|Next game| HCA
    UPD -->|New season| REG --> HCA
    UPD --> OUT
```

### Elo Parameters

| Parameter | Value | Why |
|-----------|-------|-----|
| K-factor base | 20 | Moderate update speed |
| Home advantage | +100 | ~65% home win rate in college hoops |
| Width | 400 | Standard Elo scale |
| Initial rating | 1500 | Neutral starting point |
| Season carry | 75% | Accounts for roster turnover |
| MOV scaling | ln(margin + 1) | Blowouts are more informative than 1-pt wins |

---

## Feature Engineering Pipeline

```mermaid
flowchart TB
    subgraph PER_TEAM["Per Team-Season Features (57 total)"]
        direction TB
        subgraph ELO_F["Elo (5)"]
            E1[Last / Mean / Max / Std / Trend]
        end
        subgraph STATS_F["Four Factors (25)"]
            S1[WinPct, PointDiff, Score, OppScore]
            S2[OEff, DEff, NEff]
            S3[EFG%, TOR, ORPCT, FTR]
            S4[Opponent versions of above]
            S5[3PT%, AstRate, Stl, Blk, DR, Poss, FGA, PF]
        end
        subgraph MASSEY_F["Massey (20)"]
            M1[Mean / Median / Min / Std across all systems]
            M2[Individual ranks: POM, SAG, MOR, DOK, etc.]
        end
        subgraph OTHER_F["Other (7)"]
            O1[SOS - Strength of Schedule]
            O2[Momentum - Last 10 games]
            O3[ConfStr - Conference Strength]
            O4[Quality - GLM team strength]
            O5[SeedNum - Tournament seed]
            O6[CoachExp - Coach tourney appearances]
            O7[CoachTenure - Consecutive years]
        end
    end

    subgraph MATCHUP["Per-Matchup Features (139 total)"]
        T1F[T1_* features ×46]
        T2F[T2_* features ×46]
        DIFF[d_* difference features ×46]
        GEN[IsWomen indicator ×1]
    end

    PER_TEAM -->|Team 1 lookup| T1F
    PER_TEAM -->|Team 2 lookup| T2F
    T1F --> |T1 minus T2| DIFF
    T1F & T2F & DIFF & GEN --> MODEL_IN[Model Input]
```

---

## Model Training Pipeline

```mermaid
flowchart TD
    subgraph CV["Time-Based Cross-Validation"]
        direction TB
        FOLD1["Fold 1: Train <2022 → Val 2022"]
        FOLD2["Fold 2: Train <2023 → Val 2023"]
        FOLD3["Fold 3: Train <2024 → Val 2024"]
        FOLD4["Fold 4: Train <2025 → Val 2025"]
    end

    subgraph MODELS["3 Models per Fold"]
        LGB2[LightGBM<br/>lr=0.02, leaves=31]
        XGB2[XGBoost<br/>lr=0.02, depth=5]
        CAT2[CatBoost<br/>lr=0.02, depth=5]
    end

    subgraph RETRAIN["Final Retraining"]
        FULL[Train on ALL data<br/>Best iteration × 1.1]
        PRED[Predict 132K matchups]
        CLIP[Clip to 0.02 - 0.98]
        ENS[Average 3 models]
    end

    CV --> |Best iterations| RETRAIN
    MODELS --> |Early stopping<br/>patience=200| CV

    FULL --> PRED --> ENS --> CLIP --> FINAL[submission.csv]
```

### Cross-Validation Results

| Season | Brier Score | Games |
|--------|------------|-------|
| 2022 | 0.1889 | 536 |
| 2023 | 0.1935 | 536 |
| 2024 | 0.1607 | 536 |
| 2025 | 0.1262 | 536 |
| **Overall** | **0.1673** | **2144** |

### Model Hyperparameters

| Parameter | LightGBM | XGBoost | CatBoost |
|-----------|----------|---------|----------|
| Learning rate | 0.02 | 0.02 | 0.02 |
| Max depth/leaves | 31 leaves | depth 5 | depth 5 |
| Subsample | 0.8 | 0.8 | 0.8 |
| Col sample | 0.8 | 0.8 | - |
| Min samples | 15 | 15 | 15 |
| L1 reg | 0.1 | 0.1 | - |
| L2 reg | 1.0 | 1.0 | 3.0 |
| Max rounds | 2000 | 2000 | 2000 |
| Early stopping | 200 | 200 | 200 |

---

## Top Features (by LightGBM Gain)

| Rank | Feature | Description |
|------|---------|-------------|
| 1 | d_Elo_Max | Difference in peak Elo rating |
| 2 | d_Elo_Mean | Difference in average Elo |
| 3 | d_Elo_Last | Difference in final Elo |
| 4 | d_SOS | Difference in strength of schedule |
| 5 | d_ConfStr | Difference in conference strength |
| 6 | d_SeedNum | Difference in tournament seed |
| 7 | d_FTR | Difference in free throw rate |
| 8 | d_OEff | Difference in offensive efficiency |
| 9 | d_OppFG3Pct | Difference in opponent 3PT% allowed |
| 10 | d_PointDiff | Difference in avg point differential |

---

## 2026 Predictions

### Men's Championship Odds

```mermaid
pie title Men's Championship Probability
    "Michigan" : 21.0
    "Houston" : 12.8
    "Duke" : 12.2
    "Florida" : 9.2
    "Arizona" : 7.6
    "Purdue" : 7.3
    "UConn" : 5.4
    "Michigan St" : 5.4
    "Illinois" : 4.6
    "Others" : 14.5
```

| # | Team | Elo | Championship | Finals |
|---|------|-----|-------------|--------|
| 1 | Michigan | 2069 | 21.0% | 25.9% |
| 2 | Houston | 1967 | 12.8% | 17.2% |
| 3 | Duke | 2078 | 12.2% | 17.3% |
| 4 | Florida | 2035 | 9.2% | 11.9% |
| 5 | Arizona | 2032 | 7.6% | 10.0% |
| 6 | Purdue | 1884 | 7.3% | 23.7% |
| 7 | UConn | 1971 | 5.4% | 9.1% |
| 8 | Michigan St | 1935 | 5.4% | 19.9% |

### Women's Championship Odds

```mermaid
pie title Women's Championship Probability
    "UConn" : 31.0
    "South Carolina" : 18.0
    "UCLA" : 17.1
    "LSU" : 10.0
    "Texas" : 5.7
    "Iowa" : 4.3
    "Duke" : 3.3
    "Others" : 10.6
```

| # | Team | Elo | Championship | Finals |
|---|------|-----|-------------|--------|
| 1 | UConn | 2259 | 31.0% | 35.1% |
| 2 | South Carolina | 2200 | 18.0% | 20.0% |
| 3 | UCLA | 2212 | 17.1% | 18.8% |
| 4 | LSU | 2074 | 10.0% | 12.8% |
| 5 | Texas | 2131 | 5.7% | 6.8% |
| 6 | Iowa | 2015 | 4.3% | 25.1% |
| 7 | Duke | 2000 | 3.3% | 20.5% |

---

## Data Flow Summary

```mermaid
flowchart LR
    subgraph INPUT["Input Data"]
        A[35 CSV files<br/>~170MB total]
    end

    subgraph PROCESS["Processing"]
        B[Feature Engineering<br/>57 features/team]
        C[Matchup Construction<br/>139 features/game]
        D[3-Model Ensemble<br/>LGB + XGB + CAT]
    end

    subgraph OUTPUT["Output"]
        E[submission.csv<br/>132,133 predictions]
    end

    A --> B --> C --> D --> E
```

---

## Repository Structure

```
MarchMadness/
├── README.md                    # This file
├── submission_notebook.ipynb    # Main notebook (submit to Kaggle)
├── submission.csv               # Generated predictions
├── context.txt                  # Competition notes & reference links
├── kaggle.json                  # Kaggle API credentials (gitignored)
├── march-machine-learning-mania-2026/  # Competition data (gitignored)
│   ├── MRegularSeasonCompactResults.csv
│   ├── MRegularSeasonDetailedResults.csv
│   ├── MMasseyOrdinals.csv (128MB)
│   ├── MNCAATourneyCompactResults.csv
│   ├── MNCAATourneySeeds.csv
│   ├── SampleSubmissionStage2.csv
│   └── ... (35 files total)
└── notebooks/                   # Reference notebooks (gitignored)
    ├── goto-conversion-winning-solution.ipynb
    ├── ncaa-2026-stage2-lightgbm.ipynb
    ├── ncaa-2026-eda-elo-ratings-and-gradient-esemble.ipynb
    ├── ncaa2026-public-baseline-v1.ipynb
    ├── calculate-elo-ratings.ipynb
    └── ...
```

---

## Key Design Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Elo vs raw stats | Both | Elo captures team strength trajectory; stats capture play style |
| MOV in Elo | log(margin+1) | Blowouts informative but diminishing returns |
| Massey approach | Average + top 16 individual | Robust aggregate + specific signal from best systems |
| GLM Quality | Ridge regression | More stable than OLS for team fixed-effects model |
| Ensemble method | Simple average | Robust; weighted averaging rarely helps in practice |
| Prediction clipping | [0.02, 0.98] | Avoid catastrophic Brier penalty from extreme predictions |
| CV strategy | Time-based expanding | Respects temporal nature; no future data leakage |
| Training data | Tournament games only | Tournament dynamics differ from regular season |
| Missing 2026 seeds | Use other features | Seeds unavailable pre-Selection Sunday; model still works |
| Men + Women combined | Single model + IsWomen flag | More training data; model learns gender-specific patterns |

---

## Reference Notebooks Analyzed

| Notebook | Approach | Key Technique |
|----------|----------|---------------|
| goto-conversion | Betting odds conversion | Favourite-longshot bias correction |
| ncaa-2026-stage2-lightgbm | LightGBM classifier | Symmetric data augmentation |
| ncaa-2026-elo-gradient-ensemble | LGB+XGB+CAT ensemble | Four Factors + Elo + 30 features |
| ncaa2026-public-baseline-v1 | XGBoost regression | GLM quality + spline calibration |
| calculate-elo-ratings | Pure Elo | Rich Elo summary stats (trend, std) |
| march-mania-2026-starter | Logistic regression | Google ADK agent demo |
| lb-0-0-time-and-chance | Historical lookup | Stage 1 leaderboard exploit (not useful for Stage 2) |
