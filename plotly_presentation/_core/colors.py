from enum import Enum
from plotly_presentation._core.options import options


color_dict = options.get_option("config.colors")
color_list = color_dict["color_list"]


class ColorEnum(Enum):
    def __str__(self):
        return self.value


class Color(ColorEnum):
    PRIMARY = color_dict["primary_colors"]["primary"]
    SECONDARY = color_dict["primary_colors"]["secondary"]
    TERTIARY = color_dict["primary_colors"]["tertiary"]


class DivergentColor(ColorEnum):
    START = color_dict["divergent_colors"]["start"]
    MID = color_dict["divergent_colors"]["mid"]
    END = color_dict["divergent_colors"]["end"]


class SequentialColor(ColorEnum):
    START = color_dict["sequential_colors"]["start"]
    END = color_dict["sequential_colors"]["end"]


class PlotColor(ColorEnum):
    LINE_COLOR = color_dict["plot_colors"]["line_color"]
    TEXT_COLOR = color_dict["plot_colors"]["text_color"]
    BG_COLOR = color_dict["plot_colors"]["bg_color"]


class CalloutColor(ColorEnum):
    LINE_COLOR = color_dict["callout_colors"]["line_color"]
    TEXT_COLOR = color_dict["callout_colors"]["text_color"]
    TEXT_BG_COLOR = color_dict["callout_colors"]["text_bg_color"]
    CIRCLE_LINE_COLOR = color_dict["callout_colors"]["circle_line_color"]
    CIRCLE_FILL_COLOR = color_dict["callout_colors"]["text_bg_color"]


del ColorEnum, color_dict

if __name__ == "__main__":
    print(Color.PRIMARY)
    print(PlotColor.LINE_COLOR)
    print(PlotColor.BG_COLOR)
