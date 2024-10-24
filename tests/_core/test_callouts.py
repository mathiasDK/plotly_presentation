import unittest
from plotly_presentation._core.plotter import Plotter
import plotly.graph_objs as go
import plotly.express as px


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
