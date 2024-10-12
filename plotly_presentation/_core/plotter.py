import plotly.graph_objects as go
import plotly.express as px
from plotly_presentation._core.callouts import Callout
from plotly_presentation._core.style import Style
from plotly_presentation._core.colors import Color


class Plotter:
    def __init__(self, slide_layout: str = "slide_100%") -> None:
        """Initiate the plot library with the following extentions:
        .callout
        .color

        Args:
            slide_layout (str, optional): The size of the slide. Defaults to "slide_100%".
        """
        self.slide_layout = slide_layout
        self.figure = go.Figure()
        self.callout = Callout(self.figure)
        self.color = Color

    def _initialize_figure(self) -> None:
        pass

    def _apply_settings(self) -> None:
        self.callout = Callout(self.figure)
        self.style = Style(self.figure, self.slide_layout)

    def express(self, type: str, **kwargs) -> go.Figure:
        self.figure = getattr(px, type)(**kwargs)
        self._apply_settings()
        return self.figure

    def add_trace(self, func) -> go.Figure:
        self.figure.add_trace(func)
        self._apply_settings()
        return self.figure

    def show(self):
        self.figure.show()

    def save(self, path):
        self.figure.write_image(path)
