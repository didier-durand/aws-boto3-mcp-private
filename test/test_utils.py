import unittest
from sys import platform

from utils import exec_os_command, is_xml


class TestUtils(unittest.TestCase):

    def test_exec_os_command_ko(self):
        exception, rc, stdout, stderr = exec_os_command("foo-bar-foo")
        self.assertTrue(isinstance(exception, FileNotFoundError))
        self.assertIsNone(rc)
        self.assertIsNone(stderr)
        self.assertIsNone(stdout)

    def test_exec_os_command_ok(self):
        if platform in ["linux", "linux2", "darwin"]:
            exception, rc, stdout, stderr = exec_os_command("uname -a")
            self.assertIsNone(exception)
            self.assertEqual("", stderr)
            self.assertEqual(0, rc)
            print(stdout)
            if platform == "darwin":
                self.assertTrue("Darwin" in stdout)
            if platform in ["linux", "linux2"]:
                self.assertTrue("Linux" in stdout, f"uname output: {stdout}")

    def test_is_xml(self):
        xml = "<persons><person><name>John</name></person></persons>"
        self.assertTrue(is_xml(xml))
        #
        xml = "<value>1</value><value>2</value>"
        self.assertFalse(is_xml(xml))
