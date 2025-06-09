from functools import wraps
import plotly.graph_objects as go


def assign_figure_to_self(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        # Assign to self.figure if result is a Plotly Figure
        self.figure = result
        return result

    return wrapper


def apply_setting(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if hasattr(self, "_apply_settings") and callable(
            getattr(self, "_apply_settings")
        ):
            self._apply_settings()
        return result

    return wrapper
