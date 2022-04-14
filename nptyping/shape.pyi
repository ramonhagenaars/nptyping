# type: ignore
# Let MyPy ignore this file to avoid complaints on the import of Literal under
# different Python versions.
try:
    from typing import Literal as Shape
except ImportError:
    from typing_extensions import Literal as Shape
