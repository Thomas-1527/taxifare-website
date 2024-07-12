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

# Header and logo
st.image("https://path/to/your/logo.png", width=100)
st.title("TaxiFareModel Front")

st.markdown('''
## Enter the details of your ride:
''')

# Date and time input
pickup_date = st.date_input("Pickup Date", value=datetime.datetime.now().date())
pickup_time = st.time_input("Pickup Time", value=datetime.datetime.now().time())
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

# Coordinate inputs using sliders
pickup_longitude = st.slider("Pickup Longitude", min_value=-74.05, max_value=-73.75, value=-73.985428)
pickup_latitude = st.slider("Pickup Latitude", min_value=40.63, max_value=40.85, value=40.748817)
dropoff_longitude = st.slider("Dropoff Longitude", min_value=-74.05, max_value=-73.75, value=-73.985428)
dropoff_latitude = st.slider("Dropoff Latitude", min_value=40.63, max_value=40.85, value=40.748817)
passenger_count = st.number_input("Passenger Count", value=1, min_value=1, max_value=8)

# Map
st.markdown("### Pickup and Dropoff Locations")
m = folium.Map(location=[40.748817, -73.985428], zoom_start=12)
folium.Marker([pickup_latitude, pickup_longitude], tooltip='Pickup').add_to(m)
folium.Marker([dropoff_latitude, dropoff_longitude], tooltip='Dropoff').add_to(m)
folium_static(m)

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
response = requests.get(url, params=params).json()

# Display the prediction
st.write(f"Predicted Fare: ${response['fare']}")
