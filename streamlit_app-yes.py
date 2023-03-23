import pandas as pd
import plotly.express as px
import streamlit as st

# Display title and text
st.title("Week 1 - Data and visualization")
st.markdown("Here we can see the dataframe created during this weeks project. Here are some of the steps we took to prep the data.")
st.subheader("")
st.markdown("**Preprocessed the Dataset**U+003A transposed, removed string characters, converted to a float to manipulate")
st.subheader("Converted from USD to Aregentine Pesos")
st.markdown("added 2022 inflation, corrected decimals")
st.subheader("Researched a desired location to visit")
st.markdown("added coordinates, calculate location from Airbnb")
st.subheader("Prepped the Dataset for Download")
st.markdown("added new column for location from Airbnb, color, and place to visit")
st.subheader("Created a Streamlit app")
st.markdown("used Pandas to format our dataframe, plotly for visuals and slider")

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
price_range = st.sidebar.slider('Max Price:', min_value=3000, max_value=18588, step=2000, value=18588)
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
st.markdown("Below is a map showing all the Airbnb listings with a blue dot and the location we've chosen with a red dot. Use the slider to adjust the price range.")

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
