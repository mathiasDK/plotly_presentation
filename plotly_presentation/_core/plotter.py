import plotly.graph_objects as go
import plotly.express as px

class Plotter:
    def __init__(self)->None:
        self._initialize_figure()

    def _initialize_figure(self)->None:
        self.figure = go.Figure()

    def express(self, type:str, **args, **kwargs)->go.Figure:
        self.figure = getattr(px, type)(**args, **kwargs)
        return self.figure

    def add_trace(self, func)->go.Figure:
        self.figure.add_trace(func)
        return self.figure

    def show(self):
        self.figure.show()

    def save(self, path):
        self.figure.write_image(path)