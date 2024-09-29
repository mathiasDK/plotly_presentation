from plotly_presentation._core.colors import Color, color_list, DivergentColor, SequentialColor, PlotColor, CalloutColor
import plotly.io as pio
import plotly.graph_objects as go

pio.templates["presentation_layout"] = go.layout.Template(
    layout = {
    'annotationdefaults': {
        'arrowcolor': str(CalloutColor.LINE_COLOR), 
        'arrowhead': 0, 
        'arrowwidth': 1, 
        "bgcolor": str(CalloutColor.TEXT_BG_COLOR),
        "font": {
            "color": str(CalloutColor.TEXT_COLOR)
        }
    },
    'autotypenumbers': 'strict',
    'coloraxis': {'colorbar': {'outlinewidth': 1, 'tickcolor': 'rgb(36,36,36)', 'ticks': 'outside'}},
    'colorscale': {
        'diverging': [[0, str(DivergentColor.START)], [0.5, str(DivergentColor.MID)], [1, str(DivergentColor.END)]],
        'sequential': [[0.0, str(SequentialColor.START)], [1.0, str(SequentialColor.END)]],
        'sequentialminus': [[0.0, str(SequentialColor.END)], [1.0, str(SequentialColor.START)]]
    },
    'colorway': color_list,
    'font': {'color': str(PlotColor.TEXT_COLOR)},
    'geo': {'bgcolor': 'white',
            'lakecolor': 'white',
            'landcolor': 'white',
            'showlakes': True,
            'showland': True,
            'subunitcolor': 'white'},
    'hoverlabel': {'align': 'left'},
    'hovermode': 'closest',
    'mapbox': {'style': 'light'},
    # 'paper_bgcolor': PlotColor.BG_COLOR,
    # 'plot_bgcolor': PlotColor.BG_COLOR,
    'polar': {'angularaxis': {'gridcolor': 'rgb(232,232,232)',
                              'linecolor': 'rgb(36,36,36)',
                              'showgrid': False,
                              'showline': True,
                              'ticks': 'outside'},
              'bgcolor': 'white',
              'radialaxis': {'gridcolor': 'rgb(232,232,232)',
                             'linecolor': 'rgb(36,36,36)',
                             'showgrid': False,
                             'showline': True,
                             'ticks': 'outside'}},
    'scene': {'xaxis': {'backgroundcolor': 'white',
                        'gridcolor': 'rgb(232,232,232)',
                        'gridwidth': 2,
                        'linecolor': 'rgb(36,36,36)',
                        'showbackground': True,
                        'showgrid': False,
                        'showline': True,
                        'ticks': 'outside',
                        'zeroline': False,
                        'zerolinecolor': 'rgb(36,36,36)'},
              'yaxis': {'backgroundcolor': 'white',
                        'gridcolor': 'rgb(232,232,232)',
                        'gridwidth': 2,
                        'linecolor': 'rgb(36,36,36)',
                        'showbackground': True,
                        'showgrid': False,
                        'showline': True,
                        'ticks': 'outside',
                        'zeroline': False,
                        'zerolinecolor': 'rgb(36,36,36)'},
              'zaxis': {'backgroundcolor': 'white',
                        'gridcolor': 'rgb(232,232,232)',
                        'gridwidth': 2,
                        'linecolor': 'rgb(36,36,36)',
                        'showbackground': True,
                        'showgrid': False,
                        'showline': True,
                        'ticks': 'outside',
                        'zeroline': False,
                        'zerolinecolor': 'rgb(36,36,36)'}},
    'shapedefaults': {'fillcolor': 'black', 'line': {'width': 0}, 'opacity': 0.3},
    'ternary': {'aaxis': {'gridcolor': 'rgb(232,232,232)',
                          'linecolor': 'rgb(36,36,36)',
                          'showgrid': False,
                          'showline': True,
                          'ticks': 'outside'},
                'baxis': {'gridcolor': 'rgb(232,232,232)',
                          'linecolor': 'rgb(36,36,36)',
                          'showgrid': False,
                          'showline': True,
                          'ticks': 'outside'},
                'bgcolor': 'white',
                'caxis': {'gridcolor': 'rgb(232,232,232)',
                          'linecolor': 'rgb(36,36,36)',
                          'showgrid': False,
                          'showline': True,
                          'ticks': 'outside'}},
    'title': {'x': 0.05},
    "barcornerradius": 10,
    'xaxis': {
        'automargin': True,
        'gridcolor': str(PlotColor.BG_COLOR),
        'linecolor': str(PlotColor.LINE_COLOR),
        'showgrid': False,
        'showline': True,
        'ticks': 'outside',
        'title': {'standoff': 15},
        'zeroline': False,
        'zerolinecolor': str(PlotColor.LINE_COLOR),
    },
    'yaxis': {
        'automargin': True,
        'gridcolor': str(PlotColor.BG_COLOR),
        'linecolor': str(PlotColor.LINE_COLOR),
        'showgrid': False,
        'showline': True,
        'ticks': 'outside',
        'title': {'standoff': 15},
        'zeroline': False,
        'zerolinecolor': str(PlotColor.LINE_COLOR),
    }
})
  
pio.templates.default = "presentation_layout"


class Style:
    def __init__(self, figure, slide_layout) -> None:
        self.figure = figure
        self.slide_layout = slide_layout
        self._set_width_and_height(slide_layout=slide_layout)

    def _set_width_and_height(self, slide_layout="slide_100%"):
        """Set plot width and height based on the layout"""
        self.plot_width = 960
        self.plot_height = 540
        height_multiplier, width_multiplier = 1.0, 1.0

        if slide_layout == "slide_75%":
            height_multiplier = 1.0 * 0.8
            width_multiplier = 0.75 * 0.8

        elif slide_layout == "slide_50%":
            height_multiplier = 1.0
            width_multiplier = 0.5

        elif slide_layout == "slide_25%":
            height_multiplier = 0.5
            width_multiplier = 0.5

        self.figure.update_layout(
            height = int(self.plot_height * height_multiplier),
            width = int(self.plot_width * width_multiplier)
        )
