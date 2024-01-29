# Updated Housing Map

## Data Sources

| Source Name                         | Access URL                                                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| HM Land Registry Price Paid Data    | [HM Land Registry Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#november-2023-data-current-month)          |
| Ordnance Survey (OS) Building Map   | [OS Building Map](https://osdatahub.os.uk/downloads/open/OpenMapLocal)                                                                           |
| ONS Postcode Registry               | [ONS Postcode Data](https://geoportal.statistics.gov.uk/datasets/a2f8c9c5778a452bbf640d98c166657c/about)                                         |
| ONS Median Gross Salary Data        | [ONS Salary Data](https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/averagesalarydatafromjanuary1970toaugust2022) |
| ONS Output Areas (2021) EW BFE Data | [ONS Output Areas](https://hub.arcgis.com/datasets/ons::output-areas-2021-ew-bfe/about)                                                          |

## Processing Workflow

1. **Data Merging:** Run `scripts/combine.py` to integrate data from the sources mentioned above. Place all necessary data files in the `data` directory prior to running the script.
2. **Data Conversion and Spatial Analysis:** Execute `scripts/process_combined.py`. This script transforms the combined CSV data into a GeoDataFrame, carries out spatial joins, and computes average property prices. It also updates GeoJSON properties with these averages and exports the result to `output/housing_map.geojson`.
3. **MBTiles Generation:** Use Tippecanoe to convert GeoJSON files to MBTiles format, suitable for web mapping applications. Run the following commands:

    ```bash
    tippecanoe --output=output/housing_map.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders  --minimum-zoom=0 --coalesce-fraction-as-needed  --simplify-only-low-zooms --coalesce-densest-as-needed --coalesce-smallest-as-needed --maximum-zoom=19 output/housing_map.geojson
    ```

    ```bash
    tippecanoe --output=output/buildings.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders  --minimum-zoom=0 --coalesce-fraction-as-needed  --simplify-only-low-zooms --coalesce-densest-as-needed --coalesce-smallest-as-needed --maximum-zoom=19 data/buildings.geojson
    ```

4. **Hosting:** For hosting, [OpenMapTiles](https://openmaptiles.org/docs/host/tileserver-gl/) is utilised. Ensure access to a VPN that accommodates Docker containers for this purpose. Files should be placed within a `data` directory, followed by executing the instructions provided in the linked guide. Use -d to run in detached mode (in the background).

    ```bash
    docker run -d -it -v $(pwd):/data -p 8080:80 maptiler/tileserver-gl
    ```

5. **Data Binning and Analysis:** Run `output/bins.py` to calculate the median and percentile values for normalized property prices annually. The script outputs these metrics in a JSON file.

## Key Assumptions

-   Income data is based on the latest surveys, assuming they provide the most accurate and reliable figures.
-   The year is calculated assuming 365.25 days for leap year adjustments.

## Required Data Files

The following data files must be present in the `data` directory for successful script execution:

-   `incomes.csv`: Salary data file with columns for `Year` and `Salary`.
-   `postcode-data.csv`: Postcode information file with columns for `pcds`, `lat`, and `long`.
-   `housing-price-paid.csv`: Housing transaction data file with columns for transaction price, date, and postcode.
-   `OA.geojson`: Geographical boundaries for Output Areas, used in spatial joins.
-   `buildings.geojson`: Building data from the OS Map, processed to WGS 84 format in QGIS with a visvalingam simplification of 20m tolerance.

## Output Files

-   `combined_postcode_sales.csv`: Located in the `output` directory, this file combines all data with normalised prices, postcodes, and geographical coordinates.
-   `housing_map.geojson`: Also in the `output` directory, this GeoJSON file includes spatially joined data with average prices per area and year.
-   `bins.json`: File showing the percentile and median values for the dataset.
