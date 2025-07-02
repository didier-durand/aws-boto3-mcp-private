import subprocess
import xml.etree.ElementTree as elementTree
from datetime import datetime


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def exec_os_command(command: list[str] | str = None, check: bool = False, debug: bool = False) -> tuple[Exception | None, int | None, str | None, str | None]:
    if isinstance(command, str):
        command = command.split(" ")
    if debug:
        print("\nexec_os_command:", " ".join(command))
    try:
        process: subprocess.CompletedProcess = subprocess.run(command,
                                                              stdout=subprocess.PIPE,
                                                              stderr=subprocess.PIPE,
                                                              text=True,
                                                              check=check)
    except Exception as exception:  # noqa pylint: disable=W0718
        return exception, None, None, None
    return None, process.returncode, process.stdout, process.stderr


def is_xml(value):
    try:
        elementTree.fromstring(value)
    except elementTree.ParseError:
        return False
    return True
