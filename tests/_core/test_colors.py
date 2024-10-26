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
        p.style.set_color_palette(palette_type="sequential")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": SequentialColor.START.value,
            "FB": SequentialColor.END.value,
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_sequential_negative(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential_negative")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": SequentialColor.END.value,
            "FB": SequentialColor.START.value,
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging")

        actual_colors = {d.name: d.line.color for d in p.figure.data}
        expected_colors = {
            "GOOG": DivergentColor.START.value,
            "AAPL": DivergentColor.MID.value,
            "FB": DivergentColor.END.value,
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging_negative(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging_negative")

        actual_colors = {d.name: d.line.color for d in p.figure.data}
        expected_colors = {
            "GOOG": DivergentColor.END.value,
            "AAPL": DivergentColor.MID.value,
            "FB": DivergentColor.START.value,
        }
        self.assertEqual(actual_colors, expected_colors)
