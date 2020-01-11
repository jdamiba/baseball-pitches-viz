import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import pybaseball as pb
import plotly.express as px

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
  
app.layout = html.Div(className="main", children=[
  dcc.Markdown(children="## Visualizing A Season's Worth Of Pitches With [`pybaseball`](https://github.com/jldbc/pybaseball) and [`Dash`](https://dash.plot.ly)."),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="### Project Overview"),
  dcc.Markdown(children="### Every day brings us closer to the beginning of the baseball season. One of the things I love about the game is the strong emphasis that is placed on collecting statistics about players. I could (and have) spend hours looking up interesting facts about the game. For example, did you know that [Sandy Koufax is the only pitcher to throw a perfect game while striking out a batter in every inning?](https://en.wikipedia.org/wiki/Sandy_Koufax%27s_perfect_game)"),
  dcc.Markdown(children="### At the end of 2019 I discovered this [blog post](http://kenbo.hatenablog.com/entry/2019/12/18/001332) which demonstrates how to use the `pybaseball` API and Plotly Express to make really interesting vizualizations."),
  dcc.Markdown(children="### I decided to build on that work by making a Dash app that would let you create a chart for any pitcher."),
  dcc.Markdown(children="### Enter the name of a pitcher to see scatter and box plot visualizations of all the pitches they threw in the 2019 baseball season."),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="#### First Name"),
  dcc.Input(id='first-name', value='Gerrit', type='text'),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="#### Last Name"),
  dcc.Input(id='last-name', value='Cole', type='text'),
  html.Br(),
  html.Br(),
  html.Button('Submit', id='button'),
  dcc.Graph(id='scatter'),
  dcc.Graph(id='box'),
  dcc.Markdown(children="### built by [Joe Damiba](https://josephdamiba.com)"),

])



@app.callback(
    [Output(component_id='scatter', component_property='figure'),
     Output(component_id='box', component_property='figure')],
    [Input('button', 'n_clicks')],
    [State(component_id='first-name', component_property='value'),
     State(component_id='last-name', component_property='value')])
def update_output_div(n_clicks, first_name, last_name):
  #only update on increment
  prev_clicks = 0
  if n_clicks is None or n_clicks == prev_clicks:
    raise PreventUpdate
  else: 
    start_date = "2019-03-20" 
    end_date = "2019-10-30"
    
    try:
      key = pb.playerid_lookup(last_name, first_name)["key_mlbam"].values[0] # get unique pitcher identifier
    except:
      return px.scatter(title="No player found with that name. Check spelling?"), px.box(title="No player found with that name. Check spelling?"), 
    
    data = pb.statcast_pitcher(start_date, end_date, key) # get dataset of pitches thrown by pitcher
    data = data.sort_values(["pitch_number"]) # sort pitches by order thrown, earliest first
    data = data.dropna(subset=['pitch_type']) # make sure dataset does not contain nulls

    data["seq"] = data.reset_index().index # create new column with pitch order
        
    scatter = px.scatter(data, x="seq", y="release_speed", color="pitch_type", 
                            title=f'{first_name} {last_name} 2019 Pitches Release Speed Scatter Plot')
    
    box = px.box(data, x="pitch_type", y="release_speed", color="pitch_type", 
                title=f'{first_name} {last_name} 2019 Pitches Release Speed Box Plot')
    
    prev_clicks = prev_clicks + 1
    
    return scatter, box
  
if __name__ == '__main__':
    app.run_server(debug=True)
    