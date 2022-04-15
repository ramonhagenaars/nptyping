from unittest import TestCase

from nptyping import assert_isinstance


class AssertInstanceTest(TestCase):
    def test_assert_isinstance_true(self):
        assert_isinstance(1, int)

    def test_assert_isinstance_false(self):
        with self.assertRaises(AssertionError) as err:
            assert_isinstance(1, str)
        self.assertIn("instance=1, cls=<class 'str'>", str(err.exception))

    def test_assert_isinstance_false_with_message(self):
        with self.assertRaises(AssertionError) as err:
            assert_isinstance(1, str, "That's no string")
        self.assertIn("That's no string", str(err.exception))
