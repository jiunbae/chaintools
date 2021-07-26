from __future__ import annotations
from typing import Callable, Any

class Chainable(type):
    def __rshift__(cls, function: Callable)\
            -> Chainable:
        instance: Chainable = cls()
        instance = instance >> function
        return instance

    def __lshift__(cls, item: Any) \
            -> Any:
        result = cls.__call__(item)
        return result
