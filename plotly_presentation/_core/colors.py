from enum import Enum

color_dict = {
    "primary": "#193931",
    "secondary": "#122b4f",
    "tertiary": "#54123a",
}
light_color_dict = {
    "primary": "#8c9c98",
    "secondary": "##8895a7",
    "tertiary": "#a9889c"
}
color_list = []
class ColorEnum(Enum):
    def __str__(self):
        return self.value
    
class Color(ColorEnum):
    PRIMARY = color_dict["primary"]
    SECONDARY = color_dict["secondary"]
    TERTIARY = color_dict["tertiary"]

class DivergentColor(ColorEnum):
    START = color_dict["primary"]
    MID = "#d4d4d4"
    END = color_dict["primary"]

class SequentialColor(ColorEnum):
    START = light_color_dict["primary"]
    END = color_dict["primary"]

class PlotColor(ColorEnum):
    LINE_COLOR = "#000"
    TEXT_COLOR = "#000"
    BG_COLOR = "#fff"

class CalloutColor(ColorEnum):
    LINE_COLOR = "#222222"
    TEXT_COLOR = "#000"
    TEXT_BG_COLOR = "#fff"

del ColorEnum, color_dict, light_color_dict

if __name__ == "__main__":
    print(Color.PRIMARY)
    print(PlotColor.LINE_COLOR)