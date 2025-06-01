import pandas as pd
from gpx_parser import extract_gpx_data  #Importing the gpx parser
import webbrowser
import math
#Future Expansions
#import folium as fo 
#import matplotlib.pyplot as plt
#from lxml import etree

def main():
    data = datacompiler()
    #Refined Data(Df for processing)
    df = pd.DataFrame(data)
    print("Data from datacompiler (first 3 rows):", data[:3])
    df = pd.DataFrame(data)
    print("Columns in df:", df.columns.tolist())
    print(df.head())



    print(df)
    #Data Cleanup [Spped("" = 0.0) and Azimuth ("" = 0.0 {Default {North}))]
    # Ensure Speed is numeric and not None
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce').fillna(0)
    df['Direction'] = pd.to_numeric(df['Direction'], errors='coerce').fillna(0.0)

    # Max speed per file
    max_speeds = df.groupby('Filename')['Speed'].max().reset_index()
    print("\nMax speed for each file:")
    print(max_speeds)

    # Pinpoint Max Speed overall
    max_speed = df['Speed'].max()
    if max_speed == 0:
        print("No valid speed data found.")
        return
    max_speed_row = df.loc[df['Speed'].idxmax()]  # Get row with max speed
    lat, lon = max_speed_row['Latitude'], max_speed_row['Longitude']
    timestamp = max_speed_row['Timestamp']
    print("\n📍 Row with Max Speed (overall):")
    print(max_speed_row.to_frame().T)  # display as a 1-row DataFrame


    # #Location in Google Earth URL(Off trail):
    # url = f"https://earth.google.com/web/@{lat},{lon},1500a,2000d,35y,0h,0t,0r"
    # print(f"This is where you hit the max speed of {max_speed:.2f} mph at {timestamp}: ")
    # print(f"Droppin:", url)
    # webbrowser.open(url)

    #Future Enhancement
        #Pinpoint
        # df.to_csv("output.csv", index=False) #CSV Extract


def datacompiler():
    directory = "data"

    try:
        gpx_data = extract_gpx_data(directory)
        if gpx_data is None:
            print("extract_gpx_data returned None")
            return []
    except Exception as e:
        print(f"Error extracting GPX data: {e}")
        return []
    
    all_data = []
    
    for filename, data in gpx_data.items():
        # Calculate speeds from track points only
        speeds = calculate_speed(data.get('track_points', []))

        max_len = max(len(data.get('timestamps', [])),
                      len(data.get('elevations', [])),
                      len(data.get('track_points', [])),
                      len(speeds),
                      len(data.get('azimuth', [])))

        for i in range(max_len):            
            timestamp = data['timestamps'][i] if i < len(data['timestamps']) else None
            elevation = data['elevations'][i] if i < len(data['elevations']) else None
            lat_lon = data['track_points'][i] if i < len(data['track_points']) else None

            lat = lat_lon.get('lat') if lat_lon else None
            lon = lat_lon.get('lon') if lat_lon else None
            
            # Ensure speed is included in the data
            speed = speeds[i] if i < len(speeds) else None
            if speed is None:
                speed = 0  # Default to 0 if speed is missing

            # Safe access direction (azimuth)
            direction = None
            if i < len(data.get('azimuth', [])):
                az_dict = data['azimuth'][i]
                if isinstance(az_dict, dict):
                    direction = az_dict.get('azimuth')

            all_data.append({
                'Filename': filename,
                'Timestamp': timestamp,
                'Elevation': elevation,
                'Latitude': lat,
                'Longitude': lon,
                'Speed': speed,  # Ensure Speed is added
                'Direction': direction
            })
    
    print(f"Total data points compiled: {len(all_data)}")
    if all_data:
        print(f"Sample data point: {all_data[0]}")
    return all_data


def calculate_speed(track_points, time_interval=3):
    speeds = [0]  # speed for first point
    if not track_points or len(track_points) < 2:
        return speeds  # just [0] or empty list if no points

    for i in range(1, len(track_points)):
        prev = track_points[i - 1]
        curr = track_points[i]
        if not prev or not curr:
            speeds.append(0)
            continue
        try:
            dist = haversine_distance(prev['lat'], prev['lon'], curr['lat'], curr['lon'])
        except KeyError as e:
            print(f"Missing key in track point: {e}")
            speeds.append(0)
            continue
        speed = dist / time_interval
        speeds.append(speed)
    return speeds

def haversine_distance(lat1, lon1, lat2, lon2):
    # Ensure all coordinates are floats
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except (TypeError, ValueError):
        return 0  # Return 0 distance if conversion fails
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


if __name__ == "__main__":
    main()