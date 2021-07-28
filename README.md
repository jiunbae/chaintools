# chaintools

## Function chaining

> `chaintools.Function` 를 활용해 함수를 연결하는 할 수 있다.

```python
from chaintools import Function as F
from chaintools import Argument


def add(tar: int) -> Callable[[int], int]:
    def _wrapper(src: int) -> int:
        return src + tar
    return _wrapper

# F = int -> int -> int -> int
f = F >> add(1) >> add(2)
assert f(3) == 6
```

> 함수의 반환 형태가 `Tuple[Tuple[Any, ...], Dict[str, Any]]` 형태일때 다음 함수의 `*args, **kwargs`에 값을 넣어줄 수 있다.

```python
def return_args_and_kwargs() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    return (1, 2), {'c': 1, 'd': 2}

def add_four_variable(a, b, c, d) -> int:
    return a + b + c + d

# F = None -> Tuple[Tuple[Any, ...], Dict[str, Any]] -> int
f = F >> return_args_and_kwargs >> add_four_variable
assert f() == 6
```

> 또는 함수 사이에 `F.spread`를 활용해서 `Iterable`형태의 결과값을 다음 함수의 `*args` 형태로 전달할 수 있습니다.

```python
def return_args() -> Iterable[int]:
    return 1, 2

def return_args_as_argument() -> Argument.TYPE:
    return (1, 2), None

def add_two_variable(a, b) -> int:
    return a + b

# F = None -> Iterable[int] -> [int, ...] -> int
f = F >> return_args >> F.spread() >> add_two_variable
g = F >> return_args_as_argument >> add_two_variable
assert f() == g() == 3
```
