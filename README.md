# chaintools


## Function map, filter

> `Function.map`과 `Function.filter`를 사용해서 데이터를 처리할 수 있다.
```python
from chaintools import Function as F

def to_float(a):
    return float(a)
    
def to_str(a):
    return str(a)

f = F >> to_float >> to_str
result = f.map(range(10))
assert tuple(result) == tuple(map(to_str, map(to_float, range(10))))
```

```python
from chaintools import Function as F

def is_even(a):
    return a % 2 == 0

def is_not_zero(a):
    return a != 0

f = F >> is_even >> is_not_zero
result = f.filter(range(10))
assert tuple(result) == tuple(filter(is_not_zero, filter(is_even, range(10))))
```

## Function chaining

> `Function` 를 활용해 함수를 연결하는 할 수 있다.

```python
from chaintools import Function as F

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

def return_args_as_argument() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    return (1, 2), None

def add_two_variable(a, b) -> int:
    return a + b

# F = None -> Iterable[int] -> [int, ...] -> int
f = F >> return_args >> F.spread() >> add_two_variable
# g = None -> Tuple[Tuple[Any, ...], Dict[str, Any]] -> [int, ...] -> int
g = F >> return_args_as_argument >> add_two_variable
assert f() == g() == 3
```
