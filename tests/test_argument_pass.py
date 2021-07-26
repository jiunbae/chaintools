from typing import Tuple, Any, Dict


from chaintools import Function as F
from chaintools import Argument


def test_function_argument():
    def return_args_and_kwargs() -> Tuple[Tuple, Dict[str, Any]]:
        return (1, 2), {'c': 1, 'd': 2}

    def add_four_variable(a, b, c, d) -> int:
        return a + b + c + d

    f = F >> return_args_and_kwargs >> add_four_variable
    assert f() == 6


def test_function_argument_wrapping():
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
        test_return_argument_class(),
        test_resizable_arguments(),
    ])
