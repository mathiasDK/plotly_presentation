"""Examples"""

from functools import wraps as _wraps
from inspect import getsource as _getsource

import numpy as np
import pandas as pd
import plotly.express.data as data
import plotly.graph_objs as go

from plotly_presentation import Plotter
from plotly_presentation._core.analysis import Analysis
import plotly.io as pio

pio.renderers.default = "png"


def _clean_source(source):
    source = source.split('"""')[2].replace("\t", "")
    # Replace the output variable wth its value
    # source = source.replace("_OUTPUT_FORMAT", "'{}'".format(_OUTPUT_FORMAT))
    return source


def _print_source(f):
    """Print code after the function docstring up until the first
    set of triple quotes"""

    @_wraps(f)
    def wrapper(*args, **kwargs):
        source = _getsource(f)
        print(_clean_source(source))
        return f(*args, **kwargs)

    return wrapper


@_print_source
def plot_line():
    """
    Line example
    """
    from plotly_presentation import Plotter
    import plotly.graph_objs as go

    # Generate example data
    df = data.stocks()
    print(df.head())
    """Print break"""
    _line_example_1(df)
    _line_example_2(df)


@_print_source
def _line_example_1(df):
    """Express line"""
    # Plot the data
    p = Plotter()
    p.express(type="line", data_frame=df, x="date", y=["GOOG", "AAPL", "FB"])
    p.show()


@_print_source
def _line_example_2(df):
    """Trace line"""
    # Plot the data
    p = Plotter()
    p.add_trace(go.Scatter(x=df["date"], y=df["GOOG"], name="GOOG", mode="lines"))
    p.add_trace(go.Scatter(x=df["date"], y=df["AAPL"], name="AAPL", mode="lines"))
    p.show()


@_print_source
def plot_bar():
    """
    Bar example
    """
    from plotly_presentation import Plotter
    import plotly.graph_objs as go
    import pandas as pd

    # Generate example data
    df = pd.DataFrame(
        {
            "x": ["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
            "y": [1, 3, 2, 3, 3, 2, 4, 4],
            "color": ["a", "b", "a", "b", "a", "b", "a", "b"],
        }
    )
    print(df.head())
    """Print break"""
    _bar_example_1(df)
    _bar_example_2(df)


@_print_source
def _bar_example_1(df):
    """# Express bar"""
    # Plot the data
    p = Plotter(slide_layout="slide_50%")
    p.express(type="bar", data_frame=df, x="x", y="y", color="color", barmode="group")
    p.show()


@_print_source
def _bar_example_2(df):
    """# Trace bar"""
    # Plot the data
    p = Plotter(slide_layout="slide_50%")
    p.add_trace(
        go.Bar(
            x=df[df["color"] == "a"]["x"],
            y=df[df["color"] == "a"]["y"],
            name="a",
        )
    )
    p.add_trace(
        go.Bar(
            x=df[df["color"] == "b"]["x"],
            y=df[df["color"] == "b"]["y"],
            name="b",
        )
    )
    p.show()


@_print_source
def plot_bar_callout():
    """
    Bar callouts example
    """
    from plotly_presentation import Plotter

    """Print break"""
    _bar_callout_example_1()
    _bar_callout_example_2()
    _bar_callout_example_3()
    _bar_callout_example_4()
    _bar_callout_example_5()


@_print_source
def _bar_callout_example_1():
    """
    Bar callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
        y=[1, 3, 0, 3, 3, 2, 4, 4],
        color=["a", "b", "a", "b", "a", "b", "a", "b"],
        barmode="group",
    )
    p.callout.add_line_differences(
        primary_trace_name="b",
        text_type="ratio",
        text_format=".1f",
        y_text_offset=0.1,
    )
    p.show()


@_print_source
def _bar_callout_example_2():
    """
    Bar callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
        y=[1, 3, 0, 3, 3, 2, 4, 4],
        color=["a", "b", "a", "b", "a", "b", "a", "b"],
        barmode="group",
    )
    p.callout.add_line_differences(
        primary_trace_name="b",
        text_type="difference",
        text_format=".0f",
        y_text_offset=0.1,
    )
    p.show()


@_print_source
def _bar_callout_example_3():
    """
    Bar callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
        y=[1, 3, 0, 3, 3, 2, 4, 4],
        color=["a", "b", "a", "b", "a", "b", "a", "b"],
        barmode="group",
    )
    p.callout.add_line_differences(
        primary_trace_name="a",
        text_type="difference",
        text_format=".0f",
        y_text_offset=0.1,
    )
    p.show()


@_print_source
def _bar_callout_example_4():
    """
    Bar callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["a", "b", "c"],
        y=[2.2, 2.4, 2.6],
    )
    p.callout.add_square_growth_line(
        x0="a", x1="c", y0=2.3, y1=2.7, y_top=2.9, text="+18%"
    )
    p.show()


@_print_source
def _bar_callout_example_5():
    """
    Bar callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["a", "b", "c"],
        y=[1.5, 2.4, 2.8],
    )
    p.callout.add_dash_growth_lines(
        x0="a", x1="c", y0=1.5, y1=2.8, x_end=2.7, text="+87%"
    )
    p.show()


@_print_source
def plot_line_callout():
    """
    Line callouts example
    """
    from plotly_presentation import Plotter

    """Print break"""
    _line_callout_example_1()
    _line_callout_example_2()
    _line_callout_example_3()
    _line_callout_example_4()


@_print_source
def _line_callout_example_1():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["cat1", "cat1", "cat2", "cat2", "cat3", "cat3", "cat4", "cat4"],
        y=[1, 3, 2, 3, 3, 2, 3.1, 3],
        color=["a", "b", "a", "b", "a", "b", "a", "b"],
    )
    p.callout.add_line_end_marker(
        text_type="category", text_positions=["middle right", "bottom right"]
    )
    p.show()


@_print_source
def _line_callout_example_2():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["cat1", "cat2", "cat3", "cat4"],
        y=[1, 2, 3, 3.1],
        color=["a", "a", "a", "a"],
    )
    p.callout.add_square_growth_line(
        x0="cat2", x1="cat4", y0=2.1, y1=3.2, y_top=3.5, text="+55%"
    )
    p.figure.update_layout(showlegend=False)
    p.show()


@_print_source
def _line_callout_example_3():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["cat1", "cat2", "cat3", "cat4"],
        y=[1, 2, 3, 3.1],
        color=["a", "a", "a", "a"],
    )
    p.callout.add_dash_growth_lines(
        x0="cat2", x1="cat4", y0=2, y1=3.1, x_end="cat4", text="+55%"
    )
    p.figure.update_layout(showlegend=False)
    p.show()


@_print_source
def _line_callout_example_4():
    """
    Line callouts example
    """
    df = data.stocks()
    p = Plotter(slide_layout="slide_50%")
    p.express(type="line", data_frame=df, x="date", y="GOOG")
    p.callout.add_square_growth_line(
        x0="2019-01-28", x1="2019-12-30", y0=1, y1=1.2, y_top=1.5, text="+20%"
    )
    p.figure.update_layout(showlegend=False)
    p.show()


@_print_source
def plot_general_callout():
    """
    Line callouts example
    """
    from plotly_presentation import Plotter

    """Print break"""
    _general_callout_example_1()


@_print_source
def _general_callout_example_1():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="bar",
        x=["a", "b", "c"],
        y=[2.2, 2.4, 2.6],
    )
    p.callout.add_circle_highlight(x="c", y=3, text="1")
    p.callout.add_circle_highlight(x="a", y=3, text="2")
    p.show()


@_print_source
def plot_style():
    """
    Line callouts example
    """
    from plotly_presentation import Plotter

    """Print break"""
    _style_set_colors()
    _style_set_diverging_colors()
    _style_set_sequential_colors()


@_print_source
def _style_set_sequential_colors():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
        y=[2, 2, 2, 3, 3, 3, 4, 4, 4],
        color=[
            "a",
            "a",
            "a",
            "b",
            "b",
            "b",
            "c",
            "c",
            "c",
        ],
    )
    p.style.set_color_palette(palette_type="sequential", palette_name="reds")
    p.show()


@_print_source
def _style_set_diverging_colors():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
        y=[2, 2, 2, 3, 3, 3, 4, 4, 4],
        color=[
            "a",
            "a",
            "a",
            "b",
            "b",
            "b",
            "c",
            "c",
            "c",
        ],
    )
    p.style.set_color_palette(palette_type="diverging", palette_name="reds")
    p.show()


@_print_source
def _style_set_colors():
    """
    Line callouts example
    """

    p = Plotter(slide_layout="slide_50%")
    p.express(
        type="line",
        x=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
        y=[2, 2, 2, 3, 3, 3, 4, 4, 4],
        color=[
            "a",
            "a",
            "a",
            "b",
            "b",
            "b",
            "c",
            "c",
            "c",
        ],
    )
    color_map = {"a": "#0011ff", "b": "#88ff00", "c": "#44aaaa"}
    p.style.set_color_palette(color_dict=color_map)
    p.show()


@_print_source
def plot_special_graphs():
    """
    Special graphs examples
    """
    from plotly_presentation import Plotter

    """Print break"""
    _waterfall_example_1()


@_print_source
def _waterfall_example_1():
    """
    Waterfall example
    """

    p = Plotter(slide_layout="slide_100%")
    p.add_trace(
        go.Waterfall(
            name="20",
            orientation="v",
            measure=["relative", "relative", "total", "relative", "relative", "total"],
            x=[
                "Sales",
                "Consulting",
                "Net revenue",
                "Purchases",
                "Other expenses",
                "Profit before tax",
            ],
            textposition="outside",
            text=["+60", "+80", "", "-40", "-20", "Total"],
            y=[60, 80, 0, -40, -20, 0],
        )
    )
    p.show()


@_print_source
def plot_analysis_graphs():
    """
    Analysis graphs examples
    """
    from plotly_presentation._core.analysis import Analysis

    """Print break"""
    _price_volume_mix_example_aggregated()
    _price_volume_mix_example_by_product()
    _price_volume_mix_example_aggregated_adjusted_y()


@_print_source
def _price_volume_mix_example_aggregated():
    """
    Price volume mix example
    """
    df = pd.DataFrame(
        {
            "product": ["A", "B", "C", "A", "B", "C"],
            "price": [10, 15, 20, 11, 15, 23],
            "volume": [1000, 800, 500, 1000, 700, 800],
            "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
        }
    )

    p = Analysis(slide_layout="slide_wide")
    p.price_volume_mix_analysis(
        df,
        value_col="price",
        weight_col="volume",
        period_col="period",
        groupby_col="product",
        aggregated_output=True,
        show_text=True,
        text_format=".0f",
    )
    p.show()


@_print_source
def _price_volume_mix_example_by_product():
    """
    Price volume mix example
    """
    df = pd.DataFrame(
        {
            "product": ["A", "B", "C", "A", "B", "C"],
            "price": [10, 15, 20, 11, 15, 23],
            "volume": [1000, 800, 500, 1000, 700, 800],
            "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
        }
    )

    p = Analysis(slide_layout="slide_wide")
    p.price_volume_mix_analysis(
        df,
        value_col="price",
        weight_col="volume",
        period_col="period",
        groupby_col="product",
        aggregated_output=False,
        show_text=True,
        text_format=".0f",
    )
    p.show()


@_print_source
def _price_volume_mix_example_aggregated_adjusted_y():
    """
    Price volume mix example
    """
    df = pd.DataFrame(
        {
            "product": ["A", "B", "C", "A", "B", "C"],
            "price": [10, 15, 20, 11, 15, 23],
            "volume": [1000, 800, 500, 1000, 700, 800],
            "period": ["FY23", "FY23", "FY23", "FY24", "FY24", "FY24"],
        }
    )

    p = Analysis(slide_layout="slide_wide")
    p.price_volume_mix_analysis(
        df,
        value_col="price",
        weight_col="volume",
        period_col="period",
        groupby_col="product",
        aggregated_output=True,
        show_text=True,
        text_format=".0f",
    )
    p.adjust_yaxis(range=[25000, 41000])
    p.show()
