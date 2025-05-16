# import re
import pandas as pd
# import os

from gpx_parser import extract_gpx_data  #Importing the gpx parser

# Gpx_Files directory
directory = "data"

# Get the extracted data from the GPX files
gpx_data = extract_gpx_data(directory)

#Placeholder for all the data
all_data = []

#Looping through each file
for filename, data in gpx_data.items():
    for i in range(len(data['timestamps'])):
        # Extract the information for each trackpoint
        timestamp = data['timestamps'][i] if i < len(data['timestamps']) else None
        elevation = data['elevations'][i] if i < len(data['elevations']) else None
        lat_lon = data['track_points'][i] if i < len(data['track_points']) else None
        lat = lat_lon['lat'] if lat_lon else None
        lon = lat_lon['lon'] if lat_lon else None
        
        # Correct handling of speed and azimuth from xml (Direction)
        speed = data['gps_data'][i]['speed'] if i < len(data['gps_data']) and 'speed' in data['gps_data'][i] else None
        direction = data['gps_data'][i]['azimuth'] if i < len(data['gps_data']) and 'azimuth' in data['gps_data'][i] else None

        # Compile Data
        all_data.append({
            'Filename': filename,
            'Timestamp': timestamp,
            'Elevation': elevation,
            'Latitude': lat,
            'Longitude': lon,
            'Speed': speed,
            'Direction': direction  # Use 'azimuth' here as 'Direction'
        })

# Convert to DataFrame
df = pd.DataFrame(all_data)

#Data Cleanup [speed might not be available in some GPX files]
df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce').fillna(0)
df['Direction'] = df['Direction'].fillna(pd.NA)

print(df)
df.to_csv("output.csv", index=False) #CSV Extract

max_speed = df['Speed'].max()
print("Highest speed:", max_speed)