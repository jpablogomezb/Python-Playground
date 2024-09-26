import json
import csv

# Load GeoJSON data
with (open('./geodata/csv/UCD_trees_sites/Trees_site_7.geojson', 'r')
      as geojson_file):
    geojson_data = json.load(geojson_file)

# Open a CSV file to write the data
with (open('/Users/jpgbs/Dev/UCD/CartoSpot-API/src/sa_api_v2/'
           'management/data/interval/ucd_site_7_places.csv', 'w', newline='')
      as csvfile):
    fieldnames = ['submitter', 'dataset', 'geometry', 'visible', 'data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate through GeoJSON features
    for feature in geojson_data['features']:
        geometry = feature['geometry']
        coordinates = geometry['coordinates']

        # Create the SRID and Point structure
        geometry_str = f"SRID=4326;POINT ({coordinates[0]} {coordinates[1]})"

        # Extract the properties and map them to the CSV format
        properties = feature['properties']
        data_dict = {
            "STD": properties.get("STD"),
            "canopy_area": properties.get("Area"),
            "canopy_perimeter": properties.get("Perimeter"),
            "height": properties.get("Max"),
            "avg_height": properties.get("Mean"),
            "date_created": properties.get("Date_1"),
            "NTM_ID": properties.get("NTM_ID"),
            "location_type": "data-required",
            "submitter_name": "INTERVAL Project"  # Static value
        }

        # Convert the data dict to JSON string with double quotes
        data_str = json.dumps(data_dict)

        # Write the row to the CSV
        writer.writerow({
            'submitter': 51,
            'dataset': 307,
            'geometry': geometry_str,
            'visible': 'TRUE',
            'data': data_str
        })

print("CSV generation complete!")
