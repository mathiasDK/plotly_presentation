import unittest
from plotly_presentation._core.plotter import Plotter
from plotly_presentation._core.colors import SequentialColor, DivergentColor
from plotly_presentation._core.style import Style
import plotly.graph_objects as go
import plotly.express as px


class StyleTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    def test_set_color_palette_color_dict_line(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.line.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_set_color_palette_palette_sequential_line(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="reds")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(249.0, 143.0, 112.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_sequential_negative_line(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="hot_cold")

        actual_colors = {
            d.name: d.line.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(96.0, 116.0, 141.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging_line(self):
        p = Plotter()
        p.express(type="line", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging", palette_name="reds")

        actual_colors = {d.name: d.line.color for d in p.figure.data}
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "AAPL": "rgb(194.0, 194.0, 194.0)",
            "FB": "rgb(148.0, 12.0, 8.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_color_dict_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.marker.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_set_color_palette_palette_sequential_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="reds")

        actual_colors = {
            d.name: d.marker.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(249.0, 143.0, 112.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_sequential_negative_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="sequential", palette_name="hot_cold")

        actual_colors = {
            d.name: d.marker.color for d in p.figure.data if d.name in ("GOOG", "FB")
        }
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "FB": "rgb(96.0, 116.0, 141.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_palette_diverging_bar(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_color_palette(palette_type="diverging", palette_name="reds")

        actual_colors = {d.name: d.marker.color for d in p.figure.data}
        expected_colors = {
            "GOOG": "rgb(215.0, 56.0, 9.0)",
            "AAPL": "rgb(194.0, 194.0, 194.0)",
            "FB": "rgb(148.0, 12.0, 8.0)",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_set_color_palette_color_dict_scatter(self):
        p = Plotter()
        p.express(
            type="scatter", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"]
        )

        new_colors = {
            "GOOG": "#000",
            "AAPL": "#a334f1",
            "FB": "#56ff11",
        }

        p.style.set_color_palette(color_dict=new_colors)
        actual_colors = {d.name: d.line.color for d in p.figure.data}
        self.assertEqual(new_colors, actual_colors)

    def test_set_color_palette_invalid_palette_type(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        _VALID_PALETTES = [
            "sequential",
            "diverging",
            "sequential_negative",
            "diverging_negative",
        ]

        with self.assertRaises(ValueError) as context:
            p.style.set_color_palette(
                palette_type="some palette that does not exist", palette_name="reds"
            )
            # Optionally, check the exception message
            self.assertEqual(
                str(context.exception),
                f"Invalid palette type. Must be one of {_VALID_PALETTES}",
            )

    def test_set_color_palette_invalid_input(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        with self.assertRaises(AttributeError) as context:
            p.style.set_color_palette(palette_type=None, color_dict=None)
            self.assertEqual(
                str(context.exception),
                "Either palette_type or color_dict must be provided",
            )

    def test_waterfall_style(self):
        figure = go.Figure(
            go.Waterfall(
                name="20",
                orientation="v",
                measure=[
                    "relative",
                    "relative",
                    "total",
                    "relative",
                    "relative",
                    "total",
                ],
                x=[
                    "Sales",
                    "Consulting",
                    "Net revenue",
                    "Purchases",
                    "Other expenses",
                    "Profit before tax",
                ],
                textposition="outside",
                text=["+60", "+80", "", "-40", "-20", "Total"],
                y=[60, 80, 0, -40, -20, 0],
            )
        )
        s = Style(figure, slide_layout="slide_100%")
        s._apply_waterfall_style()

        actual_colors = {
            "increase": s.figure.data[0].increasing.marker.color,
            "decrease": s.figure.data[0].decreasing.marker.color,
            "totals": s.figure.data[0].totals.marker.color,
            "connectors": s.figure.data[0].connector.line.color,
        }
        expected_colors = {
            "increase": "#09d738",
            "decrease": "#D73809",
            "totals": "#CFD6D5",
            "connectors": "black",
        }
        self.assertEqual(actual_colors, expected_colors)

    def test_slide_layout_size(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])

        p.style._set_width_and_height("slide_25%")
        self.assertEqual(960.0 / 2, p.figure.layout.width)
        self.assertEqual(540.0 / 2, p.figure.layout.height)

        p.style._set_width_and_height("slide_50%")
        self.assertEqual(960.0 / 2, p.figure.layout.width)
        self.assertEqual(540.0, p.figure.layout.height)

        p.style._set_width_and_height("slide_75%")
        self.assertEqual(960.0 * 0.75 * 0.8, p.figure.layout.width)
        self.assertEqual(540.0 * 0.8, p.figure.layout.height)

        p.style._set_width_and_height("slide_100%")
        self.assertEqual(960.0, p.figure.layout.width)
        self.assertEqual(540.0, p.figure.layout.height)

        p.style._set_width_and_height("slide_wide")
        self.assertEqual(960.0, p.figure.layout.width)
        self.assertEqual(540 * 0.75, p.figure.layout.height)

    def test_unknown_sequential_palette(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        with self.assertRaises(TypeError) as context:
            p.style.set_color_palette(palette_type="sequential", palette_name="unknown")
            self.assertEqual(
                str(context.exception),
                "Invalid palette name. Must be one of {palette_names}",
            )

    def test_unknown_divergin_palette(self):
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        with self.assertRaises(TypeError) as context:
            p.style.set_color_palette(palette_type="diverging", palette_name="unknown")
            self.assertEqual(
                str(context.exception),
                "Invalid palette name. Must be one of {palette_names}",
            )

    def test_set_legend_default(self):
        """Test set_legend with default parameters"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend()

        legend = p.figure.layout.legend
        self.assertEqual(legend.orientation, "h")
        self.assertEqual(legend.x, 0.5)
        self.assertEqual(legend.y, 1.02)
        self.assertEqual(legend.xanchor, "center")
        self.assertEqual(legend.yanchor, "bottom")

    def test_set_legend_position_top(self):
        """Test set_legend with position='top'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="top")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, 0.5)
        self.assertEqual(legend.y, 1.02)
        self.assertEqual(legend.xanchor, "center")
        self.assertEqual(legend.yanchor, "bottom")

    def test_set_legend_position_bottom(self):
        """Test set_legend with position='bottom'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="bottom")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, 0.5)
        self.assertEqual(legend.y, -0.15)
        self.assertEqual(legend.xanchor, "center")
        self.assertEqual(legend.yanchor, "top")

    def test_set_legend_position_left(self):
        """Test set_legend with position='left'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="left")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, -0.15)
        self.assertEqual(legend.y, 0.5)
        self.assertEqual(legend.xanchor, "right")
        self.assertEqual(legend.yanchor, "middle")

    def test_set_legend_position_right(self):
        """Test set_legend with position='right'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="right")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, 1.02)
        self.assertEqual(legend.y, 0.5)
        self.assertEqual(legend.xanchor, "left")
        self.assertEqual(legend.yanchor, "middle")

    def test_set_legend_position_top_left(self):
        """Test set_legend with compound position='top-left'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="top-left")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, -0.15)
        self.assertEqual(legend.y, 1.02)
        self.assertEqual(legend.xanchor, "right")
        self.assertEqual(legend.yanchor, "bottom")

    def test_set_legend_position_top_right(self):
        """Test set_legend with compound position='top-right'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(position="top-right")

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, 1.02)
        self.assertEqual(legend.y, 1.02)
        self.assertEqual(legend.xanchor, "left")
        self.assertEqual(legend.yanchor, "bottom")

    def test_set_legend_orientation_vertical(self):
        """Test set_legend with orientation='v'"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(orientation="v")

        legend = p.figure.layout.legend
        self.assertEqual(legend.orientation, "v")

    def test_set_legend_font_size(self):
        """Test set_legend with custom font size"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(font_size=16)

        legend = p.figure.layout.legend
        self.assertEqual(legend.font.size, 16)

    def test_set_legend_bgcolor(self):
        """Test set_legend with background color"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(bgcolor="rgba(255, 255, 255, 0.8)")

        legend = p.figure.layout.legend
        self.assertEqual(legend.bgcolor, "rgba(255, 255, 255, 0.8)")

    def test_set_legend_all_options(self):
        """Test set_legend with all options combined"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_legend(
            position="bottom", orientation="v", font_size=14, bgcolor="lightgray"
        )

        legend = p.figure.layout.legend
        self.assertEqual(legend.x, 0.5)
        self.assertEqual(legend.y, -0.15)
        self.assertEqual(legend.orientation, "v")
        self.assertEqual(legend.font.size, 14)
        self.assertEqual(legend.bgcolor, "lightgray")

    def test_set_title_basic(self):
        """Test set_title with just a title"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_title("Stock Prices Over Time")

        title = p.figure.layout.title
        self.assertEqual(title.text, "Stock Prices Over Time")
        self.assertEqual(title.x, 0.05)
        self.assertEqual(title.xanchor, "left")
        self.assertEqual(title.font.size, 18)

    def test_set_title_with_subtitle(self):
        """Test set_title with title and subtitle"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_title(
            title="Stock Prices Over Time",
            subtitle="Daily closing prices from 2018-2020",
        )

        title = p.figure.layout.title
        self.assertEqual(title.text, "Stock Prices Over Time")
        self.assertEqual(title.subtitle.text, "Daily closing prices from 2018-2020")
        self.assertEqual(title.subtitle.font.size, 14)
        self.assertEqual(title.x, 0.05)
        self.assertEqual(title.xanchor, "left")
        self.assertEqual(title.font.size, 18)

    def test_set_title_custom_sizes(self):
        """Test set_title with custom title and subtitle sizes"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_title(
            title="Stock Prices",
            subtitle="Subtitle text",
            title_size=24,
            subtitle_size=16,
        )

        title = p.figure.layout.title
        self.assertEqual(title.text, "Stock Prices")
        self.assertEqual(title.subtitle.text, "Subtitle text")
        self.assertEqual(title.font.size, 24)
        self.assertEqual(title.subtitle.font.size, 16)

    def test_set_title_with_none_subtitle(self):
        """Test set_title with None subtitle (should still set subtitle structure)"""
        p = Plotter()
        p.express(type="bar", data_frame=self.df, x="date", y=["GOOG", "AAPL", "FB"])
        p.style.set_title(title="Stock Prices", subtitle=None)

        title = p.figure.layout.title
        self.assertEqual(title.text, "Stock Prices")
        self.assertIsNotNone(title.subtitle)
        self.assertEqual(title.subtitle.text, None)

    def test_update_discrete_color_map_basic(self):
        """Test basic functionality of update_discrete_color_map"""
        # Create a simple figure with named traces
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Trace1'))
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[3, 2, 1], name='Trace2'))
        
        # Create a discrete color map
        color_map = {
            'Trace1': '#FF0000',  # Red
            'Trace2': '#00FF00'   # Green
        }
        
        # Create style object
        style = Style(fig, 'slide_100%', discrete_color_map=color_map)
        
        # Apply the discrete color mapping
        style.update_discrete_color_map()
        
        # Verify that colors were applied correctly
        self.assertEqual(fig.data[0].marker.color, '#FF0000')
        self.assertEqual(fig.data[1].line.color, '#00FF00')

    def test_update_discrete_color_map_with_none_traces(self):
        """Test update_discrete_color_map with traces that have no color attributes"""
        # Create a figure with traces that may not have color properties
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Bar Trace'))
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[3, 2, 1], name='Scatter Trace'))
        
        # Create a discrete color map
        color_map = {
            'Bar Trace': '#FF5733',
            'Scatter Trace': '#33FF57'
        }
        
        # Create style object
        style = Style(fig, 'slide_100%', discrete_color_map=color_map)
        
        # Apply the discrete color mapping
        style.update_discrete_color_map()
        
        # Verify that colors were applied correctly
        self.assertEqual(fig.data[0].marker.color, '#FF5733')
        self.assertEqual(fig.data[1].line.color, '#33FF57')

    def test_update_discrete_color_map_empty_map(self):
        """Test update_discrete_color_map with empty color map"""
        # Create a figure with named traces
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Trace1'))
        
        # Empty color map
        color_map = {}
        
        # Create style object
        style = Style(fig, 'slide_100%', discrete_color_map=color_map)
        initial_color = fig.data[0].marker.color
        
        # Apply the discrete color mapping (should not fail)
        style.update_discrete_color_map()
        new_color = fig.data[0].marker.color
        
        # Colors should remain unchanged
        self.assertEqual(initial_color, new_color)

    def test_update_discrete_color_map_nonexistent_trace(self):
        """Test update_discrete_color_map with color map for non-existent trace"""
        # Create a figure with named traces
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Trace1'))
        
        # Color map with non-existent trace name
        color_map = {
            'NonExistentTrace': '#FF0000',
            'Trace1': '#00FF00'
        }
        
        # Create style object
        style = Style(fig, 'slide_100%', discrete_color_map=color_map)
        
        # Apply the discrete color mapping
        style.update_discrete_color_map()
        
        # Only existing trace should be updated
        self.assertEqual(fig.data[0].marker.color, '#00FF00')

    def test_update_discrete_color_map_no_discrete_color_map(self):
        """Test update_discrete_color_map when discrete_color_map is None"""
        # Create a figure with named traces
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Trace1'))
        
        # No discrete color map provided
        style = Style(fig, 'slide_100%')
        
        # Apply the discrete color mapping (should not fail)
        style.update_discrete_color_map()

    def test_update_discrete_color_map_multiple_trace_types(self):
        """Test update_discrete_color_map with different trace types"""
        # Create a figure with different trace types
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[1, 2, 3], y=[1, 2, 3], name='Bar Trace'))
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[3, 2, 1], name='Scatter Trace'))
        fig.add_trace(go.Scattergl(x=[1, 2, 3], y=[2, 3, 1], name='ScatterGL Trace'))
        
        # Create a discrete color map
        color_map = {
            'Bar Trace': '#FF0000',
            'Scatter Trace': '#00FF00',
            'ScatterGL Trace': '#0000FF'
        }
        
        # Create style object
        style = Style(fig, 'slide_100%', discrete_color_map=color_map)
        
        # Apply the discrete color mapping
        style.update_discrete_color_map()
        
        # Verify that colors were applied correctly
        self.assertEqual(fig.data[0].marker.color, '#FF0000')
        self.assertEqual(fig.data[1].line.color, '#00FF00')
        self.assertEqual(fig.data[2].line.color, '#0000FF')