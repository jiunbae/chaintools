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
    ]

    def __init__(self, base: Annotation.TYPE):
        self.base = base
        self.__str_cache__ = self._param_str(self.base)

    def __repr__(self) \
            -> str:
        return self.__str_cache__
        
    def __str__(self) \
            -> str:
        return self.__str_cache__

    # TODO:
    #       is_subset, __eq__, __in__
    #       parameters, return_annotation, split?

    @classmethod
    def _param_str(cls, param) \
            -> str:
        if isinstance(param, typing._GenericAlias):
            generic = cls._param_str(param.__origin__)
            params = map(cls._param_str, param.__args__)
            return f'{generic}[{", ".join(params)}]'
        elif isinstance(param, typing._SpecialForm):
            return param._name
        elif isinstance(param, type):
            return param.__name__
        elif param is Ellipsis:
            return '...'
        elif isinstance(param, typing.Iterable):
            return f'{", ".join(map(cls._param_str, param))}'
        else:
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
