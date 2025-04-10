import unittest
from multiprocessing import Process
from time import sleep

import requests
import uvicorn

import boto3_fastapi_server
from boto3_fastapi_server import BackendApi, MCP_HOST, MCP_PORT, fastapi_server, ExecRequest
from boto3_mcp_server import MCP_SERVER_NAME

class TestBoto3McpServer(unittest.IsolatedAsyncioTestCase):


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
            try:
                response = requests.get(self.endpoint, timeout=2)
            except requests.exceptions.ConnectionError:
                TestBoto3McpServer.proc = Process(target=uvicorn.run,
                                    kwargs={
                                        "app": f"{boto3_fastapi_server=}".split('=',maxsplit=1)[0]
                                               + ":" + f"{fastapi_server=}".split('=',maxsplit=1)[0],
                                        "host": MCP_HOST,
                                        "port": MCP_PORT,
                                        "log_level": "info"},
                                    daemon=True
                                    )
                TestBoto3McpServer.proc.start()
                while not self.proc.is_alive():
                    sleep(0.2)
            if response is not None:
                if response.status_code == 200 and response.text == MCP_SERVER_NAME:
                    break
            sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        print(f"\n### ending {TestBoto3McpServer.__name__}")

    def test_root_url(self):
        response = requests.get(self.endpoint,timeout=2)
        print(f"response: {response.content.decode()}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(MCP_SERVER_NAME, response.text)

    def test_execute_python(self):
        exec_request = ExecRequest(code="print")
        my_obj = exec_request.json()
        response = requests.post(self.endpoint + f"/{BackendApi.EXECUTE_PYTHON}", timeout=2,json=my_obj)
        print(f"response: {response.content.decode()}")
        self.assertEqual(422, response.status_code)

    def test_invalid_url(self):
        response = requests.post(self.endpoint + f"/{BackendApi.INVALID_URL}", timeout=2)
        print(f"response: {response.content.decode()}")
        self.assertEqual(404, response.status_code)
