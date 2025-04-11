import unittest
from multiprocessing import Process
from time import sleep

import requests
import uvicorn

import boto3_fastapi_server
from boto3_fastapi_server import BackendApi, MCP_HOST, MCP_PORT, fastapi_server, ExecRequest
from boto3_mcp_server import MCP_SERVER_NAME

class TestBoto3FastapiServer(unittest.IsolatedAsyncioTestCase):


    proc: Process = None

    def setUp(self):
        print(f"\n### starting {unittest.TestCase.id(self)}")
        self.endpoint = f"http://{MCP_HOST}:{MCP_PORT}"  # noqa
        response = None
        count: int = 0
        while True:
            count += 1
            if count > 5:
                self.fail("fastapi_server did not start properly")
            app: str = (f"{boto3_fastapi_server=}".split('=', maxsplit=1)[0]
                   + ":" + f"{fastapi_server=}".split('=', maxsplit=1)[0])
            try:
                response = requests.get(self.endpoint, timeout=2)
            except requests.exceptions.ConnectionError:
                TestBoto3FastapiServer.proc = Process(target=uvicorn.run,
                                    kwargs={
                                        "app": app,
                                        "host": MCP_HOST,
                                        "port": MCP_PORT,
                                        "log_level": "info"},
                                    daemon=True
                                    )
                TestBoto3FastapiServer.proc.start()
                while not TestBoto3FastapiServer.proc.is_alive():
                    sleep(0.2)
            if response is not None:
                if response.status_code == 200 and response.text == f"{MCP_SERVER_NAME}\n":
                    break
            sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        print(f"\n### ending {TestBoto3FastapiServer.__name__}")

    def test_invalid_url(self):
        response = requests.post(self.endpoint + f"/{BackendApi.INVALID_URL}", timeout=2)
        print(f"response: {response.content.decode()}")
        self.assertEqual(404, response.status_code)

    def test_get_root_url(self):
        response = requests.get(self.endpoint,timeout=2)
        print(f"response: {response.content.decode()}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(f"{MCP_SERVER_NAME}\n", response.text)

    # curl -d '{"code":"x=3*2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/execute_python
    def test_post_execute_python(self):
        code = """
        x=0
        print(f"x:{x}")
        """
        exec_request = ExecRequest(code=code)
        json_str = exec_request.model_dump_json(exclude_unset=True)
        response = requests.post(self.endpoint + f"/{BackendApi.EXECUTE_PYTHON}", timeout=20,data=json_str.encode(encoding="utf-8"))
        print(f"request: {json_str} - response: {response.content.decode()}")
        self.assertEqual(200, response.status_code)
        self.assertEqual("\"\\nx:0\\n\"",response.text)

    def test_sandbox_config(self):
        code = """
        import sys
        import os
        import platform
        import shutil
        print(f"Linux distribution: {platform.uname()}")
        print(f"current dir: {os.getcwd()}")
        print(f"root dir content: {os.listdir(path='/')}")
        total, used, free = shutil.disk_usage("/")
        print(f"storage - total: {total//2**20:,} MiB, used: {used//2**20:,} MiB , free: {free//2**20:,} MiB")
        print(f"Python version: {sys.version}")
        print(f"Python version_info: {sys.version_info}")
        print("installed Python modules:")
        help("modules")
        """
        exec_request = ExecRequest(code=code)
        json_str = exec_request.model_dump_json(exclude_unset=True)
        response = requests.post(self.endpoint + f"/{BackendApi.EXECUTE_PYTHON}", timeout=20,data=json_str.encode(encoding="utf-8"))
        self.assertEqual(200, response.status_code)
        print("response:")
        print(response.text.replace("\\n", "\n"))

    def test_boto3(self):
        # https://stackoverflow.com/questions/54217137/from-urllib3-util-ssl-import-importerror-cannot-import-name-ssl
        code = """
        import pip
        # pip.main(['install', '--upgrade', 'urllib3'])
        # import boto3
        # import botocore
        """
        exec_request = ExecRequest(code=code)
        json_str = exec_request.model_dump_json(exclude_unset=True)
        response = requests.post(self.endpoint + f"/{BackendApi.EXECUTE_PYTHON}", timeout=20,data=json_str.encode(encoding="utf-8"))
        self.assertEqual(200, response.status_code)
        print("response:")
        print(response.text.replace("\\n", "\n"))
