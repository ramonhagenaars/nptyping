import os
import sys
from contextlib import contextmanager
from glob import glob
from pathlib import Path
from unittest import TestCase
from zipfile import ZipFile

from nptyping.package_info import __version__

_PATH_TO_SETUP = str(Path(__file__).parent.parent / "setup.py")
_ROOT = Path(__file__).parent.parent.absolute()
_EXPECTED_FILES_IN_WHEEL = {
    "__init__.py",
    "assert_isinstance.py",
    "error.py",
    "ndarray.py",
    "ndarray.pyi",
    "nptyping_type.py",
    "package_info.py",
    "py.typed",
    "shape_expression.py",
    "shape_expression.pyi",
    "typing_.py",
    "typing_.pyi",
}


@contextmanager
def working_dir(path: Path):
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


class WheelTest(TestCase):
    def test_wheel_is_built_correctly(self):

        with working_dir(_ROOT):
            res = os.system(f"{sys.executable} setup.py bdist_wheel")
            self.assertEqual(0, res)
            wheel_files = glob(f"dist/*{__version__}*")
            self.assertEqual(1, len(wheel_files))

        with ZipFile(_ROOT / Path(wheel_files[0]), "r") as zip:
            files_in_wheel = set(
                f.filename[len("nptyping/") :]
                for f in zip.filelist
                if f.filename.startswith("nptyping/")
            )

        self.assertSetEqual(_EXPECTED_FILES_IN_WHEEL, files_in_wheel)
