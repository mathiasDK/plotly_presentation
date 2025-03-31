import pandas as pd


def price_volume_analysis(
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
        result.sort_values(by=[period_col, "variable"]).reset_index(drop=True).dropna()
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
