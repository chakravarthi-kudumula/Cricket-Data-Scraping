import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

json_folder = Path("data/raw/t20s_json")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

rows = []

def is_legal_ball(delivery):
    extras = delivery.get("extras", {})
    return "wides" not in extras and "noballs" not in extras

for file in json_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data["info"]
    event_name = info.get("event", {}).get("name")
    season = str(info.get("season"))

    if event_name != "ICC Men's T20 World Cup" or season != "2022/23":
        continue

    match_id = file.stem
    teams = info.get("teams", [])

    for innings in data.get("innings", []):
        batting_team = innings["team"]
        bowling_team = [t for t in teams if t != batting_team][0]

        bowling = defaultdict(lambda: {
            "balls": 0,
            "runs": 0,
            "wickets": 0,
            "dot_balls": 0
        })

        for over in innings.get("overs", []):
            for delivery in over.get("deliveries", []):

                bowler = delivery["bowler"]

                total_runs = delivery["runs"]["total"]

                bowling[bowler]["runs"] += total_runs

                if is_legal_ball(delivery):
                    bowling[bowler]["balls"] += 1

                if total_runs == 0:
                    bowling[bowler]["dot_balls"] += 1

                for wicket in delivery.get("wickets", []):
                    kind = wicket.get("kind", "")

                    if kind not in ["run out", "retired hurt", "obstructing the field"]:
                        bowling[bowler]["wickets"] += 1

        for bowler, stats in bowling.items():

            balls = stats["balls"]
            overs = round(balls / 6, 1)

            economy = round((stats["runs"] / overs), 2) if overs > 0 else 0

            bowling_avg = (
                round(stats["runs"] / stats["wickets"], 2)
                if stats["wickets"] > 0 else None
            )

            strike_rate = (
                round(stats["balls"] / stats["wickets"], 2)
                if stats["wickets"] > 0 else None
            )

            dot_ball_pct = round(
                (stats["dot_balls"] / balls) * 100, 2
            ) if balls > 0 else 0

            rows.append({
                "match_id": match_id,
                "match": f"{teams[0]} vs {teams[1]}",
                "bowling_team": bowling_team,
                "batting_team": batting_team,
                "bowler_name": bowler,
                "overs": overs,
                "balls": balls,
                "runs": stats["runs"],
                "wickets": stats["wickets"],
                "economy": economy,
                "bowling_average": bowling_avg,
                "bowling_strike_rate": strike_rate,
                "dot_ball_percentage": dot_ball_pct
            })

df = pd.DataFrame(rows)

print(df.shape)
print(df.head(20))

df.to_csv(output_folder / "bowling_summary.csv", index=False)

print("Saved: data/processed/bowling_summary.csv")