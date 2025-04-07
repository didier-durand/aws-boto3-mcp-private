import ast
import traceback

from mcp import StdioServerParameters, stdio_client, ClientSession

from utils import exec_os_command

async def execute_code(code: str = "", debug: bool = False) -> type[bool,str]:
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
    #
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            if debug:
                print(f"tools len: {len(tools.tools)}")
                assert 1 == len(tools.tools)
                print(f"tool name: {repr(tools.tools[0].name)}")
                assert tools.tools[0].name == 'run_python_code'
                print(repr(tools.tools[0].inputSchema))
            result = await session.call_tool('run_python_code', {'python_code': code})
            if debug:
                print(result.content[0].text)
            return result.isError, result.content[0].text

def is_code_valid(code: str) -> tuple[bool,str | None]:
    try:
        module = ast.parse(code)
    except SyntaxError:
        tb = traceback.format_exc()
        return False, tb
    if isinstance(module, ast.Module):
        return True,None
    return False,None

def is_deno_installed(command="deno --version") -> bool:
    exception, rc, stdout, stderr = exec_os_command(command)
    if exception is not None or rc != 0 or stderr != "":
        return False
    print(stdout)
    return True
