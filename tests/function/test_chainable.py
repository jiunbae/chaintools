from typing import Callable

import pytest

from chaintools import Function as F


class Test:
    @staticmethod
    def add(tar: int) \
            -> Callable[[int], int]:
        def _wrapper(src: int) \
                -> int:
            return src + tar
        return _wrapper

    @staticmethod
    def to_str(a):
        return str(a)

    @staticmethod
    def to_int(b):
        return int(b)

    @staticmethod
    def to_float(c):
        return float(c)


def test_chainable():
    f = F >> Test.add(1) >> Test.add(2)
    assert f(42) == 45


def test_chainable_chain():
    f = F >> Test.to_str
    g = F >> f >> Test.to_int
    h = F >> g >> Test.to_float

    target = 42
    assert str(target) == f(target)
    assert int(target) == g(target)
    assert float(target) == h(target)
