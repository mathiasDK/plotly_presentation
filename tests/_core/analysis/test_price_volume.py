import unittest
from plotly_presentation._core.analysis_helper.price_volume import *
import pandas as pd


class UpdateDictTest(unittest.TestCase):
    def test_single_period_comparison(self):
        # Example from here https://www.investmentguide.co.uk/price-volume-price-volume-mix-revenue-bridges/
        df = pd.DataFrame(
            {
                "price": [10, 11],
                "volume": [100, 110],
                "period": ["FY23", "FY24"],
            }
        )
        x, y, measure = price_volume_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
        )
        expected_x = [
            ["FY23", "FY24", "FY24", "FY24"],
            [" ", "value_effect", "weight_effect", "  "],
        ]
        expected_y = [1000.0, 110.0, 100.0, 1210.0]
        expected_measure = ["absolute", "relative", "relative", "absolute"]
        self.assertListEqual(x, expected_x)
        self.assertListEqual(y, expected_y)
        self.assertListEqual(measure, expected_measure)

    def test_multiple_period_comparison(self):
        # Example from here https://accountancyindex.com/price-volume-mix-analysis/
        df = pd.DataFrame(
            {
                "price": [10, 11, 10],
                "volume": [100, 110, 100],
                "period": ["FY23", "FY24", "FY25"],
            }
        )
        x, y, measure = price_volume_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
        )
        expected_x = [
            ["FY23", "FY24", "FY24", "FY24", "FY25", "FY25", "FY25"],
            [
                " ",
                "value_effect",
                "weight_effect",
                "  ",
                "value_effect",
                "weight_effect",
                "   ",
            ],
        ]
        expected_y = [1000.0, 110.0, 100.0, 1210.0, -100.0, -110.0, 1000.0]
        expected_measure = [
            "absolute",
            "relative",
            "relative",
            "absolute",
            "relative",
            "relative",
            "absolute",
        ]
        self.assertListEqual(x, expected_x)
        self.assertListEqual(y, expected_y)
        self.assertListEqual(measure, expected_measure)
