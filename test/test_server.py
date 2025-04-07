import unittest

from boto3_mcp_server import startup_checks


class TestServer(unittest.TestCase):

    def test_startup_checks(self):
        self.assertTrue(startup_checks())
