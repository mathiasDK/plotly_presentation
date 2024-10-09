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
        self._DEFAULT_SMALL_TEXT_STYLE = styles["default_small_text_style"]
        self._DEFAULT_CIRCLE_STYLE = styles["default_circle_style"]
        self._DEFAULT_CIRCLE_TEXT_STYLE = styles["default_circle_text_style"]
        self._DEFAULT_CIRCLE_SIZE = styles["default_circle_size"]

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
            "default_small_text_style": {
                "bgcolor": CalloutColor.TEXT_BG_COLOR.value,
                "font": {
                    "color": CalloutColor.TEXT_COLOR.value,
                },
            },
            "default_circle_style": {
                "line": {
                    "color": CalloutColor.CIRCLE_LINE_COLOR.value,
                },
                "fillcolor": CalloutColor.CIRCLE_FILL_COLOR.value,
            },
            "default_circle_text_style": {
                "font": {
                    "color": CalloutColor.TEXT_COLOR.value,
                },
            },
        }
        styles = options.get_option("config.callout_settings")
        styles = update_dict(color_styles, styles)
        return styles

    def _get_center_point(self, a, b, axis="x"):
        # Only works for numeric and str
        if isinstance(a, str):
            vals = self.figure.data[0][axis]
            a, b = list(vals).index(a), list(vals).index(b)
        return (b - a) / 2.0 + a

    def add_circle_highlight(
        self,
        x,
        y,
        circle_x_pixel_width=None,
        circle_y_pixel_width=None,
        shape_form="round",
        text=None,
        text_format=":.1f",
        **kwargs
    ) -> go.Figure:
        _VALID_SHAPE_FORMS = ["round", "oval"]
        if shape_form not in _VALID_SHAPE_FORMS:
            raise AttributeError(
                f"The shape of the circle must be on of the following: {_VALID_SHAPE_FORMS}"
            )
        if shape_form == "round":
            if circle_x_pixel_width is None:
                circle_x_pixel_width = self._DEFAULT_CIRCLE_SIZE.get("circular_radius")
                circle_y_pixel_width = self._DEFAULT_CIRCLE_SIZE.get("circular_radius")
        else:
            if circle_x_pixel_width is None:
                circle_x_pixel_width = self._DEFAULT_CIRCLE_SIZE.get("oval_x_width")
            if circle_y_pixel_width is None:
                circle_y_pixel_width = self._DEFAULT_CIRCLE_SIZE.get("oval_y_width")

        self.figure.add_shape(
            xanchor=x,
            yanchor=y,
            x0=-circle_x_pixel_width,
            x1=circle_x_pixel_width,
            y0=-circle_y_pixel_width,
            y1=circle_y_pixel_width,
            **self._DEFAULT_CIRCLE_STYLE,
            **kwargs
        )
        if text is not None:
            self.figure.add_annotation(
                x=x, y=y, text=f"{text}".format(text_format), **self._DEFAULT_CIRCLE_TEXT_STYLE, **kwargs
            )
        return self.figure

    def add_square_growth_line(
        self,
        x0,
        x1,
        y0,
        y1,
        y_top,
        circle_x_pixel_width=None,
        circle_y_pixel_width=None,
        text=None,
    ) -> go.Figure:

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
            self.add_circle_highlight(
                x=self._get_center_point(x0, x1),
                y=y_top,
                circle_x_pixel_width=circle_x_pixel_width,
                circle_y_pixel_width=circle_y_pixel_width,
                text=text,
                shape_form="oval",
            )

        return self.figure

    def add_dash_growth_lines(
        self,
        x0,
        x1,
        x_end,
        y0,
        y1,
        circle_x_pixel_width=None,
        circle_y_pixel_width=None,
        text=None,
    ) -> go.Figure:
        l1 = {"x0": x0, "x1": x_end, "y0": y0, "y1": y0}
        l2 = {"x0": x1, "x1": x_end, "y0": y1, "y1": y1}
        for l in [l1, l2]:
            self.figure.add_shape(**l, **self._DEFAULT_DASH_LINE_STYLE)

        # Arrow
        self.figure.add_annotation(
            x=x_end, ax=x_end, y=y1, ay=y0, **self._DEFAULT_ARROW_STYLE
        )
        if text is not None:
            self.add_circle_highlight(
                x=x_end,
                y=self._get_center_point(y0, y1),
                circle_x_pixel_width=circle_x_pixel_width,
                circle_y_pixel_width=circle_y_pixel_width,
                text=text,
                shape_form="oval",
            )
        return self.figure

    def add_line_differences(
        self,
        primary_trace_name,
        secondary_trace_name,
        text_type=None,
        text_format=":.1f",
        y_offset=0
    ) -> go.Figure:
        
        if text_type is not None:
            _VALID_TEXT_TYPES = ["percentage", "difference"]
            if text_type not in _VALID_TEXT_TYPES:
                raise AttributeError(
                    f"The text type must be on of the following: {_VALID_TEXT_TYPES}"
                )
        if len(self.figure.data) != 2:
            raise AttributeError("Need at two traces to compare")
        if type(self.figure.data[0]) != go._bar.Bar:
            raise AttributeError("Only works with bar charts")
        primary_first = None
        for i, d in enumerate(self.figure.data):
            if d.name == primary_trace_name:
                primary_xs = list(d.x)
                primary_ys = list(d.y)
                primary_first = i==0
            elif d.name == secondary_trace_name:
                comparison_xs = list(d.x)
                comparison_ys = list(d.y)

        if primary_first is None:
            raise AttributeError("Could not find the traces - please provide the actual trace names")

        if self.figure.layout.bargap is not None:
            bargap = self.figure.layout.bargap
        else:
            bargap = self.figure.layout.template.layout.bargap

        # Adding a hidden extra xaxis to the figure
        self.figure.layout.xaxis2 = go.layout.XAxis(
            overlaying='x', range=[0, len(primary_xs)], showticklabels=False)
        
        # Starting to plot the lines
        for i, (primary_x, primary_y) in enumerate(zip(primary_xs, primary_ys)):
            comparison_y = comparison_ys[comparison_xs.index(primary_x)]
            diff = comparison_y - primary_y
            if primary_first:
                if diff > 0:
                    x = i + bargap/2 + (1-bargap)/4
                elif diff < 0:
                    x = i + 1 - bargap/2 - (1-bargap)/4
                else:
                    continue
            elif ~primary_first:
                if diff > 0:
                    x = i + 1 - bargap/2 - (1-bargap)/4
                elif diff < 0:
                    x = i + bargap/2 + (1-bargap)/4
                else:
                    continue
            else:
                continue           

            # y_mid = diff/2 + primary_y
            self.figure.add_shape(
                **self._DEFAULT_DASH_LINE_STYLE,
                x0=x,
                x1=x,
                y0=primary_y,
                y1=comparison_y,
                xref="x2"
            )
            if text_type is not None:
                if text_type == 'percentage':
                    text = f"{diff/primary_y:{text_format}}"
                elif text_type == 'difference':
                    text = f"{diff:{text_format}}"
                self.figure.add_annotation(
                    x=x,
                    y=max(comparison_y, primary_y)+y_offset,
                    text=f"<b>{text}</b>",
                    xref="x2",
                    **self._DEFAULT_SMALL_TEXT_STYLE
                )
        return self.figure