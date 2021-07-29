from inspect import signature

import pytest

from chaintools import Function as F


def test_signature():
    def int_to_str(a: int) -> str:
        return str(a)

    def str_to_float(a: str) -> float:
        return float(a)
    
    f = F >> int_to_str >> str_to_float
    assert f.signature == (
        signature(int_to_str),
        signature(str_to_float),
    )
