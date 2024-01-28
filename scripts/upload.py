from mapbox import Uploader
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure your Mapbox access token is set as an environment variable
if not os.getenv("MAPBOX_ACCESS_TOKEN"):
    raise ValueError("MAPBOX_ACCESS_TOKEN environment variable not set")

# Initialize the uploader
uploader = Uploader()

# Specify the path to your MBTiles file
mbtiles_file = "/output/housing_map.mbtiles"

# Create a unique tileset ID for your upload. This is typically in the format {username}.{tileset_name}
tileset_id = "edmiliband.housing_map"

# Start the upload process
with open(mbtiles_file, "rb") as src:
    upload_resp = uploader.upload(src, tileset_id)

# Check the response
if upload_resp.status_code == 201:
    print("Upload started successfully.")
    print(upload_resp.json())
else:
    print("Upload failed.")
    print(upload_resp.text)
