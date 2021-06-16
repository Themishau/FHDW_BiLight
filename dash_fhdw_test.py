# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from plot_data import BI_Data

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 15000)
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "RheinBergGalerie Dashboard"

colors = {
    'background': '#082255',
    'bg2': "#082255",
    "graph_line": "#E2A012",
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

data = BI_Data()

# data = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        #header
        html.Div (
            [
                html.Div (
                    [

                    html.H4("BI-Light", className='app__header__title'),
                    html.P(
                        "Diese app sendet SQL-Anfragen zu gescannten QR-Codes.",
                        className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("FHDW_Logo.png"),
                            className="app__menu__img",
                        )
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # qr-codes_live
                html.Div(
                    [
                        html.Div(
                            [html.H6("QR-Codes pro Stunde", className="graph__title")]
                        ),
                        # Graph zu QR-Codes
                        dcc.Graph(
                            id="qr-code-live",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=colors["background"],
                                    paper_bgcolor=colors["background"],
                                )
                            ),
                        ),
                        # Infos zu Interval
                        dcc.Interval(
                            id="qr-code-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                        # benefit_2
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Meist eingelöste Benefits", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="benefit-last-eingeloest_2",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=colors["background"],
                                            paper_bgcolor=colors["background"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container left_second",
                        ),
                    ],
                    className="two-thirds column qr_code_live_container",
                ),
                html.Div(
                    [
                        # Live Ticker (Histogram)
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Week Live Ticker",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            id="bin-slider",
                                            min=1,
                                            max=100,
                                            step=1,
                                            value=20,
                                            updatemode="drag",
                                            marks={
                                                20: {"label": "20"},
                                                40: {"label": "40"},
                                                60: {"label": "60"},
                                                80: {"label": "80"},
                                            },
                                        )
                                    ],
                                    className="slider",
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="bin-auto",
                                            options=[
                                                {"label": "Auto", "value": "Auto"}
                                            ],
                                            value=["Auto"],
                                            inputClassName="auto__checkbox",
                                            labelClassName="auto__label",
                                        ),
                                        html.P(
                                            "# of Bins: Auto",
                                            id="bin-size",
                                            className="auto__p",
                                        ),
                                    ],
                                    className="auto__container",
                                ),
                                dcc.Graph(
                                    id="week-update-histogram",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=colors["background"],
                                            paper_bgcolor=colors["background"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # benefit
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Meist eingelöste Benefits", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="benefit-last-eingeloest",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=colors["background"],
                                            paper_bgcolor=colors["background"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + now.second
    return total_time

@app.callback(
    Output("qr-code-live", "figure"), [Input("qr-code-update", "n_intervals")]
)
def generate_qr_code_graph(interval):
    """
    genrates graph with qr_code_count
    :param interval: update the graph based on an interval
    :return:
    """
    data.refresh_data()
    data.qr_code_df['hour'] = data.qr_code_df['Timestamp'].dt.hour
    data.qr_code_df['day'] = data.qr_code_df['Timestamp'].dt.day
    data.qr_code_df['month'] = data.qr_code_df['Timestamp'].dt.month
    df_count = data.qr_code_df.groupby(['hour']).size().reset_index(name='counts')
    print(df_count)
    now = dt.datetime.now()
    trace = dict(
        type="bar",
        x=df_count['hour'],
        y=df_count['counts'],
        line={"color": "#E2A012"},
        hoverinfo="skip",
        mode="lines",
    )
    layout = dict(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font={"color": "#E2A012"},
        height=700,
        xaxis={
            "range": [8, 22],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
            "ticktext": ["8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"],
            "title": "Uhrzeit",
        },
        yaxis={
            "range": [
                min(0, min(df_count['counts'])),
                max(100, max(df_count['counts']) + max(df_count['counts'])),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": colors["graph_line"],
            "nticks": df_count['counts'],
        },
    )

    return dict(data=[trace], layout=layout)

@app.callback(
    Output("benefit-last-eingeloest", "figure"), [Input("qr-code-update", "n_intervals")]
)
def generate_benefits_graph(interval):
    """
    :param interval:
    :return:
    """

    df_count_benefits = data.bi_light_df.groupby(['Benefit']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
    trace = dict(
        type="pie",
        names=df_count_benefits['Benefit'],
        values=df_count_benefits['counts'],
        text=df_count_benefits['Benefit'],
        textposition='inside',
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )
    # trace = dict(
    #     type="bar",
    #     x=df_count_benefits['Benefit'],
    #     y=df_count_benefits['counts'],
    #     line={"color": "#42C4F7"},
    #     hoverinfo="skip",
    #     mode="lines",
    # )

    layout = dict(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        height=600,
        font={"color": "#fff"}
    )

    return dict(data=[trace], layout=layout)

@app.callback(
    Output("benefit-last-eingeloest_2", "figure"), [Input("qr-code-update", "n_intervals")]
)
def generate_benefits_graph(interval):
    """
    :param interval:
    :return:
    """

    df_count_benefits = data.bi_light_df.groupby(['Benefit']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
    # trace = dict(
    #     type="pie",
    #     names=df_count_benefits['Benefit'],
    #     values=df_count_benefits['counts'],
    #     text=df_count_benefits['Benefit'],
    #     textposition='inside',
    #     line={"color": "#42C4F7"},
    #     hoverinfo="skip",
    #     mode="lines",
    # )
    trace = dict(
        type="bar",
        x=df_count_benefits['Benefit'],
        y=df_count_benefits['counts'],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font={"color": "#fff"}
    )

    return dict(data=[trace], layout=layout)
    # return dict(data=df_count_benefits.to_dict('series'), layout=layout)

@app.callback(
    Output("week-update-histogram", "figure"),
    [Input("qr-code-update", "n_intervals")],
    [
        State("qr-code-live", "figure"),
        State("bin-slider", "value"),
        State("bin-auto", "value"),
    ],
)
def gen_wind_histogram(interval, qr_code_live_figure, slider_value, auto_state):
    """
    Genererate wind histogram graph.
    :params interval: update the graph based on an interval
    :params qr_code_live_figure: derzeitige Einlösung aller Benefits
    :params slider_value: current slider value
    :params auto_state: current auto state
    """
    qr_code_value = []
    data.qr_code_df['hour'] = data.qr_code_df['Timestamp'].dt.hour
    data.qr_code_df['day'] = data.qr_code_df['Timestamp'].dt.day
    data.qr_code_df['month'] = data.qr_code_df['Timestamp'].dt.month
    df_count = data.qr_code_df.groupby(['day']).size().reset_index(name='counts')
    try:
        # Check to see whether wind-speed has been plotted yet
        if qr_code_live_figure is not None:
            qr_code_value = qr_code_live_figure["data"][0]["y"]
        if "Auto" in auto_state:
            bin_val = np.histogram(
                qr_code_value,
                bins=range(int(round(min(qr_code_value))), int(round(max(qr_code_value)))),
            )
        else:
            bin_val = np.histogram(qr_code_value, bins=slider_value)
    except Exception as error:
        raise PreventUpdate

@app.callback(
    Output("bin-auto", "value"),
    [Input("bin-slider", "value")],
    [State("qr-code-live", "figure")],
)
def deselect_auto(slider_value, qr_code_live_figure):
    """ Toggle the auto checkbox. """

    # prevent update if graph has no data
    if "data" not in qr_code_live_figure:
        raise PreventUpdate
    if not len(qr_code_live_figure["data"]):
        raise PreventUpdate

    if qr_code_live_figure is not None and len(qr_code_live_figure["data"][0]["y"]) > 5:
        return [""]
    return ["Auto"]

@app.callback(
    Output("bin-size", "children"),
    [Input("bin-auto", "value")],
    [State("bin-slider", "value")],
)
def show_num_bins(autoValue, slider_value):
    """ Display the number of bins. """

    if "Auto" in autoValue:
        return "# of Bins: Auto"
    return "# of Bins: " + str(int(slider_value))

def start_app():
    app.run_server(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    start_app()

