import pandas as pd


data = {
    "autumn": "data/merged_august.csv",
    "summer": "data/merged_june.csv",
    "spring": "data/merged_march.csv",
    "winter": "data/merged_january.csv",
}

stale_data = {
    "depth": [-50, -100, -150, -200, -250, -300, -350, -400, -450, -500],
    "autumn": [1.2, 1.7, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "winter": [1.1, 1.5, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "spring": [1.2, 1.6, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "summer": [1.2, 1.8, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
}

now = "spring"

autumn_data = pd.read_csv(data[now])

for depth in stale_data["depth"]:
    col_name = str(depth)
    autumn_data[col_name] = 0.0

for i, depth in enumerate(stale_data["depth"]):
    coefficient = stale_data[now][i]
    col_name = str(depth)
    if col_name in autumn_data.columns:
        autumn_data.loc[autumn_data["depth"] <= depth, col_name] = autumn_data[autumn_data["depth"] <= depth]["chlor"] * coefficient


out = f"final_data/{now}.csv"
autumn_data.to_csv(out, index=False)
