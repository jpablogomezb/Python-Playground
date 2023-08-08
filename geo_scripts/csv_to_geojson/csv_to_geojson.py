import os
import csv
import json
from constants import GEOJSON_COORDINATES, GEOJSON_PROPERTIES


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_geojson_feature(properties, geometry):
    feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": geometry
    }
    return feature


def create_point_geometry(latitude, longitude):
    geometry = {
        "type": "Point",
        "coordinates": [longitude, latitude]
    }
    return geometry


def main():
    csv_file = os.path.join(
        BASE_DIR, "geodata", "csv", "EPA_Ave_Quality.csv")
    geojson_file = os.path.join(
        BASE_DIR, "geodata", "geojson", "EPA_Ave_Quality.geojson")

    features = []

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            properties = {}
            for property_name in GEOJSON_PROPERTIES:
                try:
                    properties[property_name] = float(row[property_name])
                except (ValueError, TypeError):
                    properties[property_name] = str(row[property_name])

            coordinates = {}
            for coord_name in GEOJSON_COORDINATES:
                coordinates[coord_name] = float(row[coord_name])

            geometry = create_point_geometry(
                coordinates[GEOJSON_COORDINATES[0]],
                coordinates[GEOJSON_COORDINATES[1]]
            )
            feature = create_geojson_feature(properties, geometry)
            features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w') as jsonfile:
        json.dump(geojson_data, jsonfile, indent=2)


if __name__ == '__main__':
    main()
