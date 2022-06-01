from typing import Any, Tuple
from unittest import TestCase

from nptyping.base_meta_classes import (
    ComparableByArgsMeta,
    ContainerMeta,
    FinalMeta,
    ImmutableMeta,
    InconstructableMeta,
    MaybeCheckableMeta,
    SubscriptableMeta,
)
from nptyping.error import NPTypingError


class SubscriptableMetaTest(TestCase):
    def test_subscriptable_meta(self):
        class CMeta(SubscriptableMeta):
            def _get_item(cls, item: Any) -> Tuple[Any, ...]:
                return (item,)

        class C(metaclass=CMeta):
            __args__ = tuple()

        C42 = C[42]

        self.assertEqual((42,), C42.__args__)
        self.assertIs(C[42], C42)

    def test_final_meta(self):
        class CMeta(FinalMeta, implementation="C"):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:

            class C2(C):
                ...

        self.assertEqual("Cannot subclass nptyping.C.", str(err.exception))

    def test_inconstructable(self):
        class CMeta(InconstructableMeta):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C()

        self.assertIn("Cannot instantiate nptyping.C.", str(err.exception))

    def test_immutable(self):
        class CMeta(ImmutableMeta):
            ...

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C.some_attr = 42

        self.assertEqual("Cannot set values to nptyping.C.", str(err.exception))

    def test_subscriptable_cannot_parameterize_twice(self):
        class CMeta(SubscriptableMeta):
            def __str__(self) -> str:
                return "SomeName"

        class C(metaclass=CMeta):
            __args__ = tuple()

        with self.assertRaises(NPTypingError) as err:
            C[42][42]

        self.assertEqual(
            f"Type nptyping.SomeName is already parameterized.", str(err.exception)
        )

    def test_comparable_by_args_meta(self):
        class C1(metaclass=ComparableByArgsMeta):
            __args__ = (42, 42)

        class C2(metaclass=ComparableByArgsMeta):
            __args__ = (42, 42)

        class C3(metaclass=ComparableByArgsMeta):
            __args__ = (42, 42, 42)

        self.assertEqual(C1, C2)
        self.assertEqual(hash(C1), hash(C2))
        self.assertNotEqual(C1, C3)
        self.assertNotEqual(hash(C1), hash(C3))

    def test_maybe_checkable_instance_checking_is_disabled_by_default(self):
        class CMeta(MaybeCheckableMeta):
            ...

        class C(metaclass=CMeta):
            ...

        with self.assertRaises(NPTypingError) as err:
            isinstance(42, C)

        self.assertEqual(
            "Instance checking is not supported for nptyping.C.", str(err.exception)
        )

    def test_maybe_checkable_subclass_checking_is_disabled_by_default(self):
        class CMeta(MaybeCheckableMeta):
            ...

        class C(metaclass=CMeta):
            ...

        with self.assertRaises(NPTypingError) as err:
            issubclass(int, C)

        self.assertEqual(
            "Subclass checking is not supported for nptyping.C.", str(err.exception)
        )

    def test_container_meta(self):
        class TestContainerMeta(ContainerMeta, implementation="TestContainer"):
            def _normalize_expression(cls, item: str) -> str:
                return item.lower()

            def _validate_expression(cls, item: str) -> None:
                if item == "forbidden":
                    raise NPTypingError("That item is forbidden.")

        class TestContainer(metaclass=TestContainerMeta):
            __args__ = (42,)

        self.assertEqual((42,), TestContainer.__args__)
        self.assertEqual(("test",), TestContainer["test"].__args__)
        self.assertIs(TestContainer["test"], TestContainer["test"])
        self.assertIs(TestContainer["test"], TestContainer["TeSt"])

        with self.assertRaises(NPTypingError):
            TestContainer["forbidden"]

        self.assertFalse(issubclass(int, TestContainer))
