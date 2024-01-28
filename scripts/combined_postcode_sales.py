import csv
from datetime import datetime
from tqdm import tqdm


# Helper function to read incomes and create a mapping from year to salary
def read_incomes(file_path):
    year_to_salary = {}
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader, desc="Reading incomes"):
            year_to_salary[int(row["Year"])] = float(row["Salary"])
    return year_to_salary


# Helper function to create a mapping from postcode to latitude and longitude
def read_postcode_mapping(file_path):
    postcode_to_lat_long = {}
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader, desc="Mapping postcodes"):
            postcode = row["pcds"].replace(" ", "").upper()
            postcode_to_lat_long[postcode] = (row["lat"], row["long"])
    return postcode_to_lat_long


# Helper function to process housing data
def process_housing_data(file_path, postcode_to_lat_long, year_to_salary):
    combined_data = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in tqdm(reader, desc="Processing housing data"):
            _, price, date_str, postcode = row[:4]
            year = datetime.strptime(date_str, "%Y-%m-%d %H:%M").year
            normalized_postcode = postcode.replace(" ", "").upper()
            lat_long = postcode_to_lat_long.get(normalized_postcode, ("", ""))
            if lat_long != ("", "") and year in year_to_salary:
                price_normalized = float(price) / year_to_salary[year]
                combined_data.append(
                    [year, postcode, price_normalized] + list(lat_long)
                )
    return combined_data


# Helper function to write combined data to a CSV file
def write_combined_data(file_path, combined_data):
    with open(file_path, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["year", "postcode", "price_normalized", "lat", "long"])
        for row in tqdm(combined_data, desc="Writing output"):
            writer.writerow(row)


# Main script execution
if __name__ == "__main__":
    year_to_salary = read_incomes("data/incomes.csv")
    postcode_to_lat_long = read_postcode_mapping("data/postcode-data.csv")
    combined_data = process_housing_data(
        "data/housing-price-paid.csv", postcode_to_lat_long, year_to_salary
    )
    write_combined_data("output/combined_postcode_sales.csv", combined_data)
