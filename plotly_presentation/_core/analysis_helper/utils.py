from functools import wraps
import plotly.graph_objects as go


def apply_setting(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if hasattr(self, "parent"):
            if isinstance(result, go.Figure) and hasattr(self.parent, "figure"):
                self.parent.figure = result
            if hasattr(self.parent, "_apply_settings") and callable(
                getattr(self.parent, "_apply_settings")
            ):
                self.parent._apply_settings()
        else:
            if hasattr(self, "_apply_settings") and callable(
                getattr(self, "_apply_settings")
            ):
                self._apply_settings()
        return result

    return wrapper
