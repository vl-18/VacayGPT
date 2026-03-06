## Put in the backend code
import streamlit as st
import pandas as pd

from services.data_loader import load_destinations
from services.filters import filter_destinations
from utils.helpers import get_month_from_date

st.set_page_config(page_title="Travel Recommender", layout="wide")

st.title("🌍 India Travel Recommender")
st.write("Find destinations based on travel dates and crowd preferences.")

# Load dataset
df = load_destinations()

# Sidebar inputs
st.sidebar.header("Travel Preferences")

start_date = st.sidebar.date_input("Travel Start Date")
end_date = st.sidebar.date_input("Travel End Date")

crowd_pref = st.sidebar.selectbox(
    "Crowd Preference",
    ["Avoid Crowds", "Balanced", "Don't Care"]
)

dest_type = st.sidebar.selectbox(
    "Destination Type (Optional)",
    ["Any"] + sorted(df["destination_type"].unique())
)

budget = st.sidebar.number_input(
    "Budget per day (Optional ₹)",
    min_value=0,
    value=0
)

# Convert budget input
if budget == 0:
    budget = None

# Run recommendation
if start_date and end_date:

    month = get_month_from_date(start_date)

    results = filter_destinations(
        df,
        month,
        crowd_pref,
        dest_type,
        budget
    )

    st.subheader("Recommended Destinations")

    if results.empty:
        st.warning("No destinations found for these preferences.")

    else:

        for _, row in results.iterrows():

            with st.container():

                col1, col2 = st.columns([3,1])

                with col1:
                    st.markdown(f"### {row['destination']}")
                    st.write(f"📍 {row['state']}")
                    st.write(f"Type: {row['destination_type']}")
                    st.write(f"Best Months: {', '.join(row['best_months'])}")

                with col2:
                    st.metric("Budget/day", f"₹{row['budget_per_day_inr']}")
                    st.metric("Crowd Index", row["crowd_index_avg"])

                st.divider()