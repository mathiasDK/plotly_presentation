import pandas as pd


def price_volume_mix_analysis(
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
