import pandas as pd
import plotly.graph_objects as go
from plotly_presentation._core.colors import CalloutColor, Color

def create_comparison_figure(df: pd.DataFrame, category_column: str, primary_column: str, secondary_column: str, comparison_metrics: list[str] = None) -> go.Figure:
    
    _ACCEPTED_COMPARISON_METRICS = ["lift", "ratio", "difference", "percentage"]
    if comparison_metrics is not None:
        for metric in comparison_metrics:
            if metric not in _ACCEPTED_COMPARISON_METRICS:
                raise ValueError(f"Invalid lift metric '{metric}'. Please choose from {_ACCEPTED_COMPARISON_METRICS}")
            
    df = df.copy()
    df = df.sort_values(by=[primary_column, secondary_column], ascending=[True, True])
    max_x = df[[primary_column, secondary_column]].max().max()
            
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_shape(
            type="line",
            x0=row[primary_column],
            x1=row[secondary_column],
            y0=row[category_column],
            y1=row[category_column],
            line=dict(color=CalloutColor.LINE_COLOR.value, width=1),
            name=f"line_{i}",
        )
    fig.add_trace(
        go.Scatter(
            x=df[primary_column],
            y=df[category_column],
            mode='markers',
            marker=dict(size=15, color=Color.PRIMARY.value),
            name=primary_column,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[secondary_column],
            y=df[category_column],
            mode='markers',
            marker=dict(size=15, color=Color.SECONDARY.value),
            name=secondary_column,
        )
    )

    if comparison_metrics is not None:
        x_offsets = [0.1*i for i in range(len(comparison_metrics))]
        for metric, x_offset in zip(comparison_metrics, x_offsets):
            vals, normalised_vals, text = _calculate_comparison(df[primary_column], df[secondary_column], metric)
            fig.add_trace(
                go.Scatter(
                    x=[max_x+x_offset for _ in range(len(df))],
                    y=df[category_column],
                    text=text,
                    mode="text+markers",
                    name=metric,
                    showlegend=False,
                    marker=dict(
                        size=10+normalised_vals*3,
                        color=[Color.POSITIVE.value if v>0 else Color.NEGATIVE.value for v in vals],
                        opacity=0.5
                    ),
                ),
            )
            fig.add_annotation(
                x=max_x+x_offset,
                y=len(df)-0.5,
                text=metric,
                showarrow=False,
                # yshift=10
            )
    return df

def _calculate_comparison(s1: pd.Series, s2: pd.Series, metric: str, change_direction: list|pd.Series = None) -> list:
    if metric.lower() == "lift":
        vals, text = _calculate_lift(s1, s2, change_direction)
    elif metric.lower() == "ratio":
        vals, text = _calculate_ratio(s1, s2, change_direction)
    elif metric.lower() == "difference":
        vals, text = _calculate_difference
    elif metric.lower() == "percentage":
        vals, text = _calculate_percentage(s1, s2, change_direction)

    normalised_vals = (vals - vals.min()) / (vals.max() - vals.min())
    return vals, normalised_vals, text
    
def _calculate_lift(s1: pd.Series, s2: pd.Series, change_direction: list|pd.Series = None) -> list:
    if change_direction is not None:
        vals = (s1 / s2 - 1) * change_direction
    else:
        vals = (s1 / s2 - 1)
    text = vals
    return vals, text

def _calculate_ratio(s1: pd.Series, s2: pd.Series, change_direction: list|pd.Series = None) -> list:
    if change_direction is not None:
        vals = s1 / s2 * change_direction
    else:
        vals = s1 / s2
    text = [f"{val:1f}x" for val in vals]
    return vals, text

def _calculate_difference(s1: pd.Series, s2: pd.Series, change_direction: list|pd.Series = None) -> list:
    if change_direction is not None:
        vals = (s1 - s2) * change_direction
    else:
        vals = s1 - s2
    text = [f"{val:,.1f}" for val in vals]
    return vals, text

def _calculate_percentage(s1: pd.Series, s2: pd.Series, change_direction: list|pd.Series = None) -> list:
    if change_direction is not None:
        vals = (s1 - s2) / s2 * change_direction
    else:
        vals = (s1 - s2) / s2
    text = [f"{val:.1%}" for val in vals]
    return vals, text
    
    