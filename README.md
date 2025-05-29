# offtrail_tales

## About the Project
Analyze GPX data to track and extract meaningful insights from personal trail records—whether skiing, mountain biking, running, hiking, or logging laps and runs. Designed to analyze performance across diverse activities, uncover patterns in terrain usage, track progress over time, and deliver a deeper understanding of outdoor experiences through detailed metrics and visualizations.

**Note:**  
- **Speed Data:** Hiking GPX data might not have speed information (e.g., GPX data from AllTrails often lacks speed data).  
- GPX data from Slopes app provides speed information for positional instances.

- **Direction:** Some GPX files may not include direction (azimuth) values. In such cases, azimuth values defaulted to 0.0 (facing North).


## Features
- Calculate Speed using positional trail records.
- Support for multiple activity types (skiing, biking, running, hiking).  
- Handle incomplete data gracefully (e.g., missing speed or direction).  
- Visualize trail data with detailed metrics (future work / optional).

## Data and Files 
- Accepts GPS data in GPX file format (`.gpx`).  
- Compatible with files from popular apps like AllTrails and Slopes, and OsmAndMaps

## Tech Stack
- Python  
- Python Libraries(Pandas, glob, Webbrowser, BeautifulSoup)

## License
This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for full details.

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