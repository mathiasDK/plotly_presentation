import unittest
from plotly_presentation._core.colors.diverging import create_diverging_color_list
import plotly.express as px


class CalloutTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    def test_create_diverging_color_list_length_hex(self):
        colors = create_diverging_color_list("#000000", "#ffffff", "#45ff11", 6)
        self.assertEqual(len(colors), 6)

    def test_create_diverging_color_list_length_tuple(self):
        colors = create_diverging_color_list(
            (0, 0, 0), (255, 255, 255), (10, 10, 10), 6
        )
        self.assertEqual(len(colors), 6)

    def test_create_diverging_color_list_length_rgb(self):
        colors = create_diverging_color_list(
            "rgb(0,0,0)", "rgb(255,255,255)", "rgb(10,10,10)", 6
        )
        self.assertEqual(len(colors), 6)

    def test_create_diverging_color_list_length_hex_unequal(self):
        colors = create_diverging_color_list("#000000", "#60748D", "#ffffff", 11)
        self.assertEqual(len(colors), 11)
        self.assertEqual(colors[0], "rgb(0.0, 0.0, 0.0)")
        self.assertEqual(colors[5], "rgb(96.0, 116.0, 141.0)")
        self.assertEqual(colors[-1], "rgb(255.0, 255.0, 255.0)")

    def test_create_diverging_color_list_length_tuple_unequal(self):
        colors = create_diverging_color_list(
            (0, 0, 0), (255, 255, 255), (10, 10, 10), 11
        )
        self.assertEqual(len(colors), 11)

    def test_create_diverging_color_list_length_rgb_unequal(self):
        colors = create_diverging_color_list(
            "rgb(0,0,0)", "rgb(255,255,255)", "rgb(10,10,10)", 11
        )
        self.assertEqual(len(colors), 11)
