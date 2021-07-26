from typing import Callable, Any
from pydoc import locate
import inspect
import typing


class MetaType(type):
    """ Type checking metaclass
    """
    def __getattr__(cls, key: str) \
            -> Callable[[Any], Any]:
        """ getattr implementation
        """

        def is_type_check(obj: Any) \
                -> bool:
            """ check if obj is of type
            """
            key_ = key[3:]
            base_type = getattr(typing, key_.capitalize(), None)
            if base_type is None:
                base_type = getattr(typing, key_, None)

            # TODO: none assertion is not safe
            if key_.lower() == "none":
                return obj is None

            if base_type is None:
                return key_ in map(lambda x: x.__name__, inspect.getmro(type(obj)))

            return isinstance(obj, base_type)

        def to_type_check(obj: Any) \
                -> Any:
            """ check if obj is of type
            """
            key_ = key[3:]

            # TODO: none assertion is not safe
            if key_.lower() == "none":
                return None

            base_type = locate(key_)
            if isinstance(base_type, type):
                return base_type(obj)
            return None

        if key.startswith('is_'):
            return is_type_check

        if key.startswith('to_'):
            return to_type_check

        raise AttributeError(f"{cls.__name__} has no attribute '{key}'")
