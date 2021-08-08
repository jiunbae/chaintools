from typing import Callable, Tuple, Iterable
from inspect import signature

import pytest

from chaintools import Function as F
from chaintools import Argument


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

    @staticmethod
    def int_to_str(a: int) -> str:
        return str(a)
    
    @staticmethod
    def str_to_float(a: str) -> float:
        return float(a)

    @staticmethod
    def two_int_to_float(a: int, b: int) -> float:
        return float(a + b)

    @staticmethod
    def float_to_tuple(a: float) -> Tuple[int, int]:
        return (int(a), int(a))

    @staticmethod
    def return_args() -> Iterable[int]:
        return 1, 2

    @staticmethod
    def return_args_as_argument() -> Argument.TYPE:
        return (1, 2), None

    @staticmethod
    def add_two_variable(a, b) -> int:
        return a + b


def test_chainable():
    f = F >> Test.add(1) >> Test.add(2)
    assert f(42) == 45


def test_chaining():
    f = F >> Test.to_str
    g = F >> f >> Test.to_int
    h = F >> g >> Test.to_float

    target = 42
    assert str(target) == f(target)
    assert int(target) == g(target)
    assert float(target) == h(target)


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


def test_chain_map_filter_nested():
    f = F >> (F >> Test.add(1) >> Test.to_float).map >> F(Test.is_even).filter >> (F >> Test.add(1)).map
    result = f(range(10))
    assert tuple(result) == (3.0, 5.0, 7.0, 9.0, 11.0)


def test_signature():
    f = F >> Test.int_to_str >> Test.str_to_float
    assert tuple(f.signature) == (
        signature(Test.int_to_str),
        signature(Test.str_to_float),
    )


def test_stringify():
    f = F >> Test.int_to_str >> Test.str_to_float >> Test.float_to_tuple
    assert str(f) == "Function(int -> str -> float -> tuple[int, int])"


def test_stringify_param_return_not_match():
    f = F >> Test.int_to_str >> Test.two_int_to_float >> Test.float_to_tuple
    assert str(f) == "Function(int -> str(int, int) -> float -> tuple[int, int])"


def test_spread():
    f = F >> Test.return_args >> F.spread() >> Test.add_two_variable
    g = F >> Test.return_args_as_argument >> Test.add_two_variable
    assert f() == g() == 3
