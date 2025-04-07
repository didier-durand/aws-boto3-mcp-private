import ast
import traceback


def is_code_valid(code: str) -> tuple[bool,str | None]:
    try:
        module = ast.parse(code)
    except SyntaxError:
        tb = traceback.format_exc()
        return False, tb
    if isinstance(module, ast.Module):
        return True,None
    return False,None

def is_deno_installed() -> bool:
    pass
