from typing import Any, Tuple
from unittest import TestCase

from nptyping.error import NPTypingError
from nptyping.subscriptable_meta import SubscriptableMeta


class SubscriptableMetaTest(TestCase):
    def test_happy_flow(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            def _get_item(cls, item: Any) -> Tuple[Any, ...]:
                return (item,)

        class C(metaclass=CMeta):
            __args__ = tuple()

        C42 = C[42]

        self.assertEqual((42,), C42.__args__)
        self.assertIs(C[42], C42)

    def test_cannot_subclass(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:

            class C2(C):
                ...

        self.assertEqual("Cannot subclass nptyping.C.", str(err.exception))

    def test_cannot_instantiate(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C()

        self.assertIn("Cannot instantiate nptyping.C.", str(err.exception))

    def test_cannot_set_attributes(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C.some_attr = 42

        self.assertEqual("Cannot set values to nptyping.C.", str(err.exception))

    def test_cannot_parameterize_twice(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            def __str__(self) -> str:
                return "SomeName"

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C[42][42]

        self.assertEqual(
            f"Type nptyping.SomeName is already parameterized.", str(err.exception)
        )

    def test_instance_checking_is_disabled_by_default(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            ...

        class C(metaclass=CMeta):
            ...

        with self.assertRaises(NPTypingError) as err:
            isinstance(42, C)

        self.assertEqual(
            "Instance checking is not supported for nptyping.C.", str(err.exception)
        )

    def test_subclass_checking_is_disabled_by_default(self):
        class CMeta(SubscriptableMeta, cls_name="C"):
            ...

        class C(metaclass=CMeta):
            ...

        with self.assertRaises(NPTypingError) as err:
            issubclass(42, C)

        self.assertEqual(
            "Subclass checking is not supported for nptyping.C.", str(err.exception)
        )
