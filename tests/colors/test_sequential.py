import unittest
from plotly_presentation._core.colors.sequential import create_sequential_color_list
import plotly.express as px


class CalloutTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = px.data.stocks()

    def test_create_sequential_color_list_length_hex(self):
        colors = create_sequential_color_list("#000000", "#ffffff", 6)
        self.assertEqual(len(colors), 6)

    def test_create_sequential_color_list_length_tuple(self):
        colors = create_sequential_color_list((0, 0, 0), (255, 255, 255), 6)
        self.assertEqual(len(colors), 6)

    def test_create_sequential_color_list_length_rgb(self):
        colors = create_sequential_color_list("rgb(0,0,0)", "rgb(255,255,255)", 6)
        self.assertEqual(len(colors), 6)
