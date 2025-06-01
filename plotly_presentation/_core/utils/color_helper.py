def adjust_color_brightness(color, level):
    """
    Adjusts the brightness of a color.

    Args:
        color (str or tuple): Color in hex format (e.g. "#RRGGBB") or RGB tuple (R, G, B).
        level (int): Integer from -5 (darker) to +5 (lighter).

    Returns:
        tuple: Adjusted RGB tuple (R, G, B).
    """
    if not isinstance(level, int) or not -5 <= level <= 5:
        raise ValueError("level must be an integer between -5 and 5")

    # Convert hex to RGB if needed
    if isinstance(color, str):
        color = color.lstrip('#')
        if len(color) == 6:
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        else:
            raise ValueError("Hex color must be in format '#RRGGBB'")
    elif isinstance(color, tuple) and len(color) == 3:
        r, g, b = color
    else:
        raise ValueError("color must be a hex string or an RGB tuple")

    # Calculate adjustment factor
    factor = 1 + (level / 10.0)

    def clamp(x):
        return max(0, min(255, int(round(x))))

    r = clamp(r * factor)
    g = clamp(g * factor)
    b = clamp(b * factor)

    # Convert back to hex string
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return hex_color