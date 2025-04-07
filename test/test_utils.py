import unittest
from sys import platform

from utils import exec_os_command


class TestUtils(unittest.TestCase):

    def test_exec_os_command_ko(self):
        exception, rc, stdout, stderr = exec_os_command("foo-bar-foo")
        self.assertTrue(isinstance(exception, FileNotFoundError))
        self.assertIsNone(rc)
        self.assertIsNone(stderr)
        self.assertIsNone(stdout)

    def test_exec_os_command_ok(self):
        if platform in ["linux","linux2","darwin"]:
            exception, rc, stdout, stderr = exec_os_command("uname -a")
            self.assertIsNone(exception)
            self.assertEqual("",stderr)
            self.assertEqual(0,rc)
            print(stdout)
            if platform == "darwin":
                self.assertTrue("Darwin" in stdout)
            if platform in  ["linux","linux2"]:
                self.assertTrue("Darwin" in stdout,f"uname output: {stdout}")
