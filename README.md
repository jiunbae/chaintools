# chaintools


## Function chaining

> `Function` 를 활용해 함수를 연결 할 수 있습니다.

```python
from chaintools import Function as F

def add(tar: int) -> Callable[[int], int]:
    def _wrapper(src: int) -> int:
        return src + tar
    return _wrapper

# f = int -> int -> int -> int
f = F >> add(1) >> add(2)
assert f(3) == 6
```

> 함수의 반환 형태가 `Tuple[Tuple[Any, ...], Dict[str, Any]]` 형태일 때는 특수한 `Argument.TYPE`으로 여겨지며, 다음 함수 인자에 `*args, **kwargs`와 같은 형태로 전달할 수 있습니다.

```python
from chaintools import Argument

def return_args_and_kwargs() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    return (1, 2), {'c': 1, 'd': 2}

def add_four_variable(a, b, c, d) -> int:
    return a + b + c + d

# f = None -> Tuple[Tuple[Any, ...], Dict[str, Any]](Argument.TYPE) -> int
f = F >> return_args_and_kwargs >> add_four_variable
assert f() == 6
```

> 또는 함수 사이에 `Function.spread`를 활용해서 `Iterable`형태의 결과 값을 다음 함수의 `*args` 형태로 전달할 수 있습니다.

```python
def return_args() -> Iterable[int]:
    return 1, 2

def return_args_as_argument() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    return (1, 2), None

def add_two_variable(a, b) -> int:
    return a + b

# f = None -> Iterable[int] -> [int, ...] -> int
f = F >> return_args >> F.spread() >> add_two_variable
# g = None -> Tuple[Tuple[Any, ...], Dict[str, Any]]([int, ...]) -> int
g = F >> return_args_as_argument >> add_two_variable
assert f() == g() == 3
```

## Function map, filter

> `Function.map`과 `Function.filter`를 사용해서 데이터를 처리할 수 있습니다.
```python
def to_float(a):
    return float(a)

def to_str(a):
    return str(a)

# f = Any -> float -> str
f = F >> to_float >> to_str
result = f.map(range(10))
assert tuple(result) == tuple(map(to_str, map(to_float, range(10))))
```

```python
def is_even(a):
    return a % 2 == 0

def is_not_zero(a):
    return a != 0

# f = Any -> bool -> bool
f = F >> is_even >> is_not_zero
result = f.filter(range(10))
assert tuple(result) == tuple(filter(is_not_zero, filter(is_even, range(10))))
```

> `Function.map`와 `Function.filter`도 함수이기 때문에 chaining 할 수 있습니다. (단, 형태가 `Iterable -> Iterable`이어야 합니다. 즉 일반적인 `Any -> Any` 형태의 함수와 `Iterable -> Iterable`형태의 함수는 함께 사용할 수 없습니다.)

```python
# f = Iterable[Any] -> Iterable[Any] -> Iterable[Any]
f = F >> F([add(1), to_float]).map >> F(is_even).filter >> F(add(1)).map
result = f(range(10))
assert tuple(result) == (3.0, 5.0, 7.0, 9.0, 11.0)
```


## Function annotation

> `str(Function)`을 이용해서 annotation을 확인할 수 있습니다. 만약 이전 함수의 반환 값과 다음 함수의 인자 형태가 맞지 않는다면 `{이전 함수 반환}({다음 함수 인자})`로 표시됩니다.

```python
def int_to_str(a: int) -> str:
    return str(a)

def str_to_float(a: str) -> float:
    return float(a)

def float_to_tuple(a: float) -> Tuple[int, int]:
    return (int(a), int(a))

# f = int -> str -> float -> Tuple[int, int]
f = F >> int_to_str >> str_to_float >> float_to_tuple
# g = int -> str(float) -> Tuple[int, int]
g = F >> int_to_str >> float_to_tuple
assert str(f) == "Function(int -> str -> float -> tuple[int, int])"
assert str(g) == "Function(int -> str(float) -> tuple[int, int])"
```