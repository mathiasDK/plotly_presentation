from plotly_presentation._core.colors import (
    color_list,
    DivergentColor,
    SequentialColor,
    PlotColor,
    CalloutColor,
)
from plotly_presentation._core.options import options
import plotly.io as pio
import plotly.graph_objects as go
from plotly_presentation._core.utils.dict_funcs import update_dict


layout = options.get_option("config.layout")

color_layout = {
    "annotationdefaults": {
        "arrowcolor": str(CalloutColor.LINE_COLOR),
        "bgcolor": str(CalloutColor.TEXT_BG_COLOR),
        "font": {"color": str(CalloutColor.TEXT_COLOR)},
    },
    "colorscale": {
        "diverging": [
            [0, str(DivergentColor.START)],
            [0.5, str(DivergentColor.MID)],
            [1, str(DivergentColor.END)],
        ],
        "sequential": [
            [0.0, str(SequentialColor.START)],
            [1.0, str(SequentialColor.END)],
        ],
        "sequentialminus": [
            [0.0, str(SequentialColor.END)],
            [1.0, str(SequentialColor.START)],
        ],
    },
    "colorway": color_list,
    "font": {"color": str(PlotColor.TEXT_COLOR)},
    "paper_bgcolor": str(PlotColor.BG_COLOR),
    "plot_bgcolor": str(PlotColor.BG_COLOR),
    # 'plot_bgcolor': PlotColor.BG_COLOR,
    "xaxis": {
        "gridcolor": str(PlotColor.BG_COLOR),
        "linecolor": str(PlotColor.LINE_COLOR),
        "zerolinecolor": str(PlotColor.LINE_COLOR),
    },
    "yaxis": {
        "gridcolor": str(PlotColor.BG_COLOR),
        "linecolor": str(PlotColor.LINE_COLOR),
        "zerolinecolor": str(PlotColor.LINE_COLOR),
    },
}
layout = update_dict(color_layout, layout)

pio.templates["presentation_layout"] = go.layout.Template(layout=layout)
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

        elif slide_layout == "slide_wide%":
            height_multiplier = 0.75
            width_multiplier = 1

        self.figure.update_layout(
            height=int(self.plot_height * height_multiplier),
            width=int(self.plot_width * width_multiplier),
        )
