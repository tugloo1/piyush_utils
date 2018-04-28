from unittest import TestCase
from mock import patch


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests_get_patch = patch('requests.get')
        cls.requests_post_patch = patch('requests.post')
