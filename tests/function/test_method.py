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

    @staticmethod
    def is_even(a):
        return a % 2 == 0

    @staticmethod
    def is_not_zero(a):
        return a != 0

def test_chain_map():
    f = F >> Test.to_float >> Test.to_str
    result = f.map(range(10))
    assert tuple(result) == tuple(map(Test.to_str, map(Test.to_float, range(10))))


def test_chain_filter():
    f = F >> Test.is_even >> Test.is_not_zero
    result = f.filter(range(10))
    assert tuple(result) == tuple(filter(Test.is_not_zero, filter(Test.is_even, range(10))))


def test_chain_map_filter():
    f = F >> F([Test.add(1), Test.to_float]).map >> F(Test.is_even).filter >> F(Test.add(1)).map
    result = f(range(10))
    assert tuple(result) == (3.0, 5.0, 7.0, 9.0, 11.0)
