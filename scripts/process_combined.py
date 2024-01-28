import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm

# Load the CSV data
csv_file_path = "output/combined_postcode_sales.csv"
print("Loading CSV data...")
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to a GeoDataFrame
print("Converting CSV data to GeoDataFrame...")
gdf_sales = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["long"], df["lat"]))
gdf_sales.crs = "EPSG:4326"

# Load the GeoJSON data
geojson_file_path = "data/OA.geojson"
print("Loading GeoJSON data...")
gdf_areas = gpd.read_file(geojson_file_path)

# Ensure gdf_sales is in the same CRS as gdf_areas
print("Ensuring CRS match...")
gdf_sales = gdf_sales.to_crs(gdf_areas.crs)

# Perform a spatial join between sales and areas
print("Performing spatial join...")
joined = gpd.sjoin(gdf_sales, gdf_areas, how="inner", op="within")

# Group by area and year, then calculate average price
print("Calculating average prices...")
avg_prices = (
    joined.groupby(["index_right", "year"])["price_normalized"].mean().reset_index()
)
avg_prices.rename(
    columns={"index_right": "fid", "price_normalized": "avg_price"}, inplace=True
)

# Update GeoJSON properties with average prices
print("Updating GeoJSON properties with average prices...")

# Update the properties with the new data
for fid, group in tqdm(avg_prices.groupby("fid"), desc="Updating Properties"):
    # Ensure there is only one matching feature
    if len(gdf_areas.loc[gdf_areas.index == fid]) == 1:
        # Populate the GeoDataFrame with the yearly average price data
        for _, row in group.iterrows():
            year_key = f"year_{int(row['year'])}"
            # Directly update the GeoDataFrame's column for the feature
            gdf_areas.loc[gdf_areas.index == fid, year_key] = round(row["avg_price"], 2)

# Save the modified GeoDataFrame to a new GeoJSON file
output_file_path = "output/housing_map.geojson"
print(f"Saving to {output_file_path}...")

# Drop the specified columns before saving
gdf_areas = gdf_areas.drop(columns=["fid", "OA21CD", "la23cd", "sg", "g", "subg"])

gdf_areas.to_file(output_file_path, driver="GeoJSON")
print("Done.")
