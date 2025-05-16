import pandas as pd
from gpx_parser import extract_gpx_data  #Importing the gpx parser
import webbrowser
#Future Expansions
#import folium as fo 
#import matplotlib.pyplot as plt
#from lxml import etree



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
# print(df)

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


#Location in Google Earth URL(Off trail):
url = f"https://earth.google.com/web/@{lat},{lon},1500a,2000d,35y,0h,0t,0r"
print(f"This is where you hit the max speed of {max_speed:.2f} mph at {timestamp}: ")
print(f"Droppin:", url)
webbrowser.open(url)

#Pinpoint
...#future Enhancement

# df.to_csv("output.csv", index=False) #CSV Extract


