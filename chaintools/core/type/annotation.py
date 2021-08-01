from __future__ import annotations
import typing
import inspect


class Annotation:
    def __init__(self, signature: inspect.Signature):
        self.signature = signature
        self.parameters = [
            param.annotation
            for param in self.signature.parameters.values()
        ]
        self.return_annotation = self.signature.return_annotation

    def __repr__(self) \
            -> str:
        return f"[{self.param_type}] -> {self.return_type}"
        
    def __str__(self) \
            -> str:
        return f"[{self.param_type}] -> {self.return_type}"

    @property
    def param_type(self) \
            -> str:
        return ', '.join(map(self._param_str, self.parameters))

    @property
    def return_type(self) \
            -> str:
        return self._param_str(self.return_annotation)

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
        else:
            return f"{param!s}"

    @staticmethod
    def from_function(function: typing.Callable) \
            -> Annotation:
        return Annotation(inspect.signature(function))
