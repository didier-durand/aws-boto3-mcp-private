import asyncio
import logging
import sys
import textwrap
from typing import TypedDict

from mcp.server.fastmcp import FastMCP

from tools import is_deno_installed, execute_code, process_execution_log

# https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809
# https://github.com/alexei-led/aws-mcp-server

MCP_SERVER_NAME = "aws-boto3-mcp"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler(sys.stderr)])
logger = logging.getLogger(MCP_SERVER_NAME)


# run checks before start
def startup_checks() -> bool:
    """Run pre-start checks"""
    logger.info("running pre-start checks...")
    if is_deno_installed():
        logger.info("deno is installed")
    else:
        msg = "deno is not installed for Python code execution. Please install it."
        logger.error(msg)
        raise EnvironmentError(msg)
    #
    code = """
    print("Hello world!")
    """
    is_error, log = asyncio.run(execute_code(code=textwrap.dedent(code), debug=False))
    if not is_error:
        status, exec_result, dependencies = process_execution_log(log=log)
        if status == "success" and exec_result == "\nHello world!\n" and dependencies == []:
            logger.info("python code executor is up & running")
        else:
            msg = f"initial execution log is incorrect: {log}"
            logger.error(msg)
            raise EnvironmentError(msg)
    else:
        msg = "Python code executor is not working properly. Please, fix installation"
        logger.error(msg)
        raise EnvironmentError(msg)
    #
    return True


mcp_server = FastMCP(MCP_SERVER_NAME)


class CommandResult(TypedDict):
    """Type definition for command execution results."""
    status: str
    output: str


@mcp_server.tool(name=MCP_SERVER_NAME + "-execute-code",
                 description="MCP tool to execute Python code using Boto3 supplied by AWS SDK")
async def execute_boto3_code() -> CommandResult:
    return CommandResult(status="success", output="stdout_str")


if __name__ == "__main__":
    mcp_server.run()
