from typing import Callable

import pytest

from chaintools import Function as F


def test_chain_map():
    def to_float(a):
        return float(a)
        
    def to_str(a):
        return str(a)

    f = F >> to_float >> to_str
    result = f.map(range(10))
    assert tuple(result) == tuple(map(to_str, map(to_float, range(10))))


def test_chain_filter():
    def is_even(a):
        return a % 2 == 0
    
    def is_not_zero(a):
        return a != 0

    f = F >> is_even >> is_not_zero
    result = f.filter(range(10))
    assert tuple(result) == tuple(filter(is_not_zero, filter(is_even, range(10))))


def test_chain():
    def add(tar: int) \
            -> Callable[[int], int]:
        def _wrapper(src: int) \
                -> int:
            return src + tar
        return _wrapper

    def to_float(a):
        return float(a)

    def is_even(a):
        return a % 2 == 0

    # f = F((add(1), to_float)).map
    f = F >> F([add(1), to_float]).map >> F(is_even).filter >> F(add(1)).map
    result = f(range(10))
    assert tuple(result) == (3.0, 5.0, 7.0, 9.0, 11.0)
