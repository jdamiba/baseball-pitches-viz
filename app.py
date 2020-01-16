import dash
import dash_core_components as dcc
import dash_html_components as html
import pybaseball as pb
import plotly.express as px
import pandas as pd

from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "MLB Pitcher Scouting Report"
server = app.server

app.layout = html.Div(
    children=[
        html.Nav(
            className="navbar",
            children=[
                html.H1(
                    children=[
                        html.A(
                            className="navbar-brand",
                            children="MLB Pitcher Scouting Report",
                            href="/",
                        )
                    ]
                )
            ],
        ),
        html.Div(
            className="mr-5 ml-5 mt-0 pt-2 jumbotron",
            children=[
                dcc.Markdown("#### First Name"),
                dcc.Input(
                    className="mb-3", id="first-name", value="Gerrit", type="text"
                ),
                dcc.Markdown("#### Last Name"),
                dcc.Input(className="mb-3", id="last-name", value="Cole", type="text"),
                dcc.Markdown("#### Date Range"),
                dcc.DatePickerRange(
                    className="mb-3",
                    id="date-picker",
                    min_date_allowed=dt(2019, 3, 20),
                    max_date_allowed=dt(2019, 9, 29),
                    initial_visible_month=dt(2019, 3, 20),
                ),
                dcc.Markdown("#### Infield Fielding Alignment"),
                dcc.Dropdown(
                    className="mb-3 w-25",
                    id="infield-dropdown",
                    options=[
                        {"label": "Standard", "value": "Standard"},
                        {"label": "Shift", "value": "Infield shift"},
                    ],
                    value="Standard",
                ),
                dcc.Markdown("#### Outfield Fielding Alignment"),
                dcc.Dropdown(
                    className="w-25",
                    id="outfield-dropdown",
                    options=[
                        {"label": "Standard", "value": "Standard"},
                        {"label": "Strategic", "value": "Strategic"},
                    ],
                    value="Standard",
                ),
                html.Button(
                    "Create Data Visualizations!",
                    id="button",
                    className="btn btn-primary mt-3 mb-3",
                ),
                dcc.Loading(children=dcc.Graph(id="pitch-type-scatter")),
                dcc.Loading(children=dcc.Graph(id="pitch-type-box")),
            ],
        ),
    ],
)


@app.callback(
    [
        Output(component_id="pitch-type-scatter", component_property="figure"),
        Output(component_id="pitch-type-box", component_property="figure"),
    ],
    [
        Input("button", "n_clicks"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("infield-dropdown", "value"),
        Input("outfield-dropdown", "value"),
    ],
    [
        State(component_id="first-name", component_property="value"),
        State(component_id="last-name", component_property="value"),
    ],
)
def update_output_div(
    n_clicks, start_date, end_date, infield, outfield, first_name, last_name,
):
    # only update on increment
    prev_clicks = 0
    if (
        start_date is None
        or n_clicks is None
        or end_date is None
        or first_name is None
        or last_name is None
        or n_clicks == prev_clicks
        or infield is None
        or outfield is None
    ):
        raise PreventUpdate
    else:
        data = get_data(first_name, last_name, start_date, end_date)

        data = data[data["if_fielding_alignment"] == infield]
        data = data[data["of_fielding_alignment"] == outfield]

        strikes = [
            i
            for i in data["Result of Pitch"]
            if i == "called_strike" or i == "swinging_strike"
        ]
        balls = [i for i in data["Result of Pitch"] if i == "ball"]
        foul = [i for i in data["Result of Pitch"] if i == "foul"]

        FF = len(data[data["Pitch Type"] == "4-Seam Fastball"])
        KC = len(data[data["Pitch Type"] == "Knuckle Curve"])
        CU = len(data[data["Pitch Type"] == "Curveball"])
        CH = len(data[data["Pitch Type"] == "Changeup"])
        SL = len(data[data["Pitch Type"] == "Slider"])
        FT = len(data[data["Pitch Type"] == "2-Seam Fastball"])

        pitch_type_scatter = px.scatter(
            data,
            x="Pitch Number",
            y="Pitch Speed",
            color="Pitch Type",
            hover_data=["Result of Pitch", "Play by Play"],
            trendline="ols",
            title=f"Scatter Plot of {first_name} {last_name}'s Pitch Speed Between {start_date} and {end_date}",
        )

        pitch_type_box = px.box(
            data,
            x="Pitch Type",
            y="Pitch Speed",
            color="Pitch Type",
            points="all",
            hover_data=["Result of Pitch", "Play by Play"],
            title=f"Box Plot of {first_name} {last_name}'s Pitch Speed Between {start_date} and {end_date}",
        )

        prev_clicks = prev_clicks + 1

        return pitch_type_scatter, pitch_type_box


def get_data(first_name, last_name, start_date, end_date):
    try:
        key = pb.playerid_lookup(last_name, first_name)["key_mlbam"].values[
            0
        ]  # get unique pitcher identifier
    except:
        pass

    data = pb.statcast_pitcher(
        start_date, end_date, key
    )  # get dataset of pitches thrown by pitcher
    data = data.sort_values(
        ["pitch_number"]
    )  # sort pitches by order thrown, earliest first
    data = data.dropna(
        subset=["pitch_type", "des", "description"]
    )  # make sure dataset does not contain nulls

    data["order"] = data.reset_index().index  # create new column with pitch order

    df = pd.DataFrame(data)

    df = df.rename(
        {
            "des": "Play by Play",
            "description": "Result of Pitch",
            "order": "Pitch Number",
            "pitch_name": "Pitch Type",
            "release_speed": "Pitch Speed",
        },
        axis=1,
    )

    return df


if __name__ == "__main__":
    app.run_server(debug=True)
