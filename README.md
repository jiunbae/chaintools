# chaintools

## Function chaining

> `chaintools.F` 를 활용해 함수를 연결하는 할 수 있다.

```python
def add(tar: int) -> Callable[[int], int]:
    def _wrapper(src: int) -> int:
        return src + tar
    return _wrapper

f = F >> add(1) >> add(2)
assert f(3) == 6
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