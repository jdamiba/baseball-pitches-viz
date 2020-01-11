import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pybaseball as pb
import plotly.express as px

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
  
app.layout = html.Div(className="mt-5 mr-5 ml-5", children=[
  dcc.Markdown(children="## Using Data Visualization To Understand Baseball Pitching"),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="### The game of baseball places a strong emphasis on statistics. That means that the game's history is accessible for those of us who weren't there to witness it. For example, did you know that [Sandy Koufax is the only pitcher to throw a perfect game while striking out a batter in every inning?](https://en.wikipedia.org/wiki/Sandy_Koufax%27s_perfect_game)"),
  dcc.Markdown(children="### There are three common types of pitches thrown by modern pitchers: the [fastball](https://en.wikipedia.org/wiki/Fastball), the [breaking ball](https://en.wikipedia.org/wiki/Breaking_ball), and the [change-up](https://en.wikipedia.org/wiki/Changeup). Let's use data visualization to better understand the difference between these pitch types."),
  dcc.Markdown(children="### In the input boxes below, type the first and last name of a player who threw a pitch in the 2019 baseball season."),
  html.Br(),
  dcc.Markdown(children="#### First Name"),
  dcc.Input(id='first-name', value='Gerrit', type='text'),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="#### Last Name"),
  dcc.Input(id='last-name', value='Cole', type='text'),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="### We can create a dataset that contains every pitch this player threw in the 2019 baseball season using the incredible `pybaseball` Python API."),
  html.Div(className="mt-5 mr-5 ml-5", children=[dcc.Markdown(children="`import pybaseball as pb`"),
  dcc.Markdown(children="`key = pb.playerid_lookup(last_name, first_name)['key_mlbam'].values[0] # get unique pitcher identifier`"),
  dcc.Markdown(children="`data = pb.statcast_pitcher('2019-03-20', '2019-10-30', key) # get dataset of pitches thrown by pitcher in the 2019 baseball season`"),
  dcc.Markdown(children="`data = data.sort_values(['pitch_number']) # sort pitches by order thrown, earliest first`"),
  dcc.Markdown(children="`data = data.dropna(subset=['pitch_type']) # make sure dataset does not contain nulls`"),
  dcc.Markdown(children="`data['order'] = data.reset_index().index # create new column with pitch order`")]),
  dcc.Markdown(children="### The first chart we can make using this data is a [scatter plot](https://en.wikipedia.org/wiki/Scatter_plot). To do so, we'll take each pitch and place it on the x-axis based on the order in which it was thrown. The first pitch will be all the way to the left and the last pitch will be all the way to the right."),
  dcc.Markdown(children="### On the y-axis we will plot the velocity of each pitch. The slowest pitch will be at the bottom while the fastest pitch is at the top. In order to tell the difference between the pitches on the scatter plot, we'll use different colors for each pitch type."),
  html.Div(className="mt-5 mr-5 ml-5", children=[dcc.Markdown(children="`import plotly.express as px`"),
  dcc.Markdown(children="`scatter = px.scatter(data, x='order', y='release_speed', color=pitch_type',title=f'{first_name} {last_name} 2019 Pitches Release Speed Scatter Plot')`")]),
  dcc.Markdown(children="### The second chart we can make is a [box plot](https://en.wikipedia.org/wiki/Box_plot). For this chart, we'll group similar pitches together on the x-axis. The y-axis will be the same as the scatter plot- the release speed of the pitch. We'll draw a shape around each pitch type describing the 25th and 75th percentiles as well as the median. Any points past the whiskers are outliers."),
  html.Div(className="mt-5 mr-5 ml-5", children=dcc.Markdown(children="`box = px.box(data, x='pitch_type', y='release_speed', color='pitch_type', title=f'{first_name} {last_name} 2019 Pitches Release Speed Box Plot')`")),
  html.Br(),
  html.Br(),
  html.Button('Create Charts', id='button', className="btn btn-primary mb-5"),
  dcc.Markdown(children="Scatter Plot"),
  dcc.Loading(children=dcc.Graph(id='scatter')),
  dcc.Markdown(children="Box Plot"),
  dcc.Loading(children=dcc.Graph(id='box')),
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
    try:
      key = pb.playerid_lookup(last_name, first_name)["key_mlbam"].values[0] # get unique pitcher identifier
    except:
      return px.scatter(title="No player found with that name. Check spelling?"), px.box(title="No player found with that name. Check spelling?"), 
    
    data = pb.statcast_pitcher("2019-03-20", "2019-10-30", key) # get dataset of pitches thrown by pitcher
    data = data.sort_values(["pitch_number"]) # sort pitches by order thrown, earliest first
    data = data.dropna(subset=['pitch_type']) # make sure dataset does not contain nulls
    
    data["order"] = data.reset_index().index # create new column with pitch order
        
    scatter = px.scatter(data, x="order", y="release_speed", color="pitch_type", 
                         title=f'{first_name} {last_name} 2019 Pitches Release Speed Scatter Plot')
    
    box = px.box(data, x="pitch_type", y="release_speed", color="pitch_type", 
                title=f'{first_name} {last_name} 2019 Pitches Release Speed Box Plot')
    
    prev_clicks = prev_clicks + 1
    
    return scatter, box
  
if __name__ == '__main__':
    app.run_server(debug=True)
    