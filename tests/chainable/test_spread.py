from typing import Tuple

from chaintools import Function as F


def test_spread():
    def return_args() -> Tuple[int, int]:
        return 1, 2

    def add_two_variable(a, b) -> int:
        return a + b

    f = F >> return_args >> F.spread() >> add_two_variable
    assert f() == 3
