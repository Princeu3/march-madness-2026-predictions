# Technical Documentation

Detailed architecture, feature engineering, model configuration, and design decisions.

---

## Architecture Overview

```mermaid
flowchart TD
    subgraph DATA["Raw Data"]
        RS[Regular Season Results]
        DET[Detailed Box Scores]
        MASS[Massey Ordinals — 197 ranking systems]
        SEEDS[Tournament Seeds]
        COACH[Coach History]
        CONF[Conference Data]
        TOURN[Historical Tournament Results]
    end

    subgraph FEATURES["Feature Engineering"]
        ELO[Elo Ratings — MOV + Home Court + Regression]
        FF[Four Factors — OEff, DEff, EFG%, TOR, etc.]
        MAS_F[Massey Features — Mean, Median, Top 16 Systems]
        GLM[GLM Team Quality — Ridge on Point Differential]
        SOS[Strength of Schedule — Mean Opponent Elo]
        MOM[Momentum — Last 10 Game Win Rate]
        CS[Conference Strength — Mean Conference Elo]
        CF[Coach Features — Tourney Exp + Tenure]
    end

    subgraph MODEL["Ensemble Model"]
        LGB[LightGBM]
        XGB[XGBoost]
        CAT[CatBoost]
        AVG[Simple Average + Clip to 0.02–0.98]
    end

    subgraph OUTPUT["Output"]
        SUB[submission.csv — 132,133 matchup predictions]
    end

    RS --> ELO & FF & SOS & MOM
    DET --> FF
    MASS --> MAS_F
    SEEDS --> GLM
    COACH --> CF
    CONF --> CS
    RS --> GLM

    ELO & FF & MAS_F & GLM & SOS & MOM & CS & CF --> |Merge per Team-Season| TEAM_FEAT[Unified Feature Table — 57 features per team]

    TOURN --> |Build matchup pairs| TRAIN[Training Data — 8,296 tournament games]
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
        HCA[Home Court — +100 Elo to home team]
        EXP["Expected Win — 1 / (1+10^(Δ/400))"]
        MOV["MOV Multiplier — K × ln(margin+1)"]
        UPD[Update Ratings — Winner up, Loser down]
    end

    subgraph SEASON["Season Boundary"]
        REG["Regress to Mean — 75% carry + 25% × 1500"]
    end

    subgraph OUT["Output Features"]
        LAST[Elo_Last]
        MEAN[Elo_Mean]
        MAX[Elo_Max]
        STD[Elo_Std]
        TREND[Elo_Trend — Linear slope]
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
            S3["EFG%, TOR, ORPCT, FTR"]
            S4[Opponent versions of above]
            S5["3PT%, AstRate, Stl, Blk, DR, Poss, FGA, PF"]
        end
        subgraph MASSEY_F["Massey (20)"]
            M1[Mean / Median / Min / Std across all systems]
            M2["Individual ranks: POM, SAG, MOR, DOK, etc."]
        end
        subgraph OTHER_F["Other (7)"]
            O1[SOS — Strength of Schedule]
            O2[Momentum — Last 10 games]
            O3[ConfStr — Conference Strength]
            O4[Quality — GLM team strength]
            O5[SeedNum — Tournament seed]
            O6[CoachExp — Coach tourney appearances]
            O7[CoachTenure — Consecutive years]
        end
    end

    subgraph MATCHUP["Per-Matchup Features (139 total)"]
        T1F["T1_* features ×46"]
        T2F["T2_* features ×46"]
        DIFF["d_* difference features ×46"]
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
        FOLD1["Fold 1: Train on pre-2022 — Validate on 2022"]
        FOLD2["Fold 2: Train on pre-2023 — Validate on 2023"]
        FOLD3["Fold 3: Train on pre-2024 — Validate on 2024"]
        FOLD4["Fold 4: Train on pre-2025 — Validate on 2025"]
    end

    subgraph MODELS["3 Models per Fold"]
        LGB2["LightGBM — lr=0.02, leaves=31"]
        XGB2["XGBoost — lr=0.02, depth=5"]
        CAT2["CatBoost — lr=0.02, depth=5"]
    end

    subgraph RETRAIN["Final Retraining"]
        FULL["Train on ALL data — Best iteration × 1.1"]
        PRED[Predict 132K matchups]
        ENS[Average 3 models]
        CLIP[Clip to 0.02–0.98]
    end

    CV --> |Best iterations| RETRAIN
    MODELS --> |Early stopping patience=200| CV

    FULL --> PRED --> ENS --> CLIP --> FINAL[submission.csv]
```

### Cross-Validation Results

| Season | Brier Score | Games |
|--------|:----------:|:-----:|
| 2022 | 0.1889 | 536 |
| 2023 | 0.1935 | 536 |
| 2024 | 0.1607 | 536 |
| 2025 | 0.1262 | 536 |
| **Overall** | **0.1673** | **2144** |

### Model Hyperparameters

| Parameter | LightGBM | XGBoost | CatBoost |
|-----------|:--------:|:-------:|:--------:|
| Learning rate | 0.02 | 0.02 | 0.02 |
| Max depth/leaves | 31 leaves | depth 5 | depth 5 |
| Subsample | 0.8 | 0.8 | 0.8 |
| Col sample | 0.8 | 0.8 | — |
| Min samples | 15 | 15 | 15 |
| L1 reg | 0.1 | 0.1 | — |
| L2 reg | 1.0 | 1.0 | 3.0 |
| Max rounds | 2000 | 2000 | 2000 |
| Early stopping | 200 | 200 | 200 |

---

## Top Features (by LightGBM Gain)

| Rank | Feature | Description |
|:----:|---------|-------------|
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

## Key Design Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Elo vs raw stats | Both | Elo captures team strength trajectory; stats capture play style |
| MOV in Elo | log(margin+1) | Blowouts informative but diminishing returns |
| Massey approach | Average + top 16 individual | Robust aggregate + specific signal from best systems |
| GLM Quality | Ridge regression | More stable than OLS for team fixed-effects model |
| Ensemble method | Simple average | Robust; weighted averaging rarely helps in practice |
| Prediction clipping | [0.02, 0.98] | Avoid catastrophic penalty from extreme predictions |
| CV strategy | Time-based expanding | Respects temporal nature; no future data leakage |
| Training data | Tournament games only | Tournament dynamics differ from regular season |
| Missing 2026 seeds | Use other features | Seeds unavailable pre-Selection Sunday; model still works |
| Men + Women combined | Single model + IsWomen flag | More training data; model learns gender-specific patterns |

---

## Repository Structure

```
MarchMadness/
├── README.md                  # Project overview & predictions
├── TECHNICAL.md               # This file — full technical details
├── submission_notebook.ipynb   # Complete pipeline (runs on Kaggle)
└── .gitignore
```
