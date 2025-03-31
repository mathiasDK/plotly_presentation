from plotly_presentation._core.analysis_helper.change.price_volume_mix import (
    price_volume_mix_analysis,
)
from plotly_presentation._core.analysis_helper.change.price_volume import (
    price_volume_analysis,
)
from plotly_presentation._core.plotter import Plotter
import plotly.graph_objects as go
import pandas as pd


class Analysis(Plotter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def price_volume_mix_analysis(
        self,
        df: pd.DataFrame,
        value_col: str,
        weight_col: str,
        period_col: str,
        groupby_col: str,
        aggregated_output=True,
        show_text: bool = True,
        text: list[str] = None,
        text_format: str = ".1f",
        category_name: dict = {
            "value_effect": "Value Effect",
            "weight_effect": "Weight Effect",
            "mix_effect": "Mix Effect",
            "total_value": "Total Value",
        },
        **kwargs,
    ) -> go.Figure:
        """
        Perform price-volume-mix analysis on a given DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame containing the data.
            The dataframe should have the following structure:
            | groupby_col | period_col | value_col | weight_col |
            |-------------|------------|-----------|------------|
            | A           | 1          | 10        | 100        |
            | B           | 1          | 15        | 200        |
            | A           | 2          | 12        | 150        |
            | B           | 2          | 18        | 250        |
            | ...         | ...        | ...       | ...
        value_col (str): Column name representing the value.
        weight_col (str): Column name representing the weight.
        period_col (str): Column name representing the period.
        groupby_col (str): Column name to group by.
        aggregated_output (bool): If True, aggregate the results. Default is True.

        Returns:
        go.Figure: Plotly figure with the price-volume-mix analysis.
        """
        x, y, measure = price_volume_mix_analysis(
            df, value_col, weight_col, period_col, groupby_col, aggregated_output
        )
        x = self.__replace_list_names(x, category_name)
        if show_text:
            if text is None:
                text = self.__get_text(y, text_format)
        self.figure = self.add_trace(
            go.Waterfall(x=x, y=y, measure=measure, text=text, **kwargs)
        )
        return self.figure

    def price_volume_analysis(
        self,
        df: pd.DataFrame,
        value_col: str,
        weight_col: str,
        period_col: str,
        show_text: bool = True,
        text: list[str] = None,
        text_format: str = ".1f",
        category_name: dict = {
            "value_effect": "Value Effect",
            "weight_effect": "Weight Effect",
            "mix_effect": "Mix Effect",
            "total_value": "Total Value",
        },
        **kwargs,
    ) -> go.Figure:
        """
        Perform price-volume-mix analysis on a given DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame containing the data.
            The dataframe should have the following structure:
            | period_col | value_col | weight_col |
            |------------|-----------|------------|
            | 1          | 10        | 100        |
            | 1          | 15        | 200        |
            | 2          | 12        | 150        |
            | 2          | 18        | 250        |
            | ...        | ...       | ...
        value_col (str): Column name representing the value.
        weight_col (str): Column name representing the weight.
        period_col (str): Column name representing the period.

        Returns:
        go.Figure: Plotly figure with the price-volume-mix analysis.
        """
        x, y, measure = price_volume_analysis(df, value_col, weight_col, period_col)
        x = self.__replace_list_names(x, category_name)
        if show_text:
            if text is None:
                text = self.__get_text(y, text_format)
        self.figure = self.add_trace(
            go.Waterfall(x=x, y=y, measure=measure, text=text, **kwargs)
        )
        return self.figure

    def __get_text(self, y, text_format):
        return [f"{value:{text_format}}" for value in y]

    def __replace_list_names(self, x, category_name):
        return [x[0], [category_name.get(value, value) for value in x[1]]]
