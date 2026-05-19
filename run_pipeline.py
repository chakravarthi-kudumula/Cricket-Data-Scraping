import json
import subprocess
import sys
from pathlib import Path
from collections import Counter
import shutil
import re

RAW_DIR = Path("data/raw/t20s_json")
CONFIG_PATH = Path("selected_series.json")

def scan_series():
    series_counter = Counter()

    for file in RAW_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        info = data["info"]
        event_name = info.get("event", {}).get("name", "Unknown")
        season = str(info.get("season", "Unknown"))

        series_counter[(event_name, season)] += 1

    return series_counter

print("Scanning available tournaments...\n")

series_counter = scan_series()

series_list = [
    (event, season, count)
    for (event, season), count in series_counter.items()
    if count >= 5
]

series_list = sorted(series_list, key=lambda x: (x[0], x[1]))

print("Available series:\n")

for i, (event, season, count) in enumerate(series_list, start=1):
    print(f"{i}. {event} | {season} | {count} matches")

choice = int(input("\nEnter series number: "))

selected_event, selected_season, selected_count = series_list[choice - 1]

print("\nSelected:")
print(selected_event, "|", selected_season, "|", selected_count, "matches")

config = {
    "event_name": selected_event,
    "season": selected_season
}

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4)

scripts = [
    "create_match_summary.py",
    "create_batting_summary.py",
    "create_bowling_summary.py",
    "create_player_summary.py"
]

print("\nStarting cricket analytics data pipeline...\n")

for script in scripts:
    print(f"Running: {script}")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"\nPipeline failed at: {script}")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)
    print("-" * 60)

def clean_name(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

series_folder_name = f"{clean_name(selected_event)}_{clean_name(selected_season)}"
series_output_dir = Path("data/outputs") / series_folder_name
series_output_dir.mkdir(parents=True, exist_ok=True)

processed_dir = Path("data/processed")

for file_name in [
    "match_summary.csv",
    "batting_summary.csv",
    "bowling_summary.csv",
    "player_summary.csv"
]:
    src = processed_dir / file_name
    dst = series_output_dir / file_name

    if src.exists():
        shutil.copy2(src, dst)

print("\nPipeline completed successfully!")
print(f"Latest datasets saved in: data/processed/")
print(f"Series-specific copy saved in: {series_output_dir}")


print("\nPipeline completed successfully!")
print("Final datasets saved in: data/processed/")