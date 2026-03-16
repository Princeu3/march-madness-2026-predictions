# Predicting March Madness 2026

Using machine learning to forecast every possible matchup in the 2026 NCAA Men's and Women's basketball tournaments — 132,133 predictions total.

Built for the [Kaggle March Machine Learning Mania 2026](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) competition.

---

## Our Picks

### Men's — Who Cuts Down the Nets?

```mermaid
pie title Men's Title Probability
    "Duke" : 18.7
    "Michigan" : 17.8
    "Arizona" : 10.8
    "Houston" : 8.2
    "Florida" : 7.1
    "Iowa St" : 6.9
    "Illinois" : 6.3
    "Purdue" : 5.1
    "UConn" : 4.6
    "Michigan St" : 4.4
    "Field" : 10.1
```




| #   | Team         | Power Rating | Title Odds | Make Finals |
| --- | ------------ | ------------ | ---------- | ----------- |
| 1   | **Duke**     | 2078         | **18.7%**  | 22.1%       |
| 2   | Michigan     | 2069         | 17.8%      | 21.3%       |
| 3   | Arizona      | 2032         | 10.8%      | 14.2%       |
| 4   | Houston      | 1967         | 8.2%       | 11.5%       |
| 5   | Florida      | 2035         | 7.1%       | 9.8%        |
| 6   | Iowa St      | —            | 6.9%       | 9.4%        |
| 7   | Illinois     | 1909         | 6.3%       | 8.7%        |
| 8   | Purdue       | 1884         | 5.1%       | 7.6%        |
| 9   | UConn        | 1971         | 4.6%       | 7.1%        |
| 10  | Michigan St  | 1935         | 4.4%       | 6.8%        |


### Women's — Who Takes the Crown?

```mermaid
pie title Women's Title Probability
    "UConn" : 27.9
    "South Carolina" : 20.9
    "UCLA" : 17.0
    "Texas" : 13.4
    "LSU" : 3.6
    "Duke" : 3.1
    "Iowa" : 3.0
    "Field" : 11.1
```




| #   | Team               | Power Rating | Title Odds | Make Finals |
| --- | ------------------ | ------------ | ---------- | ----------- |
| 1   | **UConn**          | 2259         | **27.9%**  | 32.4%       |
| 2   | South Carolina     | 2200         | 20.9%      | 23.5%       |
| 3   | UCLA               | 2212         | 17.0%      | 19.2%       |
| 4   | Texas              | 2131         | 13.4%      | 15.6%       |
| 5   | LSU                | 2074         | 3.6%       | 5.2%        |
| 6   | Duke               | 2000         | 3.1%       | 4.8%        |
| 7   | Iowa               | 2015         | 3.0%       | 4.5%        |


> Championship odds from 50,000 Monte Carlo tournament simulations using our model's head-to-head win probabilities.

---

## Marquee Matchups

Games the model thinks will be the most competitive if these teams meet:


| Matchup              | Predicted Winner | Win Probability |
| -------------------- | ---------------- | --------------- |
| Duke vs Michigan     | Duke             | 50.3%           |
| Florida vs UConn     | Florida          | 50.5%           |
| Kansas vs Purdue     | Kansas           | 50.6%           |
| Arizona vs Houston   | Arizona          | 51.0%           |
| Duke vs Illinois     | Duke             | 51.0%           |
| Arizona vs Florida   | Arizona          | 51.4%           |


And the matchups the model is most confident about:


| Matchup              | Predicted Winner | Win Probability |
| -------------------- | ---------------- | --------------- |
| Michigan vs Kansas   | Michigan         | 90.5%           |
| Michigan vs BYU      | Michigan         | 89.8%           |
| Duke vs St Mary's    | Duke             | 88.9%           |
| Duke vs Alabama      | Duke             | 87.7%           |
| Michigan vs Gonzaga  | Michigan         | 86.4%           |


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


| Model        | What It's Good At                   |
| ------------ | ----------------------------------- |
| **LightGBM** | Fast, handles missing data well     |
| **XGBoost**  | Strong with structured/tabular data |
| **CatBoost** | Robust against overfitting          |


When all three agree, we're confident. When they disagree, the average keeps us from being too extreme.

### What Matters Most

The model's top signals when predicting who wins (ranked by importance):


| #   | Signal               | In Plain English                        |
| --- | -------------------- | --------------------------------------- |
| 1   | Peak Power Rating    | The best a team played all season       |
| 2   | Average Power Rating | Consistent strength across the year     |
| 3   | End-of-Season Rating | Where the team finished                 |
| 4   | Schedule Strength    | Strong opponents = battle-tested        |
| 5   | Conference Quality   | Playing in a tough league matters       |
| 6   | Tournament Seed      | Higher seeds historically win more      |
| 7   | Free Throw Rate      | Getting to the line is crucial in March |
| 8   | Offensive Efficiency | Points per possession                   |


---

## Accuracy

We validated the model by predicting past tournaments it had never seen:


| Tournament  | Brier Score | Accuracy Context                             |
| ----------- | ----------- | -------------------------------------------- |
| 2022        | 0.189       | Solid — St. Peter's Cinderella run was tough |
| 2023        | 0.194       | Good — UConn's dominance was predicted       |
| 2024        | 0.161       | Strong — fewer major upsets                  |
| 2025        | 0.126       | Excellent — model improving with more data   |
| **Average** | **0.168**   | **Competitive with top public solutions**    |


> scores 0.25.

---

## Run It Yourself

The full pipeline is in `[submission_notebook.ipynb](submission_notebook.ipynb)`. It runs end-to-end on [Kaggle](https://www.kaggle.com/competitions/march-machine-learning-mania-2026) or locally.

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