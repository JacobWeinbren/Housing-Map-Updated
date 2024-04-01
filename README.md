# Updated Housing Map

## Data Sources

-   **HM Land Registry Price Paid Data**: [Access Here](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#november-2023-data-current-month)
-   **Ordnance Survey (OS) Building Map**: [Access Here](https://osdatahub.os.uk/downloads/open/OpenMapLocal)
-   **ONS Postcode Registry**: [Access Here](https://geoportal.statistics.gov.uk/datasets/a2f8c9c5778a452bbf640d98c166657c/about)
-   **ONS Median Gross Salary Data**: [Access Here](https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/averagesalarydatafromjanuary1970toaugust2022)
-   **MOSA Areas EW BFE Data**: [Access Here](<https://geoportal.statistics.gov.uk/search?collection=Dataset&tags=all(BDY_RGN%2CDEC_2021)>)

## Processing Workflow

1.  **Data Merging**:
    Run `combined_postcode_sales.py` to integrate data from income and postcode sales.

2.  **Data Conversion and Spatial Analysis**:
    Execute `process_combined.py`. This script transforms CSV data into a GeoDataFrame, performs spatial joins, calculates average property prices, and exports the results to `[year].geojson`.

3.  **MBTiles Generation**:
    Convert GeoJSON to MBTiles using Tippecanoe.

    ```
    for file in output/years/*.geojson; do
        output_file="output/years_processed/$(basename "$file" .geojson).mbtiles"
        tippecanoe --output="$output_file" --generate-ids --force --no-feature-limit --no-tile-size-limit -r1 --minimum-zoom=0 --maximum-zoom=17 "$file"
    done
    ```

    ```
    tippecanoe --output=output/housing_map.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders --coalesce-fraction-as-needed --coalesce-densest-as-needed --coalesce-smallest-as-needed --coalesce --reorder --minimum-zoom=9 --maximum-zoom=16 --simplification=30 -x fid -x id -x feature_code -x FID -x MSOA21CD -x MSOA21NM -x BNG_E -x BNG_N -x LONG -x LAT -x GlobalID -r1 output/housing_map.geojson
    ```

4.  **Data Binning and Analysis**:
    Run `bins.py` to calculate median and percentile values for property prices. Outputs in `bins.json`.

## Key Assumptions

-   Income data reflects the most recent surveys.
-   Year calculation includes leap year adjustment.

## Required Data Files

Place the following files in the `data` directory:

-   `incomes.csv`: Contains `Year` and `Salary`.
-   `postcode-data.csv`: Includes `pcds`, `lat`, and `long`.
-   `housing-price-paid.csv`: Covers transaction price, date, and postcode.
-   `MSOA.geojson`: Spatial data for Output Areas.
-   `buildings.geojson`: Building data in WGS 84 format.

## Output Files

-   `combined_postcode_sales.csv`: Combined data with normalized prices.
-   `housing_map.geojson`: Spatial data with average prices per area and year.
-   `bins.json`: Percentile and median values for the dataset.
