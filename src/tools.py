import ast
import traceback

from utils import exec_os_command


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
