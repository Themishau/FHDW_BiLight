# -*- coding: utf-8 -*-
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
from scipy.stats import rayleigh

# init BI_Data
data = BI_Data()
print("BI-Light am {}, {}.{}".format(data.today_data.weekday.values[0], data.today_data.today.values[0], data.today_data.month.values[0]))

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "RheinBergGalerie Dashboard"

colors = {
    'background': '#082255',
    'bg2': "#082255",
    "graph_line": "#E2A012",
    "graph_bg": "#E2A012",
    'text': '#7FDBFF'
}



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        #header
        html.Div (
            [
                html.Div (
                    [

                    html.H4("BI-Light am {}, {}.{}".format(data.today_data.weekday.values[0], data.today_data.today.values[0], data.today_data.month.values[0]), className='app__header__title'),
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
                            [
                                html.H6(
                                    "QR-Codes am {}, {}.{}".format(data.today_data.weekday.values[0], data.today_data.today.values[0], data.today_data.month.values[0]), className="graph__title"
                                )
                            ]
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
                            #interval=3600000.0,
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                        # benefit_2
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Meist eingelöste Benefits am {}, {}.{}".format(data.today_data.weekday.values[0], data.today_data.today.values[0], data.today_data.month.values[0]), className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="benefit-last-eingeloest_today",
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
                                            "Daily Live Ticker",
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
                                            "Meist eingelöste Benefits insgesamt", className="graph__title"
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
    :param n_intervals:
    :param interval: update the graph based on an interval
    :return:
    """
    try:
        data.refresh_data()

        # korrekte umsetzung
        data.qr_code_pro_stunde_heute()
        df_count = data.qr_code_pro_stunde

        # data.qr_code_df['hour'] = data.qr_code_df['Timestamp'].dt.hour
        # data.qr_code_df['day'] = data.qr_code_df['Timestamp'].dt.day
        # data.qr_code_df['month'] = data.qr_code_df['Timestamp'].dt.month
        # df_count = data.qr_code_df.groupby(['hour']).size().reset_index(name='counts')

        trace = dict(
            type="bar",
            mode='bar',
            text=df_count['counts'],
            text_color='#ffffff',
            textposition='inside',
            x=df_count['hour'],
            y=df_count['counts'],
            colors='#ffffff',
            line={"color": "#ffffff"},
            hoverinfo="skip",
            marker=dict(color='#FF6C00'),
            marker_line_width=1.5,
            opacity=0.9
        )
        layout = dict(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": "#ffffff"},
            marker_color= "#ffffff",
            height=700,
            xaxis={
                "range": [4.5, 22.5],
                "showline": True,
                "zeroline": False,
                "fixedrange": True,
                "tickvals": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                "ticktext": ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],
                "title": "Uhrzeit",
            },
            yaxis={
                "range": [
                    min(0, min(df_count['counts'])),
                    max(100, max(df_count['counts']) + 50),
                ],
                "showgrid": True,
                "showline": True,
                "fixedrange": True,
                "zeroline": False,
                "gridcolor": "#ffffff",
                "nticks": df_count['counts']
            },
        )
    except AttributeError:
        raise PreventUpdate
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
        labels=df_count_benefits['Benefit'],
        showlegend=True,
        textposition='inside',
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )
    layout = dict(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        height=600,
        font={"color": "#fff"}
    )

    return dict(data=[trace], layout=layout)

@app.callback(
    Output("benefit-last-eingeloest_today", "figure"), [Input("qr-code-update", "n_intervals")]
)
def generate_benefits_graph(interval):
    """
    :param interval:
    :return:
    """
    try:
        # korrekte umsetzung
        data.benefit_heute()
        df_count_benefits = data.benefits_pro_day

        trace = dict(
            type="bar",
            x=df_count_benefits['Benefit'],
            y=df_count_benefits['counts'],
            text=df_count_benefits['counts'],
            textposition='inside',
            line={"color": "#42C4F7"},
            #line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
            marker=dict(color='#ff8747'),
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.9
        )

        layout = dict(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": "#fff"}
        )

    except Exception as error:
        raise PreventUpdate
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
    try:
        #print(qr_code_live_figure)
        qr_code_values = []

        # korrekte umsetzung
        data.qr_code_pro_stunde_monthly()
        df_count = data.qr_code_pro_month

        # Check to see whether wind-speed has been plotted yet
        if qr_code_live_figure is not None:
            qr_code_values = qr_code_live_figure["data"][0]["y"]
        if "Auto" in auto_state:
            bin_val = np.histogram(
                qr_code_values,
                bins=range(int(round(min(qr_code_values))), int(round(max(qr_code_values)))),
            )
        else:
            bin_val = np.histogram(qr_code_values, bins=slider_value)
    except Exception as error:
        raise PreventUpdate
    try:
        avg_val = float(sum(qr_code_values)) / len(qr_code_values)
        median_val = np.median(qr_code_values)

        pdf_fitted = rayleigh.pdf(
            bin_val[1], loc=(avg_val) * 0.55, scale=(bin_val[1][-1] - bin_val[1][0]) / 3
        )
        y_val = (pdf_fitted * max(bin_val[0]) * 20,)
        y_val_max = max(y_val[0])
        bin_val_max = max(bin_val[0])

        trace = dict(
            type="bar",
            x=bin_val[1],
            y=bin_val[0],
            marker={"color": colors["graph_line"]},
            showlegend=False,
            hoverinfo="x+y",
        )

        traces_scatter = [
            {"line_dash": "dash", "line_color": "#2E5266", "name": "Average"},
            {"line_dash": "dot", "line_color": "#BD9391", "name": "Median"},
        ]

        scatter_data = [
            dict(
                type="scatter",
                x=[bin_val[int(len(bin_val) / 2)]],
                y=[0],
                mode="lines",
                line={"dash": traces["line_dash"], "color": traces["line_color"]},
                marker={"opacity": 0},
                visible=True,
                name=traces["name"],
            )
            for traces in traces_scatter
        ]

        trace3 = dict(
            type="scatter",
            mode="lines",
            line={"color": "#42C4F7"},
            y=y_val[0],
            x=bin_val[1][: len(bin_val[1])],
            name="Rayleigh Fit",
        )
        layout = dict(
            height=400,
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": "#fff"},
            xaxis={
                "title": "Anzahl QR-Codes",
                "showgrid": False,
                "showline": False,
                "fixedrange": True,
            },
            yaxis={
                "showgrid": False,
                "showline": False,
                "zeroline": False,
                "title": "Verteilung",
                "fixedrange": True,
            },
            autosize=True,
            bargap=0.01,
            bargroupgap=0,
            hovermode="closest",
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "xanchor": "center",
                "y": 1,
                "x": 0.5,
            },
            shapes=[
                {
                    "xref": "x",
                    "yref": "y",
                    "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                    "y0": 0,
                    "x0": avg_val,
                    "x1": avg_val,
                    "type": "line",
                    "line": {"dash": "dash", "color": "#2E5266", "width": 5},
                },
                {
                    "xref": "x",
                    "yref": "y",
                    "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                    "y0": 0,
                    "x0": median_val,
                    "x1": median_val,
                    "type": "line",
                    "line": {"dash": "dot", "color": "#BD9391", "width": 5},
                },
            ],
        )
    except Exception as error:
        raise PreventUpdate
    return dict(data=[trace, scatter_data[0], scatter_data[1], trace3], layout=layout)

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

