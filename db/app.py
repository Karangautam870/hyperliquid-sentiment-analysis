import streamlit as st
import db_helper as DB

db = DB.DB()


st.sidebar.title("Flights Analytics")
user_ops = st.sidebar.selectbox(
    "Navigation", ["Select Below", "Check Flights", "Analytics"])

if user_ops == "Select Below":
    st.title("Please select an option from the sidebar.")

elif user_ops == "Check Flights":
    st.title("Check Flights")
    cities = db.fetch_cities()

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Source city",
            cities,
            index=None,
            placeholder="Select source city"
        )

    with col2:
        destination = st.selectbox(
            "Destination city",
            cities,
            index=None,
            placeholder="Select destination city"
        )

    # Validation
    if source is None or destination is None:
        st.warning("Please select both source and destination.")
    elif source == destination:
        st.error("Source and destination must be different.")
    else:
        st.success(f"Searching flights from {source} to {destination}...")
    if st.button("Search Flights"):
        ans = db.fetch_flights(source, destination)
        description_row = ["Airline,Route, Dep_Time, Duration,Price"]
        st.dataframe(description_row+ans)

elif user_ops == "Analytics":
    st.title("Analytics")
else:
    pass
