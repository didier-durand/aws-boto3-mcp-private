import unittest
from multiprocessing import Process
from time import sleep

import requests
import uvicorn

import boto3_fastapi_server
from boto3_fastapi_server import MCP_HOST, MCP_PORT, fastapi_server
from boto3_mcp_server import MCP_SERVER_NAME

class TestBoto3McpServer(unittest.IsolatedAsyncioTestCase):

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
                self.proc = Process(target=uvicorn.run,
                                    kwargs={
                                        "app": f"{boto3_fastapi_server=}".split('=',maxsplit=1)[0]
                                               + ":" + f"{fastapi_server=}".split('=',maxsplit=1)[0],
                                        "host": MCP_HOST,
                                        "port": MCP_PORT,
                                        "log_level": "info"},
                                    daemon=True
                                    )
                self.proc.start()
                while not self.proc.is_alive():
                    sleep(0.2)
            if response is not None:
                if response.status_code == 200 and response.text == MCP_SERVER_NAME:
                    break
            sleep(1)

    def tearDown(self):
        self.proc.terminate()
        print(f"\n### ending {unittest.TestCase.id(self)}")

    def test_get_root_url(self):
        response = requests.get(self.endpoint,timeout=2)
        print(f"response: {response.content.decode()}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(MCP_SERVER_NAME, response.text)
