from __future__ import annotations
from typing import Optional, Callable, Tuple, Union, Any, Dict, List


class Argument:
    """ Arguments are evaluated by the function
    """
    ARGS_TYPE = Union[Tuple[Any, ...], List[Any]]
    KWARGS_TYPE = Dict[str, Any]
    RETURN_TYPE = Tuple[ARGS_TYPE, KWARGS_TYPE]
    TYPE = Tuple[Optional[ARGS_TYPE], Optional[KWARGS_TYPE]]

    def __init__(self, *args, **kwargs):
        self.args: Argument.ARGS_TYPE = args
        self.kwargs: Argument.KWARGS_TYPE = kwargs

    def __repr__(self):
        return f'{self.__class__.__name__}({self.args}, {self.kwargs})'

    @staticmethod
    def from_result(result: Union[Any, Argument.TYPE]) \
            -> Argument:
        """ Return an Argument from a function result.

        To prevent unintentional generator evaluation, 
        explicitly convert to argument only when the argument is an Argument.TYPE.

        :param result: The result of a function evaluation.
        
        :return: The result as an Argument.
        """

        if (isinstance(result, list) or isinstance(result, tuple)) and \
                len(result) == 2 and (result[-1] is None or isinstance(result[-1], dict)):
            args, kwargs = result

            if not kwargs:
                kwargs = dict()

        elif not isinstance(result, Argument):
            args, kwargs = (result, ), dict()

        else:
            return result

        return Argument(*args, **kwargs)

    @property
    def value(self) \
            -> Any:
        """ Return the value of the argument.
        """
        if not self.kwargs and self.args:
            return self.args[0]

        if not self.args and self.kwargs and len(self.kwargs.keys()) == 1:
            return self.kwargs.get(tuple(self.kwargs.keys())[0])

        return None

    @property
    def arg(self) \
            -> Argument.RETURN_TYPE:
        """ Return the argument.
        """
        return self.args, self.kwargs

    def evaluate(self, function: Callable[[Argument.TYPE], Any]) \
            -> Argument:
        """ Evaluate the argument with a function.
        """

        result = function(*self.args, **self.kwargs)
        return Argument.from_result(result)
