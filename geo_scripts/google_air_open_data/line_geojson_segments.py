import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium
import geopandas as gpd
from shapely.geometry import LineString, mapping
from osgeo import ogr, osr
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Function to parse the geojson string into list of tuples
def parse_geojson(geojson_str):
    if isinstance(geojson_str, str):
        points = geojson_str.strip('[]').split('],[')
        # Reverse the order of each coordinate pair to (longitude, latitude)
        return [tuple(map(float, point.split(',')))[::-1] for point in points]
    return []


def process_csv(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    # Apply the parsing function to the 'line_geojson' column
    data['parsed_geojson'] = data['line_geojson'].apply(parse_geojson)
    # Determine the base name for output files
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Check if 'datetime_h' column exists, else extract by 'Date'
    if 'datetime_h' in data.columns:
        # Format the hour to always have two digits
        data['datetime_h'] = data['datetime_h'].apply(lambda x: f'{int(x):02d}')
        data['date_hour'] = data['Date'] + " " + data['datetime_h']
        # Extract separate date, hour, and timestamp fields
        data['date'] = pd.to_datetime(data['date_hour']).dt.date
        data['hour'] = pd.to_datetime(data['date_hour']).dt.hour
        data['timestamp'] = pd.to_datetime(data['date_hour'])
        # Group by 'date_hour' and calculate mean of pm25_8sMedian and NO2_8s
        grouped_data = data.groupby('date_hour').agg({
            'parsed_geojson': 'sum',
            'pm25_8sMedian': 'mean',
            'NO2_8s': 'mean',
            'date': 'first',
            'hour': 'first',
            'timestamp': 'first'
        })
    else:
        try:
            # Extracting date and hour from 'timestamp_new'
            data['timestamp_new'] = pd.to_datetime(data['timestamp_new'])
            data['date'] = data['timestamp_new'].dt.date
            data['hour'] = data['timestamp_new'].dt.hour
            data['timestamp'] = data['timestamp_new']
            data['date_hour'] = data['timestamp_new'].dt.strftime('%Y-%m-%d %H')
        except Exception as e:
            print(f"Error parsing timestamp_new: {e}")
            data['date'] = pd.to_datetime(data['Date']).dt.date
            data['hour'] = pd.to_datetime(data['Date']).dt.hour
            data['timestamp'] = pd.to_datetime(data['Date'])
            data['date_hour'] = data['Date']

        # Group by 'date' and calculate mean of pm25_8sMedian and NO2_8s
        grouped_data = data.groupby('date_hour').agg({
            'parsed_geojson': 'sum',
            'pm25_8sMedian': 'mean',
            'NO2_8s': 'mean',
            'date': 'first',
            'hour': 'first',
            'timestamp': 'first'
        })

    # Define output file for raw grouped data
    grouped_data_csv_path = os.path.join(
        BASE_DIR, "outputs", f"{file_name}_grouped_geodata_raw.csv")
    grouped_data.to_csv(grouped_data_csv_path, header=True)

    # Remove duplicate points from each list
    grouped_data['parsed_geojson'] = grouped_data['parsed_geojson'].apply(
        lambda x: list(dict.fromkeys(x))
    )

    # Define output file path for unique points
    unique_points_csv_path = os.path.join(
        BASE_DIR, "outputs", f"{file_name}_grouped_geodata_no_duplicates.csv")
    grouped_data.to_csv(unique_points_csv_path, header=True)

    return grouped_data



# Function to generate a distinct color for each unique datetime_h value
def get_color_by_hour(hour, total_hours):
    cmap = plt.colormaps['hsv']
    return mcolors.rgb2hex(cmap(hour / total_hours))


# Function to plot paths on a map with different colors for each datetime_h
def plot_paths_on_map(paths_data):
    first_path = next(iter(paths_data['parsed_geojson']), [])
    map_center = first_path[0] if first_path else (53.3498, -6.2603)
    map_object = folium.Map(
        location=map_center, zoom_start=10, tiles='CartoDB dark_matter')
    # Total number of distinct hours (or paths) for color mapping
    total_hours = len(paths_data)

    # Add each path to the map with a distinct color and a popup
    for idx, (hour, row) in enumerate(paths_data.iterrows()):
        path = row['parsed_geojson']
        color = get_color_by_hour(idx, total_hours)
        # Ensure the path has at least 2 points to form a line
        if len(path) > 1:
            popup_text = (
                f"Date/Time: {hour}<br>"
                f"PM2.5: {row['pm25_8sMedian']:.2f}<br>"
                f"NO2: {row['NO2_8s']:.2f}<br>"
                f"Date: {row['date']}<br>"
                f"Hour: {row['hour']}<br>"
                f"Timestamp: {row['timestamp']}"
            )
            folium.PolyLine(
                path,
                color=color,
                weight=3.5,
                opacity=0.8,
                popup=popup_text
            ).add_to(map_object)

    return map_object


def create_geojson_from_grouped_data(grouped_data, base_dir, file_name):
    features = []

    # Iterate over the grouped data to create LineString features
    for time_group, row in grouped_data.iterrows():
        points = row['parsed_geojson']
        # Ensure there are at least two points to form a LineString
        if len(points) > 1:
            # Reverse the order of each coordinate from (lat, lon) to (lon, lat)
            reversed_points = [point[::-1] for point in points]
            geometry = LineString(reversed_points)
            feature = {
                "type": "Feature",
                "properties": {
                    "time_group": time_group,
                    "pm25_8sMedian": row['pm25_8sMedian'],
                    "NO2_8s": row['NO2_8s'],
                    "date": row['date'].isoformat(),
                    "hour": row['hour'],
                    "timestamp": row['timestamp'].isoformat()
                },
                "geometry": mapping(geometry)
            }
            features.append(feature)

    # Compile the FeatureCollection
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    # Output path for the GeoJSON file
    geojson_path = os.path.join(
        base_dir, "outputs", f"{file_name}_paths.geojson")

    # Write GeoJSON file
    with open(geojson_path, 'w') as f:
        json.dump(feature_collection, f)

    print(f"GeoJSON saved to {geojson_path}")
    return geojson_path


def convert_geojson_to_shapefile(geojson_path, output_shp_path):
    # Register the drivers
    ogr.RegisterAll()

    # Open the GeoJSON file
    source_driver = ogr.GetDriverByName("GeoJSON")
    source_ds = source_driver.Open(geojson_path, 0)  # 0 means read-only
    if source_ds is None:
        print(f"Could not open {geojson_path}")
        return

    # Create the shapefile
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_shp_path):
        shp_driver.DeleteDataSource(output_shp_path)
    out_ds = shp_driver.CreateDataSource(output_shp_path)
    if out_ds is None:
        print(f"Could not create {output_shp_path}")
        return

    # Get the source layer
    source_layer = source_ds.GetLayer()

    # Create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    # Create the output layer
    out_layer = out_ds.CreateLayer(output_shp_path, srs, source_layer.GetGeomType())

    # Add fields to the shapefile from the source layer
    source_layer_def = source_layer.GetLayerDefn()
    for i in range(source_layer_def.GetFieldCount()):
        field_def = source_layer_def.GetFieldDefn(i)
        out_layer.CreateField(field_def)

    # Copy features from the GeoJSON layer to the shapefile layer
    for feature in source_layer:
        out_layer.CreateFeature(feature)

    # Cleanup
    source_ds = None
    out_ds = None
    print(f"Shapefile saved to {output_shp_path}")


def main():
    # Directory containing the data files
    geodata_dir = os.path.join(BASE_DIR, "geodata")

    # Iterate through each file in the geodata directory
    for filename in os.listdir(geodata_dir):
        # Construct the full file path
        file_path = os.path.join(geodata_dir, filename)

        # Skip if it's not a file
        if not os.path.isfile(file_path):
            continue

        # Processing the CSV file
        processed_data = process_csv(file_path)

        geojson_path = create_geojson_from_grouped_data(
            processed_data, BASE_DIR, filename)

        # Convert the GeoJSON to Shapefile
        shp_file_name = "{}_paths.shp".format(os.path.splitext(filename)[0])
        shp_file_path = os.path.join(BASE_DIR, "outputs/shapefiles/", shp_file_name)
        convert_geojson_to_shapefile(geojson_path, shp_file_path)

        # Plotting the paths
        map_with_paths = plot_paths_on_map(processed_data)

        # Generate a unique map file name based on the input file
        map_file_name = "{}_map_sensor_paths.html".format(
            os.path.splitext(filename)[0])
        map_file_path = os.path.join(BASE_DIR, "outputs/webmaps/", map_file_name)

        # Save the map to an HTML file
        map_with_paths.save(map_file_path)

        # Displaying the first few results and the file path of the map
        print(processed_data.head(), map_file_path, geojson_path, shp_file_path)


if __name__ == '__main__':
    main()
