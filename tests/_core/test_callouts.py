import unittest
from plotly_presentation._core.plotter import Plotter
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


class CalloutTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    # Arrow diff tests
    def test_valid_arrow_diff(self):
        p = Plotter()
        p.express(
            type="bar",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
            barmode="group",
        )
        p.callout.add_line_differences(
            primary_trace_name="b",
            text_type="ratio",
            text_format=".1f",
            y_text_offset=0.1,
        )
        self.assertEqual(type(p.figure), go.Figure)

    def test_second_trace_growth(self):
        p = Plotter()
        p.express(
            type="bar", x=["cat1", "cat1"], y=[1, 3], color=["a", "b"], barmode="group"
        )
        p.callout.add_line_differences(
            primary_trace_name="b",
            text_type="ratio",
            text_format=".1f",
            y_text_offset=0.1,
        )
        line_annotation = p.figure.layout.annotations[0]
        self.assertEqual(line_annotation.x < 0.5, True)

    def test_second_trace_decline(self):
        p = Plotter()
        p.express(
            type="bar", x=["cat1", "cat1"], y=[3, 1], color=["a", "b"], barmode="group"
        )
        p.callout.add_line_differences(
            primary_trace_name="b",
            text_type="ratio",
            text_format=".1f",
            y_text_offset=0.1,
        )
        line_annotation = p.figure.layout.annotations[0]
        self.assertEqual(line_annotation.x > 0.5, True)

    def test_first_trace_decline(self):
        p = Plotter()
        p.express(
            type="bar", x=["cat1", "cat1"], y=[3, 1], color=["a", "b"], barmode="group"
        )
        p.callout.add_line_differences(
            primary_trace_name="a",
            text_type="ratio",
            text_format=".1f",
            y_text_offset=0.1,
        )
        line_annotation = p.figure.layout.annotations[0]
        self.assertEqual(line_annotation.x > 0.5, True)

    def test_first_trace_growth(self):
        p = Plotter()
        p.express(
            type="bar", x=["cat1", "cat1"], y=[1, 3], color=["a", "b"], barmode="group"
        )
        p.callout.add_line_differences(
            primary_trace_name="a",
            text_type="ratio",
            text_format=".1f",
            y_text_offset=0.1,
        )
        line_annotation = p.figure.layout.annotations[0]
        self.assertEqual(line_annotation.x < 0.5, True)

    # Test circle highlights
    def test_circle_highlight_annotation_shape_count(self):
        p = Plotter()
        p.express(
            type="bar",
            x=[1, 2, 3],
            y=[1, 2, 3],
        )
        p.callout.add_circle_highlight(x=2, y=3, text="1")
        annotation_count = len(p.figure.layout.annotations)
        shape_count = len(p.figure.layout.shapes)
        self.assertEqual(annotation_count, 1)
        self.assertEqual(shape_count, 1)

    def test_end_line_marker_count_full(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.callout.add_line_end_marker()
        trace_count = len(p.figure.data)
        self.assertEqual(trace_count, 6)

    def test_end_line_marker_count_selected(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.callout.add_line_end_marker(
            traces=["GOOG", "FB"],
        )
        trace_count = len(p.figure.data)
        self.assertEqual(trace_count, 5)

    def test_end_line_marker_text_format_value(self):
        p = Plotter()
        p.express(
            type="line",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
        )
        p.callout.add_line_end_marker(
            traces=["a"],
            text_type="value",
            text_format=".2f",
        )
        expected_text = "4.00"
        for t in p.figure.select_traces(selector={"name": "a_marker"}):
            actual_text = t.text[0]
            self.assertEqual(expected_text, actual_text)

    def test_end_line_marker_text_format_category(self):
        p = Plotter()
        p.express(
            type="line",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
        )
        p.callout.add_line_end_marker(
            traces=["a"],
            text_type="category",
        )
        expected_text = "a"
        for t in p.figure.select_traces(selector={"name": "a_marker"}):
            actual_text = t.text[0]
            self.assertEqual(expected_text, actual_text)

    def test_end_line_marker_text_format_value_category(self):
        p = Plotter()
        p.express(
            type="line",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
        )
        p.callout.add_line_end_marker(
            traces=["a"],
            text_type="value+category",
            text_format=".0f",
        )
        expected_text = "4<br>a"
        for t in p.figure.select_traces(selector={"name": "a_marker"}):
            print(t)
            actual_text = t.text[0]
            self.assertEqual(expected_text, actual_text)

    def test_end_line_marker_text_format_category_value(self):
        p = Plotter()
        p.express(
            type="line",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
        )
        p.callout.add_line_end_marker(
            traces=["a"],
            text_type="category+value",
            text_format=".0f",
        )
        expected_text = "a<br>4"
        for t in p.figure.select_traces(selector={"name": "a_marker"}):
            print(t)
            actual_text = t.text[0]
            self.assertEqual(expected_text, actual_text)

    def test_end_line_marker_text_format_unknown_text_type(self):
        p = Plotter()
        p.express(
            type="line",
            x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            y=[1, 3, 2, 3, 3, 2, 4, 4],
            color=["a", "b", "a", "b", "a", "b", "a", "b"],
        )

        with self.assertRaises(AttributeError) as context:
            p.callout.add_line_end_marker(
                traces=["a"],
                text_type="unknown",
            )
            self.assertEqual(
                str(context.exception),
                "The text type must be on of the following: {_VALID_TEXT_TYPES}",
            )

    def test_get_center_point_categorical_x(self):
        p = Plotter()
        p.express(
            type="bar",
            x=["cat1", "cat2", "cat3", "cat4"],
            y=[1, 2, 3, 4],
            barmode="group",
        )
        actual_center = p.callout._get_center_point(a="cat1", b="cat3", axis="x")
        expected_center = 1
        self.assertEqual(actual_center, expected_center)

    def test_get_center_point_categorical_y(self):
        p = Plotter()
        p.express(
            type="bar",
            y=["cat1", "cat2", "cat3", "cat4"],
            x=[1, 2, 3, 4],
            barmode="group",
        )
        actual_center = p.callout._get_center_point(a="cat1", b="cat3", axis="y")
        expected_center = 1
        self.assertEqual(actual_center, expected_center)

    def test_get_center_point_numerical_x(self):
        p = Plotter()
        p.express(
            type="bar",
            x=[1, 2, 3, 4],
            y=[1, 2, 3, 4],
            barmode="group",
        )
        actual_center = p.callout._get_center_point(a=1, b=4, axis="x")
        expected_center = 2.5
        self.assertEqual(actual_center, expected_center)

    def test_get_center_point_numerical_y(self):
        p = Plotter()
        p.express(
            type="bar",
            y=[1, 2, 3, 4],
            x=[1, 2, 3, 4],
            barmode="group",
        )
        actual_center = p.callout._get_center_point(a=1, b=4, axis="y")
        expected_center = 2.5
        self.assertEqual(actual_center, expected_center)

    def test_get_center_point_date_x(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y="GOOG")
        print(p.figure.data[0].x)
        actual_center = p.callout._get_center_point(
            a="2018-01-08", b="2018-01-22", axis="x"
        )
        print(actual_center)
        expected_center = pd.to_datetime("2018-01-15 00:00:00")
        self.assertEqual(actual_center, expected_center)

    def test_valid_circle_shapes(self):
        p = Plotter()
        try:
            p.callout.add_circle_highlight(x=0, y=0, shape_form="round")
        except ValueError:
            self.fail("'round' is a valid input shape.")

        try:
            p.callout.add_circle_highlight(x=0, y=0, shape_form="oval")
        except ValueError:
            self.fail("'oval' is a valid input shape.")

    def test_default_circle_highlight_size(self):
        p = Plotter()
        p.callout.add_circle_highlight(x=0, y=0)
        expected_radius = p.callout._DEFAULT_CIRCLE_SIZE.get("circular_radius")
        actual_x_radius = p.figure.layout.shapes[0]["x1"]
        actual_y_radius = p.figure.layout.shapes[0]["y1"]
        self.assertEqual(expected_radius, actual_x_radius)
        self.assertEqual(expected_radius, actual_y_radius)

    def test_square_growth_line(self):
        p = Plotter()
        p.callout.add_square_growth_line(x0=0, y0=0, x1=1, y1=1, y_top=1.5)

        expected_vertical_1 = {
            "x0": 0,
            "y0": 0,
            "x1": 0,
            "y1": 1.5,
        }
        expected_horisontal = {
            "x0": 0,
            "y0": 1.5,
            "x1": 1,
            "y1": 1.5,
        }
        expected_vertical_2 = {
            "x0": 1,
            "y0": 1.5,
            "x1": 1,
            "y1": 1,
        }
        expected_shapes = [
            expected_vertical_1,
            expected_horisontal,
            expected_vertical_2,
        ]
        for expected_shape, s in zip(expected_shapes, p.figure.layout.shapes):
            actual_shape = {
                "x0": s["x0"],
                "y0": s["y0"],
                "x1": s["x1"],
                "y1": s["y1"],
            }
            self.assertEqual(actual_shape, expected_shape)

    def test_dash_growth_lines_no_text(self):
        p = Plotter()
        p.callout.add_dash_growth_lines(x0=0, y0=0, x1=1, y1=1, x_end=1.5)

        expected_dash_1 = {
            "x0": 0,
            "y0": 0,
            "x1": 1.5,
            "y1": 0,
        }
        expected_dash_2 = {
            "x0": 1,
            "y0": 1,
            "x1": 1.5,
            "y1": 1,
        }
        expected_shapes = [
            expected_dash_1,
            expected_dash_2,
        ]
        for expected_shape, s in zip(expected_shapes, p.figure.layout.shapes):
            actual_shape = {
                "x0": s["x0"],
                "y0": s["y0"],
                "x1": s["x1"],
                "y1": s["y1"],
            }
            self.assertEqual(actual_shape, expected_shape)

        actual_shapes = len(p.figure.layout.shapes)
        self.assertEqual(actual_shapes, 2)

        actual_annotations = len(p.figure.layout.annotations)
        self.assertEqual(actual_annotations, 1)

    def test_dash_growth_lines_no_text(self):
        p = Plotter()
        p.callout.add_dash_growth_lines(x0=0, y0=0, x1=1, y1=1, x_end=1.5, text="s")

        expected_dash_1 = {
            "x0": 0,
            "y0": 0,
            "x1": 1.5,
            "y1": 0,
        }
        expected_dash_2 = {
            "x0": 1,
            "y0": 1,
            "x1": 1.5,
            "y1": 1,
        }
        expected_shapes = [
            expected_dash_1,
            expected_dash_2,
        ]
        for expected_shape, s in zip(expected_shapes, p.figure.layout.shapes):
            actual_shape = {
                "x0": s["x0"],
                "y0": s["y0"],
                "x1": s["x1"],
                "y1": s["y1"],
            }
            self.assertEqual(actual_shape, expected_shape)

        actual_shapes = len(p.figure.layout.shapes)
        self.assertEqual(actual_shapes, 3)

        actual_annotations = len(p.figure.layout.annotations)
        self.assertEqual(actual_annotations, 2)
