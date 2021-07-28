from typing import Iterable

from chaintools import Function as F
from chaintools import Argument


def test_spread():
    def return_args() -> Iterable[int]:
        return 1, 2

    def return_args_as_argument() -> Argument.TYPE:
        return (1, 2), None

    def add_two_variable(a, b) -> int:
        return a + b

    # F = None -> Iterable[int] -> [int, ...] -> int
    f = F >> return_args >> F.spread() >> add_two_variable
    g = F >> return_args_as_argument >> add_two_variable

    assert f() == g() == 3
