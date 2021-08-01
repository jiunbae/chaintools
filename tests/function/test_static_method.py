from typing import Iterable

import pytest

from chaintools import Function as F
from chaintools import Argument


class Test:
    @staticmethod
    def return_args() -> Iterable[int]:
        return 1, 2

    @staticmethod
    def return_args_as_argument() -> Argument.TYPE:
        return (1, 2), None

    @staticmethod
    def add_two_variable(a, b) -> int:
        return a + b


def test_spread():
    f = F >> Test.return_args >> F.spread() >> Test.add_two_variable
    g = F >> Test.return_args_as_argument >> Test.add_two_variable
    assert f() == g() == 3
