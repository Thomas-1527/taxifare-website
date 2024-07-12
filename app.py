import streamlit as st
import requests
import datetime
import folium
from streamlit_folium import folium_static

# Style customization
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput, .stNumberInput {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Functions for geocoding and reverse geocoding
def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': address, 'format': 'json'}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Error: Unable to reach the geocoding service. Status code: {response.status_code}")
        return None, None
    data = response.json()
    if not data:
        st.error("Error: No results found for the given address.")
        return None, None
    return float(data[0]['lat']), float(data[0]['lon'])

def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {'lat': lat, 'lon': lon, 'format': 'json'}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Error: Unable to reach the reverse geocoding service. Status code: {response.status_code}")
        return None
    data = response.json()
    if not data:
        st.error("Error: No results found for the given coordinates.")
        return None
    return data['display_name']

# Header and logo
st.image("/home/thomas/code/Thomas-1527/taxifare-website/taxi.png", width=100)  # Assure-toi que 'logo.png' est dans le même répertoire que 'app.py'
st.title("TaxiFareModel Front")

st.markdown('''
## Enter the details of your ride:
''')

# Address input
pickup_address = st.text_input("Pickup Address", value="10 Downing St, Westminster, London SW1A 2AA, United Kingdom")
dropoff_address = st.text_input("Dropoff Address", value="Buckingham Palace, London SW1A 1AA, United Kingdom")

# Geocode the addresses
pickup_latitude, pickup_longitude = geocode(pickup_address)
dropoff_latitude, dropoff_longitude = geocode(dropoff_address)

if pickup_latitude is not None and dropoff_latitude is not None:
    # Display the coordinates
    st.write(f"Pickup coordinates: ({pickup_latitude}, {pickup_longitude})")
    st.write(f"Dropoff coordinates: ({dropoff_latitude}, {dropoff_longitude})")

    # Map
    st.markdown("### Pickup and Dropoff Locations")
    m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=12)
    folium.Marker([pickup_latitude, pickup_longitude], tooltip='Pickup').add_to(m)
    folium.Marker([dropoff_latitude, dropoff_longitude], tooltip='Dropoff').add_to(m)
    folium_static(m)

    # Date and time input
    pickup_datetime = st.date_input("Pickup Date", value=datetime.datetime.now().date())
    pickup_time = st.time_input("Pickup Time", value=datetime.datetime.now().time())
    pickup_datetime = datetime.datetime.combine(pickup_datetime, pickup_time)

    # Passenger count input
    passenger_count = st.number_input("Passenger Count", value=1, min_value=1, max_value=8)

    # Call the API
    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Error: Unable to reach the prediction API. Status code: {response.status_code}")
    else:
        data = response.json()
        st.write(f"Predicted Fare: ${data['fare']}")
else:
    st.error("Geocoding failed. Please check the addresses and try again.")
