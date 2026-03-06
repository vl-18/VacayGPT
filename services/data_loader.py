import pandas as pd

def load_destinations():
    df = pd.read_csv("data/destinations.csv")

    # convert month strings to list
    df["best_months"] = df["best_months"].str.replace('"','').str.split(",")
    df["worst_months"] = df["worst_months"].str.replace('"','').str.split(",")
    df["crowd_peak_months"] = df["crowd_peak_months"].str.replace('"','').str.split(",")

    # convert offbeat to boolean
    df["offbeat"] = df["offbeat"].astype(bool)

    return df