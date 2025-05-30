from plotly_presentation._core.analysis_helper.price_volume import PriceVolume, PriceVolumeWrapper
from plotly_presentation._core.colors import PlotColor
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.analysis_helper.comparison import Comparison, ComparisonWrapper
import plotly.graph_objects as go
import numpy as np


class Analysis(Plotter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.figure = None
        self.comparison = ComparisonWrapper(Comparison(), self)
        self.price_volume = PriceVolumeWrapper(PriceVolume(), self)

    def adjust_yaxis(self, range: list) -> go.Figure:
        self.figure.update_yaxes(range=range)
        # Create a secondary x-axis
        self.figure.update_layout(
            xaxis2=dict(overlaying="x", side="top", visible=False)
        )
        # Generate sinus curve data
        x_sin = np.linspace(0, 100, 1000)
        factor = (range[1] - range[0]) * 0.04
        y_sin_1 = (
            np.sin(x_sin) * factor + (range[1] - range[0]) * 0.08 + range[0]
        )  # Adjust y value to the given range

        # Add sinus curve trace
        self.figure.add_trace(
            go.Scatter(
                x=x_sin,
                y=y_sin_1,
                xaxis="x2",
                mode="lines",
                line=dict(color=PlotColor.BG_COLOR.value, width=3),
                name="sin_curve_1",
                showlegend=False,
            )
        )
        self.figure.update_layout(showlegend=False)
        return self.figure
