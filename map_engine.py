import folium
from streamlit_folium import st_folium


def generate_resource_map(vaccines, beds, treatments):
    """
    Generates an interactive map distributing optimized resources 
    across sample regional hospital centers.
    """
    # Sample coordinates for regional medical centers (e.g., Metro Area)
    hospitals = [
        {"name": "Central General Hospital",
            "lat": 40.7128, "lon": -74.0060, "share": 0.50},
        {"name": "Northside Health Center", "lat": 40.7831,
            "lon": -73.9712, "share": 0.30},
        {"name": "East Regional Clinic", "lat": 40.7484,
            "lon": -73.9857, "share": 0.20},
    ]

    # Initialize map centered on the region
    m = folium.Map(location=[40.75, -73.98],
                   zoom_start=12, tiles="OpenStreetMap")

    # Place interactive markers for each facility
    for h in hospitals:
        alloc_v = int(vaccines * h["share"])
        alloc_b = int(beds * h["share"])
        alloc_t = int(treatments * h["share"])

        popup_text = f"""
        <b>{h['name']}</b><br>
        • Vaccines Allocated: {alloc_v:,}<br>
        • ICU Beds Allocated: {alloc_b:,}<br>
        • Treatments Allocated: {alloc_t:,}
        """

        folium.Marker(
            location=[h["lat"], h["lon"]],
            popup=popup_text,
            tooltip=h["name"],
            icon=folium.Icon(
                color="red" if h["share"] >= 0.4 else "blue", icon="hospital", prefix="fa")
        ).add_to(m)

    return m
