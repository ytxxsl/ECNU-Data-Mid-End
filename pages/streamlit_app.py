import streamlit as st
import folium
from folium import plugins

# Create map object, set initial location to Beijing and zoom level
m = folium.Map(location=[39.9042, 116.4074], zoom_start=12)  # Beijing coordinates

# Add multiple path points
path = [
    [39.9042, 116.4074],  # Beijing (start point)
    [39.9142, 116.4174],  # A point along the path
    [39.9242, 116.4724],  # Another point along the path
    [39.9342, 116.4074],  # Another point along the path
    [39.9442, 116.4474]   # Endpoint
]

# Function to create a green gradient effect for the path
def create_green_gradient_path(path):
    """Create a green gradient based on path length and index."""
    path_length = len(path)
    greens = ["#006400", "#228B22", "#32CD32", "#00FF00", "#98FB98"]  # Different shades of green
    gradient_path = []
    for i, point in enumerate(path):
        color = greens[int(i / path_length * (len(greens) - 1))]
        gradient_path.append((point, color))
    return gradient_path

# Generate green gradient path
gradient_path = create_green_gradient_path(path)

# Draw the path with a green gradient effect
for i in range(1, len(gradient_path)):
    folium.PolyLine(
        locations=[gradient_path[i-1][0], gradient_path[i][0]],
        color=gradient_path[i][1],
        weight=5,
        opacity=0.7
    ).add_to(m)

# Add beautified markers with styled popups for the path
for point in path:
    popup_content = f"""
    <div style="font-family: Arial, sans-serif; color: #333; font-size: 14px;">
        <h4 style="color: #32CD32;">Location Details</h4>
        <p><strong>Coordinates:</strong> {point}</p>
        <p><strong>Address:</strong> Sample Address for {point[0]}, {point[1]}</p>
        <p><a href="https://www.google.com/maps?q={point[0]},{point[1]}" target="_blank" style="color: #32CD32;">View on Google Maps</a></p>
    </div>
    """

    # Custom marker icon in green
    folium.Marker(
        location=point,
        popup=folium.Popup(popup_content, max_width=300),
        icon=folium.Icon(color='green', icon='cloud', prefix='fa')  # Custom icon (FontAwesome cloud)
    ).add_to(m)

    # Optional: Use CircleMarker for a more colorful look with green tones
    folium.CircleMarker(
        location=point,
        radius=10,
        color='green',
        fill=True,
        fill_color='lightgreen',  # Light green fill
        fill_opacity=0.6,
        popup=folium.Popup(popup_content, max_width=300)
    ).add_to(m)

# Display the map in the Streamlit page
st.write("### Green Themed Path Map with Beautified Markers and Styled Popups")
st.components.v1.html(m._repr_html_(), height=600)
