from pydoc import locate
import inspect
import typing
from functools import partial


def is_type_check(obj: typing.Any, key: str) \
        -> bool:
    """ check if obj is of type
    """
    base_type = getattr(typing, key.capitalize(), None)

    if base_type is None:
        base_type = getattr(typing, key, None)

    if key.lower() == "none":
        return obj is None

    if base_type is None:
        return key in map(
            lambda mro: mro.__name__,
            inspect.getmro(type(obj)),
        )

    return isinstance(obj, base_type)


def to_type_cast(obj: typing.Any, key: str) \
        -> typing.Any:
    """ check if obj is of type
    """
    if key.lower() == "none":
        return None

    base_type = locate(key)

    if isinstance(base_type, type):
        return base_type(obj)

    return None


class Typeable(type):
    """ Typeable class
    """
    GETATTR_MAPPING = {
        'is_': is_type_check,
        'to_': to_type_cast,
    }

    @classmethod
    def mapping_handler(cls, key) \
            -> typing.Callable:

        for mapping_key, mapping in cls.GETATTR_MAPPING.items():
            if key.startswith(mapping_key):
                return partial(mapping, key=key[len(mapping_key):])

        return None

    def __getattr__(cls, key: str) \
            -> typing.Callable:
        """ getattr implementation
        """
        mapping = Typeable.mapping_handler(key)
        if mapping is None:
            return cls.__getattribute__(key)

        return mapping
