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
