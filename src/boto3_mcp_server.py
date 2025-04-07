import asyncio
import logging
import sys
import textwrap

from mcp.server.fastmcp import FastMCP

from tools import is_deno_installed, execute_code

# https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809
# https://github.com/alexei-led/aws-mcp-server

SERVER_NAME="aws-boto3-mcp"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler(sys.stderr)])
logger = logging.getLogger(SERVER_NAME)

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
    code ="""
    print("Hello world!")
    """
    is_error, log = asyncio.run(execute_code(code=textwrap.dedent(code), debug=False))
    if not is_error and "Hello world!" in log:
        logger.info("python code executor is up & running")
    else:
        msg = "Python code executor is not working properly. Please, fix installation"
        logger.error(msg)
        raise EnvironmentError(msg)
    #
    return True

server = FastMCP(SERVER_NAME)




@server.tool()
async def execute_boto3_code() -> str:
    return "foo"

if __name__ == "__main__":
    server.run()
