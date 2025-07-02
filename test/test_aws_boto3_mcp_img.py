import unittest

from utils import exec_os_command, get_timestamp


class TestAwsBoto3McpImage(unittest.TestCase):

    def setUp(self):
        self.account = "didierdurand"
        self.image = "aws-boto3-mcp"

    def run_python_container(self, account, image, command):
        exception, rc, stdout, stderr = exec_os_command(f"docker rm {image}", debug=False)
        self.assertIsNone(exception)
        if rc == 1:
            self.assertEqual(f"Error response from daemon: No such container: {image}\n", stderr)
        elif rc == 0:
            self.assertEqual(f"{image}\n", stdout)
        else:
            self.fail(f"unexpected rc: {rc}")
        exception, rc, stdout, stderr = exec_os_command(f"docker pull {account}/{image}", debug=False)
        self.assertIsNone(exception)
        self.assertEqual(0, rc)
        command: str = (f"docker run --rm --privileged --network host "
                        f"-v /var/run/docker.sock:/var/run/docker.sock "
                        f"--name {image} {account}/{image} {command}")
        exception, rc, stdout, stderr = exec_os_command(command=command,
                                                        check=True,
                                                        debug=True)
        self.assertIsNone(exception)
        return rc, stdout, stderr

    def test_get_docker_version_in_dind(self):
        command = "docker --version"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        print(stderr)
        self.assertEqual("", stderr)
        self.assertTrue(stdout.startswith("Docker version"))
        self.assertEqual(0, rc)

    def test_pull_nginx_in_dind(self):
        command = "docker image rm nginx"
        self.run_python_container(self.account, self.image, command)
        command = "docker pull nginx"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print("stdout:", stdout)
        print("stderr:", stderr)
        self.assertEqual("", stderr)
        self.assertTrue("Pulling from library/nginx" in stdout)
        self.assertEqual(0, rc)

    def test_get_python_version_in_dind(self):
        command = "python3.12 --version"
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        self.assertEqual(0, rc)
        self.assertEqual("", stderr)
        self.assertTrue(stdout.startswith("Python 3.12"))

    @unittest.skip
    def test_exec_python_print_in_dind(self):
        timestamp = get_timestamp()
        code = f"python3.12 -c \"print('{timestamp}')\""
        print(f"\ncode: {code}")
        rc, stdout, stderr = self.run_python_container(self.account, self.image, code)
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
        self.assertEqual(0, rc)
        self.assertEqual("", stderr)
        self.assertEqual(f"{timestamp}", stdout)

    @unittest.skip
    def test_exec_python_error_in_dind(self):
        code = "1/0"
        command = f"python3.12 -c \"{code}\""
        rc, stdout, stderr = self.run_python_container(self.account, self.image, command)
        print(stdout)
        self.assertEqual(1, rc)
        self.assertEqual("", stdout)
        self.assertEqual("", stderr)
