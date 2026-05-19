import json
from pathlib import Path

json_folder = Path("data/raw/t20s_json")

matches = []

for file in json_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data["info"]
    event_name = info.get("event", {}).get("name")
    season = str(info.get("season"))
    dates = info.get("dates", [])

    if event_name == "ICC Men's T20 World Cup" and season == "2022/23":
        matches.append({
            "file": file.name,
            "date": dates[0] if dates else None,
            "teams": " vs ".join(info.get("teams", [])),
            "venue": info.get("venue"),
            "city": info.get("city"),
            "winner": info.get("outcome", {}).get("winner")
        })

print("MATCHES FOUND:", len(matches))

for m in matches[:10]:
    print(m)