from piyush_utils.base_test_case import BaseTestCase
from piyush_utils.basic_funcs import BasicFuncs


class BasicFuncsTests(BaseTestCase):
    def test_load_json_file(self):
        file_data = '{"key": "value"}'
        with self.get_file_open_patch(file_data):
            a = BasicFuncs.load_json_file('does-not-matter')
        valid_output = {'key': 'value'}
        self.assertEqual(a, valid_output)