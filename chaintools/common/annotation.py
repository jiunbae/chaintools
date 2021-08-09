from __future__ import annotations
import typing
import inspect


class Annotation:
    """ Annotation is type expression wrapper

    Support to check whether types are equivalent or containment.
    """
    TYPE = typing.Union[
        typing._GenericAlias,
        typing._SpecialForm,
        typing.Any,
        type,
        str,
    ]

    def __init__(self, base: Annotation.TYPE):
        self.base = base

    def __repr__(self) \
            -> str:
        return f'{self.__class__.__name__}({self.base!r})'

    def __str__(self) \
            -> str:
        return self.to_str(self.base)

    def __eq__(self, other: Annotation.TYPE) -> bool:
        if isinstance(other, Annotation):
            return self.base == other.base
        return self.base == other

    def __contains__(self, other: Annotation.TYPE) -> bool:
        if isinstance(other, Annotation):
            return self.base == other.base
        return self.base == other

    @classmethod
    def to_str(cls, param) \
            -> str:
        """ Convert annotation to string representation.
        """
        if isinstance(param, str):
            return f"{param!s}"
        if isinstance(param, typing._GenericAlias):
            generic = cls.to_str(param.__origin__)
            params = map(cls.to_str, param.__args__)
            return f'{generic}[{", ".join(params)}]'
        if isinstance(param, typing._SpecialForm):
            return param._name
        if param is inspect._empty:
            return 'Any'
        if param is Ellipsis:
            return '...'
        if isinstance(param, type):
            return param.__name__
        if isinstance(param, typing.Iterable):
            return f'{", ".join(map(cls.to_str, param))}'
        return f"{param!s}"

    @staticmethod
    def from_function(function: typing.Callable) \
            -> typing.Tuple[typing.Iterable[Annotation], Annotation]:
        """ function annotation

            :return: (parameters, return_annotation)
        """
        sign = inspect.signature(function)
        return (
            Annotation([param.annotation for param in sign.parameters.values()]),
            Annotation(sign.return_annotation),
        )
