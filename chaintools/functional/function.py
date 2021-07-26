from __future__ import annotations
from typing import Optional, Union, Callable, Iterable, Any, List

from chaintools.core import Chainable
from chaintools.core import Argument


class Function(metaclass=Chainable):
    """ Chainable Function
    """
    TYPE = Callable[[Argument.TYPE], Any]

    def __init__(self, function: Optional[Union[Callable, Iterable[Callable]]] = None):
        self.__funcs__: List[Function.TYPE] = []
        if function is None:
            pass
        elif callable(function):
            self.__funcs__.append(function)
        elif isinstance(function, Iterable):
            self.__funcs__.extend(function)
        else:
            raise TypeError(f'{function} is not a callable or list of callables')

    def __call__(self, *args, **kwargs) \
            -> Any:
        args = Argument(*args, **kwargs)
        for function in self.__funcs__:
            args = args.evaluate(function)

        return args.value

    def __rshift__(self, function: Function.TYPE):
        self.__funcs__.append(function)
        return self

    def __lshift__(self, item: Any) \
            -> Any:
        result = self.__call__(item)
        return result

    @staticmethod
    def identity(arg, *args) \
            -> Any:
        """ Identity Function
        """
        return (arg, ) + args if args else arg

    @staticmethod
    def spread():
        """ Spread Function
        """
        def _wrapper(*args: Optional[Argument.ARGS_TYPE]) \
                -> Argument:
            return Argument(*args)
        return _wrapper
