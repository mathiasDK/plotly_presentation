import unittest
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.colors import SequentialColor, DivergentColor
from plotly_presentation._core.style import Style
import plotly.graph_objects as go
import plotly.express as px


class StyleTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    def test_set_color_palette_color_dict_line(self):
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

    def test_set_color_palette_palette_sequential_line(self):
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

    def test_set_color_palette_palette_sequential_negative_line(self):
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

    def test_set_color_palette_palette_diverging_line(self):
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

    def test_set_color_palette_color_dict_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.marker.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_set_color_palette_palette_sequential_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="reds")

        actual_colors = {
            d.name: d.marker.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(249.0, 143.0, 112.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_sequential_negative_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="hot_cold")

        actual_colors = {
            d.name: d.marker.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(96.0, 116.0, 141.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging", palette_name="reds")

        actual_colors = {d.name: d.marker.color for d in p.figure.data}
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "AAPL": "rgb(194.0, 194.0, 194.0)",
            "FB": "rgb(148.0, 12.0, 8.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_color_dict_scatter(self):
        p = Plotter()
        p.express(
            type="scatter", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"]
        )

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.line.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_waterfall_style(self):
        figure = go.Figure(
            go.Waterfall(
                name="20",
                orientation="v",
                measure=[
                    "relative",
                    "relative",
                    "total",
                    "relative",
                    "relative",
                    "total",
                ],
                x=[
                    "Sales",
                    "Consulting",
                    "Net revenue",
                    "Purchases",
                    "Other expenses",
                    "Profit before tax",
                ],
                textposition="outside",
                text=["+60", "+80", "", "-40", "-20", "Total"],
                y=[60, 80, 0, -40, -20, 0],
            )
        )
        s = Style(figure, slide_layout="slide_100%")
        s._apply_waterfall_style()

        actual_colors = {
            "increase": s.figure.data[0].increasing.marker.color,
            "decrease": s.figure.data[0].decreasing.marker.color,
            "totals": s.figure.data[0].totals.marker.color,
            "connectors": s.figure.data[0].connector.line.color,
        }
        expected_colors = {
            "increase": "#4c8a8e",
            "decrease": "#8E504C",
            "totals": "#CFD6D5",
            "connectors": "black",
        }
        self.assertEqual(actual_colors, expected_colors)
