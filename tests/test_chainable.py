from typing import Tuple, Dict, Any

import pytest

from chaintools import Function as F
from chaintools import Argument


def test_chainable_basic():
    def add(a, b):
        return a + b

    def sub(a, b):
        return a - b

    def mul(a, b):
        return a * b

    def div(a, b):
        return a / b

    f = F >> add

    assert 5 == f(3, 2)


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


def test_function_argument_wrapping():

    def test_function_argument():
        def function1() -> Tuple[Tuple, Dict[str, Any]]:
            return (1, 2), {'c': 1, 'd': 2}

        def function2(a, b, c=0, d=0) -> int:
            return a + b + c + d

        f = F >> function1 >> function2
        return f() == 6

    def test_return_argument_class():
        def function_return_argument_class():
            return Argument(1, 2, 3, d=4)
        
        def function_return_classic():
            return ((1, 2, 3), {'d': 4})
        
        def function_accept_argument_class(a, b, c, d=None):
            return a + b + c + d
        
        f = F >> function_return_argument_class >> function_accept_argument_class
        g = F >> function_return_classic >> function_accept_argument_class
        return f() == g() == 10

    def test_resizable_arguments():
        def argument_resize(target_size: int = 0):
            def _wrapper(*args):
                return args[:target_size]
            return _wrapper

        f = F >> argument_resize(3) >> argument_resize(2) >> argument_resize(1)
        return f(1, 2, 3, 4) == 1

    assert([
        test_function_argument(),
        test_return_argument_class(),
        test_resizable_arguments(),
    ])
