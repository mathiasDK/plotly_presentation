import plotly.graph_objs as go
from plotly_presentation._core.colors import CalloutColor
from plotly_presentation._core.options import options
from plotly_presentation._core.utils.dict_funcs import update_dict


class Callout:
    def __init__(self, figure) -> None:
        self.figure = figure

        styles = self.__create_default_styles()

        self._DEFAULT_LINE_STYLE = styles["default_line_style"]
        self._DEFAULT_DASH_LINE_STYLE = styles["default_dash_line_style"]
        self._DEFAULT_ARROW_STYLE = styles["default_arrow_style"]
        self._DEFAULT_TEXT_STYLE = styles["default_text_style"]

    def __create_default_styles(self) -> dict:
        color_styles = {
            "default_line_style": {
                "line": {
                    "color": CalloutColor.LINE_COLOR.value,
                }
            },
            "default_dash_line_style": {
                "line": {
                    "color": CalloutColor.LINE_COLOR.value,
                },
            },
            "default_arrow_style": {
                "arrowcolor": CalloutColor.LINE_COLOR.value,
            },
            "default_text_style": {
                "bgcolor": CalloutColor.TEXT_BG_COLOR.value,
                "font": {
                    "color": CalloutColor.TEXT_COLOR.value,
                },
            },
        }
        styles = options.get_option("config.callout_settings")
        styles = update_dict(color_styles, styles)
        return styles

    def _get_center_point(self, a, b, axis="x"):
        """Finding the middle point between the two points given on the axis specified.

        Given the axis is categorical then the middle point is calculated by extracting the indexes of `a` and `b`. 
        The index values are then used to calculate the middle point.

        Args:
            a (any): The value of the first point.
            b (any): The value of the second point.
            axis (str, optional): The axis where the midpoint is calculated. Defaults to "x".

        Returns:
            float: A numeric value which is the middle point between a and b.
        """
        # Only works for numeric and str
        if isinstance(a, str):
            vals = self.figure.data[0][axis]
            a, b = list(vals).index(a), list(vals).index(b)
        return (b - a) / 2.0 + a

    def add_square_growth_line(self, x0, x1, y0, y1, y_top, text=None) -> go.Figure:

        # creating points
        l1 = {"x0": x0, "y0": y0, "x1": x0, "y1": y_top}
        l2 = {"x0": x0, "y0": y_top, "x1": x1, "y1": y_top}
        l3 = {
            "x0": x1,
            "y0": y_top,
            "x1": x1,
            "y1": y1,
        }

        for l in [l1, l2, l3]:
            self.figure.add_shape(**l, **self._DEFAULT_LINE_STYLE)

        if text is not None:
            self.figure.add_annotation(
                text=text,
                x=self._get_center_point(x0, x1),
                y=y_top,
                **self._DEFAULT_TEXT_STYLE,
            )

        return self.figure

    def add_dash_growth_lines(self, x0, x1, x_end, y0, y1, text) -> go.Figure:
        l1 = {"x0": x0, "x1": x_end, "y0": y0, "y1": y0}
        l2 = {"x0": x1, "x1": x_end, "y0": y1, "y1": y1}
        for l in [l1, l2]:
            self.figure.add_shape(**l, **self._DEFAULT_DASH_LINE_STYLE)
        self.figure.add_annotation(
            x=x_end, ax=x_end, y=y1, ay=y0, **self._DEFAULT_ARROW_STYLE
        )
        self.figure.add_annotation(
            x=x_end,
            y=self._get_center_point(y0, y1),
            text=text,
            **self._DEFAULT_TEXT_STYLE,
        )
        return self.figure
