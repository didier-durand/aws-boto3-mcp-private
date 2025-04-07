import unittest
from sys import platform

from utils import exec_os_command


class TestUtils(unittest.TestCase):

    def test_exec_os_command(self):
        if platform in ["linux","linux2","darwin"]:
            exception, rc, stdout, stderr = exec_os_command("uname -a")
            self.assertIsNone(exception)
            self.assertEqual("",stderr)
            self.assertEqual(0,rc)
            print(stdout)
            if platform == "darwin":
                self.assertTrue("Darwin" in stdout)
            if platform in  ["linux","linux2"]:
                self.assertTrue("Darwin" in stdout)
