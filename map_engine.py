import folium
from streamlit_folium import st_folium


def generate_resource_map(vaccines, beds, treatments):
    """
    Generates an interactive map distributing optimized resources 
    across real regional hospital facilities in Durham Region.
    """
    # Real health system nodes with bed-capacity weighting
    hospitals = [
        {"name": "Lakeridge Health Oshawa", "lat": 43.9033,
            "lon": -78.8683, "capacity_share": 0.45},
        {"name": "Ajax Pickering Hospital", "lat": 43.8369,
            "lon": -79.0169, "capacity_share": 0.25},
        {"name": "Lakeridge Health Whitby", "lat": 43.8765,
            "lon": -78.9430, "capacity_share": 0.15},
        {"name": "Lakeridge Health Bowmanville", "lat": 43.9100,
            "lon": -78.6800, "capacity_share": 0.15},
    ]

    # Center map on Durham Region
    m = folium.Map(location=[43.88, -78.90],
                   zoom_start=11, tiles="OpenStreetMap")

    for h in hospitals:
        alloc_v = int(vaccines * h["capacity_share"])
        alloc_b = int(beds * h["capacity_share"])
        alloc_t = int(treatments * h["capacity_share"])

        popup_text = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4>{h['name']}</h4>
            <hr>
            <b>Allocated Medical Assets:</b><br>
            • <b>Vaccines:</b> {alloc_v:,} doses<br>
            • <b>ICU Beds:</b> {alloc_b:,} units<br>
            • <b>Treatments:</b> {alloc_t:,} doses
        </div>
        """

        folium.Marker(
            location=[h["lat"], h["lon"]],
            popup=popup_text,
            tooltip=h["name"],
            icon=folium.Icon(
                color="red" if h["capacity_share"] >= 0.4 else "blue",
                icon="hospital-o",
                prefix="fa"
            )
        ).add_to(m)

    return m
