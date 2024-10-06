import unittest
from plotly_presentation._core.plotter import Plotter
import plotly.graph_objs as go


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


if __name__ == "__main__":
    unittest.main()
