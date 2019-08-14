import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2("U.S. National Parks",
            style={"text-align": "center"}),
    dcc.Graph(
        id='map',
        style={
            "margin": "0px calc(100% / 8)",
        }
    ),
    html.Div([
        html.Label('Year Selector', style={"text-align": "center"}),
        dcc.Slider(
            id='year-slider',
            min=2009,
            max=2018,
            value=2018,
            marks={str(year): str(year) for year in range(2009, 2019)},
            step=None
        )
    ], style={
        "width": "50%",
        "margin": "0 auto",
    }),
    html.Div([
        html.Label('Statistic Selector', style={"text-align": "center"}),
        dcc.Dropdown(
            id="stat_selector",
            options=[
                {'label': 'Size of Park', 'value': 'Gross Area Acres'},
                {'label': u'Number of Visitors', 'value': 'Value'},
            ],
            value='Gross Area Acres',
            style={
                "label": "Dropdown",
                "width": "80%",
                "margin": "0 auto",
            })
    ], style={
        "width": "50%",
        "margin": "0 auto",
        "padding-top": "30px"
    }),

])


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='year-slider', component_property='value'),
     Input(component_id='stat_selector', component_property='value')]
)
def update_output_div(year_selector, stat_selector):
    df = pd.read_csv(f'./data/merged_data/merged_data_{year_selector}.csv', thousands=',')

    if stat_selector == "Value":
        size = df[stat_selector] / 10000
        color_label = "Visitors"
    else:
        size = df[stat_selector] / 1000
        color_label = stat_selector

    df['text'] = "Park: " + df['ParkName'] + "\n" + color_label + ": " + df[stat_selector].astype(str)

    return {
        'data': [go.Scattergeo(
            locationmode='USA-states',
            lon=df['longitude'],
            lat=df['latitude'],
            text=df['text'],
            marker=dict(
                size=size,
                color=df[stat_selector],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
                colorbar=dict(
                    title=color_label
                ),
                colorscale="Hot"
            ),
        )],
        'layout': go.Layout(
            geo_scope='usa',
            hovermode='closest',
            height=700,
            autosize=True,
            margin=go.layout.Margin(
                l=0,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
