import pandas as pd
from pathlib import Path

processed_dir = Path("data/processed")

batting = pd.read_csv(processed_dir / "batting_summary.csv")
bowling = pd.read_csv(processed_dir / "bowling_summary.csv")

# -----------------------------
# Batting aggregation
# -----------------------------
batting_summary = (
    batting.groupby(["batsman_name", "batting_team"])
    .agg(
        matches_batted=("match_id", "nunique"),
        innings=("match_id", "count"),
        total_runs=("runs", "sum"),
        total_balls=("balls", "sum"),
        total_4s=("4s", "sum"),
        total_6s=("6s", "sum"),
        outs=("out/not_out", lambda x: (x == "out").sum()),
        avg_batting_position=("batting_position", "mean")
    )
    .reset_index()
)

batting_summary["batting_average"] = batting_summary.apply(
    lambda row: round(row["total_runs"] / row["outs"], 2) if row["outs"] > 0 else row["total_runs"],
    axis=1
)

batting_summary["batting_strike_rate"] = batting_summary.apply(
    lambda row: round((row["total_runs"] / row["total_balls"]) * 100, 2) if row["total_balls"] > 0 else 0,
    axis=1
)

batting_summary["boundary_runs"] = (
    batting_summary["total_4s"] * 4 + batting_summary["total_6s"] * 6
)

batting_summary["boundary_percentage"] = batting_summary.apply(
    lambda row: round((row["boundary_runs"] / row["total_runs"]) * 100, 2) if row["total_runs"] > 0 else 0,
    axis=1
)

batting_summary = batting_summary.rename(
    columns={
        "batsman_name": "player_name",
        "batting_team": "team"
    }
)

# -----------------------------
# Bowling aggregation
# -----------------------------
bowling_summary = (
    bowling.groupby(["bowler_name", "bowling_team"])
    .agg(
        matches_bowled=("match_id", "nunique"),
        total_balls_bowled=("balls", "sum"),
        runs_conceded=("runs", "sum"),
        wickets=("wickets", "sum"),
        dot_balls=("dot_ball_percentage", "mean")
    )
    .reset_index()
)

bowling_summary["overs_bowled"] = round(bowling_summary["total_balls_bowled"] / 6, 2)

bowling_summary["economy"] = bowling_summary.apply(
    lambda row: round(row["runs_conceded"] / row["overs_bowled"], 2) if row["overs_bowled"] > 0 else 0,
    axis=1
)

bowling_summary["bowling_average"] = bowling_summary.apply(
    lambda row: round(row["runs_conceded"] / row["wickets"], 2) if row["wickets"] > 0 else None,
    axis=1
)

bowling_summary["bowling_strike_rate"] = bowling_summary.apply(
    lambda row: round(row["total_balls_bowled"] / row["wickets"], 2) if row["wickets"] > 0 else None,
    axis=1
)

bowling_summary = bowling_summary.rename(
    columns={
        "bowler_name": "player_name",
        "bowling_team": "team",
        "dot_balls": "avg_dot_ball_percentage"
    }
)

# -----------------------------
# Merge batting + bowling
# -----------------------------
player_summary = pd.merge(
    batting_summary,
    bowling_summary,
    on=["player_name", "team"],
    how="outer"
)

# Fill missing numeric values
numeric_cols = player_summary.select_dtypes(include=["number"]).columns
player_summary[numeric_cols] = player_summary[numeric_cols].fillna(0)

# -----------------------------
# Derive playing role
# -----------------------------
def assign_role(row):
    batting_sr = row.get("batting_strike_rate", 0)
    runs = row.get("total_runs", 0)
    wickets = row.get("wickets", 0)
    overs = row.get("overs_bowled", 0)
    avg_pos = row.get("avg_batting_position", 99)

    if runs >= 100 and wickets >= 5:
        return "All-rounder"
    elif wickets >= 7 and overs >= 8:
        return "Bowler"
    elif avg_pos <= 2 and runs >= 100:
        return "Opener"
    elif avg_pos <= 5 and runs >= 100:
        return "Top/Middle Order Batter"
    elif batting_sr >= 140 and runs >= 50:
        return "Finisher"
    elif runs >= 50:
        return "Batter"
    elif wickets > 0:
        return "Bowler"
    else:
        return "Player"

player_summary["playing_role"] = player_summary.apply(assign_role, axis=1)

# -----------------------------
# Same style as tutorial dim_players
# -----------------------------
player_summary["batting_style"] = ""
player_summary["bowling_style"] = ""
player_summary["description"] = ""
player_summary["image"] = ""

# Reorder columns
cols = [
    "player_name",
    "team",
    "playing_role",
    "batting_style",
    "bowling_style",
    "description",
    "image",
    "matches_batted",
    "innings",
    "total_runs",
    "batting_average",
    "batting_strike_rate",
    "boundary_percentage",
    "matches_bowled",
    "overs_bowled",
    "runs_conceded",
    "wickets",
    "economy",
    "bowling_average",
    "bowling_strike_rate",
    "avg_dot_ball_percentage"
]

player_summary = player_summary[cols]

player_summary = player_summary.sort_values(["team", "player_name"])

print(player_summary.shape)
print(player_summary.head(20))

player_summary.to_csv(processed_dir / "player_summary.csv", index=False)

print("Saved: data/processed/player_summary.csv")