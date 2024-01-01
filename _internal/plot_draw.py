import pandas as pd
import plotly.graph_objects as go

data = {
    "autumn": "final_data/autumn.csv",
    "summer": "final_data/summer.csv",
    "spring": "final_data/spring.csv",
    "winter": "final_data/winter.csv",
}

depth = [0, -50, -100, -150, -200, -250, -300, -350, -400, -450, -500]

selected_lat = 51.5
selected_lon = -131.5

fig = go.Figure()

values_by_season = {
    "depth": [0, -50, -100, -150, -200, -250, -300, -350, -400, -450, -500]
}

for season, file_path in data.items():
    df = pd.read_csv(file_path)
    selected_data = df[(df['lat'] == selected_lat) & (df['lon'] == selected_lon)]
    values = []
    values.extend(selected_data['chlor'].tolist())
    values.extend(selected_data.iloc[:, 5:16].values.flatten().tolist())

    if not values:
        values = [0] * len(depth)

    values_by_season[season] = values

print(values_by_season)
df = pd.DataFrame(values_by_season)

for season in data.keys():
    fig.add_trace(go.Scatter(x=df[season], y=depth, mode='lines', name=season, line_shape='spline'))

fig.update_layout(
    title="График хлора по глубине для разных сезонов",
    xaxis_title="Значения хлора",
    yaxis_title="Глубина",
)

array = []
array.append(df["autumn"].max())
array.append(df["summer"].max())
array.append(df["spring"].max())
array.append(df["winter"].max())

max_value = max(array)

fig.update_xaxes(range=[0, max_value + 1], rangemode='tozero')

fig.show()
