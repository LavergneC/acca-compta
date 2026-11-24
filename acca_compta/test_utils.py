import itertools
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from django.test import Client

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Generator

T = TypeVar("T")


class _Auto:
    """Sentinel value indicating an automatic default will be used."""

    def __bool__(self) -> bool:
        # Allow `Auto` to be used like `None` or `False` in boolean expressions
        return False


Auto: Any = _Auto()


def create_batch[T](factory: Callable[..., T], count, /, **kwargs) -> list[T]:
    """Use `factory` callable to create `count` objects, passing along kwargs."""
    return [factory(**kwargs) for i in range(count)]


def sequence[T](func: Callable[[int], T]) -> Generator[T]:
    """Generates a sequence of values from a sequence of integers.

    Starting at zero and passed through the callable which must take an integer argument
    """
    return (func(n) for n in itertools.count())


class HtmxClient(Client):
    def htmx_get(self, url, **kwargs):
        return self.get(url, **{"HTTP_HX-Request": "true"}, **kwargs)

    def htmx_post(self, url, **kwargs):
        return self.post(url, **{"HTTP_HX-Request": "true"}, **kwargs)
