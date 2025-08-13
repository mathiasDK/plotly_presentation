import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly_presentation._core.utils.color_helper import adjust_color_brightness
from plotly_presentation._core.colors import Color
from plotly_presentation._core.analysis_helper.utils import apply_setting


class Comparison:
    """
    Provides methods for preparing data and generating comparison charts with totals.

    Methods:
        _get_original_sorting(df, columns): Returns a dict mapping unique values to their original order.
        _prepare_data_for_total(...): Adds a total row/category to the DataFrame for plotting.
        _calculate_total(...): Calculates total values using various formulas.
        vertical_stacked_bar_with_total(...): Creates a vertical stacked bar chart with totals.
        horisontal_stacked_bar_with_total(...): Creates a horizontal stacked bar chart with totals.
    """

    def __init__(self, parent=None):
        self.figure = None
        self.parent = parent

    # def __set_analysis_settings(self):
    #     print(self.parent)
    #     if isinstance(self.parent, "plotly_presentation._core.analysis.Analysis"):
    #         print("Setting figure")
    #         self.parent.figure = self.figure
    #         print("Applying settings")
    #         self.parent._apply_settings()
    #     else:
    #         print("No parent found, not applying settings")
    #         # self.parent.figure = self.figure  # Uncomment if you want to set figure in other contexts
    #         # self.parent._apply_settings()  # Uncomment if you want to apply settings in other contexts

    def _get_original_sorting(self, df: pd.DataFrame, columns: list | str) -> dict:
        """
        Returns a dictionary mapping each unique value in the specified columns to its original order.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            columns (list or str): Column(s) to get unique value order for.

        Returns:
            dict: Mapping of column names to value-order dictionaries.
        """
        d = {}
        if isinstance(columns, str):
            columns = [columns]
        for col in columns:
            d[col] = {val: i for i, val in enumerate(df[col].unique())}
        return d

    def _prepare_data_for_total(
        self,
        df: pd.DataFrame,
        category: str,
        value: str,
        color: str = None,
        total_category: str = None,
        calculate_total: bool = False,
        total_formula: str = None,
        total_as_first: bool = True,
        order_ascending: bool = True,
    ) -> pd.DataFrame:
        """
        Prepares the DataFrame by adding a total row/category for plotting.

        Args:
            df (pd.DataFrame): Input data.
            category (str): Category column.
            value (str): Value column.
            color (str, optional): Color/grouping column.
            total_category (str, optional): Name of the total category.
            calculate_total (bool, optional): Whether to calculate the total row.
            total_formula (str, optional): Formula for calculating the total.
            total_as_first (bool, optional): Place total first or last.
            order_ascending (bool, optional): Sort order.

        Returns:
            pd.DataFrame: Modified DataFrame with total and empty rows.
        """

        if total_category is None and calculate_total is False:
            raise ValueError(
                "Please provide the total category or tell the function how to calculate it"
            )
        if total_category is not None and calculate_total is True:
            raise ValueError(
                "Please provide either the total category or tell the function how to calculate it, not both"
            )

        original_sorting = self._get_original_sorting(
            df, [category, color] if color else category
        )

        if calculate_total is True:
            totals = self._calculate_total(df, total_formula, category, value, color)
            totals["pivot"] = "total"
            df["pivot"] = "other"
            df = pd.concat([df, totals])
        else:
            if total_category not in df[category].unique():
                raise ValueError(
                    f"The category {total_category} is not present in the data"
                )
            df["pivot"] = "other"
            df.loc[df[category] == total_category, "pivot"] = "total"

        # Adding an empty row to ensure spacing between total and other categories
        if color:
            empty_dfs = []
            for c in df[color].unique():
                empty_row = pd.DataFrame({col: [pd.NA] for col in df.columns})
                empty_row["pivot"] = "empty"
                empty_row[category] = ""
                empty_row[value] = 0
                empty_row[color] = c
                empty_dfs.append(empty_row)
            empty_df = pd.concat(empty_dfs, ignore_index=True)
        else:
            empty_df = pd.DataFrame({col: [pd.NA] for col in df.columns})
            empty_df["pivot"] = "empty"
            empty_df[category] = ""
            empty_df[value] = 0
        df = pd.concat([df, empty_df], ignore_index=True)

        # Sort by 'pivot' (total first or last), then by original order of category and color (if present)
        sort_cols = ["pivot"]
        if color:
            sort_cols += [category, color]
        else:
            sort_cols += [category]

        # Map for 'pivot' sorting
        pivot_order = {
            "total": 0 if total_as_first else 1,
            "other": 1 if total_as_first else 0,
            "empty": 0.5,
        }
        df["pivot_sort"] = df["pivot"].map(pivot_order)

        # Use original_sorting for category and color
        df["cat_sort"] = df[category].map(original_sorting[category])
        if color:
            df["color_sort"] = df[color].map(original_sorting[color])
            sort_by = ["pivot_sort", "cat_sort", "color_sort"]
        else:
            sort_by = ["pivot_sort", "cat_sort"]

        df = df.sort_values(
            by=sort_by, ascending=[order_ascending] * len(sort_by)
        ).drop(columns=["pivot_sort", "cat_sort"] + (["color_sort"] if color else []))

        return df

    def _set_color_dict(
        self,
        categories: list[str],
        total_category: str = "Total",
        color_adjustment: int = 2,
        **kwargs,
    ) -> dict:
        """
        Sets the color dictionary for the total category. If the `color_discrete_map` is provided in kwargs, it uses that; otherwise, it adjusts the primary color.

        Args:
            total_category (str): Name of the total category.
            color (str, optional): Color/grouping column. Defaults to Color.PRIMARY.

        Returns:
            dict: Color dictionary for the total category.
        """
        color_discrete_map = kwargs.get("color_discrete_map", None)
        if not color_discrete_map:
            color_discrete_map = {cat: Color.PRIMARY.value for cat in categories}
            color_discrete_map[total_category] = adjust_color_brightness(
                Color.PRIMARY.value, color_adjustment
            )
        return color_discrete_map

    @apply_setting
    def vertical_stacked_bar_with_total(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        total_category: str = None,
        calculate_total: bool = False,
        total_formula: str = None,
        total_as_first: bool = True,
        total_color_adjustment: int = 2,
        **kwargs,
    ) -> go.Figure:
        """
        Creates a vertical stacked bar chart with a total row/category.

        Args:
            df (pd.DataFrame): Input data.
            x (str): X-axis category.
            y (str): Y-axis value.
            color (str, optional): Color/grouping column.
            total_category (str, optional): Name of the total category. Defaults to "Total".
            calculate_total (bool, optional): Whether to calculate the total row.
            total_formula (str, optional): Formula for calculating the total.
            total_as_first (bool, optional): Place total first or last.
            total_color_adjustment (int, optional): Adjustment level for the total category color.

        Returns:
            go.Figure: Plotly bar chart figure.
        """

        df = self._prepare_data_for_total(
            df,
            category=x,
            value=y,
            color=color,
            total_category=total_category,
            calculate_total=calculate_total,
            total_formula=total_formula,
            total_as_first=total_as_first,
            order_ascending=True,
        )

        if color is None:
            color = x
            categories = df[x].unique().tolist()
            color_discrete_map = self._set_color_dict(
                categories=categories,
                total_category="Total" if total_category is None else total_category,
                color_adjustment=total_color_adjustment,
                **kwargs,
            )
            kwargs["color_discrete_map"] = color_discrete_map

        self.figure = px.bar(df, x=x, y=y, color=color, **kwargs)
        # self.figure.for_each_annotation(lambda a: a.update(text="")) # Removing titles
        if self.parent is not None:
            self.parent.figure = self.figure
        return self.figure

    @apply_setting
    def horisontal_stacked_bar_with_total(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str = None,
        total_category: int = None,
        calculate_total: bool = False,
        total_formula: str = None,
        total_as_top: bool = True,
        total_color_adjustment: int = 2,
        **kwargs,
    ) -> go.Figure:
        """
        Creates a horizontal stacked bar chart with a total row/category.

        Args:
            df (pd.DataFrame): Input data.
            x (str): X-axis value.
            y (str): Y-axis category.
            color (str, optional): Color/grouping column.
            total_category (int, optional): Name of the total category.
            calculate_total (bool, optional): Whether to calculate the total row.
            total_formula (str, optional): Formula for calculating the total.
            total_as_top (bool, optional): Place total bottom or top.
            total_color_adjustment (int, optional): Adjustment level for the total category color.

        Returns:
            go.Figure: Plotly bar chart figure.
        """

        df = self._prepare_data_for_total(
            df,
            category=y,
            value=x,
            color=color,
            total_category=total_category,
            calculate_total=calculate_total,
            total_formula=total_formula,
            total_as_first=~total_as_top,  # Inverting total_as_first for horizontal bar chart to make it top if it is True
            order_ascending=False,  # For horizontal bar chart, we want the total to be at the top
        )

        if color is None:
            color = y
            categories = df[y].unique().tolist()
            color_discrete_map = self._set_color_dict(
                categories=categories,
                total_category="Total" if total_category is None else total_category,
                color_adjustment=total_color_adjustment,
                **kwargs,
            )
            kwargs["color_discrete_map"] = color_discrete_map

        self.figure = px.bar(
            df, x=x, y=y, color=color if color is not None else y, **kwargs
        )
        if self.parent is not None:
            self.parent.figure = self.figure
        return self.figure

    def _calculate_total(
        self,
        df: pd.DataFrame,
        total_formula: str,
        x: str,
        y: str,
        color: str,
        weight_column: str = None,
        total_name: str = "Total",
    ) -> pd.DataFrame:
        """
        Calculates total values for the DataFrame using the specified formula.

        Args:
            df (pd.DataFrame): Input data.
            total_formula (str): Formula for calculation ('sum', 'mean', etc.).
            x (str): Category column.
            y (str): Value column.
            color (str): Color/grouping column.
            weight_column (str, optional): Column for weighted mean.
            total_name (str, optional): Name for the total row/category.

        Returns:
            pd.DataFrame: DataFrame with total values.
        """
        VALID_TOTAL_FORMULAS = [
            "sum",
            "mean",
            "count",
            "median",
            "min",
            "max",
            "std",
            "var",
            "weighted_mean",
        ]
        if total_formula.lower() not in VALID_TOTAL_FORMULAS:
            raise AttributeError(
                f"Please provide a valid way to calculate the total - valid formulas are {VALID_TOTAL_FORMULAS}"
            )

        if color is not None:
            if total_formula.lower() != "weighted_mean":
                total_row = df.groupby(color).agg({y: total_formula}).reset_index()
            else:
                if weight_column is None:
                    raise ValueError(
                        "Please provide a weight column for weighted mean calculation"
                    )
                total_row = (
                    df.groupby(color)
                    .apply(
                        lambda g: (g[y] * g[weight_column]).sum()
                        / g[weight_column].sum()
                    )
                    .reset_index()
                )
                total_row = total_row.rename(columns={0: y})
        else:
            if total_formula.lower() != "weighted_mean":
                total_row = df.agg({y: total_formula}).reset_index()
            else:
                if weight_column is None:
                    raise ValueError(
                        "Please provide a weight column for weighted mean calculation"
                    )
                total_row = df.apply(
                    lambda g: (g[y] * g[weight_column]).sum() / g[weight_column].sum()
                ).reset_index()
            total_row = total_row.rename(columns={0: y})
        total_row[x] = total_name

        for col in df.columns:
            if col not in total_row.columns:
                total_row[col] = pd.NA
        total_row = total_row[df.columns]  # reordering
        return total_row

    @apply_setting
    def categorical_comparison(
        self,
        df: pd.DataFrame,
        category: str,
        metric: str,
        val: str,
        text: str = None,
        size: str = None,
        relative_to_min: bool = True,
        category_on_x: bool = True,
        **kwargs,
    ) -> go.Figure:
        """
        Creates a categorical comparison figure using Plotly express scatter plot.

        Args:
            df (pd.DataFrame): Input data.
            category (str): Category column.
            metric (str): Metric name column.
            val (str): Value column.
            text (str, optional): Text label for points. If not provided, there will be no text labels.
            size (str, optional): Column for point size. If not provided, it will be calculated based on the metric relative to the min or max value.
            relative_to_min (bool, optional): If True, size is calculated relative to the minimum value; if False, relative to the maximum value.
            category_on_y (bool, optional): If True, category is on the y-axis; if False, it is on the x-axis.
            **kwargs: Additional keyword arguments for the Plotly express scatter function.

        Returns:
            go.Figure: Plotly categorical comparison figure.
        """

        df = df.copy()
        if size is None:
            transform_function = "min" if relative_to_min else "max"
            df["size"] = (
                df[val] / df.groupby(metric)[val].transform(transform_function) * 20
            )
            size = "size"

        if category_on_x:
            x, y = category, metric
        else:
            x, y = metric, category

        self.figure = px.scatter(
            df,
            x=x,
            y=y,
            size=size,
            # color=val,
            text=text,
            **kwargs,
        )

        # self.__set_analysis_settings()
        return self.figure
