import asyncio


import pytest
from mcp import Tool
from mcp.server import FastMCP

from mcp_testcase import McpTestCase  # pylint: disable=E0401
from boto3_mcp_server import startup_checks, mcp_server


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()


@pytest.mark.usefixtures("event_loop_instance")
class TestServer(McpTestCase):

    def get_async_result(self, coro):
        """ Run a coroutine synchronously. """
        return self.event_loop.run_until_complete(coro) # noqa

    def test_startup_checks(self):
        self.assertTrue(startup_checks())

    def test_server_instance(self):
        self.assertIsNotNone(mcp_server)
        self.assertTrue(isinstance(mcp_server, FastMCP))
        #
        tools = self.get_async_result(mcp_server.list_tools())
        self.assertTrue(isinstance(tools, list))
        self.assertEqual(len(tools), 1)
        tool = tools[0]
        self.assertIsInstance(tool, Tool)
        self.assertEqual("aws-boto3-mcp-execute-code", tool.name)
