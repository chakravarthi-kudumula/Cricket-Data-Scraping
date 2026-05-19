# Cricket Scraping

This project turns raw cricket match JSON into clean CSV files that are easier to use for analysis, dashboards, or player comparisons.

The data started as JSON endpoints found on a cricket data website. Instead of manually copying tables match by match, the project downloads the T20 match JSON bundle, reads each scorecard-style file, and builds structured summaries for matches, batting, bowling, and players.

At the moment, the main processed dataset is focused on the ICC Men's T20 World Cup 2022/23, with a saved output copy also available for Zimbabwe tour of Namibia 2023/24.

## What is in this folder

- `download_cricsheet.py` downloads the raw T20 JSON zip file and extracts it into `data/raw/t20s_json/`.
- `run_pipeline.py` scans the downloaded JSON files, lets you choose a tournament/season, writes that choice to `selected_series.json`, and runs the summary scripts.
- `create_match_summary.py` creates one row per match with teams, winner, date, venue, toss, and player of the match.
- `create_batting_summary.py` creates batter-level rows for each match, including runs, balls, boundaries, strike rate, batting position, and dismissal.
- `create_bowling_summary.py` creates bowler-level rows for each match, including overs, runs, wickets, economy, average, strike rate, and dot-ball percentage.
- `create_player_summary.py` combines batting and bowling numbers into one player-level file and adds a simple playing-role label.
- `find_worldcup_matches.py`, `filter_2022_worldcup.py`, and `inspect_json.py` are helper scripts used to understand and check the downloaded JSON.
- `scrape_test.py` is a Selenium test script for opening an ESPNcricinfo records page. It is separate from the main JSON pipeline.

## Data folders

```text
data/
  raw/
    t20s_json.zip
    t20s_json/
      5211 downloaded match JSON files
  processed/
    match_summary.csv
    batting_summary.csv
    bowling_summary.csv
    player_summary.csv
  outputs/
    icc_men_s_t20_world_cup_2022_23/
    zimbabwe_tour_of_namibia_2023_24/
```

`data/processed/` always holds the latest generated CSVs. `data/outputs/` keeps series-specific copies so an older run is not lost when the pipeline is run again.

## Clone from GitHub

The project is available on GitHub here: https://github.com/chakravarthi-kudumula/Cricket-Data-Scraping

To download it on a new machine, run:

```bash
git clone https://github.com/chakravarthi-kudumula/Cricket-Data-Scraping.git
cd Cricket-Data-Scraping
```

After cloning, follow the setup steps below to create the Python environment, install the requirements, download the raw JSON data if needed, and run the pipeline.

## How to run it

Create a Python environment first. This folder already has a local virtual environment named `cricket`, but if you are setting it up again from scratch, use:

```bash
python3 -m venv cricket
source cricket/bin/activate
pip install -r requirements.txt
```

If the existing environment is already there, just activate it and make sure the requirements are installed:

```bash
source cricket/bin/activate
pip install -r requirements.txt
```

If the raw JSON files are missing, download them:

```bash
python download_cricsheet.py
```

Then run the full pipeline:

```bash
python run_pipeline.py
```

The script prints the tournaments it finds in the JSON files. Pick the number for the tournament you want, and it will generate the four CSV files in `data/processed/`. It also saves a copy under `data/outputs/` using the selected series name.

The optional Selenium script can be run separately if you want to test opening the ESPNcricinfo records page:

```bash
python scrape_test.py
```

That browser test is not required for the JSON-to-CSV pipeline.

## Current selected series

The current `selected_series.json` file points to:

```json
{
  "event_name": "ICC Men's T20 World Cup",
  "season": "2022/23"
}
```

One thing to note: the individual summary scripts currently filter directly for the ICC Men's T20 World Cup 2022/23 in the code. `run_pipeline.py` records the selected series, but the summary scripts would need a small update if you want every script to automatically read from `selected_series.json`.

## Output files

- `match_summary.csv` is useful for match-level reporting.
- `batting_summary.csv` is useful for innings-by-innings batting analysis.
- `bowling_summary.csv` is useful for spell and wicket analysis.
- `player_summary.csv` is useful for comparing overall tournament performance by player.

The player summary also includes blank columns for `batting_style`, `bowling_style`, `description`, and `image`, which leaves room to enrich the dataset later for a dashboard or player profile page.

## Power BI analysis

This project is also extended with a Power BI analysis as an external report. The Python scripts prepare the CSV datasets, and the Power BI file uses those datasets to build an interactive cricket team-analysis dashboard.

The best way to go through the report is to open the `.pbix` file in Power BI Desktop. Once it is open, move through the report pages from left to right:

1. Start with the role-based pages such as `Power Hitters`, `Anchors`, `Finishers`, `All Rounders`, and `Specialist Fast Bowlers`.
2. Use the player tables and charts to compare players by strike rate, batting average, boundary percentage, economy, bowling strike rate, dot-ball percentage, and other role-specific metrics.
3. Click player names in the report to filter the visuals. The report is interactive, so selecting one player or multiple players changes the combined performance cards and comparison charts.
4. Go to the `Final 11` page to review the selected team. This page is meant to bring the role-wise selections together and show the overall team balance.
5. Use the batting and bowling performance pages at the end to check the selected team's combined strengths across batting average, strike rate, boundary percentage, economy, bowling average, bowling strike rate, and dot-ball percentage.

If Power BI asks for the data source location, point it to the CSV files in `data/processed/` or the relevant folder inside `data/outputs/`. The report is designed around the cleaned summary files created by this pipeline.

If someone cannot install Power BI Desktop or cannot open the `.pbix` file properly, use the attached PDF export as a reference version of the report. The PDF is not interactive, so it will not support clicking players or changing filters, but it still shows the main pages, selected visuals, and the general flow of the analysis. Treat it as a readable snapshot of the dashboard rather than a replacement for the live Power BI report.

## Notes

This is a practical data-prep project, not a polished package yet. The scripts are intentionally straightforward: download the JSON, inspect it, filter the matches, flatten the useful scorecard fields, and save CSVs that are easy to open in Excel, pandas, Power BI, Tableau, or any other analysis tool.
