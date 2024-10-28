from plotly.express.colors import n_colors, label_rgb
from .utils import _convert_to_rgb
from plotly_presentation._core.options import options


color_dict = options.get_option("config.colors").get("custom_sequential")
sequential_colors = {}


def create_sequential_color_list(low_color, high_color, n) -> list:
    low_color = _convert_to_rgb(low_color)
    high_color = _convert_to_rgb(high_color)
    if low_color[:3] == "rgb":
        color_type = "rgb"
    else:
        color_type = "tuple"
    sequential_color_list = n_colors(
        low_color, high_color, n_colors=n, colortype=color_type
    )
    sequential_color_list = [label_rgb(color) for color in sequential_color_list]
    return sequential_color_list


def get_sequential_color_list(palette_name: str, n: int) -> list:
    colors = color_dict.get(palette_name)
    low_color = colors[0]
    high_color = colors[1]
    return create_sequential_color_list(low_color=low_color, high_color=high_color, n=n)


if color_dict is not None:
    for k, v in color_dict.items():
        sequential_colors[k] = create_sequential_color_list(v[0], v[1], n=10)
