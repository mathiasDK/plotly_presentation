import unittest
from plotly_presentation._core.utils.dict_funcs import update_dict


class UpdateDictTest(unittest.TestCase):
    def test_valid_update(self):
        existing_dict = {"var": [1, 2, 3], "col": {"col1": "a", "col2": "b"}}
        new_values = {"col": {"col1": "aa", "col3": "c"}}
        new_dict = update_dict(existing_dict, new_values)
        expected_dict = {
            "var": [1, 2, 3],
            "col": {"col1": "aa", "col2": "b", "col3": "c"},
        }
        self.assertEqual(new_dict, expected_dict)

    def test_order(self):
        existing_dict = {"var": [1, 2, 3], "col": {"col1": "a", "col2": "b"}}
        new_values = {"col": {"col1": "aa", "col3": "c"}}
        d1 = update_dict(existing_dict, new_values)
        d2 = update_dict(new_values, existing_dict)
        self.assertEqual(d1, d2)
