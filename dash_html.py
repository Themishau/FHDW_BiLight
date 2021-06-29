# -*- coding: utf-8 -*-
import os
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from Plot_Data.plot_data import BI_Data
from BI_Export.ReportWriter import ReportWriter
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
                        "Diese App zeigt die eingelösten QR-Codes in Echtzeit.",
                        className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div([
                html.Button('Download BI-Data', id='BI_export_Button'),
                             dcc.Download(id="download-dataframe-xlsx"),
                ]),
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
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "eingelöste QR-Codes diesen Monat", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="montly-update-histogram",
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
    Output("download-dataframe-xlsx", "data"),
    Input("BI_export_Button", "n_clicks"),
    prevent_initial_call=True,
)
def download_BI_Data(n_clicks):
    writer = ReportWriter()
    data = writer.createDailyReport("")

    return dict(content=data, base64=True, filename=writer.get_filename())

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

    data.refresh_data()

    # korrekte umsetzung
    data.qr_code_pro_stunde_heute()
    df_count = data.qr_code_pro_stunde

    # data.qr_code_df['hour'] = data.qr_code_df['Timestamp'].dt.hour
    # data.qr_code_df['day'] = data.qr_code_df['Timestamp'].dt.day
    # data.qr_code_df['month'] = data.qr_code_df['Timestamp'].dt.month
    # df_count = data.qr_code_df.groupby(['hour']).size().reset_index(name='counts')


    try:
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
    Output("montly-update-histogram", "figure"),
    [Input("qr-code-update", "n_intervals")]

)
def gen_monthly_qr(interval):
    """
    :param interval:
    :return:
    """
    try:
        # korrekte umsetzung
        data.qr_code_pro_stunde_monthly()
        df_count_montly = data.qr_code_pro_month
        sizeref = 2. * max(df_count_montly['counts']) / (2*10)

        trace = dict(
            type="Line",
            x=df_count_montly['day'],
            y=df_count_montly['counts'],
            text=df_count_montly['counts'],
            hoverinfo="all",
            mode="line",
            marker=dict(color='#ff8747',
                        sizeref=sizeref,
                        sizemode='diameter',
                        size=df_count_montly['counts'],
                        line_color='rgb(8,48,107)',
                        line_width=1.5
                        ),
            opacity=0.9
        )

        layout = dict(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": "#fff"},
            xaxis={
                "title": "Tag",
                "showgrid": True,
                "showline": True,
            },
            yaxis={
                "showgrid": True,
                "showline": True,
                "zeroline": True,
                "title": "Anzahl QR-Codes",
            },
        )

    except Exception as error:
        raise PreventUpdate
    return dict(data=[trace], layout=layout)


def start_app():
    app.run_server(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    start_app()


# def gen_monthly_qr(interval):
#     """
#     :param interval:
#     :return:
#     """
#     try:
#         # korrekte umsetzung
#         data.qr_code_pro_stunde_monthly()
#         df_count_montly = data.qr_code_pro_month
#         print(df_count_montly)
#         sizeref = 2. * max(df_count_montly['counts']) / (2*10000)
#
#         trace = dict(
#             type="Scatter",
#             x=df_count_montly['day'],
#             y=df_count_montly['counts'],
#             text=df_count_montly['counts'],
#             hoverinfo="all",
#             mode="markers",
#             marker=dict(color='#ff8747',
#                         sizeref=sizeref,
#                         sizemode='area',
#                         size=df_count_montly['counts'],
#                         line_color='rgb(8,48,107)',
#                         line_width=1.5
#                         ),
#             opacity=0.9
#         )
#
#         layout = dict(
#             plot_bgcolor=colors["background"],
#             paper_bgcolor=colors["background"],
#             font={"color": "#fff"}
#         )
#
#     except Exception as error:
#         raise PreventUpdate
#     return dict(data=[trace], layout=layout)