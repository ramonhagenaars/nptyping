from unittest import TestCase

import numpy

from nptyping import (
    Float,
    Int,
    Int8,
    Int16,
    Int32,
    Int64,
    Float16,
    Float32,
    Float64,
    UInt,
    UInt32,
    UInt8,
    UInt16,
    UInt64,
    Number,
)

_default_int_bytes = numpy.dtype(int).itemsize * 8
_default_float_bytes = numpy.dtype(float).itemsize * 8


class TestNumber(TestCase):

    def test_bits(self):
        self.assertEqual(8, Int8.bits())
        self.assertEqual(16, Int16.bits())
        self.assertEqual(32, Int32.bits())
        self.assertEqual(64, Int64.bits())

        self.assertEqual(16, Float16.bits())
        self.assertEqual(32, Float32.bits())
        self.assertEqual(64, Float64.bits())

    def test_raise_when_invalid_bits(self):
        with self.assertRaises(TypeError):
            Float[8]

        with self.assertRaises(TypeError):
            Int[128]

    def test_isinstance(self):
        self.assertIsInstance(42, Int)
        self.assertIsInstance(42, Int32)
        self.assertIsInstance(42.0, Float)
        self.assertIsInstance(42.0, Float32)
        self.assertIsInstance(42, Number)

        self.assertIsInstance(numpy.int64(42), Int[64])
        self.assertIsInstance(numpy.int64(42), Int64)
        self.assertNotIsInstance(numpy.int32(42), Int64)

        self.assertIsInstance(numpy.float64(42), Float[64])
        self.assertIsInstance(numpy.float64(42), Float64)
        self.assertNotIsInstance(numpy.float32(42), Float64)
        self.assertNotIsInstance(numpy.int64(42), Float64)

        self.assertIsInstance(numpy.float64(42), Number)
        self.assertIsInstance(numpy.int8(42), Number)
        self.assertNotIsInstance('I am not a number, I am a free man!', Number)

    def test_issubclass(self):
        self.assertTrue(issubclass(Float[32], Float32))
        self.assertTrue(issubclass(Int64, Int[64]))
        self.assertTrue(issubclass(Float16, Float))
        self.assertTrue(issubclass(Int64, Int))
        self.assertTrue(issubclass(Int64, Number))
        self.assertTrue(not issubclass(Int64, Float))
        self.assertTrue(not issubclass(Float32, Float64))

        self.assertTrue(issubclass(numpy.float64, Number))
        self.assertTrue(issubclass(numpy.int32, Number))
        self.assertTrue(issubclass(numpy.int32, Int32))
        self.assertTrue(not issubclass(numpy.int32, Int64))
        self.assertTrue(not issubclass(numpy.float32, Int32))

        self.assertTrue(issubclass(int, Number))
        self.assertTrue(issubclass(float, Number))
        self.assertTrue(issubclass(int, Int[_default_int_bytes]))
        self.assertTrue(issubclass(float, Float[_default_float_bytes]))

    def test_int_of(self):
        self.assertEqual(Int[_default_int_bytes], Int.type_of(1))
        self.assertEqual(Int[_default_int_bytes], Int.type_of(1_000_000_000))
        self.assertEqual(Int[_default_int_bytes], Int.type_of(-1_000_000_000))

        self.assertEqual(Int8, Int.type_of(numpy.int8))
        self.assertEqual(Int16, Int.type_of(numpy.int16))
        self.assertEqual(Int32, Int.type_of(numpy.int32))
        self.assertEqual(Int64, Int.type_of(numpy.int64))

    def test_uint_of(self):
        self.assertEqual(UInt[_default_int_bytes], UInt.type_of(1))
        self.assertEqual(UInt[_default_int_bytes], UInt.type_of(1_000_000_000))
        self.assertEqual(UInt[_default_int_bytes], UInt.type_of(1_000_000_000))

        self.assertEqual(UInt8, UInt.type_of(numpy.uint8))
        self.assertEqual(UInt16, UInt.type_of(numpy.uint16))
        self.assertEqual(UInt32, UInt.type_of(numpy.uint32))
        self.assertEqual(UInt64, UInt.type_of(numpy.uint64))

    def test_float_of(self):
        default_bytes = numpy.dtype(float).itemsize * 8
        self.assertEqual(Float[default_bytes], Float.type_of(1.0))
        self.assertEqual(Float[default_bytes], Float.type_of(1_000_000_000.0))
        self.assertEqual(Float[default_bytes], Float.type_of(-1_000_000_000.0))

    def test_int_fitting(self):
        self.assertEqual(Int8, Int.fitting(0))
        self.assertEqual(Int8, Int.fitting(2 ** 7 - 1))
        self.assertEqual(Int8, Int.fitting(-(2 ** 7 - 1)))

        self.assertEqual(Int16, Int.fitting(2 ** 7))
        self.assertEqual(Int16, Int.fitting(2 ** 15 - 1))
        self.assertEqual(Int16, Int.fitting(-(2 ** 7)))
        self.assertEqual(Int16, Int.fitting(-(2 ** 15 - 1)))

        self.assertEqual(Int32, Int.fitting(2 ** 15))
        self.assertEqual(Int32, Int.fitting(2 ** 31 - 1))
        self.assertEqual(Int32, Int.fitting(-(2 ** 15)))
        self.assertEqual(Int32, Int.fitting(-(2 ** 31 - 1)))

        self.assertEqual(Int64, Int.fitting(2 ** 31))
        self.assertEqual(Int64, Int.fitting(2 ** 63 - 1))
        self.assertEqual(Int64, Int.fitting(-(2 ** 31)))
        self.assertEqual(Int64, Int.fitting(-(2 ** 63 - 1)))

    def test_uint_fitting(self):
        self.assertEqual(UInt8, UInt.fitting(0))
        self.assertEqual(UInt8, UInt.fitting(2 ** 8 - 1))
        self.assertEqual(UInt8, UInt.fitting(-(2 ** 8 - 1)))

        self.assertEqual(UInt16, UInt.fitting(2 ** 8))
        self.assertEqual(UInt16, UInt.fitting(2 ** 16 - 1))
        self.assertEqual(UInt16, UInt.fitting(-(2 ** 8)))
        self.assertEqual(UInt16, UInt.fitting(-(2 ** 16 - 1)))

        self.assertEqual(UInt32, UInt.fitting(2 ** 16))
        self.assertEqual(UInt32, UInt.fitting(2 ** 32 - 1))
        self.assertEqual(UInt32, UInt.fitting(-(2 ** 16)))
        self.assertEqual(UInt32, UInt.fitting(-(2 ** 32 - 1)))

        self.assertEqual(UInt64, UInt.fitting(2 ** 32))
        self.assertEqual(UInt64, UInt.fitting(2 ** 64 - 1))
        self.assertEqual(UInt64, UInt.fitting(-(2 ** 32)))
        self.assertEqual(UInt64, UInt.fitting(-(2 ** 64 - 1)))
