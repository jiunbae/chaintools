from __future__ import annotations
from typing import Optional, Callable, Tuple, Any, Dict


class Argument:
    """ Arguments are evaluated by the function
    """
    ARGS_TYPE = Tuple[Any, ...]
    KWARGS_TYPE = Dict[str, Any]
    RETURN_TYPE = Tuple[ARGS_TYPE, KWARGS_TYPE]
    TYPE = Tuple[Optional[ARGS_TYPE], Optional[KWARGS_TYPE]]

    def __init__(self, *args, **kwargs):
        self.args: Argument.ARGS_TYPE = args
        self.kwargs: Argument.KWARGS_TYPE = kwargs

    def __repr__(self):
        return f'{self.__class__.__name__}({self.args}, {self.kwargs})'

    @staticmethod
    def from_result(result: Any) \
            -> Argument:

        if not isinstance(result, tuple) or \
            (len(result) > 0 and not isinstance(result[-1], dict)):

            if isinstance(result, Argument):
                return result

            result = (result, None)

        args, kwargs = result

        if not isinstance(args, tuple):
            args = (args, )

        if kwargs is None:
            kwargs: Dict[str, Any] = dict()

        assert isinstance(args, tuple) and isinstance(kwargs, dict)

        arg = Argument(*args, **kwargs)
        return arg

    @property
    def value(self) \
            -> Any:
        if not self.kwargs and self.args:
            return self.args[0]

        elif not self.args and self.kwargs and len(self.kwargs.keys()) == 1:
            return self.kwargs.get(tuple(self.kwargs.keys())[0])

    @property
    def arg(self) \
            -> Argument.RETURN_TYPE:
        return self.args, self.kwargs

    def evaluate(self, function: Callable[[Argument.TYPE], Any]) \
            -> Argument:
        result = function(*self.args, **self.kwargs)
        return Argument.from_result(result)
