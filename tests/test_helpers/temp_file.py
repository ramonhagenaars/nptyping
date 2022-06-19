import contextlib
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent


@contextlib.contextmanager
def temp_file(python_code: str, file_name: str = "test_file.py"):
    file_content = dedent(python_code).strip() + os.linesep
    with TemporaryDirectory() as directory_name:
        path_to_file = Path(directory_name) / file_name
        with open(path_to_file, "w") as file:
            file.write(file_content)
        yield path_to_file
