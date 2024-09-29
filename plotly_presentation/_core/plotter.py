import plotly.graph_objects as go
import plotly.express as px

class Plotter:
    def __init__(self)->None:
        self.figure = go.Figure()

    def _initialize_figure(self)->None:
        pass

    def _apply_settings(self)->None:
        pass

    def express(self, type:str, **kwargs)->go.Figure:
        self.figure = getattr(px, type)(**kwargs)
        self._apply_settings()
        return self.figure

    def add_trace(self, func)->go.Figure:
        self.figure.add_trace(func)
        self._apply_settings()
        return self.figure

    def show(self):
        self.figure.show()

    def save(self, path):
        self.figure.write_image(path)