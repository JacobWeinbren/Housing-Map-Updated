import pandas as pd
import geopandas as gpd
import json
from tqdm import tqdm
import os

# Load and process CSV data
csv_file_path = "output/combined_postcode_sales.csv"
output_dir = "output/years"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Loading and converting CSV data...")
df = pd.read_csv(csv_file_path)
gdf_sales = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["long"], df["lat"]))
gdf_sales.crs = "EPSG:4326"

# Group by year and process each group
for year, group in tqdm(gdf_sales.groupby("year")):
    # Create GeoJSON features for each row in the group
    features = []
    for _, row in group.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [row["long"], row["lat"]]},
            "properties": {"price": row["price_normalized"]},
        }
        features.append(feature)

    # Create the GeoJSON object
    geojson = {"type": "FeatureCollection", "features": features}

    # Convert the GeoJSON object to a string
    geojson_str = json.dumps(geojson)

    # Save the GeoJSON string to a file
    with open(f"{output_dir}/{year}.geojson", "w") as f:
        f.write(geojson_str)
