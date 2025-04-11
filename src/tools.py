import ast
import json
import textwrap
import traceback
from typing import Tuple

from mcp import StdioServerParameters, stdio_client, ClientSession

from utils import exec_os_command


async def execute_code(code: str = "", debug: bool = False) -> type[bool, str]:
    code = textwrap.dedent(code)
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


def process_execution_log(log: str) -> Tuple[str, str, list[str]]:
    status: str = ""
    exec_result: str = ""
    dependencies: list[str] = list[str]()
    #
    tags = ["status", "dependencies", "error", "output", "return_value"]
    while log != "":
        tag = log.split(">")[0].split("<")[1] # noqa
        if tag not in tags:
            raise ValueError(f"Unknown tag {tag}")
        log_split: list[str] = log.split("</" + tag + ">")
        log = log_split[1]
        item = log_split[0].split("<" + tag + ">")[1]
        match tag:
            case "status":
                if item not in ["success", "run-error"]:
                    raise ValueError(f"{item} is not a known status")
                status = item
            case "dependencies":
                dependencies = json.loads(item)
            case "error":
                if exec_result != "":
                    raise ValueError(f"execution result already found for error: {exec_result}")
                if item is not None:
                    exec_result = item
            case "output":
                if exec_result != "":
                    raise ValueError(f"execution result already found for output: {exec_result}")
                if item is not None:
                    exec_result = item
            case "return_value":
                pass
            case _:
                raise ValueError(f"unknown log item: {item} - {log}")
    return status, exec_result, dependencies


def is_code_valid(code: str) -> tuple[bool, str | None]:
    try:
        module = ast.parse(code)
    except SyntaxError:
        tb = traceback.format_exc()
        return False, tb
    if isinstance(module, ast.Module):
        return True, None
    return False, None


def is_deno_installed(command="deno --version") -> Tuple[bool, str]:
    exception, rc, stdout, stderr = exec_os_command(command)
    if exception is not None or rc != 0 or stderr != "":
        return False, ""
    return True, stdout
