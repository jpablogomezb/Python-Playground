import geopandas as gpd
import pandas as pd
import os
import glob

# Ask user for the file format (SHP or GeoJSON)
file_format = input("Enter the file format (SHP or GeoJSON): ").strip().lower()

# Ask user for the folder path where the files are located
folder_path = input("Enter the folder path where the files are located: ").strip()

# Search for all files in the folder with the chosen format
if file_format == "shp":
    file_extension = "*.shp"
elif file_format == "geojson":
    file_extension = "*.geojson"
else:
    raise ValueError(
        "Unsupported file format! Please enter 'SHP' or 'GeoJSON'.")

# Use glob to search for files with the chosen extension in the folder
shapefiles = glob.glob(os.path.join(folder_path, file_extension))

# Check if any files were found
if not shapefiles:
    raise FileNotFoundError(
        f"No {file_format.upper()} files found in the specified folder!")

print(f"Found {len(shapefiles)} {file_format.upper()} files to process.")

# Ask if the user wants to reproject the data
reproject = input("Do you want to reproject the data? (yes/no): ").strip().lower()

# If user chooses to reproject, ask for the EPSG code
if reproject == "yes":
    epsg_code = input(
        "Enter the EPSG code for reprojection "
        "(e.g., 2157 for Irish Transverse Mercator): ").strip()
    try:
        # Convert the EPSG code to an integer to validate it
        epsg_code = int(epsg_code)
    except ValueError:
        raise ValueError(
            "Invalid EPSG code. Please enter a valid integer EPSG code.")
    print(f"Reprojecting data to EPSG:{epsg_code}.")
else:
    print("Reprojection skipped. The data will retain the original CRS.")

# GeoPandas automatically recognizes the format from the file extension
gdf_list = [gpd.read_file(shp) for shp in shapefiles]

# Combine the GeoDataFrames into one
combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))

# Reproject the combined GeoDataFrame if the user chooses to do so
if reproject == "yes":
    combined_gdf = combined_gdf.to_crs(f"EPSG:{epsg_code}")
    print(f"Data reprojected to EPSG:{epsg_code}.")
else:
    print("Reprojection skipped. The data will retain the original CRS.")

# Set the output file format and driver based on user input
if file_format == "shp":
    output_file = f"combined_file.shp" \
        if reproject == "no" else f"combined_file_EPSG{epsg_code}.shp"
    driver = None  # No need to specify the driver for SHP
elif file_format == "geojson":
    output_file = f"combined_file.geojson" \
        if reproject == "no" else f"combined_file_EPSG{epsg_code}.geojson"
    driver = "GeoJSON"  # Specify driver for GeoJSON
else:
    raise ValueError("Unsupported file format! Please enter 'SHP' or 'GeoJSON'.")

# Save the combined GeoDataFrame into a new file
if driver:
    combined_gdf.to_file(output_file, driver=driver)
else:
    combined_gdf.to_file(output_file)

print(f"Files combined and saved as {output_file}!")
