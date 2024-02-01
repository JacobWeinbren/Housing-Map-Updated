import pandas as pd
import geopandas as gpd
import json
from tqdm import tqdm

# Load CSV data and convert to GeoDataFrame
csv_file_path = "output/combined_postcode_sales.csv"
print("Loading CSV data...")
df = pd.read_csv(csv_file_path)
gdf_sales = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["long"], df["lat"]), crs="EPSG:4326"
)

# Load GeoJSON data and convert to GeoDataFrame
geojson_file_path = "data/MSOA.geojson"
print("Loading GeoJSON data...")
with open(geojson_file_path) as file:
    gdf_areas = gpd.GeoDataFrame.from_features(
        json.load(file), crs="EPSG:27700"
    ).to_crs("EPSG:4326")

# Perform spatial join
print("Performing spatial join...")
joined = gpd.sjoin(gdf_sales, gdf_areas, how="inner", op="within")

# Calculate and map average prices
print("Calculating and mapping average prices...")
avg_prices = (
    joined.groupby(["index_right", "year"])["price_normalized"].median().reset_index()
)
avg_prices.columns = ["FID", "year", "avg_price"]

# Iterate over features and update properties
for feature in tqdm(
    gdf_areas.iterrows(), desc="Updating Properties", total=len(gdf_areas)
):
    fid = feature[1]["FID"]
    feature_years_prices = avg_prices[avg_prices["FID"] == fid]
    for _, row in feature_years_prices.iterrows():
        gdf_areas.loc[gdf_areas["FID"] == fid, f"year_{int(row['year'])}"] = round(
            row["avg_price"], 2
        )

# Save the updated GeoDataFrame to a GeoJSON file
output_file_path = "output/housing_map.geojson"
print(f"Saving updated GeoJSON to {output_file_path}...")
gdf_areas.to_file(output_file_path, driver="GeoJSON")

print("Done.")
