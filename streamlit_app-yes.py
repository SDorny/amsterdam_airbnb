import pandas as pd
import plotly.express as px
import streamlit as st

# Display title and text
st.title("Amsterdam Airbnb")
st.subheading("Week 1- Data and Visualization")
st.markdown("The goal of this project was to become familiar with NumPy. More specifically, file input/output, computation on arrays, aggregation, and modifying arrays.")
st.subheading("Description")
st.markdown("The dataset includes Airbnb data from Amsterdam, the capital of the Netherlands. The data provided were the Airbnb Listing ID, Price, Latitude, and Longitude columns. Modifications were made to those columns in addition to creating two new columns for further analysis. These are Meters from chosen location and Location.")

# Read dataframe
dataframe = pd.read_csv(
    "WK1_Airbnb_Amsterdam_listings_proj_solution.csv",
    names=[
        "Airbnb Listing ID",
        "Price",
        "Latitude",
        "Longitude",
        "Meters from chosen location",
        "Location",
    ],
)

# Sidebar - title & filters
price_range = st.sidebar.slider('Max Price:', min_value=3000.00, max_value=18588.00, step=2000, value=18588)
price_range = int(price_range)
dataframe = dataframe[(dataframe['Price'] < price_range)]

# We have a limited budget, therefore we would like to exclude
# listings with a price above 100 pounds per night
dataframe = dataframe[dataframe["Price"] <= 18588.74]

# Display as integer
dataframe["Airbnb Listing ID"] = dataframe["Airbnb Listing ID"].astype(int)
# Round of values
dataframe["Price"] = "$ " + dataframe["Price"].round(2).astype(str) # <--- CHANGE THIS POUND SYMBOL IF YOU CHOSE CURRENCY OTHER THAN POUND
# Rename the number to a string
dataframe["Location"] = dataframe["Location"].replace(
    {1.0: "To visit", 0.0: "Airbnb listing"}
)

# Display dataframe and text
st.dataframe(dataframe)
st.markdown("Below is a map showing all the Airbnb listings with a blue dot and the location I've chosen with a red dot. Use the slider to adjust the price range.")

# Create the plotly express figure
fig = px.scatter_mapbox(
    dataframe,
    lat="Latitude",
    lon="Longitude",
    color="Location",
    color_discrete_sequence=["red", "blue"],
    zoom=11,
    height=500,
    width=800,
    hover_name="Price",
    hover_data=["Meters from chosen location", "Location"],
    labels={"color": "Locations"},
)
fig.update_geos(center=dict(lat=dataframe.iloc[0][2], lon=dataframe.iloc[0][3]))
fig.update_layout(mapbox_style="stamen-terrain")

# Show the figure
st.plotly_chart(fig, use_container_width=True)
