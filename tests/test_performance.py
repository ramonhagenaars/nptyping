from timeit import Timer
from unittest import TestCase

import numpy as np

from nptyping import (
    Float,
    NDArray,
    Shape,
)


class PerformanceTest(TestCase):
    def test_instance_check_performance(self):

        arr = np.random.randn(42, 42, 3, 5)

        def _check_inst():
            isinstance(arr, NDArray[Shape["A, *, [a, b, c], 5"], Float])

        first_time_sec = Timer(_check_inst).timeit(number=1)
        second_time_sec = Timer(_check_inst).timeit(number=1)

        self.assertLess(first_time_sec, 0.02)
        self.assertLess(second_time_sec, first_time_sec)
        self.assertLess(second_time_sec, 0.0004)
