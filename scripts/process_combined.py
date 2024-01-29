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
geojson_file_path = "data/OA.geojson"
print("Loading GeoJSON data...")
with open(geojson_file_path, "r") as file:
    geojson_data = json.load(file)
gdf_areas = gpd.GeoDataFrame.from_features(geojson_data)
gdf_areas.crs = "EPSG:4326"

# Ensure CRS match and perform spatial join
print("Performing spatial join...")
gdf_sales = gdf_sales.to_crs(gdf_areas.crs)
joined = gpd.sjoin(gdf_sales, gdf_areas, how="inner", op="within")

# Calculate average prices
print("Calculating average prices...")
avg_prices = (
    joined.groupby(["index_right", "year"])["price_normalized"].mean().reset_index()
)
avg_prices.rename(
    columns={"index_right": "fid", "price_normalized": "avg_price"}, inplace=True
)

# Update GeoJSON properties with average prices
print("Updating GeoJSON properties...")
for feature in tqdm(geojson_data["features"], desc="Updating Properties"):
    fid = feature["properties"]["fid"]
    if fid in avg_prices["fid"].values:
        for _, row in avg_prices[avg_prices["fid"] == fid].iterrows():
            year_key = f"year_{int(row['year'])}"
            feature["properties"][year_key] = round(row["avg_price"], 2)

# Drop the specified columns before saving
print("Dropping specified columns...")
gdf_areas = gdf_areas.drop(columns=["fid", "OA21CD", "la23cd", "sg", "g", "subg"])

output_file_path = "output/housing_map_rounded.geojson"
with open(output_file_path, "w") as file:
    json.dump(geojson_data, file)

print("Done.")
