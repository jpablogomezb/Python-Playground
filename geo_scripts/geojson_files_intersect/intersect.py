import geopandas as gpd

# Load the points and area GeoJSON files
points_gdf = gpd.read_file('./data/new_trees.geojson')
area_gdf = gpd.read_file('./data/MapA.geojson')

# Assuming the area GeoJSON contains only one feature, extract it
area = area_gdf.geometry.unary_union

# Select points that are within or intersect with the area
selected_points = points_gdf[points_gdf.intersects(area)]

# Select points that do not intersect with the area
not_selected_points = points_gdf[~points_gdf.intersects(area)]

# Save the selected points to a new GeoJSON file
selected_points.to_file('./output/selected_points.geojson', driver='GeoJSON')

# Save the non-selected points to a separate GeoJSON file
not_selected_points.to_file('./output/not_selected_points.geojson', driver='GeoJSON')

# Optionally, you can print the results to check
print("Selected Points:")
print(selected_points)
print("\nNot Selected Points:")
print(not_selected_points)

