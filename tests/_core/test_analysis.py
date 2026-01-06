import unittest
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly_presentation._core.analysis import Analysis


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = Analysis()
        # Create a simple figure for testing
        self.analysis.figure = go.Figure()
        self.analysis.figure.add_trace(go.Scatter(x=[0, 1], y=[0, 1]))

    def test_adjust_yaxis_updates_range_and_adds_trace(self):
        y_range = [0, 100]
        fig = self.analysis.adjust_yaxis(y_range)
        # Check yaxis range
        self.assertEqual(fig.layout.yaxis.range, (0, 100))
        # Check that a new trace was added (sinus curve)
        self.assertGreaterEqual(len(fig.data), 2)
        # Check that the last trace is the sinus curve
        last_trace = fig.data[-1]
        self.assertIsInstance(last_trace, go.Scatter)
        self.assertEqual(last_trace.name, "sin_curve_1")
        self.assertEqual(last_trace.xaxis, "x2")
        # Check that the legend is hidden
        self.assertFalse(fig.layout.showlegend)

    def test_adjust_yaxis_with_different_range(self):
        y_range = [10, 20]
        fig = self.analysis.adjust_yaxis(y_range)
        self.assertEqual(fig.layout.yaxis.range, (10, 20))
        last_trace = fig.data[-1]
        # Check that the y values are within the specified range
        self.assertTrue(
            np.all(
                (last_trace.y >= min(y_range))
                & (last_trace.y <= max(y_range) + (y_range[1] - y_range[0]) * 0.2)
            )
        )

    def test_comparison_wrapper(self):
        self.analysis.figure = None
        df = pd.DataFrame(
            {
                "Country": [
                    "Germany",
                    "France",
                    "Italy",
                    "Spain",
                    "Denmark",
                ],
                "Percentage": [
                    90,
                    80,
                    70,
                    60,
                    50,
                ],
                "pivot": [*["other"] * 5],
            }
        )
        self.analysis.comparison.horisontal_stacked_bar_with_total(
            df=df,
            x="Percentage",
            y="Country",
            calculate_total=True,
            total_formula="mean",
            total_as_first=True,
        )
        self.assertIsInstance(self.analysis.figure, go.Figure)

    def test_price_volume_wrapper(self):
        self.analysis.figure = None
        df = pd.DataFrame(
            {
                "product": ["A", "B", "C", "A", "B", "C"],
                "price": [10, 15, 20, 11, 15, 23],
                "volume": [1000, 800, 500, 1000, 700, 800],
                "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
            }
        )

        self.analysis.price_volume.price_volume_mix_analysis(
            df=df,
            value_col="price",
            weight_col="volume",
            period_col="period",
            groupby_col="product",
            aggregated_output=True,
            show_text=True,
            text_format=".0f",
        )
        self.assertIsInstance(self.analysis.figure, go.Figure)


if __name__ == "__main__":
    unittest.main()
