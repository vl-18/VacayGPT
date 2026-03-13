## Put in the backend code
import streamlit as st
import pandas as pd

from services.data_loader import load_destinations
from services.filters import filter_destinations
from utils.helpers import get_month_from_date
from services.ranking import compute_travel_scores

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
    ranked_results = compute_travel_scores(results, crowd_pref)

st.subheader("Top Travel Recommendations")

top_results = ranked_results.head(10)

for _, row in top_results.iterrows():

    with st.container():

        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.markdown(f"### {row['destination']}")
            st.write(f"📍 {row['state']}")
            st.write(f"Type: {row['destination_type']}")

        with col2:
            st.metric("Travel Score", f"{row['travel_score']}/100")

        with col3:
            st.metric("Budget/day", f"₹{row['budget_per_day_inr']}")

        st.progress(row["travel_score"] / 100)

        with st.expander("ℹ️ Why this score?"):

            st.write("Score Breakdown")

            st.write(f"Season suitability: {row['season_score']}/10")
            st.write(f"Crowd match: {row['crowd_match']}/10")
            st.write(f"Accessibility: {row['accessibility_score']}/10")
            st.write(f"Budget friendliness: {row['budget_score']:.1f}/10")

            st.write("⚠ Factors lowering the score:")

            for p in row["penalties"]:
                st.write(f"- {p}")

        st.divider()


# st.subheader("Top Travel Recommendations")

# top_results = ranked_results.head(10)

# for _, row in top_results.iterrows():

#     with st.container():

#         col1, col2, col3 = st.columns([3,1,1])

#         with col1:
#             st.markdown(f"### {row['destination']}")
#             st.write(f"📍 {row['state']}")
#             st.write(f"Type: {row['destination_type']}")

#         with col2:
#             st.metric("Travel Score", f"{row['travel_score']}/100")

#         with col3:
#             st.metric("Budget/day", f"₹{row['budget_per_day_inr']}")

#         st.progress(row["travel_score"] / 100)

#         st.divider()
    # st.subheader("Recommended Destinations")

    # if results.empty:
    #     st.warning("No destinations found for these preferences.")

    # else:

    #     for _, row in results.iterrows():

    #         with st.container():

    #             col1, col2 = st.columns([3,1])

    #             with col1:
    #                 st.markdown(f"### {row['destination']}")
    #                 st.write(f"📍 {row['state']}")
    #                 st.write(f"Type: {row['destination_type']}")
    #                 st.write(f"Best Months: {', '.join(row['best_months'])}")

    #             with col2:
    #                 st.metric("Budget/day", f"₹{row['budget_per_day_inr']}")
    #                 st.metric("Crowd Index", row["crowd_index_avg"])

    #             st.divider()