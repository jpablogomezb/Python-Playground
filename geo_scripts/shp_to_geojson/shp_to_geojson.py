import geopandas as gpd
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Ask the user for the folder path containing the shapefiles
shapefile_folder = input(
    "Please enter the folder path where the shapefiles are located: ").strip()

if not os.path.exists(shapefile_folder):
    print(f"Error: The folder '{shapefile_folder}' does not exist.")
    exit(1)

# List of shapefiles in the provided folder (automatically detects .shp files)
shapefile_paths = [os.path.join(shapefile_folder, f)
                   for f in os.listdir(shapefile_folder) if f.endswith('.shp')]

if not shapefile_paths:
    print("No shapefiles (.shp) found in the provided folder.")
    exit(1)

# Ask the user for the output directory to save GeoJSON files
output_directory = input(
    "Please enter the folder path where you want to save the GeoJSON files: ").strip()

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

print(f"Processing {len(shapefile_paths)} shapefile(s)...\n")

# Convert each shapefile to GeoJSON with re-projection to WGS 84 (EPSG:4326)
for shp in shapefile_paths:
    try:
        # Load the shapefile
        gdf = gpd.read_file(shp, driver='SHP')

        # Reproject the GeoDataFrame to WGS 84 (EPSG:4326)
        gdf = gdf.to_crs(epsg=4326)

        # Create the output GeoJSON file path
        output_geojson_path = os.path.join(
            output_directory, os.path.splitext(
                os.path.basename(shp))[0] + '.geojson')

        # Save the reprojected GeoDataFrame to a GeoJSON file
        gdf.to_file(output_geojson_path, driver='GeoJSON')

        print(f"✅ Saved GeoJSON: {output_geojson_path}")
    except Exception as e:
        print(f"❌ Failed to process {shp}: {e}")

print("\nProcessing complete.")

