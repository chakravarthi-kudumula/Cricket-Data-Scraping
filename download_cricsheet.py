import requests
import zipfile
from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

url = "https://cricsheet.org/downloads/t20s_json.zip"
zip_path = RAW_DIR / "t20s_json.zip"

response = requests.get(url, timeout=60)
response.raise_for_status()

with open(zip_path, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(RAW_DIR / "t20s_json")

print("Downloaded and extracted Cricsheet T20 JSON data.")