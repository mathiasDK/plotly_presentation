import plotly.graph_objects as go
import plotly.express as px
from plotly_presentation._core.callouts import Callout
from plotly_presentation._core.style import Style


class Plotter:
    def __init__(self, slide_layout="slide_100%") -> None:
        self.slide_layout = slide_layout
        self.figure = go.Figure()
        self.callout = Callout(self.figure)

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
