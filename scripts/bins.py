import pandas as pd
import numpy as np
import json

# Load the data
df = pd.read_csv("output/combined_postcode_sales.csv")

# Ensure price_normalized is within 0-100
df["price_normalized"] = df["price_normalized"].clip(lower=0, upper=100)

# Define bins edges
bins_edges = np.arange(0, 51, 2)  # 0, 10, 20, ..., 100


# Group by year and calculate the histogram for each group
def calculate_histogram(x):
    hist, _ = np.histogram(x, bins=bins_edges)
    return hist.tolist()


grouped = df.groupby("year")["price_normalized"].agg(
    median="median", histogram=calculate_histogram
)

# Round the median to 2 decimal places
grouped["median"] = grouped["median"].round(2)

# Convert the DataFrame to a dictionary
data_dict = grouped.to_dict("index")

# Save the dictionary to a JSON file
with open("output/bins.json", "w") as f:
    json.dump(data_dict, f)
