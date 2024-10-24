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
        """Finding the middle point between the two points given on the axis specified.

        Given the axis is categorical then the middle point is calculated by extracting the indexes of `a` and `b`.
        The index values are then used to calculate the middle point.

        Args:
            a (any):
                The value of the first point.
            b (any):
                The value of the second point.
            axis (str, optional):
                The axis where the midpoint is calculated. Defaults to "x".

        Returns:
            float: A numeric value which is the middle point between a and b.
        """
        # Only works for numeric and str
        if isinstance(a, str):
            vals = self.figure.data[0][axis]
            a, b = list(vals).index(a), list(vals).index(b)
        return (b - a) / 2.0 + a

    def add_circle_highlight(
        self,
        x,
        y,
        circle_x_pixel_width: int = None,
        circle_y_pixel_width: int = None,
        shape_form="round",
        text: str = None,
        text_format: str = ":.1f",
        **kwargs,
    ) -> go.Figure:
        """Adding a circle to the graph.

        For further documentation you should explore the plotly docs for adding shapes where the xsizemode and ysizemode is pixel.

        Args:
            x (any):
                The center point for the circle on the x axis.
            y (any):
                The center point for the circle on the y axis.
            circle_x_pixel_width (int, optional):
                How many pixels the circle should be on the x axis. If long texts then you can adjust manually here. Defaults to None.
            circle_y_pixel_width (int, optional):
                How many pixels the circle should be on the y axis. If long texts then you can adjust manually here. Defaults to None.
            shape_form (str, optional):
                The shape of the circle. This can either be oval or round. If circle_x_pixel_width or circle_y_pixel_width they will override. Defaults to "round".
            text (str, optional):
                The text inside the buble. Defaults to None.

        Raises:
            AttributeError: Given there isn't enough data to create the circle.

        Returns:
            go.Figure: The plotly figure.
        """
        _VALID_SHAPE_FORMS = ["round", "oval"]
        if (
            shape_form not in _VALID_SHAPE_FORMS
            and circle_x_pixel_width is None
            and circle_y_pixel_width is None
        ):
            raise AttributeError(
                f"You must provide a shape for the circle: {_VALID_SHAPE_FORMS} or specify the size of the circle with `circle_x_pixel_width` and `circle_y_pixel_width`"
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
            **kwargs,
        )
        if text is not None:
            self.figure.add_annotation(
                x=x,
                y=y,
                text=f"{text}".format(text_format),
                **self._DEFAULT_CIRCLE_TEXT_STYLE,
                **kwargs,
            )
        return self.figure

    def add_square_growth_line(
        self,
        x0,
        x1,
        y0: float,
        y1: float,
        y_top: float,
        circle_x_pixel_width: int = None,
        circle_y_pixel_width: int = None,
        text: str = None,
    ) -> go.Figure:
        """Creating a set of lines going up from one bar across and down to another.
        An example can be found in the examples/ folder.

        The text will be shown on the middle of the line going across.

        Args:
            x0 (any):
                The x of the first vertical line.
            x1 (any):
                The x of the second vertical line.
            y0 (float):
                The y of the starting point for the first vertical line.
            y1 (float):
                The y of the starting point for the second vertical line
            y_top (float):
                The y position of both vertical lines and the position of the line across.
            circle_x_pixel_width (int, optional):
                How many pixels the circle should be on the x axis. If long texts then you can adjust manually here. Defaults to None.
            circle_y_pixel_width (int, optional):
                How many pixels the circle should be on the y axis. If long texts then you can adjust manually here. Defaults to None.
            text (str, optional):
                The text written in the highlighted circle. Defaults to None.

        Returns:
            go.Figure: The plotly figure.
        """

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
        x0: float,
        x1: float,
        x_end: float,
        y0: float,
        y1: float,
        circle_x_pixel_width: int = None,
        circle_y_pixel_width: int = None,
        text: str = None,
    ) -> go.Figure:
        """Adding two horisontal dashed lines from the given points, one arrow (up or down), and some text to describe the difference.

        Args:
            x0 (float):
                The x position of the first point. Note that even if the x axis is categorical, then you can specify the index of the point which is then being used.
            x1 (float):
                The x position of the second point. Note that even if the x axis is categorical, then you can specify the index of the point which is then being used.
            x_end (float):
                The position of where the arrow must be, and where the two dashed lines will stop.
                This should be outside the actual plot area, e.g. if there are 4 bars, then specify 4.2.
            y0 (float):
                The y position of the first dashed line.
            y1 (float):
                The y position of the second dashed line.
            circle_x_pixel_width (int, optional):
                How many pixels the circle should be on the x axis. If long texts then you can adjust manually here. Defaults to None.
            circle_y_pixel_width (int, optional):
                How many pixels the circle should be on the y axis. If long texts then you can adjust manually here. Defaults to None.
            text (str, optional):
                The text in the circle. If it is None then no text is shown. Defaults to None.

        Returns:
            go.Figure: The plotly figure.
        """

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
        primary_trace_name: str,
        text_type=None,
        text_format=".1f",
        y_text_offset: float = 0,
    ) -> go.Figure:
        """Adding a set of annotations to a group barchart with exactly two traces.
        The annotations compares the primary to the secondary trace and can plot various texts for comparison.

        Args:
            primary_trace_name (str):
                The name of the primary trace.
            secondary_trace_name (str):
                The name of the secondary trace.
            text_type (str, optional):
                The type of text comparison. Valid values are percentage, difference and ratio.
                Text examples:
                    - 'percentage' and text_format='.1%' = 10.5%
                    - 'difference' and text_format='.0f' = 10
                    - 'ratio' and text_format='.1f' = 10.5x
                If set to None then it won't show any text.
                Defaults to None.
            text_format (str, optional):
                The format of the text. This should be without the colon. Defaults to ".1f".
            y_text_offset (float, optional):
                How much above the horisontal line the text should be positioned. Defaults to 0.

        Returns:
            go.Figure: The plotly figure.
        """

        if text_type is not None:
            _VALID_TEXT_TYPES = ["percentage", "difference", "ratio"]
            if text_type not in _VALID_TEXT_TYPES:
                raise AttributeError(
                    f"The text type must be on of the following: {_VALID_TEXT_TYPES}"
                )
        if len(self.figure.data) != 2:
            raise AttributeError(
                "This can only be done when there are exactly two traces."
            )
        if self.figure.layout.barmode != "group":
            raise AttributeError(
                "The barmode must be group - the bars must be side by side."
            )
        if type(self.figure.data[0]) != go._bar.Bar:
            raise AttributeError("Only works with bar charts")
        primary_first = None
        for i, d in enumerate(self.figure.data):
            if d.name == primary_trace_name:
                primary_xs = list(d.x)
                primary_ys = list(d.y)
                primary_first = i == 0
            else:
                comparison_xs = list(d.x)
                comparison_ys = list(d.y)

        if primary_first is None:
            raise AttributeError(
                "Could not find the traces - please provide the actual trace names."
            )

        # Setting the bargap used to calculate the line positions.
        if self.figure.layout.bargap is not None:
            bargap = self.figure.layout.bargap
        else:
            bargap = self.figure.layout.template.layout.bargap

        if bargap is None:
            raise AttributeError(
                "Please specify a bargap - either in the layout or in the default theme."
            )

        # Adding a hidden extra xaxis to the figure
        self.figure.layout.xaxis2 = go.layout.XAxis(
            overlaying="x", range=[0, len(primary_xs)], showticklabels=False
        )

        # Starting to plot the lines
        for i, (primary_x, primary_y) in enumerate(zip(primary_xs, primary_ys)):
            comparison_y = comparison_ys[comparison_xs.index(primary_x)]
            diff = primary_y - comparison_y
            if text_type in ["ratio", "percentage"] and comparison_y == 0:
                # Do not show a diff if the comparison value is 0 and the type is ratio or percentage
                continue
            if primary_first:
                if diff < 0:
                    x = i + bargap / 2 + (1 - bargap) / 4
                    x0 = i + bargap / 2
                    x1 = i + bargap / 2 + (1 - bargap) / 2
                elif diff > 0:
                    x = i + 1 - bargap / 2 - (1 - bargap) / 4
                    x0 = i + 1 - bargap / 2
                    x1 = i + 1 - bargap / 2 - (1 - bargap) / 2
                else:
                    continue
            elif ~primary_first:
                if diff < 0:
                    x = i + 1 - bargap / 2 - (1 - bargap) / 4
                    x0 = i + 1 - bargap / 2
                    x1 = i + 1 - bargap / 2 - (1 - bargap) / 2
                elif diff > 0:
                    x = i + bargap / 2 + (1 - bargap) / 4
                    x0 = i + bargap / 2
                    x1 = i + bargap / 2 + (1 - bargap) / 2
                else:
                    continue
            else:
                continue

            y_max = max(comparison_y, primary_y)

            # Adding the line and arrow
            ARROW_STYLE = update_dict(
                self._DEFAULT_ARROW_STYLE, {"xref": "x2", "axref": "x2"}
            )
            self.figure.add_annotation(
                x=x,
                ax=x,
                y=primary_y,
                ay=comparison_y,
                **ARROW_STYLE,
                text="",
                bgcolor="rgba(0,0,0,0)",
            )
            self.figure.add_shape(  # horisontal line
                **self._DEFAULT_LINE_STYLE, x0=x0, x1=x1, y0=y_max, y1=y_max, xref="x2"
            )

            # Adding the text
            if text_type is not None:
                if text_type == "percentage":
                    text = f"{diff/comparison_y:{text_format}}"
                elif text_type == "difference":
                    text = f"{diff:{text_format}}"
                elif text_type == "ratio":
                    text = f"{primary_y/comparison_y:{text_format}}x"
                self.figure.add_annotation(
                    x=x,
                    y=y_max + y_text_offset,
                    text=f"<b>{text}</b>",
                    xref="x2",
                    **self._DEFAULT_SMALL_TEXT_STYLE,
                )
        return self.figure

    def add_line_end_marker(
        self,
        traces: list[str] | str = None,
        text_type: str = None,
        text_format: str = ".1f",
        text_positions: list[str] | str = None,
        marker_size: int = 10,
    ) -> go.Figure:
        """Creating a marker at the end of the line with optional text.

        Note that if the marker is set at the beginning of the line, then you must sort your data accordingly.
        It might also be necessary to adjust the range of the x axis.

        Args:
            traces (list[str] | str, optional):
                The names of the traces which should be highlighted. Defaults to None.
            text_type (str, optional):
                What should be text should be plotted. Defaults to None.
                If category is mentioned then the legend will be hidden.

                - 'value' = The value of the y axis.
                - 'category' = The name of the trace.
                - 'value+category' = The value of the y axis and the name of the trace.
                - 'category+value' = The name of the trace and the value of the y axis.
                - None = No text.
            text_format (str, optional):
                How the yaxis value should be formatted. Defaults to ".1f".
            text_positions (list[str] | str, optional):
                When the traces are close the text can tend to overlap. This can be used to adjust the position slightly.
                If it is None then the text position will be "middle right".
                Defaults to None.
            marker_size (int, optional):
                The size of the marker. Defaults to 10.

        Returns:
            go.Figure: The plotly figure.
        """

        if type(self.figure.data[0]) != go._scatter.Scatter:
            raise AttributeError("Only works with scatter charts")

        if traces is None:
            traces = [d.name for d in self.figure.data]
        elif isinstance(traces, str):
            traces = [traces]

        _VALID_TEXT_TYPES = ["value", "category", "value+category", "category+value"]
        if text_type is not None:
            if text_type not in _VALID_TEXT_TYPES:
                raise AttributeError(
                    f"The text type must be on of the following: {_VALID_TEXT_TYPES}"
                )

        if text_positions is None:
            text_positions = ["middle right"] * len(traces)

        showlegend = self.figure.layout.showlegend
        if showlegend is None:
            showlegend = True

        i = 0
        for d in self.figure.data:
            if d.name in traces:
                x = d.x[-1]
                y = d.y[-1]
                name = d.name
                color = d.line.color
                if text_type is None:
                    text = None
                elif text_type == "value":
                    text = f"{y:{text_format}}"
                elif text_type == "category":
                    showlegend = False
                    text = f"{name}"
                elif text_type == "value+category":
                    showlegend = False
                    text = f"{y:{text_format}}<br>{name}"
                elif text_type == "category+value":
                    showlegend = False
                    text = f"{name}<br>{y:{text_format}}"

                self.figure.add_trace(
                    go.Scatter(
                        x=[x],
                        y=[y],
                        mode="markers+text",
                        text=[text],
                        marker=dict(color=color, size=marker_size),
                        showlegend=False,
                        textposition=text_positions[i],
                    )
                )
                i += 1
        self.figure.update_layout(showlegend=showlegend)
        return self.figure
