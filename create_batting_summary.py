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
    return "wides" not in extras

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

        batting = defaultdict(lambda: {
            "runs": 0,
            "balls": 0,
            "4s": 0,
            "6s": 0,
            "dismissal": ""
        })

        batting_order = []

        for over in innings.get("overs", []):
            for delivery in over.get("deliveries", []):
                batter = delivery["batter"]

                if batter not in batting_order:
                    batting_order.append(batter)

                batter_runs = delivery["runs"]["batter"]
                batting[batter]["runs"] += batter_runs

                if is_legal_ball(delivery):
                    batting[batter]["balls"] += 1

                if batter_runs == 4:
                    batting[batter]["4s"] += 1
                elif batter_runs == 6:
                    batting[batter]["6s"] += 1

                for wicket in delivery.get("wickets", []):
                    if wicket.get("player_out") == batter:
                        batting[batter]["dismissal"] = wicket.get("kind", "")

        for pos, batter in enumerate(batting_order, start=1):
            runs = batting[batter]["runs"]
            balls = batting[batter]["balls"]
            strike_rate = round((runs / balls) * 100, 2) if balls > 0 else 0

            rows.append({
                "match_id": match_id,
                "match": f"{teams[0]} vs {teams[1]}",
                "batting_team": batting_team,
                "bowling_team": bowling_team,
                "batsman_name": batter,
                "batting_position": pos,
                "runs": runs,
                "balls": balls,
                "4s": batting[batter]["4s"],
                "6s": batting[batter]["6s"],
                "strike_rate": strike_rate,
                "out/not_out": "out" if batting[batter]["dismissal"] else "not out",
                "dismissal": batting[batter]["dismissal"]
            })

df = pd.DataFrame(rows)
df = df.sort_values(["match_id", "batting_team", "batting_position"])

print(df.shape)
print(df.head(20))

df.to_csv(output_folder / "batting_summary.csv", index=False)
print("Saved: data/processed/batting_summary.csv")