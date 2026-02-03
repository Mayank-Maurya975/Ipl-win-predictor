import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
matches = pd.read_csv("data/matches.csv")
balls = pd.read_csv("data/deliveries.csv")

print("Matches:", len(matches))
print("Deliveries:", len(balls))

# =============================
# KEEP ONLY CHASE INNINGS
# =============================
balls_2nd = balls[balls["inning"] == 2].copy()

# =============================
# CUMULATIVE RUNS & WICKETS
# =============================
balls_2nd["cum_runs"] = balls_2nd.groupby("match_id")["total_runs"].cumsum()
balls_2nd["cum_wkts"] = balls_2nd.groupby("match_id")["is_wicket"].cumsum()

# =============================
# CORRECT BALL NUMBER
# over=1 ball=1 → ball 1
# over=1 ball=6 → ball 6
# over=2 ball=1 → ball 7
# =============================
balls_2nd["ball_number"] = (balls_2nd["over"] - 1) * 6 + balls_2nd["ball"]
balls_2nd["balls_left"] = 120 - balls_2nd["ball_number"]

# =============================
# TARGET = FIRST INNINGS RUNS + 1
# =============================
first_innings = balls[balls["inning"] == 1]

target_series = (
    first_innings
    .groupby("match_id")["total_runs"]
    .sum()
    + 1
)

balls_2nd["runs_target"] = balls_2nd["match_id"].map(target_series)

# drop if target missing
balls_2nd = balls_2nd.dropna(subset=["runs_target"])

# =============================
# DERIVED FEATURES
# =============================
balls_2nd["runs_left"] = balls_2nd["runs_target"] - balls_2nd["cum_runs"]
balls_2nd["wickets_left"] = 10 - balls_2nd["cum_wkts"]

# remove invalid states
balls_2nd = balls_2nd[
    (balls_2nd["balls_left"] > 0) &
    (balls_2nd["runs_left"] >= 0)
]

# current run rate
balls_2nd["overs_bowled"] = balls_2nd["ball_number"] / 6
balls_2nd["crr"] = balls_2nd["cum_runs"] / balls_2nd["overs_bowled"]
balls_2nd["crr"] = balls_2nd["crr"].replace([np.inf, -np.inf], 0).fillna(0)

# required run rate
balls_2nd["rrr"] = (balls_2nd["runs_left"] * 6) / balls_2nd["balls_left"]
balls_2nd["rrr"] = balls_2nd["rrr"].replace([np.inf, -np.inf], 99)

# =============================
# ADD MATCH META
# =============================
meta_cols = ["id", "winner", "venue", "city"]
meta = matches[meta_cols].rename(columns={"id": "match_id"})

balls_2nd = balls_2nd.merge(meta, on="match_id", how="left")

# =============================
# TARGET VARIABLE
# =============================
balls_2nd["batting_win"] = (
    balls_2nd["winner"] == balls_2nd["batting_team"]
).astype(int)

# =============================
# SNAPSHOT — ONE ROW PER OVER
# =============================
snapshots = (
    balls_2nd
    .sort_values(["match_id","ball_number"])
    .groupby(["match_id","over"])
    .last()
    .reset_index()
)

print("Snapshot rows:", len(snapshots))

# =============================
# SAVE TRAINING TABLE
# =============================
snapshots.to_csv("training_table.csv", index=False)

print("✅ training_table.csv saved")
