# offtrail_tales

## About the Project
Analyze GPX data to track and extract meaningful insights from personal trail records—whether skiing, mountain biking, running, hiking, or logging laps and runs. Designed to analyze performance across diverse activities, uncover patterns in terrain usage, track progress over time, and deliver a deeper understanding of outdoor experiences through detailed metrics and visualizations.

> **Note:**  
> - Speed data from hiking GPX files (e.g., AllTrails) may be missing.  
> - GPX files from Slopes provide speed data per location point.  
> - If direction (azimuth) is missing, a default direction of **0°(N)** North is assumed.

## Features
- Calculate Speed using positional trail records.
- Support for multiple activity types (skiing, biking, running, hiking).  
- Handle incomplete data gracefully (e.g., missing speed or direction).  
- Visualize trail data with detailed metrics (future work / optional).

## Data and Files 
- Accepts GPS data in GPX file format (`.gpx`).  
- Compatible with files from popular apps like AllTrails and Slopes, and OsmAndMaps.
**Note:**
- **GPX file:** `.gpx` would need a manual extract from apps listed above

## Tech Stack
- Python  
- Python Libraries(Pandas, glob, Webbrowser, BeautifulSoup)

## License
This project is licensed under the MIT License. Full Details: [LICENSE](./LICENSE)

## Getting Started
1. Obtain GPX files from your device or favorite app.  
2. Follow the installation instructions below to set up the environment.  
3. Run the analysis script with your GPX data.

## Screenshots
...

## Installation
_Example:_

```bash
# Clone the repo (venv Recommended)
git clone https://github.com/a-regmi/offtrail_tales.git

# Install dependencies
pip install -r requirements.txt