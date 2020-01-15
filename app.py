import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pybaseball as pb
import plotly.express as px
import pandas as pd
from datetime import datetime as dt

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Baseball Pitches Visualizer"
server = app.server

intro = dcc.Markdown(
    children="""
  # MLB Pitcher Scouting Report
  
  Enter the name of a Major League Baseball pitcher who played and a date range in the 2019 baseball season (3/20/19 - 9/29/19). 
  
  Then, click Get Statistics!
  
  Hover over a point to see more information that particular pitch.
  
  #### First Name
  """
)

app.layout = html.Div(
    className="mt-1 mr-5 ml-5",
    children=[
        intro,
        dcc.Input(className="mb-3", id="first-name", value="Gerrit", type="text"),
        dcc.Markdown(children="#### Last Name"),
        dcc.Input(id="last-name", value="Cole", type="text"),
        html.Br(),
        html.Br(),
        dcc.Markdown(children="#### Date Range"),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=dt(2019, 3, 20),
            max_date_allowed=dt(2019, 9, 29),
            initial_visible_month=dt(2019, 3, 20),
        ),
        html.Br(),
        html.Button(
            "Get Statistics!", id="button", className="btn btn-primary mt-3 mb-3"
        ),
        dcc.Markdown(id="text-box"),
        dcc.Loading(children=dcc.Graph(id="pitch-type-scatter")),
        dcc.Loading(children=dcc.Graph(id="pitch-type-box")),
    ],
)


@app.callback(
    [
        Output(component_id="pitch-type-scatter", component_property="figure"),
        Output(component_id="pitch-type-box", component_property="figure"),
        Output(component_id="text-box", component_property="children"),
    ],
    [
        Input("button", "n_clicks"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
    ],
    [
        State(component_id="first-name", component_property="value"),
        State(component_id="last-name", component_property="value"),
    ],
)
def update_output_div(n_clicks, start_date, end_date, first_name, last_name):
    # only update on increment
    prev_clicks = 0
    if n_clicks is None or n_clicks == prev_clicks:
        raise PreventUpdate
    elif (
        start_date is None
        or end_date is None
        or first_name is None
        or last_name is None
    ):
        raise PreventUpdate
    else:
        data = get_data(first_name, last_name, start_date, end_date)
        
        strikes = [
            i
            for i in data["Result of Pitch"]
            if i == "called_strike" or i == "swinging_strike"
        ]
        balls = [i for i in data["Result of Pitch"] if i == "ball"]
        foul = [i for i in data["Result of Pitch"] if i == "foul"]

        pitch_type_scatter = px.scatter(
            data,
            x="Pitch Number",
            y="Pitch Speed",
            color="Pitch Type",
            hover_data=["Result of Pitch", "Play by Play"],
            trendline="lowess",
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

        text = f"""
        Gathered {len(data)} pitches with descriptions for {first_name} {last_name} in the database for the time period between {start_date} and {end_date}.   
        Strikes: {len(strikes)}  
        Balls: {len(balls)}  
        Foul: {len(foul)}
        """

        prev_clicks = prev_clicks + 1

        return pitch_type_scatter, pitch_type_box, text


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

    df = df.rename({"des": "Play by Play", "description": "Result of Pitch", "order": "Pitch Number", "pitch_name": "Pitch Type", "release_speed": "Pitch Speed"}, axis=1)

    return df


if __name__ == "__main__":
    app.run_server(debug=True)
