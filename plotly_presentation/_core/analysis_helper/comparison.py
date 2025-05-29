import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class Comparison:
    def __init__(self):
        self.figure = None

    def _get_original_sorting(self, df:pd.DataFrame, columns:list|str) -> dict:
        d = {}
        if isinstance(columns, str):
            columns = [columns]
        for col in columns:
            d[col] = {val: i for i, val in enumerate(df[col].unique())}
        return d
    
    def _prepare_data_for_total(
            self, 
            df:pd.DataFrame, 
            category:str, 
            value:str, 
            color:str=None, 
            total_category:str=None, 
            calculate_total:bool=False, 
            total_formula:str=None, 
            total_as_first:bool=True,
            order_ascending:bool=True
        ) -> pd.DataFrame:

        if total_category is None and calculate_total is False:
            raise ValueError("Please provide the total category or tell the function how to calculate it")
        if total_category is not None and calculate_total is True:
            raise ValueError("Please provide either the total category or tell the function how to calculate it, not both")
        
        original_sorting = self._get_original_sorting(df, [category, color] if color else category)

        if calculate_total is True:
            totals = self._calculate_total(df, total_formula, category, value, color)
            totals["pivot"] = "total"
            df["pivot"] = "other"
            df = pd.concat([df, totals])
        else:
            if total_category not in df[category].unique():
                raise ValueError(f"The category {total_category} is not present in the data")
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
        pivot_order = {"total": 0 if total_as_first else 1, "other": 1 if total_as_first else 0, "empty": 0.5}
        df = df.copy()
        df["pivot_sort"] = df["pivot"].map(pivot_order)

        # Use original_sorting for category and color
        df["cat_sort"] = df[category].map(original_sorting[category])
        if color:
            df["color_sort"] = df[color].map(original_sorting[color])
            sort_by = ["pivot_sort", "cat_sort", "color_sort"]
        else:
            sort_by = ["pivot_sort", "cat_sort"]


        df = df.sort_values(by=sort_by, ascending=[order_ascending]*len(sort_by)).drop(columns=["pivot_sort", "cat_sort"] + (["color_sort"] if color else []))

        return df

    def vertical_stacked_bar_with_total(self, df:pd.DataFrame, x:str, y:str, color:str=None, total_placement:int=None, calculate_total:bool=False, total_formula:str=None, total_as_first:bool=True, **kwargs) -> go.Figure:

        df = self._prepare_data_for_total(
            df, 
            category=x, 
            value=y, 
            color=color, 
            total_category=total_placement, 
            calculate_total=calculate_total, 
            total_formula=total_formula, 
            total_as_first=total_as_first,
            order_ascending=True
        )

        self.figure = px.bar(
            df,
            x = x,
            y = y,
            color = color,
            **kwargs
        )
        # self.figure.for_each_annotation(lambda a: a.update(text="")) # Removing titles
        return self.figure

    def horisontal_stacked_bar_with_total(self, df:pd.DataFrame, x:str, y:str, color:str=None, total_placement:int=None, calculate_total:bool=False, total_formula:str=None, total_as_first:bool=True, **kwargs) -> go.Figure:

        df = self._prepare_data_for_total(
            df, 
            category=y, 
            value=x, 
            color=color, 
            total_category=total_placement, 
            calculate_total=calculate_total, 
            total_formula=total_formula, 
            total_as_first=total_as_first, # Inverting total_as_first for horizontal bar chart to make it top if it is True
            order_ascending=False  # For horizontal bar chart, we want the total to be at the top
        )

        self.figure = px.bar(
            df,
            x = x,
            y = y,
            color = color,
            **kwargs
        )
        # self.figure.for_each_trace(lambda t: t.update(text="")) # Removing titles

        return self.figure

    def _calculate_total(self, df: pd.DataFrame, total_formula:str, x:str, y:str, color:str, weight_column:str=None, total_name:str="Total") -> pd.DataFrame:
        VALID_TOTAL_FORMULAS = ["sum", "mean"]
        if total_formula.lower() not in VALID_TOTAL_FORMULAS:
            raise AttributeError(f"Please provide a valid way to calculate the total - valid formulas are {VALID_TOTAL_FORMULAS}")
        
        if color is not None:
            total_row = df.groupby(color).agg({y: total_formula}).reset_index()
        else:
            total_row = df.agg({y: total_formula}).reset_index().rename(columns={0: y})
        total_row[x] = total_name

        for col in df.columns:
            if col not in total_row.columns:
                total_row[col] = pd.NA
        total_row = total_row[df.columns] # reordering
        return total_row