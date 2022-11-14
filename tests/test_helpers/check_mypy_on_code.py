from typing import Tuple

from mypy import api

from tests.test_helpers.temp_file import temp_file


def check_mypy_on_code(python_code: str) -> Tuple[int, str, str]:
    with temp_file(python_code) as path_to_file:
        stdout, stderr, exit_code = api.run([str(path_to_file)])
    return exit_code, stdout, stderr
