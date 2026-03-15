# Predicting March Madness 2026

Using machine learning to forecast every possible matchup in the 2026 NCAA Men's and Women's basketball tournaments — 132,133 predictions total.

Built for the [Kaggle March Machine Learning Mania 2026](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) competition.

---

## Our Picks

### Men's — Who Cuts Down the Nets?

```mermaid
pie title Men's Title Probability
    "Michigan" : 21.0
    "Houston" : 12.8
    "Duke" : 12.2
    "Florida" : 9.2
    "Arizona" : 7.6
    "Purdue" : 7.3
    "UConn" : 5.4
    "Michigan St" : 5.4
    "Illinois" : 4.6
    "Field" : 14.5
```

| # | Team | Power Rating | Title Odds | Make Finals |
|---|------|:------------:|:----------:|:-----------:|
| 1 | **Michigan** | 2069 | **21.0%** | 25.9% |
| 2 | Houston | 1967 | 12.8% | 17.2% |
| 3 | Duke | 2078 | 12.2% | 17.3% |
| 4 | Florida | 2035 | 9.2% | 11.9% |
| 5 | Arizona | 2032 | 7.6% | 10.0% |
| 6 | Purdue | 1884 | 7.3% | 23.7% |
| 7 | UConn | 1971 | 5.4% | 9.1% |
| 8 | Michigan St | 1935 | 5.4% | 19.9% |

### Women's — Who Takes the Crown?

```mermaid
pie title Women's Title Probability
    "UConn" : 31.0
    "South Carolina" : 18.0
    "UCLA" : 17.1
    "LSU" : 10.0
    "Texas" : 5.7
    "Iowa" : 4.3
    "Duke" : 3.3
    "Field" : 10.6
```

| # | Team | Power Rating | Title Odds | Make Finals |
|---|------|:------------:|:----------:|:-----------:|
| 1 | **UConn** | 2259 | **31.0%** | 35.1% |
| 2 | South Carolina | 2200 | 18.0% | 20.0% |
| 3 | UCLA | 2212 | 17.1% | 18.8% |
| 4 | LSU | 2074 | 10.0% | 12.8% |
| 5 | Texas | 2131 | 5.7% | 6.8% |
| 6 | Iowa | 2015 | 4.3% | 25.1% |
| 7 | Duke | 2000 | 3.3% | 20.5% |

> Championship odds from 50,000 Monte Carlo tournament simulations using our model's head-to-head win probabilities.

---

## Marquee Matchups

Games the model thinks will be the most competitive if these teams meet:

| Matchup | Predicted Winner | Win Probability |
|---------|:----------------:|:---------------:|
| Tennessee vs Alabama | Tennessee | 50.5% |
| Arizona vs Houston | Arizona | 51.0% |
| Duke vs Illinois | Duke | 51.0% |
| Arizona vs Florida | Arizona | 51.4% |
| Florida vs Houston | Florida | 51.8% |
| Florida vs UConn | Florida | 52.3% |

And the matchups the model is most confident about:

| Matchup | Predicted Winner | Win Probability |
|---------|:----------------:|:---------------:|
| Michigan vs Kansas | Michigan | 90.6% |
| Michigan vs Alabama | Michigan | 90.1% |
| Duke vs Alabama | Duke | 87.7% |
| Michigan vs Gonzaga | Michigan | 86.4% |
| Duke vs Virginia | Duke | 86.3% |

---

## How It Works

```mermaid
flowchart LR
    A["20+ Years of\nNCAA Game Data"] --> B["139 Features\nPer Matchup"]
    B --> C["3 ML Models\nVote Together"]
    C --> D["Win Probability\nfor Every Matchup"]
```

**The short version:** We feed two decades of college basketball data into three machine learning models, and they vote on who wins every possible game.

### What the Model Looks At

We measure each team across **8 dimensions** before comparing any two teams head-to-head:

```mermaid
flowchart TD
    TEAM["How Good Is\nThis Team?"]

    TEAM --> ELO["Power Rating (Elo)\nOverall strength based\non wins, losses & margins"]
    TEAM --> FOUR["Playing Style\nShooting efficiency,\nturnover rate, rebounding"]
    TEAM --> RANK["Expert Rankings\nAggregated from 197\nnational ranking systems"]
    TEAM --> SOS["Schedule Strength\nHow tough were\ntheir opponents?"]
    TEAM --> MOM["Momentum\nWin rate over\nlast 10 games"]
    TEAM --> CONF["Conference Strength\nHow good is their\nleague top to bottom?"]
    TEAM --> QUAL["Team Quality Index\nLatent strength from\npoint differentials"]
    TEAM --> COACH["Coaching\nTournament experience\n& program tenure"]
```

For any matchup — say Michigan vs Duke — we compare all these dimensions and let the models figure out who has the edge.

### The Three Models

We don't rely on a single model. Three different algorithms each make independent predictions, and we average them:

| Model | What It's Good At |
|-------|-------------------|
| **LightGBM** | Fast, handles missing data well |
| **XGBoost** | Strong with structured/tabular data |
| **CatBoost** | Robust against overfitting |

When all three agree, we're confident. When they disagree, the average keeps us from being too extreme.

### What Matters Most

The model's top signals when predicting who wins (ranked by importance):

| # | Signal | In Plain English |
|---|--------|------------------|
| 1 | Peak Power Rating | The best a team played all season |
| 2 | Average Power Rating | Consistent strength across the year |
| 3 | End-of-Season Rating | Where the team finished |
| 4 | Schedule Strength | Strong opponents = battle-tested |
| 5 | Conference Quality | Playing in a tough league matters |
| 6 | Tournament Seed | Higher seeds historically win more |
| 7 | Free Throw Rate | Getting to the line is crucial in March |
| 8 | Offensive Efficiency | Points per possession |

---

## Accuracy

We validated the model by predicting past tournaments it had never seen:

| Tournament | Brier Score | Accuracy Context |
|------------|:----------:|-----------------|
| 2022 | 0.189 | Solid — St. Peter's Cinderella run was tough |
| 2023 | 0.194 | Good — UConn's dominance was predicted |
| 2024 | 0.161 | Strong — fewer major upsets |
| 2025 | 0.126 | Excellent — model improving with more data |
| **Average** | **0.167** | **Competitive with top public solutions** |

> **Brier Score** measures how close predictions are to reality (0 = perfect, 1 = worst). Lower is better. A coin flip scores 0.25.

---

## Run It Yourself

The full pipeline is in [`submission_notebook.ipynb`](submission_notebook.ipynb). It runs end-to-end on [Kaggle](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) or locally.

**Requirements:** Python 3.8+, pandas, numpy, scikit-learn, lightgbm, xgboost, catboost

```bash
# Local setup
pip install pandas numpy scipy scikit-learn lightgbm xgboost catboost

# Download competition data from Kaggle, place in march-machine-learning-mania-2026/
# Run the notebook — it handles everything from raw data to final predictions
```

For the full technical breakdown (hyperparameters, feature engineering details, Elo formulas, cross-validation strategy), see [TECHNICAL.md](TECHNICAL.md).

---

## Credits & Acknowledgments

This project builds on ideas from the Kaggle community. Key inspirations:

- **[goto-conversion winning solution](https://www.kaggle.com/code/kaito510/goto-conversion-winning-solution)** — favourite-longshot bias insight
- **[NCAA 2026 EDA, Elo & Gradient Ensemble](https://www.kaggle.com/code/ibrahimqasimi/ncaa-2026-eda-elo-ratings-and-gradient-esemble)** — Four Factors + multi-model ensemble approach
- **[NCAA 2026 Public Baseline](https://www.kaggle.com/code/ravi20076/ncaa2026-public-baseline-v1)** — GLM team quality metric & spline calibration
- **[Calculate Elo Ratings](https://www.kaggle.com/code/lennarthaupts/calculate-elo-ratings)** — Elo summary statistics (trend, volatility)
- **[NCAA 2026 Stage 2 LightGBM](https://www.kaggle.com/code/jiaoyouzhang/ncaa-2026-stage2-lightgbm)** — symmetric data augmentation technique

Data provided by [Kaggle](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) and the NCAA.
