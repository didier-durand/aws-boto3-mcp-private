import unittest
import requests

from boto3_mcp_server import MCP_HOST, MCP_PORT, MCP_HELLO_WORLD


class TestBoto3McpServer(unittest.TestCase):

    def setUp(self):
        self.endpoint=f"http://{MCP_HOST}:{MCP_PORT}"

    def test_hello_world(self):
        response = requests.get(self.endpoint)
        print(response.content.decode())
        self.assertEqual(200,response.status_code)
        self.assertEqual(MCP_HELLO_WORLD,response.text)
        response = requests.get(self.endpoint + "/resp1")
        self.assertEqual(200, response.status_code)
        self.assertEqual("response1", response.text)

