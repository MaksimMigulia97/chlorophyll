import pandas as pd
import plotly.graph_objects as go


def draw_graph(data, depth, selected_lat, selected_lon):
    fig = go.Figure()

    values_by_season = {
        "depth": depth
    }

    for season, file_path in data.items():
        df = pd.read_csv(file_path)
        selected_data = df[(df['lat'] == selected_lat) &
                           (df['lon'] == selected_lon)]
        values = []
        values.extend(selected_data['chlor'].tolist())
        values.extend(selected_data.iloc[:, 5:16].values.flatten().tolist())

        if not values:
            values = [0] * len(depth)

        values_by_season[season] = values

    df = pd.DataFrame(values_by_season)

    for season in data.keys():
        fig.add_trace(
            go.Scatter(
                x=df[season],
                y=depth,
                mode='lines',
                name=season,
                line_shape='spline'
            )
        )

    fig.update_layout(
        title="Chlorophyll concentration by the seasons and depth for last point",
        xaxis_title="Chlorophyll concentration (mg/m³)",
        yaxis_title="Depth (m)",
    )

    table_data = pd.DataFrame(values_by_season).round(4)

    array = [df[season].max() for season in data]
    max_value = max(array)
    fig.update_xaxes(range=[0, max_value + max_value*0.1], rangemode='tozero')
    return fig, table_data
