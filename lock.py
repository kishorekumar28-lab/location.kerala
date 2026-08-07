import folium
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2

# =====================================================
# PATIENT INFORMATION
# =====================================================

patient = {
    "name": "Rahul",
    "condition": "Pneumonia",      # Change this condition
    "lat": 11.2588,                # Patient Latitude
    "lon": 75.7804                 # Patient Longitude
}

# =====================================================
# DISEASE -> SPECIALIST
# =====================================================

conditions = {
    "Fibrosis": "Pulmonologist",
    "Hernia": "General Surgeon",
    "Infiltration": "Pulmonologist",
    "Mass": "Medical Oncologist",
    "No Finding": "General Physician",
    "Nodule": "Pulmonologist",
    "Pleural Thickening": "Pulmonologist",
    "Pneumonia": "Pulmonologist",
    "Pneumothorax": "Emergency Medicine"
}

# =====================================================
# HOSPITAL DATABASE
# =====================================================

hospitals = [

    {
        "name":"Amrita Hospital",
        "city":"Kochi",
        "lat":10.0315,
        "lon":76.3082,
        "specialties":[
            "Pulmonologist",
            "Medical Oncologist",
            "Thoracic Surgeon",
            "General Surgeon",
            "Emergency Medicine"
        ]
    },

    {
        "name":"Aster Medcity",
        "city":"Kochi",
        "lat":10.0481,
        "lon":76.2766,
        "specialties":[
            "Pulmonologist",
            "Thoracic Surgeon",
            "General Surgeon",
            "Emergency Medicine"
        ]
    },

    {
        "name":"KIMSHEALTH",
        "city":"Thiruvananthapuram",
        "lat":8.5241,
        "lon":76.9366,
        "specialties":[
            "Pulmonologist",
            "Emergency Medicine"
        ]
    },

    {
        "name":"Rajagiri Hospital",
        "city":"Kochi",
        "lat":10.0158,
        "lon":76.3644,
        "specialties":[
            "Pulmonologist",
            "General Surgeon",
            "Emergency Medicine"
        ]
    },

    {
        "name":"Baby Memorial Hospital",
        "city":"Kozhikode",
        "lat":11.2588,
        "lon":75.7804,
        "specialties":[
            "Pulmonologist",
            "Emergency Medicine"
        ]
    },

    {
        "name":"Regional Cancer Centre",
        "city":"Thiruvananthapuram",
        "lat":8.5206,
        "lon":76.9284,
        "specialties":[
            "Medical Oncologist",
            "Thoracic Surgeon"
        ]
    },

    {
        "name":"Malabar Cancer Centre",
        "city":"Kannur",
        "lat":11.8745,
        "lon":75.4838,
        "specialties":[
            "Medical Oncologist",
            "Thoracic Surgeon"
        ]
    },

    {
        "name":"Govt Medical College TVM",
        "city":"Thiruvananthapuram",
        "lat":8.5237,
        "lon":76.9289,
        "specialties":[
            "Emergency Medicine",
            "Pulmonologist",
            "General Surgeon"
        ]
    }

]

# =====================================================
# DISTANCE FUNCTION
# =====================================================

def distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2

    c = 2*atan2(sqrt(a),sqrt(1-a))

    return R*c

# =====================================================
# REQUIRED SPECIALIST
# =====================================================

specialist = conditions[patient["condition"]]

print("Condition :", patient["condition"])
print("Required Specialist :", specialist)

# =====================================================
# CREATE MAP
# =====================================================

m = folium.Map(
    location=[patient["lat"],patient["lon"]],
    zoom_start=7
)

# =====================================================
# PATIENT MARKER
# =====================================================

folium.Marker(
    [patient["lat"],patient["lon"]],
    tooltip="Patient",
    popup=f"""
    <b>Patient</b><br>
    Condition: {patient['condition']}<br>
    Required: {specialist}
    """,
    icon=folium.Icon(color="red",icon="plus")
).add_to(m)

# =====================================================
# SEARCH HOSPITALS
# =====================================================

nearest = None
nearest_distance = 999999

for hospital in hospitals:

    if specialist in hospital["specialties"]:

        km = distance(
            patient["lat"],
            patient["lon"],
            hospital["lat"],
            hospital["lon"]
        )

        if km < nearest_distance:
            nearest_distance = km
            nearest = hospital

        popup = f"""
        <h3>{hospital['name']}</h3>
        City : {hospital['city']}<br>
        Specialist : {specialist}<br>
        Distance : {km:.2f} km
        """

        folium.Marker(
            [hospital["lat"],hospital["lon"]],
            popup=popup,
            tooltip=hospital["name"],
            icon=folium.Icon(color="green",icon="hospital-o",prefix="fa")
        ).add_to(m)

# =====================================================
# DRAW ROUTE TO NEAREST HOSPITAL
# =====================================================

if nearest:

    folium.PolyLine(
        [
            [patient["lat"],patient["lon"]],
            [nearest["lat"],nearest["lon"]]
        ],
        color="blue",
        weight=5
    ).add_to(m)

    print("\nNearest Hospital")
    print(nearest["name"])
    print(nearest_distance,"km")

# =====================================================
# SAVE MAP
# =====================================================

m.save("Medical_Intelligence_Map.html")

webbrowser.open(
    "file://" + os.path.abspath("Medical_Intelligence_Map.html")
)

print("\nMap Generated Successfully")