import pandas as pd
import geopandas as gpd
import json
from tqdm import tqdm

# Load and process CSV data
csv_file_path = "output/combined_postcode_sales.csv"
print("Loading and converting CSV data...")
df = pd.read_csv(csv_file_path)
gdf_sales = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["long"], df["lat"]))
gdf_sales.crs = "EPSG:4326"

# Load GeoJSON data
geojson_file_path = "data/MSOA.geojson"
print("Loading GeoJSON data...")
with open(geojson_file_path, "r") as file:
    geojson_data = json.load(file)
gdf_areas = gpd.GeoDataFrame.from_features(geojson_data)
gdf_areas.crs = "EPSG:27700"
gdf_areas = gdf_areas.to_crs("EPSG:4326")

# Ensure CRS match and perform spatial join
print("Performing spatial join...")
joined = gpd.sjoin(gdf_sales, gdf_areas, how="inner", op="within")

# Calculate average prices
print("Calculating average prices...")
avg_prices = (
    joined.groupby(["index_right", "year"])["price_normalized"].median().reset_index()
)
avg_prices.rename(
    columns={"index_right": "FID", "price_normalized": "avg_price"}, inplace=True
)

# Update GeoJSON properties with average prices
print("Updating GeoJSON properties...")
for feature in tqdm(geojson_data["features"], desc="Updating Properties"):
    fid = feature["properties"]["FID"]
    if fid in avg_prices["FID"].values:
        for _, row in avg_prices[avg_prices["FID"] == fid].iterrows():
            year_key = f"year_{int(row['year'])}"
            feature["properties"][year_key] = round(row["avg_price"], 2)

# Convert updated GeoJSON data to a GeoDataFrame to ensure correct CRS
gdf_updated = gpd.GeoDataFrame.from_features(geojson_data)
gdf_updated.crs = "EPSG:27700"
gdf_updated = gdf_updated.to_crs("EPSG:4326")

# Save the updated GeoDataFrame to a GeoJSON file
output_file_path = "output/housing_map.geojson"
print(f"Saving updated GeoJSON to {output_file_path}...")
gdf_updated.to_file(output_file_path, driver="GeoJSON")

print("Done.")
