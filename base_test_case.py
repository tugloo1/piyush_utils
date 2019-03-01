from piyush_utils.basic_funcs import BasicFuncs
from numpy import testing
from unittest import TestCase
from mock import patch, mock_open


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests_get_patch = patch('requests.get')
        cls.requests_post_patch = patch('requests.post')

    @staticmethod
    def get_file_open_patch(read_data: str):
        """
        :param read_data: Data that will be mocked as being part of the text file
        :return:
        """
        m = mock_open(read_data=read_data)
        return patch('builtins.open', m, create=True)

    @staticmethod
    def assert_numpy_array_equal(x, y, err_msg='', verbose=True):
        testing.assert_array_equal(x, y, err_msg=err_msg, verbose=verbose)

    def assert_file_content_equal_to_string(self, actual_string: str, file_path: str):
        """ This method will check if the string in the file path is the same as the actual_string
        :param actual_string:
        :param file_path:
        :return:
        """
        file_string = BasicFuncs.load_file_as_string(file_path)
        self.assertMultiLineEqual(file_string, actual_string)
