import textwrap
import unittest

import pytest

from utils import exec_os_command, get_timestamp


class TestAlpythonImage(unittest.TestCase):

    def setUp(self):
        self.account = "didierdurand"
        self.image = "alpython"

    def run_python_container(self, account, image, command):
        exception, rc, stdout, stderr = exec_os_command(f"docker rm {image}")
        self.assertIsNone(exception)
        if rc == 1:
            self.assertEqual(f"Error response from daemon: No such container: {image}\n", stderr)
        elif rc == 0:
            self.assertEqual(f"{image}\n", stdout)
        else:
            self.fail(f"unexpected rc: {rc}")
        exception, rc, stdout, stderr = exec_os_command(f"docker pull {account}/{image}")
        self.assertIsNone(exception)
        self.assertEqual(0, rc)
        exception, rc, stdout, stderr = exec_os_command(f"docker run --name {image} "
                                                        f"{account}/{image} {command}")
        self.assertIsNone(exception)
        return rc, stdout, stderr

    def test_get_python_version(self):
        command = "python3.12 --version"
        rc, stdout,stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        self.assertEqual(0, rc)
        self.assertEqual("", stderr)
        self.assertEqual("Python 3.12.10\n", stdout)

    @pytest.mark.skip
    def test_exec_python_print(self):
        msg = get_timestamp()
        command = f"python3.12 -c \"print('{msg}')\""
        _, stdout, _ = self.run_python_container(self.account, self.image, command)
        print(stdout)
        self.assertEqual(f"{msg}", stdout)

    @pytest.mark.skip
    def test_exec_python_code_ko(self):
        code = """
        x=1
        y=0
        x/y
        """
        code=textwrap.dedent(code)
        command = f"python3.12 -c \"{code}\""
        rc, stdout,stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        self.assertEqual(1, rc)
        self.assertEqual("", stdout)
        self.assertEqual("", stderr)
