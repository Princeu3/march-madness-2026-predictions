# Twitter/X Post — March Madness 2026

---

## Main Tweet

We built an ML model that predicts every possible matchup in the 2026 NCAA Tournament.

132,133 predictions. Here's what it sees:

Men's champion: Duke (18.7%)
Runner-up: Michigan (17.8%)
Championship game: Duke vs Michigan — 50.3% to 49.7%. A coin flip.

Women's champion: UConn (27.9%)
They went 34-0 and STILL only get a 28% chance. March is brutal.

Thread below.

---

## Reply 1 — Final Four

The model's Final Four path:

Semi 1 (East vs South): Duke over Florida — 63%
Semi 2 (West vs Midwest): Michigan over Arizona — 59%
Championship: Duke vs Michigan — dead even

Top 5 men's title odds:
Duke — 18.7%
Michigan — 17.8%
Arizona — 10.8%
Houston — 8.2%
Florida — 7.1%

---

## Reply 2 — How It Works

How: 3 gradient boosting models (LightGBM, XGBoost, CatBoost) trained on 20 years of NCAA data.

139 features per matchup:
- Elo power ratings
- Four Factors (shooting, turnovers, rebounding, FT rate)
- Strength of schedule
- 197 ranking systems aggregated
- Coaching tournament experience

They vote. We average.

---

## Reply 3 — Key Insight

The #1 predictor isn't seed. It's not ranking.

It's peak power rating — the best a team played all season.

Free throw rate (#7) ranks higher than 3PT% and rebounds as a predictor.

Getting to the line wins games in March.

---

## Reply 4 — Upset Watch

Upsets to watch Thursday:

Iowa over (8) Clemson — 57%
Utah St over (8) Villanova — 53%

No major Cinderella (12+ seed) predicted, but High Point has a 32.3% shot against Wisconsin.

---

## Reply 5 — Validation

Model accuracy on past tournaments:
2022: 0.189 Brier (St. Peter's run was tough)
2023: 0.194 (UConn dominance predicted)
2024: 0.161 (fewer upsets)
2025: 0.126 (best yet)

Avg: 0.168 (random = 0.25)

Full bracket + code: [link]

---

*Posting tips: Post ~2hrs before Thursday tip-off. Quote-tweet after predicted upsets hit to validate the model. Pin the main tweet during the tournament.*
