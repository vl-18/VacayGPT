def filter_destinations(df, month, crowd_pref, dest_type=None, budget=None):

    filtered = df.copy()

    # Filter by best travel months
    filtered = filtered[filtered["best_months"].apply(lambda x: month in x)]

    # Crowd preference logic
    if crowd_pref == "Avoid Crowds":
        filtered = filtered[filtered["crowd_index_avg"] <= 5]

    elif crowd_pref == "Balanced":
        filtered = filtered[filtered["crowd_index_avg"] <= 7]

    # Optional destination type
    if dest_type and dest_type != "Any":
        filtered = filtered[filtered["destination_type"] == dest_type]

    # Optional budget filter
    if budget:
        filtered = filtered[filtered["budget_per_day_inr"] <= budget]

    return filtered