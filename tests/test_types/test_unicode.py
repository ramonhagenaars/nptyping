from unittest import TestCase

from nptyping import Unicode


class TestUnicode(TestCase):

    def test_isinstance(self):
        self.assertIsInstance('Sure', Unicode)
        self.assertIsInstance('', Unicode)
        self.assertIsInstance('Yes', Unicode[3])
        self.assertIsInstance('Yes', Unicode[4])
        self.assertNotIsInstance('No', Unicode[1])
        self.assertNotIsInstance(42, Unicode)
        self.assertNotIsInstance(42, Unicode[42])

    def test_repr(self):
        self.assertEqual('Unicode', repr(Unicode))
        self.assertEqual('Unicode[50]', repr(Unicode[50]))

    def test_type_of(self):
        self.assertEqual(Unicode[4], Unicode.type_of('test'))
