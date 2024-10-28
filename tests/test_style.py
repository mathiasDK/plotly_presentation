import unittest
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.colors import SequentialColor, DivergentColor
import plotly.express as px


class CalloutTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    def test_set_color_palette_color_dict(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.line.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_set_color_palette_palette_sequential(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="reds")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(249.0, 143.0, 112.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_sequential_negative(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="hot_cold")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(96.0, 116.0, 141.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging", palette_name="reds")

        actual_colors = {d.name: d.line.color for d in p.figure.data}
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "AAPL": "rgb(194.0, 194.0, 194.0)",
            "FB": "rgb(148.0, 12.0, 8.0)",
        }
        self.assertEqual(actual_colors, expected_colors)
