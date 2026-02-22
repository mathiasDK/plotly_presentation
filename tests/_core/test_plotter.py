import unittest
from plotly_presentation._core.plotter import Plotter
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class PlotterTests(unittest.TestCase):
    def test_valid_express(self):
        p = Plotter()
        p.express(type="bar", x=[1, 2, 3], y=[1, 2, 3])
        self.assertEqual(type(p.figure), go.Figure)

    def test_invalid_express_type(self):
        p = Plotter()
        with self.assertRaises(Exception) as context:
            p.express(type="some-invalid-plot-type", x=[1, 2, 3], y=[1, 2, 3])

        self.assertTrue(
            "module 'plotly.express' has no attribute 'some-invalid-plot-type'"
            in str(context.exception)
        )

    def test_valid_add_trace(self):
        p = Plotter()
        p.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3]))
        self.assertEqual(type(p.figure), go.Figure)

    # Added tests for Plotly subplots figures
    def test_make_subplots_layout_axes(self):
        fig = make_subplots(rows=1, cols=2)
        p = Plotter(figure=fig)
        self.assertIsInstance(p.figure, go.Figure)

    def test_add_trace_to_subplot_assigns_axis(self):
        fig = make_subplots(rows=1, cols=2)
        p = Plotter(figure=fig)
        p.add_trace(go.Bar(x=[1], y=[1]), row=1, col=2)
        self.assertEqual(p.figure.data[-1].xaxis, "x2")


if __name__ == "__main__":
    unittest.main()
