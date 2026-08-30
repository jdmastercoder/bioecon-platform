import folium


def generate_resource_map(vaccines, beds, treatments, peak_hospitalized=0):
    """
    Generates an interactive map with resource allocation markers and dynamic 
    ICU capacity risk radius overlays across regional facilities.
    """
    hospitals = [
        {"name": "Lakeridge Health Oshawa", "lat": 43.9033, "lon": -
            78.8683, "capacity_share": 0.45, "base_beds": 225},
        {"name": "Lakeridge Health Ajax Pickering", "lat": 43.8369,
            "lon": -79.0169, "capacity_share": 0.25, "base_beds": 125},
        {"name": "Lakeridge Health Whitby", "lat": 43.8765, "lon": -
            78.9430, "capacity_share": 0.15, "base_beds": 75},
        {"name": "Lakeridge Health Bowmanville", "lat": 43.9100,
            "lon": -78.6800, "capacity_share": 0.15, "base_beds": 75},
    ]

    m = folium.Map(location=[43.88, -78.90],
                   zoom_start=11, tiles="OpenStreetMap")

    for h in hospitals:
        alloc_v = int(vaccines * h["capacity_share"])
        alloc_b = int(beds * h["capacity_share"])
        alloc_t = int(treatments * h["capacity_share"])

        # Calculate local strain ratio
        local_demand = peak_hospitalized * h["capacity_share"]
        strain_ratio = local_demand / alloc_b if alloc_b > 0 else 1.0

        # Determine risk circle color and radius
        if strain_ratio >= 1.0:
            risk_color = "red"
            fill_opacity = 0.4
        elif strain_ratio >= 0.7:
            risk_color = "orange"
            fill_opacity = 0.3
        else:
            risk_color = "green"
            fill_opacity = 0.2

        radius_meters = min(5000, max(1500, int(strain_ratio * 2500)))

        # Add dynamic risk halo
        folium.Circle(
            location=[h["lat"], h["lon"]],
            radius=radius_meters,
            color=risk_color,
            fill=True,
            fill_color=risk_color,
            fill_opacity=fill_opacity,
            popup=f"Strain Level: {strain_ratio*100:.1f}% of ICU capacity"
        ).add_to(m)

        # Add facility marker
        popup_text = f"""
        <div style="font-family: Arial; width: 210px;">
            <h4>{h['name']}</h4>
            <hr>
            <b>Allocated Assets:</b><br>
            • <b>Vaccines:</b> {alloc_v:,}<br>
            • <b>ICU Beds:</b> {alloc_b:,}<br>
            • <b>Treatments:</b> {alloc_t:,}<br><br>
            <b>ICU Strain Ratio:</b> {strain_ratio:.2f}x
        </div>
        """

        folium.Marker(
            location=[h["lat"], h["lon"]],
            popup=popup_text,
            tooltip=h["name"],
            icon=folium.Icon(color="red" if strain_ratio >=
                             1.0 else "blue", icon="hospital-o", prefix="fa")
        ).add_to(m)

    return m
