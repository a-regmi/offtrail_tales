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


def calculate_speed(track_points):
    speeds = [0]  # speed for first point
    if not track_points or len(track_points) < 2:
        return speeds

    # Debug: print first few track points
    print("First 3 track points for speed calculation:")
    for pt in track_points[:3]:
        print(pt)

    for i in range(1, len(track_points)):
        prev = track_points[i - 1]
        curr = track_points[i]
        if not prev or not curr:
            speeds.append(0)
            continue
        try:
            dist = haversine_distance(prev['lat'], prev['lon'], curr['lat'], curr['lon'])
            
            # Filter out unrealistic distances (GPS jitter)
            # 0.0006 miles ≈ 1 meter - ignore very tiny movements that might be GPS noise
            if dist < 0.0006:
                speeds.append(speeds[-1])  # Keep previous speed
                continue

            # Parse timestamps if available
            t1 = prev.get('time')
            t2 = curr.get('time')
            if t1 and t2:
                from dateutil import parser
                try:
                    dt1 = parser.parse(t1)
                    dt2 = parser.parse(t2)
                    time_delta = (dt2 - dt1).total_seconds()
                    
                    # Skip if time difference is too small or too large
                    if time_delta < 1 or time_delta > 30:  # Skip intervals <1s or >30s
                        speeds.append(speeds[-1])  # Keep previous speed
                        continue
                        
                    # Calculate speed in mph
                    speed = (dist / time_delta) * 3600
                    
                    # Apply activity-based speed limits
                    # Skiing: max ~60 mph
                    # Hiking: max ~15 mph
                    # Biking: max ~45 mph
                    MAX_SPEED = 60  # mph, absolute maximum
                    if speed > MAX_SPEED:
                        speed = speeds[-1]  # Keep previous speed if unrealistic
                    
                    print(f"dist={dist:.4f}mi, time_delta={time_delta:.2f}s, speed={speed:.2f} mph, t1={t1}, t2={t2}")
                except Exception as ex:
                    print(f"Timestamp parse error: {ex}")
                    speed = 0
            else:
                speed = 0

            # Debug output
            print(f"DEBUG: i={i}, prev=({prev['lat']}, {prev['lon']}, {prev.get('time')}), curr=({curr['lat']}, {curr['lon']}, {curr.get('time')}), dist={dist:.4f}mi, time_delta={time_delta:.2f}s, speed={speed:.2f} mph")

        except Exception as e:
            print(f"Error calculating speed: {e}")
            speed = speeds[-1]  # Keep previous speed on error
                
        # Check for out-of-order timestamps
        if t1 and t2 and dt2 < dt1:
            print(f"WARNING: Out-of-order timestamps at i={i}: t1={t1}, t2={t2}")

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
    R = 3958.8  # Earth radius in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Returns distance in miles


if __name__ == "__main__":
    main()