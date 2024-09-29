
class Style:
    def __init__(self, figure, slide_layout) -> None:
        self.figure = figure
        self.slide_layout = slide_layout

    def _set_width_and_height(self, slide_layout="slide_100%"):
        """Set plot width and height based on the layout"""
        self.plot_width = 960
        self.plot_height = 540
        height_multiplier, width_multiplier = 1.0, 1.0

        if slide_layout == "slide_75%":
            height_multiplier = 1.0 * 0.8
            width_multiplier = 0.75 * 0.8

        elif slide_layout == "slide_50%":
            height_multiplier = 1.0
            width_multiplier = 0.5

        elif slide_layout == "slide_25%":
            height_multiplier = 0.5
            width_multiplier = 0.5

        self.figure.update_layout(
            height = int(self.plot_height * height_multiplier),
            width = int(self.plot_width * width_multiplier)
        )
