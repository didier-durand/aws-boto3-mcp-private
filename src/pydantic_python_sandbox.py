import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CODE = """
import numpy
a = numpy.array([1, 2, 3])
print(a)
a
"""
server_params = StdioServerParameters(
    command='deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio',
    ],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(len(tools.tools))
            assert 1 == len(tools.tools)
            print(repr(tools.tools[0].name))
            assert repr(tools.tools[0].name) == 'run_python_code'
            print(repr(tools.tools[0].inputSchema))
            result = await session.call_tool('run_python_code', {'python_code': CODE})
            print(result.content[0].text)

if __name__ == '__main__':
    asyncio.run(main())
