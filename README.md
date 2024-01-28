# Housing Map - Updated

## Sources

| Source                           | URL                                                                                                                                                                                                                                                            |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HM Land Registry Price Paid Data | [https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#november-2023-data-current-month](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#november-2023-data-current-month)                               |
| OS Building Map                  | [https://www.arcgis.com/home/item.html?id=e0df7f3ac3a64e8d96f312dfc3f757b6](https://www.arcgis.com/home/item.html?id=e0df7f3ac3a64e8d96f312dfc3f757b6)                                                                                                         |
| ONS Postcode Registry            | [https://geoportal.statistics.gov.uk/datasets/a2f8c9c5778a452bbf640d98c166657c/about](https://geoportal.statistics.gov.uk/datasets/a2f8c9c5778a452bbf640d98c166657c/about)                                                                                     |
| ONS Average Salary Data          | [https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/averagesalarydatafromjanuary1970toaugust2022](https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/averagesalarydatafromjanuary1970toaugust2022) |
| ONS Output Areas (2021) EW BFE   | [https://hub.arcgis.com/datasets/ons::output-areas-2021-ew-bfe/about](https://hub.arcgis.com/datasets/ons::output-areas-2021-ew-bfe/about)                                                                                                                     |

## Steps

1. Run `scripts/combine.py` to merge and process the data from the sources listed above. Ensure all required data files are placed in the `data` directory before running the script.
2. Execute `scripts/process_combined.py` to convert the combined CSV data into a GeoDataFrame, perform spatial joins, and calculate average prices. This script also updates the GeoJSON properties with these average prices and saves the output to `output/housing_map.geojson`.
3. Use Tippecanoe to convert the GeoJSON file into an MBTiles format suitable for web mapping applications. Run the following command:

```bash
tippecanoe --output=output/housing_map.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders  --minimum-zoom=0 --coalesce-fraction-as-needed  --simplify-only-low-zooms --coalesce-densest-as-needed --coalesce-smallest-as-needed --maximum-zoom=23 output/housing_map.geojson
```

### Assumptions

-   We are using the latest surveys for all income data, as they are the most likely to be reliable.
-   There are 365.25 days in a year

### Required Data Files

For the script to run successfully, ensure the following data files are available in the `data` directory:

-   `incomes.csv`: Contains salary data. Each row should have `Year` and `Salary` columns.
-   `postcode-data.csv`: Contains postcode mappings to latitude and longitude. Each row should have `pcds`, `lat`, and `long` columns.
-   `housing-price-paid.csv`: Contains housing transaction data. Each row should include at least the transaction price, date, and postcode.
-   `OA.geojson`: Contains the geographical boundaries for Output Areas used in the spatial join process.

### Output

The script generates a file named `combined_postcode_sales.csv` in the `output` directory. This file contains the combined data with normalized prices, postcodes, and geographical coordinates. Additionally, the `scripts/process_combined.py` script produces a GeoJSON file named `housing_map.geojson` in the `output` directory, which includes the spatially joined data and average prices per area and year.
