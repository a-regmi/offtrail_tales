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
    print(df)
    #Data Cleanup [Spped("" = 0.0) and Azimuth ("" = 0.0 {Default {North}))]
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce').fillna(0)
    df['Direction'] = pd.to_numeric(df['Direction'], errors='coerce').fillna(0.0) 

    #Pinpooint Max Speed
    max_speed = df['Speed'].max()
    max_speed_row = df.loc[df['Speed'].idxmax()]  # Get row with max speed
    lat, lon = max_speed_row['Latitude'], max_speed_row['Longitude']
    timestamp = max_speed_row['Timestamp']
    print("📍 Row with Max Speed:")
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

    # Get the extracted data from the GPX files
    gpx_data = extract_gpx_data(directory)

    
    all_data = []
    
    for filename, data in gpx_data.items():
        # Calculate speeds from track points only
        speeds = calculate_speed(data['track_points'])
        
        for i in range(len(data['timestamps'])):
            timestamp = data['timestamps'][i] if i < len(data['timestamps']) else None
            elevation = data['elevations'][i] if i < len(data['elevations']) else None
            lat_lon = data['track_points'][i] if i < len(data['track_points']) else None
            lat = lat_lon['lat'] if lat_lon else None
            lon = lat_lon['lon'] if lat_lon else None
            
            # Always use calculated speed
            speed = speeds[i] if i < len(speeds) else None
            
            # Direction (azimuth) still from gps_data if present
            direction = data['gps_data'][i]['azimuth'] if i < len(data['gps_data']) and 'azimuth' in data['gps_data'][i] else None
            
            all_data.append({
                'Filename': filename,
                'Timestamp': timestamp,
                'Elevation': elevation,
                'Latitude': lat,
                'Longitude': lon,
                'Speed': speed,
                'Direction': direction
            })
    
    return all_data

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_speed(track_points, time_interval=3):
    speeds = [0]  # Speed for first point is 0 (no previous point)
    
    for i in range(1, len(track_points)):
        prev = track_points[i - 1]
        curr = track_points[i]
        dist = haversine_distance(prev['lat'], prev['lon'], curr['lat'], curr['lon'])
        speed = dist / time_interval
        speeds.append(speed)
    return speeds


if __name__ == "__main__":
    main()