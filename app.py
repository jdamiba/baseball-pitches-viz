import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

shapes = [
  {
    "type": "rect",
    "layer": "below",
    "x0": 0,
    "x1": 0.5,
    "y0": 0,
    "y1": 0.5
  },
  {
    "type": "rect",
    "layer": "below",
    "x0": 0.5,
    "x1": 1,
    "y0": 0,
    "y1": 0.5
  },
  {
    "type": "rect",
    "layer": "below",
    "x0": 0.5,
    "x1": 1,
    "y0": 0.5,
    "y1": 1
  },
  {
    "type": "rect",
    "layer": "below",
    "x0": 0,
    "x1": 0.5,
    "y0": 0.5,
    "y1": 1
  }
]

colors = [
  "aquamarine",
  "brown",
  "chocolate",
  "darkblue",
  "darkgreen",
  "forestgreen",
  "gold",
  "honeydew",
  "indigo",
  "navajowhite",
  "khaki",
  "lightblue",
  "magenta",
  "navy",
  "orange",
  "pink",
  "aqua",
  "red",
  "silver",
  "tomato",
  "turquoise",
  "violet",
  "wheat",
  "yellow",
  "azure"
]

values = [256, 64, 16, 4, 1]

parents = [255, 63, 15, 3, 0]

uniformtext = {
  "mode": ["false", "hide", "show"][1],
  "minsize": 12
}

textposition = ["inside", "auto", "outside"][1]

fig1 = {
    "data": [
    {
      "parents": parents,
      "labels": values,
      "values": values,
      "text": values,
      "title": "insidetextorientation: horizontal",
      "textposition": textposition,
      "insidetextorientation": [
        "auto",
        "horizontal",
        "radial",
        "tangential"
       ][1],
      "type": "pie", 
      "domain": {
        "x": [
          0.5,
          1
        ],
        "y": [
          0.5,
          1
        ]
      }
    },
    {
      "parents": parents,
      "labels": values,
      "values": values,
      "text": values,
      "title": "insidetextorientation: radial",
      "textposition": textposition,
      "insidetextorientation": [
        "auto",
        "horizontal",
        "radial",
        "tangential"
       ][2],
      "type": "pie", 
      "domain": {
        "x": [
          0.5,
          1
        ],
        "y": [
          0,
          0.5
        ]
      }
    },
    {
      "parents": parents,
      "labels": values,
      "values": values,
      "text": values,
      "title": "insidetextorientation: tangential",
      "textposition": textposition,
      "insidetextorientation": [
        "auto",
        "horizontal",
        "radial",
        "tangential"
       ][3],
      "type": "pie", 
      "domain": {
        "x": [
          0,
          0.5
        ],
        "y": [
          0,
          0.5
        ]
      }
    },
    {
      "parents": parents,
      "labels": values,
      "values": values,
      "text": values,
      "title": "insidetextorientation: auto",
      "textposition": textposition,
      "insidetextorientation": [
        "auto",
        "horizontal",
        "radial",
        "tangential"
       ][0],
      "type": "pie", 
      "domain": {
        "x": [
          0,
          0.5
        ],
        "y": [
          0.5,
          1
        ]
      }
    }, 
  ],
  "layout": {
    "uniformtext": uniformtext,
    "margin": {
      "t": 20,
      "b": 10,
      "l": 10,
      "r": 10
    },
    "legend": {
      "title": {
        "text": "<b>legend title</b>"
      }
    },
     "shapes": shapes,
  },
  
}

fig2_parents = [
  "",
  "Alpha",
  "Alpha",
  "Charlie",
  "Charlie",
  "Charlie",
  "Foxtrot",
  "Foxtrot",
  "Foxtrot",
  "Foxtrot",
  "Juliet",
  "Juliet",
  "Juliet",
  "Juliet",
  "Juliet",
  "Oscar",
  "Oscar",
  "Oscar",
  "Oscar",
  "Oscar",
  "Oscar",
  "Uniform",
  "Uniform",
  "Uniform",
  "Uniform",
  "Uniform",
  "Uniform"
]

fig2_labels = [
  "Alpha",
  "Bravo",
  "Charlie",
  "Delta",
  "Echo",
  "Foxtrot",
  "Golf",
  "Hotel",
  "India",
  "Juliet",
  "Kilo",
  "Lima",
  "Mike",
  "November",
  "Oscar",
  "Papa",
  "Quebec",
  "Romeo",
  "Sierra",
  "Tango",
  "Uniform",
  "Victor",
  "Whiskey",
  "X ray",
  "Yankee",
  "Zulu"
]

fig2 = {
    "data": [
    {
      "name": "horizontal",
      "insidetextorientation": "horizontal",
      "type": "sunburst",
      "parents": fig2_parents,
      "labels": fig2_labels,
      "marker": {
        "colors": colors
      },
      "textinfo": "label+value",
      "domain": {
        "x": [
          0.5,
          1
        ],
        "y": [
          0.5,
          1
        ]
      }
    },
    {
      "name": "radial",
      "insidetextorientation": "radial",
      "type": "sunburst",
      "parents": fig2_parents,
      "labels": fig2_labels,
      "textinfo": "label+value",
      "domain": {
        "x": [
          0.5,
          1
        ],
        "y": [
          0,
          0.5
        ]
      }
    },
    {
      "name": "tangential",
      "insidetextorientation": "tangential",
      "type": "sunburst",
      "parents": fig2_parents,
      "labels": fig2_labels,
      "textinfo": "label+value",
      "domain": {
        "x": [
          0,
          0.5
        ],
        "y": [
          0,
          0.5
        ]
      }
    },
    {
      "title": "auto",
      "insidetextorientation": "auto",
      "type": "sunburst",
      "parents": fig2_parents,
      "labels": fig2_labels,
      "textinfo": "label+value",
      "domain": {
        "x": [
          0,
          0.5
        ],
        "y": [
          0.5,
          1
        ]
      }
    }
  ],
  "layout": {
    "margin": {
      "t": 10,
      "b": 10,
      "l": 10,
      "r": 10
    },
    "showlegend": "True", 
    "font": {
      "size": 14
    },
    "shapes": [
      {
        "type": "rect",
        "layer": "below",
        "x0": 0,
        "x1": 0.5,
        "y0": 0,
        "y1": 0.5
      },
      {
        "type": "rect",
        "layer": "below",
        "x0": 0.5,
        "x1": 1,
        "y0": 0,
        "y1": 0.5
      },
      {
        "type": "rect",
        "layer": "below",
        "x0": 0.5,
        "x1": 1,
        "y0": 0.5,
        "y1": 1
      },
      {
        "type": "rect",
        "layer": "below",
        "x0": 0,
        "x1": 0.5,
        "y0": 0.5,
        "y1": 1
      }
    ],
    "annotations": [
      {
        "text": "auto",
        "showarrow": "false",
        "xref": "paper",
        "yref": "paper",
        "xanchor": "right",
        "yanchor": "bottom",
        "x": 0.5,
        "y": 0.5,
        "font": {
          "size": 20
        }
      },
      {
        "text": "tangential",
        "showarrow": "false",
        "xref": "paper",
        "yref": "paper",
        "xanchor": "right",
        "yanchor": "bottom",
        "x": 0.5,
        "y": 0,
        "font": {
          "size": 20
        }
      },
      {
        "text": "radial",
        "showarrow": "false",
        "xref": "paper",
        "yref": "paper",
        "xanchor": "right",
        "yanchor": "bottom",
        "x": 1,
        "y": 0,
        "font": {
          "size": 20
        }
      },
      {
        "text": "horizontal",
        "showarrow": "false",
        "xref": "paper",
        "yref": "paper",
        "xanchor": "right",
        "yanchor": "bottom",
        "x": 1,
        "y": 0.5,
        "font": {
          "size": 20
        }
      }
    ]
  }
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Markdown(children='## insidetextorientation and legend.title'),
    dcc.Markdown(children='### [Codepen #1](https://codepen.io/MojtabaSamimi/pen/zYxBLJe)'),
    dcc.Markdown(children='### [Codepen #2](https://codepen.io/MojtabaSamimi/pen/MWYpooK)'),
    dcc.Markdown(children='### [GitHub PR](https://github.com/plotly/plotly.js/pull/4420)'),
    dcc.Graph(
        id='example-graph',
        figure=fig1
    ),
    dcc.Graph(
        id='example-graph-2',
        figure=fig2
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
    