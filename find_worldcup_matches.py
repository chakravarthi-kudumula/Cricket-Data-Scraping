import json
from pathlib import Path
from collections import Counter

json_folder = Path("data/raw/t20s_json")

events = Counter()

for file in json_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    event = data["info"].get("event", {})
    event_name = event.get("name", "Unknown")

    events[event_name] += 1

print("TOP EVENTS:")
for event, count in events.most_common(50):
    print(count, "->", event)