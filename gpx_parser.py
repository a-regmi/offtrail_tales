from bs4 import BeautifulSoup
import os
import glob

def extract_gpx_data(directory):
    gpx_data = {}  # Dictionary to hold all files' data

    # Using glob lib to get all .gpx files in the data directory
    gpx_files = glob.glob(os.path.join(directory, '*.gpx'))

    for filename in gpx_files:
        print(f"\nProcessing: {filename}")

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'lxml-xml')  #XML parsing

                timestamps = []
                elevations = []
                track_points = []
                gps_data = []

                for trkpt in soup.find_all('trkpt'):
                    lat = trkpt.get('lat')
                    lon = trkpt.get('lon')
                    time = trkpt.find('time')
                    ele = trkpt.find('ele')

                    # Defaults
                    speed = None
                    azimuth = None

                    # Getting speed and azimuth<extensions><gte:gps ... />
                    extensions = trkpt.find('extensions')
                    if extensions:
                        gps_tag = extensions.find('gte:gps')
                        if gps_tag:
                            speed = gps_tag.get('speed')
                            azimuth = gps_tag.get('azimuth')

                    # Collect data
                    timestamps.append(time.text.strip() if time else None)
                    elevations.append(ele.text.strip() if ele else None)
                    track_points.append({'lat': lat, 'lon': lon})
                    gps_data.append({
                        'speed': speed,
                        'azimuth': azimuth
                    })

                gpx_data[os.path.basename(filename)] = {
                    'timestamps': timestamps,
                    'elevations': elevations,
                    'track_points': track_points,
                    'gps_data': gps_data
                }

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return gpx_data
