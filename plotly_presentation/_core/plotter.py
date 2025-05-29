import plotly.graph_objects as go
import plotly
import plotly.express as px
from plotly_presentation._core.callouts import Callout
from plotly_presentation._core.style import Style


class Plotter:
    def __init__(
        self, figure: go.Figure = None, slide_layout: str = "slide_100%"
    ) -> None:
        """Initiate the plot library with the following extentions:
        .callout

        Args:
            slide_layout (str, optional): The size of the slide. Defaults to "slide_100%".
        """
        self.slide_layout = slide_layout
        if figure is not None:
            self.figure = figure
            if type(figure.data[0]) == plotly.graph_objs.Waterfall:
                self.style._apply_waterfall_style()
        else:
            self.figure = go.Figure()
        self._apply_settings()

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
        if type(func) == plotly.graph_objs.Waterfall:
            self.style._apply_waterfall_style()
        return self.figure

    def show(self):
        self.figure.show()

    def save(self, path):
        self.figure.write_image(path)
