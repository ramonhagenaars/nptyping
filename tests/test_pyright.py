from functools import partial
from subprocess import PIPE, run
from typing import Tuple
from unittest import TestCase

import pyright

from tests.test_helpers.temp_file import temp_file


def _check_pyright_on_code(python_code: str) -> Tuple[int, str, str]:
    pyright.node.subprocess.run = partial(run, stdout=PIPE, stderr=PIPE)
    try:
        with temp_file(python_code) as path_to_file:
            result = pyright.run(str(path_to_file))
        return (
            result.returncode,
            bytes.decode(result.stdout),
            bytes.decode(result.stderr),
        )
    finally:
        pyright.node.subprocess.run = run


class PyrightTest(TestCase):
    def test_pyright_accepts_array_with_shape(self):
        exit_code, stdout, sterr = _check_pyright_on_code(
            """
            from typing import Any
            from nptyping import NDArray, Shape


            NDArray[Shape["*, ..."], Any]
        """
        )
        self.assertEqual(0, exit_code, stdout)

    def test_pyright_accepts_array_with_structure(self):
        exit_code, stdout, sterr = _check_pyright_on_code(
            """
            from typing import Any
            from nptyping import NDArray, Structure


            NDArray[Any, Structure["x: Int, y: Float"]]
        """
        )
        self.assertEqual(0, exit_code, stdout)
