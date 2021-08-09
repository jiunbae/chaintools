from __future__ import annotations
import typing
import inspect
import collections

from . import (
    Annotation,
    Argument,
)

from ..type import (
    Chainable,
)


class Function(metaclass=Chainable):
    """ Chainable Function
    """
    TYPE = typing.Callable[[Argument.TYPE], typing.Any]
    INPUT_TYPE = typing.Union[typing.Callable, typing.Iterable[typing.Callable]]

    def __init__(self, function: Function.INPUT_TYPE = None):
        self.__funcs__: typing.List[Function.TYPE] = []
        if function is None:
            pass
        elif callable(function):
            self.__funcs__.append(function)
        elif isinstance(function, collections.abc.Iterable):
            self.__funcs__.extend(function)
        else:
            raise TypeError(f'{function} is not a callable or list of callables')

    def __str__(self) \
            -> str:
        types: typing.List[str] = []
        for param_annotation, return_annotation in self.annotations:
            if len(types) > 0:
                if types[-1] != str(param_annotation):
                    types[-1] = f'{types[-1]}({param_annotation!s})'
            else:
                types.append(str(param_annotation))

            types.append(str(return_annotation))

        return f'{self.__class__.__name__}({" -> ".join(types)})'

    def __call__(self, *args, **kwargs) \
            -> typing.Any:
        args = Argument(*args, **kwargs)
        for function in self.__funcs__:
            args = args.evaluate(function)

        return args.value

    def __rshift__(self, function: Function.TYPE):
        self.__funcs__.append(function)
        return self

    def __lshift__(self, item: typing.Any) \
            -> typing.Any:
        result = self.__call__(item)
        return result

    @property
    def signature(self) \
            -> typing.Iterable[inspect.Signature]:
        """ return signature of functions
        """
        return map(inspect.signature, self.__funcs__)

    @property
    def annotations(self) \
            -> typing.Iterable[typing.Tuple[typing.Iterable[Annotation], Annotation]]:
        """ return annotations of functions
        """
        return map(Annotation.from_function, self.__funcs__)

    def map(self, items: typing.Iterable[typing.Any]) \
            -> typing.Generator[typing.Any, None, None]:
        """ map function to items
        """
        for function in self.__funcs__:
            items = map(function, items)

        return items

    def filter(self, items: typing.Iterable[typing.Any]) \
            -> typing.Generator[typing.Any, None, None]:
        """ filter function to items
        """
        for function in self.__funcs__:
            items = filter(function, items)

        return items

    @staticmethod
    def spread():
        """ Spread Function
        """
        def _wrapper(args: typing.Optional[Argument.ARGS_TYPE]) \
                -> Argument:
            return Argument(*args)

        return _wrapper
