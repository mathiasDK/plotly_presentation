
from plotly_presentation._core.analysis_helper.price_volume import PriceVolume
from plotly_presentation._core.colors import PlotColor
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.analysis_helper.comparison import Comparison
import plotly.graph_objects as go
import numpy as np
from plotly_presentation._core.analysis_helper.utils import apply_setting


class Analysis(Plotter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.figure = None

    @apply_setting
    def comparison(self, method_name: str, *args, **kwargs):
        """
        Calls a specific comparison method from the Comparison class.

        Args:
            method_name (str): Name of the comparison method to call.
            *args: Arguments to pass to the comparison method.
            **kwargs: Keyword arguments to pass to the comparison method.

        Returns:
            The result of the called comparison method.
        """
        comp = Comparison()
        method = getattr(comp, method_name, None)
        if not method or not callable(method):
            raise AttributeError(f"'Comparison' object has no method '{method_name}'")
        result = getattr(comp, method_name)(*args, **kwargs)
        if isinstance(result, go.Figure):
            # If the result is a Plotly Figure, assign it to self.figure
            self.figure = result
        return result

    @apply_setting
    def price_volume(self, method_name: str, *args, **kwargs):
        """
        Calls a specific method from the PriceVolume class.

        Args:
            method_name (str): Name of the method to call.
            *args: Arguments to pass to the method.
            **kwargs: Keyword arguments to pass to the method.

        Returns:
            The result of the called price volume method.
        """
        pv = PriceVolume()
        method = getattr(pv, method_name, None)
        if not method or not callable(method):
            raise AttributeError(f"'PriceVolume' object has no method '{method_name}'")
        result = getattr(pv, method_name)(*args, **kwargs)
        if isinstance(result, go.Figure):
            # If the result is a Plotly Figure, assign it to self.figure
            self.figure = result
        return result

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
