import pandas as pd


def crowd_match_score(crowd_index, preference):

    if preference == "Avoid Crowds":
        score = max(0, 10 - crowd_index)

    elif preference == "Balanced":
        score = 10 - abs(crowd_index - 5)

    else:
        score = 7

    return max(1, min(score, 10))


def budget_score(budget_per_day):

    # normalize assuming range 2000-15000
    min_budget = 2000
    max_budget = 15000

    score = 10 - ((budget_per_day - min_budget) / (max_budget - min_budget)) * 10
    return max(1, min(score, 10))


def compute_travel_scores(df, crowd_pref):

    df = df.copy()

    df["crowd_match"] = df["crowd_index_avg"].apply(
        lambda x: crowd_match_score(x, crowd_pref)
    )

    df["budget_score"] = df["budget_per_day_inr"].apply(budget_score)

    df["travel_score"] = (
        df["season_score"] * 0.4
        + df["crowd_match"] * 0.3
        + df["accessibility_score"] * 0.2
        + df["budget_score"] * 0.1
    )

    df["travel_score"] = (df["travel_score"] * 10).round(1)

    df = df.sort_values(by="travel_score", ascending=False)

    return df