from typing import Callable, Generic, TypeVar

from ..type import (
    Typeable
)


class Type(metaclass=Typeable):
    """ Type is a base class
    """
    T = TypeVar('T')

    @staticmethod
    def to_(base: Generic[T], *base_args, **base_kwargs)\
            -> Callable[[], T]:
        """ Convert to a new type
        """
        def _wrapper(*args, **kwargs) \
                -> Type.T:
            return base(*args, **kwargs)
        return _wrapper

    @staticmethod
    def is_(base: Generic[T]) \
            -> Callable[[T], bool]:
        """ Check if an object is a type
        """
        def _wrapper(obj: object)\
                -> bool:
            return isinstance(obj, base)
        return _wrapper
