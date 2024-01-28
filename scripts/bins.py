import pandas as pd
import numpy as np
import json

# Load the data
df = pd.read_csv("output/combined_postcode_sales.csv")

# Group by year and calculate the median and percentiles
grouped = df.groupby("year")["price_normalized"].agg(
    median="median",
    bins=lambda x: [round(p, 2) for p in np.percentile(x, np.linspace(0, 100, 11))],
)

# Round the median to 2 decimal places
grouped["median"] = grouped["median"].round(2)

# Convert the DataFrame to a dictionary
data_dict = grouped.to_dict("index")

# Save the dictionary to a JSON file
with open("output/bins.json", "w") as f:
    json.dump(data_dict, f)
