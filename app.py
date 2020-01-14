import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pybaseball as pb
import plotly.express as px
import dash_ace
from datetime import datetime as dt

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Baseball Pitches Visualizer'
server = app.server

intro = dcc.Markdown(
    children="""
  # Baseball Pitches Visualizer
  
  In the input boxes below, type the first and last name of a Major League Baseball pitcher.
  
  Also, enter a date range. Then, click create charts!
  
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
            "Create Charts!", id="button", className="btn btn-primary mt-3 mb-3"
        ),
        dcc.Loading(children=dcc.Graph(id="scatter")),
        dcc.Loading(children=dcc.Graph(id="box")),
    ],
)


@app.callback(
    [
        Output(component_id="scatter", component_property="figure"),
        Output(component_id="box", component_property="figure"),
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
    elif start_date is None or end_date is None:
        raise Exception("Date cannot be empty")
    else:
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
            subset=["pitch_type"]
        )  # make sure dataset does not contain nulls

        data["order"] = data.reset_index().index  # create new column with pitch order

        scatter = px.scatter(
            data,
            x="order",
            y="release_speed",
            color="pitch_type",
            title=f"Scatter Plot of {first_name} {last_name}'s Pitch Release Speed For Between {start_date} and {end_date}",
        )

        box = px.box(
            data,
            x="pitch_type",
            y="release_speed",
            color="pitch_type",
            title=f"Box Plot of {first_name} {last_name}'s Pitch Release Speed For Between {start_date} and {end_date}",
        )

        prev_clicks = prev_clicks + 1

        return scatter, box


if __name__ == "__main__":
    app.run_server(debug=True)
