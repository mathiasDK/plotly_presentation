from enum import Enum
from plotly_presentation._core.options import options


color_dict = options.get_option("config.colors")
color_list = color_dict["color_list"]


class ColorEnum(Enum):
    def __str__(self):
        return self.value


class Color(ColorEnum):
    PRIMARY = color_dict["primary_colors"].get("primary", "#D73809")
    SECONDARY = color_dict["primary_colors"].get("secondary", "#60748D")
    TERTIARY = color_dict["primary_colors"].get("tertiary", "#940C08")
    POSITIVE = color_dict["primary_colors"].get("positive", "#4c8a8e")
    NEGATIVE = color_dict["primary_colors"].get("negative", "#8E504C")
    NEUTRAL = color_dict["primary_colors"].get("neutral", "#CFD6D5")


class DivergentColor(ColorEnum):
    START = color_dict["divergent_colors"].get("start", "#D73809")
    MID = color_dict["divergent_colors"].get("mid", "#c2c2c2")
    END = color_dict["divergent_colors"].get("end", "#940C08")


class SequentialColor(ColorEnum):
    START = color_dict["sequential_colors"].get("start", "#D73809")
    END = color_dict["sequential_colors"].get("end", "#f98f70")


class PlotColor(ColorEnum):
    LINE_COLOR = color_dict["plot_colors"].get("line_color", "#000000")
    TEXT_COLOR = color_dict["plot_colors"].get("text_color", "#000000")
    BG_COLOR = color_dict["plot_colors"].get("bg_color", "#ffffff")


class CalloutColor(ColorEnum):
    LINE_COLOR = color_dict["callout_colors"].get("line_color", "#222222")
    TEXT_COLOR = color_dict["callout_colors"].get("text_color", "#000000")
    TEXT_BG_COLOR = color_dict["callout_colors"].get("text_bg_color", "#ffffff")
    CIRCLE_LINE_COLOR = color_dict["callout_colors"].get("circle_line_color", "#D73809")
    CIRCLE_FILL_COLOR = color_dict["callout_colors"].get("text_bg_color", "#ffffff")


del ColorEnum, color_dict

if __name__ == "__main__":
    print(Color.PRIMARY)
    print(PlotColor.LINE_COLOR)
    print(PlotColor.BG_COLOR)
