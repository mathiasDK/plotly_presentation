import unittest
import pandas as pd
from plotly_presentation._core.analysis_helper.comparison import Comparison
import plotly.graph_objects as go

class TestComparison(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Country': [
                'All', 'Germany', 'France',
                'All', 'Germany', 'France',
                'All', 'Germany', 'France',
            ],
            'Response': [
                'Positive', 'Positive', 'Positive',
                'Neutral', 'Neutral', 'Neutral',
                'Negative', 'Negative', 'Negative',
            ],
            'Percentage': [
                60, 80, 50,
                25, 15, 30,
                15,  5, 20,
            ],
            'Respondents': [
                180, 80, 100,
                75,  15,  60,
                45,   5,  40,
            ]
        })
        self.df_no_color = pd.DataFrame({
            'Country': [
                'All', 'Germany', 'France',
            ],
            'Percentage': [
                60, 80, 50,
            ],
            'Respondents': [
                180, 80, 100,
            ]
        })
        self.comp = Comparison()

    def test_get_original_sorting_str(self):
        result = self.comp._get_original_sorting(self.df, "Country")
        self.assertEqual(result["Country"], {"All": 0, "Germany": 1, "France": 2})

    def test_get_original_sorting_list(self):
        result = self.comp._get_original_sorting(self.df, ["Country", "Response"])
        print(result)
        self.assertEqual(result["Country"], {"All": 0, "Germany": 1, "France": 2})
        self.assertEqual(result["Response"], {"Positive": 0, "Neutral": 1, "Negative": 2})

    def test_prepare_data_for_total_with_total_category_total_first(self):
        df = self.df_no_color.copy()
        result = self.comp._prepare_data_for_total(
            df, category="Country", value="Percentage", total_category="All", total_as_first=True, total_formula="sum", calculate_total=False
        ).reset_index(drop=True)
        expected_dataframe = pd.DataFrame({
            'Country': ['All', 'Germany', 'France'],
            'Percentage': [60, 80, 50],
            'Respondents': [180, 80, 100],
            'pivot': ['total', 'other', 'other']
        })
        pd.testing.assert_frame_equal(result, expected_dataframe, check_index_type=False)

    def test_prepare_data_for_total_with_total_category_total_last(self):
        df = self.df_no_color.copy()
        result = self.comp._prepare_data_for_total(
            df, category="Country", value="Percentage", total_category="All", total_as_first=False, total_formula="sum", calculate_total=False
        ).reset_index(drop=True)
        expected_dataframe = pd.DataFrame({
            'Country': ['Germany', 'France', 'All', ],
            'Percentage': [80, 50, 60, ],
            'Respondents': [80, 100, 180, ],
            'pivot': ['other', 'other', 'total', ]
        })
        pd.testing.assert_frame_equal(result, expected_dataframe, check_index_type=False)

    def test_prepare_data_for_total_with_total_category_total_first_with_color(self):
        df = self.df.copy()
        result = self.comp._prepare_data_for_total(
            df, category="Country", value="Percentage", color = "Response", total_category="All", total_as_first=True, total_formula="sum", calculate_total=False
        ).reset_index(drop=True)
        print(result)
        expected_dataframe = pd.DataFrame({
            'Country': [
                'All', 'All', 'All',
                'Germany', 'Germany', 'Germany',
                'France', 'France', 'France',
            ],
            'Response': [
                'Positive', 'Neutral', 'Negative', 
                'Positive', 'Neutral', 'Negative', 
                'Positive', 'Neutral', 'Negative', 
            ],
            'Percentage': [
                60, 25, 15,
                80, 15, 5,
                50, 30, 20,
            ],
            'Respondents': [
                180, 75, 45,
                80, 15, 5,
                100, 60, 40,
            ],
            'pivot': [
                'total', 'total', 'total', 
                'other', 'other', 'other', 
                'other', 'other', 'other', 
            ]
        })
        pd.testing.assert_frame_equal(result, expected_dataframe, check_index_type=False)

    def test_prepare_data_for_total_with_total_category_total_last_with_color(self):
        df = self.df.copy()
        result = self.comp._prepare_data_for_total(
            df, category="Country", value="Percentage", color = "Response", total_category="All", total_as_first=False, total_formula="sum", calculate_total=False
        ).reset_index(drop=True)
        expected_dataframe = pd.DataFrame({
            'Country': [
                'Germany', 'Germany', 'Germany',
                'France', 'France', 'France',
                'All', 'All', 'All',
            ],
            'Response': [
                'Positive', 'Neutral', 'Negative', 
                'Positive', 'Neutral', 'Negative', 
                'Positive', 'Neutral', 'Negative', 
            ],
            'Percentage': [
                80, 15, 5,
                50, 30, 20,
                60, 25, 15
            ],
            'Respondents': [
                80, 15, 5,
                100, 60, 40,
                180, 75, 45,
            ],
            'pivot': [
                'other', 'other', 'other', 
                'other', 'other', 'other', 
                'total', 'total', 'total', 
            ]
        })
        pd.testing.assert_frame_equal(result, expected_dataframe, check_index_type=False)

    def test_prepare_data_for_total_error_both_total_and_calc(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df, category="Country", value="Percentage",
                total_category="All", calculate_total=True, total_formula="sum"
            )

    def test_prepare_data_for_total_error_neither_total_nor_calc(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df, category="Country", value="Percentage"
            )

    def test_prepare_data_for_total_error_total_category_missing(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df, category="Country", value="Percentage", total_category="NotThere"
            )

    def test_calculate_total_sum(self):
        df = self.df_no_color[self.df_no_color['Country'] != 'All'].copy()
        print(df)
        total = self.comp._calculate_total(df, "sum", "Country", "Percentage", None)
        print(total)
        expected_dataframe = pd.DataFrame({
            'Country': ['Total'],
            'Percentage': [130],  # Sum of percentages for Germany and France
            'Respondents': [pd.NA],
        })
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_mean(self):
        df = self.df_no_color[self.df_no_color['Country'] != 'All'].copy()
        total = self.comp._calculate_total(df, "mean", "Country", "Percentage", None)
        print(total)
        expected_dataframe = pd.DataFrame({
            'Country': ['Total'],
            'Percentage': [65.],  # Sum of percentages for Germany and France
            'Respondents': [pd.NA],
        })
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_with_color(self):
        df = self.df[self.df['Country'] != 'All'].copy()
        total = self.comp._calculate_total(df, "mean", "Country", "Percentage", "Response", total_name="All").sort_values(by=["Country", "Response"]).reset_index(drop=True)
        print(total)
        expected_dataframe = pd.DataFrame({
            'Country': ['All', 'All', 'All'],
            'Response': ['Positive', 'Neutral', 'Negative'],
            'Percentage': [65., 22.5, 12.5],  # Mean of percentages for each response
            'Respondents': [pd.NA, pd.NA, pd.NA]  # Respondents are not calculated in this case
        }).sort_values(by=["Country", "Response"]).reset_index(drop=True)
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False, )

    # def test_calculate_total_with_color_weighted(self):
    #     df = self.df[self.df['Country'] != 'All'].copy()
    #     total = self.comp._calculate_total(df, "weighted_mean", "Country", "Percentage", "Response", weight_column="Respondents")
    #     self.assertIn("Country", total.columns)
    #     self.assertIn("Response", total.columns)
    #     self.assertIn("Percentage", total.columns)
    #     expected_dataframe = pd.DataFrame({
    #         'Country': ['Total', 'Total', 'Total'],
    #         'Response': ['Positive', 'Neutral', 'Negative'],
    #         'Percentage': [60, 25, 20]  # Weighted percentages for each response
    #     })
    #     pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_invalid_formula(self):
        df = self.df[self.df['Country'] != 'All'].copy()
        with self.assertRaises(AttributeError):
            self.comp._calculate_total(df, "invalid_formula", "Country", "Percentage", None)

    def test_vertical_stacked_bar_with_total(self):
        df = self.df.copy()
        comp = Comparison()
        comp.vertical_stacked_bar_with_total(
            df, x="Country", y="Percentage", total_placement="All"
        )
        self.assertIsNotNone(comp.figure)
        self.assertIsInstance(comp.figure, go.Figure)

    def test_horisontal_stacked_bar_with_total(self):
        df = self.df.copy()
        comp = Comparison()
        comp.horisontal_stacked_bar_with_total(
            df, x="Percentage", y="Country", total_placement="All"
        )
        self.assertIsNotNone(comp.figure)
        self.assertIsInstance(comp.figure, go.Figure)

if __name__ == "__main__":
    unittest.main()