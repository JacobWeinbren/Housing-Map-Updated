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
    Execute `process_combined.py`. This script transforms CSV data into a GeoDataFrame, performs spatial joins, calculates average property prices, and exports the results to `housing_map.geojson`.

3.  **Intersect Maps**:
    Intersects `buildings.geojson` with `housing_map.geojson`

    ```bash
    python intersect.py
    ```

4.  **MBTiles Generation**:
    Convert GeoJSON to MBTiles using Tippecanoe. Example commands:

    ```
    tippecanoe --output=output/merged.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders --minimum-zoom=0 --coalesce-fraction-as-needed --coalesce-densest-as-needed --coalesce-smallest-as-needed --coalesce --reorder --minimum-zoom=9 --maximum-zoom=16 --simplification=20 -x fid -x id -x feature_code -x FID -x MSOA21CD -x MSOA21NM -x BNG_E -x BNG_N -x LONG -x LAT -x GlobalID output/merged.geojson
    ```

5.  **Hosting**:
    Use [OpenMapTiles](https://openmaptiles.org/docs/host/tileserver-gl/) for hosting. Run the following Docker command (-d for running in the background):

    ```
    docker run -it -d -v /root/map-server:/data -p 8080:8080 maptiler/tileserver-gl -c /data/config.json
    ```

6.  **Data Binning and Analysis**:
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

## HTTPS Configuration with Nginx

To serve the application securely over HTTPS, configure Nginx as a reverse proxy:

1. **Edit Nginx Configuration**:
   Edit the configuration for your domain:

    ```
    sudo nano /etc/nginx/sites-available/map.kafkaesque.blog
    ```

2. **Configuration Details**:
   Redirect HTTP to HTTPS and proxy HTTPS to port 8080. Use the provided SSL certificate paths.

3. **Enable Site Configuration**:

    ```
    sudo ln -s /etc/nginx/sites-available/map.kafkaesque.blog /etc/nginx/sites-enabled/
    ```

4. **Test and Reload Nginx**:

    ```
    sudo nginx -t
    sudo systemctl reload nginx
    ```

5. **Verify HTTPS Setup**:
   Ensure the site `https://map.kafkaesque.blog` is accessible.

## Obtaining SSL Certificate with Certbot

1. **Install Certbot and Plugin**:

    ```
    sudo apt update
    sudo apt install certbot python3-certbot-nginx
    ```

2. **Obtain and Install SSL Certificate**:

    ```
    sudo certbot --nginx -d map.kafkaesque.blog
    ```

3. **Verify Auto-Renewal**:

    ```
    sudo certbot renew --dry-run
    ```

4. **Check Scheduled Renewal**:
   Verify the scheduling of the Certbot renewal process.

    ```
    systemctl list-timers | grep certbot
    ```
