from plotly.express.colors import hex_to_rgb, label_rgb


def _convert_to_rgb(color):
    if color[0] == "#":
        color = hex_to_rgb(color)
    elif isinstance(color, tuple):
        color = label_rgb(color)
    return color
