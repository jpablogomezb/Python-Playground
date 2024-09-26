import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load the data (use your file here)
gdf = gpd.read_file("../combine_geodata_files/combined_file.geojson")

# Specify the attribute to classify (replace with your column name)
attribute = "NO2_8s"

# Define the bins (based on the values you want to classify)
bins = [14, 25, 50, 120, 370]  # Adjust based on your data
labels = ["14 to 25", "25 to 50", "50 to 120", "120 to 370"]

# Create a new column in the GeoDataFrame with the binned data
gdf['binned'] = pd.cut(gdf[attribute], bins=bins, labels=labels, include_lowest=True)

# Set up a color map for the discrete values (4 bins)
cmap = plt.get_cmap("RdYlBu_r")  # You can change the color map here
colors = ["#fef0d9", "#fdcc8a", "#fc8d59", "#d7301f"]  # Replace with desired color values

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(column='binned', cmap=cmap, legend=True, ax=ax, linewidth=1, edgecolor="black")

# Customize the legend
legend = ax.get_legend()
legend.set_bbox_to_anchor((1, 1))  # Position the legend

# Display the map
plt.show()
