import unittest
import pandas as pd
from plotly_presentation._core.analysis_helper.comparison import Comparison
import plotly.graph_objects as go


class TestComparison(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "Country": [
                    "All",
                    "Germany",
                    "France",
                    "All",
                    "Germany",
                    "France",
                    "All",
                    "Germany",
                    "France",
                ],
                "Response": [
                    "Positive",
                    "Positive",
                    "Positive",
                    "Neutral",
                    "Neutral",
                    "Neutral",
                    "Negative",
                    "Negative",
                    "Negative",
                ],
                "Percentage": [
                    60,
                    80,
                    50,
                    25,
                    15,
                    30,
                    15,
                    5,
                    20,
                ],
                "Respondents": [
                    300,
                    100,
                    200,
                    300,
                    100,
                    200,
                    300,
                    100,
                    200,
                ],
            }
        )
        self.df_no_color = pd.DataFrame(
            {
                "Country": [
                    "All",
                    "Germany",
                    "France",
                ],
                "Percentage": [
                    60,
                    80,
                    50,
                ],
                "Respondents": [
                    300,
                    100,
                    200,
                ],
            }
        )
        self.comp = Comparison()

    def test_get_original_sorting_str(self):
        result = self.comp._get_original_sorting(self.df, "Country")
        self.assertEqual(result["Country"], {"All": 0, "Germany": 1, "France": 2})

    def test_get_original_sorting_list(self):
        result = self.comp._get_original_sorting(self.df, ["Country", "Response"])
        print(result)
        self.assertEqual(result["Country"], {"All": 0, "Germany": 1, "France": 2})
        self.assertEqual(
            result["Response"], {"Positive": 0, "Neutral": 1, "Negative": 2}
        )

    def test_prepare_data_for_total_with_total_category_total_first(self):
        df = self.df_no_color.copy()
        result = self.comp._prepare_data_for_total(
            df,
            category="Country",
            value="Percentage",
            total_category="All",
            total_as_first=True,
            total_formula="sum",
            calculate_total=False,
        ).reset_index(drop=True)
        expected_dataframe = pd.DataFrame(
            {
                "Country": ["All", "", "Germany", "France"],
                "Percentage": [60, 0, 80, 50],
                "Respondents": [300, pd.NA, 100, 200],
                "pivot": ["total", "empty", "other", "other"],
            }
        )
        pd.testing.assert_frame_equal(
            result, expected_dataframe, check_index_type=False
        )

    def test_prepare_data_for_total_with_total_category_total_last(self):
        df = self.df_no_color.copy()
        result = self.comp._prepare_data_for_total(
            df,
            category="Country",
            value="Percentage",
            total_category="All",
            total_as_first=False,
            total_formula="sum",
            calculate_total=False,
        ).reset_index(drop=True)
        print(result)
        expected_dataframe = pd.DataFrame(
            {
                "Country": [
                    "Germany",
                    "France",
                    "",
                    "All",
                ],
                "Percentage": [
                    80,
                    50,
                    0,
                    60,
                ],
                "Respondents": [
                    100,
                    200,
                    pd.NA,
                    300,
                ],
                "pivot": [
                    "other",
                    "other",
                    "empty",
                    "total",
                ],
            }
        )
        pd.testing.assert_frame_equal(
            result, expected_dataframe, check_index_type=False
        )

    def test_prepare_data_for_total_with_total_category_total_first_with_color(self):
        df = self.df.copy()
        result = (
            self.comp._prepare_data_for_total(
                df,
                category="Country",
                value="Percentage",
                color="Response",
                total_category="All",
                total_as_first=True,
                total_formula="sum",
                calculate_total=False,
            )
            .head(6)
            .reset_index(drop=True)
        )
        print(result)
        expected_dataframe = pd.DataFrame(
            {
                "Country": [
                    "All",
                    "All",
                    "All",
                    "",
                    "",
                    "",
                ],
                "Response": [
                    "Positive",
                    "Neutral",
                    "Negative",
                    "Positive",
                    "Neutral",
                    "Negative",
                ],
                "Percentage": [
                    60,
                    25,
                    15,
                    0,
                    0,
                    0,
                ],
                "Respondents": [
                    300,
                    300,
                    300,
                    pd.NA,
                    pd.NA,
                    pd.NA,
                ],
                "pivot": [
                    "total",
                    "total",
                    "total",
                    "empty",
                    "empty",
                    "empty",
                ],
            }
        )
        pd.testing.assert_frame_equal(
            result, expected_dataframe, check_index_type=False
        )

    def test_prepare_data_for_total_with_total_category_total_last_with_color(self):
        df = self.df.copy()
        result = (
            self.comp._prepare_data_for_total(
                df,
                category="Country",
                value="Percentage",
                color="Response",
                total_category="All",
                total_as_first=False,
                total_formula="sum",
                calculate_total=False,
            )
            .tail(6)
            .reset_index(drop=True)
        )
        print(df)
        expected_dataframe = pd.DataFrame(
            {
                "Country": [
                    "",
                    "",
                    "",
                    "All",
                    "All",
                    "All",
                ],
                "Response": [
                    "Positive",
                    "Neutral",
                    "Negative",
                    "Positive",
                    "Neutral",
                    "Negative",
                ],
                "Percentage": [0, 0, 0, 60, 25, 15],
                "Respondents": [
                    pd.NA,
                    pd.NA,
                    pd.NA,
                    300,
                    300,
                    300,
                ],
                "pivot": [
                    "empty",
                    "empty",
                    "empty",
                    "total",
                    "total",
                    "total",
                ],
            }
        )
        pd.testing.assert_frame_equal(
            result, expected_dataframe, check_index_type=False
        )

    def test_prepare_data_for_total_error_both_total_and_calc(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df,
                category="Country",
                value="Percentage",
                total_category="All",
                calculate_total=True,
                total_formula="sum",
            )

    def test_prepare_data_for_total_error_neither_total_nor_calc(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df, category="Country", value="Percentage"
            )

    def test_prepare_data_for_total_error_total_category_missing(self):
        with self.assertRaises(ValueError):
            self.comp._prepare_data_for_total(
                self.df,
                category="Country",
                value="Percentage",
                total_category="NotThere",
            )

    def test_calculate_total_sum(self):
        df = self.df_no_color[self.df_no_color["Country"] != "All"].copy()
        print(df)
        total = self.comp._calculate_total(df, "sum", "Country", "Percentage", None)
        print(total)
        expected_dataframe = pd.DataFrame(
            {
                "Country": ["Total"],
                "Percentage": [130],  # Sum of percentages for Germany and France
                "Respondents": [pd.NA],
            }
        )
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_mean(self):
        df = self.df_no_color[self.df_no_color["Country"] != "All"].copy()
        total = self.comp._calculate_total(df, "mean", "Country", "Percentage", None)
        print(total)
        expected_dataframe = pd.DataFrame(
            {
                "Country": ["Total"],
                "Percentage": [65.0],  # Sum of percentages for Germany and France
                "Respondents": [pd.NA],
            }
        )
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_with_color(self):
        df = self.df[self.df["Country"] != "All"].copy()
        total = (
            self.comp._calculate_total(
                df, "mean", "Country", "Percentage", "Response", total_name="All"
            )
            .sort_values(by=["Country", "Response"])
            .reset_index(drop=True)
        )
        print(total)
        expected_dataframe = (
            pd.DataFrame(
                {
                    "Country": ["All", "All", "All"],
                    "Response": ["Positive", "Neutral", "Negative"],
                    "Percentage": [
                        65.0,
                        22.5,
                        12.5,
                    ],  # Mean of percentages for each response
                    "Respondents": [
                        pd.NA,
                        pd.NA,
                        pd.NA,
                    ],  # Respondents are not calculated in this case
                }
            )
            .sort_values(by=["Country", "Response"])
            .reset_index(drop=True)
        )
        pd.testing.assert_frame_equal(
            total,
            expected_dataframe,
            check_index_type=False,
        )

    def test_calculate_total_with_color_weighted(self):
        df = self.df[self.df["Country"] != "All"].copy()
        total = (
            self.comp._calculate_total(
                df,
                "weighted_mean",
                "Country",
                "Percentage",
                "Response",
                weight_column="Respondents",
            )
            .sort_values(by=["Country", "Response"])
            .reset_index(drop=True)
        )
        print(total)
        expected_dataframe = (
            pd.DataFrame(
                {
                    "Country": ["Total", "Total", "Total"],
                    "Response": ["Positive", "Neutral", "Negative"],
                    "Percentage": [
                        60.0,
                        25.0,
                        15.0,
                    ],  # Weighted percentages for each response
                    "Respondents": [
                        pd.NA,
                        pd.NA,
                        pd.NA,
                    ],  # Total respondents for each response
                }
            )
            .sort_values(by=["Country", "Response"])
            .reset_index(drop=True)
        )
        pd.testing.assert_frame_equal(total, expected_dataframe, check_index_type=False)

    def test_calculate_total_invalid_formula(self):
        df = self.df[self.df["Country"] != "All"].copy()
        with self.assertRaises(AttributeError):
            self.comp._calculate_total(
                df, "invalid_formula", "Country", "Percentage", None
            )

    def test_vertical_stacked_bar_with_total(self):
        df = self.df.copy()
        comp = Comparison()
        comp.vertical_stacked_bar_with_total(
            df, x="Country", y="Percentage", total_category="All"
        )
        self.assertIsNotNone(comp.figure)
        self.assertIsInstance(comp.figure, go.Figure)

    def test_horisontal_stacked_bar_with_total(self):
        df = self.df.copy()
        comp = Comparison()
        comp.horisontal_stacked_bar_with_total(
            df, x="Percentage", y="Country", total_category="All"
        )
        self.assertIsNotNone(comp.figure)
        self.assertIsInstance(comp.figure, go.Figure)

    def test_vertical_stacked_bar_with_total_sorting(self):
        pass

    def test_horisontal_stacked_bar_with_total_sorting(self):
        pass

    def test_categorical_comparison_figure(self):
        df = pd.DataFrame(
            {
                "category": ["Dem", "Rep", "Dem", "Rep"],
                "metric": ["A", "A", "B", "B"],
                "value": [10, 20, 30, 40],
                "text": ["10%", "20%", "30%", "40%"],
            }
        )
        comp = Comparison()
        comp.categorical_comparison(
            df,
            category="category",
            metric="metric",
            val="value",
            text="text",
            size = "value",
        )
        self.assertIsInstance(comp.figure, go.Figure)

    def test_categorical_comparison_size_max(self):
        df = pd.DataFrame(
            {
                "category": ["Dem", "Rep", "Dem", "Rep"],
                "metric": ["A", "A", "B", "B"],
                "value": [10, 20, 30, 40],
                "text": ["10%", "20%", "30%", "40%"],
            }
        )
        comp = Comparison()
        comp.categorical_comparison(
            df,
            category="category",
            metric="metric",
            val="value",
            text="text",
            relative_to_min=False,
        )
        actual_size = comp.figure.data[0].marker.size.tolist()
        print(actual_size)
        expected_size = [5., 10., 7.5, 10.]  
        self.assertListEqual(actual_size, expected_size)

    def test_categorical_comparison_size_min(self):
        df = pd.DataFrame(
            {
                "category": ["Dem", "Rep", "Dem", "Rep"],
                "metric": ["A", "A", "B", "B"],
                "value": [10, 20, 30, 45],
                "text": ["10%", "20%", "30%", "40%"],
            }
        )
        comp = Comparison()
        comp.categorical_comparison(
            df,
            category="category",
            metric="metric",
            val="value",
            text="text",
            # relative_to_min=True,
        )
        actual_size = comp.figure.data[0].marker.size.tolist()
        print(actual_size)
        expected_size = [10., 20., 10., 15.]  
        self.assertListEqual(actual_size, expected_size)



if __name__ == "__main__":
    unittest.main()
