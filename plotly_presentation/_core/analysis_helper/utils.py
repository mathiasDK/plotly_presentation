from functools import wraps
import plotly.graph_objects as go


def assign_figure_to_self(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        # If parent exists, assign to parent.figure, otherwise assign to self.figure
        if hasattr(self, "parent") and self.parent is not None:
            self.parent.figure = result
        else:
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
