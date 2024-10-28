from plotly.express.colors import n_colors, label_rgb
from .utils import _convert_to_rgb
from plotly_presentation._core.options import options
import numpy as np


color_dict = options.get_option("config.colors").get("custom_diverging")
diverging_colors = {}


def create_diverging_color_list(low_color, mid_color, high_color, n) -> list:
    low_color = _convert_to_rgb(low_color)
    mid_color = _convert_to_rgb(mid_color)
    high_color = _convert_to_rgb(high_color)

    if low_color[:3] == "rgb":
        color_type = "rgb"
    else:
        color_type = "tuple"

    if n % 2 == 0:
        low_colors = n_colors(
            lowcolor=low_color,
            highcolor=mid_color,
            n_colors=int(np.ceil(n / 2) + 1),
            colortype=color_type,
        )
        high_colors = n_colors(
            lowcolor=mid_color,
            highcolor=high_color,
            n_colors=int(np.ceil(n / 2) + 1),
            colortype=color_type,
        )
        diverging_color_list = (
            low_colors[:-1] + high_colors[1:]
        )  # ensuring that the mid color isn't shown twice
    else:
        low_colors = n_colors(
            lowcolor=low_color,
            highcolor=mid_color,
            n_colors=int(np.ceil(n / 2)),
            colortype=color_type,
        )
        high_colors = n_colors(
            lowcolor=mid_color,
            highcolor=high_color,
            n_colors=int(np.ceil(n / 2)),
            colortype=color_type,
        )
        diverging_color_list = (
            low_colors + high_colors[1:]
        )  # ensuring that the mid color isn't shown twice
    diverging_color_list = [label_rgb(color) for color in diverging_color_list]
    return diverging_color_list


def get_diverging_color_list(palette_name: str, n: int) -> list:
    colors = color_dict.get(palette_name)
    low_color = colors[0]
    mid_color = colors[1]
    high_color = colors[2]
    return create_diverging_color_list(
        low_color=low_color, mid_color=mid_color, high_color=high_color, n=n
    )


if color_dict is not None:
    for k, v in color_dict.items():
        diverging_colors[k] = create_diverging_color_list(v[0], v[1], v[2], n=10)
