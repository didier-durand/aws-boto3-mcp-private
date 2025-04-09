import pytest
import pytest_asyncio
from mcp import Tool
from mcp.server import FastMCP

from mcp_testcase import McpTestCase  # pylint: disable=E0401
from boto3_mcp_server import startup_checks, mcp_server


class TestServer(McpTestCase):

    def test_startup_checks(self):
        self.assertTrue(startup_checks())

    @pytest_asyncio.fixture
    async def get_mcp_server(self):
        return mcp_server

    @pytest.mark.asyncio
    async def test_server_instance(self):
        server = await self.get_mcp_server()
        self.assertIsNotNone(mcp_server)
        self.assertTrue(isinstance(server, FastMCP))
        #
        tools = await server.list_tools()
        self.assertTrue(isinstance(tools, list))
        self.assertEqual(len(tools), 1)
        tool = tools[0]
        self.assertIsInstance(tool, Tool)
        self.assertEqual("", tool.name)
