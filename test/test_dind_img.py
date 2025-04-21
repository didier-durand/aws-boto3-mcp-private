import unittest

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
        exception, rc, stdout, stderr = exec_os_command(command=f"docker run --rm --name {image} "
                                                                f"{account}/{image} {command}",
                                                        debug=False)
        self.assertIsNone(exception)
        return rc, stdout, stderr

    def test_get_version_in_dind(self):
        command = "docker --version"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        print(stderr)
        self.assertEqual("", stderr)
        self.assertTrue(stdout.startswith("Docker version"))
        self.assertEqual(0, rc)

    @unittest.skip
    def test_pull_alpython_in_dind(self):
        command = "docker pull didierdurand/alpython"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        print(stderr)
        self.assertEqual("", stderr)
        self.assertEqual("", stdout)
        self.assertEqual(0, rc)
