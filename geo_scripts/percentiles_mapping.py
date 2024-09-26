import geopandas as gpd


def classify_and_sort_segments(
        input_geojson, output_geojson, property_name):
    # Step 1: Load the GeoJSON file
    gdf = gpd.read_file(input_geojson)

    # Ensure the property exists in the GeoDataFrame
    if property_name not in gdf.columns:
        raise ValueError(
            f"Property '{property_name}' not found in the data. "
            f"Available properties are: {list(gdf.columns)}")

    # Step 2: Sort the features by the selected property
    # (property_name) in ascending order
    gdf = gdf.sort_values(by=property_name, ascending=True)

    # Step 3: Calculate the percentiles based on the selected property
    p1 = gdf[property_name].quantile(0.01)
    p5 = gdf[property_name].quantile(0.05)
    p10 = gdf[property_name].quantile(0.10)
    p90 = gdf[property_name].quantile(0.90)
    p95 = gdf[property_name].quantile(0.95)
    p99 = gdf[property_name].quantile(0.99)

    # Step 4: Define a function to classify the road segments
    def classify_segment(value):
        if value >= p99:
            return 'Hotspot 99th'
        elif value >= p95:
            return 'Hotspot 95th'
        elif value >= p90:
            return 'Hotspot 90th'
        elif value <= p1:
            return 'Coldspot 1st'
        elif value <= p5:
            return 'Coldspot 5th'
        elif value <= p10:
            return 'Coldspot 10th'
        else:
            return 'Not Significant'

    # Step 5: Apply the classification to the GeoDataFrame
    gdf['classification'] = gdf[property_name].apply(classify_segment)

    # Step 6: Export the classified and sorted segments to a GeoJSON file
    gdf.to_file(output_geojson, driver='GeoJSON')

# Example usage:
classify_and_sort_segments(
    './combine_geodata_files/combined_file.geojson',
    './outputs/NO2_percentile_segments.geojson',
    'NO2_8s')
