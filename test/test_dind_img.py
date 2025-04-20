
import unittest

import pytest

from utils import exec_os_command


class TestDindImage(unittest.TestCase):

    def setUp(self):
        self.account = "didierdurand"
        self.image = "aws-boto3-mcp"

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

    @pytest.mark.skip
    def test_pull_alpython(self):
        command = "docker pull didierdurand/alpython"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        print(stderr)
        self.assertEqual(0, rc)
        self.assertEqual("", stderr)
        self.assertEqual("", stdout)
