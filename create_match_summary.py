import json
import pandas as pd
from pathlib import Path

json_folder = Path("data/raw/t20s_json")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

rows = []

for file in json_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data["info"]
    event_name = info.get("event", {}).get("name")
    season = str(info.get("season"))

    if event_name == "ICC Men's T20 World Cup" and season == "2022/23":
        teams = info.get("teams", [])
        outcome = info.get("outcome", {})

        rows.append({
            "match_id": file.stem,
            "team1": teams[0] if len(teams) > 0 else None,
            "team2": teams[1] if len(teams) > 1 else None,
            "winner": outcome.get("winner"),
            "result": outcome.get("result"),
            "date": info.get("dates", [None])[0],
            "venue": info.get("venue"),
            "city": info.get("city"),
            "toss_winner": info.get("toss", {}).get("winner"),
            "toss_decision": info.get("toss", {}).get("decision"),
            "player_of_match": ", ".join(info.get("player_of_match", []))
        })

df = pd.DataFrame(rows)
df = df.sort_values("date")

print(df.shape)
print(df.head())

df.to_csv(output_folder / "match_summary.csv", index=False)
print("Saved: data/processed/match_summary.csv")