import pandas as pd
import plotly.graph_objects as go
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.analysis_helper.utils import (
    assign_figure_to_self,
    apply_setting,
)


class PriceVolume:
    def __init__(self, parent=None):
        """
        Initialize the PriceVolumeAnalysis class.
        This class provides methods to perform price-volume-mix analysis on a DataFrame.

        Parameters:
        parent: Optional parent Analysis instance. If provided, figures will be assigned to parent.figure.
        """
        # self.figure = None
        self.parent = parent

    def _price_volume_mix_analysis(
        self,
        df: pd.DataFrame,
        value_col: str,
        weight_col: str,
        period_col: str,
        groupby_col: str,
        aggregated_output: bool = True,
    ) -> pd.DataFrame:
        """
        Perform price-volume-mix analysis on a given DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame containing the data.
        value_col (str): Column name representing the value.
        weight_col (str): Column name representing the weight.
        period_col (str): Column name representing the period.
        groupby_col (str): Column name to group by.
        aggregated_output (bool): If True, aggregate the results. Default is True.

        Returns:
        pd.DataFrame: Transformed DataFrame with price, volume, and mix effects.
        """
        df = df.copy()

        # Calculate total value and weight for each period
        df["total_value"] = df[value_col] * df[weight_col]
        df["lag_value"] = df.groupby([groupby_col])[value_col].shift(1)
        df["lag_weight"] = df.groupby([groupby_col])[weight_col].shift(1)
        df["lag_total_value"] = df.groupby([groupby_col])["total_value"].shift(1)

        # Calculate price and volume for each period
        df["value_effect"] = (df[value_col] - df["lag_value"]) * df["lag_weight"]
        df["weight_effect"] = (df[weight_col] - df["lag_weight"]) * df["lag_value"]
        df["mix_effect"] = (
            (df["total_value"] - df["lag_total_value"])
            - df["value_effect"]
            - df["weight_effect"]
        )

        if aggregated_output:
            # Aggregate the results
            df[groupby_col] = "FIXED"
            df = (
                df.groupby([period_col, groupby_col])[
                    ["value_effect", "weight_effect", "mix_effect", "total_value"]
                ]
                .sum()
                .reset_index()
            )
            df.loc[0, ["value_effect", "weight_effect", "mix_effect"]] = pd.NA

        # Reshape the data
        result = df.melt(
            id_vars=[period_col, groupby_col],
            value_vars=["value_effect", "weight_effect", "mix_effect", "total_value"],
        )

        if not aggregated_output:
            totals = (
                result[result["variable"] == "total_value"]
                .groupby([period_col, "variable"])
                .sum(numeric_only=True)
                .reset_index()
            )
            totals[groupby_col] = [" " * (i + 1) for i in range(len(totals))]
            df = result[result["variable"] != "total_value"]
            result = pd.concat([df, totals], ignore_index=True)
        # Create a sort order for the variables
        variable_order = pd.CategoricalDtype(
            [
                "value_effect",
                "weight_effect",
                "mix_effect",
                "total_value",
                *[f"{' '*i}" for i in range(1, 10)],
            ],
            ordered=True,
        )
        result["variable"] = result["variable"].astype(variable_order)
        result[groupby_col] = pd.Categorical(
            result[groupby_col],
            categories=sorted(
                result[groupby_col].unique(), key=lambda x: (x.strip() == "", x)
            ),
        )

        # Sort the result by period, product, and variable
        result = (
            result.sort_values(by=[period_col, groupby_col, "variable"])
            .reset_index(drop=True)
            .dropna()
        )

        # Replace "total_value" with spaces and add more spaces for each occurrence
        i = 0
        for idx, row in result.iterrows():
            if row["variable"] == "total_value":
                i += 1
                result.loc[idx, "variable"] = " " * i

        result["measure"] = "absolute"
        result.loc[result["variable"].str.strip() != "", "measure"] = "relative"

        if aggregated_output:
            x = [result["period"].tolist(), result["variable"].tolist()]
            y = result["value"].tolist()
            measure = result["measure"].tolist()
        else:
            x1, x2 = [], []
            space_counter = 0
            for idx, row in result.iterrows():
                if row["variable"].strip() == "":
                    x1.append(row["period"])
                    x2.append(row["variable"])
                    space_counter += 1
                else:
                    x1.append(row[groupby_col] + " " * space_counter)
                    x2.append(row["variable"])
            x = [x1, x2]
            y = result["value"].tolist()
            measure = result["measure"].tolist()

        return x, y, measure

    def _price_volume_analysis(
        self,
        df: pd.DataFrame,
        value_col: str,
        weight_col: str,
        period_col: str,
    ) -> pd.DataFrame:
        """
        Perform price-volume-mix analysis on a given DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame containing the data.
        value_col (str): Column name representing the value.
        weight_col (str): Column name representing the weight.
        period_col (str): Column name representing the period.

        Returns:
        pd.DataFrame: Transformed DataFrame with price, volume, and mix effects.
        """
        df = df.copy()

        # Calculate total value and weight for each period
        df["total_value"] = df[value_col] * df[weight_col]
        df["lag_value"] = df[value_col].shift(1)
        df["lag_weight"] = df[weight_col].shift(1)
        df["lag_total_value"] = df["total_value"].shift(1)

        # Calculate price and volume for each period
        df["value_effect"] = (df[value_col] - df["lag_value"]) * df[weight_col]
        df["weight_effect"] = (df[weight_col] - df["lag_weight"]) * df["lag_value"]

        # Aggregate the results
        df = (
            df.groupby([period_col])[["value_effect", "weight_effect", "total_value"]]
            .sum()
            .reset_index()
        )
        df.loc[0, ["value_effect", "weight_effect"]] = pd.NA

        # Reshape the data
        result = df.melt(
            id_vars=[period_col],
            value_vars=["value_effect", "weight_effect", "total_value"],
        )

        # Create a sort order for the variables
        variable_order = pd.CategoricalDtype(
            [
                "value_effect",
                "weight_effect",
                "total_value",
                *[f"{' '*i}" for i in range(1, 100)],
            ],
            ordered=True,
        )
        result["variable"] = result["variable"].astype(variable_order)

        # Sort the result by period, product, and variable
        result = (
            result.sort_values(by=[period_col, "variable"])
            .reset_index(drop=True)
            .dropna()
        )

        # Replace "total_value" with spaces and add more spaces for each occurrence
        i = 0
        for idx, row in result.iterrows():
            if row["variable"] == "total_value":
                i += 1
                result.loc[idx, "variable"] = " " * i

        result["measure"] = "absolute"
        result.loc[result["variable"].str.strip() != "", "measure"] = "relative"

        x = [result["period"].tolist(), result["variable"].tolist()]
        y = result["value"].tolist()
        measure = result["measure"].tolist()

        return x, y, measure

    @assign_figure_to_self
    @apply_setting
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
        x, y, measure = self._price_volume_mix_analysis(
            df, value_col, weight_col, period_col, groupby_col, aggregated_output
        )
        x = self.__replace_list_names(x, category_name)
        if show_text:
            if text is None:
                text = self.__get_text(y, text_format)
        self.figure = Plotter().add_trace(
            go.Waterfall(x=x, y=y, measure=measure, text=text, **kwargs)
        )
        if self.parent is not None:
            self.parent.figure = self.figure
        return self.figure

    @assign_figure_to_self
    @apply_setting
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
        x, y, measure = self._price_volume_analysis(
            df, value_col, weight_col, period_col
        )
        x = self.__replace_list_names(x, category_name)
        if show_text:
            if text is None:
                text = self.__get_text(y, text_format)
        self.figure = Plotter().add_trace(
            go.Waterfall(x=x, y=y, measure=measure, text=text, **kwargs)
        )
        if self.parent is not None:
            self.parent.figure = self.figure
        return self.figure

    def __get_text(self, y, text_format):
        return [f"{value:{text_format}}" for value in y]

    def __replace_list_names(self, x, category_name):
        return [x[0], [category_name.get(value, value) for value in x[1]]]
