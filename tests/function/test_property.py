from inspect import signature
from typing import Tuple

import pytest

from chaintools import Function as F


class Test:
    @staticmethod
    def int_to_str(a: int) -> str:
        return str(a)
    
    @staticmethod
    def str_to_float(a: str) -> float:
        return float(a)

    @staticmethod
    def float_to_tuple(a: float) -> Tuple[int, int]:
        return (int(a), int(a))


def test_signature():
    f = F >> Test.int_to_str >> Test.str_to_float
    assert f.signature == (
        signature(Test.int_to_str),
        signature(Test.str_to_float),
    )

def test_stringify():
    f = F >> Test.int_to_str >> Test.str_to_float >> Test.float_to_tuple
    assert str(f) == "Function(int -> str -> float -> tuple[int, int])"

def test_stringify_param_return_not_match():
    f = F >> Test.int_to_str >> Test.int_to_str >> Test.float_to_tuple
    assert str(f) == "Function(int -> str(int) -> str(float) -> tuple[int, int])"
