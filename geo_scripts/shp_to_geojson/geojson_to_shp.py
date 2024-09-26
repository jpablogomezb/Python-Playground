import geopandas as gpd
import os

# Ask the user for the folder path containing the GeoJSON files
geojson_folder = input(
    "Please enter the folder path where the GeoJSON files are located: ")

# List of GeoJSON files in the provided folder
# (automatically detects .geojson files)
geojson_paths = [os.path.join(geojson_folder, f)
                 for f in os.listdir(geojson_folder) if f.endswith('.geojson')]

print(f"Found {len(geojson_paths)} files to process.")

# Ask the user for the output directory to save Shapefiles
output_directory = input(
    "Please enter the folder path where you want to save the Shapefiles: ")

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Ask if the user wants to reproject the data
reproject = input("Do you want to reproject the data? (yes/no): ").strip().lower()

# If the user chooses to reproject, ask for the EPSG code
if reproject == "yes":
    epsg_code = input(
        "Enter the EPSG code for reprojection "
        "(e.g., 2157 for Irish Transverse Mercator): ").strip()
    try:
        # Convert the EPSG code to an integer to validate it
        epsg_code = int(epsg_code)
        print(f"Reprojecting data to EPSG:{epsg_code}.")
    except ValueError:
        raise ValueError(
            "Invalid EPSG code. Please enter a valid integer EPSG code.")
else:
    print("Reprojection skipped. The data will retain the original CRS.")

# Convert each GeoJSON file to Shapefile
for geojson in geojson_paths:
    try:
        # Load the GeoJSON file
        gdf = gpd.read_file(geojson)

        # Reproject if the user requested it
        if reproject == "yes":
            gdf = gdf.to_crs(epsg=epsg_code)

        # Create the output Shapefile path
        output_shapefile_path = os.path.join(
            output_directory, os.path.splitext(
                os.path.basename(geojson))[0] + '.shp')

        # Save the GeoDataFrame as a Shapefile
        gdf.to_file(output_shapefile_path, driver='ESRI Shapefile')

        print(f"Saved Shapefile: {output_shapefile_path}")
    except Exception as e:
        print(f"Failed to process {geojson}: {e}")
