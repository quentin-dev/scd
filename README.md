# sunbro's Comics Downloader (sCD)

A tiny utility to automatically organize and download comics

## Prerequisites
- Python
- Poetry

## Quick start
1. Clone the repo and `cd` into it
2. Install dependencies: `poetry install`
3. Run: `poetry run scd`

## Generating a .exe file (Windows only)
1. Follow Quick Start steps 1 & 2
2. `poetry run pyinstaller -wF .\scd\main.py`
3. Run the .exe found in the `dist/` folder