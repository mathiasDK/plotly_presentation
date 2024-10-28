import unittest
from plotly_presentation._core.colors.utils import _convert_to_rgb


class TestConvertToRGB(unittest.TestCase):
    def test_rgb_input(self):
        color = "rgb(0,0,0)"
        expected_color = "rgb(0,0,0)"
        color = _convert_to_rgb(color=color)
        self.assertEqual(color, expected_color)

    def test_hex_input(self):
        color = "#000000"
        expected_color = (0, 0, 0)
        color = _convert_to_rgb(color=color)
        self.assertEqual(color, expected_color)

    def test_tuple_input(self):
        color = (0, 0, 0)
        expected_color = "rgb(0, 0, 0)"
        color = _convert_to_rgb(color=color)
        self.assertEqual(color, expected_color)
