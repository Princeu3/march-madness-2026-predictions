# LinkedIn Post — March Madness 2026

---

**Duke vs Michigan is a coin flip.**

That's what our ML model says about a potential championship game — 50.3% to 49.7%. Dead even.

My team built a machine learning pipeline that predicts every possible matchup in the 2026 NCAA Tournament — 132,133 predictions total. Here's what the model sees:

**Men's Title Odds:**
- Duke — 18.7%
- Michigan — 17.8%
- Arizona — 10.8%
- Houston — 8.2%
- Florida — 7.1%

**The Final Four Path:**
- Semi 1 (East vs South): Duke over Florida — 63% confidence
- Semi 2 (West vs Midwest): Michigan over Arizona — 59% confidence
- Championship: Duke vs Michigan — a true coin flip

**Women's Pick:** UConn at 27.9% — and they went 34-0 this season. The model still only gives them a ~28% shot. That's how hard it is to win six straight in March.

**How it works:**
We trained an ensemble of three gradient boosting models (LightGBM, XGBoost, CatBoost) on 20 years of NCAA game data. Each team is measured across 139 features — Elo ratings, shooting efficiency, strength of schedule, momentum, coaching experience, and signals from 197 national ranking systems.

The top predictor? Peak power rating — the best a team played all season matters more than where they finished.

**Upsets to watch Thursday:**
- Iowa over (8) Clemson — 57%
- Utah St over (8) Villanova — 53%

Model validated on 4 past tournaments with a Brier score of 0.168 (lower is better; random guessing scores 0.25).

Full bracket, methodology, and code: [link to repo]

#MarchMadness #MachineLearning #NCAA #DataScience #SportsAnalytics

---

*Posting tips: Share Sunday evening or Monday morning before tournament starts. Update with quote comments as predictions hit.*
