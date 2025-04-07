import subprocess


def exec_os_command(command: list[str] | str = None) -> tuple[Exception | None, int | None, str | None, str | None]:
    if isinstance(command, str):
        command = command.split(" ")
    print("executing:", " ".join(command))
    try:
        process: subprocess.CompletedProcess = subprocess.run(command,
                                                              capture_output=True,
                                                              text=True, check=False)
    except Exception as exception:  # noqa pylint: disable=W0718
        return exception, None, None, None
    return None, process.returncode, process.stdout, process.stderr
