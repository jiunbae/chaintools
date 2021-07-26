from typing import Callable

import pytest

from chaintools import Function as F



def test_chainable_basic():
    def add(tar: int) \
            -> Callable[[int], int]:
        def _wrapper(src: int) \
                -> int:
            return src + tar
        return _wrapper


    f = F >> add(1) >> add(2)
    assert f(3) == 6


def test_chainable_chain():
    def to_str(a):
        return str(a)

    def to_int(b):
        return int(b)

    def to_float(c):
        return float(c)

    f = F >> to_str
    g = F >> f >> to_int
    h = F >> g >> to_float

    target = 3

    assert str(target) == f(target)
    assert int(target) == g(target)
    assert float(target) == h(target)
