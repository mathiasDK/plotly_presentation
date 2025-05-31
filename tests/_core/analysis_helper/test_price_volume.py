import unittest
from plotly_presentation._core.analysis_helper.price_volume import *
import pandas as pd


class PriceVolumeTest(unittest.TestCase):
    def setUp(self):
        self.price_volume = PriceVolume()

    def test_single_period_comparison(self):
        # Example from here https://www.investmentguide.co.uk/price-volume-price-volume-mix-revenue-bridges/
        df = pd.DataFrame(
            {
                "price": [10, 11],
                "volume": [100, 110],
                "period": ["FY23", "FY24"],
            }
        )
        x, y, measure = self.price_volume._price_volume_analysis(
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
        x, y, measure = self.price_volume._price_volume_analysis(
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

    def test_single_period_comparison_aggregated(self):
        # Example from here https://accountancyindex.com/price-volume-mix-analysis/
        df = pd.DataFrame(
            {
                "product": ["A", "B", "C", "A", "B", "C"],
                "price": [10, 15, 20, 11, 15, 23],
                "volume": [1000, 800, 500, 1000, 700, 800],
                "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
            }
        )
        x, y, measure = self.price_volume._price_volume_mix_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
            groupby_col="product",
            aggregated_output=True,
        )
        expected_x = [
            ["FY23", "FY24", "FY24", "FY24", "FY24"],
            [" ", "value_effect", "weight_effect", "mix_effect", "  "],
        ]
        expected_y = [32000.0, 2500.0, 4500.0, 900.0, 39900.0]
        expected_measure = ["absolute", "relative", "relative", "relative", "absolute"]
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)
        self.assertEqual(measure, expected_measure)

    def test_multiple_period_comparison_aggregated(self):
        # Example from here https://accountancyindex.com/price-volume-mix-analysis/
        df = pd.DataFrame(
            {
                "product": ["A", "B", "C", "A", "B", "C", "A", "B", "C"],
                "price": [10, 15, 20, 11, 15, 23, 10, 15, 20],
                "volume": [1000, 800, 500, 1000, 700, 800, 1000, 800, 500],
                "period": [
                    "FY23",
                    "FY23",
                    "FY23",
                    "FY24",
                    "FY24",
                    "FY24",
                    "FY25",
                    "FY25",
                    "FY25",
                ],
            }
        )
        x, y, measure = self.price_volume._price_volume_mix_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
            groupby_col="product",
            aggregated_output=True,
        )
        expected_x = [
            ["FY23", "FY24", "FY24", "FY24", "FY24", "FY25", "FY25", "FY25", "FY25"],
            [
                " ",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "  ",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "   ",
            ],
        ]
        expected_y = [
            32000.0,
            2500.0,
            4500.0,
            900.0,
            39900.0,
            -3400.0,
            -5400.0,
            900.0,
            32000.0,
        ]
        expected_measure = [
            "absolute",
            "relative",
            "relative",
            "relative",
            "absolute",
            "relative",
            "relative",
            "relative",
            "absolute",
        ]
        self.assertEqual(x, expected_x)
        self.assertEqual(y, expected_y)
        self.assertEqual(measure, expected_measure)

    def test_single_period_comparison_with_groupby(self):
        # Example from here https://accountancyindex.com/price-volume-mix-analysis/
        df = pd.DataFrame(
            {
                "product": ["A", "B", "C", "A", "B", "C"],
                "price": [10, 15, 20, 11, 15, 23],
                "volume": [1000, 800, 500, 1000, 700, 800],
                "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
            }
        )
        x, y, measure = self.price_volume._price_volume_mix_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
            aggregated_output=False,
            groupby_col="product",
        )
        expected_x = [
            ["FY23", "A ", "A ", "A ", "B ", "B ", "B ", "C ", "C ", "C ", "FY24"],
            [
                " ",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "  ",
            ],
        ]
        expected_y = [
            32000.0,
            1000.0,
            0.0,
            0.0,
            0.0,
            -1500.0,
            0.0,
            1500.0,
            6000.0,
            900.0,
            39900.0,
        ]
        expected_measure = [
            "absolute",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "absolute",
        ]

        self.assertListEqual(x, expected_x)
        self.assertEqual(y, expected_y)
        self.assertEqual(measure, expected_measure)

    def test_multiple_period_comparison_with_groupby(self):
        # Example from here https://accountancyindex.com/price-volume-mix-analysis/
        df = pd.DataFrame(
            {
                "product": ["A", "B", "C", "A", "B", "C", "A", "B", "C"],
                "price": [10, 15, 20, 11, 15, 23, 10, 15, 20],
                "volume": [1000, 800, 500, 1000, 700, 800, 1000, 800, 500],
                "period": [
                    "FY23",
                    "FY23",
                    "FY23",
                    "FY24",
                    "FY24",
                    "FY24",
                    "FY25",
                    "FY25",
                    "FY25",
                ],
            }
        )
        x, y, measure = self.price_volume._price_volume_mix_analysis(
            df,
            value_col="price",
            weight_col="volume",
            period_col="period",
            groupby_col="product",
            aggregated_output=False,
        )
        expected_x = [
            [
                "FY23",
                "A ",
                "A ",
                "A ",
                "B ",
                "B ",
                "B ",
                "C ",
                "C ",
                "C ",
                "FY24",
                "A  ",
                "A  ",
                "A  ",
                "B  ",
                "B  ",
                "B  ",
                "C  ",
                "C  ",
                "C  ",
                "FY25",
            ],
            [
                " ",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "  ",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "value_effect",
                "weight_effect",
                "mix_effect",
                "   ",
            ],
        ]
        expected_y = [
            32000.0,
            1000.0,
            0.0,
            0.0,
            0.0,
            -1500.0,
            0.0,
            1500.0,
            6000.0,
            900.0,
            39900.0,
            -1000.0,
            0.0,
            0.0,
            0.0,
            1500.0,
            0.0,
            -2400.0,
            -6900.0,
            900.0,
            32000.0,
        ]
        expected_measure = [
            "absolute",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "absolute",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "relative",
            "absolute",
        ]
        self.assertListEqual(x, expected_x)
        self.assertEqual(y, expected_y)
        self.assertEqual(measure, expected_measure)
