import geopandas as gpd
import os

# List your shapefile paths here
shapefile_paths = [
    'geodata/MapA.shp',
    'geodata/MapB.shp',
    'geodata/MapC.shp',
    'geodata/MapD.shp',
    'geodata/MapE.shp',
    'geodata/MapF.shp',
    'geodata/MapG.shp',
    'geodata/MapH.shp',
    'geodata/MapI.shp',
    'geodata/MapJ.shp'
]

# Directory where you want to save the GeoJSON files
output_directory = 'geodata/geojson'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Convert each shapefile to GeoJSON with re-projection to WGS 84 (EPSG:4326)
for shp in shapefile_paths:
    # Load the shapefile
    gdf = gpd.read_file(shp)

    # Reproject the GeoDataFrame to WGS 84 (EPSG:4326)
    gdf = gdf.to_crs(epsg=4326)

    # Create the output GeoJSON file path
    output_geojson_path = os.path.join(
        output_directory, os.path.splitext(
            os.path.basename(shp))[0] + '.geojson')

    # Save the reprojected GeoDataFrame to a GeoJSON file
    gdf.to_file(output_geojson_path, driver='GeoJSON')

    print(f"Saved GeoJSON: {output_geojson_path}")
