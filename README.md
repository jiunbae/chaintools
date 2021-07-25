# chaintools

## Function chaining

> `chaintools.F` 를 활용해 함수를 연결하는 할 수 있다.

```python
def add(a: int, b: int) -> int:
    return a + b

def sub(a: int, b: int) -> int:
    return a - b

f = F >> add >> F.duplicate() >> sub
assert f(1, 2) == 0
```

> 함수의 반환 형태가 `Tuple[Tuple, Dict[str, Any]]` 형태일때 다음 함수의 `*args, **kwargs`에 값을 넣어줄 수 있다.

```python
def function1() -> Tuple[Tuple, Dict[str, Any]]:
    return (1, 2), {'c': 1, 'd': 2}

def function2(a, b, c, d) -> int:
    return a + b + c + d

f = F >> function1 >> function2
assert f() == 6
```