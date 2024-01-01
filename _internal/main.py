import plotly.graph_objects as go
import pandas as pd
import dash
import json
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import callback_context
import webbrowser
from dash.exceptions import PreventUpdate

# Local
from draw import draw_graph
from utils import get_info_and_table_data
from constants import data, depth, options, MAX_POINTS, columns


initial_df = pd.read_csv(data["August 2023"])

app = dash.Dash(__name__)
point_plot_figure = go.FigureWidget()

app.layout = html.Div([
    dcc.Dropdown(
        id='dataset-dropdown',
        options=options,
    ),
    html.Div([
    dcc.Graph(
        id='map-graph',
        style={
            'width': '90%',
            'height': '500px',
            'margin': '0 auto',
        }
    ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'margin': 'auto'}
    ), 
    html.Div([
    dcc.Graph(
        id='map-graph-color',
        style={
            'width': '90%',
            'height': '500px',
            'margin': '0 auto',
        }
    ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'margin': 'auto'}
    ),
    
    html.Div([
        dash_table.DataTable(
            id='selected-point-table-data-1',
            style_table={
                'height': '100%',
                'overflowY': 'auto',
                'width': '100%',
                'margin': 'auto',
                'margin-top': '20px',
            },
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal'},
            columns=[
                {'name': 'Data', 'id': 'Data'},
                {'name': 'Value', 'id': 'Value'},
            ],
            data=[],
        ),
        dash_table.DataTable(
            id='selected-point-table-depth-1',
            style_table={
                'height': '100%',
                'overflowY': 'auto',
                'width': '100%',
                'margin': 'auto',
                'margin-left': '20px',
                'margin-top': '20px',
            },
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal'},
            columns=columns,
            data=[],
        ),
        dash_table.DataTable(
            id='selected-point-table-data-2',
            style_table={
                'height': '100%',
                'overflowY': 'auto',
                'width': '100%',
                'margin': 'auto',
                'margin-top': '20px',
                'margin-left': '40px',
            },
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal'},
            columns=[
                {'name': 'Data', 'id': 'Data'},
                {'name': 'Value', 'id': 'Value'},
            ],
            data=[],
        ), 
        dash_table.DataTable(
            id='selected-point-table-depth-2',
            style_table={
                'height': '100%',
                'overflowY': 'auto',
                'width': '100%',
                'margin': 'auto',
                'margin-left': '60px',
                'margin-top': '20px',
            },
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal'},
            columns=columns,
            data=[],
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '54%', 'margin': 'auto'}),
    
    dcc.Graph(
        figure=point_plot_figure,
        id='point-plot',
        style={
            'width': '80%',
            'margin': '0 auto'
        }
    ),
    html.Div([
        dash_table.DataTable(
            id='compare-table',
            style_table={
                'height': '100%',
                'overflowY': 'auto',
                'width': '100%',
                'margin': 'auto',
                'margin-top': '20px',
            },
            style_cell={'textAlign': 'left'},
            style_data={'whiteSpace': 'normal'},
            columns=[
                {'name': 'Latitude (°)', 'id': 'lat'},
                {'name': 'Longitude (°)', 'id': 'lon'},
                {'name': 'Depth max (m)', 'id': 'depth'},
                {'name': 'Chlorophyll concentration (mg/m³)', 'id': 'chlor'},
                {'name': 'Temperature (°C)', 'id': 'temp'},
            ],
            data=[],
        ),
    ], style={'width': '60%', 'margin': 'auto'}
    )
])

selected_points = []
click_data_store = []

table_store = []


@app.callback(
    Output('map-graph', 'figure'),
    [Input('dataset-dropdown', 'value'),
     Input('map-graph', 'clickData')]
)
def update_graph(selected_dataset, click_data_for_color_change):

    if not callback_context.triggered_id:
        selected_points.clear()
        click_data_store.clear()
        click_data_for_color_change.clear()
        table_store.clear()
        print(("here"), selected_points, click_data_store, click_data_for_color_change)
        raise PreventUpdate

    df = pd.read_csv(selected_dataset)

    fig = go.Figure(go.Scattergeo(
        lat=df.lat,
        lon=df.lon,
        mode='markers',
        marker=dict(
            size=5,
            cmin=0,
            cmax=5,
            color=df.chlor,
            colorbar=dict(title='Chlorophyll concentration (mg/m³))'),
            colorscale='Viridis',
            showscale=True,
        ),
        text=df[
            ['lat', 'lon', 'depth', 'chlor', 'temp']
        ].apply(
            lambda x: f'Lat: {x[0]}, Lon: {x[1]}, Depth: {x[2]}, Chlor: {x[3]}, Temp: {x[4]}',
            axis=1
        )
    )
    )

    if click_data_for_color_change:
        new_colors = []
        for lat, lon, chlor_value in zip(df.lat, df.lon, df.chlor):
            if any(d['lat'] == lat and d['lon'] == lon for d in click_data_for_color_change):
                new_colors.append('red')
            else:
                new_colors.append(chlor_value)

        fig.update_traces(marker=dict(color=new_colors))
    
    fig.update_yaxes(range=[0, 5], title='Chlorophyll')
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        autosize=True,
    )
    return fig


@app.callback(
    [Output('point-plot', 'figure'),
     Output('map-graph-color', 'figure'),
     Output('selected-point-table-data-1', 'data'),
     Output('selected-point-table-data-2', 'data'),
     Output('selected-point-table-depth-1', 'data'),
     Output('selected-point-table-depth-2', 'data'),
     Output('compare-table', 'data')],
    [Input('map-graph', 'clickData'),
     Input('dataset-dropdown', 'value')]
)
def display_selected_point(click_data, selected_dataset):
    if click_data is None:
        return go.Figure(), "No selected point", pd.DataFrame()

    selected_lat = click_data['points'][0]['lat']
    selected_lon = click_data['points'][0]['lon']

    fig, df_table = draw_graph(data, depth, selected_lat, selected_lon)
    selected_info_text = click_data['points'][0]['text']
    point_data = selected_info_text.split(',')

    numeric_values = clear_point_data(point_data)

    add_point(*numeric_values)
    add_point_cord(selected_lat, selected_lon)
    table_data_dict = get_info_and_table_data(selected_info_text).to_dict('records')
    df_table_dict = df_table.to_dict('records')
    compare_data = get_selected_points()
    click_data_for_color_change = get_selected_points_cord()
    updated_figure = update_graph(selected_dataset, click_data_for_color_change)
    add_table_data(table_data_dict, df_table_dict)
    table_data_dict = pd.DataFrame(table_store).to_dict('records')

    table_point_1 = pd.DataFrame(
        table_data_dict[0]['point_data']
        ).to_dict('records')
    table_depth_1 = pd.DataFrame(
        table_data_dict[0]['table_data']
        ).to_dict('records')
    if not len(compare_data) >= 2:
        table_point_2, table_depth_2 = [], []
        return fig, updated_figure, table_point_1, table_point_2, table_depth_1, table_depth_2, compare_data
    else:
        table_point_2 = pd.DataFrame(
            table_data_dict[1]['point_data']
            ).to_dict('records')
        table_depth_2 = pd.DataFrame(
            table_data_dict[1]['table_data']
            ).to_dict('records')
        return fig, updated_figure, table_point_1, table_point_2, table_depth_1, table_depth_2, compare_data


def clear_point_data(point_data):
    numeric_values = []

    for item in point_data:
        value_str = ''.join(
            char for char in item if char.isdigit() or char in ('.', '-'))
        if value_str:
            numeric_values.append(float(value_str))
    return numeric_values


def add_point(lat, lon, depth, chlor, temp):
    point_data = {
        'lat': lat,
        'lon': lon,
        'depth': depth,
        'chlor': chlor,
        'temp': temp,
    }

    if len(selected_points) >= MAX_POINTS:
        selected_points.pop(0)

    selected_points.append(point_data)


def add_point_cord(lat, lon):
    point_data_cord = {
        'lat': lat,
        'lon': lon,
    }

    if len(click_data_store) >= MAX_POINTS:
        click_data_store.pop(0)

    click_data_store.append(point_data_cord)


def add_table_data(table_data_dict, df_table_dict):
    table_data = {
        'point_data': table_data_dict,
        'table_data': df_table_dict
    }

    if len(table_store) >= MAX_POINTS:
        table_store.pop(0)

    table_store.append(table_data)


def get_selected_points():
    return selected_points


def get_selected_points_cord():
    return click_data_store


def update_point_colors(click_data_for_color_change, current_figure):
    updated_figure = current_figure

    scatter = updated_figure['data'][0]
    latitudes = scatter['lat']
    longitudes = scatter['lon']
    indexes_to_update = [
        i for i, point in enumerate(click_data_for_color_change)
        if 'color' in point
    ]

    for index in indexes_to_update:
        latitudes[index] = click_data_for_color_change[index]['lat']
        longitudes[index] = click_data_for_color_change[index]['lon']
    return updated_figure

def browser_open():
    website_url = "http://127.0.0.1:8050"
    webbrowser.open(website_url)


if __name__ == '__main__':
    browser_open()
    app.run_server(debug=False)
