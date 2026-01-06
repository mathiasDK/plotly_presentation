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

    def set_legend(
        self,
        position: str = "top",
        orientation: str = "h",
        font_size: int = None,
        bgcolor: str = None,
    ):
        """
        Configure legend position and styling for better analytics.

        Parameters:
        position (str): 'top', 'bottom', 'left', 'right', or 'top-left', etc.
        orientation (str): 'h' (horizontal) or 'v' (vertical)
        font_size (int): Font size for legend
        bgcolor (str): Background color for legend
        """
        legend_dict = {
            "orientation": orientation,
        }

        # Map position strings to plotly positions
        position_map = {
            "top": {"x": 0.5, "y": 1.02, "xanchor": "center", "yanchor": "bottom"},
            "bottom": {"x": 0.5, "y": -0.15, "xanchor": "center", "yanchor": "top"},
            "left": {"x": -0.15, "y": 0.5, "xanchor": "right", "yanchor": "middle"},
            "right": {"x": 1.02, "y": 0.5, "xanchor": "left", "yanchor": "middle"},
        }

        if position in position_map:
            legend_dict.update(position_map[position])
        else:
            # Handle compound positions like "top-left"
            parts = position.split("-")
            if len(parts) == 2:
                x_pos = (
                    -0.15
                    if "left" in parts[1]
                    else (1.02 if "right" in parts[1] else 0.5)
                )
                y_pos = (
                    1.02
                    if "top" in parts[0]
                    else (-0.15 if "bottom" in parts[0] else 0.5)
                )
                xanchor = (
                    "right"
                    if "left" in parts[1]
                    else ("left" if "right" in parts[1] else "center")
                )
                yanchor = (
                    "bottom"
                    if "top" in parts[0]
                    else ("top" if "bottom" in parts[0] else "middle")
                )
                legend_dict.update(
                    {"x": x_pos, "y": y_pos, "xanchor": xanchor, "yanchor": yanchor}
                )

        if font_size:
            legend_dict["font"] = {"size": font_size}

        if bgcolor:
            legend_dict["bgcolor"] = bgcolor

        self.figure.update_layout(legend=legend_dict)
        return self.figure

    def set_title(
        self,
        title: str,
        subtitle: str = None,
        title_size: int = 18,
        subtitle_size: int = 14,
    ):
        """
        Set title and optional subtitle for analytics charts.

        Parameters:
        title (str): Main title
        subtitle (str): Optional subtitle
        title_size (int): Font size for title
        subtitle_size (int): Font size for subtitle
        """
        self.figure.update_layout(
            title={
                "text": title,
                "subtitle": {
                    "text": subtitle,
                    "font": {"size": subtitle_size},
                },
                "x": 0.05,
                "xanchor": "left",
                "font": {"size": title_size},
            }
        )
        return self.figure
