from plotly_presentation._core.colors import (
    color_list,
    Color,
    DivergentColor,
    SequentialColor,
    PlotColor,
    CalloutColor,
    get_sequential_color_list,
    get_diverging_color_list,
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

        elif slide_layout == "slide_wide":
            height_multiplier = 0.75
            width_multiplier = 1

        self.figure.update_layout(
            height=int(self.plot_height * height_multiplier),
            width=int(self.plot_width * width_multiplier),
        )

    def set_color_palette(
        self,
        palette_type: str = None,
        palette_name: str = None,
        color_dict: dict = None,
    ):
        """Set the color palette for the plot"""
        _VALID_PALETTES = [
            "sequential",
            "diverging",
            "sequential_negative",
            "diverging_negative",
        ]
        if palette_type not in _VALID_PALETTES and palette_type is not None:
            raise ValueError(f"Invalid palette type. Must be one of {_VALID_PALETTES}")

        if palette_type is None and color_dict is None:
            raise AttributeError("Either palette_type or color_dict must be provided")

        if color_dict is not None:
            for key, value in color_dict.items():
                try:
                    self.figure.update_traces(
                        line_color=value, selector=({"name": key})
                    )
                except ValueError:
                    self.figure.update_traces(
                        marker_color=value, selector=({"name": key})
                    )
        elif palette_type in ["sequential", "diverging"]:
            trace_names = [d.name for d in self.figure.data]
            n_traces = len(trace_names)

            if n_traces > 1:
                if palette_type == "sequential":
                    try:
                        colors = get_sequential_color_list(
                            palette_name=palette_name, n=n_traces
                        )
                    except TypeError:
                        raise TypeError(
                            "You must specify the custom color palette in the colors_config.yaml file."
                        )
                else:
                    try:
                        colors = get_diverging_color_list(
                            palette_name=palette_name, n=n_traces
                        )
                    except TypeError:
                        raise TypeError(
                            "You must specify the custom color palette in the colors_config.yaml file."
                        )

                for color, name in zip(colors, trace_names):
                    try:
                        self.figure.update_traces(
                            line_color=color, selector=({"name": name})
                        )
                    except ValueError:
                        self.figure.update_traces(
                            marker_color=color, selector=({"name": name})
                        )

    def _apply_waterfall_style(self):
        self.figure.data[0]["increasing"] = {"marker": {"color": Color.POSITIVE.value}}
        self.figure.data[0]["decreasing"] = {"marker": {"color": Color.NEGATIVE.value}}
        self.figure.data[0]["totals"] = {"marker": {"color": Color.NEUTRAL.value}}
        self.figure.data[0]["connector"] = {
            "mode": "between",
            "line": {"width": 0.5, "color": "black", "dash": "solid"},
        }
