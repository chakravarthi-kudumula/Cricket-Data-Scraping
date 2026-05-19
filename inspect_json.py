import json
from pathlib import Path

json_folder = Path("data/raw/t20s_json")

json_files = list(json_folder.glob("*.json"))

print("NUMBER OF JSON FILES:", len(json_files))

first_file = json_files[0]
print("FIRST FILE:", first_file.name)

with open(first_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("\nTOP LEVEL KEYS:")
print(data.keys())

print("\nINFO KEYS:")
print(data["meta"].keys() if "meta" in data else "No meta")
print(data["info"].keys())

print("\nEVENT:")
print(data["info"].get("event"))

print("\nTEAMS:")
print(data["info"].get("teams"))

print("\nDATES:")
print(data["info"].get("dates"))

print("\nINNINGS TYPE:")
print(type(data.get("innings")))

print("\nFIRST INNINGS PREVIEW:")
print(data.get("innings", [])[:1])