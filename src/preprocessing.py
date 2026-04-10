# src/preprocessing.py
import pandas as pd

import json

# with open("public_lev_1/users.json") as f:
#     data = json.load(f)
# print(type(data))        # list or dict?
# print(data[0].keys()) 

# with open("public_lev_1/status.csv") as f:
#     data = pd.read_csv(f)
# print(type(data))        # list or dict?
# print(data.columns) 

# with open("public_lev_1/locations.json") as f:
#     data = json.load(f)
# print(type(data))        # list or dict?
# print(data[0].keys()) 


def load_json_as_df(path):
    with open(path) as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_and_merge_data():
    # Load datasets
    status = pd.read_csv("public_lev_1/status.csv")
    users = load_json_as_df("public_lev_1/users.json")
    locations = load_json_as_df("public_lev_1/locations.json")

    # Rename columns for consistency user_id -> CitizenID
    users = users.rename(columns={"user_id": "CitizenID"})
    locations = locations.rename(columns={"user_id": "CitizenID"})

    # Merge datasets step by step
    merged = status.merge(users, on="CitizenID", how="left")
    merged = merged.merge(locations, on="CitizenID", how="left")

    # drop duplicates, handle missing values
    merged = merged.drop_duplicates(subset=["CitizenID"])
    merged = merged.fillna("Unknown")

    return merged

if __name__ == "__main__":
    df = load_and_merge_data()
    print("Merged dataframe shape:", df.shape)
    print(df.head())

