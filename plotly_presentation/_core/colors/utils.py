from plotly.express.colors import hex_to_rgb, label_rgb, convert_to_RGB_255


def _convert_to_rgb(color):
    if color[0] == "#":
        color = hex_to_rgb(color)
        # color = label_rgb(color)
    elif isinstance(color, tuple):
        # color = convert_to_RGB_255(color)
        color = label_rgb(color)
    return color
