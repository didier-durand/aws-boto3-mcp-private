from mcp.server import FastMCP

from mcp_testcase import McpTestCase  # pylint: disable=E0401
from boto3_mcp_server import startup_checks, mcp_server


class TestServer(McpTestCase):

    def test_startup_checks(self):
        self.assertTrue(startup_checks())

    async def test_server_instance(self):
        self.assertIsNotNone(mcp_server)
        self.assertTrue(isinstance(mcp_server, FastMCP))
        #
        tools = await mcp_server.list_tools()
        self.assertTrue(isinstance(tools, list))
        self.assertEqual(len(tools), 1)
