import re 
import pandas as pd
import glob

gpx_files = glob.glob("data/*.gpx")

for file_path in gpx_files:
    with open(file_path, "r", encoding="utf-8") as f:
        gpx_data = f.read()

wpt_pattern = re.compile(r'<wpt lat="([^"]+)" lon="([^"]+)">(.*?)</wpt>', re.DOTALL)
wpts = wpt_pattern.findall(gpx_data)

data = []
for lat, lon, content in wpts:
    ele = re.search(r"<ele>(.*?)</ele>", content)
    time = re.search(r"<time>(.*?)</time>", content)
    name = re.search(r"<name>(.*?)</name>", content)
    typ = re.search(r"<type><!\[CDATA\[(.*?)\]\]></type>", content)

    data.append({
        "lat": float(lat),
        "lon": float(lon),
        "ele": float(ele.group(1)) if ele else None,
        "time": time.group(1) if time else None,
        "name": name.group(1) if name else None,
        "type": typ.group(1) if typ else None
    })

#Dataframing
df = pd.DataFrame(data)

#Analysis
print("First few rows: ", df.head)
print("Last few records:", df.tail)